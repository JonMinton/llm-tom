import numpy as np

from llm_tom.sd_pilot import bootstrap_ncme_sd


def test_bootstrap_sd_positive_and_deterministic():
    rng = np.random.default_rng(0)
    den = 4.0 + rng.normal(0, 0.5, 100)
    num = 2.0 + rng.normal(0, 0.5, 100)
    s1 = bootstrap_ncme_sd(num, den, n_boot=500, seed=42)
    s2 = bootstrap_ncme_sd(num, den, n_boot=500, seed=42)
    assert s1 == s2
    assert s1 > 0
