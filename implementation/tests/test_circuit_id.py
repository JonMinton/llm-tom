import numpy as np

from llm_tom.circuit_id import identify_shared_circuit


def test_unified_when_shared_component_mediates_enough():
    # 3 conditions x 4 components; component 0 strong in all, sum >= 0.70 per condition
    eff = np.array(
        [
            [0.80, 0.05, 0.05, 0.05],
            [0.75, 0.05, 0.05, 0.05],
            [0.72, 0.05, 0.05, 0.05],
        ]
    )
    r = identify_shared_circuit(eff, component_threshold=0.5)
    assert r.outcome == "unified"
    assert 0 in r.shared_components


def test_disjoint_when_each_condition_potent_but_no_overlap():
    eff = np.array(
        [
            [0.80, 0.00, 0.00],
            [0.00, 0.80, 0.00],
            [0.00, 0.00, 0.80],
        ]
    )
    r = identify_shared_circuit(eff, component_threshold=0.5)
    assert r.outcome == "disjoint"
    assert r.shared_components == ()


def test_inconclusive_when_diffuse():
    eff = np.full((3, 5), 0.1)  # nothing potent anywhere
    r = identify_shared_circuit(eff, component_threshold=0.5)
    assert r.outcome == "inconclusive"
