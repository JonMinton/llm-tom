"""Upstream encoding-gate.

A ridge probe at an early layer decodes the stimulus's deterministic surface
ground-truth; trials are partitioned by the decode accuracy ``alpha`` into
``T_parsed`` (kept) / ``T_unparsed`` (excluded) / ambiguous (reported). This
conditions on *"was the surface encoded"* — NOT on the bottleneck's separation —
so it does NOT discard B2's distant-failure evidence (the fix for the decay
ambiguity). The ``partition`` logic is pure and unit-tested.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class GatePartition:
    parsed: np.ndarray  # alpha >= pass_threshold  -> kept
    unparsed: np.ndarray  # alpha <  fail_threshold -> excluded (uninterpretable)
    ambiguous: np.ndarray  # in between -> reported, never silently dropped


def partition(alpha, pass_threshold: float = 0.95, fail_threshold: float = 0.90) -> GatePartition:
    """Partition trials by early-decode accuracy ``alpha`` into the gate sets."""
    a = np.asarray(alpha, float)
    return GatePartition(
        parsed=a >= pass_threshold,
        unparsed=a < fail_threshold,
        ambiguous=(a >= fail_threshold) & (a < pass_threshold),
    )


def surface_decode_confidence(early_features, surface_targets, seed: int = 0, cv: int = 5):
    """Per-trial probability the early-layer probe assigns to the TRUE surface
    class — a continuous proxy for ``alpha(t)``.

    The pre-registration specifies a ridge probe; logistic regression is used
    here only because it exposes calibrated per-trial probabilities — a Stage-2
    calibration detail. sklearn imported at call time.
    """
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import cross_val_predict

    x = np.asarray(early_features)
    y = np.asarray(surface_targets)
    proba = cross_val_predict(
        LogisticRegression(max_iter=1000, random_state=seed), x, y, cv=cv, method="predict_proba"
    )
    classes = list(np.unique(y))
    return np.array([proba[i, classes.index(y[i])] for i in range(len(y))])
