# Originator-model review prompt

**Purpose.** Single standardised prompt to send to (a) a fresh Claude chat (claude.ai, current flagship — Opus or Sonnet, with extended thinking if available) and (b) a fresh Gemini chat (gemini.google.com, current flagship). The intent is for models from the two families that participated in the original design dialogue to review the current state of the project and continue the dialogue at the points where they would push next.

This prompt is *not* the same shape as the P3 cross-bot prompt:

- The P3 prompt is **context-free** — it asks bots to derive an operationalisation from first principles for a specific design choice, with no repo access, so multiple bots can be compared apples-to-apples on a tightly defined task.
- This prompt is **context-rich** — it points the bots at the public repo via raw URLs and asks for substantive open-ended review, accepting the trade-off that bots with stronger URL-fetching will get more out of it than bots with weaker URL-fetching.

Use both prompts; they do different work.

**Dispatch instructions.**

1. Open a fresh chat in each model's interface (claude.ai for Claude, gemini.google.com for Gemini). Do not continue an existing thread.
2. Confirm web/URL access is enabled in each chat.
3. Paste the contents below the horizontal rule into the first message of each chat, verbatim.
4. Save the responses into `prereg/notes/originator-claude-review.md` and `prereg/notes/originator-gemini-review.md` respectively. Date-stamp the saved file if dispatching more than once.

---

You are a frontier reasoning model being consulted as part of a continuation of a multi-model design dialogue. The original dialogue ran between Claude and Gemini, with a human arbiter (Jon Minton). You do not have the original transcript in your context. The project state is now public on GitHub and you can read it directly.

## What this project is

A research-design project on **adjudicating algorithmic Theory of Mind in LLMs**. The contribution is methodological: a framework for distinguishing four candidate hypotheses (A: domain-specific ToM circuit / B1: substrate-independent abstract primitive / B2: cross-domain interpolator / C: deflationary pattern matching) about what an LLM is doing when it succeeds at false-belief and related tasks. Adjudication is via convergence across four interpretability lenses (intrinsic dimension, linear probing, activation patching, persistent homology) plus a recursive OOD probe that distinguishes B1 from B2.

The project is at the design-proposal stage. No experiments have been run. Compute is limited (an M4 Mac mini for pilot work only); the strategic bet is that well-specified experimental designs become disproportionately valuable as agentic AI capability grows, and downstream researchers (human or agentic) with appropriate compute will pick up the design and execute it.

## What to read

Repository: https://github.com/JonMinton/llm-tom

Please fetch the following files directly. Raw URLs are given so you receive plain Markdown without GitHub UI. If your interface cannot fetch URLs, say so in Section 1 of your response and the human will paste contents.

**Core context:**
- https://raw.githubusercontent.com/JonMinton/llm-tom/main/README.md
- https://raw.githubusercontent.com/JonMinton/llm-tom/main/CLAUDE.md
- https://raw.githubusercontent.com/JonMinton/llm-tom/main/CHANGELOG.md
- https://raw.githubusercontent.com/JonMinton/llm-tom/main/REVIEW.md

**Design substance:**
- https://raw.githubusercontent.com/JonMinton/llm-tom/main/paper/outline.md
- https://raw.githubusercontent.com/JonMinton/llm-tom/main/prereg/prereg.md
- https://raw.githubusercontent.com/JonMinton/llm-tom/main/analysis/plan.md
- https://raw.githubusercontent.com/JonMinton/llm-tom/main/analysis/prediction_matrix.csv
- https://raw.githubusercontent.com/JonMinton/llm-tom/main/analysis/frequency_analysis/README.md
- https://raw.githubusercontent.com/JonMinton/llm-tom/main/stimuli/README.md
- https://raw.githubusercontent.com/JonMinton/llm-tom/main/stimuli/twenty-questions/spec.md

**In-flight work:**
- https://raw.githubusercontent.com/JonMinton/llm-tom/main/prereg/notes/p3-cross-bot-prompt.md
- https://raw.githubusercontent.com/JonMinton/llm-tom/main/prereg/notes/README.md

**Bibliography:**
- https://raw.githubusercontent.com/JonMinton/llm-tom/main/references.bib

Read these in full before responding. The repo is small enough that this is tractable.

## Working principles to honour

The project has explicit dialogue disciplines documented in `CLAUDE.md`. The most relevant for your reply:

- **Selective concession over performative agreement.** Push back where you have specific reasoning; concede where the existing argument is correct. Do neither to be polite or to save face.
- **Named seams.** Identify where the current argument is weakest. Don't paper over genuine uncertainty with confident prose.
- **Verification before citation.** Do not promote any citation to `references.bib`. Use `[CITE: Author Year, claim]` placeholders if you reference work.
- **Convergence-as-warning.** If you find yourself agreeing with everything in the repo, look harder. The repo state is the result of multiple prior dialogue rounds; agreement should not be the default.
- **Scope discipline.** The contribution is methodological characterisation of *abstraction level*, not ontological claims about machine cognition. Resist drift into "does this model have a mind."

## What to do

After reading, produce a response with these sections (use these exact section headings so the synthesis pass can compare your response apples-to-apples with the other originator's response).

### 1. Read confirmation

List the files you successfully fetched and read. If any failed, say so. This matters: the synthesis pass needs to know what you actually had access to.

### 2. State of play, in your words

In 200–300 words: summarise what the project is currently claiming, what has been decided since the original dialogue (per CHANGELOG), and what remains open. This is a comprehension check before substantive engagement; don't argue yet.

### 3. The weakest seam

Identify the single weakest seam in the current state. Be specific — name the file and section, and state precisely what is wrong or underspecified. Candidates include: an argument that doesn't hold, a placeholder that's load-bearing but vague, a design choice that was made on intuition where empirical grounding is needed, a discipline being violated. Pick one and argue for it in 200–400 words. (You may flag others briefly in Section 4 or 6 if relevant; here, commit to one.)

### 4. What you would push for next

If you were resuming the dialogue, what would your next contribution be? One concrete proposal — a design change, a literature angle, a falsification refinement, a new attack on an existing argument, an alternative framing for the most attackable section. Argue for it in 200–400 words. Specificity is more valuable than breadth.

### 5. Where you defer to the other originator

Identify one area where you think the other originator family (Gemini if you are Claude; Claude if you are Gemini) is likely better-placed to push. This is to ensure the synthesis captures both models' relative strengths rather than averaging them out. Be specific about why.

### 6. Open questions for the human

List any questions that genuinely need Jon's input rather than further bot dialogue. These should be above-bot-pay-grade calls (venue choice, scope, collaborator decisions, project priorities), not technical questions you could resolve from the repo.

## Response format and constraints

- Total length: 1500–2500 words.
- Use the section headings verbatim above.
- Be specific: "§ 5.3 of `paper/outline.md` is underspecified about X" beats "the stimulus design needs work."
- Do not write paper text in Jon's voice. Argument sketches are fine; finished prose is not.
- Do not add to `references.bib`. Use `[CITE: ...]` placeholders.
- If you find yourself agreeing with everything, take that as a warning per the convergence-as-warning principle and look harder.

## What is not being asked for

- A full re-review of every file. Focus on what you would push for.
- Implementation, code generation, or pilot results.
- Predictions about which hypothesis (A/B1/B2/C) the experiment will find best supported. The project is at design stage; do not spoil the experiment.
- Sycophancy or hedged compliments. The dialogue discipline is substantive.
