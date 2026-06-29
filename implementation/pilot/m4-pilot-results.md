---
status: pilot run — pipeline validation only (NOT a scientific result)
model: pythia-160m
host: Apple silicon (M-series), CPU, deterministic (seed 0)
date: 2026-06-29
thresholds: ALL PROVISIONAL — calibration values, not committed
---

# M4 pilot — results note

Pipeline validation of the `implementation/` template on Pythia-160m, per the
hand-off in [`../../prereg/notes/p3-synthesis.md`](../../prereg/notes/p3-synthesis.md)
§"Hand-off to the M4 pilot". This validates that the wired patching path and the
decision core execute end-to-end on **real activations**; it makes **no** claim
about whether Pythia-160m has Theory of Mind. Every numeric value below is
PROVISIONAL and calibration-only — none is committed to `config.py`.

Reproduce: `cd implementation && python pilot/m4_pilot.py` (≈2–3 min, CPU).

## What was wired

`src/llm_tom/patching.py` — previously `raise NotImplementedError` — now implements
the TransformerLens hook loop:

- `patched_logit_diffs(model, clean_item, corrupted_item, component, pos=-1)` →
  `(l_clean, l_patched, l_corrupted)`. **Denoising direction**: runs the corrupted
  prompt, patches the clean activation of `component` into it, measures recovery.
  This is exactly the NCME quantity `(L_patched − L_corrupted)/(L_clean − L_corrupted)`.
- `component_effects(model, items, components, pos=-1)` → per-condition × per-component
  single-component NCME matrix, feeding `circuit_id.identify_shared_circuit`. The
  clean/corrupted passes are run once per condition and reused across components.
- Component specs: `("resid_post", layer)`, `("attn_out", layer)`, `("mlp_out", layer)`,
  `("z", layer, head)`; a **list** of specs patches a whole circuit jointly. `pos=-1`
  patches the final (prediction) position — robust to clean/corrupted length mismatch.

The 20 decision-core unit tests still pass unchanged (the heavy stack stays lazily
imported).

## 1. IOI patching validation (known-good circuit)

Matched clean/corrupted IOI pairs (n=24), subject-swap corruption (only the giver
name flips; token length preserved), correct/incorrect = IO/subject names.

- Baseline logit diffs: `l_clean` mean **+2.77**, `l_corrupted` mean **−4.90** —
  the corruption cleanly flips the answer, denominator `l_clean − l_corrupted` ≈ 7.7.
- **Plumbing check:** patching `resid_post` at the final layer (END position) gives
  NCME = **1.0000** exactly — copying the clean final residual reproduces the clean
  logits, confirming the hook plumbing is correct.
- **`resid_post` layer sweep** (mean NCME @END), the recovery curve:

  | L0 | L1 | L2 | L3 | L4 | L5 | L6 | L7 | L8 | L9 | L10 | L11 |
  |----|----|----|----|----|----|----|----|----|----|-----|-----|
  | .00 | .00 | .01 | .00 | .00 | −.01 | **.23** | **.46** | **.90** | .95 | .98 | 1.00 |

  Flat through L5, then the decision crystallises across L6–L9 — the predicted
  mid-late compression / operational-discretisation zone.
- **Name-mover heads** (top single-head NCME @END): **L8H9 +0.50**, L8H10 +0.17,
  L6H6 +0.14, L9H6 +0.08, L6H5 +0.07, L8H2 +0.06. (Most-negative: L9H1 −0.10, an
  S-inhibition-like head.) L8H9 is Pythia-160m's dominant name mover.
- **Circuit recovery:** patching the 6-head name-mover set `{L8H9, L8H10, L6H6,
  L9H6, L6H5, L8H2}` jointly recovers NCME = **0.931** of the clean logit
  difference; an equal-size layer-0 control set recovers **−0.001**. ⇒ *Patching the
  name-mover heads recovers the clean logit difference*, and the effect is specific.

## 2. SD_pilot calibration

`sd_pilot.bootstrap_ncme_sd` on the name-mover circuit's per-pair `(num, den)` arrays
(1000 bootstraps, seed 0):

> **SD_pilot = 0.0204** (deterministic across repeated runs). **PROVISIONAL.**

This is the bootstrap SD of the aggregate NCME (ratio of means) on the known-good
circuit — internally consistent with the between-pair NCME SD 0.109 over n=24
(0.109/√24 ≈ 0.022). It sets the scale of the ROPE and all SD_pilot-relative
thresholds; with `rope_sd_multiple = 1.0` the ROPE half-width is 0.0204. A
Stage-2 registration would lock a value from a larger, scientific-grade calibration
set, not this 24-pair pilot.

## 3. Encoding-gate alpha calibration (known-good stimuli)

Same logical content rendered in three surface forms (S0 narrative / S1 code-like /
S2 logical notation), 45 trials; ridge/logistic probe over the early gate layers
[2,4] decoding surface form (5-fold CV per-trial confidence α):

- α mean **0.998**, min **0.996** ⇒ **45/45 → `T_parsed`** (α ≥ 0.95), 0 ambiguous,
  0 `T_unparsed`.

On known-good stimuli the early layers encode surface near-perfectly, so the
PROVISIONAL 0.95 pass / 0.90 fail thresholds are satisfiable. (Genuine threshold
calibration needs the real recursive-probe stimuli, where some trials are *meant* to
fail the gate; this only confirms known-good stimuli pass.)

## 4. End-to-end `run_recursive_probe` on real activations

Placeholder 3×3×2 factorial (`stimuli.placeholder_items`), valid/invalid minimal
pairs as clean/corrupted, patching the name-mover set; SD arrays from the IOI
circuit. The full decision core ran without error and returned a `ProbeResult`:

- SD_pilot 0.0204 · ROPE 0.0204 · T-slope(S0) +0.060 (se 0.016, df 1) ·
  Fieller NCME −0.276 [−0.35, −0.22] (bounded) · Lipschitz-B1 False · both-sink
  falsification False · **verdict = inconclusive**.

The placeholder stimuli are degenerate (trivial " A"/" B" targets), so the verdict
is **not** a scientific finding — the point is that real activations flow through
patching → NCME → SD_pilot → Fieller → TOST/Lipschitz/falsification → `ProbeResult`
deterministically and without crashing. `inconclusive` is the honest expected
outcome (df=1 makes the slope CI span both ROPE and B2 territory).

## Validation-criteria status (`implementation/README.md`)

1. End-to-end on Pythia-160m, ≪10 min on an M-series Mac — **met** (CPU, ~2–3 min).
2. Each exercised lens produces non-trivial, non-NaN output — **met** (patching
   recovery curve, head map, α distribution, Fieller interval all sensible).
3. Deterministic given fixed seed — **met** (CPU; SD_pilot identical across runs).
4. Convergence summary table without error — *not exercised here* (this pilot
   targets the patching + recursive-probe decision path; the four-lens convergence
   table is a separate smoke path).

## Issues / seams (flagged, not smoothed)

- **transformer-lens 3.5.0 installed, `pyproject.toml` floor is `>=2.0`.** The 3.x
  hook-point API used here (`blocks.{l}.hook_resid_post`, `blocks.{l}.attn.hook_z`)
  is stable across 2.x/3.x, but the floor should be tightened/pinned before a
  scientific run for reproducibility.
- **Patching position.** Validation patches at the END (prediction) position — the
  canonical IOI direct-effect probe, and robust to length mismatch. The recursive
  probe over genuinely different surface forms (S0/S1/S2) will need a deliberate
  choice of patch position(s) and token-alignment handling; `pos=None` (all
  positions) requires length-aligned pairs, which arbitrary surface renderings are
  not.
- **`component_effects` cost.** O(conditions × components) forward passes (clean/
  corrupted cached per condition). Fine at pilot scale (a 144-head sweep is seconds);
  a larger model / stimulus set will want batching or attribution-patching
  approximations.
- **Name movers are Pythia-160m-specific.** L8H9 etc. are *this* model's empirical
  name movers, discovered by the sweep — not transferable head indices. The
  validated artefact is the *method* (sweep → set → joint-patch recovery), not the
  indices.
- **SD_pilot scale.** 0.0204 comes from 24 IOI pairs; treat as order-of-magnitude
  for ROPE sizing only. The real calibration set should be larger and matched to the
  recursive-probe estimator.
