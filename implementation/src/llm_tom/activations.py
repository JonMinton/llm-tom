"""Residual-stream activation extraction via TransformerLens.

``torch`` / ``transformer_lens`` are imported lazily so the statistical core and
its tests run without the heavy ML stack. Wired for the M4 pilot host.
"""

from __future__ import annotations


def load_model(model_name: str = "pythia-160m", device: str = "cpu"):
    """Load a HookedTransformer. Heavy import is deferred to call time."""
    from transformer_lens import HookedTransformer

    return HookedTransformer.from_pretrained(model_name, device=device)


def run_with_cache(model, prompt: str):
    """Return ``(logits, cache)`` for a single prompt."""
    tokens = model.to_tokens(prompt)
    logits, cache = model.run_with_cache(tokens)
    return logits, cache


def residual_by_layer(cache, n_layers: int):
    """Stack the last-token ``resid_post`` across layers -> ``(n_layers, d_model)``."""
    import numpy as np

    return np.stack(
        [cache["resid_post", layer][0, -1].detach().cpu().numpy() for layer in range(n_layers)]
    )
