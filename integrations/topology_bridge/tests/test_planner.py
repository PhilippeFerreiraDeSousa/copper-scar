import copy
import sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from planner import propose, fixture_parent, render

def test_changes_sites_only_on_affected_net_and_preserves_parent():
    parent=fixture_parent();parent['topology']=propose(parent,{'TP4':[8,6]},offsets=(2,))[0]['topology'];before=copy.deepcopy(parent)
    candidates=propose(parent,{'TP4':[10,8]})
    assert parent==before
    assert candidates[0]['topology']['CROSS_A']!=candidates[1]['topology']['CROSS_A']
    for c in candidates:
        for n in ('HOLD','CROSS_B','CROSS_C'): assert c['topology'][n]==parent['topology'][n]
        assert c['affected_nets']==['CROSS_A']
        assert c['topology']['CROSS_A']['vias']['cross_a_escape_b']['xy'][1]==8

def test_unknown_or_partial_scope_rejected():
    p=fixture_parent();p['scope']='partial-real-board'
    with pytest.raises(ValueError,match='external net'): propose(p,{'TP4':[10,8]})
    p=fixture_parent();p['nets']['CROSS_A']['ports'].append('EXTERNAL.p')
    with pytest.raises(ValueError,match='complete'): propose(p,{'TP4':[10,8]})

def test_barrier_and_layer_gate():
    with pytest.raises(ValueError,match='envelope'): propose(fixture_parent(),{'TP4':[2,8]})
    with pytest.raises(ValueError,match='layer'): propose(fixture_parent(),{'TP4':[10,8]},lower_layers=(2,))
