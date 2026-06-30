"""Frequency-analysis PILOT: representational separation of the S and T axes.

**Status: pilot — methodology check, NOT the locked frequency analysis.** The
locked protocol (this directory's README) computes support-sparsity sigma(x)
against a 50-100 GB Dolma/RedPajama reference corpus. That absolute-novelty step
is deferred. This pilot answers the prior, corpus-free question the stress-test
raised:

    Does Surface-novelty (S) and Structural-novelty (T) move the representation
    in SEPARABLE ways, or does surface dominate and swamp structure?

The stress-test rejected the original single composite "substrate-distance" axis
precisely because it conflated surface and structural novelty. The identification
defence needs structure to be representationally present *independent of* surface.

Method: embed the DRAFT S x T x Validity grid (psychological + technical;
``llm_tom.stimuli_content.draft_items``; T2/novel deferred) with
``all-MiniLM-L6-v2`` (per CLAUDE.md), then report:

  1. Per-axis perturbation: mean cosine distance induced by varying S / T / V
     while the other factors are held constant (how far each axis moves the point).
  2. Decoding: surface (S0/S1/S2) and domain (psych/technical) recoverability, and
     -- the load-bearing test -- T0-vs-T1 decodability *within each fixed surface*.
     High within-surface T decoding => structure is encoded independently of
     surface => the S x T decomposition is non-degenerate.

This is the M4-tractable, sentence-embedding proxy; the scientific version uses
the model's own residual stream + the locked corpus. All read-only; nothing here
commits a PROVISIONAL threshold.

Run::

    cd analysis/frequency_analysis
    python separation_pilot.py            # or: python separation_pilot.py --json out.json
"""

from __future__ import annotations

import argparse
import json
import sys
from itertools import combinations
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "implementation" / "src"))

from llm_tom import stimuli_content  # noqa: E402

SEED = 0


def _cos_dist(a: np.ndarray, b: np.ndarray) -> float:
    """Cosine distance for L2-normalised embeddings."""
    return float(1.0 - np.dot(a, b))


def axis_perturbations(emb: dict[tuple, np.ndarray]) -> dict[str, float]:
    """Mean cosine distance induced by moving along each axis, others held fixed.

    Keys of ``emb`` are (content_id, surface, structural, validity).
    """
    contents = sorted({k[0] for k in emb})
    surfaces, structs, vals = ("S0", "S1", "S2"), ("T0", "T1"), ("valid", "invalid")

    d_s, d_t, d_v = [], [], []
    for c in contents:
        for t in structs:
            for v in vals:  # S axis: all surface pairs at fixed (c, t, v)
                for s1, s2 in combinations(surfaces, 2):
                    d_s.append(_cos_dist(emb[(c, s1, t, v)], emb[(c, s2, t, v)]))
        for s in surfaces:
            for v in vals:  # T axis: T0 vs T1 at fixed (c, s, v)
                d_t.append(_cos_dist(emb[(c, s, "T0", v)], emb[(c, s, "T1", v)]))
            for t in structs:  # V axis: valid vs invalid at fixed (c, s, t)
                d_v.append(_cos_dist(emb[(c, s, t, "valid")], emb[(c, s, t, "invalid")]))
    return {
        "delta_S": float(np.mean(d_s)), "delta_S_sd": float(np.std(d_s)),
        "delta_T": float(np.mean(d_t)), "delta_T_sd": float(np.std(d_t)),
        "delta_V": float(np.mean(d_v)), "delta_V_sd": float(np.std(d_v)),
    }


def _cv_accuracy(X: np.ndarray, y: np.ndarray, n_splits: int = 5) -> float:
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import StratifiedKFold, cross_val_score

    n_splits = min(n_splits, int(np.min(np.bincount(y))))
    if n_splits < 2:
        return float("nan")
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=SEED)
    clf = LogisticRegression(max_iter=2000)
    return float(np.mean(cross_val_score(clf, X, y, cv=skf)))


def decoding(items, X: np.ndarray) -> dict:
    surf = np.array([it.surface for it in items])
    dom = np.array(["psy" if it.item_id.startswith("psy") else "tec" for it in items])
    struct = np.array([it.structural for it in items])

    def enc(labels):
        u = {v: i for i, v in enumerate(sorted(set(labels)))}
        return np.array([u[v] for v in labels])

    out = {
        "surface_decode_acc": _cv_accuracy(X, enc(surf)),     # expect ~1.0 (sanity)
        "domain_decode_acc": _cv_accuracy(X, enc(dom)),
        "T_within_surface": {},
    }
    for s in ("S0", "S1", "S2"):
        m = surf == s
        out["T_within_surface"][s] = _cv_accuracy(X[m], enc(struct[m]))
    vals = [a for a in out["T_within_surface"].values() if a == a]
    out["T_within_surface_mean"] = float(np.mean(vals)) if vals else float("nan")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", type=str, default=None)
    args = ap.parse_args()

    items = stimuli_content.draft_items()
    prompts = [it.prompt for it in items]
    print(f"embedding {len(items)} draft stimuli with all-MiniLM-L6-v2 ...", flush=True)

    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    X = np.asarray(model.encode(prompts, normalize_embeddings=True, show_progress_bar=False))

    emb = {
        (it.item_id.rsplit("-", 3)[0], it.surface, it.structural, it.validity): X[i]
        for i, it in enumerate(items)
    }
    pert = axis_perturbations(emb)
    dec = decoding(items, X)

    print("\n--- axis perturbation (mean cosine distance, others held fixed) ---")
    print(f"  S (surface) : {pert['delta_S']:.4f} +/- {pert['delta_S_sd']:.4f}")
    print(f"  T (structure): {pert['delta_T']:.4f} +/- {pert['delta_T_sd']:.4f}")
    print(f"  V (validity) : {pert['delta_V']:.4f} +/- {pert['delta_V_sd']:.4f}")
    print(f"  ratio delta_T / delta_S = {pert['delta_T']/pert['delta_S']:.3f}")
    print("\n--- decoding (5-fold CV logistic accuracy) ---")
    print(f"  surface (S0/S1/S2, chance .33): {dec['surface_decode_acc']:.3f}")
    print(f"  domain (psy/tec, chance .50)  : {dec['domain_decode_acc']:.3f}")
    print("  T0-vs-T1 WITHIN fixed surface (chance .50) -- the load-bearing test:")
    for s, a in dec["T_within_surface"].items():
        print(f"    {s}: {a:.3f}")
    print(f"    mean: {dec['T_within_surface_mean']:.3f}")

    interp = (
        "structure decodable within surface => S x T separable (non-degenerate)"
        if dec["T_within_surface_mean"] >= 0.75
        else "structure weakly separable from surface in this proxy -- investigate"
    )
    print(f"\ninterpretation (PILOT, sentence-embedding proxy): {interp}")
    print("NB: absolute sigma(x) vs the locked reference corpus is deferred (see README).")

    if args.json:
        Path(args.json).write_text(json.dumps(
            {"n_items": len(items), "perturbation": pert, "decoding": dec}, indent=2))
        print(f"\nwrote {args.json}")


if __name__ == "__main__":
    main()
