from llm_tom.stimuli import factorial_grid_keys, placeholder_items


def test_grid_is_3x3x2():
    keys = factorial_grid_keys()
    assert len(keys) == 18
    assert len(set(keys)) == 18


def test_placeholder_items_well_formed():
    items = placeholder_items(n_per_cell=2)
    assert len(items) == 36
    assert all(it.correct_token != it.incorrect_token for it in items)
    assert all(it.item_id for it in items)
