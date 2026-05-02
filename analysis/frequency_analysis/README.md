---
status: protocol-only (no data yet)
last_update: 2026-05-02
---

# Frequency analysis: corpus prevalence of stimulus structures

The argument that the **State-Rollback** condition is in-distribution and the **Combinatorially Novel** condition is OOD requires empirical grounding rather than intuition. This directory holds the protocol, scripts (when written), and results (when run) for that grounding.

## Why this is a prerequisite

The position paper's core claim — that B1 / B2 hypotheses can be discriminated by behaviour on a designed novel condition — depends on the novel condition actually being structurally absent from the training distribution. If structurally similar examples are common in pre-training corpora, "OOD" fails on its own terms and the experiment loses traction.

This analysis does not need to be perfect. It needs to be defensible enough that a reviewer pushing back on "is this really OOD?" can be answered with data rather than intuition.

## Protocol

### Corpus

- 50–100 GB random sub-sample of [Dolma](https://huggingface.co/datasets/allenai/dolma) or [RedPajama](https://huggingface.co/datasets/togethercomputer/RedPajama-Data-V2).
- Sub-sampling stratified across source domains where possible (web vs books vs code vs academic).
- Recorded: sub-sample seed, source manifest, total tokens, per-domain token counts.

### Stimulus variants

- 50 paraphrased variations of each stimulus type (psychological, technical, combinatorially novel).
- Variations differ in surface form (names, settings, narrative wrapping) but preserve the structural feature of interest (divergent state, isomorphic operator structure).
- Stored under `stimuli/{psychological,technical,novel}/variants/` and referenced from this directory.

### Embedding

- Lightweight model: `sentence-transformers/all-MiniLM-L6-v2` (384-dim, fast on CPU).
- Per stimulus type: embed all 50 variants, compute centroid vector.
- Per corpus chunk (e.g. 256-token windows with stride): embed.

### Matching

- Cosine similarity between each chunk embedding and each centroid.
- Per category, retrieve top 1000 chunks by similarity.
- Manual inspection of a sample (e.g. 50 per category) to sanity-check whether the hits are structurally similar or merely topically adjacent.

### Threshold for the in-/out-of-distribution claim

Pre-commit before running:

- **State-Rollback declared in-distribution** if its top-1000 hits show frequency and similarity comparable to Psychological's top-1000 (e.g. median similarity within 0.05; manual-inspection structural-match rate within 20 percentage points).
- **Combinatorially Novel declared OOD** if its top-1000 hits are dominated by topical false positives and structural-match rate (manual inspection) is near zero.

Specify what the operationalisation is **before** seeing the numbers, and lock it in the pre-registration.

### Supplementary structural matching

Embedding similarity may miss structural isomorphism (matching on plot/topic, missing on relational structure). Supplement with:

- Dependency-parse pattern matching for the top-N chunks per category (e.g. via spaCy or stanza), looking for the divergent-state relational signature.
- AST-style matching for the technical condition (e.g. tree-sitter on code-like spans).

This is computationally expensive on the full 50 GB but tractable on the top-1000 filtered subsets.

## Compute budget

The full pipeline is intended to run on the M4 Mac mini.

- Embedding 50 GB at MiniLM speed: roughly tens of hours on CPU (manageable; feasible with batching). Acceleration via Metal (PyTorch MPS backend) where supported.
- Top-K retrieval and inspection: trivial relative to the embedding step.
- Structural matching: dominated by parse time; bound by the chosen subset size.

## Outputs

When run, write into this directory:

```
frequency_analysis/
├── README.md                  # this file
├── protocol.md                # the locked protocol (post-prereg)
├── scripts/                   # numbered pipeline scripts
├── data/                      # ⊳ gitignored ⊲ corpus chunks, manifests
├── embeddings/                # ⊳ gitignored ⊲
├── results/                   # ⊳ gitignored ⊲ raw match tables
└── report.md                  # human-readable summary; what to cite in the paper
```

`data/`, `embeddings/`, and `results/` are listed in the top-level `.gitignore`.
