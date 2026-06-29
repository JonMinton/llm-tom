"""End-to-end smoke test of the DECISION pipeline with synthetic (mocked) logit
differences — runs without torch/transformer_lens. Validates orchestration and
determinism; the model-coupled activation/patching steps are not exercised here.
"""

import numpy as np

from llm_tom.config import RunConfig
from llm_tom.pipeline import run_recursive_probe


def _synthetic_trials(seed=0, b2=False):
    rng = np.random.default_rng(seed)
    n = 200
    return {
        "sd_num": 3.4 + rng.normal(0, 0.3, n),  # known-good calibration circuit
        "sd_den": 4.0 + rng.normal(0, 0.3, n),
        "clean": 4.0 + rng.normal(0, 0.3, n),
        "patched": (1.0 if b2 else 3.6) + rng.normal(0, 0.3, n),
        "corrupted": 0.0 + rng.normal(0, 0.3, n),
    }


def test_pipeline_runs_and_is_deterministic():
    trials = _synthetic_trials()
    sigma = np.linspace(1, 20, 18)
    ncme_pts = np.full(18, 0.88)  # flat & high
    slope = (0.0, 0.01, 100)  # flat NCME-vs-T slope at fixed S
    r1 = run_recursive_probe(trials, slope, sigma, ncme_pts, 0.9, RunConfig())
    r2 = run_recursive_probe(trials, slope, sigma, ncme_pts, 0.9, RunConfig())
    assert r1.sd_pilot == r2.sd_pilot
    assert r1.sd_pilot > 0
    assert r1.verdict in {"B1", "B2", "inconclusive"}


def test_pipeline_flags_b2_with_steep_slope():
    trials = _synthetic_trials(b2=True)
    sigma = np.linspace(1, 20, 18)
    ncme_pts = np.linspace(0.85, 0.05, 18)  # decays under the envelope
    slope = (-0.30, 0.02, 100)  # steep negative slope at fixed S
    r = run_recursive_probe(trials, slope, sigma, ncme_pts, 0.9, RunConfig())
    assert r.verdict in {"B2", "inconclusive"}
    assert not r.lipschitz_b1
