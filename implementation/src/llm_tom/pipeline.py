"""End-to-end driver for the recursive OOD probe.

This is the (unit-tested) *decision core*: it bootstraps ``SD_pilot``, sets the
ROPE, applies the equivalence (TOST) decision, the Lipschitz-envelope test, and
the both-sink global falsification. The activations / patching that PRODUCE the
inputs are supplied by the model-coupled modules on the M4 host; this function
runs without ``torch`` and is covered by ``tests/test_pipeline_smoke.py``.
"""

from __future__ import annotations

from dataclasses import dataclass

from . import equivalence, lipschitz, ncme, sd_pilot
from .config import RunConfig


@dataclass
class ProbeResult:
    sd_pilot: float
    rope_halfwidth: float
    verdict: str  # "B1" | "B2" | "inconclusive"
    ncme: ncme.Interval
    lipschitz_b1: bool
    falsified: bool


def run_recursive_probe(
    trials: dict,
    slope_fit: tuple[float, float, float],
    sigma,
    ncme_per_point,
    behavioural_acc: float,
    cfg: RunConfig | None = None,
) -> ProbeResult:
    """Wire the recursive-OOD-probe decision logic.

    Parameters
    ----------
    trials
        Dict of paired logit-difference arrays: ``sd_num``/``sd_den`` (the
        known-good circuit, for ``SD_pilot``) and ``clean``/``patched``/``corrupted``
        (the encoding-gate-passed probe trials).
    slope_fit
        ``(estimate, se, df)`` of the NCME-vs-structural-novelty slope at fixed
        surface novelty.
    sigma, ncme_per_point
        Per-point support sparsity and NCME, for the Lipschitz-envelope test.
    behavioural_acc
        OOD behavioural accuracy, for the both-sink global falsification rule.
    """
    cfg = cfg or RunConfig()
    th = cfg.thresholds

    sd = sd_pilot.bootstrap_ncme_sd(
        trials["sd_num"], trials["sd_den"], n_boot=th.n_bootstrap, seed=cfg.seed
    )
    rope = th.rope_sd_multiple * sd

    est, se, df = slope_fit
    ci = equivalence.slope_ci(est, se, df, conf=0.90)
    verdict = equivalence.decide_b1_b2(ci, rope)

    agg = ncme.ncme_aggregate(
        trials["clean"], trials["patched"], trials["corrupted"], alpha=cfg.alpha
    )
    lz = lipschitz.lipschitz_test(
        sigma, ncme_per_point, lam=th.lipschitz_lambda, b1_floor=th.b1_ncme_floor
    )
    falsified = equivalence.global_falsification(
        behavioural_acc,
        agg.point,
        agg.lo,
        agg.hi,
        acc_floor=th.falsify_behavioural_acc,
        ncme_ceiling=th.falsify_ncme_max,
    )
    if falsified:
        verdict = "inconclusive"  # the both-sink falsification overrides B1/B2

    return ProbeResult(
        sd_pilot=sd,
        rope_halfwidth=rope,
        verdict=verdict,
        ncme=agg,
        lipschitz_b1=lz.b1_supported,
        falsified=falsified,
    )
