"""Candidate shared-circuit identification and its three pre-specified outcomes.

- **Unified**: a shared intersection of components mediates >= ``tau_unified`` of
  the clean logit difference across ALL conditions -> proceed to the recursive probe.
- **Deflationary-disjoint**: potent per-condition circuits whose intersection
  mediates <= ``tau_disjoint`` -> definitive Hypothesis C, terminate.
- **Inconclusive**: diffuse, no discrete shared circuit.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np

CircuitOutcome = Literal["unified", "disjoint", "inconclusive"]


@dataclass(frozen=True)
class CircuitResult:
    outcome: CircuitOutcome
    shared_components: tuple[int, ...]
    mediation_fraction: float


def identify_shared_circuit(
    effects_by_condition,
    component_threshold: float,
    tau_unified: float = 0.70,
    tau_disjoint: float = 0.15,
) -> CircuitResult:
    """Intersect components above ``component_threshold`` in EVERY condition.

    ``effects_by_condition``: ``(n_conditions, n_components)`` array, each entry the
    fraction of the clean logit difference mediated by that component in that
    condition. The intersection's mediation is taken as the weakest (min) across
    conditions, then classified.
    """
    eff = np.asarray(effects_by_condition, float)
    above = eff >= component_threshold
    shared_mask = above.all(axis=0)
    shared = tuple(int(i) for i in np.where(shared_mask)[0])

    if not shared:
        # No shared circuit. Potent-but-disjoint per condition => Hypothesis C; else diffuse.
        each_condition_potent = bool(above.any(axis=1).all())
        return CircuitResult("disjoint" if each_condition_potent else "inconclusive", shared, 0.0)

    frac = float(eff[:, shared_mask].sum(axis=1).min())
    if frac >= tau_unified:
        outcome: CircuitOutcome = "unified"
    elif frac <= tau_disjoint:
        outcome = "disjoint"
    else:
        outcome = "inconclusive"
    return CircuitResult(outcome, shared, frac)
