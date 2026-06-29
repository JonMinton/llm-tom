from llm_tom.equivalence import decide_b1_b2, global_falsification, slope_ci, within_rope


def test_b1_when_ci_within_rope():
    ci = slope_ci(estimate=0.0, se=0.005, df=100, conf=0.90)
    assert within_rope(ci, rope_halfwidth=0.05)
    assert decide_b1_b2(ci, 0.05) == "B1"


def test_b2_when_negative_beyond_rope():
    ci = slope_ci(estimate=-0.20, se=0.01, df=100, conf=0.90)
    assert decide_b1_b2(ci, 0.05) == "B2"


def test_inconclusive_when_straddling():
    ci = slope_ci(estimate=-0.06, se=0.05, df=100, conf=0.90)
    assert decide_b1_b2(ci, 0.05) == "inconclusive"


def test_global_falsification_sinks_both():
    # high accuracy, NCME ~ 0 with CI including 0 -> bottleneck was a local artefact
    assert global_falsification(0.90, 0.05, -0.02, 0.08)
    # strong mediation -> not falsified
    assert not global_falsification(0.90, 0.50, 0.40, 0.60)
