"""Recorded broad placement then incremental route on the surviving live identity."""
from pathlib import Path
import json,os,sys,time,shutil
from observability import command,write,sha
from feasibility import evaluate
from placement_parameters import render
B=Path('/Users/philippe/dev/copper-scar-jitx');L=B/'runs/stage1';H=Path(__file__).parent.resolve();P=B/'.venv/bin/python';S=Path('/Users/philippe/dev/copper-scar-demo/.venv/bin/python')
name='pcbgolf_import.stage_one_002.StageOne002';uid=sys.argv[1] if len(sys.argv)>1 else 'iteration-008-group-floorplan';proposal_path=Path(sys.argv[2]) if len(sys.argv)>2 else L/'group-floorplan-008.json';out=L/uid;out.mkdir(exist_ok=False);proposal=json.loads(proposal_path.read_text());proposal.update(id=uid,design=name,mode='incremental',action=proposal['rationale']);write(out/'proposal.json',proposal)
st={'state':'running','runner_pid':os.getpid(),'started_at':time.time(),'proposal':proposal,'tools_sha256':{x.name:sha(x) for x in H.glob('*.py')}};write(out/'attempt-state.json',st)
shutil.copytree(B/'pcbgolf_import',out/'source',ignore=shutil.ignore_patterns('__pycache__'))
write(out/'placement-parameters.json',render(B/'pcbgolf_import/Pcbgolf.py',proposal['overrides'],out/'Pcbgolf-proposed.py'))
def run(label,args,timeout):
 r=command(args,B,out,label,timeout)
 if r['exit_code']!=0:raise RuntimeError(label+' failed; keep incumbent and preserved evidence')
def capture(label,route=False):
 args=[str(P),str(H/'native_iteration.py'),name,str(out/label)]
 if route:
  args.append('--route')
  for net in proposal.get('nets',[]):args+=['--net',net]
 run(label,args,900)
 c=B/'candidates'/(uid+'-'+label)
 run(label+'-normalize',[str(S),str(H/'roundtrip.py'),str(out/label/'export'/(name+'.kicad_pcb')),str(c)],60)
 result=evaluate(c,L,(proposal['action_kind']+' with preserved native identity; ' if label!='input' else 'Actual input to placement trial; exploratory live state, incumbent retained separately; ')+label)
 write(out/(label+'-evaluation.json'),result);return c,result
try:
 initial,first=capture('input')
 if not first['evaluation_reliable'] or not first['invariants_ok']:raise RuntimeError('input checks unreliable or invariants failed; do not reposition')
 run('placement',[str(P),str(H/'reposition_groups.py'),name,str(proposal_path),str(out/'placement')],200)
 shutil.copy2(out/'placement/placement-delta.json',out/'placement-delta.json')
 placed,mid=capture('placed')
 if not mid['evaluation_reliable'] or not mid['invariants_ok']:raise RuntimeError('mid-placement checks unreliable or invariants failed; do not route')
 run('placement-copper-audit',[str(S),str(H/'copper_audit.py'),str(initial/'pcbgolf.kicad_pcb'),str(placed/'pcbgolf.kicad_pcb'),str(out/'placement-copper-delta.json')],60)
 routed,last=capture('routed',True)
 run('route-copper-audit',[str(S),str(H/'copper_audit.py'),str(placed/'pcbgolf.kicad_pcb'),str(routed/'pcbgolf.kicad_pcb'),str(out/'route-copper-delta.json')],60)
 if last['retain']:write(L/'best-placement-parameters.json',{'candidate':str(routed),'design':name,'overrides':proposal['overrides'],'source_proposal':str(out/'Pcbgolf-proposed.py'),'native_state_runtime_owned':True,'rebuild_qualification':'blocked by separately observed native cache load crash; do not modify designs files'})
 st.update(state='completed',finished_at=time.time(),candidate=str(routed));write(out/'attempt-state.json',st)
except Exception as e:
 st.update(state='failed',finished_at=time.time(),error=str(e));write(out/'attempt-state.json',st);failure={'proposal':proposal,'error':str(e),'cost':None,'valid':False,'retain':False,'evaluation_reliable':False,'time':time.time()};write(out/'failure.json',failure)
 with (L/'iterations.jsonl').open('a') as f:f.write(json.dumps(failure)+'\n');f.flush();os.fsync(f.fileno())
 raise
