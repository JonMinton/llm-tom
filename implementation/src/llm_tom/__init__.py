"""llm-tom: implementation template for adjudicating algorithmic Theory of Mind.

The statistical / decision core (``ncme``, ``equivalence``, ``lipschitz``,
``sd_pilot``, ``circuit_id``, ``geometric``) depends only on numpy / scipy /
scikit-learn and is unit-tested. The model-coupled lenses (``activations``,
``patching``, ``probing``, ``topology``) import ``torch`` / ``transformer_lens``
lazily and are wired for the M4 pilot host. See ``README.md`` and, for the
design they implement, ``../../prereg/notes/p3-synthesis.md``.
"""

from . import (
    circuit_id,
    config,
    encoding_gate,
    equivalence,
    geometric,
    lipschitz,
    ncme,
    sd_pilot,
    stimuli,
)

__all__ = [
    "circuit_id",
    "config",
    "encoding_gate",
    "equivalence",
    "geometric",
    "lipschitz",
    "ncme",
    "sd_pilot",
    "stimuli",
]
__version__ = "0.0.1"
