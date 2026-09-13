"""Compare exported net/layer fixed polygons to declared transferred conductors."""
import json
from pathlib import Path
import sys
import sexpdata as sx
from shapely.geometry import LineString, Polygon, box
from shapely.ops import unary_union
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'placement_bridge'))
from verify_incremental_fixture import children,one
root=Path(sys.argv[1]);m=json.loads((root/'transfer-manifest.json').read_text());dx=m['frame']['dx'];dy=m['frame']['dy']
b=sx.loads(next((root/'01-transferred/export').glob('*.kicad_pcb')).read_text());nets={int(n[1]):str(n[2]) for n in children(b,'net')}
expected={};actual={}
for r in m['segments']:
    expected.setdefault((r['net'],r['layer']),[]).append(LineString([r['start'],r['end']]).buffer(r['width']/2,quad_segs=64))
expected.setdefault(('HOLD',1),[]).append(box(*m['added_plane']['bounds']))
for g in children(b,'gr_poly'):
    layer=str(one(g,'layer')[1])
    if layer not in ('F.Cu','B.Cu'):continue
    net=nets[int(one(g,'net')[1])];pts=[[float(p[1])-dx,dy-float(p[2])] for p in one(g,'pts')[1:]]
    actual.setdefault((net,0 if layer=='F.Cu' else 1),[]).append(Polygon(pts))
assert actual.keys()==expected.keys()
rows=[]
for key in sorted(expected):
    e=unary_union(expected[key]);a=unary_union(actual[key]);distance=e.hausdorff_distance(a);area=e.symmetric_difference(a).area
    assert distance<1e-8 and area<1e-7
    rows.append({'net':key[0],'layer':key[1],'hausdorff_mm':distance,'symmetric_difference_mm2':area})
result={'fixed_geometry_transfer_passed':True,'export_primitive':'net-bearing gr_poly, not mutable Route/segment','fixed_plane_exact':True,'plane_refill_or_thermal_equivalence_tested':False,'arc_transfer_tested':False,'input_straight_segments':len(m['segments']),'retained_through_vias':len(m['vias']),'added_plane_vias':1,'maximum_round_cap_sagitta_mm':m['maximum_round_cap_sagitta_mm'],'rows':rows}
(root/'geometry-result.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
