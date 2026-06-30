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

---

# Follow-up: residual-stream instrument (`residual_separation_pilot.py`)

The MiniLM null prompted the faithful re-test: the same separation metrics on
**Pythia-160m's `resid_post` at the final token, per layer** — the space activation
patching actually reads — instead of the semantic proxy. 96 items × 12 layers,
~11 s on the idle butler (CPU), seed 0.

## Result — the null flips

T0-vs-T1 is **linearly separable within fixed surface in the residual stream**,
where the semantic proxy saw nothing:

| layer | Δ_T | surface decode | T0/T1 within-surface (mean; S0 / S1 / S2) |
|------:|----:|:--------------:|:------------------------------------------|
| L0 | 0.019 | 1.00 | 0.92 (1.00 / 1.00 / 0.77) |
| **L4** | 0.134 | 1.00 | **0.98 (1.00 / 1.00 / 0.94)** ← peak |
| L8 | 0.125 | 1.00 | 0.78 (1.00 / 0.94 / 0.40) |
| L11 | 0.004 | 1.00 | 0.63 (0.77 / 0.77 / 0.34) |

Surface decodes at **1.00 at every layer**; peak within-surface T decode **L4 = 0.98**.
⇒ In the right instrument the **S×T decomposition is non-degenerate** even at this
DRAFT's depth-2 T1 — **caveat 1 of the MiniLM null is confirmed** (proxy was wrong).

## Two named seams (flagged, not smoothed)

1. **S2 (logical notation) is the weak surface.** T decode is near-perfect within
   S0 (narrative) and S1 (code-like) but ranges 0.34–0.94 within S2, collapsing in
   late layers (L10–L11 ≈ 0.34). The model separates structure cleanly in narrative
   and code, but **not reliably in belief-operator notation** — relevant to the
   gate/surface controls and to whether S2 belongs as drawn.
2. **Lexical confound on the T contrast.** T1 appends a clause (the second-order
   "onlooker" layer), so the final-token residual differs partly because the
   *contexts* differ lexically, not purely because nesting depth is *structurally*
   encoded. Against a pure-lexical reading: the decode **peaks mid-layer (L4) then
   declines**, and is **surface-dependent** (S2 weak) — neither of which a flat
   lexical difference would produce. But a clean claim needs a **length/lexically
   matched T-control** (a T0 with a structurally-irrelevant clause of matched
   length). That is the next step to make this rigorous.

## Net

The faithful instrument answers the proxy's caveat 1: structure is **not** invisible
— it is strongly present in early-mid layers (peak L4) for narrative/code surfaces.
Open before any claim: the lexical-control test (seam 2) and the S2 weakness (seam
1). Deeper T1 (spec: 4+ levels), the absolute σ(x)/locked corpus, and T2 remain
deferred. Exploratory; nothing committed.

---

# Lexical control — seam 2 closed (`lexical_control_pilot.py`)

To separate "nesting depth is structurally encoded" from "T1 is just longer / has an
extra entity", a **T0-padded** control was added (`render_t0_padded`): a *first-order*
probe that carries the *same* onlooker clause as T1, so T0pad and T1 differ only in
the final clause (`"... Sarah will look in"` vs `"... Mia expects Sarah to look in"`).
Per layer, within fixed surface, decode the original **unmatched** (T0 vs T1) beside
the **matched** (T0pad vs T1). 144 items, Pythia-160m residual stream.

| layer | unmatched (T0 vs T1) | matched (T0pad vs T1) | lexical share |
|------:|:--------------------:|:---------------------:|:-------------:|
| L2 | 0.962 | 0.952 | +0.02 |
| **L4** | **0.981** | **0.981** | **+0.00** |
| L6 | 0.868 | 0.867 | +0.00 |
| L8 | 0.779 | 0.610 | +0.61 |
| L11 | 0.627 | 0.460 | (below chance) |

**Result: at the layers where T0/T1 separates best (L2–L6, peak L4 = 0.98), the
matched decode equals the unmatched** — holding the onlooker entity and clause
length constant removes *nothing*. So the early-mid separation is driven by the
**epistemic nesting (probe order), not by length or entity-presence**. The lexical
confound only contributes in *late* layers (L7+), where the decode is already weak.

⇒ **Seam 2 closed:** Pythia-160m linearly represents epistemic nesting depth in
early-mid layers (peak L4), genuinely — even at this DRAFT's T1 depth-2.

Remaining: **seam 1 (S2 logical-notation weakness)** is largely a *late-layer*
effect — at the peak layer L4 even S2 decodes ~0.94 — but warrants its own look.
Depth-2 suffices for *detection*; whether 4+ nesting is needed for downstream B1/B2
*discrimination* is a separate question. σ(x)/locked corpus and T2 stay deferred.
