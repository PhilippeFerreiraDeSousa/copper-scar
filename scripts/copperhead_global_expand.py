"""Expand the full board by translating explicit schematic circuit groups rigidly."""
import argparse,json,math,collections,hashlib
from pathlib import Path
import pcbnew as p
ap=argparse.ArgumentParser();ap.add_argument('candidate',type=Path);ap.add_argument('--proposal',type=Path,required=True);a=ap.parse_args();cfg=json.loads(a.proposal.read_text());board=a.candidate/'pcbgolf.kicad_pcb';b=p.LoadBoard(str(board));fs={f.GetReference():f for f in b.GetFootprints()};groups=cfg['groups'];flat=[r for rs in groups.values() for r in rs];assert len(flat)==len(set(flat)) and set(flat)==set(fs),'Every footprint must belong to exactly one declared group'
mm=p.ToMM;pt=lambda v:(mm(v.x),mm(v.y));old={r:(pt(f.GetPosition()),f.GetOrientationDegrees()) for r,f in fs.items()};owner={r:g for g,rs in groups.items() for r in rs}
initial_net_groups=collections.defaultdict(set)
for r,f in fs.items():
 for q in f.Pads():
  if q.GetNetname():initial_net_groups[q.GetNetname()].add(owner[r])
group_copper=collections.defaultdict(list)
for t in b.GetTracks():
 gs=initial_net_groups.get(t.GetNetname(),set())
 if len(gs)==1:group_copper[next(iter(gs))].append(t)
def bounds(rs):
 zs=[fs[r].GetBoundingBox(False,False) for r in rs]+[t.GetBoundingBox() for t in group_copper[owner[rs[0]]]];return min(mm(z.GetX()) for z in zs),min(mm(z.GetY()) for z in zs),max(mm(z.GetRight()) for z in zs),max(mm(z.GetBottom()) for z in zs)
# Shelf-pack rigid groups with 20 mm body-envelope gaps; no scaling or rotation.
x0,y0=110,60;gap=20;x,y=x0,y0;rowheight=0;extentx=x0;extenty=y0
transforms={};group_records=[]
for i,(g,rs) in enumerate(groups.items()):
 z=bounds(rs);width=z[2]-z[0];height=z[3]-z[1]
 if i and i%3==0:x=x0;y+=rowheight+gap;rowheight=0
 delta=(x-z[0],y-z[1]);transforms[g]=delta;group_records.append(dict(group=g,refs=rs,old_bounds_mm=z,translation_mm=delta,new_bounds_mm=[x,y,x+width,y+height]))
 for r in rs:
  xy,angle=old[r];f=fs[r];f.SetPosition(p.VECTOR2I(p.FromMM(xy[0]+delta[0]),p.FromMM(xy[1]+delta[1])))
 x+=width+gap;rowheight=max(rowheight,height);extentx=max(extentx,x-gap);extenty=max(extenty,y+height)
net_groups=collections.defaultdict(set)
for r,f in fs.items():
 for q in f.Pads():
  if q.GetNetname():net_groups[q.GetNetname()].add(owner[r])
retained=collections.Counter();removed=collections.Counter()
for t in list(b.GetTracks()):
 n=t.GetNetname();gs=net_groups.get(n,set())
 if len(gs)==1:
  g=next(iter(gs));dx,dy=transforms[g];t.Move(p.VECTOR2I(p.FromMM(dx),p.FromMM(dy)));retained[n]+=1
 else:removed[n]+=1;b.Delete(t)
# Keep original plane nets, layers and rules, but resize/refill their polygon.
outline=[100,50,math.ceil(extentx+10),math.ceil(extenty+10)];plane_records=[]
for z in b.Zones():
 before=dict(net=z.GetNetname(),layers=[b.GetLayerName(l) for l in z.GetLayerSet().Seq()]);poly=z.Outline();poly.RemoveAllContours();poly.NewOutline()
 for xy in [(outline[0]+.5,outline[1]+.5),(outline[2]-.5,outline[1]+.5),(outline[2]-.5,outline[3]-.5),(outline[0]+.5,outline[3]-.5)]:poly.Append(p.FromMM(xy[0]),p.FromMM(xy[1]))
 plane_records.append(before)
for d in list(b.GetDrawings()):
 if d.GetLayer()==p.Edge_Cuts:b.Delete(d)
for u,v in zip([(outline[0],outline[1]),(outline[2],outline[1]),(outline[2],outline[3]),(outline[0],outline[3])],[(outline[2],outline[1]),(outline[2],outline[3]),(outline[0],outline[3]),(outline[0],outline[1])]):
 d=p.PCB_SHAPE();d.SetShape(p.SHAPE_T_SEGMENT);d.SetLayer(p.Edge_Cuts);d.SetWidth(p.FromMM(.05));d.SetStart(p.VECTOR2I(p.FromMM(u[0]),p.FromMM(u[1])));d.SetEnd(p.VECTOR2I(p.FromMM(v[0]),p.FromMM(v[1])));b.Add(d)
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(board),b)
moves=[dict(ref=r,from_mm=old[r][0],to_mm=pt(fs[r].GetPosition()),from_degrees=old[r][1],to_degrees=fs[r].GetOrientationDegrees()) for r in sorted(fs) if old[r][0]!=pt(fs[r].GetPosition())];assert len(moves)>200
result=dict(schema_version=1,outer_kind='global_expansion',group_members=flat,groups=group_records,moves=moves,affected_nets=sorted(net_groups),group_body_gap_mm=gap,outline_before_mm=[100,50,240,155],outline_after_mm=outline,copper_layers=b.GetCopperLayerCount(),retained_internal_copper_items=sum(retained.values()),removed_boundary_copper_items=sum(removed.values()),retained_by_net=dict(retained),removed_by_net=dict(removed),plane_intent=plane_records,qualification='All footprint sizes/orientations and within-group offsets preserved. Explicit group manifest is a conservative schematic-based circuit grouping, not assembly or electrical qualification. Cross-group copper removed because rigidly translating it would disconnect endpoints; internal-net copper translated with its group. Original plane rules/layers retained and polygons refilled.')
(a.candidate/'placement-search.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:result[k] for k in ['outline_after_mm','copper_layers','retained_internal_copper_items','removed_boundary_copper_items']}))
