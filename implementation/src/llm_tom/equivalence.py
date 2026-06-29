"""Equivalence (TOST / ROPE) testing and the B1 / B2 / inconclusive decision rule.

B1 is supported only by POSITIVELY clearing an equivalence bound (the slope CI
lies entirely within the ROPE), never by failure-to-reject a null — this is the
fix for the "confirmation-by-weakness" flaw the stress-test identified. B2 is
supported by a significant negative slope entirely beyond the ROPE. Everything
else is reported as ``inconclusive`` (a real verdict, not forced).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from scipy import stats

Verdict = Literal["B1", "B2", "inconclusive"]


@dataclass(frozen=True)
class SlopeCI:
    estimate: float
    lo: float
    hi: float


def slope_ci(estimate: float, se: float, df: float, conf: float = 0.90) -> SlopeCI:
    """Two-sided ``conf`` CI for a slope estimate with standard error ``se``."""
    t = stats.t.ppf(1 - (1 - conf) / 2, df=df)
    h = t * se
    return SlopeCI(float(estimate), float(estimate - h), float(estimate + h))


def within_rope(ci: SlopeCI, rope_halfwidth: float) -> bool:
    """TOST equivalence: the slope CI lies entirely within ``[-rope, +rope]``."""
    rope = abs(rope_halfwidth)
    return ci.lo >= -rope and ci.hi <= rope


def decide_b1_b2(ci: SlopeCI, rope_halfwidth: float) -> Verdict:
    """Map a slope CI + ROPE to a verdict. Inconclusive when the CI straddles
    both the ROPE interior and B2 territory."""
    rope = abs(rope_halfwidth)
    if within_rope(ci, rope):
        return "B1"
    if ci.hi < -rope:
        return "B2"
    return "inconclusive"


def global_falsification(
    behavioural_acc: float,
    ncme_point: float,
    ncme_ci_lo: float,
    ncme_ci_hi: float,
    acc_floor: float = 0.80,
    ncme_ceiling: float = 0.10,
) -> bool:
    """Sinks BOTH B1 and B2: high OOD behavioural accuracy yet the candidate
    bottleneck mediates ~nothing (NCME <= ceiling, with the CI including 0) —
    the bottleneck was a local A/C artefact and OOD success came from elsewhere.
    """
    return (
        behavioural_acc >= acc_floor
        and ncme_point <= ncme_ceiling
        and ncme_ci_lo <= 0.0 <= ncme_ci_hi
    )
