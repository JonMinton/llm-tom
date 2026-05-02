---
status: scaffold
target_length: 8000–12000 words (TMLR-style); shorter workshop version possible
last_update: 2026-05-02
---

# Position paper — outline

This is a section-and-claims scaffold derived from the handover. Each section is named with its load-bearing claim. Order, length, and titles are open for challenge — the claims are not.

## 1. Introduction

**Claim.** "Do LLMs have Theory of Mind?" is an underdetermined question that conflates levels of abstraction. The productive question is: *at what level of abstraction is the model operating, and where is the corresponding mechanism?* This paper proposes a methodology for adjudicating that question via convergence across independent lenses.

Open with a worked example showing how the same Sally-Anne success can be consistent with multiple incompatible cognitive architectures (modular ToM module / abstract divergent-state primitive / pattern-matched narrative completion). Argue this is not a deflationary point but a methodological one.

## 2. Related work and the gap

**Claim.** Existing ToM-in-LLMs work falls into two camps — behavioural success/failure papers (Kosinski-style) and mechanistic-interpretability papers — without a connecting framework that asks *which level of computational abstraction* the observed behaviour is happening at.

Cover briefly: ToM benchmarking, Sally-Anne probes, mech-interp circuits (IOI, ACDC), intrinsic-dimension geometric work, persistent-homology approaches. The gap is methodological, not empirical.

## 3. Theoretical framework: levels of abstraction

**Claim.** The four-hypothesis space (A, B1, B2, C) is the smallest set that captures the genuine alternatives. A and C predict identically on the three-condition matrix (handles ambiguity that pure behavioural studies cannot).

Define the four hypotheses precisely. Use the prediction matrix in `analysis/prediction_matrix.csv`. State the reason this maps cleanly to abstraction level: A and C are level-mismatched in different directions; B1 and B2 differ in *kind* of abstraction.

## 4. Methodology: convergence across lenses

**Claim.** Structural reality in interpretability is what survives across methodologically independent frames. Convergence across geometric, behavioural, causal, and topological lenses on the same computational locus is the standard.

Subsections per lens:

- 4.1 Geometric (intrinsic dimension) — TwoNN/GRIDE; expand-then-compress prediction.
- 4.2 Behavioural (linear probing) — per-layer separability rises in compression zone.
- 4.3 Causal (activation patching) — circuit identification.
- 4.4 Topological (persistent homology) — non-adversarial application of Fay et al. methodology.

For each: what the lens measures, what its known limits are, why it's not redundant with the others.

## 5. Stimulus design

**Claim.** The three-condition matrix (psychological / technical / combinatorially novel) is the minimum set required to distinguish A vs B vs C, and the recursive OOD probe is the minimum addition required to distinguish B1 vs B2.

5.1 Psychological — Sally-Anne false-belief / true-belief, matched on syntax / character count / event structure.
5.2 Technical — State-Rollback isomorphism. Argue mathematical equivalence to false-belief.
5.3 Combinatorially novel — substrate-composition novelty. Defend why CA-as-belief-systems (or whatever final form) is OOD-in-the-right-way and not surface weirdness. **This section is the most attackable; treat it accordingly.**
5.4 Recursive OOD probe — what's tested, what counts as the primitive vs interpolator signature. **Equally attackable; do not handwave.**

## 6. Frequency analysis

**Claim.** OOD claims about pre-training distribution must be empirically grounded, not asserted. The protocol in `analysis/frequency_analysis/` operationalises this.

Briefly summarise the protocol; report results when available.

## 7. Pre-specified analysis plan

**Claim.** The methodology is pre-registered with falsification rules. See `analysis/plan.md` and the OSF prereg.

This section is short — pointer rather than re-statement.

## 8. Implementation template

**Claim.** The methodology executes on a small open-weight model. The implementation in `implementation/` validates the pipeline runs end-to-end without making strong claims about the small model's cognition.

Pointer to the repo; describe what the template demonstrates and what it does not (it does not claim Pythia-160M has ToM).

## 9. Discussion

**Claim.** The framework is descriptive of *abstraction level*, not normative about cognition. We do not claim machines have minds; we claim machines have computational primitives at characterisable levels of abstraction, and offer a method for characterising them.

Address the obvious objections:

- "B1 and B2 are still behaviourally indistinguishable in real deployments" — reply: the recursive OOD probe is a *diagnostic*, not a deployment criterion.
- "Linear-probe success is just feature presence, not computation" — reply: the four-lens convergence requirement is precisely how we avoid this trap.
- "Topological methods are noisy on small samples" — reply: the prediction is convergence of signal across lenses; topology is corroboration, not the sole evidence.

## 10. Limitations and caveats

- Convergence-as-warning: agreement between methods can also reflect shared confounds.
- Compute scope: the full experiment requires resources beyond what we can pilot.
- Stimulus naturalness: matched stimuli are artefactually constrained; real-world ToM is messier.
- B1/B2 distinguishability may itself be model-scale-dependent.

## 11. Conclusion

Restate the methodological contribution; identify the next experiments (alternative novel-stimulus families; cross-model comparison; scaling the recursive probe).

---

## Open structural calls

- Whether the recursive OOD probe is in-paper or a companion paper (currently in-paper).
- Whether to include a worked pilot result on Pythia-160M as an in-paper figure or only as a code template.
- Workshop vs full TMLR submission. Workshop forces brevity, may help discipline the exposition.
