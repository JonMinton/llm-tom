"""M4 pilot driver — pipeline validation on Pythia-160m (NOT a scientific run).

Exercises the model-coupled patching path and the decision core end-to-end on
real activations, in four steps:

  1. IOI patching validation (known-good circuit). Builds matched clean/corrupted
     IOI pairs (subject-swap corruption), confirms the denoising plumbing
     (resid_post[final] @END NCME == 1.0), sweeps resid_post by layer and every
     attention head to locate Pythia-160m's empirical name movers, and confirms
     that patching the name-mover head set recovers the clean logit difference.
  2. SD_pilot calibration. Bootstraps the NCME standard deviation on that
     name-mover circuit (``sd_pilot.bootstrap_ncme_sd``).
  3. Encoding-gate alpha calibration on known-good stimuli (same logical content
     in three surface forms): confirms the early-layer probe encodes surface and
     the PROVISIONAL 0.95 pass threshold is satisfiable.
  4. End-to-end ``pipeline.run_recursive_probe`` on the placeholder 3x3x2 factorial
     with real activations — a plumbing test; its verdict is not meaningful.

ALL numeric thresholds remain PROVISIONAL (``config.py``); this script calibrates,
it does not commit values. Deterministic given the seed; runs on CPU.

Run::

    cd implementation
    python pilot/m4_pilot.py            # full run (~2-3 min on an M-series Mac, CPU)
    python pilot/m4_pilot.py --json out.json
"""

from __future__ import annotations

import argparse
import json

# Make ``llm_tom`` importable when run as a plain script (mirrors pytest's pythonpath=src).
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from llm_tom import encoding_gate, patching, sd_pilot, stimuli  # noqa: E402
from llm_tom.config import RunConfig  # noqa: E402
from llm_tom.lipschitz import support_sparsity  # noqa: E402
from llm_tom.pipeline import run_recursive_probe  # noqa: E402

SEED = 0
DEVICE = "cpu"  # CPU for determinism (validation criterion 3)

NAMES = ["John", "Mary", "Tom", "James", "Anna", "Mark", "Paul", "Kevin",
         "Lisa", "Sarah", "David", "Susan", "Mike", "Laura", "Peter", "Emma"]
OBJECTS = ["drink", "book", "ball", "ring"]
PLACES = ["store", "park", "school", "office"]
IOI_TEMPLATE = "When{io} and{s} went to the {place},{giver} gave a {obj} to"
T_INDEX = {"T0": 0, "T1": 1, "T2": 2}


@dataclass
class Item:
    prompt: str
    correct_token: str
    incorrect_token: str


def ncme(l_clean, l_patched, l_corrupted):
    return (l_patched - l_corrupted) / (l_clean - l_corrupted)


def single_token(model, name: str) -> bool:
    return len(model.to_tokens(" " + name, prepend_bos=False)[0]) == 1


def make_ioi_pairs(model, n_pairs: int, seed: int = SEED):
    """Matched clean/corrupted IOI pairs; corruption swaps the giver name (subject),
    flipping the answer while preserving token length."""
    rng = np.random.default_rng(seed)
    names = [n for n in NAMES if single_token(model, n)]
    pairs, seen = [], set()
    while len(pairs) < n_pairs:
        io, s = rng.choice(names, size=2, replace=False)
        obj, place = rng.choice(OBJECTS), rng.choice(PLACES)
        key = (io, s, obj, place)
        if key in seen:
            continue
        seen.add(key)
        clean = Item(
            IOI_TEMPLATE.format(io=f" {io}", s=f" {s}", place=place, giver=f" {s}", obj=obj),
            f" {io}", f" {s}",
        )
        corrupt = Item(
            IOI_TEMPLATE.format(io=f" {io}", s=f" {s}", place=place, giver=f" {io}", obj=obj),
            f" {io}", f" {s}",
        )
        pairs.append((clean, corrupt))
    return pairs


def step1_ioi_validation(model, pairs):
    n_layers, n_heads = model.cfg.n_layers, model.cfg.n_heads

    # baselines + plumbing check (resid_post[final] @END must give NCME == 1.0)
    l_clean, l_corr, final_ncme = [], [], []
    for clean, corrupt in pairs:
        lc, lp, lcorr = patching.patched_logit_diffs(
            model, clean, corrupt, ("resid_post", n_layers - 1), pos=-1
        )
        l_clean.append(lc)
        l_corr.append(lcorr)
        final_ncme.append(ncme(lc, lp, lcorr))
    l_clean, l_corr, final_ncme = map(np.array, (l_clean, l_corr, final_ncme))
    print(f"  l_clean mean={l_clean.mean():+.3f}  l_corrupted mean={l_corr.mean():+.3f}")
    print(f"  plumbing: resid_post[final] @END NCME mean={final_ncme.mean():.4f} (expect 1.0)")

    # resid_post layer sweep (recovery curve)
    layer_curve = []
    for layer in range(n_layers):
        vals = [ncme(*_lp(model, c, k, ("resid_post", layer))) for c, k in pairs[:12]]
        layer_curve.append(float(np.mean(vals)))
    print("  resid_post layer sweep (mean NCME @END): "
          + " ".join(f"L{i}:{v:+.2f}" for i, v in enumerate(layer_curve)))

    # per-head z sweep -> name movers
    head_specs = [("z", layer, head) for layer in range(n_layers) for head in range(n_heads)]
    eff = np.array(patching.component_effects(model, pairs[:10], head_specs, pos=-1))
    head_ncme = eff.mean(axis=0).reshape(n_layers, n_heads)
    flat = sorted(
        (((layer, head), float(head_ncme[layer, head]))
         for layer in range(n_layers) for head in range(n_heads)),
        key=lambda kv: kv[1], reverse=True,
    )
    print("  top name-mover heads: "
          + ", ".join(f"L{ly}H{h}:{v:+.2f}" for (ly, h), v in flat[:6]))
    mover_set = [("z", ly, h) for (ly, h), v in flat if v >= 0.05][:6]

    # patch the name-mover set jointly -> recovery + the num/den for SD_pilot
    num, den, set_ncme = [], [], []
    for clean, corrupt in pairs:
        lc, lp, lcorr = patching.patched_logit_diffs(model, clean, corrupt, mover_set, pos=-1)
        num.append(lp - lcorr)
        den.append(lc - lcorr)
        set_ncme.append(ncme(lc, lp, lcorr))
    num, den, set_ncme = map(np.array, (num, den, set_ncme))
    # control: an equal-size set of layer-0 heads should recover ~0
    early_set = [("z", 0, h) for h in range(len(mover_set))]
    ctrl = np.array([ncme(*_lp(model, c, k, early_set)) for c, k in pairs])
    print(f"  name-mover set {[(ly, h) for (_, ly, h) in mover_set]} "
          f"joint NCME={set_ncme.mean():.3f} | layer-0 control={ctrl.mean():.3f}")

    return {
        "l_clean_mean": float(l_clean.mean()),
        "l_corrupted_mean": float(l_corr.mean()),
        "plumbing_final_ncme": float(final_ncme.mean()),
        "resid_layer_sweep": layer_curve,
        "top_heads": [{"layer": ly, "head": h, "ncme": v} for (ly, h), v in flat[:6]],
        "name_mover_set": [[ly, h] for (_, ly, h) in mover_set],
        "mover_set_ncme_mean": float(set_ncme.mean()),
        "mover_set_ncme_sd": float(set_ncme.std(ddof=1)),
        "control_layer0_ncme": float(ctrl.mean()),
    }, mover_set, num, den


def _lp(model, clean, corrupt, component):
    """Convenience: (l_clean, l_patched, l_corrupted) for one pair + component."""
    return patching.patched_logit_diffs(model, clean, corrupt, component, pos=-1)


def step2_sd_pilot(num, den):
    sd = sd_pilot.bootstrap_ncme_sd(num, den, n_boot=1000, seed=SEED)
    sd2 = sd_pilot.bootstrap_ncme_sd(num, den, n_boot=1000, seed=SEED)
    print(f"  SD_pilot (bootstrap NCME sd on IOI circuit) = {sd:.4f} "
          f"(deterministic={sd == sd2})  [PROVISIONAL]")
    return {"sd_pilot": float(sd), "deterministic": bool(sd == sd2)}


def step3_encoding_gate(model, cfg):
    lo, hi = cfg.early_gate_layers
    pairs = [("Mary", "John"), ("Anna", "Mark"), ("Lisa", "Paul"), ("Emma", "Peter"),
             ("Laura", "Kevin"), ("Susan", "David"), ("Sarah", "Mike"), ("Mary", "Tom"),
             ("Anna", "David"), ("Emma", "John"), ("Laura", "Paul"), ("Lisa", "Mark"),
             ("Susan", "Tom"), ("Sarah", "Kevin"), ("Emma", "Mike")]

    def render(io, s, surface):
        return {
            "S0": f"When {io} and {s} went to the store, {s} gave a drink to",
            "S1": f"agents = [{io}, {s}]; giver = {s}; recipient =",
            "S2": f"holds({s}, gives) & present({io}) -> recipient =",
        }[surface]

    feats, labels = [], []
    with torch.no_grad():
        for io, s in pairs:
            for surface in ("S0", "S1", "S2"):
                _, cache = model.run_with_cache(model.to_tokens(render(io, s, surface)))
                feats.append(np.concatenate(
                    [cache["resid_post", layer][0, -1].cpu().numpy() for layer in range(lo, hi + 1)]
                ))
                labels.append(surface)
    feats, labels = np.array(feats), np.array(labels)
    alpha = encoding_gate.surface_decode_confidence(feats, labels, seed=SEED, cv=5)
    part = encoding_gate.partition(
        alpha,
        pass_threshold=cfg.thresholds.encoding_gate_pass,
        fail_threshold=cfg.thresholds.encoding_gate_fail,
    )
    print(f"  alpha mean={alpha.mean():.3f} min={alpha.min():.3f} | "
          f"T_parsed={int(part.parsed.sum())}/{len(alpha)} "
          f"ambiguous={int(part.ambiguous.sum())} unparsed={int(part.unparsed.sum())}  "
          f"[0.90/0.95 PROVISIONAL]")
    return {
        "early_gate_layers": [lo, hi],
        "alpha_mean": float(alpha.mean()),
        "alpha_min": float(alpha.min()),
        "n_parsed": int(part.parsed.sum()),
        "n_total": int(len(alpha)),
    }


def step4_pipeline_e2e(model, mover_set, sd_num, sd_den, cfg):
    items = {(it.surface, it.structural, it.validity): it for it in stimuli.placeholder_items()}
    clean_a, patched_a, corr_a, t_idx, s_lab = [], [], [], [], []
    for s in ("S0", "S1", "S2"):
        for t in ("T0", "T1", "T2"):
            v, iv = items[(s, t, "valid")], items[(s, t, "invalid")]
            clean = Item(v.prompt, v.correct_token, v.incorrect_token)
            corrupt = Item(iv.prompt, v.correct_token, v.incorrect_token)
            lc, lp, lcorr = patching.patched_logit_diffs(model, clean, corrupt, mover_set, pos=-1)
            clean_a.append(lc)
            patched_a.append(lp)
            corr_a.append(lcorr)
            t_idx.append(T_INDEX[t])
            s_lab.append(s)
    clean_a, patched_a, corr_a = map(np.array, (clean_a, patched_a, corr_a))
    ncme_cells = ncme(clean_a, patched_a, corr_a)

    # T-axis slope at fixed S=S0 (OLS)
    s0 = [i for i, s in enumerate(s_lab) if s == "S0"]
    x = np.array([t_idx[i] for i in s0], float)
    y = np.array([ncme_cells[i] for i in s0], float)
    xm, sxx = x.mean(), ((x - x.mean()) ** 2).sum()
    b = ((x - xm) * (y - y.mean())).sum() / sxx
    resid = y - (y.mean() - b * xm + b * x)
    se = float(np.sqrt((resid**2).sum() / (len(x) - 2) / sxx))
    slope_fit = (float(b), se, len(x) - 2)

    # support sparsity over the 9 valid cells (Lipschitz lens)
    emb = []
    with torch.no_grad():
        for s in ("S0", "S1", "S2"):
            for t in ("T0", "T1", "T2"):
                it = items[(s, t, "valid")]
                _, cache = model.run_with_cache(model.to_tokens(it.prompt))
                emb.append(cache["resid_post", model.cfg.n_layers - 1][0, -1].cpu().numpy())
    sigma = support_sparsity(np.array(emb), k=min(50, len(emb) - 1))

    trials = {"sd_num": sd_num, "sd_den": sd_den,
              "clean": clean_a, "patched": patched_a, "corrupted": corr_a}
    res = run_recursive_probe(trials, slope_fit, sigma, ncme_cells, 0.5, cfg)
    print(f"  SD_pilot={res.sd_pilot:.4f} ROPE={res.rope_halfwidth:.4f} "
          f"T-slope(S0)={slope_fit[0]:+.3f} NCME={res.ncme.point:+.3f}"
          f"[{res.ncme.lo:+.2f},{res.ncme.hi:+.2f}] "
          f"lipschitzB1={res.lipschitz_b1} falsified={res.falsified}")
    print(f"  VERDICT = {res.verdict}  (placeholder stimuli -> NOT a scientific verdict)")
    return {
        "sd_pilot": res.sd_pilot, "rope_halfwidth": res.rope_halfwidth,
        "t_slope_S0": {"est": slope_fit[0], "se": slope_fit[1], "df": slope_fit[2]},
        "ncme_point": res.ncme.point, "ncme_lo": res.ncme.lo, "ncme_hi": res.ncme.hi,
        "ncme_unbounded": res.ncme.unbounded,
        "lipschitz_b1": res.lipschitz_b1, "falsified": res.falsified, "verdict": res.verdict,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", type=str, default=None, help="optional path to write a results JSON")
    ap.add_argument("--n-pairs", type=int, default=24, help="IOI pairs for validation/SD_pilot")
    args = ap.parse_args()

    torch.manual_seed(SEED)
    np.random.seed(SEED)
    from transformer_lens import HookedTransformer

    cfg = RunConfig()
    print(f"loading {cfg.model_name} on {DEVICE} ...", flush=True)
    model = HookedTransformer.from_pretrained(cfg.model_name, device=DEVICE)
    model.eval()

    pairs = make_ioi_pairs(model, n_pairs=args.n_pairs)
    print(f"\n[1] IOI patching validation  (example: {pairs[0][0].prompt!r})")
    ioi, mover_set, num, den = step1_ioi_validation(model, pairs)
    print("\n[2] SD_pilot calibration")
    sd = step2_sd_pilot(num, den)
    print("\n[3] encoding-gate alpha calibration (known-good stimuli)")
    gate = step3_encoding_gate(model, cfg)
    print("\n[4] end-to-end run_recursive_probe on placeholder factorial (real activations)")
    e2e = step4_pipeline_e2e(model, mover_set, num, den, cfg)

    results = {
        "model": cfg.model_name, "device": DEVICE, "seed": SEED, "n_pairs": args.n_pairs,
        "thresholds_status": "ALL PROVISIONAL — calibration only, not committed",
        "ioi_validation": ioi, "sd_pilot": sd, "encoding_gate": gate, "pipeline_e2e": e2e,
    }
    if args.json:
        Path(args.json).parent.mkdir(parents=True, exist_ok=True)
        Path(args.json).write_text(json.dumps(results, indent=2))
        print(f"\nwrote {args.json}")


if __name__ == "__main__":
    main()
