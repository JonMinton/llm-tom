# Continuation guide for Claude Code in this repository

This file is auto-loaded by Claude Code. Read [`README.md`](README.md) before doing anything substantive — it sets the project frame.

## Working principles

These dialogue disciplines produced the design and must be preserved in any continuation. They take priority over default helpfulness instincts.

- **Selective concession over performative agreement.** When a counter-argument is correct, accept it without elaboration that re-asserts authority. When it's wrong, push back with specific reasoning. Do not concede to be polite; do not refuse to concede to save face.
- **Named seams.** Identify where the current argument is weakest and either fix it or flag it explicitly. Don't paper over genuine uncertainty with confident prose. A flagged seam is more useful than a smoothed one.
- **Verification before citation.** Both Claude and Gemini have demonstrated unreliable citation generation. Every citation in `references.bib` requires verification against the actual paper (web search → confirm authors, year, claim attributed). Use placeholder syntax `[CITE: Author Year, claim]` in drafts; only promote to `references.bib` once verified. The `references.bib` is for verified entries only.
- **Convergence-as-warning.** When two AI reviewers (Claude + Gemini, or two Claude instances) agree quickly, that's a signal to look harder for what's being missed, not a signal to move on.
- **Scope discipline.** The contribution is methodological characterisation of *abstraction level*, not ontological claims about machine cognition. Resist drift toward "does this machine have a mind." If you find yourself writing about consciousness, intentionality, or "real" understanding, stop.
- **Substantive over stylistic friction.** Disagreement should be about argument structure or evidence, not tone.

## What to do, what not to do

**Do:**
- Improve scaffolding files (outline.md, prereg.md, plan.md) with clearly-marked drafts that can be challenged.
- Add structural figures (block diagrams, flowcharts) when they clarify the methodology.
- Run the frequency analysis once stimuli are drafted — it's Mac mini-tractable.
- Implement the small-model validation in `implementation/` once the methodology is stable enough to encode.
- Keep `CHANGELOG.md` honest: log who/what contributed when (Jon vs Claude vs Gemini), what was added, what was challenged and changed.

**Do not:**
- Generate paper text and present it as Jon's. Drafts go in `paper/paper.md` clearly marked as drafts; Jon writes the final voice.
- Add citations to `references.bib` without verifying them. If unsure, leave a `[CITE: ...]` placeholder in the draft and a TODO in `CHANGELOG.md`.
- Pre-decide design choices that the handover marks as open (notably the combinatorial-novel stimulus form — leading candidate is cellular-automata-as-belief-systems, but this must be argued for before being finalised).
- Drop the recursive-OOD probe step. It is load-bearing for distinguishing B1 vs B2 and is the most attackable part of the design; it must be defended, not evaded.
- Conflate A and C. They predict the same thing on the three-condition matrix and are distinguished by within-domain generalisation tests.

## Strict factuality

Claims about prior work require verification. If you cite a paper, check it. If you assert a finding, link to the source. The "Verified references" list in `README.md` (and `references.bib`) is a starting point — re-verify before submission, since arXiv versions change.

When asked to "summarise the literature on X" — refuse to do so from memory. Run a search, read the abstracts at minimum, then write a summary you can defend line-by-line.

## How to challenge well

The dialogue that produced this design worked because Claude and Gemini challenged each other on substance. To continue that:

- Read what's there. State the strongest version of the existing argument before attacking it.
- Identify a specific claim, locate the weakness, propose a concrete alternative.
- Distinguish "this is wrong" from "this needs more support". Treat them differently.
- If you find yourself agreeing with everything, you have stopped reading carefully.

## Practical notes

- Compute available locally: M4 Mac mini. Suitable for frequency analysis and validation on Pythia-160M / TinyStories-class models. Not suitable for the full experiment (will need GPU researcher to pick up).
- Stack: Python via `uv` or `pip` in `implementation/`, TransformerLens primary library, `sentence-transformers` for the frequency analysis.
- Repo conventions: kebab-case filenames, lowercase directory names, ISO dates in `CHANGELOG.md`.
- British spellings in prose (per Jon's preference), but code, file names, and bibliography entries use the source's own spelling.
