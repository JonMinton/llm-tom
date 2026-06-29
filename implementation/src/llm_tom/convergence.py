"""Cross-lens convergence summary.

Assemble per-layer outputs from the four lenses into one layer-indexed table, to
inspect whether they agree on a single computational locus — the standard for
"structural reality" rather than a single-lens artefact.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class LayerRow:
    layer: int
    intrinsic_dim: float | None = None  # geometric lens (TwoNN/GRIDE)
    probe_acc: float | None = None  # behavioural lens (linear probe)
    patch_effect: float | None = None  # causal lens (activation patching)
    topo_distance: float | None = None  # topological lens (Wasserstein between conditions)


@dataclass
class ConvergenceTable:
    rows: list[LayerRow] = field(default_factory=list)

    def add(self, row: LayerRow) -> None:
        self.rows.append(row)

    def as_dicts(self) -> list[dict]:
        return [vars(r) for r in self.rows]

    def compression_layer(self) -> int | None:
        """The layer of minimal intrinsic dimension (the predicted compression /
        operational-discretisation zone), if intrinsic dimension is populated."""
        rows = [r for r in self.rows if r.intrinsic_dim is not None]
        return min(rows, key=lambda r: r.intrinsic_dim).layer if rows else None
