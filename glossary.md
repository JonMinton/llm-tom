# Glossary

**Status: living document.** Acronyms and key terms used across the design dialogue, the prereg, and the implementation. Plain-language gloss first; precise definitions live in the prereg and paper. Where a term names a paper/circuit, the citation still requires verification before entering `references.bib` (per CLAUDE.md).

## The four hypotheses (what the experiment adjudicates)

| Term | Meaning |
|------------------------------------|------------------------------------|
| **A** | *Domain-specific ToM.* The model has a modular, psychology-specific Theory-of-Mind circuit. Fires for psychological stimuli only. |
| **B1** | *Strong abstraction.* The model has a substrate-independent abstract **primitive** for representing *divergent state*. Same circuit fires across psychological, technical, and novel stimuli — and behaves like a genuine compositional primitive under further probing. |
| **B2** | *Sophisticated cross-domain interpolator.* Same cross-domain firing as B1, but the shared circuit is an **interpolator** over the training distribution, not a clean primitive. Distinguished from B1 only by the recursive OOD probe. |
| **C** | *Deflationary.* Domain-specific pattern-matching; different circuits fire for different stimulus types. |

## Core concepts

| Term | Meaning |
|------------------------------------|------------------------------------|
| **ToM** | Theory of Mind — attributing mental states (beliefs, knowledge) to agents. |
| **Divergent state** | The structural feature that an agent's belief about X may differ from the actual state of X. The abstraction B1/B2 may have captured. |
| **OOD** | Out-of-distribution — inputs unlike the training data. The *recursive OOD probe* is the step that separates B1 from B2. |
| **Sally-Anne** | The classic false-belief task (psychological condition). |
| **State-Rollback** | The technical condition: a system snapshot → hidden migration → recovery protocol, mathematically isomorphic to a false-belief task. |
| **CA** | Cellular Automata — the leading candidate for the *combinatorially novel* condition (cell states encode beliefs about neighbours, updated by non-trivial rules). |
| **Marr's levels** | Marr's three levels of analysis: computational (what/why) / algorithmic (how, representation) / implementational (physical). The project asks *which level* the LLM operates at. |

## The four interpretability lenses (convergence across these = evidence)

| Term | Meaning |
|------------------------------------|------------------------------------|
| **ID** | Intrinsic Dimension — the geometric lens; estimates the effective dimensionality of the residual stream per layer. |
| **TwoNN / GRIDE** | Two specific intrinsic-dimension estimators. |
| **Linear probing** | The behavioural lens — train a linear classifier per layer for the false/true-belief distinction; tracks where the feature becomes linearly separable. |
| **Activation patching** | The causal lens — swap activations of individual components (attention heads, MLP blocks) between conditions to localise which carry the distinction. |
| **ACDC** | Automated Circuit DisCovery — an automated method for finding the minimal circuit (associated with Conmy et al.; *verify before citing*). |
| **IOI** | Indirect Object Identification — a well-studied benchmark task/circuit in mech-interp, used as a reference point for effect sizes (associated with Wang et al.; *verify before citing*). |
| **Persistent homology / barcodes** | The topological lens — track topological features of activation point-clouds across layers. |

## P3 operationalisation terms (B1-vs-B2 quantitative signatures)

| Term | Meaning |
|------------------------------------|------------------------------------|
| **DM** | Dependent Measure — the quantity measured along the probe axis. |
| **NCME** | Normalized Causal Mediation Effect — the chosen DM: `(L_patched − L_corrupted) / (L_clean − L_corrupted)`. How much patching the candidate circuit restores correct behaviour, normalised to \[0,1\]. |
| **L_clean / L_patched / L_corrupted** | The logit difference (correct − incorrect state-query token) under, respectively, the clean run, the run with the candidate circuit patched in, and the corrupted run. |
| **IA** | Independent Axis — the dimension along which B1 and B2 are predicted to diverge. |
| **IA-α** | Compositional depth (1, 2, 3… nested compositions of the primitive). |
| **IA-β** | Distance from training distribution (semantic-embedding distance). |
| **IA-β\*** | Gemini's variant: *Normalized Structural-Semantic Distance* from pre-training distribution (a composite Claude argues should be decomposed). |
| **IA-γ** | Substrate distance (psychological → technical → CA → further). |
| **IA-ε** | Pragmatic-stance distance — vary the represented agent's utility/stance (collaborative vs literal vs adversarial); derived from the 20-Questions game. |
| **IA-δ** | An explicit combination of the above axes. |
| **D_M** | Mahalanobis distance — the metric in which the independent axis X is measured. |
| **V** | Logical-validity axis (binary) — Claude's proposed second factor, crossing with substrate-distance to give a 2×3 factorial instead of a single composite. |
| **m_B1 / m_B2** | The predicted regression slopes of NCME against X under B1 / B2. |
| **S_valid** | Observed linear slope of NCME across the valid range (X∈\[0,8\]). |
| **R_drop** | Ratio of the NCME drop at the corrupted boundary to the total NCME drop across the valid range. |
| **τ (tau)** | ACDC's edge-attribution threshold — controls how many components enter the candidate circuit. |
| **Breakpoint / step-collapse** | The discrete-primitive (B1) signature: a sharp local drop at the compositional boundary. |
| **Asymptote** | The tail value NCME approaches at maximum distance (a contested B2 parameter). |

## Models, compute, corpora, infrastructure

| Term | Meaning |
|------------------------------------|------------------------------------|
| **TransformerLens** | The primary mechanistic-interpretability library for the implementation. |
| **Pythia-160M / Pythia-2.8B** | Small models for pilot/validation work (Mac-mini-tractable). |
| **TinyStories** | A class of very small language models. |
| **Llama-3-8B** | A candidate model for the main experiment (raises quantisation concerns at 4/8-bit). |
| **GPT-2 small** | A reference model size for published effect-size comparisons. |
| **M4 Mac mini** | Jon's local compute — frequency analysis + small-model pilots only. |
| **Dolma / RedPajama / C4 / Pile** | Pre-training corpora used in the frequency analysis (in-distribution vs OOD grounding). |
| **all-MiniLM-L6-v2** | Lightweight sentence-embedding model used in the frequency analysis. |
| **OSF** | Open Science Framework — host for the pre-registration. |
| **Zenodo** | Archive that mints a DOI for the bundle. |
| **arXiv / TMLR** | Preprint server / Transactions on Machine Learning Research — target venues. |
| **prereg** | Pre-registration — the canonical executable spec (`prereg/prereg.md`). |

## Statistics

| Term          | Meaning                                              |
|---------------|------------------------------------------------------|
| **CI**        | Confidence Interval.                                 |
| **Bootstrap** | Resampling to estimate CIs around slopes/asymptotes. |