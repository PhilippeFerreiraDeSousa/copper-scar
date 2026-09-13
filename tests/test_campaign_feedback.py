from copper_scar.tools.copperhead.campaign_feedback import score_preview


def action(ref='R71',delta=(-6,-1)):
    return dict(parent_board_sha256='parent',refs=[ref],translation_mm=list(delta),rotation_deg=180,nets=['CH2_IMON','GND'],local_approach=dict(after_mm=5.8))


def failure():
    return dict(attempt='failed-r71',action=action(),native_delta=3,split_groups=[['pad-a','pad-b']],collision_removals=[dict(uuid='collateral-via',net='CH2_SBU2_IGN')])


def test_exact_failed_pose_is_excluded_despite_shorter_approach():
    result=score_preview(action(),dict(removed=[],native_errors_remaining=0),dict(split_groups=[]),[failure()])
    assert not result['eligible']
    assert result['feedback_record_ids']==['failed-r71']


def test_recorded_collateral_cut_changes_next_candidate_ranking():
    candidate=action(delta=(-5,-1))
    clear=score_preview(candidate,dict(removed=[],native_errors_remaining=0),dict(split_groups=[]),[failure()])
    cut=score_preview(candidate,dict(removed=[dict(uuid='collateral-via',net='CH2_SBU2_IGN')],native_errors_remaining=0),dict(split_groups=[['pad-a','pad-b']]),[failure()])
    assert clear['score']<cut['score']
    assert cut['repeated_collateral_records']==[dict(attempt='failed-r71',feature_uuids=['collateral-via'])]
    assert cut['feedback_record_ids']==['failed-r71']


def test_changed_parent_does_not_fabricate_exact_pose_repeat():
    result=score_preview({**action(),'parent_board_sha256':'different'},dict(removed=[],native_errors_remaining=0),dict(split_groups=[]),[failure()])
    assert result['eligible']
