# `prereg/notes/`

Working notes feeding the pre-registration. Files here are scratch — drafts, cross-bot reviews, synthesis worksheets — and may not be self-consistent until promoted into `prereg/prereg.md`.

## Files

### P3 — context-free operationalisation review (B1/B2 thresholds)

Tightly defined task; no repo access; bots reason from first principles for apples-to-apples comparison.

- **`p3-cross-bot-prompt.md`** — canonical standardised prompt for parallel independent review of the B1/B2 operationalisation. Dispatch instructions at the top.
- **`p3-claude-draft.md`**, **`p3-gemini-draft.md`**, **`p3-gpt5-draft.md`** — drop-in stubs for each bot's response.
- **`p3-synthesis.md`** *(not yet written)* — Jon's synthesis of the three drafts; bridges this directory and the prereg's "Recursive OOD probe" subsection.

### Originator-model review — context-rich open-ended review

Models from the two families that participated in the original design dialogue review the current repo state and continue the dialogue at the points where they would push next. Pointed at raw GitHub URLs.

- **`originator-review-prompt.md`** — standardised prompt. Dispatch instructions at the top.
- **`originator-claude-review.md`**, **`originator-gemini-review.md`** — drop-in stubs for each originator's response.
- **`originator-synthesis.md`** *(not yet written)* — synthesis pass; outputs feed into design decisions and / or surface new open seams.

## Convention

Bot drafts are quoted verbatim, not paraphrased. The synthesis file extracts load-bearing sentences with attribution. Per `../../CLAUDE.md` "How to challenge well": this directory is where disagreement between bots gets surfaced and worked, before any conclusion is moved into the prereg.
