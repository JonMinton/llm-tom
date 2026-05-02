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
