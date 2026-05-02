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
5.4 Recursive OOD probe — specifies the B1/B2 discriminator. The position paper presents the probe as a planned analysis pre-registered for downstream execution; it **does not claim to have run the probe**. Operational thresholds and falsification rules live in `prereg/prereg.md` § "Recursive OOD probe". The position paper's argument here is methodological: *this* is the right discriminator to specify, and *this* is what its locked-in form looks like in the prereg. Decision rationale: option 3 from CHANGELOG 2026-05-02 (P2 resolution) — design infrastructure framing requires the prereg to be the executable contract.

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

Anticipated objections and replies:

### *"B1 and B2 are still behaviourally indistinguishable in real deployments."*

The recursive OOD probe is a diagnostic, not a deployment monitor. It is run under controlled conditions with chosen stimuli and chosen patching interventions, in the same status as any mechanistic-interpretability finding — probes, activation patching, intrinsic-dimension estimation are all offline analyses on selected inputs. The B1/B2 distinction informs what the model is computing, not what label to attach to its outputs at runtime.

The diagnostic value translates downstream rather than directly. A model best characterised by B2 (an interpolator) has a known failure-mode shape: graceful degradation as inputs move further from the trained distribution, with no informative breakpoint to monitor. A B1-characterised model has a different shape: structurally informative breakdowns at compositional boundaries. Engineers monitoring deployed systems get different signals to attend to depending on which characterisation a model carries. The B1/B2 distinction therefore generates engineering-relevant predictions even though it is not itself an engineering tool.

### *"Linear-probe success is just feature presence, not computation."*

True for the linear-probe lens individually, and exactly the reason the framework requires four-lens convergence rather than treating any single lens as decisive.

Each lens has a known failure mode where it would falsely claim structural reality:

- **Linear probing.** Succeeds when a feature is linearly recoverable at a layer, regardless of whether the model causally uses it for downstream computation. A model can encode many features it never acts on; probe success alone cannot rule this in or out.
- **Intrinsic-dimension estimation.** Contraction can reflect normalisation artefacts — RMS-norm or LayerNorm push the residual stream onto a sphere, producing apparent dimension reduction that is geometric bookkeeping, not computational discretisation.
- **Activation patching.** Identifies components causally necessary for the measured behaviour but cannot, by itself, distinguish a compositional-primitive implementation from a lookup-table implementation that happens to produce the same answer on the tested inputs.
- **Persistent homology.** Sensitive to point-cloud sampling. Apparent topological structure at small N may be a sampling artefact; barcodes can be unstable under resampling.

These failure modes are mutually independent. Probe-detects-presence-only is orthogonal to ID-contraction-is-a-norm-artefact, which is orthogonal to patching-cannot-distinguish-primitive-from-lookup, which is orthogonal to PH-sampling-noise. For the four lenses to falsely converge on the same computational locus, four independent failure modes would have to align in a structured way that produces the same false positive — and the joint probability of structured alignment across independent failure modes is sharply lower than the probability of any individual failure.

The convergence requirement is therefore not "all four lenses agreed" but "all four lenses agreed in a way that joint failure would require an implausibly structured coincidence". Where lenses *fail* to converge — for instance, probe success without patching effect — that itself is the diagnostic: feature is present but not computationally engaged, which is the deflationary case the objection rightly identifies. The framework discriminates feature-presence from computation precisely by requiring patching evidence in addition to probe evidence, with both anchored to the same layer indices identified by the geometric and topological lenses.

### *"Topological methods are noisy on small samples."*

The prediction is convergence across lenses; topology is corroborative, not load-bearing. The topology lens is included because it is sensitive to structural features that linear probes miss — barcodes capture cycle structure and connectivity that linear separability cannot detect — and because its failure modes are independent of the other three lenses (the previous reply). Where topology agrees with the other three on the locus, the joint signal strengthens; where topology disagrees, the joint signal weakens but the framework can still adjudicate from the other three.

Sample-size concerns are addressed in the analysis plan (see `analysis/plan.md`): bootstrap resampling for barcode confidence intervals; pre-committed thresholds for what counts as "distinct" topology that account for sample-size effects; per-layer Wasserstein-distance comparisons rather than absolute barcode features. The pre-registration commits the noise floor before the data is run.

A remaining open call is whether to drop the topology lens from the primary analysis if pilot results on the small-model template indicate the lens fails to produce stable signal at the planned stimulus-set size. This is preferable to inflating claims with a noisy lens; reported as a possible deviation in the prereg.

## 10. Limitations and caveats

- Convergence-as-warning: agreement between methods can also reflect shared confounds.
- Compute scope: the full experiment requires resources beyond what we can pilot.
- Stimulus naturalness: matched stimuli are artefactually constrained; real-world ToM is messier.
- B1/B2 distinguishability may itself be model-scale-dependent.

## 11. Conclusion

Restate the methodological contribution; identify the next experiments (alternative novel-stimulus families; cross-model comparison; scaling the recursive probe).

Close with the handoff framing: this paper specifies a research programme; the prereg is the executable contract; the implementation template is the working pipeline. Downstream researchers — human or agentic — with appropriate compute are the intended executors. Cite the repository and DOI explicitly so the handoff is locatable.

---

## Open structural calls

- ~~Whether the recursive OOD probe is in-paper or a companion paper.~~ **Resolved 2026-05-02 (P2): option 3 — prereg-only, position paper argues for the programme.** See CHANGELOG.
- Whether to include a worked pilot result on Pythia-160M as an in-paper figure or only as a code template.
- Workshop vs full TMLR submission. Workshop forces brevity, may help discipline the exposition.
