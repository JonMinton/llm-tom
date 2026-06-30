"""Stimulus schema for the primary matrix and the recursive OOD probe.

Defines the factorial schema and lightweight placeholder generators so the
pipeline and tests can run. The real linguistic content (matched Sally-Anne sets,
the State-Rollback isomorph, cellular-automata-as-belief-systems) is finalised in
``../../stimuli/``. The recursive probe holds the same logical content constant
across surface forms (structural novelty varied at fixed surface novelty).
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Literal

Substrate = Literal["psychological", "technical", "novel"]
Surface = Literal["S0", "S1", "S2"]  # narrative English / code-like / logical notation
Structural = Literal["T0", "T1", "T2"]  # standard / deeply-nested / non-standard update rule
Validity = Literal["valid", "invalid"]


@dataclass(frozen=True)
class StimulusItem:
    item_id: str
    prompt: str
    correct_token: str
    incorrect_token: str
    surface: Surface
    structural: Structural
    validity: Validity
    surface_ground_truth: str  # target for the upstream encoding-gate ridge probe


def factorial_grid_keys() -> list[tuple[Surface, Structural, Validity]]:
    """The Surface x Structural x Validity cells of the recursive OOD probe (3x3x2)."""
    return list(product(("S0", "S1", "S2"), ("T0", "T1", "T2"), ("valid", "invalid")))


def render(content_id: str, surface: Surface, structural: Structural, validity: Validity):
    """Render a fixed logical content into a (surface, structural, validity) cell.

    Delegates to the DRAFT content in ``stimuli_content`` (psychological + technical,
    T0/T1 only; T2/novel deferred). Lazy import avoids a module cycle.
    """
    from .stimuli_content import ALL_CONTENTS
    from .stimuli_content import render as _render

    by_id = {c.content_id: c for c in ALL_CONTENTS}
    if content_id not in by_id:
        raise KeyError(f"unknown content_id {content_id!r}; have {sorted(by_id)}")
    return _render(by_id[content_id], surface, structural, validity)


def placeholder_items(n_per_cell: int = 1) -> list[StimulusItem]:
    """Trivial, well-formed items for PIPELINE VALIDATION ONLY (not scientific stimuli)."""
    items: list[StimulusItem] = []
    for s, t, v in factorial_grid_keys():
        for i in range(n_per_cell):
            items.append(
                StimulusItem(
                    item_id=f"{s}-{t}-{v}-{i}",
                    prompt=f"[{s}|{t}|{v}] placeholder prompt {i}",
                    correct_token=" A",
                    incorrect_token=" B",
                    surface=s,
                    structural=t,
                    validity=v,
                    surface_ground_truth="A",
                )
            )
    return items
