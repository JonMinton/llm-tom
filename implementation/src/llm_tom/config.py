"""Provisional configuration for the llm-tom pilot.

**Every numeric threshold here is PROVISIONAL** and is pilot-calibrated per the
Stage-1 pre-registration; the Stage-2 registration locks the calibrated values.
These are defaults so the pipeline runs end-to-end, NOT scientific commitments.
See ``../../prereg/notes/p3-synthesis.md`` and ``../../prereg/prereg.md``.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Thresholds:
    """All PROVISIONAL, pending Stage-2 pilot calibration."""

    rope_sd_multiple: float = 1.0  # ROPE half-width = r * SD_pilot (B1 equivalence band)
    deadzone_sd_multiple: float = 1.5  # dead-zone alternative effect, for the power analysis
    lipschitz_lambda: float = 0.1  # envelope slope: NCME_max(sigma) = 1 - lambda * sigma
    b1_ncme_floor: float = 0.85  # B1 keeps NCME >= this in sparse-support regions
    b2_asymptote_max: float = 0.40  # loosened distant asymptote for B2
    encoding_gate_pass: float = 0.95  # alpha >= this  => T_parsed (surface encoded; kept)
    encoding_gate_fail: float = 0.90  # alpha <  this  => T_unparsed (excluded)
    circuit_unified_frac: float = 0.70  # shared intersection mediates >= this => Unified
    circuit_disjoint_frac: float = 0.15  # <= this => Deflationary-disjoint (Hypothesis C)
    knn_k: int = 50  # neighbours for the support-sparsity index sigma(x)
    n_bootstrap: int = 1000
    falsify_behavioural_acc: float = 0.80  # >= this accuracy AND NCME<=below => sinks B1 & B2
    falsify_ncme_max: float = 0.10

    # NOTE: there is deliberately NO downstream denominator gate (it is survivorship
    # bias). Near-zero/near-zero ratio trials are kept and handled by Fieller intervals.


@dataclass(frozen=True)
class RunConfig:
    model_name: str = "pythia-160m"
    seed: int = 0
    early_gate_layers: tuple[int, int] = (2, 4)  # ridge probe layer range for the encoding gate
    alpha: float = 0.05
    thresholds: Thresholds = field(default_factory=Thresholds)
