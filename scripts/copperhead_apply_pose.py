"""Apply an explicit rigid pose proposal to native CAD with audited copper handling."""
import argparse,collections,hashlib,json
from pathlib import Path
import pcbnew as p
ap=argparse.ArgumentParser();ap.add_argument('candidate',type=Path);ap.add_argument('--proposal',type=Path,required=True);a=ap.parse_args();cfg=json.loads(a.proposal.read_text());path=a.candidate/'pcbgolf.kicad_pcb';assert hashlib.sha256(path.read_bytes()).hexdigest()==cfg['parent_board_sha256'],'Stale parent board'
b=p.LoadBoard(str(path));fs={f.GetReference():f for f in b.GetFootprints()};refs=set(cfg['refs']);assert refs and refs|set(cfg['locked_refs'])==set(fs) and not refs&set(cfg['locked_refs']);dx,dy=cfg['translation_mm'];delta=p.VECTOR2I(p.FromMM(dx),p.FromMM(dy));old={r:(p.VECTOR2I(f.GetPosition()),f.GetOrientationDegrees()) for r,f in fs.items()};net_refs=collections.defaultdict(set)
for r,f in fs.items():
 for q in f.Pads():
  if q.GetNetname():net_refs[q.GetNetname()].add(r)
rotation=cfg.get('rotation_deg',0);assert not rotation or len(refs)==1,'Rotation requires one moved member with fixed group anchors'
rotation_center=next(iter(old[r][0] for r in refs))
oldpads=[q for r in refs for q in fs[r].Pads()]
oldboxes=[(q.GetNetname(),q.GetBoundingBox(),q.GetLayerSet()) for q in oldpads]
for ref in refs:
 f=fs[ref];expected=cfg['from_poses'][ref];pos=f.GetPosition();assert abs(p.ToMM(pos.x)-expected['x_mm'])<1e-5 and abs(p.ToMM(pos.y)-expected['y_mm'])<1e-5 and abs(f.GetOrientationDegrees()-expected['angle_deg'])<1e-5,'Stale source pose';f.SetPosition(pos+delta);f.SetOrientationDegrees(expected['angle_deg']+rotation)
affected={n for n,owners in net_refs.items() if owners&refs};assert affected==set(cfg['nets']);retained=collections.Counter();removed=collections.Counter();unchanged=0;preserved_boundary_vias=[]
for t in list(b.GetTracks()):
 n=t.GetNetname();owners=net_refs.get(n,set())
 if n not in affected:unchanged+=1;continue
 if owners<=refs:
  if rotation:t.Rotate(rotation_center,p.EDA_ANGLE(rotation,p.DEGREES_T))
  t.Move(delta);retained[n]+=1
 else:
  detach=cfg.get('copper_policy')!='detach_moved_pad_incident' or any(n==net and any(t.IsOnLayer(layer) for layer in layers.Seq()) and (box.Contains(t.GetStart()) or box.Contains(t.GetEnd())) for net,box,layers in oldboxes)
  if detach and isinstance(t,p.PCB_VIA) and cfg.get('boundary_via_policy')=='preserve_existing_sites':
   preserved_boundary_vias.append(dict(uuid=t.m_Uuid.AsString(),net=n,position_mm=[p.ToMM(t.GetPosition().x),p.ToMM(t.GetPosition().y)],layers=[b.GetLayerName(t.TopLayer()),b.GetLayerName(t.BottomLayer())]));detach=False
  if detach:removed[n]+=1;b.Delete(t)
  else:unchanged+=1
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(path),b)
moves=[]
for r,f in fs.items():
 pos,angle=old[r]
 if r in refs:
  assert f.GetPosition()==pos+delta and abs((f.GetOrientationDegrees()-angle-rotation+180)%360-180)<1e-6
  moves.append({'ref':r,'uuid':f.m_Uuid.AsString(),'from_mm':[p.ToMM(pos.x),p.ToMM(pos.y)],'to_mm':[p.ToMM(f.GetPosition().x),p.ToMM(f.GetPosition().y)],'from_degrees':angle,'to_degrees':f.GetOrientationDegrees()})
 else:assert f.GetPosition()==pos and f.GetOrientationDegrees()==angle
result={'moves':moves,'affected_nets':sorted(affected),'retained_internal_copper_items':sum(retained.values()),'removed_boundary_copper_items':sum(removed.values()),'unchanged_copper_items':unchanged,'retained_by_net':dict(retained),'removed_by_net':dict(removed),'parent_board_sha256':cfg['parent_board_sha256'],'proxy_before':cfg['proxy_before'],'proxy_after':cfg['proxy_after'],'group':cfg['group'],'group_members':cfg.get('group_members',sorted(refs)),'anchor_refs':cfg.get('anchor_refs',[]),'rotation_deg':rotation,'translation_mm':cfg['translation_mm'],'outline_changed':False,'copper_layers':b.GetCopperLayerCount(),'copper_policy':cfg.get('copper_policy','remove_boundary_nets'),'qualification':'Explicit pose applied to original native project. Boundary copper handling follows recorded policy; internal-net copper translated, unrelated nets retained. Native physical/invariant check and whole-board routing required; no proxy-based promotion.'}
result.update(boundary_via_policy=cfg.get('boundary_via_policy','detach_incident'),preserved_boundary_vias=preserved_boundary_vias,incident_detachment_layer_scope='Only layers occupied by original moved pads; retained other-layer traces preserve via-to-trunk access')
(a.candidate/'placement-search.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k not in ['moves','retained_by_net','removed_by_net','affected_nets']},indent=2))
