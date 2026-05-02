# Changelog

Provenance log. Each entry: date, contributor (human / Claude / Gemini), action, and where the change was challenged or accepted.

The point of this file is to keep AI contribution honest and traceable, per the authorship discipline in `README.md` and `CLAUDE.md`. Don't let it rot.

## 2026-05-02

- **Repository initialised.** Empty public GitHub repo `JonMinton/llm-tom` created.
- **Initial scaffolding committed** (Claude Code, supervised by Jon Minton).
  - `README.md` — handover document lightly adapted for repo presentation.
  - `CLAUDE.md` — continuation discipline extracted from the handover's "Working principles" section so it auto-loads in future Claude Code sessions.
  - `analysis/prediction_matrix.csv` — tabular form of the four-hypothesis prediction matrix from the handover.
  - `analysis/plan.md` — analysis-plan scaffold; pre-specified analysis pipeline placeholder.
  - `analysis/frequency_analysis/README.md` — protocol description for the corpus frequency check (prerequisite to the position paper's argument).
  - `paper/outline.md` — section-and-claims scaffold derived from the framework section; not the final structure, intended for challenge.
  - `paper/paper.md` — placeholder.
  - `prereg/prereg.md` — pre-registration scaffold matching OSF's standard sections.
  - `stimuli/README.md` — three-condition design overview; subdirectory placeholders for the three condition types.
  - `implementation/README.md`, `pyproject.toml` — TransformerLens-based template scaffold; no code yet.
  - `references.bib` — verified citations from the handover only; placeholders flagged.
  - `.gitignore`, `CHANGELOG.md` — boilerplate.
- **Not done deliberately:** no paper text drafted; no novel stimuli generated; no citations added beyond the handover's verified set; no implementation code; no licence chosen.
- **Open design calls flagged in scaffolding:**
  - Combinatorially novel stimulus form (CA-as-belief-systems is leading candidate, not finalised).
  - Target model(s) for validation pilot beyond "Pythia-160M class".
  - Whether the recursive-OOD probe is itself a within-paper experiment or a separate companion paper.

## 2026-05-02 — citation discipline correction

External review (`REVIEW.md`, added in this commit) flagged that three of the six entries in `references.bib` had hallucinated author names despite the file's "VERIFIED ENTRIES ONLY" header. Author names were independently re-checked against the canonical arXiv abstract pages on 2026-05-02 and the review's corrections were confirmed correct.

### Worked example of the failure mode

The handover document gave authors in initials-only form (e.g. "Fay, A., García-Redondo, I., Wang, Q., …"). When transcribed into `references.bib`, those initials were rendered into full names *from memory* rather than re-fetched from the source. This produced plausible but incorrect names — "Andrew Fay" instead of "Aideen Fay", "Qiang Wang" instead of "Qiquan Wang", "Meng-Hao Chen" instead of "Meng-Hsi Chen", and so on. The hallucinations were undetectable to the writer because the names were plausible.

This is the precise loophole the project's "verification before citation" discipline did not explicitly close. The discipline did catch it (an external reviewer flagged the issue) but only because verification was made adversarial; it would not have been caught by self-review.

### Corrections applied

- `fay2025shape`: Andrew → **Aideen**, Qiang → **Qiquan**.
- `chen2025rethinking`: Meng-Hao → **Meng-Hsi**, Yi-An → **Yu-Ang**.
- `liao2026revisiting`: Meng-Hao → **Meng-Hsi**, Guo-Tang → **Guan-Ting**.
- `joshi2025geometry`: previously had `[first names to verify]`; now filled in as **Abhinav Joshi, Divyanshu Bhatt, Ashutosh Modi** (verified against OpenReview `Jj4NdJtXwp` and arXiv:2511.20315).
- `geometry2025tokens` renamed to `viswanathan2025geometry` (lead-author cite key); previously had `[authors to verify]`; now filled in as **Karthik Viswanathan, Yuri Gardinazzi, Giada Panerai, Alberto Cazzaniga, Matteo Biagetti** (verified against arXiv:2501.10573).
- `janapati2024comparative`: already correct, no change.

Each verified entry now carries a `verified = {YYYY-MM-DD against <URL>}` field so the verification status is machine-readable and dated.

### Discipline tightening

- `references.bib` header rewritten to specify that verification means *verbatim copy from the canonical source*, not paraphrase from memory.
- `CLAUDE.md` "Strict factuality" section gained an "Author lists must be copied verbatim from the canonical source" subsection covering the specific failure mode (rendering initials into full names from memory).
- This entry serves as the worked example future contributors are pointed to.

### Scope note

This correction was triggered by an external chat-instance review, not by self-review. The convergence-as-warning principle therefore applies: even with the tightened rule, periodic adversarial review is part of the discipline, not an alternative to it.

## 2026-05-02 — `.gitattributes` for language indicator (cosmetic)

Added `.gitattributes` with `references.bib linguist-detectable=false` so the GitHub language bar reflects actual project content (markdown / Python) rather than reading "TeX 100%" off a single BibTeX file. Cosmetic only; does not affect repo behaviour.

## 2026-05-02 — 20Q anchor and pragmatic-stance condition added

Following discussion of construct validity — that the primary three-condition matrix tests *necessary* conditions for a B1/B2 characterisation of 20-Questions-style behaviour but not *sufficient* ones — added a 20Q-derived validation bridge to the design. Specifically:

- **`paper/outline.md` § 1 restructured** with three subsections: (1.1) elevator-pitch opening on 20 Questions including the loss-function-multiplicity / stance observation, (1.2) the underdetermined question, (1.3) the productive question. The Sally-Anne worked example is now a brief mention in 1.2 rather than the section opener; the loss-function-ambiguity in 20 Questions is named as an experimental handle rather than a complication.
- **`paper/outline.md` § 10** gained a "Construct validity: from 20 Questions to single-turn matched-pair stimuli" subsection naming the methodological compromise (mech-interp tooling does not natively handle multi-turn games), the asymmetry transformation (information asymmetry between players → between model and represented agent), and the role of the 20Q condition as a validation bridge.
- **`stimuli/twenty-questions/spec.md`** drafted. Single-turn input (stance framing + transcript + probe question + scored output). Three stance variants — collaborative / strictly correctness-oriented / adversarial-within-rules — all consistent with playing 20 Questions correctly, producing different expected answer profiles. Probes representation of the answerer's *utility function* and pragmatic update; related but distinct primitive from divergent-state tracking.
- **`stimuli/README.md`** updated to register the new condition. Explicit that 20Q is *not* part of the primary A/B/C-discriminating matrix; runs alongside as construct-validity check.
- **`prereg/notes/p3-cross-bot-prompt.md`** gained **IA-ε: pragmatic-stance distance** as a fourth named candidate independent axis for the recursive OOD probe. If selected by the cross-bot review, the 20Q condition is promoted from validation-only to primary test bed for B1/B2 discrimination.

Rationale per Jon: 20Q anchoring at the start of the paper does two things — provides a concrete elevator pitch that humans (with high cognitive scarcity) can latch onto from experience, and follows the recognisable lineage of game-anchored research while being honest that 20Q's loss function is itself contested across collaborative/strict/adversarial subgames. The subgame ambiguity is *not* a methodological problem; it is the experimental handle by which different cognitive architectures might be distinguished.

## 2026-05-02 — P4: discussion-section replies replaced with substantive arguments

`paper/outline.md` § 9 had three slogan-thin replies to anticipated reviewer objections. The review (`REVIEW.md`) flagged this as the second-highest-leverage substantive issue after P1. Replaced each slogan with a substantive paragraph or two. Specifically:

- **"B1 and B2 are still behaviourally indistinguishable in real deployments"** — reply distinguishes diagnostic from deployment-monitor status, and argues the distinction generates engineering-relevant downstream predictions (different failure-mode shapes to monitor for) without being itself an engineering tool.
- **"Linear-probe success is just feature presence, not computation"** — reply specifies each lens's individual failure mode (probe-detects-feature-presence-only; ID-can-be-norm-artefact; patching-cannot-distinguish-primitive-from-lookup; PH-sample-noise), argues these failure modes are mutually independent, and concludes the convergence requirement is informative because joint structured alignment of four independent failure modes is sharply less likely than any individual failure. Where lenses fail to converge, that itself is diagnostic.
- **"Topological methods are noisy on small samples"** — reply notes topology is corroborative not load-bearing, points to bootstrap resampling and pre-committed thresholds in the analysis plan, and flags an explicit open call: if pilot results show topology lens unstable at planned N, drop it from primary analysis rather than inflate claims.

Substantive material now in place for paper drafting; the replies are not the final voice but the argument structure is committed and locatable.

Per Jon's note on this work: he is positioned as facilitator for the design becoming a public artefact rather than as PI driving the agenda. The pattern across reasoning-LLM responses to this task family is itself a noted observation, not material for the paper.

## 2026-05-02 — P3 scaffolding: standardised cross-bot prompt for B1/B2 operationalisation

Drafted the canonical prompt at `prereg/notes/p3-cross-bot-prompt.md` for parallel independent review of the B1/B2 operationalisation across multiple bot families (recommended: Claude Opus 4.7, current-flagship Gemini, current-flagship general-purpose OpenAI model — *not* Codex; rationale: P3 is operationalisation-derivation work, not coding, so coding-specialised products are the wrong fit).

Drop-in stub files for each bot's response. README documents dispatch protocol and synthesis convention (quote verbatim, do not paraphrase).

Compute-free; awaiting Jon's review of the prompt before dispatch. Synthesis output will be promoted into `prereg/prereg.md` § "Recursive OOD probe" once available.

## 2026-05-02 — P2 resolved: recursive OOD probe is prereg-only

**Decision.** The recursive OOD probe is *not* an in-paper experiment and *not* a companion paper. The position paper specifies the probe in detail in the prereg as a planned analysis, argues for the research programme that includes it, and does not claim to have executed it. The prereg is the canonical executable contract.

**Rationale.** Matches what is actually true about the project (no compute for the full experiment) and the project's strategic-bet framing (design infrastructure for downstream agents with compute). Forces the prereg to carry the load that the position paper would otherwise pretend to carry; this is more honest and more useful.

**Sharpened by Jon's reply on this decision:** the design is intended to be *publicly bot-accessible* soon, on the bet that other agentic systems with more ToM/CS expertise and compute will be able to greenlight implementation. This raises the bar on machine-readability across the repo (prediction matrix as CSV ✓, prereg as executable spec, implementation skeleton actually runnable). The README's strategic-bet section was extended with this framing.

**Coupling.** Option 3 raises the urgency of P3 (locking the B1/B2 signature thresholds). Under options 1 and 2 the position paper carried some of the load; under option 3 the prereg carries all of it. Until P3 closes, the prereg is not submittable and the position paper is not shippable as designed. The prereg's "Recursive OOD probe" subsection is now explicitly the load-bearing section the position paper points to.

**Files updated.**
- `README.md`: strategic-bet section extended with the machine-readability constraints and downstream-agent handoff framing.
- `paper/outline.md`: § 5.4 reframed as a pointer to the prereg; § 11 closes with the handoff framing; "Open structural calls" entry struck through with resolution note.
- `prereg/prereg.md`: "Recursive OOD probe" subsection promoted to load-bearing status with a structured placeholder for the P3 operationalisation work.
