import json
from scripts.copperhead_krt_rules import project_audit


def test_producer_hole_floor_lowering_is_recorded_as_contract_violation():
    original=json.dumps({'board':{'rules':{'hole':0.25,'clearance':0.2}}}).encode()
    producer=json.dumps({'board':{'rules':{'hole':0.2,'clearance':0.2}}}).encode()
    audit=project_audit(original,producer)
    assert audit['producer_rule_preservation']=='violated'
    assert audit['semantic_changes']==[{'path':'board.rules.hole','before':0.25,'after':0.2}]


def test_json_reformatting_is_distinct_from_rule_change():
    audit=project_audit(b'{"clearance":0.2}',b'{\n "clearance": 0.2\n}')
    assert audit['producer_rule_preservation']=='verified'
    assert audit['semantic_changes']==[]
    assert audit['original_sha256']!=audit['producer_sha256']
