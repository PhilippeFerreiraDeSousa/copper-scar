from scripts.copperhead_route_evidence import evidence


def test_exported_but_unstarted_route_has_no_fabricated_execution(tmp_path):
    (tmp_path/'pcbgolf.dsn').write_text('(pcb test (structure (layer F.Cu)) (network (net GND (pins R1-1))) (placement (component R (place R1 0 0 front 0))))')
    result=evidence(tmp_path)
    assert result['exported_nets']==1
    assert result['exported_assigned_pins']==1
    assert not result['autoroute_started']
    assert result['termination']=='not_started'
