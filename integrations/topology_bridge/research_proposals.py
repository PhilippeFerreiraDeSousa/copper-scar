"""Bounded pose-only proposals using pinned KRT geometry; never writes native CAD."""
import argparse,hashlib,json,sys,time
from pathlib import Path
LOCAL=Path('/Users/philippe/dev/copper-scar-demo/.local/copperhead');repo=LOCAL/'tools/KiCadRoutingTools'
ap=argparse.ArgumentParser();ap.add_argument('parent',type=Path);ap.add_argument('--manifest',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--group',required=True);ap.add_argument('--board-name',default='pcbgolf.kicad_pcb');a=ap.parse_args();started=time.monotonic()
provenance=json.loads((LOCAL/'tools/krt-provenance.json').read_text())
for name,digest in provenance['files'].items():assert hashlib.sha256((repo/name).read_bytes()).hexdigest()==digest,'KRT source drift: '+name
sys.path.insert(0,str(repo/'py_placer'));import _path
from kicad_parser import parse_kicad_pcb
from placement.groups import derive_groups,parse_sources
from placement.diagnosis import make_state,diagnose,to_json
board=a.parent/a.board_name;before_hash=hashlib.sha256(board.read_bytes()).hexdigest();# Use native KiCad spelling in an external copy for KRT regex parsers.
import subprocess
parser_dir=a.output.parent/(a.output.stem+'-parser-input');parser_dir.mkdir(exist_ok=False)
parser_board=parser_dir/board.name
kp='/Users/philippe/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3'
normalization=subprocess.check_output([kp,str(Path(__file__).with_name('normalize_for_research.py')),str(board.resolve()),str(parser_board.resolve())],text=True)
(parser_dir/'normalization.json').write_text(normalization)
data=parse_kicad_pcb(str(parser_board));cfg=json.loads(a.manifest.read_text());groups=cfg['groups'];flat=[r for rs in groups.values() for r in rs];assert set(flat)==set(data.footprints) and len(flat)==len(set(flat))
data.groups=groups;derived=derive_groups(data,parse_sources('kicad'))
# Group and search translations are explicit input; all other bodies are fixed.
group=a.group;refs=groups[group];ignored={i for i,n in data.nets.items() if n.name in cfg.get('proxy_ignored_nets',[])}
state=make_state(data,str(parser_board),clearance=cfg.get('clearance_mm',.25),board_edge_clearance=cfg.get('board_edge_clearance_mm',.5),ignore_net_ids=ignored,extra_locked_refs=set(flat)-set(refs),move_refs=set(refs))
state.build_neighbor_lists(22.0);baseline=state.total_cost();diagnosis=to_json(diagnose(state,data,{group:refs},ignore_net_ids=sorted(ignored),budget=13))
poses={r:{'x_mm':state.parts[r].x,'y_mm':state.parts[r].y,'angle_deg':state.parts[r].rot} for r in refs}
deltas=cfg['translation_candidates_mm']
trials=[]
for dx,dy in deltas:
 legal=state.group_move_valid(refs,dx,dy);item={'translation_mm':[dx,dy],'geometry_screen':legal}
 if legal:
  state.apply_group_move(refs,dx,dy);item['proxy']=state.total_cost();state.apply_group_move(refs,-dx,-dy)
 trials.append(item)
legal=sorted([r for r in trials if r['geometry_screen']],key=lambda r:r['proxy']['total']);assert legal,'No geometry-screened pose'
selected=legal[:3];affected=sorted({p.net_name for ref in refs for p in data.footprints[ref].pads if p.net_name})
result={'schema_version':1,'kind':'group_pose','parent_candidate':str(a.parent.resolve()),'parent_board_sha256':before_hash,'parser_copy_sha256':hashlib.sha256(parser_board.read_bytes()).hexdigest(),'group':group,'refs':refs,'groups':groups,'locked_refs':sorted(set(flat)-set(refs)),'from_poses':poses,'translation_mm':selected[0]['translation_mm'],'nets':affected,'reason':'Parameterized pinned KRT group translation search on the hash-bound supplied parent','hypothesis':'Improve relative interface placement while keeping outline and within-group poses fixed; geometric proxy does not establish routing gain','feedback_used':[],'proxy_before':baseline,'proxy_after':selected[0]['proxy'],'proxy_ignored_nets':cfg.get('proxy_ignored_nets',[]),'full_board_evaluation_includes_ignored_proxy_nets':True,'trials':trials,'finalists':selected,'diagnosis':diagnosis,'krt_groups_derived':derived,'krt_revision':'1c428c0b2285a4dfe8901ca7035109ded6cfbb4d','screen_limitation':'KRT ranking/geometry only, pad legality layer off; native physical/invariant recheck mandatory, retained copper not modeled by KRT','elapsed_seconds':time.monotonic()-started}
assert hashlib.sha256(board.read_bytes()).hexdigest()==before_hash
for ref,pose in poses.items():assert abs(state.parts[ref].x-pose['x_mm'])<1e-7 and abs(state.parts[ref].y-pose['y_mm'])<1e-7
result['proxy_improvement']=result['proxy_after']['total']<baseline['total']
a.output.write_text(json.dumps(result,indent=2));print(json.dumps({k:result[k] for k in ['group','translation_mm','proxy_before','proxy_after','elapsed_seconds']},indent=2))
