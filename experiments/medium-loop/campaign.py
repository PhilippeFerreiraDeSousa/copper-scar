"""Fixed-budget placement policy comparison using Copperhead's whole-board router."""
from pathlib import Path
import argparse,copy,hashlib,itertools,json,random,shutil,subprocess,sys,time,os
from datetime import datetime,timezone
import sexpdata as sx
from audit import audit,inventory,nodes,first
ROOT=Path(__file__).resolve().parents[2]
KIPY='/Users/philippe/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3.9'
KICAD='/Users/philippe/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli'
def now():return datetime.now(timezone.utc).isoformat()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,v):
 tmp=p.with_name(p.name+'.tmp');tmp.write_text(json.dumps(v,indent=2)+'\n');os.replace(tmp,p)
def command(argv,f,label):
 t=time.monotonic();start=now();script_hashes={str(v):sha(v) for v in argv if str(v).endswith('.py') and Path(v).is_file()}
 with (f/(label+'.log')).open('w') as log:r=subprocess.run(list(map(str,argv)),stdout=log,stderr=subprocess.STDOUT,timeout=360)
 record={'script_sha256_at_start':script_hashes,'command':list(map(str,argv)),'started_at':start,'finished_at':now(),'elapsed_seconds':time.monotonic()-t,'returncode':r.returncode};write(f/(label+'.command.json'),record)
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
 folder.mkdir();shutil.copy2(base/'authoritative-project.json',folder/'pcbgolf.kicad_pro');shutil.copytree(base/'input/pcbgolf.pretty',folder/'pcbgolf.pretty');shutil.copy2(base/'input/fp-lib-table',folder/'fp-lib-table');putposes(base/'input/medium-loop.kicad_pcb',folder/'pcbgolf.kicad_pcb',placements)
 shutil.copytree(base/'input/models',folder/'models')
 shutil.copy2(base/'input/medium-loop.kicad_sch',folder/'pcbgolf.kicad_sch');shutil.copy2(base/'input/pcbgolf.kicad_sym',folder/'pcbgolf.kicad_sym');shutil.copy2(base/'input/sym-lib-table',folder/'sym-lib-table')
 project=(folder/'pcbgolf.kicad_pro').read_bytes();cmds=[]
 def native(action):
  cmds.append(command([KIPY,ROOT/'experiments/medium-loop/native_stage.py',action,folder],folder,action))
  current=(folder/'pcbgolf.kicad_pro').read_bytes()
  if current!=project:
   (folder/(action+'-producer-project.json')).write_bytes(current)
  (folder/'pcbgolf.kicad_pro').write_bytes(project)
 native('export');shutil.copy2(folder/'pcbgolf.kicad_pcb',folder/'preview.kicad_pcb')
 cmds.append(command([KICAD,'pcb','drc','--schematic-parity','--format','json','-o',folder/'preflight.json',folder/'pcbgolf.kicad_pcb'],folder,'preflight'))
 pre=json.loads((folder/'preflight.json').read_text());legal=not pre['violations']
 if route and legal:
  cmds.append(command([sys.executable,ROOT/'scripts/copperhead_route.py',folder,'--seconds','240','--passes','100','--whole-board','--skip-fanout'],folder,'full-route'));native('import')
 native('audit');cmds.append(command([KICAD,'pcb','drc','--schematic-parity','--format','json','-o',folder/'drc.json',folder/'pcbgolf.kicad_pcb'],folder,'drc'))
 result=audit(folder,manifest,source);result['placement_legal']=legal;result['routing_attempted']=bool(route and legal)
 cmds.append(command([KICAD,'pcb','export','svg','--layers','F.Cu,B.Cu,F.SilkS,Edge.Cuts','--mode-single','--page-size-mode','2','--exclude-drawing-sheet','-o',folder/'board.svg',folder/'pcbgolf.kicad_pcb'],folder,'render'))
 command(['/opt/homebrew/bin/rsvg-convert','-w','1400','-o',folder/'board.png',folder/'board.svg'],folder,'raster')
 write(folder/'evaluation.json',result);return result,cmds
