---
status: scaffold
last_update: 2026-05-02
---

# Pre-specified analysis plan

This is a scaffold. Each section below names what must be specified before any analysis is run, and what counts as falsification. The plan should be locked in (and pre-registered) before stimuli are run through any model.

## Models

To be specified. Constraints:

- Validation pilot: a small open-weight transformer for which TransformerLens supports activation patching out-of-the-box. Pythia-160M is the placeholder; alternatives include GPT-2-small / GPT-2-medium, TinyStories-instruct.
- Full experiment: open-weight model large enough to plausibly succeed at Sally-Anne (≥ Pythia-2.8B / Llama-3-8B-class). The full experiment is **out of scope for this repo's compute** — the implementation template demonstrates the pipeline; the actual run is delegated.

## Lens 1 — intrinsic dimension (geometric)

- Estimator: TwoNN. Sanity check with GRIDE.
- Inputs: residual-stream activations at each layer for each stimulus condition.
- Output: ID per layer per condition.
- Pre-registered prediction: ID expands in early-middle layers, compresses in middle-late layers (operational discretisation). Compression-zone layer indices are hypothesised to align with the layers where causal patching identifies the ToM bottleneck.

## Lens 2 — linear probing (behavioural)

- Probe: logistic regression (L2-regularised), trained per layer, on the false-belief / true-belief distinction.
- Train/test split: stimulus-level (no leakage of paraphrases across splits).
- Output: per-layer accuracy and AUC.
- Pre-registered prediction: linear separability rises sharply at the same layer indices identified by ID compression.

## Lens 3 — activation patching (causal)

- Method: per-head and per-MLP patching between matched-pair stimuli (false-belief vs true-belief variant of the same narrative).
- Metric: change in next-token logit for the answer token.
- Output: ranked list of components carrying the distinction.
- Pre-registered prediction: a small set of attention heads (≤ ~10) and at most a few MLP blocks carry the bulk of the distinction, concentrated in the compression-zone layers.

## Lens 4 — persistent homology (topological)

- Construction: point cloud of per-stimulus residual-stream vectors (one per stimulus per layer per condition).
- Filtration: Vietoris-Rips on cosine distance.
- Output: persistence barcodes (H0 and H1) per layer per condition.
- Pre-registered prediction: topological signatures for psychological vs technical vs novel conditions converge in the compression zone (under B1/B2) or diverge (under A/C). What "convergence" means must be operationalised pre-registration — current placeholder is "Wasserstein distance between barcodes is significantly lower in the compression zone than in earlier layers, with bootstrap CIs not overlapping".

## Convergence criterion

Evidence is strongest when all four lenses point to the same set of layers. Specify the falsification rule: e.g. "if the components identified by activation patching do not overlap with the ID-compression zone, the framework's claim of methodological convergence is not supported on this model". This must be locked before running.

## Recursive OOD probe (B1 vs B2)

This step is load-bearing for distinguishing B1 and B2 and must not be dropped. Specify:

- The OOD generalisation test applied to the candidate shared circuit (e.g. patching the circuit's components into stimuli with novel agent types / novel substrates).
- The signature that distinguishes "primitive" from "interpolator" (e.g. degradation curve vs OOD distance, or compositional behaviour under multi-condition combinations).
- The pre-committed thresholds.

This is the most attackable part of the design. Defending it requires more than handwave — finalise the operationalisation before pre-registration.

## Multiple comparisons

Across lens × layer × condition the search space is large. Specify in advance:

- Whether the ID compression zone is identified per-model from the data, or fixed by hypothesis.
- Correction strategy (Bonferroni / FDR / permutation-based, depending on the test).
- Whether each lens result is weighted equally or hierarchically.

## Reporting

- All analysis runs versioned (random seed, model checkpoint, code commit hash).
- Negative results reported with the same prominence as positive results.
- Place a `RESULTS.md` next to this file once any pilot has been run.
