from copper_scar.tools.copperhead.metrics import measure,ordering

def report(v=(),u=()):return dict(violations=list(v),schematic_parity=[],unconnected_items=list(u))
def item(kind,severity='error',description='',x=3):return dict(type=kind,severity=severity,description=description,items=[dict(uuid='a',pos=dict(x=0,y=0)),dict(uuid='b',pos=dict(x=x,y=4))])
def test_dedup_and_distance():
 u=item('unconnected_items');m=measure(report(u=[u,u]));assert m['missing_endpoint_pairs']==1;assert m['raw_unconnected_report_count']==2;assert m['total_missing_endpoint_distance_mm']==5

def test_short_cannot_be_bought_with_connectivity():
 a=measure(report(v=[item('shorting_items')]));b=measure(report(u=[item('unconnected_items')]));assert ordering(a,True)>ordering(b,True)

def test_unknown_severity_is_not_fabricated():
 m=measure(report(v=[item('clearance',description='unparseable native description')]));assert m['clearance_severity_coverage']==dict(measured=0,findings=1)

def test_clearance_deficit_and_invariant_priority():
 m=measure(report(v=[item('clearance',description='Clearance violation ( clearance 0.2000 mm; actual 0.1626 mm)')]));assert abs(m['maximum_measured_clearance_shortfall_mm']-.0374)<1e-9;assert ordering(measure(report()),False)>ordering(m,True)
