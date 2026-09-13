import hashlib,json
import pytest
from copper_scar.tools.copperhead.routing_options import ORIGINAL,SMALL,context,dsn_context,record_context,verify_after_exports
from copper_scar.tools.copperhead.campaign_feedback import score_preview


@pytest.mark.parametrize('action',['placement','via_seed'])
def test_ordinary_pose_and_seed_always_reverify_exported_options(action):
    commands=[(action,['apply'],60),('export',['native-export'],60),('route',['router'],600)]
    result=verify_after_exports(commands,'python','verify.py','candidate')
    assert [x[0] for x in result]==[action,'export','export_effective_options','route']


def test_fanout_then_fresh_export_verifies_both_inputs():
    commands=[(name,[name],60) for name in ('fanout_export','fanout','fanout_import','export','route')]
    assert [x[0] for x in verify_after_exports(commands,'python','verify.py','candidate')]==['fanout_export','fanout_export_effective_options','fanout','fanout_import','export','export_effective_options','route']


def test_library_presence_does_not_change_creation_context():
    source=f'(library (padstack "{SMALL}")) (network (class default (circuit (use_via "{ORIGINAL}"))))'
    assert dsn_context(source,'rules')['digest']==context([ORIGINAL],'rules')['digest']
    assert dsn_context(source,'rules')['digest']!=context([ORIGINAL,SMALL],'rules')['digest']


def test_legacy_context_requires_matching_original_routing_input_hash(tmp_path):
    dsn=tmp_path/'pcbgolf.dsn';dsn.write_text(f'(use_via "{ORIGINAL}")')
    record=dict(candidate=str(tmp_path),constraint_scope='rules',routing_scope=dict(execution=dict(coverage=dict(dsn_sha256=hashlib.sha256(dsn.read_bytes()).hexdigest()))))
    assert record_context(record)['provenance']=='inferred_from_frozen_hashed_dsn'
    dsn.write_text(f'(use_via "{ORIGINAL}" "{SMALL}")')
    assert record_context(record)['digest'] is None
    assert record_context({})['digest'] is None


def test_failed_pose_exclusion_is_scoped_to_effective_options():
    old=context([ORIGINAL],'rules');new=context([ORIGINAL,SMALL],'rules')
    action=dict(parent_board_sha256='parent',refs=['R123'],translation_mm=[-2,.5],rotation_deg=0,nets=['GND'],local_approach=dict(after_mm=1),realization_context_digest=old['digest'])
    failure=dict(attempt='old-failure',action=action,realization_context=old,split_groups=[],native_delta=1,collision_removals=[])
    args=(dict(removed=[],native_errors_remaining=0),dict(split_groups=[]),[failure])
    assert not score_preview(action,*args)['eligible']
    assert score_preview({**action,'realization_context_digest':new['digest']},*args)['eligible']
