# Review of `JonMinton/llm-tom` for Claude Code revision

**Reviewer:** Claude (chat instance), via Jon Minton.
**Review date:** 2 May 2026.
**Scope:** files visible to the chat instance via web fetch — `README.md`, `CLAUDE.md`, `CHANGELOG.md`, `paper/outline.md`, `prereg/prereg.md`, `references.bib`. Files not directly fetched but documented in the changelog: `paper/paper.md` (placeholder), `analysis/plan.md` (scaffold), `analysis/prediction_matrix.csv`, `analysis/frequency_analysis/README.md`, `stimuli/README.md` and subdirectory placeholders, `implementation/README.md`, `pyproject.toml`, `.gitignore`. Treat any review claim about an unfetched file as inferred from the changelog rather than directly verified.

This document is intended as input to a Claude Code session for the next revision pass. Treat the items in **§ Priority revision tasks** as the actionable list. Other sections give context.

## Executive summary

The repository is in good shape. The handover landed cleanly, the structure is correct, the working principles transferred into `CLAUDE.md` with sharpening that improves on the original, and most files are appropriately scaffolded rather than over-drafted. The discipline of marking sections "attackable" rather than smoothing them is being maintained.

There is **one critical issue** which the project's own discipline should have caught and didn't: subtle hallucinations in author names in `references.bib`, despite that file being labelled "VERIFIED ENTRIES ONLY." This is the highest-priority fix, both because it undermines the file's stated guarantee and because the same failure mode is likely to recur in any new citation work unless explicitly corrected.

There are several **substantive issues** of medium priority — under-specified placeholder thresholds, a thin discussion section in the outline, an unaddressed open question about whether the recursive OOD probe is in-paper or a companion paper.

There are several **minor issues** of low priority — small consistency points and one cosmetic concern about the GitHub language indicator.

## What landed well

- `CLAUDE.md` is doing real work. The "do / do not" structure is sharper than the source handover, particularly the explicit instruction not to write paper text in Jon's voice. The "How to challenge well" section is good and worth keeping verbatim.
- The pre-registration scaffold gets the falsification logic right. "A pre-registration that cannot be falsified is not a pre-registration" is exactly the standard. The requirement that pre-registration happen *after* frequency analysis but *before* main stimulus runs preserves the empirical chain of evidence.
- The outline correctly identifies sections 5.3 (combinatorially novel stimulus), 5.4 (recursive OOD probe), and 9 (discussion) as the most attackable parts. This is the named-seam discipline operating correctly.
- `CHANGELOG.md` lists what was *deliberately not done* in the initial commit. That kind of explicit non-action log is unusually valuable; preserve the convention.
- The "Open design calls flagged in scaffolding" entry in the changelog is good practice and should be maintained on subsequent commits.

## Critical: `references.bib` author hallucinations

`references.bib` is labelled "VERIFIED ENTRIES ONLY" and the headline comment promises every entry was checked via web search on 2 May 2026. **Three of the six entries have hallucinated or incorrect author names** that don't match the actual papers. The papers themselves exist; the bibliographic metadata is wrong.

Compared against the search results from earlier in the project (which were verified against arXiv abstract pages, OpenReview, and Semantic Scholar):

### `fay2025shape`

- **Bib has:** `Fay, Andrew and García-Redondo, Inés and Wang, Qiang and Dubossarsky, Haim and Monod, Anthea`.
- **Should be:** `Fay, Aideen and García-Redondo, Inés and Wang, Qiquan and Dubossarsky, Haim and Monod, Anthea`.
- Errors: "Andrew" → "Aideen"; "Qiang" → "Qiquan".

### `chen2025rethinking`

- **Bib has:** `Chen, Meng-Hao and Lee, Yi-An and Liao, Feng-Ting and Shiu, Da-shan`.
- **Should be:** `Chen, Meng-Hsi and Lee, Yu-Ang and Liao, Feng-Ting and Shiu, Da-shan`.
- Errors: "Meng-Hao" → "Meng-Hsi"; "Yi-An" → "Yu-Ang".

### `liao2026revisiting`

- **Bib has:** `Liao, Feng-Ting and Chen, Meng-Hao and Yi, Guo-Tang and Shiu, Da-shan`.
- **Should be:** `Liao, Feng-Ting and Chen, Meng-Hsi and Yi, Guan-Ting and Shiu, Da-shan`.
- Errors: "Meng-Hao" → "Meng-Hsi"; "Guo-Tang" → "Guan-Ting".

### Already-flagged-as-unverified, leave as-is

- `joshi2025geometry`: first names listed as "[first names to verify]". Don't promote until verified — and note the field has at least one paper plausibly mis-attributed to "Joshi et al." in cross-references. May be Denti et al. Verify directly against the OpenReview entry.
- `geometry2025tokens`: authors listed as "[authors to verify]". Don't promote until verified.

### Already correct

- `janapati2024comparative`: matches arXiv listing (Saahith Janapati, Yangfeng Ji).

### Why this matters more than three name-spelling errors

Three issues compound:

1. The file's own opening comment promises every entry has been verified. The label is currently false. Either the entries are verified or they aren't; a partially-true verification claim is worse than no claim because it teaches downstream readers to trust an unreliable signal.
2. The hallucinations are *plausible*. "Meng-Hao" is a common Chinese transliteration; "Andrew Fay" is a plausible Anglicised name. They were not generated from random noise — they were generated by a process that approximates plausible names when uncertain. That same process will recur every time a new citation is added unless the discipline is tightened.
3. The project's stated discipline is verification-before-citation. The file silently violated that discipline at the very first commit. If this isn't caught and corrected, the project is operating one level less rigorously than it claims.

### Required action

- Fix the three author lists above against the canonical sources (arXiv abstract pages and OpenReview where applicable).
- Rewrite the opening comment of `references.bib` to specify *what verification actually means* — at minimum, every author name and the title and the year should be cross-checked against the canonical record (arXiv ID page, OpenReview entry, journal DOI). A "vibes-based verification" — paper exists, must be roughly right — is not the standard the project is operating to.
- Add a subsection to `CLAUDE.md` under "Strict factuality" specifying that author lists must be copied verbatim from the canonical source rather than rendered from memory. This is the loophole the current discipline left open.
- Log this correction explicitly in `CHANGELOG.md` as a worked example of the verification discipline catching a violation. The example value of having a documented correction is genuinely useful for the project's "infrastructure" framing.

## Substantive issues

### Outline § 5.4 (recursive OOD probe) and § 9 (discussion)

These are the two sections whose argumentative success the paper depends on, and both are currently thinner than they should be in the outline.

**§ 5.4 (recursive OOD probe).** The outline says "what's tested, what counts as the primitive vs interpolator signature. Equally attackable; do not handwave." Correct in principle, but the outline is itself handwaving. By the time of position-paper drafting, this section needs at least a sketch of: (a) what counts as a "primitive signature" operationally (e.g. sharp degradation at compositional boundaries with invariant performance within boundaries), (b) what counts as an "interpolator signature" (e.g. smooth degradation with distance from training neighbourhood), (c) how the experiment distinguishes them quantitatively. Without these, the B1/B2 distinction is unfalsifiable, and the position paper falls over at its load-bearing claim.

The pre-registration is the natural place to lock the operational thresholds. Currently the prereg lists "Pre-commit signature thresholds for 'primitive' vs 'interpolator' behaviour" as a placeholder. **This placeholder must be filled before the prereg can be submitted, and the filling-in is the highest-leverage design work remaining on the project.**

**§ 9 (discussion).** The outline pre-empts three reviewer objections, which is the right discipline, but the replies as drafted are slogan-thin:

> "Linear-probe success is just feature presence, not computation" — reply: the four-lens convergence requirement is precisely how we avoid this trap.

This is gestural, not argumentative. A careful reviewer will ask *why* convergence avoids the feature-presence trap rather than just reproducing it across multiple methods that share the trap. The reply needs to specify what features each lens *cannot* recover, such that convergence would be evidence of structure rather than shared methodological limit. This may be the hardest argument in the paper and it deserves to be developed before the discussion section is drafted, not during.

### Open structural call: in-paper or companion paper for the recursive OOD probe?

The outline lists this as an open call. The CHANGELOG flags it as one of three open design calls from the initial scaffolding. **It must be resolved before serious drafting begins**, because it determines whether sections 5.4 and the relevant parts of 6, 7, 9 are full sections or pointers to a follow-up paper. The two options are not equivalent in scope:

- **In-paper.** Position paper becomes 10–15k words rather than 8–12k. Increases scope and reviewer cost. Strengthens the standalone contribution.
- **Companion paper.** Position paper stays smaller. The companion paper would need its own complete drafting cycle. Risks the position paper looking like it's deferring its load-bearing argument.

A third option not currently flagged: **position paper makes the methodological argument, with the recursive OOD probe specified in the prereg as a planned analysis but not in-paper as an experimental section**. This treats the position paper as advocating for a research programme that includes the recursive probe, without claiming to have executed it. This is consistent with the "design infrastructure" framing the project has adopted.

Recommend resolving by the third option unless the recursive probe is run on Pythia-160M as part of pipeline validation, in which case in-paper as a worked example is justifiable.

### Combinatorially novel stimulus form

The outline names cellular-automata-as-belief-systems as the leading candidate but explicitly does not finalise it. The CHANGELOG flags this as an open design call. The prereg is correctly waiting on this before its stimulus matrix can be locked.

The substantive worry from the chat dialogue was that this is the most attackable element of the design. Specifically: cellular-automata-as-belief-systems risks being not-OOD-enough (Conway's Game of Life, Wolfram's classifications, and various belief-propagation algorithms are all in training distribution; the composition might already exist) or OOD-in-the-wrong-way (the model might fail behaviourally for reasons unrelated to abstract divergent-state representation, simply because the surface form is unfamiliar enough to derail standard processing).

Before locking, draft 5–10 candidate stimulus instances, run them through the frequency analysis protocol against Dolma/RedPajama, and check the empirical OOD claim. If the candidate fails the frequency check (i.e. cellular-automata-as-belief-systems shows similarity scores comparable to State-Rollback rather than near-zero), the leading candidate is wrong and a different combinatorially novel form is needed. Don't lock on intuition.

### Outline § 6 (frequency analysis): commit to the method, not just the protocol

The outline's section 6 is currently very brief — pointer to `analysis/frequency_analysis/`. That directory's `README.md` (per CHANGELOG) describes the protocol. Before drafting, decide: (a) is the embedding-based cosine-similarity method the only one used, or is it supplemented by structural matching as discussed in the dialogue?, (b) what corpus exactly — Dolma vs RedPajama vs a sub-sample of either, named version?, (c) what threshold operationally separates "in-distribution" from "OOD" in the cosine-similarity scores?

These are not just implementation details. They determine whether the position paper's argument about training distribution is empirically grounded or asserted. The frequency analysis is a prerequisite for the prereg's OOD claims being meaningful.

## Minor issues

### GitHub language indicator: TeX 100%

The repo's languages bar shows "TeX 100%". This is GitHub Linguist treating `references.bib` as TeX (BibTeX shares Linguist's TeX classification). It's cosmetic and benign. If a contributor or reviewer reads "TeX 100%" and assumes the paper is being drafted in LaTeX rather than Markdown, that creates a small expectation mismatch.

Two options: ignore (the file structure makes the actual situation obvious to anyone who looks); or add a `.gitattributes` entry to mark `references.bib` as `linguist-detectable=false` so the language bar reflects actual project activity once the first Markdown content lands. Either is fine. Mentioning here for completeness rather than as a required action.

### CHANGELOG single commit

The repo currently has one commit. This is a squash-merge artefact, presumably. As subsequent revisions happen, the commit history should naturally diversify. No action needed; just noting.

### Licence

`README.md` flags licence as "to be decided" and suggests CC BY 4.0 for paper / prereg / stimuli and MIT or Apache-2.0 for implementation code. This needs to be applied before any external sharing. Recommend deciding now (the suggestions are reasonable defaults) and committing the relevant LICENCE files and `LICENCE` field in `pyproject.toml`. Doing this on a separate commit makes the project's licensing status legible to scrapers and indexers.

## Priority revision tasks

In rough order of leverage. Each task is intended to be actionable in a Claude Code session.

### P1 — Fix `references.bib` author hallucinations and tighten verification discipline

1. Correct the three entries identified above (`fay2025shape`, `chen2025rethinking`, `liao2026revisiting`) by fetching the canonical arXiv abstract pages and copying the author list verbatim. Specifically:
   - https://arxiv.org/abs/2505.20435 (Fay et al.)
   - https://arxiv.org/abs/2510.01796 (Chen et al.)
   - https://arxiv.org/abs/2602.06471 (Liao et al.)
2. Verify the two unverified entries (`joshi2025geometry`, `geometry2025tokens`) against their canonical sources and either complete the author lists or remove the entries until verified. For `joshi2025geometry`, in particular, check whether it is Joshi et al. or Denti et al. — I have seen at least one cross-reference suggesting confusion.
3. Rewrite the opening comment of `references.bib` to specify the actual verification standard: every author name, title, and year cross-checked against the canonical record (arXiv abstract page, OpenReview entry, or journal DOI), with a note that author lists must be copied verbatim rather than rendered from memory.
4. Add a subsection to `CLAUDE.md` under "Strict factuality" specifying the verbatim-copy requirement for author lists.
5. Log all of the above in `CHANGELOG.md` as a single dated entry, including a brief description of *why* the correction was needed (i.e. naming the failure mode for future reference).

### P2 — Resolve the in-paper-vs-companion-paper structural question for the recursive OOD probe

Decide between in-paper, companion paper, or "in prereg as planned analysis only." Document the decision in `CHANGELOG.md` and update `paper/outline.md` § 5.4 and § 11, and `prereg/prereg.md`'s "Recursive OOD probe" subsection accordingly.

### P3 — Lock the operational definitions of "primitive signature" vs "interpolator signature"

This is the load-bearing distinction for B1 vs B2. The placeholder in `prereg/prereg.md` cannot ship as-is. Draft concrete operationalisations:

- What is the dependent measure — patching-effect magnitude, behavioural accuracy, both?
- What is the independent axis along which "interpolator" and "primitive" predictions diverge — distance from training distribution, compositional depth, substrate distance?
- What pre-committed thresholds distinguish them quantitatively — e.g. a slope cutoff in the patching effect vs distance, with confidence interval bounds?

This work probably needs another dialogue round with Gemini before it can be locked. Flag in `CHANGELOG.md` if it's deferred to a subsequent commit so the open status is tracked.

### P4 — Strengthen `paper/outline.md` § 9 (discussion) with substantive replies, not slogans

For each of the three pre-empted objections, replace the slogan reply with a one-paragraph argument sketch suitable for expansion into the final discussion section. The "linear-probe success is just feature presence" objection in particular needs a real reply: specify which structural failures each lens *cannot* recover, such that joint convergence is evidence of structure rather than shared methodological limit.

### P5 — Run the frequency analysis on candidate stimulus forms before locking the combinatorially novel condition

Generate 5–10 candidate cellular-automata-as-belief-system stimulus instances. Run them through the frequency analysis protocol against the chosen corpus sub-sample. If the OOD claim is empirically supported, lock the candidate; if not, draft alternative combinatorially novel forms (substrate-composition variants are the natural family) and re-test. This is Mac mini-tractable and a precondition for the prereg being submittable.

### P6 — Apply licences

Add `LICENCE` (or `LICENSE` — match GitHub convention) files for CC BY 4.0 (paper, prereg, stimuli) and MIT or Apache-2.0 (implementation code). Update `pyproject.toml` licence field. Single commit, low effort, removes a licensing ambiguity that blocks external use.

### P7 — Cosmetic: linguist override for language indicator

If desired, add `references.bib linguist-detectable=false` to a `.gitattributes` file. Optional.

## What not to do

Reproducing the discipline from `CLAUDE.md` because it bears repeating in this revision pass.

- **Do not draft paper text in Jon's voice without his review.** Paper drafts go in `paper/paper.md` clearly marked as drafts.
- **Do not promote citations to `references.bib` without verifying author lists verbatim against canonical sources.** This is the failure mode identified in P1; do not perpetuate it.
- **Do not lock the combinatorially novel stimulus form without running the frequency analysis first.** Intuition is not enough.
- **Do not silently fill in the prereg's placeholder thresholds for B1/B2.** They require argument; flag deferral if not done in this pass.
- **Do not collapse the four-hypothesis space to three.** A and C produce identical predictions on the three-condition matrix and are distinguished by within-domain generalisation. Keep all four; the apparent redundancy is the point.

## Open questions that need Jon

These are above Claude Code's pay grade and should be flagged for Jon rather than decided autonomously:

- Whether the recursive OOD probe is in-paper, companion-paper, or prereg-only (P2).
- Whether the licence choices match Jon's preferences for the project (P6).
- Whether to invite human collaborators (mentioned in `prereg.md` as "any human collaborators") and if so when.
- Target submission venue — TMLR vs workshop vs domain-specific.

---

## Summary for handover

The single most important task is P1: the verification discipline failed silently, and the file that was supposed to anchor the project's epistemic standards has subtle hallucinations in it. Fixing this also models the discipline working — naming the failure mode, correcting it, documenting it, and tightening the rule that allowed it. Treat it as a worked example of the convergence-as-warning principle: a "verified" file looking clean was a signal to look harder, not to move on.

P2 and P3 are the design-substance tasks. P4–P7 are smaller. P5 is empirically grounding the stimulus design and could happen in parallel with P2/P3.

The repo as a whole is a good handover artefact. The remaining work is sharpening, not restructuring.
