# P3 cross-bot review prompt

**Purpose.** This file is the canonical standardised prompt for the P3 cross-bot review of the B1/B2 operationalisation. Per the project's convergence-as-warning discipline, the same prompt is to be sent in parallel to multiple frontier model families (recommended: Claude Opus 4.7, Gemini current-flagship, GPT-5 or current OpenAI flagship — *not* Codex; see CHANGELOG 2026-05-02 for rationale). Each bot's response is dropped into a sibling file (`p3-claude-draft.md`, `p3-gemini-draft.md`, `p3-gpt5-draft.md`). Jon synthesises across the three.

**Dispatch instructions for Jon.** Paste everything below the horizontal rule into each target bot's chat interface as the *first message in a new conversation* (no prior context). Use a fresh chat per bot — don't continue an existing thread. Save the bot's full response into the corresponding stub file under this directory. Once all three drafts are in, do a synthesis pass.

**What to look for during synthesis.**

- **Convergence on the same quantitative shape across all three bots.** This is the strongest evidence the operationalisation is right. Treat with the convergence-as-warning caveat: shared assumptions about typical interpretability practice may produce shared answers without the answers being correct.
- **Divergence on the choice of dependent measure or independent axis.** Likely the most informative source of insight — exposes the design space's genuine open calls.
- **Divergence on threshold values where bots agree on shape.** Expected; threshold values are often pilot-anchored in any case.
- **Common assumptions across bots' Section 8.** These are the project's hidden assumptions surfaced; flag explicitly in the prereg.
- **Open gaps that all bots flag in Section 9.** These are the genuine remaining unknowns — natural seeds for follow-up work.

**Editorial discipline reminder.** Per `../../CLAUDE.md`: do not paraphrase the bots' drafts when synthesising. Quote the load-bearing sentences verbatim and attribute them. The synthesis is Jon's; the bot outputs are evidence.

---

You are being consulted as part of a multi-bot independent review. The same prompt is being sent in parallel to several frontier language models from different vendors. Please answer self-sufficiently from this prompt alone. Do not ask follow-up questions. Where information is missing, make assumptions explicit (Section 8) rather than seeking clarification.

## What the project is

A research design (not yet executed) for adjudicating the *level of computational abstraction* at which a large language model solves Theory-of-Mind tasks. The contribution is methodological: a framework for distinguishing, via convergence across multiple interpretability lenses, between four hypotheses about what a successful LLM is doing when it answers a Sally-Anne-style false-belief question.

## The four hypotheses

The pre-registered alternatives:

- **A — Domain-specific ToM.** The model has a modular psychology-specific Theory-of-Mind circuit. Prediction: the relevant computational bottleneck activates for psychological stimuli only.
- **B1 — Strong abstraction.** The model has acquired a substrate-independent abstract primitive for representing *divergent state* — the structural feature that an agent's belief about X may differ from the actual state of X. Prediction: the same circuit fires across psychological, technical (system state-rollback), and combinatorially novel stimuli that share the divergent-state structure, AND under further out-of-distribution probing the circuit shows the signature of a genuine compositional primitive.
- **B2 — Sophisticated cross-domain interpolator.** The model has a shared circuit spanning multiple domains, but it is itself an *interpolator* over the training distribution rather than a clean compositional primitive. Same predictions as B1 on the three primary stimulus conditions; diverges from B1 only under further OOD probing, where it shows interpolator signature rather than primitive signature.
- **C — Deflationary.** Domain-specific pattern-matching for each task type. Prediction: different circuits fire for different stimulus types.

A and C make identical predictions on the three primary stimulus conditions and are distinguished by within-domain generalisation tests. **B1 and B2 also make identical predictions on the three primary conditions, and are distinguished only by the *recursive OOD probe* — the experimental step you are operationalising.**

## The recursive OOD probe

Once a candidate shared circuit has been identified via causal patching across the three primary conditions (psychological, technical, combinatorially novel), apply that circuit to a fourth stimulus set designed to push along an axis where B1 and B2 predict different behaviour.

The intuition is:

- A genuine compositional primitive operates cleanly within its compositional boundary and breaks at the boundary in a structurally informative way (e.g. step-function-like degradation when a non-primitive composition is required).
- An interpolator's behaviour is smooth in the metric space of training-distribution-distance — it degrades gracefully with distance and shows no structural breakpoints.

This intuition is too informal to pre-register. Operationalising it quantitatively is your task.

## The methodological apparatus

The experimental design uses four interpretability lenses, each producing per-layer per-condition outputs:

1. **Geometric** — intrinsic dimension estimation (TwoNN, GRIDE) of the residual stream.
2. **Behavioural** — linear-probe accuracy on the false-belief / true-belief distinction.
3. **Causal** — activation patching effect on next-token logit, measured per-component (per attention head, per MLP block).
4. **Topological** — persistent homology barcodes of per-stimulus residual-stream point clouds.

The recursive OOD probe re-uses lens 3 (activation patching) primarily, with optional cross-lens corroboration.

## Operationalisation space

The **dependent-measure (DM) space** for the recursive probe could be:

- **DM-i.** Patching-effect magnitude on next-token logit (causal, fine-grained, but circuit-restricted to the candidate components).
- **DM-ii.** Behavioural accuracy on the recursive-probe stimuli when the candidate circuit is patched in or ablated (causal, coarser, but tracks task success directly).
- **DM-iii.** Composite of i and ii (and how to combine them).
- **DM-other.** Argue for an alternative.

The **independent-axis (IA) space** — the dimension along which B1 and B2 diverge — could be:

- **IA-α.** *Compositional depth.* Test stimuli requiring 1, 2, 3, … nested or sequential compositions of the candidate primitive operation.
- **IA-β.** *Distance from training distribution.* Stimuli at increasing semantic-embedding distance from the corpus subspace covered by the original conditions.
- **IA-γ.** *Substrate distance.* Substrates at increasing remove from the trained ones (psychological → technical → cellular-automata-as-belief-systems → still further).
- **IA-δ.** Some explicit combination of the above (e.g. depth crossed with substrate).
- **IA-other.** Argue for an alternative.

You may pick any DM and IA combination, or argue for using more than one axis.

## Your task

Produce a quantitative operationalisation of the B1 vs B2 distinction suitable for OSF pre-registration. Specifically:

1. **Choose a dependent measure** and justify the choice in terms of what B1 and B2 actually predict differently along it.
2. **Choose an independent axis** and justify why B1 and B2 predict divergent behaviour along this axis specifically.
3. **State, quantitatively, the predicted signature for B1** along the chosen axis. By "quantitatively" I mean: at the level of slopes, breakpoints, asymptotes, and confidence-interval bounds. *"Step-function-like"* is not quantitative. *"The change in DM at the compositional boundary should be at least 3× the change at non-boundary distances of the same magnitude, with bootstrap 95% CI excluding 1.5×"* is quantitative. Hit this standard.
4. **State, quantitatively, the predicted signature for B2** along the same axis. Same standard.
5. **State the decision rule** that maps an experimental result to one of {B1 supported, B2 supported, inconclusive}. Specify what falls in the inconclusive zone explicitly.
6. **State the falsification rule** for the recursive probe as a whole — what experimental result would *falsify both* B1 and B2 (e.g. neither pattern emerges within CI), in which case the conclusion is that the methodology has not adjudicated B1/B2 on this model.
7. **Distinguish shape from threshold values.** The *shape* of each prediction may be derivable from theory; specific *threshold values* may require empirical anchoring from a pilot run. Be explicit about which of your numbers are theory-derived and which are pilot-anchored placeholders.
8. **Make assumptions explicit.** Any assumption you make about the model's training distribution, the candidate circuit's behaviour, the stimulus design, or the statistical properties of the dependent measure should be stated so a downstream reader can challenge it.
9. **Flag open gaps.** If your operationalisation has remaining ambiguities that you cannot resolve from the prompt alone, state them — do not paper over them.

## Response format

Please structure your reply with these section headings (verbatim) so three independent responses can be compared apples-to-apples:

```
## 1. Dependent measure
## 2. Independent axis
## 3. B1 predicted signature (quantitative)
## 4. B2 predicted signature (quantitative)
## 5. Decision rule
## 6. Falsification rule
## 7. Theory-derived vs pilot-anchored
## 8. Assumptions
## 9. Open gaps
```

Target length: 800–1500 words. Quantitative precision matters more than length.

## What is not being asked for

- A research plan or paper outline. The operationalisation is the deliverable.
- A literature survey, unless you draw on a specific paper for a specific quantitative claim.
- Speculation about whether B1 or B2 is more likely to be the true description of any extant model. Operationalise both equally rigorously.
- Hedging that "this depends on the model / setup / etc." — the prompt commits to the apparatus described above; operationalise within it.
