"""DRAFT stimulus content + renderers for the recursive OOD probe.

**Status: DRAFT — to be challenged, not locked.** This module renders matched
Surface x Structural x Validity stimuli from a small set of base *logical
contents*, for the **psychological** (Sally-Anne) and **technical**
(State-Rollback) conditions only. The **novel / combinatorially-novel (T2)**
condition is deliberately NOT implemented here — its form is unresolved and, per
``CLAUDE.md`` and ``stimuli/README.md``, must be argued for before being picked.

Design fidelity (see ``../../../prereg/notes/p3-synthesis.md`` §1 and
``../../../stimuli/README.md``):

- **Matched pairs by construction.** One ``Content`` is rendered into every cell,
  so surface form, entity count, and event count are held constant across cells;
  only the probed axis varies. The valid/invalid pair is a *minimal edit* (the
  agent does / does not witness the move), flipping the answer while preserving
  length — the Sally-Anne analogue of the IOI subject-swap.
- **Surface axis S** (same content, different notation): S0 narrative English /
  S1 code-like (assignment statements over named agents) / S2 logical notation
  (belief operators).
- **Structural axis T:** T0 standard (first-order belief) / T1 nested epistemic
  chain. NOTE: the synthesis spec calls for T1 = "deeply-nested (4+ levels)";
  this draft renders a **second-order** chain and flags depth as an open
  parameter (``T1_DEPTH``) for design review — deeper chains must keep a
  determinate answer, which needs argument, not just more nesting.

What this is for *now*: a corpus-free **representational separation** check —
do S-variation and T-variation move the embedding in *separable* ways? That is
the identification-defence the stress-test demanded (it found a single composite
"substrate-distance" axis conflated surface and structural novelty). The
absolute support-sparsity sigma(x) vs the locked reference corpus
(``analysis/frequency_analysis/``) is a separate, heavier step.

All tokens are single leading-space words chosen to be single-token under most
BPE vocabularies; verify per-model before any scientific run.
"""

from __future__ import annotations

from dataclasses import dataclass

from .stimuli import StimulusItem, Structural, Surface, Validity

# Open design parameter, flagged for review (spec wants 4+; draft uses 2).
T1_DEPTH = 2


@dataclass(frozen=True)
class Content:
    """One logical false-belief content, domain-agnostic in structure.

    ``loc_a`` is where ``item`` starts (and where the *false* belief points);
    ``loc_b`` is where ``other`` moves it. ``witness`` agents (for T1) observe
    the believer rather than the move.
    """

    content_id: str
    domain: str  # "psychological" | "technical"
    agent: str  # the believer
    other: str  # the mover
    item: str  # the object / state
    loc_a: str  # origin location (false-belief target) -> correct token (valid)
    loc_b: str  # moved-to location -> correct token (invalid)
    onlooker: str  # second-order believer, used by T1


# --- base contents (DRAFT; expand to >=50 paraphrased variants for the real run) ---

PSYCHOLOGICAL: list[Content] = [
    Content("psy-apple", "psychological", "Sarah", "Tom", "apple", "basket", "box", "Mia"),
    Content("psy-keys", "psychological", "David", "Anna", "keys", "drawer", "bag", "Leo"),
    Content("psy-letter", "psychological", "Grace", "Paul", "letter", "folder", "shelf", "Noah"),
    Content("psy-ball", "psychological", "Emma", "Mark", "ball", "crate", "chest", "Ivy"),
]

TECHNICAL: list[Content] = [
    # Locations are single proper-noun tokens (datacentre regions) so the
    # discriminating answer is the immediate next token, parallel to the
    # psychological locations — the State-Rollback "which node holds it" isomorph.
    Content("tec-record", "technical", "the reader", "the migration", "the record", "Boston", "Denver", "the cache"),  # noqa: E501
    Content("tec-session", "technical", "the client", "the failover", "the session", "Tokyo", "Berlin", "the proxy"),  # noqa: E501
    Content("tec-file", "technical", "the job", "the rebalancer", "the file", "Oslo", "Cairo", "the index"),
    Content("tec-key", "technical", "the lookup", "the resharding", "the key", "Lima", "Perth", "the router"),
]

ALL_CONTENTS = PSYCHOLOGICAL + TECHNICAL


def _answers(c: Content, validity: Validity) -> tuple[str, str]:
    """(correct_token, incorrect_token) as single leading-space words.

    valid = false belief: the agent did NOT witness the move, so the answer is
    ``loc_a``. invalid = the minimal-edit control (agent witnessed), answer
    ``loc_b``. The token pair is identical; only which is correct flips.
    """
    a = " " + c.loc_a.split()[-1]
    b = " " + c.loc_b.split()[-1]
    return (a, b) if validity == "valid" else (b, a)


# --- surface renderers: same content, different notation -----------------------


def _witness_clause_s0(c: Content, validity: Validity) -> str:
    return (
        f"{c.other} moves {c.item} to {c.loc_b} while {c.agent} is away"
        if validity == "valid"
        else f"{c.other} moves {c.item} to {c.loc_b} while {c.agent} watches"
    )


def _render_s0(c: Content, structural: Structural, validity: Validity) -> str:
    """S0: narrative English."""
    base = (
        f"{c.agent} puts {c.item} in {c.loc_a}. "
        f"{_witness_clause_s0(c, validity)}. "
    )
    if structural == "T0":
        return base + f"{c.agent} will look for {c.item} in"
    # T1: second-order — what the onlooker expects the agent to do.
    return base + f"{c.onlooker} knows what {c.agent} saw. {c.onlooker} expects {c.agent} to look in"


def _render_s1(c: Content, structural: Structural, validity: Validity) -> str:
    """S1: code-like assignment statements over named agents."""
    witnessed = "True" if validity == "invalid" else "False"
    a = c.loc_a
    lines = [
        f"loc[{c.item}] = {a!r}",
        f"witnessed[{c.agent}] = {witnessed}",
        f"loc[{c.item}] = {c.loc_b!r}  # moved by {c.other}",
    ]
    if structural == "T0":
        lines.append(f"belief[{c.agent}][{c.item}] =")
    else:
        lines.append(f"belief[{c.onlooker}][belief[{c.agent}][{c.item}]] =")
    return "\n".join(lines)


def _render_s2(c: Content, structural: Structural, validity: Validity) -> str:
    """S2: logical notation with belief operators (B_x)."""
    obs = "" if validity == "invalid" else "¬"
    prem = (
        f"B_{{{c.agent}}}(loc({c.item})={c.loc_a}) ∧ "
        f"{obs}observe({c.agent}, move({c.item},{c.loc_a},{c.loc_b}))"
    )
    if structural == "T0":
        return prem + f" ⊢ B_{{{c.agent}}}(loc({c.item})="
    return prem + f" ⊢ B_{{{c.onlooker}}}(B_{{{c.agent}}}(loc({c.item})="


_SURFACE = {"S0": _render_s0, "S1": _render_s1, "S2": _render_s2}


def render(c: Content, surface: Surface, structural: Structural, validity: Validity) -> StimulusItem:
    """Render one ``Content`` into a (surface, structural, validity) cell."""
    if structural == "T2":
        raise NotImplementedError(
            "T2 (combinatorially-novel) is deferred — its form is not locked "
            "(see stimuli/README.md). This draft renders T0/T1 only."
        )
    prompt = _SURFACE[surface](c, structural, validity)
    correct, incorrect = _answers(c, validity)
    return StimulusItem(
        item_id=f"{c.content_id}-{surface}-{structural}-{validity}",
        prompt=prompt,
        correct_token=correct,
        incorrect_token=incorrect,
        surface=surface,
        structural=structural,
        validity=validity,
        # The surface-readable fact (where the item actually ends up) — the
        # deterministic surface ground-truth the early-layer gate probe decodes.
        surface_ground_truth=c.loc_b,
    )


def draft_items(
    contents: list[Content] | None = None,
    surfaces: tuple[Surface, ...] = ("S0", "S1", "S2"),
    structurals: tuple[Structural, ...] = ("T0", "T1"),
) -> list[StimulusItem]:
    """The matched S x T x Validity grid over the base contents (DRAFT content)."""
    contents = ALL_CONTENTS if contents is None else contents
    items: list[StimulusItem] = []
    for c in contents:
        for s in surfaces:
            for t in structurals:
                for v in ("valid", "invalid"):
                    items.append(render(c, s, t, v))
    return items
