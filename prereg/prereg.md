---
status: scaffold
target_platform: OSF (https://osf.io/)
last_update: 2026-05-02
---

# OSF pre-registration — scaffold

This is a scaffold matching OSF's standard pre-registration sections. The point of pre-registering this work is to discipline the paper's specificity: vague analysis plans become unfalsifiable, and the B1/B2 distinction in particular needs falsification rules locked in before any data is run.

Pre-registration should happen **after** the frequency analysis confirms the OOD status of the combinatorial-novel stimuli, and **before** any model is run on the matched stimulus matrix.

## Study information

### Title

Adjudicating Algorithmic Theory of Mind in Language Models: A Methodology for Distinguishing Domain-Specific, Abstract-Primitive, Cross-Domain-Interpolation, and Pattern-Matching Hypotheses.

### Authors

Jon Minton (statistician, Edinburgh) and any human collaborators. AI contribution acknowledged in dedicated section per the authorship discipline (see `README.md`).

### Description

One-paragraph plain-language summary. To be drafted from the README's introduction.

## Hypotheses

Four hypotheses on the level of computational abstraction at which an LLM solves Theory-of-Mind tasks. Each makes a specific prediction across the three-condition stimulus matrix and the recursive OOD probe — see `analysis/prediction_matrix.csv` for the tabular form.

State the falsification rule for each. Specify in advance:

- What pattern of results would falsify A.
- What pattern would falsify C.
- What pattern would falsify B (jointly).
- What signature distinguishes B1 from B2 in the recursive probe, with pre-committed thresholds.

A pre-registration that cannot be falsified is not a pre-registration.

## Design

### Stimulus matrix

Three conditions × matched-pair structure (false-belief / true-belief, or domain-equivalent divergent-state / non-divergent control):

1. Psychological — Sally-Anne variants.
2. Technical — State-Rollback isomorphism.
3. Combinatorially novel — final form to be specified once finalised in `stimuli/novel/`.

50 stimulus pairs per condition (numbers to be confirmed by power calculation; see Sample Size below).

### Recursive OOD probe

The B1/B2 discriminator. Operationalisation must be locked here. Placeholder:

- Identify the candidate shared circuit from causal patching results across the three primary conditions.
- Apply patching of that circuit to a fourth-condition stimulus set designed to push beyond the trained-primitive boundary.
- Pre-commit signature thresholds for "primitive" vs "interpolator" behaviour.

This is the most attackable part of the design; finalise the operationalisation before submission.

### Models

To be specified. Pilot on Pythia-160M class for pipeline validation; full experiment on a model class plausibly capable of Sally-Anne success — to be locked here.

## Sampling plan

### Sample size justification

Power calculation TBD. Anchor: number of stimulus pairs needed to detect a per-layer linear-probe accuracy difference of [X] with α=0.05 and 1−β=0.80 across [N] layers under multiple-comparisons correction.

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

Pre-register **after** frequency analysis has been run (so OOD status of the novel condition is empirical), **before** any model is run on the full matched stimulus matrix.
