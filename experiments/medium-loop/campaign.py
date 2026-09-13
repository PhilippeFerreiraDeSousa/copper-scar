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
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
def command(argv,f,label):
 t=time.monotonic();start=now()
 with (f/(label+'.log')).open('w') as log:r=subprocess.run(list(map(str,argv)),stdout=log,stderr=subprocess.STDOUT,timeout=360)
 record={'command':list(map(str,argv)),'started_at':start,'finished_at':now(),'elapsed_seconds':time.monotonic()-t,'returncode':r.returncode};write(f/(label+'.command.json'),record)
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

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True);ap.add_argument('--source',type=Path,required=True);ap.add_argument('--decisions',type=int,default=3);a=ap.parse_args();base=a.base.resolve();out=base/'campaign';out.mkdir();manifest=base/'input/circuit.json';m=json.loads(manifest.read_text());source=a.source.resolve();commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
 assert json.loads((base/'feasible-width200/acceptance.json').read_text())['accepted'],'Feasibility must be established first'
 # This initializer does not read known feasible coordinates. Only circuit ref IDs.
 refs=sorted(r for r in m['refs'] if r!='J4');slots=[[38+8*(i%4),26+8*(i//4),0] for i in range(16)];rng=random.Random(713);rng.shuffle(slots);initial={r:slots[i] for i,r in enumerate(refs)};initial['J4']=[27,34,0]
 protocol={'schema':1,'hypothesis':'Excluding ubiquitous supply nets from placement ranking may improve routability under equal decision budget.','baseline':'all-net-hpwl','challenger':'signal-net-hpwl','source_sha':commit,'primary_metric':'retained feasibility_cost at N','N':a.decisions,'tie_policy':'keep baseline on equal primary cost; wire length and vias descriptive only','route_budget':{'seconds':60,'passes':30,'threads':1,'scope':'whole board both copper layers','fanout':False},'starting_poses':initial,'known_solution_coordinates_used':False,'lower_retention':'strict lower feasibility cost, then strictly shorter routed length at equal cost; forbid infeasible replacement of feasible incumbent','sample_limit':'One board, one deterministic placement seed, no verified router seed; descriptive pilot only','topology':'Each proposal explicitly starts a fresh full-board copper realization from its unrouted placement state. No inherited vias or tracks; existing routed evidence never edited. All stage parent/preview states contain zero vias, new routed vias must keep declared net membership and original dimensions.'}
 write(out/'protocol.json',protocol)
 initial_eval,cmds=realize(base,out/'initial-unrouted',initial,manifest,source,False)
 assert initial_eval['placement_legal'],'Initial placement is not legal'
 initial_routed,cmds=realize(base,out/'initial-routing-only',initial,manifest,source)
 records=[{'step':0,'arm':'routing-only','action':{'kind':'route_only'},'after':initial_routed,'folder':str(out/'initial-routing-only'),'source_sha':commit}]
 # Same baseline routing receipt shared by both arms. N counts placement decisions.
 for policy in ['all-net-hpwl','signal-net-hpwl']:
  ps=copy.deepcopy(initial);inc=copy.deepcopy(initial_routed);incpath=out/'initial-routing-only';tried=set();curve=[inc['feasibility_cost']]
  for step in range(1,a.decisions+1):
   start=now();candidate,action=propose(ps,m['nets'],policy,tried);folder=out/(policy+'-'+str(step));write(out/(policy+'-'+str(step)+'-proposal.json'),action)
   result,commands=realize(base,folder,candidate,manifest,source)
   retain=result['placement_legal'] and (result['feasibility_cost'],result['wire_length_mm'])<(inc['feasibility_cost'],inc['wire_length_mm'])
   record={'arm':policy,'step':step,'started_at':start,'finished_at':now(),'source_sha':commit,'parent_placement':ps,'parent_routed_evidence':str(incpath),'action':action,'after':result,'retain':retain,'folder':str(folder),'commands':commands,'preview_sha':sha(folder/'preview.kicad_pcb')}
   if retain:ps=candidate;inc=result;incpath=folder
   record['retained_cost']=inc['feasibility_cost'];record['retained_wire_mm']=inc['wire_length_mm'];records.append(record);write(folder/'decision.json',record);write(out/'records.json',records);curve.append(inc['feasibility_cost']);print(policy,step,result['feasibility_cost'],result['wire_length_mm'],'retain',retain,flush=True)
  write(out/(policy+'-outcome.json'),{'policy':policy,'curve':curve,'cost_at_N':inc['feasibility_cost'],'wire_length_mm':inc['wire_length_mm'],'selected_folder':str(incpath)})
 b=json.loads((out/'all-net-hpwl-outcome.json').read_text());c=json.loads((out/'signal-net-hpwl-outcome.json').read_text());winner='signal-net-hpwl' if c['cost_at_N']<b['cost_at_N'] else 'all-net-hpwl';write(out/'higher-loop-decision.json',{'baseline':b,'challenger':c,'selected_policy':winner,'challenger_kept':winner=='signal-net-hpwl','reason':'Primary cost@N; ties retain baseline','source_sha':commit,'limitations':protocol['sample_limit']})
if __name__=='__main__':main()
