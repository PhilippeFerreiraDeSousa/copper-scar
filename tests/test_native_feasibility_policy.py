from copper_scar.tools.copperhead.stage1 import choose_action

def state(**changes):
    result=dict(invariants_ok=True,counts={},unconnected=10,violations=[])
    result.update(changes)
    return result

def feedback(action,improved,scope='scope'):
    return dict(attempt='prior',action=action,diagnostic_improved=improved,scope=scope)

def test_broken_reference_prevents_routing():
    assert choose_action(state(invariants_ok=False),[],'scope')['kind']=='stop'

def test_short_prevents_blind_routing():
    assert choose_action(state(counts={'shorting_items':1}),[],'scope')['kind']=='stop'

def test_foreign_stagnation_does_not_stop_current_scope():
    old=[feedback('route_continue',False,'other')]*2
    assert choose_action(state(),old,'scope')['kind']=='route_continue'

def test_ground_regression_does_not_trigger_same_escape_again():
    result=state(violations=[dict(type='unconnected_items',items=[dict(description='Pad [GND]')])]*8)
    history=[feedback('route_continue',True)]*2
    assert choose_action(result,history,'scope')['kind']=='ground_escape'
    history.append(feedback('ground_escape',False))
    assert choose_action(result,history,'scope')['kind']=='route_continue'

def test_two_measured_stagnant_routes_need_new_proposal():
    assert choose_action(state(),[feedback('route_continue',False)]*2,'scope')['kind']=='stop'

def test_backend_proposal_requires_current_missing_net_and_valid_reference():
    import pytest
    from copper_scar.tools.copperhead.stage1 import validate_proposal
    p=dict(kind='krt_reconnect',net='BTN',reason='measured plateau',hypothesis='alternate route',feedback_used=['prior'])
    current=state(errors=0,violations=[dict(type='unconnected_items',items=[dict(description='Pad [BTN]')])])
    assert validate_proposal(p,current)==p
    with pytest.raises(ValueError):validate_proposal(dict(p,net='absent'),current)
    with pytest.raises(ValueError):validate_proposal(p,dict(current,invariants_ok=False))

def test_identical_design_cannot_promote_on_airwire_measurement_variation():
    from copper_scar.tools.copperhead.stage1 import classify_action
    from copper_scar.tools.copperhead.metrics import measure
    c=measure(dict(violations=[],schematic_parity=[],unconnected_items=[]))
    c['missing_endpoint_pairs']=2;c['total_missing_endpoint_distance_mm']=5
    before=dict(design_sha256='same',invariants_ok=True,search_cost=c)
    after=dict(before,search_cost=dict(c,total_missing_endpoint_distance_mm=4))
    assert classify_action(before,after)==(True,True,False,'measurement_variation')
    assert classify_action(before,dict(after,design_sha256='changed'))==(False,True,True,'improvement')

def test_placement_change_resets_stagnation_and_tried_nets():
    old=[dict(feedback('route_continue',False),geometry_scope='old')]*2
    old.append(dict(feedback('krt_reconnect',False),geometry_scope='old',action_parameters={'net':'BTN'}))
    result=state(geometry_scope='new',violations=[dict(type='unconnected_items',items=[dict(description='Pad [BTN]')])])
    assert choose_action(result,old,'scope')['net']=='BTN'
    assert choose_action(state(geometry_scope='new'),old[:2],'scope')['kind']=='route_continue'

def test_group_proposal_requires_members_anchors_and_current_open_net():
    import pytest
    from copper_scar.tools.copperhead.stage1 import validate_proposal
    current=state(errors=0,violations=[dict(type='unconnected_items',items=[dict(description='Pad [CMD]')])])
    p=dict(kind='placement_group',refs=['R1','R2'],anchors=['U1','J1'],nets=['CMD','DATA'],net='CMD',reason='connected bus',hypothesis='shorter detour',feedback_used=['prior'])
    assert validate_proposal(p,current)==p
    with pytest.raises(ValueError):validate_proposal(dict(p,refs=['R1']),current)
    with pytest.raises(ValueError):validate_proposal(dict(p,anchors=[]),current)
