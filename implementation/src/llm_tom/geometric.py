"""Intrinsic-dimension estimation (the geometric lens).

A dependency-light maximum-likelihood TwoNN estimator (Facco et al. 2017) so the
geometric lens runs in the smoke test without ``scikit-dim``. The full pipeline
may prefer ``scikit-dim`` / GRIDE; this is the minimal version.
"""

from __future__ import annotations

import numpy as np


def twonn_id(x, discard_fraction: float = 0.1) -> float:
    """Maximum-likelihood TwoNN intrinsic dimension of point cloud ``x`` ``(n, d)``.

    For each point, ``mu = r2 / r1`` (2nd / 1st nearest-neighbour distance); the
    MLE is ``d = N / sum(log mu)`` after discarding the largest-``mu`` tail.
    """
    x = np.asarray(x, float)
    n = len(x)
    if n < 3:
        raise ValueError("need >= 3 points")
    d2 = ((x[:, None, :] - x[None, :, :]) ** 2).sum(-1)
    np.fill_diagonal(d2, np.inf)
    nn = np.sqrt(np.sort(d2, axis=1)[:, :2])  # r1, r2 per point
    r1, r2 = nn[:, 0], nn[:, 1]
    good = r1 > 0
    mu = np.sort(r2[good] / r1[good])
    keep = max(3, int(len(mu) * (1 - discard_fraction)))
    mu = mu[:keep]
    return float(len(mu) / np.log(mu).sum())
