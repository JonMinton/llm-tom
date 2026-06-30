---
status: pilot — methodology proxy, NOT the locked frequency analysis
embedding: sentence-transformers/all-MiniLM-L6-v2 (384-dim)
date: 2026-06-30 (butler M4)
thresholds: none committed — PROVISIONAL / exploratory
---

# Frequency-analysis separation pilot — results note

Corpus-free representational check, per `separation_pilot.py`. It does **not**
compute the locked support-sparsity σ(x) (that needs the 50–100 GB Dolma/RedPajama
reference corpus — deferred). It answers the prior question the P3 stress-test
raised: **do Surface (S) and Structural (T) novelty move the representation in
*separable* ways, or does surface dominate and swamp structure?**

Instrument: the 96-item DRAFT S×T×V grid (`llm_tom.stimuli_content.draft_items`,
psychological + technical, T0/T1; T2 deferred) embedded with `all-MiniLM-L6-v2`.
This is a **sentence-embedding proxy**, not the target model's residual stream
(which the design actually probes) — read accordingly.

## Results

**Per-axis perturbation** (mean cosine distance induced by moving one axis, others held fixed):

| Axis | Δ (mean) | SD |
|------|---------|-----|
| **S (surface)** | **0.338** | 0.086 |
| **T (structure)** | **0.054** | 0.033 |
| **V (validity)** | 0.043 | 0.050 |

Δ_T / Δ_S = **0.159** — structure perturbs the embedding only ~16% as much as surface.

**Decoding** (5-fold CV logistic accuracy):

| Target | Acc | Chance |
|--------|-----|--------|
| surface S0/S1/S2 | **1.000** | .33 |
| domain psy/tec | **1.000** | .50 |
| **T0-vs-T1 within fixed surface** | **0.379** (S0 .43, S1 .40, S2 .31) | .50 |

## Reading (honest, caveated)

The pipeline is sound — it recovers surface and domain at 1.0 — so the **T null is
real, not an artefact**: in this proxy, the structural axis (epistemic-nesting
depth) is **not separable from surface**, and surface dominates the geometry. That
**corroborates the stress-test's conflation concern in this proxy**, and is *why*
the design's upstream encoding-gate and surface controls are load-bearing.

But a null here is **suggestive, not decisive**, for two non-exclusive reasons:

1. **Wrong instrument (expected).** `all-MiniLM-L6-v2` is a *semantic-similarity*
   sentence encoder, not the target LLM. The design's structural signal lives in
   the target model's **residual stream** (where activation patching reads it),
   not in a generic semantic embedding. A semantic encoder mapping T0 and T1
   close together is roughly what we'd expect — they *are* semantically near.
   The decisive separation test must use the target model's activations.

2. **T1 is under-expressed in this DRAFT.** `stimuli_content.T1_DEPTH = 2`
   (second-order nesting), whereas the synthesis spec calls for **"deeply-nested
   (4+ levels)"**. The textual T0→T1 change here is one short clause, small
   against content variation across the 8 base stimuli — so even a model that
   *could* encode nesting depth may show little footprint at depth 2. This is a
   concrete, pre-data reason to revisit T1 depth (a design decision: deeper chains
   must keep a determinate answer, which needs argument — see `CLAUDE.md`).

## Implications / next

- **Surface axis confirmed** real and dominant (perfect decode) — consistent with
  the design's premise that surface effects must be gated/controlled.
- **Structural axis needs (a) the target model's residual stream and/or (b) deeper
  T1 nesting** before its separability can be judged. The sentence-embedding proxy
  is insufficient for T — a useful negative result that bounds what this cheap lens
  can show.
- Does **not** touch the absolute σ(x) / locked-corpus step, nor the deferred
  T2/combinatorially-novel form.

All numbers exploratory; nothing committed to `config.py`.
