# Adjudicating Algorithmic Theory of Mind in LLMs

A research-design project: methodology for adjudicating Level-2 algorithmic equivalence in LLM Theory of Mind, via convergence across mechanistic, geometric, behavioural, and topological lenses.

**Status:** design-proposal stage. No experiments have been run. This repository will host the position-paper draft, OSF pre-registration, stimuli, analysis plan, and an end-to-end implementation template intended to validate the methodology on a small model (Pythia-160M class).

**Principal investigator:** Jon Minton (statistician, Edinburgh). M4 Mac mini available for pilot work and frequency analysis; full-scale experiment intended to be picked up by researchers with appropriate compute.

## Intended outputs

1. A position paper articulating the methodological framework — target arXiv preprint and TMLR / workshop track.
2. An OSF pre-registration specifying hypotheses, stimulus design, analysis plan, and success criteria.
3. An implementation template on GitHub with TransformerLens-based code that runs end-to-end on a small model, validating that the methodology executes correctly.
4. A Zenodo archive of the bundle with a DOI, cross-linked to the above.

## Strategic bet

As agentic AI capability increases over coming weeks and months, well-specified experimental designs become disproportionately valuable infrastructure. The contribution here is a rigorously specified design that a downstream researcher — human or agentic — can pick up and execute, not a finished experimental result.

This makes machine-readability a load-bearing design constraint, not a stylistic preference:

- The prediction matrix lives as CSV, not as a prose table buried in the paper.
- The pre-registration is the **canonical executable spec** for the experiment; the position paper argues for *why this spec* without duplicating it.
- Falsification rules and operational thresholds in the prereg are intended to be precise enough that an agent with compute can convert them into running code without further design choices.
- The implementation template is intended to *run end-to-end* on a small model, demonstrating that the pipeline is real rather than gestural.

A downstream agent picking up this repo should treat `prereg/prereg.md` as the contract, `paper/paper.md` (when drafted) as the argument, and `implementation/` as the working pipeline.

## How this project came to exist

This design emerged from an unusually productive AI-mediated dialogue between a Claude 4.7 instance and a Google Gemini instance, with Jon as arbiter, beginning with a game of 20 Questions and progressing through philosophy of mind, mechanistic interpretability, and experimental design. The dialogue's discipline — selective concession, named seams, willingness to retract, verification before citation — is the working principle to preserve in continuation. The full transcript is available on request from Jon.

The continuation discipline is captured in [`CLAUDE.md`](CLAUDE.md), which Claude Code auto-loads. Any future Claude session in this repo should read it.

## Theoretical framework

The project's core contribution is methodological. Rather than asking the underdetermined question "do LLMs have Theory of Mind," it asks: what level of abstraction is the LLM operating at when it solves ToM tasks, and can we localise the corresponding computational mechanism?

This reframing avoids the Fodorian trap of expecting symbolic compositionality in distributed neural representations, while also avoiding the deflationary collapse that treats all neural-network behaviour as sophisticated pattern completion. The intermediate position: LLMs may have acquired computational primitives at varying levels of abstraction, and these primitives are empirically characterisable via methodological triangulation across mechanistic, geometric, and behavioural lenses.

### Four-hypothesis space

The experiment is designed to discriminate:

- **Hypothesis A — Domain-specific ToM.** Model has a modular psychology-specific ToM circuit. Predicts: ToM bottleneck fires for psychological stimuli only.
- **Hypothesis B1 — Strong abstraction.** Model has a substrate-independent abstract primitive for divergent-state representation. Predicts: bottleneck fires across psychological, technical, and combinatorially novel stimuli, AND the circuit shows compositional-primitive signature under further OOD probing.
- **Hypothesis B2 — Sophisticated cross-domain interpolation.** Model has a shared circuit spanning multiple domains but it is itself an interpolator, not a primitive. Predicts: bottleneck fires across all three stimulus types but shows interpolator signature under recursive OOD probing.
- **Hypothesis C — Deflationary.** Model uses domain-specific pattern matching for each task type. Predicts: different circuits fire for different stimulus types.

B1 and B2 are behaviourally indistinguishable on the three-condition stimulus matrix; distinguishing them requires probing the candidate shared circuit's own generalisation behaviour. This recursive aspect is load-bearing for the paper's argument and must not be dropped.

Tabular form: [`analysis/prediction_matrix.csv`](analysis/prediction_matrix.csv).

## Methodological apparatus

The experimental design rests on convergence across methodologically independent lenses, following the principle that "objective structure" in interpretability is whatever survives across multiple frames of reference. The agreed lenses:

1. **Geometric — intrinsic dimension.** Layer-wise ID estimation via TwoNN and GRIDE, following Joshi et al. (2025) "Geometry of Decision Making in Language Models" and the related Geometry-of-Tokens work. Expected signature: ID expands in early-middle layers and compresses in later layers (operational discretisation).
2. **Behavioural — linear probing.** Train linear probes at each layer for the ToM-relevant distinction. Expected signature: linear separability rises sharply in the compression zone.
3. **Causal — activation patching.** Following Conmy et al.'s automated circuit discovery and the IOI methodology. Patch individual attention heads and MLP blocks between conditions to identify components carrying the ToM distinction.
4. **Topological — persistent homology.** Following Fay et al. (2025) "The Shape of Adversarial Influence" methodology, applied in a non-adversarial setting. Construct point clouds of stimulus-condition vs control activations at each layer; compute persistence barcodes; ask whether topological signatures change at the layers where ID compression and linear separability emergence co-occur.

Convergence across all four lenses on the same computational locus is the standard for evidence of structural reality rather than methodological artefact.

## Stimulus design

Three-way comparison structure (see [`stimuli/`](stimuli/) for full specification as it is finalised):

1. **Psychological condition.** Sally-Anne style narratives with matched epistemic structure across false-belief and true-belief variants. Matched syntactic complexity, character count, event structure; only the epistemic dependency differs.
2. **Technical condition.** State-Rollback isomorphism. System snapshot at T1, hidden migration at T2, recovery protocol at T3 must determine which server to query. Mathematically isomorphic to false-belief task but in non-psychological domain.
3. **Combinatorially novel condition.** Substrate-composition novelty. Specific form to be finalised — leading candidate is cellular-automata-as-belief-systems, where cell states encode beliefs about neighbouring cells' states updated by non-trivial rules, with divergent-state structure emerging from automaton dynamics rather than narrative specification. Other candidates considered and rejected: surface notation variants (fail because early layers translate alien notation back to standard semantics before reaching the bottleneck), non-standard update rules (fail because they reduce to compositions of well-trained primitives like negation and belief-attribution).

The combinatorial novelty must achieve OOD-in-the-right-way: structural composition the model couldn't have abstracted from training, not surface-level weirdness that breaks the model for unrelated reasons.

## Frequency analysis prerequisite

The argument that State-Rollback is in-distribution and Combinatorially Novel is OOD requires empirical grounding rather than intuition. See [`analysis/frequency_analysis/`](analysis/frequency_analysis/) for the full protocol.

In summary:

- **Corpus:** 50–100 GB random sub-sample of Dolma or RedPajama.
- **Protocol:** 50 variations per stimulus type; embed via lightweight model (e.g. `all-MiniLM-L6-v2`); compute centroid vectors; chunk corpus, embed chunks, compute cosine similarity against centroids; pull top 1000 matches per category.
- **Threshold:** State-Rollback declared in-distribution if it appears with frequency and similarity comparable to Psychological. Combinatorially Novel declared OOD if it returns near-zero high-similarity structural matches.
- **Supplementary:** Embedding-based similarity may miss structural isomorphism. Supplement with structural matching on dependency-parse or AST representations for high-priority comparisons.

This analysis is suitable for the M4 Mac mini and is a prerequisite for the position paper's argument being sound, not just for the experiment.

## Repository structure

```
.
├── README.md                  # This file
├── CLAUDE.md                  # Continuation discipline (auto-loaded by Claude Code)
├── CHANGELOG.md               # Provenance log of contributions
├── references.bib             # Verified citations only
├── paper/
│   ├── paper.md               # Working manuscript draft
│   ├── outline.md             # Section structure and key claims
│   └── figures/               # Reproducible figure-generation scripts
├── prereg/
│   └── prereg.md              # OSF pre-registration draft
├── stimuli/
│   ├── README.md              # Stimulus design overview
│   ├── psychological/         # Sally-Anne variants
│   ├── technical/             # State-Rollback variants
│   └── novel/                 # Combinatorially novel stimuli
├── analysis/
│   ├── prediction_matrix.csv  # Tabular form of the four-hypothesis predictions
│   ├── plan.md                # Pre-specified analysis plan
│   └── frequency_analysis/    # Corpus frequency verification
└── implementation/
    ├── README.md              # How to run the template
    ├── pyproject.toml         # Dependencies
    ├── src/                   # TransformerLens-based code
    └── tests/                 # Validation on small models
```

## Immediate next steps

1. Run the frequency analysis on the candidate stimuli (Mac mini-tractable).
2. Finalise the combinatorially novel stimulus design specification.
3. Draft the position paper outline (sections, claims, target length) — see [`paper/outline.md`](paper/outline.md).
4. Begin section-by-section drafting with Gemini review at structural milestones.
5. In parallel, draft the pre-registration to discipline the paper's specificity — see [`prereg/prereg.md`](prereg/prereg.md).
6. In parallel, build the implementation template skeleton, validate on Pythia-160M or similar.

## Caveats

- The design has not been pilot-tested. Holes likely exist that dialogue could not surface.
- Citation hygiene was good as of 2 May 2026 but should be re-verified before submission.
- The combinatorially novel stimulus form is the most under-specified element and the highest-priority item to finalise.
- The B1/B2 distinction is the most argumentatively delicate part of the paper and requires the most careful exposition.

## Authorship and attribution

Per arXiv and standard journal policy, LLMs cannot be named authors. The paper's named author(s) will be Jon Minton and any human collaborators. Methodology and acknowledgement sections will document AI contribution honestly: the design emerged from dialogue between Claude 4.7 and Gemini, with Jon as arbiter. Code generation and drafting will continue with significant Claude Code involvement, again documented in acknowledgements. See [`CHANGELOG.md`](CHANGELOG.md) for a running provenance log.

## Licences

Dual-licensed by content type.

- **Textual content** (Markdown files, prediction-matrix CSV, README, CHANGELOG, REVIEW) — [Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE). Share and adapt with attribution to Jon Minton.
- **Implementation code** (Python source under `implementation/`, plus any code that lands in `analysis/frequency_analysis/scripts/` or elsewhere) — [MIT License](implementation/LICENSE).

When citing or building on this work, attribution to Jon Minton (and any future named collaborators) is requested. External use should preserve existing licence notices.
