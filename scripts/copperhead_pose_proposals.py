"""Bounded pose-only proposals using pinned KRT geometry; never writes native CAD."""
import argparse,hashlib,json,sys,time,math,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];LOCAL=ROOT/'.local/copperhead';repo=LOCAL/'tools/KiCadRoutingTools'
ap=argparse.ArgumentParser();ap.add_argument('parent',type=Path);ap.add_argument('--manifest',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--group',default='sd_card_interface');ap.add_argument('--move-refs');ap.add_argument('--rotations',default='0');ap.add_argument('--steps',default='-15,-10,-5,5,10,15');ap.add_argument('--feedback',type=Path);ap.add_argument('--allow-proxy-regression',action='store_true');ap.add_argument('--x-steps');ap.add_argument('--y-steps');a=ap.parse_args();started=time.monotonic()
if bool(a.x_steps)!=bool(a.y_steps):ap.error('--x-steps and --y-steps must be supplied together')
provenance=json.loads((LOCAL/'tools/krt-provenance.json').read_text())
for name,digest in provenance['files'].items():assert hashlib.sha256((repo/name).read_bytes()).hexdigest()==digest,'KRT source drift: '+name
sys.path.insert(0,str(repo/'py_placer'));import _path
from kicad_parser import parse_kicad_pcb
from placement.groups import derive_groups,parse_sources
from placement.diagnosis import make_state,diagnose,to_json
board=a.parent/'pcbgolf.kicad_pcb';before_hash=hashlib.sha256(board.read_bytes()).hexdigest();data=parse_kicad_pcb(str(board));cfg=json.loads(a.manifest.read_text());groups=cfg['groups'];flat=[r for rs in groups.values() for r in rs];assert set(flat)==set(data.footprints) and len(flat)==len(set(flat))
data.groups=groups;derived=derive_groups(data,parse_sources('kicad'))
# Search one declared connected group while all other bodies remain fixed.
group=a.group;members=groups[group];refs=a.move_refs.split(',') if a.move_refs else members;assert set(refs)<=set(members);rotations=[float(x) for x in a.rotations.split(',')];assert len(refs)==1 or rotations==[0.0];ignored={i for i,n in data.nets.items() if n.name in ('GND','+3V3','+5V','+12V')}
state=make_state(data,str(board),clearance=.2,board_edge_clearance=.5,ignore_net_ids=ignored,extra_locked_refs=set(flat)-set(refs),move_refs=set(refs))
state.build_neighbor_lists(max(abs(float(x)) for x in ((a.x_steps+","+a.y_steps) if a.x_steps else a.steps).split(","))*math.sqrt(2)+1);baseline=state.total_cost();diagnosis=to_json(diagnose(state,data,{group:refs},ignore_net_ids=sorted(ignored),budget=13))
poses={r:{'x_mm':state.parts[r].x,'y_mm':state.parts[r].y,'angle_deg':state.parts[r].rot} for r in refs}
# Bind local approach proxies to a native report for these exact board bytes.
local_targets=[];diagnostic_source=None
for record_path in sorted((LOCAL/'runs').glob('stage1-*/attempt.json'),reverse=True):
 record=json.loads(record_path.read_text());evaluation=record.get('before',{})
 if evaluation.get('files',{}).get('pcbgolf.kicad_pcb')!=before_hash:continue
 diagnostic_source=evaluation.get('report')
 for finding in evaluation.get('violations',[]):
  if finding['type']!='unconnected_items' or len(finding.get('items',[]))!=2:continue
  endpoints=[]
  for item in finding['items']:
   match=re.search(r' of (\S+) on ',item.get('description',''));endpoints.append(dict(ref=match.group(1) if match else None,position=item.get('pos'),uuid=item.get('uuid'),description=item.get('description')))
  if sum(e['ref'] in refs for e in endpoints)==1 and all(e['position'] for e in endpoints):local_targets.append(endpoints)
 break
def local_approach(dx,dy,rotation):
 total=0
 for endpoints in local_targets:
  points=[]
  for e in endpoints:
   x,y=e['position']['x'],e['position']['y']
   if e['ref'] in refs:
    pose=poses[e['ref']];rx,ry=x-pose['x_mm'],y-pose['y_mm'];angle=math.radians(rotation)
    x=pose['x_mm']+rx*math.cos(angle)+ry*math.sin(angle)+dx;y=pose['y_mm']-rx*math.sin(angle)+ry*math.cos(angle)+dy
   points.append((x,y))
  total+=math.dist(*points)
 return total

steps=[float(x) for x in a.steps.split(',')];deltas=list(dict.fromkeys([(x,0) for x in steps]+[(0,x) for x in steps]+[(x,y) for x in steps for y in steps if abs(x)==abs(y)]))
if a.x_steps:deltas=[(float(x),float(y)) for x in a.x_steps.split(',') for y in a.y_steps.split(',')]
feedback=json.loads(a.feedback.read_text()) if a.feedback else []
tried={(tuple(f['action_parameters']['translation_mm']),f['action_parameters'].get('rotation_deg',0)) for f in feedback if f.get('action_parameters',{}).get('group')==group and f.get('action_parameters',{}).get('parent_board_sha256')==before_hash and f.get('action_parameters',{}).get('refs')==refs}
trials=[]
for dx,dy in deltas+([(0,0)] if any(rotations) else []):
 for rotation in rotations:
  if dx==dy==rotation==0:continue
  legal=((dx,dy),rotation) not in tried and (state.candidate_valid(refs[0],poses[refs[0]]['x_mm']+dx,poses[refs[0]]['y_mm']+dy,(poses[refs[0]]['angle_deg']+rotation)%360) if rotation else state.group_move_valid(refs,dx,dy))
  item={'translation_mm':[dx,dy],'rotation_deg':rotation,'geometry_screen':legal,'already_evaluated_on_parent':((dx,dy),rotation) in tried,'local_approach_mm':local_approach(dx,dy,rotation)}
  if legal:
   if len(refs)==1:
    ref=refs[0];pose=poses[ref];state.apply_move(ref,pose['x_mm']+dx,pose['y_mm']+dy,(pose['angle_deg']+rotation)%360);item['proxy']=state.total_cost();state.apply_move(ref,pose['x_mm'],pose['y_mm'],pose['angle_deg'])
   else:
    state.apply_group_move(refs,dx,dy);item['proxy']=state.total_cost();state.apply_group_move(refs,-dx,-dy)
  trials.append(item)
legal=sorted([r for r in trials if r['geometry_screen']],key=lambda r:(r['local_approach_mm'] if a.move_refs else 0,r['proxy']['total']));assert legal,'No geometry-screened pose'
selected=legal[:3];affected=sorted({p.net_name for ref in refs for p in data.footprints[ref].pads if p.net_name})
result={'schema_version':1,'kind':'group_pose','parent_candidate':str(a.parent.resolve()),'parent_board_sha256':before_hash,'group':group,'refs':refs,'group_members':members,'anchor_refs':sorted(set(members)-set(refs)),'rotation_deg':selected[0]['rotation_deg'],'groups':groups,'locked_refs':sorted(set(flat)-set(refs)),'from_poses':poses,'translation_mm':selected[0]['translation_mm'],'nets':affected,'net':affected[0], 'copper_policy':'detach_moved_pad_incident','reason':f'Bounded KRT pose search for {group}; exclude {len(tried)} evaluated moves on this exact parent; preserve declared fixed components','hypothesis':'Improve relative interface placement while keeping outline and declared fixed-component poses unchanged; geometric proxy does not establish routing gain','feedback_used':[f['attempt'] for f in feedback[-8:]] or ['pcb-placement-research.md'],'ranking':'local_failed_endpoint_approach_then_global_proxy' if a.move_refs else 'global_proxy','generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'local_approach':dict(native_report=diagnostic_source,targets=local_targets,before_mm=local_approach(0,0,0),after_mm=selected[0]['local_approach_mm'],qualification='Native representative disconnected-item distance proxy; not a legal route or complete copper-island distance'),'proxy_before':baseline,'proxy_after':selected[0]['proxy'],'proxy_ignored_nets':['GND','+3V3','+5V','+12V'],'full_board_evaluation_includes_ignored_proxy_nets':True,'excluded_moves':[dict(translation_mm=list(t),rotation_deg=r) for t,r in sorted(tried)],'trials':trials,'finalists':selected,'diagnosis':diagnosis,'krt_groups_derived':derived,'krt_revision':'1c428c0b2285a4dfe8901ca7035109ded6cfbb4d','screen_limitation':'KRT ranking/geometry only, pad legality layer off; native physical/invariant recheck mandatory, retained copper not modeled by KRT','elapsed_seconds':time.monotonic()-started}
assert hashlib.sha256(board.read_bytes()).hexdigest()==before_hash
for ref,pose in poses.items():assert abs(state.parts[ref].x-pose['x_mm'])<1e-7 and abs(state.parts[ref].y-pose['y_mm'])<1e-7
assert a.allow_proxy_regression or result['proxy_after']['total']<baseline['total'],'No cheaper proposal; native diagnostic hypothesis required to explore proxy regression'
a.output.write_text(json.dumps(result,indent=2));print(json.dumps({k:result[k] for k in ['group','translation_mm','proxy_before','proxy_after','elapsed_seconds']},indent=2))
