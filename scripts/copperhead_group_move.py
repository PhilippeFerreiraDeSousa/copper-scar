"""Bounded topology-defined passive bundle placement; retained unrelated copper."""
import argparse,json,math,hashlib
from pathlib import Path
import pcbnew as p
ap=argparse.ArgumentParser();ap.add_argument('candidate',type=Path);ap.add_argument('--proposal',type=Path,required=True);a=ap.parse_args()
proposal=json.loads(a.proposal.read_text());refs=proposal['refs'];anchors=set(proposal['anchors'])
bp=a.candidate/'pcbgolf.kicad_pcb';source_hash=hashlib.sha256(bp.read_bytes()).hexdigest()
b=p.LoadBoard(str(bp));fs={f.GetReference():f for f in b.GetFootprints()};members=[fs[r] for r in refs]
assert len(refs)==len(set(refs)) and len(refs)>1
assert all(r.startswith('R') and len(list(fs[r].Pads()))==2 for r in refs),'This producer supports series-resistor bundles'
mm=p.ToMM
pt=lambda v:(mm(v.x),mm(v.y))
def setpose(f,xy,angle):f.SetPosition(p.VECTOR2I(p.FromMM(xy[0]),p.FromMM(xy[1])));f.SetOrientationDegrees(angle)
def box(q):
 z=q.GetBoundingBox(False,False) if isinstance(q,p.FOOTPRINT) else q.GetBoundingBox()
 return mm(z.GetX()),mm(z.GetY()),mm(z.GetRight()),mm(z.GetBottom())
def overlap(q,v,m=.3):return q[0]<v[2]+m and q[2]>v[0]-m and q[1]<v[3]+m and q[3]>v[1]-m
def dist(x,u,v):
 dx=v[0]-u[0];dy=v[1]-u[1];d=dx*dx+dy*dy;t=max(0,min(1,((x[0]-u[0])*dx+(x[1]-u[1])*dy)/d)) if d else 0
 return math.hypot(x[0]-u[0]-t*dx,x[1]-u[1]-t*dy)
nets={q.GetNetname() for f in members for q in f.Pads()};assert not nets & {'','GND','+3V3','+5V','+12V'}
assert nets==set(proposal['nets']),'Proposal must state exact touched nets'
old={r:(pt(fs[r].GetPosition()),fs[r].GetOrientationDegrees()) for r in refs}
fixed={r:(pt(f.GetPosition()),f.GetOrientationDegrees()) for r,f in fs.items() if r not in refs}
targets={n:[pt(q.GetPosition()) for r,f in fs.items() if r in anchors for q in f.Pads() if q.GetNetname()==n] for n in nets}
assert all(targets.values()),'Every series-terminal net must reach a declared interface anchor'
retained=[(pt(t.GetStart()),pt(t.GetEnd()),mm(t.GetWidth(p.F_Cu) if isinstance(t,p.PCB_VIA) else t.GetWidth())/2) for t in b.GetTracks() if t.GetNetname() not in nets and t.IsOnLayer(p.F_Cu)]
def cost(f):return sum(min(math.dist(pt(q.GetPosition()),t) for t in targets[q.GetNetname()]) for q in f.Pads())
def valid(f):
 z=box(f)
 if z[0]<101 or z[1]<51 or z[2]>239 or z[3]>154:return False
 if any(overlap(z,v) for v in active_obstacles):return False
 for q in f.Pads():
  qb=box(q);radius=math.hypot(qb[2]-qb[0],qb[3]-qb[1])/2
  if any(dist(pt(q.GetPosition()),u,v)<radius+w+.21 for u,v,w in retained):return False
 return True
before=sum(cost(f) for f in members);trials=[]
# Two deterministic packing orders expose order sensitivity without a new controller.
for order in [refs,list(reversed(refs))]:
 for r,(xy,ang) in old.items():setpose(fs[r],xy,ang)
 counts={}
 for r in order:
  f=fs[r];active_obstacles=[box(x) for key,x in fs.items() if key!=r];positions={tuple(old[r][0])}
  for q in f.Pads():
   for x,y in targets[q.GetNetname()]:positions.update((round(x+dx*.5,2),round(y+dy*.5,2)) for dx in range(-12,13) for dy in range(-12,13))
  options=[(cost(f),old[r][0],old[r][1])]
  for xy in sorted(positions):
   for angle in [0,90,180,270]:
    setpose(f,xy,angle)
    if valid(f):options.append((cost(f),xy,angle))
  _,xy,angle=min(options);setpose(f,xy,angle);counts[r]=len(options)-1
 poses={r:(pt(fs[r].GetPosition()),fs[r].GetOrientationDegrees()) for r in refs}
 trials.append(dict(order=order,cost=sum(cost(f) for f in members),poses=poses,screened_options=counts))
best=min(trials,key=lambda t:t['cost']);assert best['cost']<before,'No bundle wire-demand improvement'
for r,(xy,ang) in best['poses'].items():setpose(fs[r],xy,ang)
assert all((pt(fs[r].GetPosition()),fs[r].GetOrientationDegrees())==v for r,v in fixed.items())
ripped=0
for t in list(b.GetTracks()):
 if t.GetNetname() in nets:b.Delete(t);ripped+=1
p.SaveBoard(str(bp),b)
result=dict(schema_version=1,outer_kind='placement_group',group_members=refs,anchors=sorted(anchors),input_board_sha256=source_hash,moves=[dict(ref=r,from_mm=old[r][0],to_mm=best['poses'][r][0],from_degrees=old[r][1],to_degrees=best['poses'][r][1]) for r in refs if old[r]!=best['poses'][r]],affected_nets=sorted(nets),removed_copper_items=ripped,estimated_interface_distance_before_mm=before,estimated_interface_distance_after_mm=best['cost'],packing_trials=trials,fixed_requirements='Original parts, pad assignments and design rules; unaffected poses/copper, outline and layers retained',search_guards='0.3 mm body spacing, 0.21 mm retained-copper pad screen, 0.5 mm grid within 6 mm of declared interface pads; original member pose allowed',qualification='Experimental placement proxy. Fresh native mid-placement and after-route checks required; no electrical or manufacturing qualification')
(a.candidate/'placement-search.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
