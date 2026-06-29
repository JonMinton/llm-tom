import numpy as np

from llm_tom.geometric import twonn_id


def test_twonn_recovers_low_dim():
    rng = np.random.default_rng(0)
    z = rng.normal(size=(500, 2))  # intrinsically 2-D ...
    x = np.hstack([z, np.zeros((500, 3))])  # ... embedded in 5-D
    d = twonn_id(x)
    assert 1.5 < d < 3.0
