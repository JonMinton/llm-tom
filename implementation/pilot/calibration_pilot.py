"""Calibration pilot — SD_pilot at scale + encoding-gate α on real draft stimuli.

The M4 pilot calibrated ``SD_pilot`` on only 24 IOI pairs (= 0.0204) and ran the
encoding gate on 45 known-good strings. This script does the larger, more careful
calibration the pilot note flagged ("the real calibration set should be larger"),
on the now-existing DRAFT stimuli. **Still PROVISIONAL — calibration only, no value
committed to ``config.py``; no scientific claim.**

Two parts:

1. **SD_pilot, n-aware.** ``SD_pilot`` is the bootstrap SD of the *aggregate* NCME
   (a ratio of means) on the known-good IOI name-mover circuit, so it shrinks
   ~``σ_trial / √n``. The transferable, n-independent quantity is the **per-trial
   NCME SD σ_trial**; ``SD_pilot(n)`` then follows for whatever n the confirmatory
   run uses, and the ROPE (= ``rope_sd_multiple · SD_pilot``) inherits that n. We
   estimate σ_trial on a larger IOI set and show ``SD_pilot(n)`` vs ``σ_trial/√n``.
   **Design note surfaced:** tying the ROPE to SD_pilot means the confirmatory n
   must be fixed *before* the ROPE is meaningful — calibrate at that n.

2. **Encoding-gate α on the DRAFT stimuli**, by surface. The early-layer [2,4]
   probe decodes surface form; we report the α distribution per surface on the
   real S0/S1/S2 stimuli (incl. S2 logical notation, the weak surface from the
   separation pilots — seam 1). NB a SPEC/PILOT discrepancy is flagged inline: the
   synthesis spec gates on the decoded *surface ground-truth fact*; the pilot (and
   this) decode *surface form*. Resolving that is a separate gate-semantics task.

Run::

    cd implementation
    python pilot/calibration_pilot.py [--n-ioi 120] [--json out.json]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parent))           # m4_pilot
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))  # llm_tom

from llm_tom import encoding_gate, sd_pilot, stimuli_content  # noqa: E402
from llm_tom.config import RunConfig  # noqa: E402
from m4_pilot import make_ioi_pairs, step1_ioi_validation  # noqa: E402

SEED = 0


def calibrate_sd_pilot(model, n_ioi: int) -> dict:
    pairs = make_ioi_pairs(model, n_pairs=n_ioi)
    _, mover_set, num, den = step1_ioi_validation(model, pairs)
    per_pair = num / den
    sigma_trial = float(np.std(per_pair, ddof=1))
    agg_ncme = float(np.mean(num) / np.mean(den))

    print(f"\n  n_ioi={n_ioi}  aggregate NCME={agg_ncme:.3f}  "
          f"per-trial NCME SD σ_trial={sigma_trial:.4f}")
    print("  SD_pilot(n) vs σ_trial/√n (should track):")
    grid = sorted({nn for nn in (24, 48, 96, n_ioi) if nn <= n_ioi})
    sd_by_n = {}
    for nn in grid:
        sd = sd_pilot.bootstrap_ncme_sd(num[:nn], den[:nn], n_boot=1000, seed=SEED)
        sd_by_n[nn] = float(sd)
        print(f"    n={nn:>4}: SD_pilot={sd:.4f}   σ_trial/√n={sigma_trial/np.sqrt(nn):.4f}")

    # n needed for a couple of target ROPE half-widths (rope = 1.0·SD_pilot here)
    targets = {t: int(np.ceil((sigma_trial / t) ** 2)) for t in (0.02, 0.01, 0.005)}
    print("  n required for SD_pilot ≤ target (≈ (σ_trial/target)²):")
    for t, n_req in targets.items():
        print(f"    target {t:.3f}: n ≈ {n_req}")
    return {
        "n_ioi": n_ioi, "sigma_trial": sigma_trial, "aggregate_ncme": agg_ncme,
        "sd_pilot_by_n": sd_by_n, "mover_set": [[ly, h] for (_, ly, h) in mover_set],
        "n_required_for_target_sd": targets,
    }


def calibrate_encoding_gate(model, cfg: RunConfig) -> dict:
    lo, hi = cfg.early_gate_layers
    items = stimuli_content.draft_items()
    feats, surf = [], []
    with torch.no_grad():
        for it in items:
            _, cache = model.run_with_cache(model.to_tokens(it.prompt))
            feats.append(np.concatenate(
                [cache["resid_post", L][0, -1].cpu().numpy() for L in range(lo, hi + 1)]))
            surf.append(it.surface)
    feats, surf = np.array(feats), np.array(surf)
    alpha = encoding_gate.surface_decode_confidence(feats, surf, seed=SEED, cv=5)
    part = encoding_gate.partition(
        alpha, pass_threshold=cfg.thresholds.encoding_gate_pass,
        fail_threshold=cfg.thresholds.encoding_gate_fail)

    print(f"\n  encoding-gate α on {len(items)} DRAFT stimuli (early layers [{lo},{hi}], "
          f"decoding SURFACE FORM):")
    by_surface = {}
    for s in ("S0", "S1", "S2"):
        m = surf == s
        by_surface[s] = {"alpha_mean": float(alpha[m].mean()), "alpha_min": float(alpha[m].min())}
        print(f"    {s}: α mean={alpha[m].mean():.3f} min={alpha[m].min():.3f}")
    print(f"    overall: α mean={alpha.mean():.3f}  T_parsed={int(part.parsed.sum())}/{len(alpha)}"
          f"  ambiguous={int(part.ambiguous.sum())}  unparsed={int(part.unparsed.sum())}"
          f"  [0.90/0.95 PROVISIONAL]")
    print("    NB spec gates on the surface-GROUND-TRUTH fact, not surface form — discrepancy flagged.")
    return {
        "early_gate_layers": [lo, hi], "alpha_overall_mean": float(alpha.mean()),
        "by_surface": by_surface, "n_parsed": int(part.parsed.sum()), "n_total": int(len(alpha)),
        "decode_target": "surface_form (PILOT) — spec wants surface_ground_truth_fact",
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-ioi", type=int, default=120)
    ap.add_argument("--json", type=str, default=None)
    args = ap.parse_args()

    torch.manual_seed(SEED)
    np.random.seed(SEED)
    from transformer_lens import HookedTransformer

    cfg = RunConfig()
    print(f"loading {cfg.model_name} (CPU) for calibration ...", flush=True)
    model = HookedTransformer.from_pretrained(cfg.model_name, device="cpu")
    model.eval()

    print("\n[1] SD_pilot calibration (n-aware, on the IOI known-good circuit)")
    sd = calibrate_sd_pilot(model, args.n_ioi)
    print("\n[2] encoding-gate α calibration (on real DRAFT stimuli, by surface)")
    gate = calibrate_encoding_gate(model, cfg)

    if args.json:
        Path(args.json).write_text(json.dumps(
            {"model": cfg.model_name, "thresholds_status": "ALL PROVISIONAL — not committed",
             "sd_pilot_calibration": sd, "encoding_gate_calibration": gate}, indent=2))
        print(f"\nwrote {args.json}")


if __name__ == "__main__":
    main()
