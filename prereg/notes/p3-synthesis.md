# P3 — synthesis: the reconciled revised recursive-OOD probe

**Status: design-converged (2026-06-29).** This is Jon's synthesis bridging `prereg/notes/` to the prereg's "Recursive OOD probe" subsection, per the directory README. It consolidates the full P3 arc and is the canonical revised design.

**Provenance of this design:**
- Operationalisation proposed (Gemini) → 5 pushbacks + named seam (Claude) → adopted, recast as 2×3 factorial (Gemini) → ratified by both. Files: `p3-instance-gemini.md`, `p3-instance-claude.md`.
- A fabricated empirical citation in Claude's Pushback 2 (an "IOI/ACDC report NCME variance 0.05–0.15" claim) was caught by a verification subagent against canonical sources; prescription survived, citation dropped. IOI + ACDC now verified in `references.bib`.
- Fresh-eyes lock gate (3 independent adversarial reviewers, no context): verdict **non-identified as drawn**; reviewers 2 and 3 independently found the same core flaw. File: `p3-stress-test.md`.
- Revision round (both instances): `p3-revision-gemini.md`, `p3-revision-claude.md`. Final gating seam reconciled — Claude conceded.

---

## The core repair

The original single composite "substrate-distance" axis conflated **surface/lexical novelty** with **structural-compositional novelty** (and with distance-from-the-model's-interpolable-support). Because LLM representational geometry tracks surface frequency, not human semantic taxonomy, neither a flat nor a decaying NCME was interpretable. The fix decomposes the axis and converts both ambiguities into *positive, falsifiable* tests.

## The reconciled probe

### 1. Factor structure — Surface-Novelty (S) × Structural-Novelty (T)

A **3×3 grid**, with the **same logical content rendered across all three surface forms** (T held constant across S — this is what makes it identifying):
- **Surface axis S:** S0 narrative English / S1 code-like (assignment statements over named agents) / S2 logical notation (belief operators).
- **Structural axis T:** T0 standard Sally-Anne / T1 deeply-nested epistemic chains (4+ levels) / T2 non-standard update rules (retrocausal / non-Bayesian).
- **Primary discriminator:** at *fixed S*, does NCME degrade with T? **B1 → invariance along T at any fixed S; B2 → decay along T at fixed S.** The **main effect of T at fixed S** bears the load (not the interaction). Surface-driven encoding effects appear along S at fixed T and are handled by the gate + controls below.
- **Continuous complement (Gemini):** also measure each stimulus's **support sparsity** `σ(x) = (1/k) Σ_j D_M(x, NN_j(x))` (mean Mahalanobis distance to k≈50 nearest neighbours in the M4 reference corpus). Validate the S/T ordering *representationally* rather than by fiat.

### 2. Upstream encoding-gate (replaces the rejected downstream denominator gate)

Train a ridge-regression probe at an early layer `l ∈ [2,4]` to decode the deterministic surface ground-truth of the stimulus. Partition each trial by early-decode accuracy α: **`T_unparsed` (α < 90%)** → surface never encoded → uninterpretable for any hypothesis → **excluded**; **`T_parsed` (α ≥ 95%)** → surface provably encoded → **kept**. Compute NCME conditioned on `T_parsed`. This conditions on *"was the surface encoded upstream,"* a different thing from *"does the bottleneck separate cleanly,"* so it **does not discard B2's distant-failure evidence**. The 90%/95% thresholds are `PROVISIONAL` pending pilot calibration of the probe's accuracy distribution on known-good stimuli.

### 3. Dependent measure & estimator

NCME = (L_patched − L_corrupted)/(L_clean − L_corrupted), computed on `T_parsed`. **No downstream denominator gate** (it is survivorship bias: it discards exactly the distant-OOD trials where B2 predicts the forward pass collapses, manufacturing a false B1). Instead use **Fieller (denominator-conditioned) intervals** for the ratio CI — near-zero/near-zero trials are the data, not noise; Fieller widens the CI honestly rather than throwing them away. A near-zero numerator over a near-zero denominator *is* B2's predicted collapse.

### 4. Two positive identifiability tests

- **(a) Equivalence test on the T-slope (answers reviewer 1's "confirmation-by-weakness").** Pre-register a **ROPE in SD_pilot units** (proposal ±1.0·SD_pilot). **B1 support requires the 90% CI of the T-axis slope at each fixed S to fall *entirely within* the ROPE** (TOST). A CI spanning both ROPE-interior and B2-territory → **inconclusive**, not B1. Power analysis is for the equivalence test, with reviewer 1's dead-zone alternative (−1.5·SD_pilot) as the effect to rule out.
- **(b) Lipschitz-envelope test (Gemini).** Any continuous interpolator obeys a bounded decay envelope `NCME_max(σ) ≤ 1 − λ·σ`. **B2:** points sit on/below the envelope. **B1:** points *violate* it — NCME ≥ 0.85 where σ ≫ 1/λ — which a continuous interpolator mathematically cannot do in a sparse-support neighbourhood. Flatness becomes a positive signature.

These are complementary: (a) is the categorical-grid test; (b) is the continuous-sparsity test. Convergence of both strengthens the verdict; divergence is itself diagnostic.

### 5. Factor 2 (validity) de-confounding

Match valid (v=1) and invalid (v=0) minimal pairs on an **unrelated LM baseline cross-entropy / reference-corpus surprisal**, enforcing |ΔP| ≤ ~0.1–0.15 nats/token (not length/syntactic depth). Substrate-level baseline differences remain but are then explicitly measured, not confounded.

### 6. All numeric thresholds are PROVISIONAL

Including: the NCME/slope thresholds, the Section-0 circuit-ID thresholds (70%/15%), the encoding-gate thresholds (90%/95%), λ, the ROPE width. Each is pilot-calibrated against measured noise on the M4 — never committed a priori (the lesson the dialogue had to relearn twice).

---

## Honest residual identification limit (load-bearing for the paper's framing)

The revised probe achieves **partial identification** — conditional on the encoding controls being approximately correct. The paper must:
1. State this caveat explicitly; the contribution is the **rigorous methodology** (decomposed axes, encoding-gating, equivalence testing, Lipschitz bounding, Fieller estimation) + an **honest identification analysis**, not a claim to have fully cracked B1 vs B2.
2. **Turn the fresh-eyes catch into a citable contribution**, not hide it: *"earlier formulations treated surface and structural novelty as a single composite axis, which is non-identifying because LLM representational geometry tracks surface frequency rather than human semantic taxonomy."*
3. Include a clearly-marked section on the residual limit and what would close it.

Both originating instances independently converged on this meta-conclusion.

---

## Hand-off to the M4 pilot (the next phase)

The design is now executable; remaining work is empirical calibration, Mac-mini-tractable:
1. **Frequency analysis** (already scoped in `analysis/frequency_analysis/`) — now doubles as the source of σ(x) support-sparsity and the S/T ordering validation.
2. **Encoding-gate probe** — ridge probe at layers 2–4 on a small model; calibrate the 90%/95% thresholds on known-good stimuli.
3. **SD_pilot calibration** — bootstrap NCME variance on a known-good (IOI-equivalent) circuit; sets the ROPE and all SD_pilot-relative thresholds.
4. **Implementation skeleton** (`implementation/`) — wire NCME + Fieller + the equivalence test end-to-end on Pythia-160M-class to validate the pipeline runs.
