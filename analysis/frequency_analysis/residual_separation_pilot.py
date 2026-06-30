"""Residual-stream separation pilot — the FAITHFUL instrument for the S/T check.

The sentence-embedding pilot (``separation_pilot.py``) found surface separable but
structure (T0/T1) not — in an ``all-MiniLM-L6-v2`` *semantic* proxy. That is the
wrong space: the design's structural signal lives in the **target model's residual
stream**, where activation patching reads it. This script reruns the exact same
separation metrics on **Pythia-160m's ``resid_post`` at the final token, per
layer** — answering: *at which layer, if any, does T0-vs-T1 become linearly
separable within a fixed surface?*

Linear-probing lens, essentially. Strong within-surface T decoding at some layer
=> structure is encoded independently of surface in the target model (the S×T
decomposition is non-degenerate in the right instrument), even though the semantic
proxy could not see it. Flat-at-chance across all layers (at this DRAFT's T1
depth-2) => evidence the structural contrast must be deepened (spec: 4+ levels).

Vectors are L2-normalised per layer so the cosine perturbation and the decoding
are comparable across layers and with the MiniLM pilot. DRAFT stimuli; T2 deferred;
nothing here commits a PROVISIONAL threshold.

Run::

    cd analysis/frequency_analysis
    python residual_separation_pilot.py            # ~10 s on an idle M4 (CPU)
    python residual_separation_pilot.py --json out.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "implementation" / "src"))

from llm_tom import stimuli_content  # noqa: E402
from separation_pilot import axis_perturbations, decoding  # noqa: E402  (same directory)

SEED = 0


def _l2(X: np.ndarray) -> np.ndarray:
    return X / (np.linalg.norm(X, axis=1, keepdims=True) + 1e-9)


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

    items = stimuli_content.draft_items()
    print(f"extracting resid_post[final] for {len(items)} items x {n_layers} layers "
          f"({args.model}, CPU) ...", flush=True)

    acts = []  # per item: (n_layers, d_model)
    with torch.no_grad():
        for it in items:
            _, cache = model.run_with_cache(model.to_tokens(it.prompt))
            acts.append(np.stack(
                [cache["resid_post", L][0, -1].cpu().numpy() for L in range(n_layers)]))
    acts = np.stack(acts)  # (n_items, n_layers, d_model)
    keys = [(it.item_id.rsplit("-", 3)[0], it.surface, it.structural, it.validity) for it in items]

    print("\nlayer | dS     dT     dV   | surf  dom  | T0/T1 within-surface (chance .50)")
    print("------+--------------------+------------+----------------------------------")
    per_layer = []
    for L in range(n_layers):
        Xn = _l2(acts[:, L, :])
        emb = {keys[i]: Xn[i] for i in range(len(items))}
        pert = axis_perturbations(emb)
        dec = decoding(items, Xn)
        per_layer.append({"layer": L, "perturbation": pert, "decoding": dec})
        tw = dec["T_within_surface"]
        print(f"  L{L:<2} | {pert['delta_S']:.3f}  {pert['delta_T']:.3f}  {pert['delta_V']:.3f} |"
              f" {dec['surface_decode_acc']:.2f}  {dec['domain_decode_acc']:.2f} |"
              f" mean {dec['T_within_surface_mean']:.2f}  "
              f"(S0 {tw['S0']:.2f} S1 {tw['S1']:.2f} S2 {tw['S2']:.2f})")

    best = max(per_layer, key=lambda r: (r["decoding"]["T_within_surface_mean"]
                                         if r["decoding"]["T_within_surface_mean"] == r["decoding"]["T_within_surface_mean"]
                                         else -1))
    bm = best["decoding"]["T_within_surface_mean"]
    print(f"\npeak within-surface T0/T1 decode: L{best['layer']} = {bm:.3f}")
    verdict = (
        f"structure becomes linearly separable in the residual stream (peak L{best['layer']} "
        f"{bm:.2f}) -> S×T non-degenerate in the faithful instrument"
        if bm >= 0.70 else
        f"structure NOT linearly separable at any layer (peak {bm:.2f}) even in the residual "
        f"stream -> at DRAFT T1 depth-2 the contrast is too weak; deepen T1 (spec: 4+ levels)"
    )
    print("interpretation (PILOT):", verdict)
    print("NB: absolute σ(x) vs the locked reference corpus remains deferred.")

    if args.json:
        Path(args.json).write_text(json.dumps(
            {"model": args.model, "n_layers": n_layers, "n_items": len(items),
             "per_layer": per_layer, "peak_T_layer": best["layer"], "peak_T_mean": bm}, indent=2))
        print(f"\nwrote {args.json}")


if __name__ == "__main__":
    main()
