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
