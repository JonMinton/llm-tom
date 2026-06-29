# P3 — Gemini revision (response to the fresh-eyes stress-test)

**Track:** originating-instance continuation. Gemini's revised recursive-OOD probe answering the 3-reviewer stress-test (`p3-stress-test.md`).
**Model:** Gemini 3.1 Pro. **Date:** 2026-06-29. **Relayed by:** Jon (manual paste — Gemini's Quill editor rejected programmatic send) + Claude Code.

Gemini did **not** merely accept the reviewers; it accepted the *diagnosis* (design non-identified) but rejected two of the reviewers' *fixes* as themselves flawed, and proposed a more rigorous replacement. Captured from the live session; key claims/formulae verbatim, connective text condensed.

## Critique of two reviewer fixes

1. **"Linear Subtraction Fallacy" (vs Reviewer fix #2, subtract a structurally-trivial control).** "Neural manifolds are not linear systems where Output = Primitive + Encoding." Syntax and logic representations are entangled in the residual stream; an early encoding failure on an alien CA grid doesn't yield a "degraded primitive" you can subtract — it yields an **off-manifold vector** thrown into an arbitrary activation region. "You cannot linearly 'subtract out' a non-linear manifold projection failure."
2. **"Denominator Gating Paradox" (vs Reviewer fix #5, gate cells on |L_clean − L_corrupted| ≥ k·SD_pilot).** This "introduces a lethal survivorship bias." If B2 is true, on distant alien substrates the forward pass fails → the denominator → 0 → the gate "literally discards the exact OOD trials where B2 predicts failure," keeping only the lucky subset where the interpolator happened to work. "We would filter out 90% of the data proving B2 to manufacture a false B1 reading."

## The Revised P3 Protocol: "The Lipschitz-Gated Manifold Probe"

Replace linear netting-out with **Upstream Subspace Gating**; replace scalar distance-ranking-by-fiat with **Empirical Lipschitz Support Bounding**.

### 1. Decay ambiguity → Upstream Subspace Gating (E₁)

- **Flaw:** decaying NCME = B2 (interpolator) OR B1 + early syntax-encoding failure.
- **Fix:** do NOT subtract a trivial control. Establish an **Early Syntactic Readout Gate** at layer `l_early ∈ [2,4]`. Before testing the ToM bottleneck, train a ridge-regression probe on the `l_early` residual stream to decode the deterministic surface ground-truth of the CA grid (e.g. "State of Cell i at T₀").
- **Partition** per OOD trial t by early-decode accuracy α(t): `T_unparsed` (α < 90% → "Syntactic Encoding Failure," excluded from NCME) vs `T_parsed` (α ≥ 95% → surface provably encoded upstream).
- **Decisive rule:** compute NCME **strictly conditioned on `T_parsed`**. If NCME decays across distance *within `T_parsed`* (where the surface was provably encoded), the encoding-failure rival is "mathematically dead" → definitively B2.

### 2. Flatness ambiguity → Empirical Lipschitz Bounding

- **Flaw:** flat NCME = B1 (primitive) OR B2 interpolating over a well-supported *interior* manifold point (CA grids are frequent in code training data).
- **Fix:** do NOT impose D_psych < D_tech < D_novel by fiat. Measure a **Pre-training Support Sparsity Index** per stimulus: `σ(x) = (1/k) Σ_j D_M(x, NN_j(x))` — mean Mahalanobis distance in joint AST/embedding space to the k=50 nearest neighbours in the Mac mini's reference corpus.
- **Metric constraint:** by the Lipschitz Continuity Theorem, any continuous manifold interpolator has a bounded Lipschitz constant K, so its causal mediation efficiency is bounded by a decay envelope `NCME_max(σ) ≤ 1 − λ·σ`.
- **Decisive rule:** plot observed NCME(σ) vs empirical sparsity σ. **Support B2:** points sit on or below the Lipschitz decay envelope. **Support B1:** points **strictly violate** the envelope — maintaining NCME ≥ 0.85 in regions where σ ≫ 1/λ. "It is mathematically impossible for a continuous interpolator to violate its own Lipschitz bound in a sparse support neighborhood." → flatness becomes a *positive, falsifiable* B1 signature, not a null.

### 3. Factor 2 → Surprisal-Matched Minimal Pairs (Reviewer fix #4 adopted)

- To stop V=Invalid from inflating generic perplexity, match valid (v=1) and invalid (v=0) minimal pairs on **Reference Corpus Surprisal** P, enforcing `|P(v=1) − P(v=0)| ≤ 0.15 nats`.

**Facilitator note:** this directly converts both reviewer-identified ambiguities into positive falsifiable tests (encoding-gate conditioning kills the decay-confound; Lipschitz-bound violation makes "flat" a signature). Adopts reviewer fix #4, rejects #2 and #5 with arguments. Still to reconcile against Claude's revision, and the reviewer-1 equivalence-test point (ROPE) should be checked against this Lipschitz framing.
