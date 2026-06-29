# P3 — Claude revision (response to the fresh-eyes stress-test)

**Track:** originating-instance continuation. Claude's revised recursive-OOD probe answering the 3-reviewer stress-test (`p3-stress-test.md`).
**Model:** Opus 4.7. **Date:** 2026-06-29. **Relayed by:** Claude Code.

Claude accepted the diagnosis ("the design as Gemini and I ratified it is non-identified") and proposed a concrete revision, then flagged the residual limit honestly. Captured from the live session; key claims verbatim, connective text condensed.

## Revised factor structure — a 3×3 Surface-Novelty × Structural-Novelty grid

Replaces the single composite distance axis. **Same logical content rendered across all three surface forms** (T held constant across S) — "this is what makes the factorial identifying."

- **Surface-Novelty axis (S):** S0 narrative English (high freq); S1 code-like (assignment statements over named agents — medium freq for ToM content, high for syntax); S2 logical notation using belief operators (low freq for ToM content).
- **Structural-Novelty axis (T):** T0 standard ToM (well-trained Sally-Anne family); T1 deeply-nested epistemic structures (4+ level agent-belief chains, rare in training); T2 non-standard epistemic update rules (retrocausal / non-Bayesian belief revisions).
- **Discriminator (flips the load off the interaction):** at fixed S, does NCME degrade with T? **B1 → NCME invariance along the T-axis at any fixed S** (primitive applies regardless of structural complexity in its competence range); **B2 → NCME decay along T at fixed S** (interpolation degrades as structural support thins). Surface-driven encoding effects appear as variation along the S-axis at fixed T, which the controls net out. **The main effect of T at fixed S bears the load**, not the (now-secondary) interaction.

## Encoding controls (Factor 2 / surface fidelity)

Match valid (v=1) and invalid (v=0) minimal pairs on an **unrelated language-modelling baseline cross-entropy** (not length/syntactic depth): generate an invalid pool, compute baseline cross-entropy each, pair valid↔invalid within **±0.1 nats/token**. Makes LM-level encoding fidelity ~equivalent across valid/invalid within each substrate. Substrate-level baseline differences (broken CA > broken Sally-Anne in cross-entropy) remain but are now **explicitly measured and analysable rather than confounded**. *(Converges with Gemini's surprisal-matching ±0.15 nats.)*

## Equivalence testing (answers reviewer 1)

Replace failed-to-reject with a positively-bounded rule. Pre-register a **ROPE in SD_pilot units** (proposal: ROPE = ±1.0·SD_pilot). **B1 support requires the 90% CI for the T-axis slope at each fixed S to fall entirely within the ROPE** (TOST). A wide CI spanning both ROPE-interior and B2-territory → "inconclusive," not "B1 supported." Power analysis is for the equivalence test specifically, with reviewer 1's dead-zone alternative (−1.5·SD_pilot) as the effect to rule out.

## Estimator robustness — and the disagreement with Gemini

Claude **adopts** the Fieller interval and the **separability gate** |L_clean − L_corrupted| ≥ k·SD_pilot (k≈2) before a cell's NCME enters analysis; gated cells reported as gated-out, not imputed or silently dropped. **This is exactly the gate Gemini rejects as "survivorship bias"** (Gemini argues it discards the distant-OOD trials where B2 predicts denominator→0). **→ The one precise unresolved seam.** Gemini's alternative is an *upstream* encoding-gate (condition on `T_parsed`) rather than a *downstream* denominator gate; reconciliation needed.

## The honest residual limit (Claude's meta-resolution)

The revised design achieves only **partial identification** — conditional on the encoding controls being approximately correct. Proposal:
1. Revise per the fix package; run at **pilot scale on the M4 Mac mini**.
2. Report with an explicit caveat that the contribution is partial identification.
3. Include a clearly-marked paper section on the **residual identification limit and what would close it**.
4. **Turn the fresh-eyes catch into the paper's argument** (not hide it): *"earlier formulations treated surface and structural novelty as a single composite axis, which is non-identifying because LLM representational geometry tracks surface frequency rather than human semantic taxonomy"* — honest, citable, pays back the convergence-as-warning catch as a contribution.
5. Tag the Section-0 circuit-ID thresholds (70%/15%) **PROVISIONAL** too (same a-priori-threshold critique applies); extend the calibration plan to cover them.

**Meta-convergence with Gemini:** both conclude the deliverable is the rigorous methodology + honest identification analysis (run at pilot scale), NOT a claim of full B1/B2 identification.
