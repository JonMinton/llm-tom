---
status: design-locked (recursive-OOD-probe section is executable; numeric thresholds pilot-calibrated per pre-committed procedure)
target_platform: OSF (https://osf.io/)
last_update: 2026-06-29
---

# OSF pre-registration — scaffold

This is a scaffold matching OSF's standard pre-registration sections. The point of pre-registering this work is to discipline the paper's specificity: vague analysis plans become unfalsifiable, and the B1/B2 distinction in particular needs falsification rules locked in before any data is run.

**This is a two-stage preregistration (decided 2026-06-29).** *Stage 1* (this document, posted now) locks the design, hypotheses, decision rules, falsification rules, and the threshold-*calibration procedure*, before any empirical work — every numeric threshold is explicitly marked PROVISIONAL-pending-pilot. *Stage 2* (posted after the M4 pilot) locks the pilot-calibrated numeric thresholds, the σ(x)/S–T ordering validation, the power/sample-size analysis, and the confirmatory model — **before** any model is run on the full matched stimulus matrix. Rationale: the frequency analysis and `SD_pilot` calibration must inform the OOD ordering, the power analysis, and the thresholds; freezing those numbers a priori would violate the design's own discipline (and was the exact failure mode the stress-test caught — see `prereg/notes/p3-stress-test.md`).

## Study information

### Title

Adjudicating Algorithmic Theory of Mind in Language Models: A Methodology for Distinguishing Domain-Specific, Abstract-Primitive, Cross-Domain-Interpolation, and Pattern-Matching Hypotheses.

### Authors

Jon Minton (statistician, Edinburgh) and any human collaborators. AI contribution acknowledged in dedicated section per the authorship discipline (see `README.md`).

### Description

This study specifies and pre-registers a methodology for adjudicating *what level of computational abstraction* a large language model operates at when it succeeds on Theory-of-Mind tasks such as the Sally-Anne false-belief task — rather than the underdetermined question of whether it "has" Theory of Mind. Four hypotheses are distinguished — **A** (a domain-specific psychological-ToM circuit), **B1** (a substrate-independent abstract "divergent-state" primitive), **B2** (a cross-domain interpolator over the training distribution), and **C** (domain-specific pattern matching) — by convergence across four methodologically independent interpretability lenses (intrinsic dimension, linear probing, activation patching, persistent homology) applied to a matched three-condition stimulus matrix (psychological / technical-isomorph / combinatorially-novel), plus a recursive out-of-distribution probe that distinguishes B1 from B2. No experiment has been run; this is a design pre-registration, with numeric thresholds calibrated in a pre-committed pilot (Stage 2). The recursive probe achieves *partial* identification (conditional on the encoding controls specified below); the contribution is the methodology plus an honest identification analysis, not a claim of full identification.

## Hypotheses

Four hypotheses on the level of computational abstraction at which an LLM solves Theory-of-Mind tasks. Each makes a specific prediction across the three-condition stimulus matrix and the recursive OOD probe — see `analysis/prediction_matrix.csv` for the tabular form.

Falsification rules (pre-committed; tabular predictions in `analysis/prediction_matrix.csv`):

- **Falsifies A** (domain-specific ToM circuit): A predicts the candidate bottleneck fires for *psychological* stimuli only. A is falsified if a shared circuit mediates the divergent-state distinction across the technical and/or combinatorially-novel conditions as well (cross-domain firing). *(A and C make identical predictions on the three-condition matrix; they are separated by within-domain generalisation tests — see Analysis plan.)*
- **Falsifies C** (deflationary, domain-specific pattern-matching): C predicts *different* circuits for different stimulus types. C is falsified by the "Unified" circuit-identification outcome — a shared component intersection mediating ≥ τ_U of the clean logit-difference across all three primary conditions.
- **Falsifies B jointly** (B1 or B2, i.e. a shared cross-domain circuit): B is falsified if no shared circuit exists ("Deflationary-disjoint" circuit-ID outcome → C) or if the circuit fires for psychological stimuli only (→ A); and by the global falsification rule — high OOD behavioural accuracy (≥80%) with the candidate bottleneck mediating ≤0.10 NCME (Fieller 95% CI including 0), proving the bottleneck is a local A/C artefact and OOD success came from independent circuitry.
- **B1 vs B2** (the recursive OOD probe — see Design § "Recursive OOD probe" for the executable contract): B1 requires the NCME-vs-structural-novelty slope at fixed surface novelty to fall positively within a pre-registered equivalence band (ROPE), corroborated by NCME violating the Lipschitz decay envelope in sparse-support regions; B2 requires monotonic NCME decay (slope negative and outside the ROPE) with points on/below the envelope; results consistent with neither are reported **inconclusive**, not forced.

A pre-registration that cannot be falsified is not a pre-registration.

## Design

### Stimulus matrix

Three conditions × matched-pair structure (false-belief / true-belief, or domain-equivalent divergent-state / non-divergent control):

1. Psychological — Sally-Anne variants.
2. Technical — State-Rollback isomorphism.
3. Combinatorially novel — final form to be specified once finalised in `stimuli/novel/`.

50 stimulus pairs per condition (numbers to be confirmed by power calculation; see Sample Size below).

### Recursive OOD probe

**This section is the canonical executable contract for the B1/B2 discriminator.** The position paper points here for operational details rather than duplicating them (decision logged in `CHANGELOG.md` 2026-05-02, P2 resolution). Consolidated 2026-06-29 from the P3 design dialogue, a 3-reviewer adversarial stress-test, and a revision round; full provenance and rationale in `prereg/notes/p3-synthesis.md` and the `p3-*` notes (`CHANGELOG.md` 2026-06-29). The probe is pre-registered as achieving **partial identification** — conditional on the encoding controls below.

**Factor structure.** A **Surface-Novelty (S) × Structural-Novelty (T)** factorial, replacing the original single composite "substrate-distance" axis (found non-identifying: it conflated surface novelty with structural novelty, and LLM representational geometry tracks surface frequency, not human semantic taxonomy, so neither a flat nor a decaying patching effect was interpretable).
- **S (surface):** S0 narrative English / S1 code-like (assignment statements over named agents) / S2 logical-operator notation.
- **T (structural):** T0 standard Sally-Anne / T1 deeply-nested epistemic chains (≥4 levels) / T2 non-standard update rules (retrocausal / non-Bayesian).
- The **same logical content is rendered across all three S forms at each T level** (T held constant across S). This is what makes the factorial identifying: structural novelty varies at fixed surface novelty and vice versa.
- **Continuous complement:** for each stimulus also compute support sparsity `σ(x) = (1/k) Σ_j D_M(x, NN_j(x))` (mean Mahalanobis distance to k≈50 nearest reference-corpus neighbours), to validate the S/T ordering empirically rather than by fiat.

**Candidate shared circuit identification.** Rank components by patching effect on the three primary conditions; take the intersection above a pre-committed threshold. Pre-specified outcomes: **Unified** (intersection mediates ≥ τ_U of clean logit-diff across all three → proceed); **Deflationary-disjoint** (≤ τ_D → definitive Hypothesis-C, terminate); **Inconclusive** (diffuse, no discrete circuit). τ_U, τ_D PROVISIONAL (calibration below).

**Upstream encoding-gate.** Train a ridge-regression probe at an early layer l ∈ [2,4] to decode the stimulus's deterministic surface ground-truth. Partition trials by early-decode accuracy α: **T_parsed** (α ≥ α_hi → surface provably encoded → kept) vs **T_unparsed** (α < α_lo → excluded as uninterpretable). Compute the dependent measure on T_parsed only. This conditions on *"was the surface encoded,"* not on *"does the bottleneck separate cleanly,"* so it does not discard B2's distant-failure evidence. α_hi, α_lo PROVISIONAL.

**Dependent measure & estimator.** NCME = (L_patched − L_corrupted)/(L_clean − L_corrupted), computed on T_parsed. **No downstream denominator gate** — gating on |L_clean − L_corrupted| is survivorship bias (it discards exactly the distant trials where B2 predicts the forward pass collapses). Ratio CIs via **Fieller's method**, which widens honestly for near-zero/near-zero trials rather than excluding them.

**Factor-2 (validity) de-confound.** Match valid/invalid minimal pairs on unrelated-LM baseline cross-entropy (reference-corpus surprisal) within |ΔP| ≤ ~0.1–0.15 nats/token; measure and report residual substrate-level baseline differences rather than confounding them.

**B1 signature (two convergent tests).**
- (a) **Equivalence test:** the 90% CI of the NCME-vs-T slope at each fixed S falls entirely within a pre-registered ROPE (±r·SD_pilot). B1 is *positively* supported, never inferred from failure-to-reject.
- (b) **Lipschitz-violation:** NCME stays ≥ 0.85 in genuinely sparse-support regions (σ ≫ 1/λ), violating the decay envelope `NCME_max(σ) ≤ 1 − λ·σ` that any continuous interpolator must obey.

**B2 signature.** NCME decays monotonically with T at fixed S (slope CI negative and outside the ROPE) AND data points sit on or below the Lipschitz envelope.

**Decision rule.** B1 supported iff (a) holds (corroboratively (b)); B2 supported iff the decay + envelope criteria hold; **inconclusive** if the slope CI spans both ROPE-interior and B2-territory, or the two B1 tests disagree. Inconclusive is a real, reportable verdict — not forced to B1/B2.

**Falsification (sinks both B1 and B2).** On OOD conditions with high behavioural accuracy (≥ 80%), the candidate bottleneck mediates ≤ 0.10 NCME with a Fieller 95% CI including 0 → the bottleneck was a local A/C artefact and OOD success came from independent circuitry; report as such.

**Threshold calibration (this is what makes the PROVISIONAL numbers legitimate).** Every numeric threshold — SD_pilot, ROPE half-width r, λ, τ_U/τ_D, α_hi/α_lo, k — is set from the **pilot**, not a priori, by this pre-committed procedure: bootstrap NCME variance on a known-good (IOI-equivalent) circuit to fix SD_pilot; set the ROPE and B1/B2 slope bands as pre-registered multiples of SD_pilot before the confirmatory run; calibrate the encoding-gate α thresholds from the ridge probe's accuracy distribution on known-good stimuli; power the equivalence test against the dead-zone alternative (−1.5·SD_pilot). This calibration is the content of the M4 pilot phase and is itself pre-registered, even though the numbers are pending.

**Residual identification limit (pre-registered honesty).** This probe identifies B1 vs B2 only conditional on the encoding controls being approximately correct. The pre-registration and paper state this limit explicitly; the contribution is the methodology (decomposed axes, encoding-gating, equivalence testing, Lipschitz bounding, Fieller estimation) and an honest identification analysis, not a claim of full identification.

### Models

**Stage 1 (locked now):** pipeline validation and threshold calibration on a **Pythia-160M-class** open-weight model (Mac-mini-tractable); the encoding-gate ridge probe and `SD_pilot` calibration use a known-good (IOI-equivalent) circuit on the same small model. **Stage 2 (locked after pilot):** the confirmatory model — a model class plausibly capable of Sally-Anne success (candidate: Llama-3-8B, with the pre-registered unquantised-baseline guardrail for the quantisation confound) — is named at Stage 2, once the pilot confirms the pipeline runs end-to-end.

## Sampling plan

### Sample size justification

**Deferred to Stage 2 (pilot-dependent).** A power analysis cannot be honestly computed before the pilot fixes `SD_pilot` and the NCME noise distribution. Pre-committed procedure: power the primary equivalence test (NCME-vs-T slope at fixed S) against the dead-zone alternative (−1.5·`SD_pilot`) at α=0.05, 1−β=0.80, with multiplicity correction across the S levels; report items-per-cell needed to keep the false-B1 (dead-zone misclassification) rate below 5%. Stimulus-pair counts per cell are set from this analysis at Stage 2 (working assumption ≈50/cell, to be confirmed).

### Data exclusion

Specify in advance: stimuli where the model's output is malformed (refusal, off-topic continuation), runs where activation patching fails sanity checks (e.g. patching everything fails to reproduce baseline).

## Variables

### Independent variables

- Stimulus condition (psychological / technical / novel).
- Stimulus type within condition (false-belief / true-belief, or domain-equivalent).
- Model layer index.
- Component patched (for causal lens).

### Dependent variables

- Per-layer ID estimate (TwoNN, GRIDE).
- Per-layer linear-probe accuracy and AUC.
- Per-component patching effect on next-token logit.
- Per-layer per-condition persistence barcodes (Wasserstein distance between conditions).

## Analysis plan

Pointer to `analysis/plan.md`. Lock that file's contents at pre-registration time. Any deviation in the paper requires explicit acknowledgement and justification.

## Multiple comparisons

State correction strategy explicitly. See `analysis/plan.md`.

## Other

### Conditional analyses

Specify: if the four-lens convergence does not hold, what secondary analyses are reported? (Reporting these as exploratory, not confirmatory, is the discipline.)

### Falsification

The position-paper claim — that the methodology can adjudicate A/B1/B2/C — is *itself* falsifiable. If on the chosen model the four lenses do not converge on a consistent locus, the methodology is not supported on that model; report this honestly.

### Pre-registration timing

Two-stage (see top of document). **Stage 1** posted now (design + procedures, pre-empirical). **Stage 2** posted after the frequency analysis and pilot calibration (so OOD status, the σ(x)/S–T ordering, thresholds, power, and confirmatory model are empirical), and **before** any model is run on the full confirmatory matched stimulus matrix.
