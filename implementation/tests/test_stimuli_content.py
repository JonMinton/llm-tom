"""Tests for the DRAFT S x T x Validity stimulus generator (no heavy deps)."""

from __future__ import annotations

import pytest

from llm_tom import stimuli, stimuli_content


def test_grid_shape_and_fields():
    items = stimuli_content.draft_items()
    # 8 contents x 3 surfaces x 2 structurals x 2 validity
    assert len(items) == len(stimuli_content.ALL_CONTENTS) * 3 * 2 * 2
    for it in items:
        assert it.prompt and not it.prompt.endswith(" ")  # rendered, no trailing space
        for tok in (it.correct_token, it.incorrect_token):
            assert tok.startswith(" ") and " " not in tok.strip()  # single leading-space word
        assert it.surface in ("S0", "S1", "S2")
        assert it.structural in ("T0", "T1")
        assert it.validity in ("valid", "invalid")
        assert it.surface_ground_truth


def test_valid_invalid_is_a_token_flip():
    """The minimal pair swaps which answer is correct; the token set is identical."""
    c = stimuli_content.PSYCHOLOGICAL[0]
    for s in ("S0", "S1", "S2"):
        for t in ("T0", "T1"):
            v = stimuli_content.render(c, s, t, "valid")
            iv = stimuli_content.render(c, s, t, "invalid")
            assert v.correct_token == iv.incorrect_token
            assert v.incorrect_token == iv.correct_token


def test_tokens_matched_across_surface_and_structure():
    """Same content + validity -> identical answer tokens in every cell (matched)."""
    c = stimuli_content.PSYCHOLOGICAL[0]
    cells = [stimuli_content.render(c, s, t, "valid")
             for s in ("S0", "S1", "S2") for t in ("T0", "T1")]
    assert len({it.correct_token for it in cells}) == 1
    assert len({it.incorrect_token for it in cells}) == 1


def test_t2_is_deferred():
    c = stimuli_content.PSYCHOLOGICAL[0]
    with pytest.raises(NotImplementedError):
        stimuli_content.render(c, "S0", "T2", "valid")


def test_schema_render_delegates_by_id():
    c = stimuli_content.ALL_CONTENTS[0]
    viaschema = stimuli.render(c.content_id, "S1", "T0", "valid")
    direct = stimuli_content.render(c, "S1", "T0", "valid")
    assert viaschema == direct
    with pytest.raises(KeyError):
        stimuli.render("no-such-content", "S0", "T0", "valid")


def test_surface_forms_actually_differ():
    """S0/S1/S2 of the same cell are distinct strings (real surface variation)."""
    c = stimuli_content.PSYCHOLOGICAL[0]
    prompts = {stimuli_content.render(c, s, "T0", "valid").prompt for s in ("S0", "S1", "S2")}
    assert len(prompts) == 3
