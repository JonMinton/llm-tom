---
status: skeleton
last_update: 2026-05-02
---

# Implementation template

End-to-end TransformerLens-based code intended to validate that the methodology executes correctly on a small open-weight transformer (Pythia-160M class). The template does **not** make claims about whether the small model has Theory of Mind — it demonstrates the pipeline.

## What this template proves and does not prove

- **Proves:** the four-lens pipeline (intrinsic-dimension estimation, linear probing, activation patching, persistent-homology computation) runs end-to-end on real activations from a real model with a small set of matched-pair stimuli, without crashing and producing sensible artefacts.
- **Does not prove:** that the model has any particular cognitive capacity. A pilot result on Pythia-160M is a pipeline test, not a scientific finding.

## Stack

- Python ≥ 3.11.
- [`transformer-lens`](https://github.com/TransformerLensOrg/TransformerLens) — primary mechanistic-interpretability toolkit.
- [`sentence-transformers`](https://github.com/UKPLab/sentence-transformers) — for the frequency-analysis pipeline (lightweight embedding model).
- `scikit-learn` — linear probing.
- `scikit-dim` or hand-rolled TwoNN/GRIDE — intrinsic dimension.
- `gudhi` or `ripser` — persistent homology.
- `pytest` — tests.

Dependency definitions live in `pyproject.toml`.

## Layout (to be built)

```
implementation/
├── README.md                # this file
├── pyproject.toml
├── src/
│   ├── llm_tom/
│   │   ├── __init__.py
│   │   ├── stimuli.py       # load and validate stimulus pairs
│   │   ├── activations.py   # extract per-layer residual stream activations
│   │   ├── geometric.py     # ID estimation (TwoNN, GRIDE)
│   │   ├── probing.py       # per-layer linear probes
│   │   ├── patching.py      # activation patching (component-level)
│   │   ├── topology.py      # persistent-homology pipeline
│   │   ├── convergence.py   # cross-lens convergence summary
│   │   └── pipeline.py      # end-to-end driver
│   └── ...
└── tests/
    ├── test_stimuli.py
    ├── test_activations.py
    ├── test_pipeline_smoke.py   # runs the whole pipeline on 4 stimuli
    └── ...
```

## Validation criteria

The template is considered validated when:

1. The smoke test (`test_pipeline_smoke.py`) runs end-to-end on Pythia-160M with 4 matched-pair stimuli on the M4 Mac mini in under 10 minutes.
2. Each lens produces a non-trivial output (not all zeros, not all NaN).
3. Outputs are deterministic given fixed seed.
4. The convergence summary produces a layer-indexed table without error.

## Reproducibility

- All random seeds set explicitly.
- Model checkpoint version pinned in `pyproject.toml`.
- Each result file records: code commit, dependency hashes, run timestamp.

## Out of scope

- The full experiment (larger model, full stimulus set). Compute requirement is beyond the local Mac mini; intended to be picked up by researchers with appropriate infrastructure.
- Any claim about which hypothesis (A/B1/B2/C) is supported. The pilot is for pipeline validation only.
