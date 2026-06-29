# P3 — fresh-eyes adversarial stress-test (lock gate)

**Date:** 2026-06-29
**Purpose:** the convergence-as-warning lock gate before declaring the P3 (recursive-OOD probe) architecture locked. Three independent reviewers, **no dialogue context** (fresh eyes per the instance-as-author principle's case (ii)), each given the converged 2×3-factorial design and asked for the single strongest objection from one lens. Run via Claude Code subagents; both originating instances had ratified the design before this gate.

**Verdict: P3 is NOT lockable as drawn.** All three reviewers returned FATAL-as-specified objections, each downgradeable to SERIOUS with concrete fixes. Reviewers 2 and 3 converge **independently** on the same core flaw; Reviewer 1 adds a distinct inferential problem. The recursive-OOD probe — flagged in `CLAUDE.md` as the load-bearing, most-attackable step — is **non-identified as drawn**. Both originating instances (and the facilitator) missed this; a textbook convergence-as-warning case.

---

## The core flaw — where reviewers 2 and 3 independently converge

The B1/B2 separation rests on the shape of NCME across Factor 1 (substrate-distance): **flat ⇒ B1 (primitive), decay ⇒ B2 (interpolator)**. But Factor 1 (Mahalanobis D_M in an embedding+dependency-parse space) is a **surface/semantic-distance axis**, not a **distance-from-the-model's-interpolable-support axis**. These are not the same — LLM representation geometry is dominated by surface form, token frequency, and syntactic template, not human semantic taxonomy. Once that identity is broken, **both** read-outs are confounded:

- **Flat NCME is not evidence of a primitive (Reviewer 2).** A good interpolator over a well-supported shared relational scaffold ("agent A holds representation R of object O; rule U updates R") reads out flat NCME across all three substrates — reproducing the full B1 fingerprint with no divergent-state primitive. The "combinatorially-novel" CA stimulus is novel to a *human* but is built from cells/grids/update-rules, content massively represented in code/math training data — plausibly an *interior* manifold point, possibly less OOD than Sally-Anne. The validity collapse can itself be a frequency/support artefact, substrate-invariantly, with a null interaction.
- **Decaying NCME is not evidence of an interpolator (Reviewer 3).** Activation-patching effects shrink *mechanically* when a stimulus is encoded less cleanly. Surface-induced encoding degradation along D_M produces NCME decay regardless of mechanism. So decay is predicted equally by B2 **and** by "B1 + encoding failure" (the model *has* the primitive but can't map the lexically-alien CA surface onto it).

Net: neither flatness nor decay is interpretable. The independent variable is operationalised as the very nuisance that supplies the rival explanation for its decisive result. The design's *confirmatory success state* (flat valid-NCME + substrate-invariant collapse + null interaction) and its *most likely artefact* are the same observation.

---

## Reviewer 1 — statistical / measurement validity: "confirmation-by-weakness"

**Objection.** B1 and B2 are inferentially asymmetric. B2's signature is *positive* thresholds to clear; B1's is the *negation* (invariance + **non-significant** interaction). With **no equivalence bound (TOST/ROPE)** and no positive floor for "invariant," B1 is the residual category that absorbs every outcome failing B2's bar — so B1 is confirmed by *failing to reject* nulls. Two forces push results into that dead zone exactly where it matters: (i) a 6-cell 2×3 of noisy patching data is **underpowered for the interaction term**, so failing to reject the null interaction is the *expected* result whether B1 or B2 is true; (ii) **NCME's denominator (L_clean − L_corrupted) collapses toward zero at the combinatorially-novel tier** — where the model is weakest and B2 predicts decay — making the ratio heavy-tailed and inflating the bootstrap CI precisely at the discriminating tier, killing power to detect B2's decay. All three forces bias toward spurious B1.

**Severity:** FATAL as specified (confirmation-by-weakness at the core of the decision rule).

**Fix (→ SERIOUS):** (1) replace "non-significant" with a pre-registered **equivalence test / ROPE in SD_pilot units** (B1 must *positively* clear an invariance bound) + an "inconclusive" bucket at the B1/B2 stage, or a Bayes-factor threshold; (2) pre-register an **interaction-contrast power analysis** at a "dead-zone" alternative (e.g. −1.5·SD_pilot) and report items-per-cell to keep false-B1 < 5%; (3) **gate cells on minimum clean separability** (|L_clean − L_corrupted| ≥ k·SD_pilot), report **Fieller** (denominator-conditioned) intervals not naïve bootstrap, and control forking paths (one pre-registered primary contrast; precision/τ sweeps as robustness only, with multiplicity correction).

**Existing safeguards don't address it:** SD_pilot supplies the *scale* for a ROPE but the design never builds the equivalence test; the both-sink falsifier sinks B1 and B2 together (doesn't *distinguish* them); the "inconclusive" bucket exists only at the circuit-ID pre-stage, not the B1/B2 decision stage.

---

## Reviewer 2 — construct validity: the discriminating contrast smuggles an unargued identity

**Objection.** The B1/B2 split assumes `semantic-substrate-distance ≈ distance-from-interpolable-support`. That identity is unargued and, given what's known about LLM representation geometry (surface/frequency/syntax-dominated), likely false. Break it and a good interpolator yields the *exact* B1 signature (flat NCME across substrates that share dense, locally-flat support). "Flat" is consistent with "primitive," with "good interpolator over interior points," and with "axis too short / measure underpowered to decay" — three accounts, one read-out. The failure is **confound-aligned**: the design's "we found the primitive" outcome is precisely what an interpolator on a misaligned/interior axis most likely yields.

**Severity:** FATAL to the confirmatory inference (the 2×3 apparatus itself is salvageable).

**Fix (→ SERIOUS, additions not tuning):** (1) **validate the IV against the construct** — independently measure each class's distance-from-support in representation space (per-token likelihood/perplexity, k-NN to a corpus-embedding reference, the planned frequency analysis) and show the classes are monotonically ordered *and well-separated representationally*, not just intuitively; if CA turns out interior, the "novel" arm is void; (2) add a **positive interpolator control** (a task with a known interpolative mechanism on a deliberately support-graded axis) to show NCME *does* decay where it should — otherwise "flat" has no calibrated zero; (3) **equivalence test** (as Reviewer 1); (4) **de-confound Factor 2** — match valid/invalid on model likelihood/support so the validity collapse isn't "invalid = rarer string."

**Existing safeguards don't address it:** the C-exit and the both-sink falsifier both fire in the *wrong cell* (no-circuit, ≈0-mediation); this objection lives in the **shared-circuit, high-mediation, flat-NCME** cell the design reads as B1. *Subordinate note:* identify-circuit-then-probe mildly assumes its conclusion (a single shared bottleneck), but the C-exit partially handles that — SERIOUS-at-most and secondary.

---

## Reviewer 3 — stimulus / OOD validity: Factor 1 is the nuisance that explains its own result

**Objection.** D_M measures lexical/topical/syntactic distance — a **surface-novelty** metric. It does not decompose into "structural-compositional novelty the model couldn't have abstracted" vs "surface novelty that degrades baseline processing." CA scores maximally far largely because its *vocabulary/frame* is alien, independent of whether its divergent-state structure is novel. Since patching effects shrink mechanically with poorer encoding, **surface-induced encoding degradation alone produces NCME decay along D_M** — so observed decay is predicted equally by B2 and by "B1 + encoding failure." No manipulation separates them. **Aggravator:** a "broken/non-causal CA rule" (Factor 2 invalid) is an *additional* surface perturbation; matching on length/syntactic-complexity does not match on **processability** (a non-causal rule is one the model's learned dynamics resist, so it is differentially hard to encode by construction), and the psychological "broken-update Sally-Anne" sits inside heavily-trained narrative scaffolding so its brokenness costs far less encoding fidelity — Factor 2 is **non-equivalent across substrates**.

**Severity:** FATAL as specified (core inference non-identified).

**Fix (→ SERIOUS, new conditions):** (1) **orthogonal surface-difficulty control at each distance** — a stimulus matched in D_M / lexical alienness but structurally *trivial* (no divergent-state relation); its NCME estimates pure encoding degradation, to be subtracted; (2) **primitive-free encoding positive-control for the CA cell** (e.g. "apply this trivial deterministic rule one step; report cell 3's state") — if the model fails *this*, the CA cell is uninterpretable for B1/B2; (3) **cross the design** — a structurally-novel-but-lexically-*familiar* divergent-state item; if decay tracks D_M but this item is handled well, decay was surface; (4) **re-specify Factor 1 as 2-D** (surface-novelty × structural-novelty) and test invariance against the *structural* axis at fixed surface novelty — the monotone psych < technical < novel ordering must be *demonstrated*, and likely won't hold (the substrates differ from the centroid in *direction*, not just magnitude, so a scalar D_M need not rank them monotonically). *Secondary:* Mahalanobis covariance is ill-conditioned/singular on Mac-mini-scale sampling without heavy shrinkage / a low-rank subspace.

**Existing safeguards don't address it:** the frequency-analysis prerequisite only *confirms* CA is far in D_M (i.e. confirms surface-novelty → **strengthens** the confound — wrong direction); the quantisation/precision check is orthogonal.

---

## Convergent fix package (what all three point to)

These overlap heavily — the fixes form one coherent revision, not three separate patches:

1. **Decompose & validate Factor 1 into surface-novelty × structural-novelty** (Rev 2, 3). The discriminating test becomes invariance against the *structural* axis at fixed surface novelty. Validate the ordering representationally (per-token likelihood / k-NN / the frequency analysis), don't impose it.
2. **Add positive/encoding controls** (Rev 2, 3): a structurally-trivial stimulus matched in D_M (estimates pure encoding degradation, to subtract) and a known-interpolator control (calibrates that NCME *does* decay when it should — gives "flat" a meaningful zero).
3. **Equivalence testing** (Rev 1, 2): replace "non-significant interaction ⇒ B1" with a pre-registered ROPE/TOST + an "inconclusive" bucket at the B1/B2 stage; add an interaction-contrast power analysis.
4. **De-confound Factor 2 on model likelihood/support** (Rev 2, 3), and address the cross-substrate non-equivalence of "brokenness."
5. **Estimator robustness** (Rev 1): gate cells on minimum clean separability; Fieller intervals; forking-path / multiplicity control.

**Bottom line:** salvageable but it is a real revision of the recursive-OOD probe, not a tweak — and the revision lands squarely on the section the project always flagged as load-bearing and most-attackable.
