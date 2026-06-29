"""Bootstrap calibration of ``SD_pilot``.

``SD_pilot`` is the empirical standard deviation of the NCME statistic, estimated
by bootstrapping over trials on a KNOWN-GOOD (IOI-equivalent) circuit. It sets the
scale of the ROPE and all SD_pilot-relative thresholds. This is the load-bearing
Stage-2 calibration step (run on the M4); the function is deterministic given a seed.
"""

from __future__ import annotations

import numpy as np


def bootstrap_ncme_sd(num, den, n_boot: int = 1000, seed: int = 0) -> float:
    """``SD_pilot`` = std of the bootstrap distribution of ``mean(num)/mean(den)``.

    ``num``/``den`` are paired per-trial logit-difference arrays from the
    known-good calibration circuit.
    """
    num = np.asarray(num, float)
    den = np.asarray(den, float)
    n = len(num)
    if n != len(den) or n < 2:
        raise ValueError("num and den must be paired arrays of length >= 2")
    rng = np.random.default_rng(seed)
    ratios = np.empty(n_boot)
    for b in range(n_boot):
        idx = rng.integers(0, n, n)
        ratios[b] = num[idx].mean() / den[idx].mean()
    return float(np.std(ratios, ddof=1))
