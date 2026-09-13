"""Fixed-budget placement policy comparison using Copperhead's whole-board router."""
from pathlib import Path
import argparse,copy,hashlib,itertools,json,random,shutil,subprocess,sys,time
from datetime import datetime,timezone
import sexpdata as sx
from audit import audit,inventory,nodes,first
ROOT=Path(__file__).resolve().parents[2]
KIPY='/Users/philippe/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3.9'
KICAD='/Users/philippe/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli'
def now():return datetime.now(timezone.utc).isoformat()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,v):
 p=Path(p);temporary=p.with_name(p.name+'.tmp');temporary.write_text(json.dumps(v,indent=2)+'\n');temporary.replace(p)
def command(argv,f,label):
 t=time.monotonic();start=now();arguments=list(map(str,argv));scripts={v:sha(v) for v in arguments if v.endswith('.py') and Path(v).is_file()};error=None;r=None
 try:
  with (f/(label+'.log')).open('w') as log:r=subprocess.run(arguments,stdout=log,stderr=subprocess.STDOUT,timeout=360)
 except subprocess.TimeoutExpired as exc:error=exc
 record={'command':arguments,'script_sha256':scripts,'started_at':start,'finished_at':now(),'elapsed_seconds':time.monotonic()-t,'returncode':r.returncode if r else None,'timeout':error is not None};write(f/(label+'.command.json'),record)
 if error:raise error
 if r.returncode:raise RuntimeError(record)
 return record

def poses(board):return {r:v['pose'] for r,v in inventory(board)[0].items()}
def putposes(template,output,placements):
 d=sx.loads(template.read_text())
 for f in nodes(d,'footprint'):
  r=next(v[2] for v in nodes(f,'property') if v[1]=='Reference');at=first(f,'at');at[1:]=placements[r]
 output.write_text(sx.dumps(d))

def hpwl(ps,nets,signals=False):
 total=0
 for n,pads in nets.items():
  if signals and n in ['GND','EXT_5V']:continue
  rs=set(p.split('.')[0] for p in pads);xs=[ps[r][0] for r in rs];ys=[ps[r][1] for r in rs]
  total+=max(xs)-min(xs)+max(ys)-min(ys)
 return total

def propose(ps,nets,policy,tried):
 """Swap legal-size passive packages; rank only current placement and net groups."""
 refs=sorted(r for r in ps if r.startswith('R'))
 options=[]
 for a,b in itertools.combinations(refs,2):
  candidate=copy.deepcopy(ps);candidate[a],candidate[b]=candidate[b],candidate[a]
  key=json.dumps(candidate,sort_keys=True)
  if key in tried:continue
  signal=hpwl(candidate,nets,True);allnets=hpwl(candidate,nets)
  ranking=(allnets,signal,a,b) if policy=='all-net-hpwl' else (signal,allnets,a,b)
  affected={n:p for n,p in nets.items() if any(v.split('.')[0] in (a,b) for v in p)}
  options.append((ranking,candidate,{'kind':'swap_placements','components':[a,b],'before':{r:ps[r] for r in (a,b)},'after':{r:candidate[r] for r in (a,b)},'affected_net_groups':affected,'hpwl_before':hpwl(ps,nets),'hpwl_after':allnets,'signal_hpwl_before':hpwl(ps,nets,True),'signal_hpwl_after':signal}))
 _,candidate,action=min(options,key=lambda v:v[0]);tried.add(json.dumps(candidate,sort_keys=True));return candidate,action

def realize(base,folder,placements,manifest,source,route=True):
 folder.mkdir();write(folder/'source-receipt.json',{'source_sha':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'source_files':{str(p.relative_to(ROOT)):sha(p) for p in (ROOT/'experiments/large-loop').rglob('*.py')},'input_board_sha256':sha(base/'input/large-loop.kicad_pcb'),'input_manifest_sha256':sha(manifest),'created_at':now()});shutil.copy2(base/'authoritative-project.json',folder/'pcbgolf.kicad_pro');shutil.copytree(base/'input/pcbgolf.pretty',folder/'pcbgolf.pretty');shutil.copy2(base/'input/fp-lib-table',folder/'fp-lib-table');putposes(base/'input/large-loop.kicad_pcb',folder/'pcbgolf.kicad_pcb',placements)
 shutil.copytree(base/'input/models',folder/'models')
 shutil.copytree(base/'input/pcbgolf.3dshapes',folder/'pcbgolf.3dshapes')
 shutil.copy2(base/'input/large-loop.kicad_sch',folder/'pcbgolf.kicad_sch');shutil.copy2(base/'input/pcbgolf.kicad_sym',folder/'pcbgolf.kicad_sym');shutil.copy2(base/'input/sym-lib-table',folder/'sym-lib-table')
 project=(folder/'pcbgolf.kicad_pro').read_bytes();cmds=[]
 def native(action):
  cmds.append(command([KIPY,ROOT/'experiments/large-loop/native_stage.py',action,folder],folder,action))
  current=(folder/'pcbgolf.kicad_pro').read_bytes()
  if current!=project:
   (folder/(action+'-producer-project.json')).write_bytes(current)
  (folder/'pcbgolf.kicad_pro').write_bytes(project)
 native('export');shutil.copy2(folder/'pcbgolf.kicad_pcb',folder/'preview.kicad_pcb')
 cmds.append(command([KICAD,'pcb','drc','--schematic-parity','--format','json','-o',folder/'preflight.json',folder/'pcbgolf.kicad_pcb'],folder,'preflight'))
 pre=json.loads((folder/'preflight.json').read_text())
 # Routing may investigate an input with a documented immutable intrinsic DRC floor.
 # This does not waive those violations from independent acceptance.
 def signature(v):return (v['type'],tuple(sorted(i['uuid'] for i in v['items'])))
 frozen=json.loads((base/'intrinsic-violations.json').read_text()) if (base/'intrinsic-violations.json').exists() else []
 known={signature(v) for v in frozen}
 new_required=[v for v in pre['violations'] if signature(v) not in known and (v['severity']=='error' or v['type'] in ['silk_over_copper','silk_overlap','text_height','text_thickness'])]
 legal=not new_required and not pre.get('schematic_parity',[{}])
 if route and legal:
  cmds.append(command([sys.executable,ROOT/'scripts/copperhead_route.py',folder,'--seconds','240','--passes','100','--whole-board','--skip-fanout'],folder,'full-route'));native('import')
 native('audit');cmds.append(command([KICAD,'pcb','drc','--schematic-parity','--format','json','-o',folder/'drc.json',folder/'pcbgolf.kicad_pcb'],folder,'drc'))
 result=audit(folder,manifest,source);result['placement_legal']=legal;result['routing_attempted']=bool(route and legal);result['intrinsic_violation_count']=len(frozen);result['new_preflight_violations']=new_required
 cmds.append(command([KICAD,'pcb','export','svg','--layers','F.Cu,B.Cu,F.SilkS,Edge.Cuts','--mode-single','--page-size-mode','2','--exclude-drawing-sheet','-o',folder/'board.svg',folder/'pcbgolf.kicad_pcb'],folder,'render'))
 command(['/opt/homebrew/bin/rsvg-convert','-w','1400','-o',folder/'board.png',folder/'board.svg'],folder,'raster')
 write(folder/'evaluation.json',result);return result,cmds

def stage_one_terminal(evaluation):
 """Only the independent native acceptance gate authorizes Stage2."""
 return bool(evaluation.get('accepted')) and evaluation.get('native_open_count')==0 and evaluation.get('feasibility_cost')==0 and evaluation.get('schematic_parity_issues')==0 and evaluation.get('erc_violations')==0

def require_stage_one_work(parent):
 evaluation=json.loads((Path(parent)/'evaluation.json').read_text())
 if stage_one_terminal(evaluation):
  raise SystemExit('Stage1 already complete at this fully valid native checkpoint; hand off to Stage2 instead of making another feasibility proposal.')
