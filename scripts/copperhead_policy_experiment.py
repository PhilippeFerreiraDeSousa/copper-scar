"""One preregistered, matched two-policy pilot using the native lower loop.

Independent incumbents; all screened candidates and failed decisions are retained.
Policy choice is based only on cost after the fixed decision count, never proxy wins.
"""
import argparse, fcntl, hashlib, json, os, subprocess, sys, time, uuid
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from copper_scar.tools.copperhead import stage1 as s
from copper_scar.tools.copperhead.routing_options import candidate_options, context as routing_context
LOCAL=s.LOCAL;WORK=LOCAL/'policy-experiment';POLICIES=ROOT/'copper_scar/tools/copperhead/policies'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def cost(e,preserved=None):
 return dict(opens=e['unconnected'],physical_errors=e['errors'],warnings=e['warnings'],manufacturing_findings=e['manufacturing_findings_count'],pad_groups_preserved=preserved,invariants_ok=e['invariants_ok'],validity_gate=e['validity_gate'],airwire_distance_mm=e['search_cost']['total_missing_endpoint_distance_mm'])
def rank(policy,row):
 a=row['action'];topology=a['kind']=='local_topology_replan';distance=a.get('local_approach_mm',0)
 if policy['ranking']=='placement_then_endpoint':return (topology,distance,a['id'])
 if policy['ranking']=='split_burden_then_topology_then_endpoint':return (row['split_group_count'],row['introduced_islands'],not topology,distance,a['id'])
 raise ValueError('Unknown frozen ranking')
def winner(a,b):
 return 'island_first' if b['opens']<a['opens'] and not b['physical_errors'] and not b['manufacturing_findings'] and b['invariants_ok'] else 'placement_first'
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,required=True);ap.add_argument('--route-seconds',type=int,default=600);ap.add_argument('--decisions',type=int,default=3);ap.add_argument('--prepare-only',action='store_true');a=ap.parse_args()
 assert a.decisions==3 and a.route_seconds==600,'Frozen pilot protocol'
 WORK.mkdir(parents=True,exist_ok=True);lock=(WORK/'runner.lock').open('a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 assert not (WORK/'manifest.json').exists(),'Never overwrite an existing experiment'
 experiment='matched-policy-'+s.now().replace(':','').replace('+','-');events=WORK/'events.jsonl';seq=0
 def emit(kind,**kw):
  nonlocal seq
  seq+=1;row=dict(event_id=f'{experiment}:{seq}',timestamp_utc=s.now(),experiment_id=experiment,type=kind,**kw)
  with events.open('a') as f:f.write(json.dumps(row)+'\n');f.flush();os.fsync(f.fileno())
 def run(argv,folder,label,timeout=150):
  r=s.command([str(x) for x in argv],folder,label,timeout)
  if r['returncode']!=0:raise RuntimeError(f'{label}: {r}')
  return r
 revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
 paths=list((ROOT/'scripts').glob('copperhead_*.py'))+list((ROOT/'scripts/native').glob('Copperhead*.java'))+list((ROOT/'copper_scar/tools/copperhead').glob('*.py'))+list(POLICIES.glob('*.json'))
 hashes={str(p.relative_to(ROOT)):sha(p) for p in paths}
 protocol=dict(source_board_path=str(a.source/'pcbgolf.kicad_pcb'),source_board_sha256=sha(a.source/'pcbgolf.kicad_pcb'),source_support=s.support(a.source),source_commit=revision,implementation_hashes=hashes,router_jar_sha256=sha('/private/tmp/copper-router/freerouting-mount/freerouting.app/Contents/app/freerouting-executable.jar'),N=3,N_definition='Three policy decisions per arm; all library previews recorded; no-feasible-candidate decisions consume a step; at most one full route per step',max_route_seconds=600,max_decision_seconds=1100,order=['placement_first','island_first']*3,router_seed=None,seed_qualification='No exposed seed in installed RouterSettings; sequential ordering and one router thread, reproducibility not guaranteed',candidate_library='R123 translations (-2,.5),(-1,0),(-.5,0), and CAN2 x141 exact native island anchors; unavailable bindings explicitly recorded',shared_correctness='CAN2-only split-existing-junctions-v1; original600/300 and450/200 via eligibility; original rules and all copper layers; foreign collision ripup disabled',decision_rule='Only a strictly lower retained native missing-link count after exactly3 decisions keeps challenger; hard physical/manufacturing/invariant/original-pad-group gates; ties keep baseline. Time and distance secondary diagnostics only.',prior_discovery='Prior-informed single-board pilot. Both policies know previous R123 failed trials, CAN2 contact diagnosis and a 0.709s bounded CAN2 route that yielded44 native opens. That probe is excluded from initial board and not counted as fresh generalization. Manual discovery time is outside measured arm time and not precisely recorded.',qualification='Measured policy selection on one board; no statistical or general convergence claim; no engineering acceptance claim')
 policies=[]
 for name in ['placement_first','island_first']:
  p=POLICIES/(name+'.json');policies.append(dict(**json.loads(p.read_text()),source_commit=revision,source_path=str(p),source_sha256=sha(p)))
 common_options=json.loads((a.source/'routing-options.json').read_text());common_options['dsn_contact_normalization']=dict(version='split-existing-junctions-v1',nets=['CAN2_H']);protocol['realization_context']=routing_context(common_options['allowed_via_options'],s.design_digest(s.support(a.source)),common_options['dsn_contact_normalization']);protocol['topology_template_sha256']=sha(POLICIES/'anchor_template.json');protocol_hash=hashlib.sha256(json.dumps(protocol,sort_keys=True).encode()).hexdigest();manifest=dict(experiment_id=experiment,common_protocol=protocol,common_protocol_sha256=protocol_hash,policies=policies,status='preparing',created_at=s.now());s.write(WORK/'manifest.json',manifest)
 emit('experiment_started',common_protocol=protocol,common_protocol_sha256=protocol_hash)
 common=LOCAL/'candidates'/('policy-common-'+experiment);s.copy_project(a.source,common);native=WORK/'initial';native.mkdir();s.finalize_board(common,native);initial=s.evaluate(common,native,'saved',s.support(a.source),saved_board=True);assert initial['errors']==0 and initial['invariants_ok'] and initial['manufacturing_rules_clear']
 options=json.loads((common/'routing-options.json').read_text());options['dsn_contact_normalization']=dict(version='split-existing-junctions-v1',nets=['CAN2_H']);s.write(common/'routing-options.json',options)
 _,context=candidate_options(common,LOCAL,initial['constraint_scope'])
 # Both arms receive exactly the same saved-fill board and complete original support.
 manifest.update(status='prepared',common_board_path=str(common/'pcbgolf.kicad_pcb'),common_board_sha256=sha(common/'pcbgolf.kicad_pcb'),realization_context=context,initial_nativecost=cost(initial,True));s.write(WORK/'manifest.json',manifest)
 template=WORK/'topology-template.json';s.write(template,json.loads((POLICIES/'anchor_template.json').read_text()))
 arms={}
 for policy in policies:
  folder=WORK/policy['id'];folder.mkdir();parent=LOCAL/'candidates'/('policy-'+policy['id']+'-'+experiment);s.copy_project(common,parent)
  assert sha(parent/'pcbgolf.kicad_pcb')==manifest['common_board_sha256']
  arms[policy['id']]=dict(parent=parent,evaluation=initial,evaluation_path=native/'saved/evaluation.json',used=set(),elapsed=0,route_count=0,failed=False,history=[dict(elapsed_seconds=0,nativecost=cost(initial,True))])
  emit('policy_started',policy=policy,lower=dict(index=0,status='native_baseline_no_routing',nativecost=cost(initial,True),retainedbest=cost(initial,True),retained_board_path=str(parent/'pcbgolf.kicad_pcb'),retained_board_sha256=sha(parent/'pcbgolf.kicad_pcb'),elapsed_seconds=0),common_protocol_sha256=protocol_hash)
 if a.prepare_only:return
 manifest['status']='running';s.write(WORK/'manifest.json',manifest)
 for index in range(1,4):
  for policy in policies:
   assert all(sha(ROOT/p)==h for p,h in hashes.items()),'Frozen source changed during experiment'
   arm=arms[policy['id']];started=time.monotonic();parent=arm['parent'];folder=WORK/policy['id']/f'{index:02d}';folder.mkdir();s.DEADLINE=started+1100
   emit('lower_started',policy=policy,lower=dict(index=index,status='screening',input_board_path=str(parent/'pcbgolf.kicad_pcb'),input_board_sha256=sha(parent/'pcbgolf.kicad_pcb'),retainedbest=cost(arm['evaluation'],True)))
   rows=[];selected=None;record=None;error=None
   try:
    run([s.KIPY,ROOT/'scripts/copperhead_policy_candidates.py',parent,arm['evaluation_path'],template,folder/'library.json'],folder,'generate')
    library=json.loads((folder/'library.json').read_text());emit('candidate_library',policy=policy,lower=dict(index=index,library_path=str(folder/'library.json'),unavailable=library['unavailable']))
    for action in library['actions']:
     key=(sha(parent/'pcbgolf.kicad_pcb'),action['id'])
     if key in arm['used']:continue
     preview=folder/action['id'];preview.mkdir();project=preview/'project';s.copy_project(parent,project);action['realization_context_digest']=context['digest'];proposal=preview/'proposal.json';s.write(proposal,action)
     t=time.monotonic();row=dict(action=action,proposal_path=str(proposal),pre_board_path=str(project/'pcbgolf.kicad_pcb'),feasible=False,split_group_count=999999,introduced_islands=999999)
     try:
      script='copperhead_apply_pose.py' if action['kind']=='group_pose' else 'copperhead_topology_replan.py'
      run([s.KIPY,ROOT/'scripts'/script,project,'--proposal',proposal],preview,'apply')
      s.finalize_board(project,preview);e=s.evaluate(project,preview,'saved',s.support(parent),saved_board=True)
      run([s.KIPY,ROOT/'scripts/copperhead_pad_partitions.py','--before',parent/'pcbgolf.kicad_pcb','--after',project/'pcbgolf.kicad_pcb','--output',preview/'partitions.json'],preview,'partitions')
      proof=json.loads((preview/'partitions.json').read_text());row.update(nativecost=cost(e,proof['no_connected_pad_group_split']),split_group_count=len(proof['split_groups']),introduced_islands=max(0,len(proof['after']['groups'])-len(proof['before']['groups'])),feasible=e['errors']==0 and e['invariants_ok'] and e['manufacturing_rules_clear'],evaluation_path=str(preview/'saved/evaluation.json'),pre_board_sha256=sha(project/'pcbgolf.kicad_pcb'))
     except Exception as exc:row['error']=repr(exc)
     row.update(input_board_path=str(parent/'pcbgolf.kicad_pcb'),input_board_sha256=sha(parent/'pcbgolf.kicad_pcb'),preview_after_board_path=str(project/'pcbgolf.kicad_pcb'),preview_after_board_sha256=sha(project/'pcbgolf.kicad_pcb'),pre_board_semantics='After proposed update, before full routing');row['elapsed_seconds']=time.monotonic()-t;rows.append(row);emit('candidate_screened',policy=policy,lower=dict(index=index,**row))
    feasible=[r for r in rows if r['feasible']];pool=feasible or rows
    if not pool:raise RuntimeError('Finite untried library exhausted; counted unavailable decision')
    selected=min(pool,key=lambda r:rank(policy,r));action=selected['action'];arm['used'].add((sha(parent/'pcbgolf.kicad_pcb'),action['id']))
    emit('proposal_selected',policy=policy,lower=dict(index=index,action=action,feasible=selected['feasible'],ranking_key=list(rank(policy,selected)),screened_count=len(rows)))
    if selected['feasible']:
     proposal=LOCAL/'proposals'/f'{experiment}-{policy["id"]}-{index}.json';s.write(proposal,action);state_dir=WORK/policy['id']/'state'
     run([s.PYTHON,'-m','copper_scar.tools.copperhead.stage1','--source',parent,'--proposal',proposal,'--route-seconds','600','--budget','850','--state-dir',state_dir],folder,'lower',900)
     state=json.loads((state_dir/'state.json').read_text());receipt=Path(state['attempts'][-1])/'attempt.json';record=json.loads(receipt.read_text())
     if record.get('routing_scope',{}).get('execution'):arm['route_count']+=1
     if record.get('became_incumbent'):
      assert record['status']=='completed' and record['selection_decision']['no_connected_pad_group_split']
      assert not record['after']['errors'] and record['after']['manufacturing_rules_clear']
      arm.update(parent=Path(record['candidate']),evaluation=record['after'],evaluation_path=receipt.parent/'after/evaluation.json')
     result=dict(status=('completed_retained' if record.get('became_incumbent') else 'completed_rejected') if record['status']=='completed' else 'failed',attempt_id=record['attempt'],receipt_path=str(receipt),receipt_sha256=sha(receipt),nativecost=cost(record['after'],record.get('selection_decision',{}).get('no_connected_pad_group_split')) if record.get('after') else None,candidate_board_path=str(Path(record['candidate'])/'pcbgolf.kicad_pcb'),candidate_board_sha256=sha(Path(record['candidate'])/'pcbgolf.kicad_pcb'),pre_board_path=str(Path(record.get('placement_snapshot') or (receipt.parent/'topology-replan-project'))/'pcbgolf.kicad_pcb'),router=record.get('routing_scope'),retained=record.get('became_incumbent',False),selection_decision=record.get('selection_decision'),error=record.get('error'))
    else:result=dict(status='precheck_rejected',nativecost=selected.get('nativecost'),retained=False,pre_board_path=selected['pre_board_path'],pre_board_sha256=selected.get('pre_board_sha256'),error=selected.get('error'))
   except Exception as exc:
    error=repr(exc);result=dict(status='unavailable',retained=False,error=error,nativecost=None)
   elapsed=time.monotonic()-started;arm['elapsed']+=elapsed;arm['failed']=arm['failed'] or result['status'] in ('failed','unavailable');arm['history'].append(dict(elapsed_seconds=arm['elapsed'],nativecost=cost(arm['evaluation'],True)))
   lower=dict(index=index,**result,action=selected['action'] if selected else None,input_board_path=str(parent/'pcbgolf.kicad_pcb'),input_board_sha256=sha(parent/'pcbgolf.kicad_pcb'),elapsed_seconds=elapsed,cumulative_elapsed_seconds=arm['elapsed'],routed_dispatch_count=arm['route_count'],screened_count=len(rows),retainedbest=cost(arm['evaluation'],True),retained_board_path=str(arm['parent']/'pcbgolf.kicad_pcb'),retained_board_sha256=sha(arm['parent']/'pcbgolf.kicad_pcb'))
   s.write(folder/'result.json',lower);emit('lower_completed',policy=policy,lower=lower);s.DEADLINE=None
 for policy in policies:
  arm=arms[policy['id']];emit('policy_completed',policy=policy,lower=dict(index=3,retainedbest=cost(arm['evaluation'],True),cumulative_elapsed_seconds=arm['elapsed'],routed_dispatch_count=arm['route_count'],retained_board_path=str(arm['parent']/'pcbgolf.kicad_pcb'),retained_board_sha256=sha(arm['parent']/'pcbgolf.kicad_pcb')))
 base=arms['placement_first'];challenger=arms['island_first'];equal_time=min(base['elapsed'],challenger['elapsed']);equal={k:max((h for h in arm['history'] if h['elapsed_seconds']<=equal_time),key=lambda h:h['elapsed_seconds']) for k,arm in arms.items()}
 decision=dict(kept_policy='placement_first' if challenger['failed'] else winner(cost(base['evaluation']),cost(challenger['evaluation'])),criterion=protocol['decision_rule'],cost_at_N={k:cost(v['evaluation'],True) for k,v in arms.items()},equal_wall_time_seconds=equal_time,equal_wall_time_cost=equal,qualification=protocol['qualification']);selected_policy=next(p for p in policies if p['id']==decision['kept_policy']);next_hypothesis='Expand the shared native-bound action library to another disconnected net or reviewed component group; current native island preservation and candidate feasibility are the measured constraints. Evaluate in another matched pilot before accepting a policy change.';selection=dict(policy=selected_policy,decision_path=str(WORK/'decision.json'),selected_at=s.now(),next_hypothesis=next_hypothesis,next_trial_status='queued_not_executed',next_campaign_initial_board=str(arms[selected_policy['id']]['parent']/'pcbgolf.kicad_pcb'),qualification='Outcome-written policy configuration for the next campaign; next campaign has not run; policies agent-authored');s.write(WORK/'selected-policy.json',selection);decision.update(selected_policy_path=str(WORK/'selected-policy.json'),next_hypothesis=next_hypothesis,execution_failure_by_arm={k:v['failed'] for k,v in arms.items()});s.write(WORK/'decision.json',decision);emit('policy_decision',decision=decision);manifest.update(status='completed',finished_at=s.now(),decision=decision);s.write(WORK/'manifest.json',manifest)
if __name__=='__main__':main()
