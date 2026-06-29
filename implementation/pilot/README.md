# M4 pilot

Pipeline-validation driver for the `implementation/` template, run on Pythia-160m.
**Not a scientific run** — it confirms the wired patching path and the decision core
execute end-to-end on real activations, and calibrates PROVISIONAL pilot values
(`SD_pilot`, encoding-gate α). See [`m4-pilot-results.md`](m4-pilot-results.md) for
the latest run and the flagged seams.

```
cd implementation
python -m pytest -q              # 20 decision-core tests (no torch)
python pilot/m4_pilot.py         # full pilot: IOI validation + SD_pilot + gate + e2e
python pilot/m4_pilot.py --json pilot/results/m4-pilot.json   # also write a results JSON
```

Requires the heavy stack (`torch`, `transformer-lens`); install with
`uv pip install torch "transformer-lens>=2.0"` into the `implementation/` env.
Runs on CPU for determinism (~2–3 min). `pilot/results/` is git-ignored
(regenerable artefacts).

Steps: (1) IOI patching validation on a known-good circuit — plumbing check,
resid/​head sweeps, name-mover set recovery; (2) `SD_pilot` bootstrap on that
circuit; (3) encoding-gate α calibration on known-good stimuli; (4) end-to-end
`pipeline.run_recursive_probe` on the placeholder factorial. All thresholds stay
PROVISIONAL.
