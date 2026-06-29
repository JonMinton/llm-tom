"""Persistent homology (the topological lens). ``gudhi`` imported lazily."""

from __future__ import annotations


def persistence_diagram(point_cloud, max_dim: int = 1):
    """Vietoris-Rips persistence of a per-condition activation point cloud."""
    import gudhi
    import numpy as np

    pts = np.asarray(point_cloud, float)
    rips = gudhi.RipsComplex(points=pts)
    st = rips.create_simplex_tree(max_dimension=max_dim + 1)
    st.compute_persistence()
    return st.persistence()


def wasserstein_between(diag_a, diag_b, order: int = 1) -> float:
    """Wasserstein distance between two persistence diagrams (per layer, between
    conditions) — the per-layer topological summary used in the convergence table.
    """
    import numpy as np
    from gudhi.wasserstein import wasserstein_distance

    def _finite_points(diag):
        return np.array(
            [[birth, death] for (_dim, (birth, death)) in diag if death != float("inf")]
        )

    return float(wasserstein_distance(_finite_points(diag_a), _finite_points(diag_b), order=order))
