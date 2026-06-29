---
status: scaffold built (decision core implemented + unit-tested; model-coupled lenses wired for the M4)
last_update: 2026-06-29
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

## What is implemented (2026-06-29)

The **statistical / decision core** is implemented and unit-tested (`python -m pytest` → 20 passed; runs **without** `torch`):

- `ncme.py` — NCME with **Fieller** intervals (honestly unbounded near a zero denominator; there is **no** survivorship-biasing denominator gate).
- `equivalence.py` — **TOST/ROPE** equivalence test, the B1 / B2 / inconclusive decision rule, and the both-sink global falsification.
- `lipschitz.py` — support sparsity σ(x) + the **Lipschitz-envelope** test (turns flat NCME into a positive B1 signature).
- `sd_pilot.py` — bootstrap `SD_pilot` calibration.
- `circuit_id.py` — Unified / Deflationary-disjoint / Inconclusive circuit-identification outcomes.
- `geometric.py` — TwoNN intrinsic dimension; `stimuli.py` — the 3×3×2 (Surface × Structural × Validity) factorial schema; `encoding_gate.py` — the `T_parsed` / `T_unparsed` partition.
- `pipeline.py` — `run_recursive_probe()` wires the decision core end-to-end (smoke-tested on synthetic logit differences).

The **model-coupled lenses** (`activations.py`, `patching.py`, `probing.py`, `topology.py`) import `torch` / `transformer_lens` / `gudhi` **lazily** and expose the interfaces to be wired on the M4 pilot host (the patching hook loop raises `NotImplementedError` until then).

All numeric thresholds live in `config.py` and are **PROVISIONAL**, pilot-calibrated per the Stage-1 pre-registration (<https://osf.io/z9t4a>).

### Run the tests

```
cd implementation
python -m pytest -q        # 20 passed; the decision core needs no torch
```

## Layout (built — see `src/llm_tom/`; P3 decision modules added alongside the four lenses)

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
