"""Apply an explicit rigid pose proposal to native CAD with audited copper handling."""
import argparse,collections,hashlib,json
from pathlib import Path
import pcbnew as p
ap=argparse.ArgumentParser();ap.add_argument('candidate',type=Path);ap.add_argument('--proposal',type=Path,required=True);a=ap.parse_args();cfg=json.loads(a.proposal.read_text());path=a.candidate/'pcbgolf.kicad_pcb';assert hashlib.sha256(path.read_bytes()).hexdigest()==cfg['parent_board_sha256'],'Stale parent board'
b=p.LoadBoard(str(path));fs={f.GetReference():f for f in b.GetFootprints()};refs=set(cfg['refs']);assert refs and refs|set(cfg['locked_refs'])==set(fs) and not refs&set(cfg['locked_refs']);dx,dy=cfg['translation_mm'];delta=p.VECTOR2I(p.FromMM(dx),p.FromMM(dy));old={r:(p.VECTOR2I(f.GetPosition()),f.GetOrientationDegrees()) for r,f in fs.items()};net_refs=collections.defaultdict(set)
for r,f in fs.items():
 for q in f.Pads():
  if q.GetNetname():net_refs[q.GetNetname()].add(r)
for ref in refs:
 f=fs[ref];expected=cfg['from_poses'][ref];pos=f.GetPosition();assert abs(p.ToMM(pos.x)-expected['x_mm'])<1e-5 and abs(p.ToMM(pos.y)-expected['y_mm'])<1e-5 and abs(f.GetOrientationDegrees()-expected['angle_deg'])<1e-5,'Stale source pose';f.SetPosition(pos+delta)
affected={n for n,owners in net_refs.items() if owners&refs};assert affected==set(cfg['nets']);retained=collections.Counter();removed=collections.Counter();unchanged=0
for t in list(b.GetTracks()):
 n=t.GetNetname();owners=net_refs.get(n,set())
 if n not in affected:unchanged+=1;continue
 if owners<=refs:t.Move(delta);retained[n]+=1
 else:removed[n]+=1;b.Delete(t)
p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(path),b)
moves=[]
for r,f in fs.items():
 pos,angle=old[r]
 if r in refs:
  assert f.GetPosition()==pos+delta and f.GetOrientationDegrees()==angle
  moves.append({'ref':r,'uuid':f.m_Uuid.AsString(),'from_mm':[p.ToMM(pos.x),p.ToMM(pos.y)],'to_mm':[p.ToMM(f.GetPosition().x),p.ToMM(f.GetPosition().y)],'from_degrees':angle,'to_degrees':angle})
 else:assert f.GetPosition()==pos and f.GetOrientationDegrees()==angle
result={'moves':moves,'affected_nets':sorted(affected),'retained_internal_copper_items':sum(retained.values()),'removed_boundary_copper_items':sum(removed.values()),'unchanged_copper_items':unchanged,'retained_by_net':dict(retained),'removed_by_net':dict(removed),'parent_board_sha256':cfg['parent_board_sha256'],'proxy_before':cfg['proxy_before'],'proxy_after':cfg['proxy_after'],'group':cfg['group'],'translation_mm':cfg['translation_mm'],'outline_changed':False,'copper_layers':b.GetCopperLayerCount(),'qualification':'Rigid pose applied to original native project. Whole affected boundary nets removed, internal-net copper translated, unrelated nets retained. Native physical/invariant check and whole-board routing required; no proxy-based promotion.'}
(a.candidate/'placement-search.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k not in ['moves','retained_by_net','removed_by_net','affected_nets']},indent=2))
