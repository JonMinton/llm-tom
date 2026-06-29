"""Activation patching -> the ``L_clean`` / ``L_patched`` / ``L_corrupted`` logit
differences that feed NCME, and per-component effects for circuit identification.

The interface is fixed here; the TransformerLens hook loop is wired on the M4
host. The dependency-light smoke test exercises the downstream NCME / decision
logic with synthetic logit differences instead.
"""

from __future__ import annotations


def logit_diff(logits, correct_id: int, incorrect_id: int) -> float:
    """Logit difference (correct - incorrect) at the final sequence position."""
    return float(logits[0, -1, correct_id] - logits[0, -1, incorrect_id])


def patched_logit_diffs(model, clean_item, corrupted_item, component) -> tuple[float, float, float]:
    """Return ``(l_clean, l_patched, l_corrupted)`` for one trial by patching
    ``component`` (e.g. ``("resid_post", layer)`` or an attention head) from the
    clean run into the corrupted run.

    Implemented on the pilot host with TransformerLens hooks; raises here so the
    smoke test uses the synthetic mock in ``tests/``.
    """
    raise NotImplementedError("Wire to TransformerLens hooks on the M4 pilot host.")


def component_effects(model, items, components) -> "list[list[float]]":
    """Per-component patching effect (fraction of clean logit-diff mediated),
    one row per condition. Feeds ``circuit_id.identify_shared_circuit``. Wired on host.
    """
    raise NotImplementedError("Wire to TransformerLens hooks on the M4 pilot host.")
