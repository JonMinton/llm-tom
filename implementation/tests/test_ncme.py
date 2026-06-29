import numpy as np

from llm_tom.ncme import fieller_interval, ncme_aggregate, ncme_pointwise


def test_pointwise_ratio():
    # num = patched - corrupted = 1.0; den = clean - corrupted = 1.5; ratio = 2/3
    got = ncme_pointwise([2.0, 2.0], [1.5, 1.5], [0.5, 0.5])
    assert np.allclose(got, [1.0 / 1.5, 1.0 / 1.5])


def test_fieller_bounded_with_strong_denominator():
    rng = np.random.default_rng(0)
    den = 5.0 + rng.normal(0, 0.1, 200)  # denominator far from zero
    num = 3.0 + rng.normal(0, 0.1, 200)
    ci = fieller_interval(num, den, alpha=0.05)
    assert not ci.unbounded
    assert ci.lo < ci.point < ci.hi
    assert abs(ci.point - 0.6) < 0.05


def test_fieller_unbounded_when_denominator_near_zero():
    rng = np.random.default_rng(1)
    den = rng.normal(0.0, 1.0, 100)  # denominator straddles zero (B2-collapse regime)
    num = rng.normal(0.1, 1.0, 100)
    ci = fieller_interval(num, den, alpha=0.05)
    assert ci.unbounded  # honestly unbounded, NOT discarded


def test_aggregate_matches_fieller():
    rng = np.random.default_rng(2)
    clean = 5.0 + rng.normal(0, 0.2, 100)
    patched = 4.0 + rng.normal(0, 0.2, 100)
    corrupted = 1.0 + rng.normal(0, 0.2, 100)
    agg = ncme_aggregate(clean, patched, corrupted)
    direct = fieller_interval(patched - corrupted, clean - corrupted)
    assert np.isclose(agg.point, direct.point)
