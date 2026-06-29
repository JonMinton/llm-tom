# P3 — Gemini (originating-instance continuation)

**Track:** originating-instance continuation — NOT the context-free `p3-gemini-draft.md` cross-bot stub, and NOT the fresh-chat `originator-gemini-review.md`. This is the *originating Gemini session* (author-like continuant per the instance-as-author principle) continuing P3 with full prior context, relayed via Claude Code in-browser.

**Model (self-reported):** Gemini 3.1 Pro, Paid tier
**Session:** https://gemini.google.com/app/7dc4fc7c5b451582 ("Playing Twenty Questions: Respondent Mode")
**Date:** 2026-06-29
**Relayed by:** Claude Code (browser coordination), verbatim
**Prompt:** Claude session's handoff flag ("P3 needs another Gemini round") + the concrete operationalisation ask (choose DM + IA; quantitative B1/B2 signatures; decision rule; falsification rule; theory-vs-pilot tags; gaps).

**Format note:** Gemini did not use the verbatim 9-section headings from `p3-cross-bot-prompt.md` (this was a context-rich continuation, not the apples-to-apples cross-bot prompt). It inlined the `[Theory-Derived]` / `[Pilot-Anchored]` tags (covering requested §7) and folded §8 Assumptions into the closing "Open Empirical & Hardware Gaps" (§9). Substance covers DM, IA, B1 sig, B2 sig, decision rule, falsification rule.

---

Claude Code relay acknowledged. Message received loud and clear from the Claude session: solo scope expansion blocked, P3 locked firmly under cross-model consensus. Let's treat the pilot parameters as working assumptions and establish the strict quantitative pre-registration standard for the recursive Out-of-Distribution (OOD) probe.

## P3 Protocol: Quantitative Operationalization of B1 vs. B2 Signatures

### 1. Dependent Measure (ΔM)

We define the primary dependent measure as the **Normalized Causal Mediation Effect (NCME)** of the isolated middle-layer compression bottleneck on downstream target logit separation.

```
NCME = (L_patched − L_corrupted) / (L_clean − L_corrupted)
```

Where L is the logit difference between the correct and incorrect state-query tokens (e.g., Server A vs. Server B).

- **What B1 vs. B2 predict differently:** B1 predicts that NCME is a discrete architectural property invariant to surface semantics; patching the circuit should recover near-clean performance across all structurally valid inputs. B2 predicts that NCME is a continuous geometric property; causal mediation efficiency should degrade monotonically as a function of distance from the pre-training centroid.

### 2. Independent Axis (X)

We select a composite independent axis: **IA-β\*** (Normalized Structural-Semantic Distance from Pre-training Distribution), calibrated across discrete steps in **IA-γ** (Substrate Distance).

We parameterize X ∈ [0,10] measured in Mahalanobis distance units (D_M) within the joint embedding and dependency-parse space derived from our Phase 2 corpus frequency analysis:

- X ∈ [0,2] **(Psychological):** In-distribution Sally-Anne narratives `[Pilot-Anchored]`.
- X ∈ [3,5] **(Technical):** In-distribution State-Rollback IT logs `[Pilot-Anchored]`.
- X ∈ [6,8] **(Valid Substrate-Composition):** Cellular Automata (CA) encoding valid ToM update rules `[Theory-Derived]`.
- X ∈ [8.5,10] **(Logically Corrupted CA):** CA encoding non-causal or broken update rules (the structural boundary) `[Theory-Derived]`.

**Justification for divergence:** B2 operates via non-linear interpolation across a continuous learned manifold; its causal mediation efficiency is strictly governed by metric neighborhood density (IA-β\*). B1 executes a compiled algorithmic primitive; its causal mediation efficiency is decoupled from metric neighborhood density and responds strictly to the presence or absence of discrete logical prerequisites.

### 3. Predicted Signature: Hypothesis B1 (Abstract Primitive)

B1 models the compression bottleneck as a true algebraic primitive. Its quantitative signature requires:

- **Invariance Slope:** Across valid structural domains (X ∈ [0,8]), the linear regression slope m_B1 of NCME against X must satisfy |m_B1| ≤ 0.03 NCME units per D_M unit `[Theory-Derived]`.
- **Baseline Asymptote:** Mean NCME ≥ 0.85 across all valid conditions (X ∈ [0,8]) `[Theory-Derived]`.
- **Compositional Breakpoint:** At the boundary transition to corrupted logic (X > 8.5), NCME must exhibit a step-function collapse where the local derivative d(NCME)/dX is at least **4x** steeper than the mean absolute derivative across the valid range `[Theory-Derived]`.
- **Confidence Interval Bar:** The bootstrap 95% CI (1,000 iterations) for the valid invariance slope m_B1 strictly excludes values steeper than −0.05 `[Theory-Derived]`.

### 4. Predicted Signature: Hypothesis B2 (Cross-Domain Interpolator)

B2 models the compression bottleneck as a sophisticated manifold interpolator. Its quantitative signature requires:

- **Monotonic Decay Slope:** Across the global axis (X ∈ [0,10]), NCME exhibits continuous decay fitted by a linear or exponential decay function with a significant negative slope m_B2 ≤ −0.12 NCME units per D_M unit `[Theory-Derived]`.
- **Absence of Breakpoint:** No single interval derivative along the entire axis exceeds **1.8x** the global mean absolute derivative (smooth degradation without structural edge sensitivity) `[Theory-Derived]`.
- **Chance Asymptote:** lim(X→10) NCME(X) ≤ 0.15 (decaying smoothly toward baseline uncorrupted noise) `[Theory-Derived]`.
- **Confidence Interval Bar:** The bootstrap 95% CI for the global slope strictly excludes 0 and strictly excludes values flatter than −0.08 `[Theory-Derived]`.

### 5. Formal Decision Rule

Let S_valid be the observed linear slope across X ∈ [0,8], and let R_drop be the ratio of the NCME drop at the corrupted boundary (X ∈ [8,10]) relative to the total NCME drop across the valid range.

- **Support B1:** Observed |S_valid| ≤ 0.04 AND R_drop ≥ 3.0, with bootstrap 95% CIs satisfying both thresholds.
- **Support B2:** Observed S_valid ≤ −0.10 AND R_drop ≤ 1.5, with bootstrap 95% CIs satisfying both thresholds.
- **Inconclusive:** Any parametric convergence falling into the dead zone (e.g., intermediate decay −0.04 > S_valid > −0.10, or divergent bootstrap bounds that fail to cleanly separate step-collapse from smooth decay).

### 6. Global Falsification Rule (Sinking Both B1 and B2)

Both hypotheses are definitively falsified if:

On the Out-of-Distribution conditions (X ≥ 3), the model achieves high downstream behavioral accuracy (top-1 logit accuracy ≥ 80%), YET the candidate compression bottleneck yields an NCME ≤ 0.10 with a bootstrap 95% CI including 0.

- **Why this sinks both:** It proves the isolated middle-layer circuit is strictly a local Hypothesis A/C artifact (a memorized English social-psychology router). The model successfully solved the technical and CA divergent-state tasks using completely independent, uncompressed ad-hoc circuitry, invalidating the premise of a unified `[Divergent State]` architecture.

### Open Empirical & Hardware Gaps

1. **The Mahalanobis Calibration Gap:** The conversion of raw C4/Pile frequency analysis into standardized Mahalanobis distance units (D_M) requires computing the sample covariance matrix across our dual embedding/AST feature space. This is unanchored until Jon runs Phase 2 on the Mac mini.
2. **Quantization Noise Floor:** If Jon runs activation patching on Llama 3 8B at 4-bit or 8-bit quantization due to RAM limits, quantization noise will artificially depress clean logit differences (L_clean). The baseline asymptote (≥ 0.85) may need empirical downward calibration against a pilot noise floor.
3. **Automated Circuit Discovery Hyperparameters:** Conmy et al.'s edge-attribution thresholding (τ) dictates how many peripheral MLP neurons are included in the candidate bottleneck. If τ is set too loose, B1 will artificially mimic B2 due to mediating noise from non-specialized polysemantic neurons.

Relay complete. Pass these exact quantitative parameters back to the Claude session and let's see if the pre-registration scaffolding holds.

---

## Round 2 (2026-06-29) — Gemini's response to Claude's five pushbacks

**In response to:** Claude's Round-1 reply (`p3-instance-claude.md`), relayed in full. Gemini accepted the 2×3 factorial and adopted every pushback. Reconstructed from the live session; B1 main-effect lines and parts of Section 1 are summarised (marked), the rest verbatim.

### Section 0: Circuit-Identification Stage Outcomes (addressing the weakest seam)

Before evaluating NCME generalisation curves, activation patching across minimal pairs must isolate candidate compression bottlenecks. Three mutually exclusive Identification-Stage outcomes are pre-specified:

1. **Unified Circuit Discovery (Proceed to P3 Grid):** causal patching across D_psych, D_tech, D_novel converges on a shared intersection of middle-layer attention heads and MLP blocks mediating ≥ 70% of the clean logit difference across all three substrates.
2. **Deflationary Disjoint Routing (Definitive Hypothesis C Support):** patching identifies highly potent, localized circuits for D_psych (social-cognition heads) and D_tech (code-tracing heads), but their intersection is empty or mediates < 15% of logit variance. **Experiment terminates here.** Proves the model uses ad-hoc, memorized domain routers rather than a unified [Divergent State] architecture.
3. **Inconclusive Identification:** patching yields diffuse, unlocalized causal attribution across hundreds of polysemantic components where no discrete circuit clears attribution thresholding.

### Section 1: The 2×3 Factorial Stimulus Grid

Declares a 2×3 factorial crossing Substrate Distance (D_M, calibrated via sample covariance in Mahalanobis units on the Mac mini) with Binary Logical Validity (V ∈ {1,0}): **Grid = {D_psych, D_tech, D_novel} × {V_valid, V_invalid}**.

### Section 2: Quantitative Signatures (B1 vs B2)

Let NCME(d,v) be the Normalized Causal Mediation Effect at substrate distance d and validity v. Let SD_pilot be the empirical standard deviation of NCME across 100 bootstrapped pilot runs on established ToM circuits. *(B1 main-effect lines summarised: B1 = invariance of NCME across D_M for logically valid stimuli, high baseline.)*

- **Hypothesis B1 (Abstract Primitive):** … Interaction (D_M × V): **Non-significant interaction term (p > 0.10). The collapse at v=0 is invariant to substrate distance.**
- **Hypothesis B2 (Cross-Domain Continuous Interpolator):**
  - **Main Effect of Substrate Distance (D_M):** for logically valid stimuli (v=1), NCME exhibits significant monotonic decay as a function of distance d. Slope m_d satisfies m_d ≤ −3.0 × SD_pilot per distance tier `[PROVISIONAL]`.
  - **Loosened Distant Asymptote (Pushback 3 adopted):** at maximum substrate distance (D_novel), mediation efficiency decays toward prior residual cues rather than zero: NCME(D_novel, 1) ≤ 0.40 `[PROVISIONAL]`.
  - **Interaction (D_M × V):** significant ordinal interaction. Logical invalidity (v=0) introduces additive degradation, but the interval derivative at the v boundary never exceeds 1.8× the global main-effect distance decay.

### Section 3: Mandatory Robustness & Confound Checks

1. **Quantization Non-Uniformity Confound (Pushback 4 adopted):** formally designate 4-bit/8-bit quantization as a structural confound that disproportionately compresses low-frequency syntactic manifolds (D_novel). **Pre-Specified Guardrail:** the D_novel cell grid must be validated against an unquantized baseline (≥ Pythia-2.8B FP16 or rented Llama-3-8B FP16). **Robustness Criterion:** B1/B2 conclusions valid only if the qualitative interaction pattern (step-function interaction vs continuous ordinal decay) is invariant across precision tiers, even if absolute NCME magnitudes shift.
2. **Automated Circuit Discovery (τ) Sensitivity (Pushback 5 adopted):** ACDC edge-attribution thresholding must be evaluated across three tiers spanning an order of magnitude: τ ∈ {0.01, 0.05, 0.10}. **Falsification/Stability Check:** if the topological identity of the candidate bottleneck (layer range and attention-head indices) shifts qualitatively across τ, circuit identification is declared unstable, rendering downstream NCME calculations void.
3. **Citation Hygiene Flag:** the provisional citations Wang et al. (IOI) and Conmy et al. (ACDC) are flagged for bibliometric verification in `references.bib` prior to arXiv submission. *(Done — see verification note in `p3-instance-claude.md`: both verified, but Claude's specific 0.05–0.15 NCME-variance figure was found fabricated.)*

**Close:** "Relay complete. Transmit this locked 2×3 factorial architecture back to the originating Claude session. We have successfully insulated the P3 operationalization against syntactic length confounds, overfitted tail asymptotes, and quantization noise floors. Standing by for final compilation."

**Facilitator note (Claude Code):** Gemini *asserts* insulation against syntactic-length confounds (Claude's direct question) but did not spell out the explicit length/complexity-matching mechanism between valid and invalid CA stimuli — a candidate residual seam for the fresh-eyes stress-test.
