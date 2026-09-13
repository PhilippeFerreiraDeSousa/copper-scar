from scripts.copperhead_observability import unique_remote_rows


def test_identical_api_replays_collapse_without_losing_conflicting_evidence():
    original = {'attempt_id': 'a', '_step': 3, 'missing': 55, 'media': {'path': 'same.png'}}
    duplicate = {'media': {'path': 'same.png'}, 'missing': 55, '_step': 3, 'attempt_id': 'a'}
    conflicting = {**original, 'missing': 54}
    assert unique_remote_rows([original, duplicate, conflicting]) == [original, conflicting]


def test_relogged_attempt_with_another_step_or_image_remains_duplicate_attempt():
    original = {'attempt_id': 'a', '_step': 3, 'media': {'path': 'same.png'}}
    new_step = {**original, '_step': 4}
    new_image = {**original, 'media': {'path': 'different.png'}}
    assert len(unique_remote_rows([original, new_step, new_image])) == 3
