"""Activation patching -> the ``L_clean`` / ``L_patched`` / ``L_corrupted`` logit
differences that feed NCME, and per-component effects for circuit identification.

The interface is fixed here; the TransformerLens hook loop is wired on the M4
host. The dependency-light smoke test exercises the downstream NCME / decision
logic with synthetic logit differences instead.

**Patching direction (denoising / restoration).** We run the *corrupted* prompt
and patch the *clean* activation of ``component`` into it, then measure how far the
logit difference is restored toward the clean value. This is exactly the quantity
``NCME = (L_patched - L_corrupted) / (L_clean - L_corrupted)``: 0 = the component
carries none of the clean signal, 1 = patching it alone fully recovers the clean
behaviour. This matches the IOI name-mover validation ("patching the name-mover
heads recovers the clean logit difference"). See ``ncme.py`` and
``../../prereg/notes/p3-synthesis.md``.

``torch`` / ``transformer_lens`` are not imported at module load; the heavy stack
is touched only inside the functions, so the decision core stays import-light.

Component specification (``component``)::

    ("resid_post", layer)        # residual stream after block ``layer``
    ("attn_out", layer)          # block ``layer`` attention output (all heads)
    ("mlp_out", layer)           # block ``layer`` MLP output
    ("z", layer, head)           # single attention head's output (hook_z slice)
    ("head", layer, head)        # alias for ("z", layer, head)
    [spec, spec, ...]            # a LIST patches several components in one pass
                                 # (e.g. a whole name-mover head set = the circuit)

``pos`` selects the sequence position(s) to patch: ``-1`` (default) patches only
the final-token / prediction position — the canonical IOI direct-effect probe, and
robust to clean/corrupted length mismatch; ``None`` patches every position (clean
and corrupted must then be token-length aligned).
"""

from __future__ import annotations


def logit_diff(logits, correct_id: int, incorrect_id: int) -> float:
    """Logit difference (correct - incorrect) at the final sequence position."""
    return float(logits[0, -1, correct_id] - logits[0, -1, incorrect_id])


# --- component -> TransformerLens hook resolution -----------------------------


def _hook_name(spec) -> str:
    """Map a component spec to its TransformerLens hook point name."""
    kind = spec[0]
    layer = spec[1]
    if kind == "resid_post":
        return f"blocks.{layer}.hook_resid_post"
    if kind == "attn_out":
        return f"blocks.{layer}.hook_attn_out"
    if kind == "mlp_out":
        return f"blocks.{layer}.hook_mlp_out"
    if kind in ("z", "head"):
        return f"blocks.{layer}.attn.hook_z"
    raise ValueError(f"unknown component kind: {spec[0]!r}")


def _make_hook(spec, clean_cache, pos):
    """Build one ``(hook_name, fn)`` that writes the clean activation of ``spec``
    into the running (corrupted) activation, in place. ``pos=-1`` patches the final
    position; ``pos=None`` patches all positions; an int patches that position.
    """
    name = _hook_name(spec)
    clean_value = clean_cache[name]
    head = spec[2] if spec[0] in ("z", "head") else None

    def fn(act, hook):  # noqa: ARG001 (hook arg required by TransformerLens)
        if head is None:
            if pos is None:
                if act.shape != clean_value.shape:
                    raise ValueError(
                        f"pos=None needs aligned lengths; got {tuple(act.shape)} vs "
                        f"{tuple(clean_value.shape)} for {name}"
                    )
                act[...] = clean_value
            else:
                act[:, pos, ...] = clean_value[:, pos, ...]
        else:  # single attention head: act is (batch, pos, head, d_head)
            if pos is None:
                act[:, :, head, :] = clean_value[:, :, head, :]
            else:
                act[:, pos, head, :] = clean_value[:, pos, head, :]
        return act

    return name, fn


def _to_specs(component):
    """Normalise ``component`` to a list of specs (a list input patches jointly)."""
    return component if isinstance(component, list) else [component]


# --- core: per-trial logit differences ---------------------------------------


def _token_ids(model, item):
    return model.to_single_token(item.correct_token), model.to_single_token(item.incorrect_token)


def _prep(model, clean_item, corrupted_item):
    """Run the clean (cached) and corrupted (baseline) passes once.

    Returns ``(correct_id, incorrect_id, corr_tokens, clean_cache, l_clean,
    l_corrupted)``. The clean cache supplies every patch source; the corrupted
    tokens are re-run per component with hooks. NCME uses the CLEAN task's
    correct/incorrect tokens throughout (the corrupted prompt only supplies the
    corrupting input).
    """
    import torch

    correct_id, incorrect_id = _token_ids(model, clean_item)
    clean_tokens = model.to_tokens(clean_item.prompt)
    corr_tokens = model.to_tokens(corrupted_item.prompt)
    with torch.no_grad():
        clean_logits, clean_cache = model.run_with_cache(clean_tokens)
        corr_logits = model(corr_tokens)
    l_clean = logit_diff(clean_logits, correct_id, incorrect_id)
    l_corrupted = logit_diff(corr_logits, correct_id, incorrect_id)
    return correct_id, incorrect_id, corr_tokens, clean_cache, l_clean, l_corrupted


def _patched_diff(model, corr_tokens, clean_cache, component, correct_id, incorrect_id, pos):
    """Logit difference of the corrupted run with ``component`` patched from clean."""
    import torch

    hooks = [_make_hook(spec, clean_cache, pos) for spec in _to_specs(component)]
    with torch.no_grad():
        patched_logits = model.run_with_hooks(corr_tokens, fwd_hooks=hooks)
    return logit_diff(patched_logits, correct_id, incorrect_id)


def patched_logit_diffs(
    model, clean_item, corrupted_item, component, pos: int | None = -1
) -> tuple[float, float, float]:
    """Return ``(l_clean, l_patched, l_corrupted)`` for one trial by patching
    ``component`` (e.g. ``("resid_post", layer)`` or ``("z", layer, head)``) from
    the clean run into the corrupted run.

    ``component`` may be a list of specs to patch a whole circuit jointly. ``pos``
    selects the patched position(s); see the module docstring.
    """
    correct_id, incorrect_id, corr_tokens, clean_cache, l_clean, l_corrupted = _prep(
        model, clean_item, corrupted_item
    )
    l_patched = _patched_diff(
        model, corr_tokens, clean_cache, component, correct_id, incorrect_id, pos
    )
    return l_clean, l_patched, l_corrupted


def component_effects(model, items, components, pos: int | None = -1) -> list[list[float]]:
    """Per-component patching effect (fraction of clean logit-diff mediated),
    one row per condition. Feeds ``circuit_id.identify_shared_circuit``.

    ``items``: an iterable of ``(clean_item, corrupted_item)`` pairs, one per
    condition. ``components``: a list of component specs (the columns). Each entry
    is the single-component NCME ``(l_patched - l_corrupted)/(l_clean - l_corrupted)``
    for that condition. The clean/corrupted passes are run once per condition and
    reused across all components.
    """
    rows: list[list[float]] = []
    for clean_item, corrupted_item in items:
        correct_id, incorrect_id, corr_tokens, clean_cache, l_clean, l_corrupted = _prep(
            model, clean_item, corrupted_item
        )
        den = l_clean - l_corrupted
        row: list[float] = []
        for comp in components:
            l_patched = _patched_diff(
                model, corr_tokens, clean_cache, comp, correct_id, incorrect_id, pos
            )
            row.append((l_patched - l_corrupted) / den if den != 0 else float("nan"))
        rows.append(row)
    return rows
