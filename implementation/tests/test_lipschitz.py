import numpy as np

from llm_tom.lipschitz import lipschitz_test, support_sparsity


def test_sparsity_shape_and_positive():
    x = np.random.default_rng(0).normal(size=(20, 5))
    s = support_sparsity(x, k=3)
    assert s.shape == (20,)
    assert np.all(s > 0)


def test_b1_violates_envelope_in_sparse_region():
    sigma = np.array([1.0, 5.0, 20.0])  # 1/lambda = 10, so sigma=20 is sparse support
    ncme = np.array([0.90, 0.88, 0.90])  # stays high even where support is sparse
    r = lipschitz_test(sigma, ncme, lam=0.1, b1_floor=0.85)
    assert r.b1_supported


def test_b2_under_envelope_is_not_b1():
    sigma = np.array([1.0, 5.0, 20.0])
    ncme = np.array([0.85, 0.40, 0.05])  # decays; in the sparse region NCME is low
    r = lipschitz_test(sigma, ncme, lam=0.1, b1_floor=0.85)
    assert not r.b1_supported
