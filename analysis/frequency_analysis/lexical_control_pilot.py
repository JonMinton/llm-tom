"""Lexical-control test for the residual-stream T0/T1 separation (seam 2).

The residual-stream pilot found T0/T1 linearly separable (peak L4 0.98). But T1
appends a clause introducing the ``onlooker`` entity, so some of that decode could
be lexical ("T1 is longer / has an extra name") rather than structural ("nesting
depth is represented"). This script isolates it.

For each (content, surface, validity) it builds three items:
  - **T0**    : first-order probe, no onlooker (the original unpadded condition);
  - **T1**    : nested second-order probe (introduces onlooker);
  - **T0pad** : first-order probe that ALSO introduces onlooker + a matched clause.

Then, per layer, within each fixed surface, it decodes:
  - **unmatched**  T0  vs T1   (reproduces the confounded ~0.98)
  - **matched**    T0pad vs T1 (onlooker held constant => isolates nesting)

If the matched decode stays high, nesting is represented *beyond* the lexical
confound. If it collapses toward chance, the earlier separation was largely
lexical. The drop (unmatched - matched) quantifies the lexical share.

Pythia-160m residual stream, final token, L2-normalised per layer. DRAFT stimuli;
nothing committed.

Run::

    cd analysis/frequency_analysis
    python lexical_control_pilot.py [--json out.json]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "implementation" / "src"))

from llm_tom import stimuli_content as sc  # noqa: E402
from separation_pilot import _cv_accuracy  # noqa: E402  (same directory)

SEED = 0
SURFACES = ("S0", "S1", "S2")


def _l2(X: np.ndarray) -> np.ndarray:
    return X / (np.linalg.norm(X, axis=1, keepdims=True) + 1e-9)


def _resid_final(model, prompt: str, n_layers: int) -> np.ndarray:
    import torch

    with torch.no_grad():
        _, cache = model.run_with_cache(model.to_tokens(prompt))
    return np.stack([cache["resid_post", L][0, -1].cpu().numpy() for L in range(n_layers)])


def _decode_within_surface(acts, cond, surfs, a: str, b: str, n_layers: int):
    """Per-layer mean within-surface decode of condition ``a`` vs ``b``."""
    mask = np.isin(cond, [a, b])
    out = []
    for L in range(n_layers):
        per_s = []
        for s in SURFACES:
            m = mask & (surfs == s)
            Xn = _l2(acts[m, L, :])
            y = (cond[m] == a).astype(int)
            per_s.append(_cv_accuracy(Xn, y))
        out.append((float(np.nanmean(per_s)), per_s))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", type=str, default=None)
    ap.add_argument("--model", type=str, default="pythia-160m")
    args = ap.parse_args()

    import torch
    from transformer_lens import HookedTransformer

    torch.manual_seed(SEED)
    model = HookedTransformer.from_pretrained(args.model, device="cpu")
    model.eval()
    n_layers = model.cfg.n_layers

    prompts, cond, surfs = [], [], []
    for c in sc.ALL_CONTENTS:
        for s in SURFACES:
            for v in ("valid", "invalid"):
                prompts.append(sc.render(c, s, "T0", v).prompt); cond.append("T0"); surfs.append(s)
                prompts.append(sc.render(c, s, "T1", v).prompt); cond.append("T1"); surfs.append(s)
                prompts.append(sc.render_t0_padded(c, s, v).prompt); cond.append("T0pad"); surfs.append(s)
    cond, surfs = np.array(cond), np.array(surfs)
    print(f"extracting resid_post[final] for {len(prompts)} items x {n_layers} layers ...", flush=True)
    acts = np.stack([_resid_final(model, p, n_layers) for p in prompts])

    unmatched = _decode_within_surface(acts, cond, surfs, "T1", "T0", n_layers)
    matched = _decode_within_surface(acts, cond, surfs, "T1", "T0pad", n_layers)

    print("\nlayer | unmatched (T0 vs T1) | matched (T0pad vs T1) | lexical share")
    print("------+----------------------+-----------------------+--------------")
    per_layer = []
    for L in range(n_layers):
        um, mm = unmatched[L][0], matched[L][0]
        share = (um - mm) / (um - 0.5) if um > 0.5 else float("nan")
        per_layer.append({"layer": L, "unmatched": um, "matched": mm, "lexical_share": share})
        print(f"  L{L:<2} | {um:.3f}                | {mm:.3f}                 | {share:+.2f}")

    peak_m = max(per_layer, key=lambda r: r["matched"])
    print(f"\npeak MATCHED (T0pad vs T1) decode: L{peak_m['layer']} = {peak_m['matched']:.3f} "
          f"(unmatched there {peak_m['unmatched']:.3f})")
    verdict = (
        f"nesting survives the lexical control (matched peak {peak_m['matched']:.2f}) "
        f"-> genuine structural signal, not just length/entity"
        if peak_m["matched"] >= 0.70 else
        f"matched decode collapses (peak {peak_m['matched']:.2f}) -> the T0/T1 separation "
        f"was largely LEXICAL; structure must be strengthened (deeper T1) to be detectable"
    )
    print("interpretation (PILOT):", verdict)

    if args.json:
        Path(args.json).write_text(json.dumps(
            {"model": args.model, "per_layer": per_layer,
             "peak_matched_layer": peak_m["layer"], "peak_matched": peak_m["matched"]}, indent=2))
        print(f"\nwrote {args.json}")


if __name__ == "__main__":
    main()
