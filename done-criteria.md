# Done-criteria — when is it "good enough"?

**Status: DRAFT for challenge.** Proposed by Claude Code at Jon's request, 2026-06-29. These are stopping conditions, not a contract. "Good enough" is partly judgement; the point of writing it down is to make that judgement *accountable*, not to replace it. Challenge freely — and the originating instances should be invited to attack this list too.

Two artifacts have two distinct bars: the **dialogue** (the multi-session design discussion) and the **manuscript bundle** (`paper/paper.md` + `prereg/prereg.md` + `implementation/`).

## The dialogue is "good enough" when

1. **Every load-bearing choice has been adjudicated.** Dependent measure, independent axis, B1/B2 quantitative signatures, decision rule, falsification rule, and the recursive-OOD probe have each been put to both originating instances and either (a) converged *with stated reasons*, or (b) had the disagreement captured as a **named seam** with both positions quoted verbatim (per the `prereg/notes/` convention) — not smoothed over.
2. **Convergence has been stress-tested.** Wherever the two instances agreed quickly, at least one deliberate adversarial / fresh-eyes pass has been run against that agreement (convergence-as-warning) and found no fatal hole — or the hole is logged.
3. **No load-bearing placeholder remains.** Every `TBD` / `[CITE:]` / threshold-placeholder on a load-bearing item is either filled or explicitly tagged pilot-anchored with a reason.
4. **Diminishing returns reached.** Two consecutive relay rounds add no new named seam and resolve no existing one — only restatement or polish. (Loop-until-dry, not loop-forever.)
5. **Residual open questions are above-bot-pay-grade.** What remains needs *Jon* (venue, scope, collaborators, compute), not more bot dialogue.

## The manuscript bundle is "good enough" to post (arXiv preprint / workshop) when

1. **Structurally complete.** Every section in `paper/outline.md` is drafted; no scaffold/placeholder headers remain.
2. **Citations verified.** No `[CITE:]` left in the body; every `references.bib` entry carries a `verified =` field against a canonical source (CLAUDE.md verification discipline).
3. **The attackable sections survive an adversarial read.** The B1/B2 distinction, the recursive-OOD-probe defence, and the discussion-section objection replies each pass a fresh-eyes adversarial read with no fatal hole — or the limitation is stated honestly in the text.
4. **Paper and prereg are consistent.** The prereg is the executable spec; the paper argues for it; there are no contradictions between them.
5. **The downstream-executable bar (the project's own thesis).** A competent downstream researcher — human or agentic — could convert `prereg/prereg.md` into running code *without further design choices*. This is the README's strategic bet and the single sharpest criterion.
6. **The pipeline is real, not gestural.** The `implementation/` template runs end-to-end on a small model (Pythia-160M class); figures regenerate from scripts.
7. **Comprehension check.** A fresh reader can correctly restate the contribution and the falsification logic from the manuscript alone.
8. **Jon owns the voice.** Jon has read the final prose and it reads as his (Claude drafts; Jon writes the final voice).

## Fallback stop (hard iteration cap)

Like any optimisation, the loop needs a finite-N fallback in case the convergence conditions above never cleanly trigger. **Cap: at most ~10 relay rounds** per thread (per load-bearing design question, or per manuscript section). On hitting the cap without convergence, **stop** and surface to Jon with the residual disagreement written up as a named seam and both instances' final positions quoted — do not silently keep iterating. The cap is a backstop, not a target; most threads should converge (or dry up per dialogue-criterion 4) well before it.

## The art part (made explicit)

The marginal round eventually trades substance for polish. **Stop** when (5) and (7) hold and the remaining edits are stylistic. Over-iterating a design preprint past "honestly represents the design and its limitations" is wasted motion — and actively risks the convergence trap (agreement mistaken for correctness). The preprint bar is **defensible + honest + downstream-executable**, not **unimprovable**. A submitted-but-honest design that names its own seams beats a polished one that hides them.
