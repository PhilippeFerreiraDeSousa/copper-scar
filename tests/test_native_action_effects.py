from copper_scar.tools.copperhead.effects import compare

def board(path,end='1.0',net='A'):
    path.write_text(f'(kicad_pcb (net 1 "{net}") (segment (start 0 0) (end {end} 0) (width 0.2) (layer "F.Cu") (net 1) (uuid "anything")))')

def test_serialization_precision_is_not_copper_change(tmp_path):
    a=tmp_path/'a';b=tmp_path/'b';board(a);board(b,end='1')
    assert compare(a,b,['A'])['copper_changes']==[]

def test_actual_unselected_net_change_is_reported(tmp_path):
    a=tmp_path/'a';b=tmp_path/'b';board(a,net='B');board(b,end='2',net='B')
    result=compare(a,b,['A']);assert result['changed_unselected_nets']==['B'];assert result['copper_changes'][0]['removed']==1

def test_geometry_scope_ignores_copper_but_tracks_placement_and_layers(tmp_path):
    from copper_scar.tools.copperhead.effects import geometry_scope
    a=tmp_path/'a';b=tmp_path/'b'
    base='(kicad_pcb (layers (0 "F.Cu" signal)) (footprint "R" (at 1 2 0) (property "Reference" "R1")) %s)'
    a.write_text(base%'');b.write_text(base%'(segment (start 0 0) (end 2 0) (net 1))')
    assert geometry_scope(a)==geometry_scope(b)
    b.write_text((base%'').replace('(at 1 2 0)','(at 1 2 90)'))
    assert geometry_scope(a)!=geometry_scope(b)
    b.write_text((base%'').replace('(0 "F.Cu" signal)','(0 "F.Cu" signal) (31 "B.Cu" signal)'))
    assert geometry_scope(a)!=geometry_scope(b)
