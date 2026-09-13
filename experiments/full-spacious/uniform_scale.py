"""True uniform scaling of anchor positions and outline, never footprint geometry."""
import argparse,hashlib,json
from fractions import Fraction
from pathlib import Path
import pcbnew as p
ap=argparse.ArgumentParser();ap.add_argument('folder',type=Path);ap.add_argument('--scale',required=True);a=ap.parse_args()
folder=a.folder.resolve();board=folder/'pcbgolf.kicad_pcb';project=folder/'pcbgolf.kicad_pro';pro=project.read_bytes();source_hash=hashlib.sha256(board.read_bytes()).hexdigest()
b=p.LoadBoard(str(board));assert len(list(b.GetFootprints()))==245 and not list(b.GetTracks()) and not list(b.Zones())
s=Fraction(a.scale);assert 1<s<=2
# Fixed center of the prior ring floorplan's exact (100,50)-(240,155) mm outline.
c=(170000000,102500000)
def transform(xy):return tuple(round(Fraction(c[i])+s*(xy[i]-c[i])) for i in [0,1])
def geometry(fp):
 pos=fp.GetPosition()
 return dict(angle=fp.GetOrientationDegrees(),side=fp.GetLayer(),pads=sorted((q.m_Uuid.AsString(),q.GetNumber(),q.GetNetname(),q.GetPosition().x-pos.x,q.GetPosition().y-pos.y,q.GetSize().x,q.GetSize().y,q.GetDrillSize().x,q.GetDrillSize().y,str(q.GetShape()),q.GetLayerSet().FmtHex()) for q in fp.Pads()))
def envelope(fp):
 z=fp.GetBoundingBox(False,False);return [z.GetX(),z.GetY(),z.GetRight(),z.GetBottom()]
rows=[]
for fp in b.GetFootprints():
 old=(fp.GetPosition().x,fp.GetPosition().y);expected=transform(old);g=geometry(fp);box=envelope(fp)
 fp.SetPosition(p.VECTOR2I(*expected));new=(fp.GetPosition().x,fp.GetPosition().y)
 assert geometry(fp)==g and new==expected
 residual=[float(Fraction(new[i])-(Fraction(c[i])+s*(old[i]-c[i]))) for i in [0,1]];assert max(map(abs,residual))<=.5
 rows.append(dict(ref=fp.GetReference(),uuid=fp.m_Uuid.AsString(),before_nm=old,after_nm=new,angle_degrees=fp.GetOrientationDegrees(),side=fp.GetLayer(),transform_residual_nm=residual,before_envelope_nm=box,after_envelope_nm=envelope(fp)))
edges=list(d for d in b.GetDrawings() if d.GetLayer()==p.Edge_Cuts);assert len(edges)==4
for d in edges:
 for get,setter in [(d.GetStart,d.SetStart),(d.GetEnd,d.SetEnd)]:
  v=get();setter(p.VECTOR2I(*transform((v.x,v.y))))
p.SaveBoard(str(board),b);project.write_bytes(pro)
result=dict(primitive='uniform_position_and_outline_scale',source_board_sha256=source_hash,scale=str(s),center_nm=c,formula='p_next = center + scale * (p - center)',rounding='nearest integer nanometer, ties to even',maximum_transform_residual_nm=max(abs(x) for r in rows for x in r['transform_residual_nm']),before_outline_mm=[100,50,240,155],after_outline_mm=[v/1e6 for xy in [transform((100000000,50000000)),transform((240000000,155000000))] for v in xy],poses=rows,part_count=len(rows),source_project_sha256=hashlib.sha256(pro).hexdigest(),physical_footprint_geometry_preserved=True,rotations_and_sides_preserved=True,board_sha256=hashlib.sha256(board.read_bytes()).hexdigest(),qualification='Only component anchor positions and four outline corners scaled by one scalar about one fixed center; no regrouping, rotation, footprint/model scaling, copper, vias or rule change. Native parity and physical-floor checks follow.')
(folder/'uniform-scale.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='poses'}))
