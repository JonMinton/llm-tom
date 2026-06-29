"""Normalized Causal Mediation Effect (NCME) and Fieller confidence intervals.

``NCME = (L_patched - L_corrupted) / (L_clean - L_corrupted)`` where ``L`` is the
logit difference between the correct and incorrect state-query tokens.

Per the converged design we DO NOT gate on the denominator (gating on
``|L_clean - L_corrupted|`` is survivorship bias: it discards exactly the
distant-OOD trials where B2 predicts the forward pass collapses). Instead we
report Fieller (1954) intervals, which widen honestly — to unbounded — as the
denominator approaches zero. See ``../../prereg/notes/p3-synthesis.md``.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import stats


@dataclass(frozen=True)
class Interval:
    point: float
    lo: float
    hi: float
    unbounded: bool  # True when Fieller's g >= 1 (denominator ~ 0): CI is unbounded, not dropped


def ncme_pointwise(l_clean, l_patched, l_corrupted) -> np.ndarray:
    """Per-trial NCME from per-trial logit differences (1-D, paired arrays)."""
    num = np.asarray(l_patched, float) - np.asarray(l_corrupted, float)
    den = np.asarray(l_clean, float) - np.asarray(l_corrupted, float)
    return num / den


def fieller_interval(num, den, alpha: float = 0.05) -> Interval:
    """Fieller (1954) CI for the ratio ``mean(num) / mean(den)`` of paired samples.

    Returns an *unbounded* interval (``unbounded=True``) when the denominator is
    not significantly different from zero (Fieller's ``g >= 1``) — the B2-collapse
    regime, kept and reported rather than discarded.
    """
    num = np.asarray(num, float)
    den = np.asarray(den, float)
    n = len(num)
    if n != len(den) or n < 2:
        raise ValueError("num and den must be paired arrays of length >= 2")
    mn, md = num.mean(), den.mean()
    cov = np.cov(num, den, ddof=1) / n  # variances/covariance OF THE MEANS
    v_nn, v_dd, v_nd = cov[0, 0], cov[1, 1], cov[0, 1]
    r = mn / md
    t = stats.t.ppf(1 - alpha / 2, df=n - 1)
    g = (t**2) * v_dd / (md**2)
    disc = v_nn - 2 * r * v_nd + r**2 * v_dd - g * (v_nn - v_nd**2 / v_dd)
    if g >= 1 or disc < 0:
        return Interval(point=float(r), lo=float("-inf"), hi=float("inf"), unbounded=True)
    centre = (r - g * v_nd / v_dd) / (1 - g)
    halfwidth = (t / md) * np.sqrt(disc) / (1 - g)
    lo, hi = centre - halfwidth, centre + halfwidth
    return Interval(point=float(r), lo=float(min(lo, hi)), hi=float(max(lo, hi)), unbounded=False)


def ncme_aggregate(l_clean, l_patched, l_corrupted, alpha: float = 0.05) -> Interval:
    """Aggregate NCME with a Fieller CI from paired per-trial logit differences."""
    num = np.asarray(l_patched, float) - np.asarray(l_corrupted, float)
    den = np.asarray(l_clean, float) - np.asarray(l_corrupted, float)
    return fieller_interval(num, den, alpha=alpha)
