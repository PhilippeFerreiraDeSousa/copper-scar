from copper_scar.tools.copperhead.dsn_contacts import partition
from copper_scar.tools.copperhead.routing_options import context,ORIGINAL,SMALL

def test_via_contact_partitions_existing_wire_without_changing_other_bytes():
    original='(pcb test\n    (wire (path F.Cu 200 0 0 1000 0)(net CAN2_H)(type route))\n    (via "through" 400 0 (net CAN2_H))\n (rule (clearance 200))\n)\n'
    result,proof=partition(original,['CAN2_H'])
    assert len(proof['changes'])==1
    assert '(path F.Cu 200 0 0 400 0)' in result
    assert '(path F.Cu 200 400 0 1000 0)' in result
    assert '    (via "through" 400 0 (net CAN2_H))\n (rule (clearance 200))\n' in result
    assert partition(result,['CAN2_H'])[0]==result

def test_multiline_wire_and_exact_decimal_t_junction():
    original='    (wire (path F.Cu 200\n 0 59.9 1000 59.9)(net N)(type route))\n    (wire (path F.Cu 200 400 59.9 400 70)(net N)(type route))\n'
    result,proof=partition(original,['N'])
    assert len(proof['changes'])==1
    assert '(path F.Cu 200 0 59.9 400 59.9)' in result
    assert '(path F.Cu 200 400 59.9 1000 59.9)' in result
    assert original.splitlines()[-1] in result

def test_nearby_foreign_net_or_other_layer_endpoint_is_not_a_contact():
    original='    (wire (path F.Cu 200 0 0 1000 0)(net A)(type route))\n    (via "through" 400 0.001 (net A))\n    (via "through" 500 0 (net B))\n    (wire (path B.Cu 200 600 0 600 100)(net A)(type route))\n'
    assert partition(original,['A'])[0]==original

def test_rule_or_width_changes_are_not_part_of_normalization():
    original='    (wire (path F.Cu 500 0 0 1000 0)(net "power net")(type route))\n    (via "through" 400 0 (net "power net"))\n'
    result,proof=partition(original,['power net'])
    assert len(proof['changes'])==1 and result.count('(path F.Cu 500 ')==2
    assert result.count('(net "power net")')==3

def test_changed_contact_policy_is_a_distinct_feedback_context():
    old=context([ORIGINAL,SMALL],'scope')
    corrected=context([ORIGINAL,SMALL],'scope',{'version':'split-existing-junctions-v1','nets':['CAN2_H']})
    broader=context([ORIGINAL,SMALL],'scope',{'version':'split-existing-junctions-v1','nets':['CAN2_H','+5V']})
    assert len({old['digest'],corrected['digest'],broader['digest']})==3
    assert old['schema_version']=='effective-via-rules-v1'
