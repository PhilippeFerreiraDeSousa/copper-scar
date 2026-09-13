"""Search a passive's position and rotation against real pads and retained copper."""
import argparse,json,math
from pathlib import Path
import pcbnew as p
ap=argparse.ArgumentParser();ap.add_argument('candidate',type=Path);ap.add_argument('--ref',required=True);a=ap.parse_args()
b=p.LoadBoard(str(a.candidate/'pcbgolf.kicad_pcb'));fs={f.GetReference():f for f in b.GetFootprints()};f=fs[a.ref]
assert a.ref.startswith('R') and len(list(f.Pads()))==2,'Initial search supports two-pad resistors'
mm=lambda v:p.ToMM(v);pt=lambda q:(mm(q.x),mm(q.y))
def box(q):
 z=q.GetBoundingBox(False,False) if isinstance(q,p.FOOTPRINT) else q.GetBoundingBox()
 return (mm(z.GetX()),mm(z.GetY()),mm(z.GetRight()),mm(z.GetBottom()))
def overlap(q,v,margin):return q[0]<v[2]+margin and q[2]>v[0]-margin and q[1]<v[3]+margin and q[3]>v[1]-margin
def dist(x,u,v):
 dx=v[0]-u[0];dy=v[1]-u[1];d=dx*dx+dy*dy;t=max(0,min(1,((x[0]-u[0])*dx+(x[1]-u[1])*dy)/d)) if d else 0
 return math.hypot(x[0]-u[0]-t*dx,x[1]-u[1]-t*dy)
nets={q.GetNetname() for q in f.Pads()};assert not nets & {'GND','+3V3','+5V','+12V'},'Global-rail rip-up requires a separate group proposal'
targets={n:[q for x in fs.values() if x is not f for q in x.Pads() if q.GetNetname()==n] for n in nets};assert all(targets.values())
retained=[(pt(t.GetStart()),pt(t.GetEnd()),mm(t.GetWidth(p.F_Cu) if isinstance(t,p.PCB_VIA) else t.GetWidth())/2) for t in b.GetTracks() if t.GetNetname() not in nets and t.IsOnLayer(p.F_Cu)];obstacles=[box(x) for x in fs.values() if x is not f]
old=pt(f.GetPosition());oldangle=f.GetOrientationDegrees()
def cost():return sum(min(math.dist(pt(q.GetPosition()),pt(t.GetPosition())) for t in targets[q.GetNetname()]) for q in f.Pads())
oldcost=cost();options=[]
# Both locations and rotations vary. Electrical pin numbering never swaps.
centers=[pt(q.GetPosition()) for qs in targets.values() for q in qs]
positions=set((round(x+dx*.5,2),round(y+dy*.5,2)) for x,y in centers for dx in range(-12,13) for dy in range(-12,13))
for xy in sorted(positions):
 if math.dist(xy,old)<.5:continue
 f.SetPosition(p.VECTOR2I(p.FromMM(xy[0]),p.FromMM(xy[1])))
 for angle in [0,90,180,270]:
  f.SetOrientationDegrees(angle);z=box(f)
  if z[0]<101 or z[1]<51 or z[2]>239 or z[3]>154 or any(overlap(z,v,.3) for v in obstacles):continue
  valid=True
  for q in f.Pads():
   qb=box(q);radius=math.hypot(qb[2]-qb[0],qb[3]-qb[1])/2
   for u,v,tr in retained:
    if dist(pt(q.GetPosition()),u,v)<radius+tr+.21:valid=False;break
   if not valid:break
  if valid:options.append((cost(),xy,angle))
assert options,'No screened relocation found'
best,xy,angle=min(options);assert best<oldcost,'No estimated wire-demand improvement'
f.SetPosition(p.VECTOR2I(p.FromMM(xy[0]),p.FromMM(xy[1])));f.SetOrientationDegrees(angle)
ripped=0
for t in list(b.GetTracks()):
 if t.GetNetname() in nets:b.Delete(t);ripped+=1
p.SaveBoard(str(a.candidate/'pcbgolf.kicad_pcb'),b)
r=dict(moves=[dict(ref=a.ref,from_mm=old,to_mm=xy,from_degrees=oldangle,to_degrees=angle)],affected_nets=sorted(nets),removed_copper_items=ripped,screened_options=len(options),estimated_nearest_pad_distance_before_mm=oldcost,estimated_nearest_pad_distance_after_mm=best,fixed_requirements='Original circuit, pad identities, design rules, outline and layer stack retained',search_guards='0.3 mm body gap and 0.21 mm retained-copper pad screening; these are generation guards, not rule changes',qualification='Distance is a placement search proxy, not feasibility or electrical qualification')
(a.candidate/'placement-search.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
