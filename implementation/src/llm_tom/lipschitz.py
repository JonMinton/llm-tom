"""Support sparsity ``sigma(x)`` and the Lipschitz-envelope test (the flatness fix).

A continuous interpolator obeys a bounded decay envelope
``NCME_max(sigma) <= 1 - lambda * sigma``. B1 is supported when NCME stays above a
high floor in genuinely sparse-support regions (``sigma >> 1/lambda``), VIOLATING
that envelope — a positive, falsifiable signature rather than a null. This is the
fix for the "flat NCME could be interpolation over interior points" confound.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


def support_sparsity(embeddings, k: int = 50, cov=None) -> np.ndarray:
    """``sigma(x)`` = mean distance to the ``k`` nearest neighbours.

    Mahalanobis metric if the reference-corpus covariance ``cov`` is supplied,
    else Euclidean. ``embeddings``: ``(n, d)``. Pilot-scale dense implementation.
    """
    x = np.asarray(embeddings, float)
    n = len(x)
    k = min(k, n - 1)
    if cov is not None:
        # Whiten by the inverse covariance: Mahalanobis = Euclidean in whitened space.
        ell = np.linalg.cholesky(np.linalg.inv(np.asarray(cov, float)))
        x = x @ ell.T
    d2 = ((x[:, None, :] - x[None, :, :]) ** 2).sum(-1)
    np.fill_diagonal(d2, np.inf)
    dist = np.sqrt(np.sort(d2, axis=1)[:, :k])
    return dist.mean(axis=1)


@dataclass(frozen=True)
class LipschitzResult:
    violates_envelope: np.ndarray  # bool per point: NCME above the 1 - lambda*sigma envelope
    b1_supported: bool  # any genuinely sparse-support point stays above the floor
    envelope: np.ndarray  # the envelope value per point


def lipschitz_test(sigma, ncme, lam: float = 0.1, b1_floor: float = 0.85) -> LipschitzResult:
    """Classify ``(sigma, ncme)`` points against the envelope ``1 - lam*sigma``.

    B1 supported iff any point in genuinely sparse support (``sigma > 1/lam``)
    keeps ``NCME >= b1_floor`` (i.e. violates the interpolator's Lipschitz bound).
    """
    sigma = np.asarray(sigma, float)
    ncme = np.asarray(ncme, float)
    envelope = 1.0 - lam * sigma
    violates = ncme > envelope
    sparse = sigma > (1.0 / lam)
    b1 = bool(np.any(sparse & (ncme >= b1_floor)))
    return LipschitzResult(violates, b1, envelope)
