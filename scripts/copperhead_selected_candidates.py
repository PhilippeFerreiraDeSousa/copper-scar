"""Bind the next diagnostic R89 placement catalog; separate from matched pilot."""
import argparse, hashlib, json, math
from pathlib import Path
import pcbnew as p
ap=argparse.ArgumentParser();ap.add_argument('parent',type=Path);ap.add_argument('evaluation',type=Path);ap.add_argument('template',type=Path);ap.add_argument('output',type=Path);a=ap.parse_args()
path=a.parent/'pcbgolf.kicad_pcb';manager=p.SETTINGS_MANAGER();pro=a.parent/'pcbgolf.kicad_pro';manager.LoadProject(str(pro));b=p.LoadBoard(str(path));b.SetProject(manager.GetProject(str(pro)));p.ZONE_FILLER(b).Fill(b.Zones());conn=b.GetConnectivity();conn.Build(b);conn.RecalculateRatsnest()
sha=hashlib.sha256(path.read_bytes()).hexdigest();evaluation=json.loads(a.evaluation.read_text());assert evaluation['files']['pcbgolf.kicad_pcb']==sha
fs={f.GetReference():f for f in b.GetFootprints()};pads={q.m_Uuid.AsString():q for f in fs.values() for q in f.Pads()};actions=[];unavailable=[]
ref='R89';f=fs[ref];nets=sorted({q.GetNetname() for q in f.Pads() if q.GetNetname()});position=f.GetPosition()
def proxy(dx,dy):
 total=0
 for v in evaluation['violations']:
  items=v.get('items',[])
  if v['type']!='unconnected_items' or len(items)!=2 or not any(' of R89 on ' in i.get('description','') for i in items):continue
  points=[]
  for i in items:
   pt=i['pos'];moved=' of R89 on ' in i.get('description','');points.append((pt['x']+(dx if moved else 0),pt['y']+(dy if moved else 0)))
  total+=math.dist(*points)
 return total
for ident,dx,dy in [('r89-left-two',-2,.5),('r89-left-one',-1,0),('r89-left-half',-.5,0)]:
 actions.append(dict(id=ident,kind='group_pose',parent_board_sha256=sha,refs=[ref],locked_refs=sorted(set(fs)-{ref}),from_poses={ref:dict(x_mm=p.ToMM(position.x),y_mm=p.ToMM(position.y),angle_deg=f.GetOrientationDegrees())},translation_mm=[dx,dy],rotation_deg=0,nets=nets,net=nets[0],group='port_channel_3',group_members=[ref],copper_policy='detach_moved_pad_incident',boundary_via_policy='preserve_existing_sites',preserve_foreign_copper=True,proxy_before=dict(total=proxy(0,0)),proxy_after=dict(total=proxy(dx,dy)),local_approach_mm=proxy(dx,dy),reason='Shared finite native-bound R89 placement library',hypothesis='Shorter disconnected endpoint approach may improve full-board realizability',feedback_used=[str(a.evaluation)]))
template=json.loads(a.template.read_text());sites=template['via_sites'];valid=True
for site in sites:
 x,y=map(p.FromMM,site['position_mm']);matches=[]
 for t in b.GetTracks():
  if t.GetClass()!='PCB_TRACK' or t.GetNetname()!=site['net'] or b.GetLayerName(t.GetLayer())!=site['target_layer']:continue
  s=t.GetStart();e=t.GetEnd();dx=e.x-s.x;dy=e.y-s.y
  if dx*(y-s.y)!=dy*(x-s.x) or not min(s.x,e.x)<=x<=max(s.x,e.x) or not min(s.y,e.y)<=y<=max(s.y,e.y):continue
  matches.append(t)
 if len(matches)!=1:valid=False;break
 t=matches[0];uid=t.m_Uuid.AsString();site['target_track_uuid']=uid
 site['target_track_geometry']=dict(uuid=uid,net=t.GetNetname(),kind='TRACK',position_mm=[p.ToMM(t.GetPosition().x),p.ToMM(t.GetPosition().y)],layers=[b.GetLayerName(t.GetLayer())],start_mm=[p.ToMM(t.GetStart().x),p.ToMM(t.GetStart().y)],end_mm=[p.ToMM(t.GetEnd().x),p.ToMM(t.GetEnd().y)],width_mm=p.ToMM(t.GetWidth()))
 site['expected_original_island_item_uuids']=sorted({z.m_Uuid.AsString() for z in conn.GetConnectedItems(t) if isinstance(z,(p.PAD,p.PCB_TRACK))}|{uid})
 site.pop('proof_via_uuid',None)
if valid:
 group0=set(sites[0]['expected_original_island_item_uuids']);group1=set(sites[1]['expected_original_island_item_uuids'])
 if group0&group1:valid=False;unavailable.append(dict(id='can2-existing-island-anchors',reason='Native target islands already connected'))
if valid:
 actions.append(dict(id='can2-existing-island-anchors',schema_version=1,kind='local_topology_replan',parent_board_sha256=sha,net='CAN2_H',nets=['CAN2_H'],remove_items=[],via_sites=sites,required_original_track_width_mm={'CAN2_H':.2},final_acceptance=dict(maximum_retained_missing_links=evaluation['unconnected']-1),reason='Add explicit layer access to two currently disconnected CAN2 islands while retaining power copper',hypothesis='Existing-island anchors make alternate copper layers available to full-board realization',feedback_used=[str(a.evaluation),str(a.template)],local_approach_mm=21.3135))
else:unavailable.append(dict(id='can2-existing-island-anchors',reason='Native exact anchor binding unavailable or already connected'))
a.output.write_text(json.dumps(dict(parent_board_sha256=sha,actions=actions,unavailable=unavailable),indent=2));assert hashlib.sha256(path.read_bytes()).hexdigest()==sha
