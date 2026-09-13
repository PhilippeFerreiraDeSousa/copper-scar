"""Deadline-bounded placement campaign driven by recorded native outcomes.

One writer, matched routing controls, explicit group moves, immutable attempts.
A rejected candidate never becomes the parent. This is diagnostic search only.
"""
import argparse,collections,fcntl,hashlib,json,os,re,subprocess,sys,time
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from copper_scar.tools.copperhead.stage1 import LOCAL,write,now
ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path);ap.add_argument('--until',required=True);ap.add_argument('--route-seconds',type=int,default=600);a=ap.parse_args();deadline=datetime.fromisoformat(a.until).timestamp()
work=LOCAL/'campaign';work.mkdir(exist_ok=True);lock=(work/'supervisor.lock').open('a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
path=work/'state.json';state=json.loads(path.read_text()) if path.exists() else dict(started_at=now(),decisions=[]);state.update(pid=os.getpid(),status='running',until=a.until);state.pop('finished_at',None)
manifest=LOCAL/'proposals/global-expanded.json';groups=json.loads(manifest.read_text())['groups'];python=str(ROOT/'.venv/bin/python');krt=str(LOCAL/'tools/krt-venv/bin/python')
def run(argv,label):
 with (work/(label+'.log')).open('w') as log:
  child=subprocess.Popen(argv,cwd=ROOT,stdout=log,stderr=subprocess.STDOUT)
  while child.poll() is None:
   state.update(heartbeat_at=now(),worker_pid=child.pid,phase=label);write(path,state);time.sleep(5)
  state.update(worker_pid=None,heartbeat_at=now());write(path,state)
  return child.returncode
# Wait for an already-authorized control to finish, without touching its worker.
with (LOCAL/'loop/runner.lock').open('a') as runner:
 while True:
  try:fcntl.flock(runner,fcntl.LOCK_EX|fcntl.LOCK_NB);fcntl.flock(runner,fcntl.LOCK_UN);break
  except BlockingIOError:state.update(phase='waiting for existing native worker',heartbeat_at=now());write(path,state);time.sleep(5)
epoch_parent=a.source.resolve() if a.source else None;epoch_trials=0;exhausted=set()
while time.time()+a.route_seconds+180<deadline:
 loop=json.loads((LOCAL/'loop/state.json').read_text());best=Path(loop['best_feasibility']['candidate'])
 if epoch_parent is None or epoch_trials>=6:
  epoch_parent=best;epoch_trials=0;exhausted=set()
 board_hash=hashlib.sha256((epoch_parent/'pcbgolf.kicad_pcb').read_bytes()).hexdigest()
 records=[json.loads(p.read_text()) for p in sorted((LOCAL/'runs').glob('stage1-*/attempt.json'))]
 for pending in state['decisions']:
  if 'attempt' not in pending:
   digest=hashlib.sha256(Path(pending['proposal']).read_bytes()).hexdigest();matches=[r for r in records if r.get('action',{}).get('proposal_sha256')==digest and r.get('status')!='running']
   if matches:
    r=matches[-1];pending.update(attempt=r['attempt'],status=r['status'],finished_at=r.get('finished_at'),became_incumbent=r.get('became_incumbent',False),after={k:r.get('after',{}).get(k) for k in ('unconnected','errors','warnings','invariants_ok')})
 write(path,state)
 controls=[r for r in records if Path(r.get('input',''))==epoch_parent and r.get('action',{}).get('kind')=='initial_route' and r.get('routing_scope',{}).get('effort_limit_seconds')==a.route_seconds and r.get('status')=='completed']
 if not controls:
  label='control-'+board_hash[:12];state['phase']=label;write(path,state)
  run([python,'-m','copper_scar.tools.copperhead.stage1','--source',str(epoch_parent),'--route-seconds',str(a.route_seconds),'--budget',str(a.route_seconds+240)],label)
  records=[json.loads(p.read_text()) for p in sorted((LOCAL/'runs').glob('stage1-*/attempt.json'))];controls=[r for r in records if Path(r.get('input',''))==epoch_parent and r.get('action',{}).get('kind')=='initial_route' and r.get('routing_scope',{}).get('effort_limit_seconds')==a.route_seconds and r.get('status')=='completed']
  if not controls:state.update(status='needs_attention',reason='No completed matched routing control; inspect preserved failure before new placement');break
 control=controls[-1];baseline=control['before'];feedback=json.loads((LOCAL/'loop/feedback.json').read_text());scores=[]
 for group,refs in groups.items():
  if group.startswith('mechanical') or group in exhausted:continue
  findings=[v for v in baseline['violations'] if v['type']=='unconnected_items' and any(any('of '+ref+' on ' in i.get('description','') for ref in refs) for i in v.get('items',[]))]
  if not findings:continue
  history=[r for r in records if r.get('action',{}).get('group')==group and r.get('action',{}).get('parent_board_sha256')==board_hash]
  # Actual failed attempts lower priority; never interpret the geometric proxy as native improvement.
  penalty=len(history);incident_gains=[]
  for prior in history:
   if prior.get('status')=='completed' and prior.get('effects'):
    measured=json.loads(Path(prior['effects']).read_text());incident_gains.append(sum(measured.get('missing_before',{}).get(n,0)-measured.get('missing_after',{}).get(n,0) for n in prior['action']['nets']))
  native_gain=max(incident_gains or [0])
  scores.append((len(findings)/(1+penalty)+max(0,native_gain),group,findings,history))
 if not scores:state.update(status='needs_attention',reason='All available diagnostic group moves exhausted for current parent');break
 queue=json.loads((work/'queue.json').read_text()) if (work/'queue.json').exists() else []
 queued=next((q for q in queue if q['id'] not in {d.get('queued_id') for d in state['decisions']}),None)
 if queued:
  scores=[x for x in scores if x[1]==queued['group']]
  if not scores:state.update(status='needs_attention',reason='Queued group has no current failed endpoints');break
 _,group,findings,history=max(scores,key=lambda x:(not state['decisions'] and x[1]=='can_channel_0',x[0]));index=len(state['decisions']);label=f'{index:03d}-{group}';proposal=LOCAL/'proposals'/('campaign-'+label+'.json')
 code=run([krt,str(ROOT/'scripts/copperhead_pose_proposals.py'),str(epoch_parent),'--manifest',str(manifest),'--output',str(proposal),'--group',group,'--steps='+queued.get('steps','-0.5,0.5,-1,1') if queued else '--steps=-0.5,0.5,-1,1,-2,2,-3,3,-5,5',*(['--move-refs',queued['move_refs'],'--rotations',queued.get('rotations','0')] if queued and queued.get('move_refs') else []),'--feedback',str(LOCAL/'loop/feedback.json'),'--allow-proxy-regression'],label+'-generate')
 if code:exhausted.add(group);continue
 action=json.loads(proposal.read_text());action.update(reason=f'{len(findings)} native missing endpoint pairs touch {group}; {len(history)} earlier moves on this exact parent inform priority and excluded translations',hypothesis='Change connected-group relative spacing to improve remaining interface access; native full-board and incident-net outcomes decide retention',diagnostic_endpoints=findings,matched_control=control['attempt'],matched_control_after={k:control['after'][k] for k in ('unconnected','errors','warnings')});action['research_context']=queued;write(proposal,action)
 decision=dict(index=index,queued_id=queued['id'] if queued else None,parent=str(epoch_parent),parent_board_sha256=board_hash,group=group,translation_mm=action['translation_mm'],proposal=str(proposal),matched_control=control['attempt'],diagnostic_pair_count=len(findings),prior_group_attempts=[r['attempt'] for r in history],started_at=now());state['decisions'].append(decision);write(path,state)
 run([python,'-m','copper_scar.tools.copperhead.stage1','--source',str(epoch_parent),'--proposal',str(proposal),'--route-seconds',str(a.route_seconds),'--budget',str(a.route_seconds+300)],label+'-evaluate')
 records=[json.loads(p.read_text()) for p in (LOCAL/'runs').glob('stage1-*/attempt.json')];matching=[r for r in records if r.get('action',{}).get('proposal_sha256')==hashlib.sha256(proposal.read_bytes()).hexdigest()]
 if not matching:state.update(status='needs_attention',reason='Evaluation produced no attributable attempt');break
 result=matching[-1];decision.update(attempt=result['attempt'],status=result['status'],finished_at=now(),became_incumbent=result.get('became_incumbent',False),error=result.get('error'),after={k:result.get('after',{}).get(k) for k in ('unconnected','errors','warnings','invariants_ok')})
 if result.get('effects'):
  effects=json.loads(Path(result['effects']).read_text());before=effects.get('missing_before',{});after=effects.get('missing_after',{});decision['incident_net_changes']={n:dict(before=before.get(n,0),after=after.get(n,0)) for n in action['nets'] if before.get(n,0)!=after.get(n,0)}
 write(path,state);epoch_trials+=1
 if result.get('became_incumbent'):epoch_parent=None
 if result.get('status')=='failed' and 'Placement failed native' not in result.get('error',''):
  state.update(status='needs_attention',reason='Execution failure requires supervisor inspection');break
 try:
  from copper_scar.tools.copperhead.replay_service import start
  state['replay']=start('outer')
 except Exception as e:state['replay_error']=repr(e)
else:state.update(status='packaging_freeze',reason='No new full routing evaluation fits before the packaging deadline')
state.update(heartbeat_at=now(),finished_at=now(),worker_pid=None);write(path,state);print(json.dumps(state,indent=2))
