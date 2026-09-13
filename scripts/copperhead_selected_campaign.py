"""Consume a completed higher-loop policy decision and execute one next update.

The new R89 catalog is a queued diagnostic follow-up, outside the matched pilot.
"""
import argparse, hashlib, json, subprocess, sys, time
from datetime import datetime
from pathlib import Path

def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def verify_selection(selection_path,root):
 selection=json.loads(selection_path.read_text());policy=selection['policy'];source=Path(policy['source_path']).resolve();relative=source.relative_to(root)
 assert digest(source)==policy['source_sha256'],'Selected policy bytes changed'
 committed=subprocess.check_output(['git','show',policy['source_commit']+':'+str(relative)],cwd=root)
 assert hashlib.sha256(committed).hexdigest()==policy['source_sha256'],'Selected policy differs from its commit'
 config=json.loads(source.read_text());assert all(policy.get(k)==v for k,v in config.items()),'Selected configuration differs from committed policy'
 decision_path=Path(selection['decision_path']);decision=json.loads(decision_path.read_text());assert decision['kept_policy']==policy['id']
 manifest=json.loads((selection_path.parent/'manifest.json').read_text());assert manifest['status']=='completed' and manifest['decision']==decision
 events=[json.loads(line) for line in (selection_path.parent/'events.jsonl').read_text().splitlines()]
 protocol=manifest['common_protocol'];assert protocol['N']==3
 assert hashlib.sha256(json.dumps(protocol,sort_keys=True).encode()).hexdigest()==manifest['common_protocol_sha256'],'Protocol hash mismatch'
 assert {e['experiment_id'] for e in events}=={manifest['experiment_id']},'Mixed experiment events'
 starts=[e for e in events if e['type']=='experiment_started'];assert len(starts)==1 and starts[0]['common_protocol']==protocol and starts[0]['common_protocol_sha256']==manifest['common_protocol_sha256']
 assert {p['id'] for p in manifest['policies']}=={'placement_first','island_first'}
 for arm in manifest['policies']:
  done=[e for e in events if e['type']=='lower_completed' and e['policy']['id']==arm['id']]
  assert sorted(e['lower']['index'] for e in done)==[1,2,3],'Incomplete or duplicate N3 decisions'
  endings=[e for e in events if e['type']=='policy_completed' and e['policy']['id']==arm['id']]
  assert len(endings)==1 and endings[0]['lower']['index']==3,'Incomplete policy completion'
  assert all(e['policy']==arm for e in events if e.get('policy',{}).get('id')==arm['id']),'Policy metadata drift'
 completed=[e for e in events if e['type']=='policy_completed' and e['policy']['id']==policy['id']];assert len(completed)==1
 decisions=[e['decision'] for e in events if e['type']=='policy_decision'];assert len(decisions)==1 and decisions[0]==decision,'Decision file differs from append-only outcome';last=completed[0]['lower'];board=Path(selection['next_campaign_initial_board']).resolve();assert board==Path(last['retained_board_path']).resolve() and digest(board)==last['retained_board_sha256']
 return selection,decision,board,dict(selection_path=str(selection_path),selection_sha256=digest(selection_path),decision_path=str(decision_path),decision_sha256=digest(decision_path),policy_id=policy['id'],policy_version=policy['version'],policy_source_commit=policy['source_commit'],policy_source_sha256=policy['source_sha256'],input_board_path=str(board),input_board_sha256=digest(board),verified=True)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--selection',type=Path,required=True);ap.add_argument('--deadline',required=True);a=ap.parse_args();root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
 from copper_scar.tools.copperhead import stage1 as s
 from copperhead_policy_experiment import rank,cost
 from copper_scar.tools.copperhead.routing_options import candidate_options
 selection_path=a.selection.resolve();selection,decision,board,receipt=verify_selection(selection_path,root)
 folder=selection_path.parent/'next-campaign';folder.mkdir(exist_ok=False);start=time.monotonic();deadline=datetime.fromisoformat(a.deadline).timestamp();s.DEADLINE=time.monotonic()+max(0,deadline-time.time());policy=selection['policy'];parent=board.parent
 events=[json.loads(line) for line in (selection_path.parent/'events.jsonl').read_text().splitlines()];failures=[dict(event_id=e['event_id'],attempt_id=e['lower'].get('attempt_id'),receipt_path=e['lower'].get('receipt_path'),receipt_sha256=e['lower'].get('receipt_sha256')) for e in events if e['type']=='lower_completed' and 'R123' in (e['lower'].get('action') or {}).get('refs',[]) and (e['lower'].get('selection_decision') or {}).get('no_connected_pad_group_split') is False];assert failures,'R89 follow-up requires measured R123 restoration failures';receipt['diagnostic_evidence']=failures
 receipt.update(consumed_at=s.now(),consumer_source_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),consumer_sha256=digest(__file__),candidate_generator_sha256=digest(root/'scripts/copperhead_selected_candidates.py'),next_catalog='r89-native-bound-v1',next_hypothesis='Measured R123 restoration burden motivates another known disconnected resistor endpoint: R89 to LED13. Reuse the selected ranking on native-screened R89 pose candidates; original rules and all-layer realization unchanged.',qualification='Actual selected-policy consumer, one new lower decision; outside matched policy comparison')
 s.write(folder/'consumed-decision.json',receipt)
 try:
  def run(argv,where,label,timeout=150):
   r=s.command([str(x) for x in argv],where,label,timeout)
   if r['returncode']!=0:raise RuntimeError(f'{label}: {r}')
   return r
  evaluation=s.evaluate(parent,folder,'input-saved',s.support(parent),saved_board=True);assert digest(board)==receipt['input_board_sha256'] and evaluation['invariants_ok'] and not evaluation['errors'];assert any(v['type']=='unconnected_items' and any(' of R89 on ' in i.get('description','') for i in v.get('items',[])) for v in evaluation['violations']),'No current missing endpoint on R89'
  _,context=candidate_options(parent,s.LOCAL,evaluation['constraint_scope']);template=root/'copper_scar/tools/copperhead/policies/anchor_template.json'
  run([s.KIPY,root/'scripts/copperhead_selected_candidates.py',parent,folder/'input-saved/evaluation.json',template,folder/'library.json'],folder,'generate')
  rows=[]
  for action in json.loads((folder/'library.json').read_text())['actions']:
   preview=folder/action['id'];preview.mkdir();project=preview/'project';s.copy_project(parent,project);action['realization_context_digest']=context['digest'];proposal=preview/'proposal.json';s.write(proposal,action)
   row=dict(action=action,proposal_path=str(proposal),feasible=False,split_group_count=999999,introduced_islands=999999)
   try:
    script='copperhead_apply_pose.py' if action['kind']=='group_pose' else 'copperhead_topology_replan.py'
    run([s.KIPY,root/'scripts'/script,project,'--proposal',proposal],preview,'apply');s.finalize_board(project,preview);e=s.evaluate(project,preview,'saved',s.support(parent),saved_board=True)
    run([s.KIPY,root/'scripts/copperhead_pad_partitions.py','--before',board,'--after',project/'pcbgolf.kicad_pcb','--output',preview/'partitions.json'],preview,'partitions')
    proof=json.loads((preview/'partitions.json').read_text());row.update(nativecost=cost(e,proof['no_connected_pad_group_split']),split_group_count=len(proof['split_groups']),introduced_islands=max(0,len(proof['after']['groups'])-len(proof['before']['groups'])),feasible=not e['errors'] and e['invariants_ok'] and e['manufacturing_rules_clear'])
   except Exception as exc:row['error']=repr(exc)
   row.update(input_board_path=str(board),input_board_sha256=digest(board),preview_after_board_path=str(project/'pcbgolf.kicad_pcb'),preview_after_board_sha256=digest(project/'pcbgolf.kicad_pcb'));rows.append(row);s.write(folder/'screens.json',rows)
  feasible=[r for r in rows if r['feasible']];selected=min(feasible or rows,key=lambda r:rank(policy,r)) if rows else None
  result=dict(policy=policy,consumed_decision=str(folder/'consumed-decision.json'),input_board_path=str(board),input_board_sha256=digest(board),selected=selected,screened_count=len(rows),retained=False,status='precheck_rejected',qualification='Next campaign decision only; not part of the matched comparison')
  if selected and selected['feasible']:
   proposal=s.LOCAL/'proposals'/('selected-policy-next-'+str(int(time.time()))+'.json');s.write(proposal,selected['action']);result['proposal_path']=str(proposal)
   if time.time()+780>deadline:result['status']='queued_no_time_for_full_route'
   else:
    run([s.PYTHON,'-m','copper_scar.tools.copperhead.stage1','--source',parent,'--proposal',proposal,'--route-seconds','600','--budget','780','--state-dir',folder/'state'],folder,'lower',810)
    state=json.loads((folder/'state/state.json').read_text());path=Path(state['attempts'][-1])/'attempt.json';r=json.loads(path.read_text());result.update(status=r['status'],retained=r.get('became_incumbent',False),attempt_id=r['attempt'],receipt_path=str(path),receipt_sha256=digest(path),nativecost=cost(r['after'],r.get('selection_decision',{}).get('no_connected_pad_group_split')) if r.get('after') else None,error=r.get('error'))
  result.update(elapsed_seconds=time.monotonic()-start,finished_at=s.now());s.write(folder/'result.json',result);receipt.update(consumer_status=result['status'],result_path=str(folder/'result.json'));s.write(folder/'consumed-decision.json',receipt);print(json.dumps(result,indent=2))
 except Exception as exc:
  failure=dict(status='failed',error=repr(exc),retained=False,finished_at=s.now(),elapsed_seconds=time.monotonic()-start,consumed_decision=str(folder/'consumed-decision.json'),input_board_path=str(board),input_board_sha256=digest(board) if board.exists() else None,qualification='Failed next lower step; never a completed or retained result')
  statepath=folder/'state/state.json'
  if statepath.exists():
   state=json.loads(statepath.read_text())
   if state.get('attempts'):
    attempt=Path(state['attempts'][-1])/'attempt.json';native=json.loads(attempt.read_text());failure.update(receipt_path=str(attempt),receipt_sha256=digest(attempt),native_status=native['status'],nativecost=cost(native['after'],native.get('selection_decision',{}).get('no_connected_pad_group_split')) if native.get('after') else None)
  s.write(folder/'result.json',failure);receipt.update(consumer_status='failed',result_path=str(folder/'result.json'),error=repr(exc));s.write(folder/'consumed-decision.json',receipt);raise

if __name__=='__main__':main()
