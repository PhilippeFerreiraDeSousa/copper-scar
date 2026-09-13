"""Three explicit CMD-branch placement controls, with local copper detachment."""
import argparse,json,math
from pathlib import Path
import pcbnew as p
ap=argparse.ArgumentParser();ap.add_argument('candidate',type=Path);ap.add_argument('--proposal',type=Path,required=True);a=ap.parse_args();cfg=json.loads(a.proposal.read_text())
b=p.LoadBoard(str(a.candidate/'pcbgolf.kicad_pcb'));fs={f.GetReference():f for f in b.GetFootprints()};refs=cfg['refs'];assert refs==['R37','R42']
mm=p.ToMM;pt=lambda x:(mm(x.x),mm(x.y))
def pose(f):return pt(f.GetPosition()),f.GetOrientationDegrees()
def setpose(f,xy,angle):f.SetPosition(p.VECTOR2I(p.FromMM(xy[0]),p.FromMM(xy[1])));f.SetOrientationDegrees(angle)
def box(q):
 z=q.GetBoundingBox(False,False) if isinstance(q,p.FOOTPRINT) else q.GetBoundingBox();return mm(z.GetX()),mm(z.GetY()),mm(z.GetRight()),mm(z.GetBottom())
def overlap(x,y,m=.3):return x[0]<y[2]+m and x[2]>y[0]-m and x[1]<y[3]+m and x[3]>y[1]-m
def distance(x,u,v):
 dx=v[0]-u[0];dy=v[1]-u[1];z=dx*dx+dy*dy;t=max(0,min(1,((x[0]-u[0])*dx+(x[1]-u[1])*dy)/z)) if z else 0
 return math.hypot(x[0]-u[0]-t*dx,x[1]-u[1]-t*dy)
retained=[(t.GetNetname(),pt(t.GetStart()),pt(t.GetEnd()),mm(t.GetWidth(p.F_Cu) if isinstance(t,p.PCB_VIA) else t.GetWidth())/2) for t in b.GetTracks() if t.IsOnLayer(p.F_Cu)]
def pad_screen(f):
 for q in f.Pads():
  z=box(q);radius=math.hypot(z[2]-z[0],z[3]-z[1])/2
  if any(n!=q.GetNetname() and distance(pt(q.GetPosition()),u,v)<radius+w+.21 for n,u,v,w in retained):return False
 return True
old={r:pose(f) for r,f in fs.items()};oldpads=[(q.GetNetname(),box(q),pt(q.GetPosition())) for r in refs for q in fs[r].Pads()];nets={n for n,_,_ in oldpads};assert nets==set(cfg['nets'])
variant=cfg['variant'];options_count=None
if variant=='space':
 for r in refs:
  xy,ang=old[r];setpose(fs[r],(xy[0]+100,xy[1]),ang)
 for d in b.GetDrawings():
  if d.GetLayer()!=p.Edge_Cuts:continue
  for getter,setter in [(d.GetStart,d.SetStart),(d.GetEnd,d.SetEnd)]:
   v=getter()
   if abs(mm(v.x)-240)<1e-5:setter(p.VECTOR2I(p.FromMM(284),v.y))
elif variant=='relative':
 f=fs['R37'];anchor=next(q for q in fs['R42'].Pads() if q.GetNetname()=='Net-(J2-CMD)');ax,ay=pt(anchor.GetPosition());obstacles=[box(x) for r,x in fs.items() if r!='R37'];options=[]
 for dx in range(-24,25):
  for dy in range(-24,25):
   xy=(ax+dx*.5,ay+dy*.5)
   for angle in [0,90,180,270]:
    setpose(f,xy,angle);z=box(f)
    if z[0]<101 or z[1]<51 or z[2]>239 or z[3]>154 or any(overlap(z,v) for v in obstacles):continue
    if not pad_screen(f):continue
    q=next(q for q in f.Pads() if q.GetNetname()=='Net-(J2-CMD)');options.append((math.dist(pt(q.GetPosition()),(ax,ay)),xy,angle))
 assert options,'No body-screened local position';options_count=len(options);_,xy,ang=min(options);setpose(f,xy,ang)
elif variant=='pad_access':
 xy,ang=old['R37'];setpose(fs['R37'],xy,ang+90)
else:raise ValueError('Unknown variant')
moved=[r for r in refs if pose(fs[r])!=old[r]];assert moved
# Detach only copper touching an OLD pad of an actually moved member.
oldpads=[]
for r in moved:
 new=pose(fs[r]);setpose(fs[r],*old[r]);oldpads.extend((q.GetNetname(),box(q)) for q in fs[r].Pads());setpose(fs[r],*new)
def inside(x,z):return z[0]-.001<=x[0]<=z[2]+.001 and z[1]-.001<=x[1]<=z[3]+.001
removed=[]
for t in list(b.GetTracks()):
 if any(t.GetNetname()==n and (inside(pt(t.GetStart()),z) or inside(pt(t.GetEnd()),z)) for n,z in oldpads):
  removed.append(dict(net=t.GetNetname(),uuid=t.m_Uuid.AsString(),start_mm=pt(t.GetStart()),end_mm=pt(t.GetEnd())));b.Delete(t)
assert all(pose(fs[r])==v for r,v in old.items() if r not in refs)
p.SaveBoard(str(a.candidate/'pcbgolf.kicad_pcb'),b)
result=dict(schema_version=1,variant=variant,group_members=refs,moves=[dict(ref=r,from_mm=old[r][0],to_mm=pose(fs[r])[0],from_degrees=old[r][1],to_degrees=pose(fs[r])[1]) for r in moved],affected_nets=sorted(nets),removed_copper_items=len(removed),removed_copper=removed,outline_before_mm=[100,50,240,155],outline_after_mm=[100,50,284 if variant=='space' else 240,155],screened_options=options_count,qualification='Explicit hypothesis control; native placement check must pass before routing. Only old-pad incident copper detached; unrelated routes retained. Physical validity and routing benefit are not inferred from spacing.')
(a.candidate/'placement-search.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
