"""Linear probing (the behavioural lens)."""

from __future__ import annotations


def fit_layer_probe(features, labels, seed: int = 0, cv: int = 5) -> float:
    """Cross-validated per-layer linear-probe accuracy for the divergent-state
    distinction. Returns the mean CV accuracy. (sklearn imported at call time.)
    """
    import numpy as np
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import cross_val_score

    clf = LogisticRegression(max_iter=1000, random_state=seed)
    return float(cross_val_score(clf, np.asarray(features), np.asarray(labels), cv=cv).mean())
