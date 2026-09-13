"""Publish immutable whole-board evaluations, with remote deduplication and verification.

Authentication is read from a private file into process memory only. This is
historical evidence backfill, not a claim that native execution was live-traced.
"""
from pathlib import Path
import argparse, collections, fcntl, hashlib, json, os, subprocess, uuid, time
from datetime import datetime
ROOT=Path(__file__).resolve().parents[1];LOCAL=ROOT/'.local/copperhead'
PROJECT='philippe-fdesousa/copper-scar'

def unique_remote_rows(rows):
 # The history API can replay identical rows after resume. Never collapse
 # conflicting values, timestamps, media paths or step identities.
 seen=set();unique=[]
 for row in rows:
  key=json.dumps(row,sort_keys=True,separators=(',',':'))
  if key not in seen:seen.add(key);unique.append(row)
 return unique

def verify_repeated_publications(rows):
 """Allow repeated uploads only when every evidence value and image hash agrees.

 Keep all upload rows in receipts; only upload timing/step and content-addressed
 media paths may differ. Conflicting native results or images remain failures.
 """
 assert rows, 'Missing remote history row'
 def evidence(row):
  result={k:v for k,v in row.items() if k not in ('_step','_runtime','_timestamp')}
  for key in ('board/attempted','board/incumbent'):
   if key in result:
    assert result[key].get('sha256'), 'Remote media lacks content hash'
    result[key]={k:v for k,v in result[key].items() if k!='path'}
  return result
 expected=evidence(rows[0])
 assert all(evidence(row)==expected for row in rows), 'Conflicting repeated remote publication'
 return rows[0]

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--credential-file',type=Path,required=True);a=ap.parse_args()
 out=LOCAL/'observability';out.mkdir(exist_ok=True)
 lock=(out/'publish.lock').open('w');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 os.environ['WANDB_API_KEY']=a.credential_file.read_text().strip()
 os.environ['WANDB_SILENT']='true'
 os.environ['WANDB_CONSOLE']='off'
 import requests,wandb,weave
 from PIL import Image
 # Verify the intended destination before any write; no credential appears in URLs.
 response=requests.post('https://api.wandb.ai/graphql',auth=('api',os.environ['WANDB_API_KEY']),json={'query':'{ project(name:"copper-scar", entityName:"philippe-fdesousa") { name } }'},timeout=30)
 response.raise_for_status();assert response.json().get('data',{}).get('project'),'Intended project inaccessible'
 api=wandb.Api();client=weave.init(PROJECT)
 records=[];failures=[]
 for p in sorted((LOCAL/'runs').glob('stage1-*/attempt.json')):
  r=json.loads(p.read_text())
  if r.get('comparison_kind')=='routed_placement' and r.get('status')=='failed' and r.get('after'):failures.append((p,r))
  if r.get('comparison_kind') in ('initial_routed_placement','routed_placement') and r.get('routing_scope',{}).get('completion')=='routed_and_natively_evaluated' and r.get('finished_at') and r.get('after'):records.append((p,r))
 assert records,'No completed whole-board evaluations'
 groups=collections.defaultdict(list)
 for p,r in records:groups[(r['policy'],r['constraint_scope'])].append((p,r))
 report={'project':PROJECT,'mode':'historical immutable backfill','runs':[]}
 def preview(board,evaluation):
  digest=hashlib.sha256(board.read_bytes()).hexdigest();assert digest==evaluation['files']['pcbgolf.kicad_pcb'],'Board drift'
  directory=out/'boards'/digest;directory.mkdir(parents=True,exist_ok=True)
  if not (directory/'board.png').exists():
   subprocess.run(['/Users/philippe/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli','pcb','export','svg','--layers','F.Cu,B.Cu,F.SilkS,Edge.Cuts','--mode-single','--page-size-mode','2','--exclude-drawing-sheet','-o',str(directory/'board.svg'),str(board)],check=True,capture_output=True)
   subprocess.run(['/opt/homebrew/bin/rsvg-convert','-w','1600','-o',str(directory/'board.png'),str(directory/'board.svg')],check=True,capture_output=True)
  return directory/'board.png',digest
 for (policy,scope),items in groups.items():
  baseline=items[0][1]['before']['design_sha256'];run_id='ch-'+hashlib.sha256((policy+scope+baseline).encode()).hexdigest()[:16]
  run_path=PROJECT+'/'+run_id
  try:remote=api.run(run_path)
  except wandb.errors.CommError as exc:
   if 'Could not find run' not in str(exc) and 'not found' not in str(exc).lower():raise
   remote=None
  existing={x.get('attempt_id') for x in remote.scan_history()} if remote else set()
  # A successful prior readback is durable evidence of publication. If the API
  # temporarily omits that row, retry verification rather than uploading again.
  receipt=out/'verified.json'
  if receipt.exists():
   existing.update(row['attempt_id'] for rr in json.loads(receipt.read_text()).get('runs',[]) if rr['run_id']==run_id for row in rr.get('rows',[]))
  run=wandb.init(entity=PROJECT.split('/')[0],project=PROJECT.split('/')[1],id=run_id,resume='allow',name='Copperhead whole-board '+policy,group='copperhead-'+policy,job_type='native-feasibility',tags=['copperhead','whole-board','historical-backfill'],dir=str(out),config={'track':'copperhead','policy':policy,'baseline_hash':baseline,'constraint_scope':scope,'comparison':'completed placement plus whole-board routing','qualification':'No valid board; Stage2 locked','rule_note':'KiCad DSN export includes50um smd_smd exception; native acceptance uses unchanged original rules. No source-rule relaxation.'})
  run.define_metric('outer_index')
  for metric in ['loss/*','incumbent/*','native/*','board/*','routing/*']:run.define_metric(metric,step_metric='outer_index')
  entries=[];coverage_by_attempt={}
  for index,(path,r) in enumerate(items):
   e=r['after'];route=r['routing_scope'];execution=route.get('execution',{})
   incumbent=r.get('incumbent_after') or r.get('incumbent_before')
   ib=Path(incumbent['candidate'])/'pcbgolf.kicad_pcb'
   ir=next((json.loads(q.read_text()) for q in (LOCAL/'runs').glob('stage1-*/attempt.json') if json.loads(q.read_text()).get('candidate')==str(ib.parent)),None)
   ie=ir['after'] if ir else r['before'];attempt_png,attempt_hash=preview(Path(r['candidate'])/'pcbgolf.kicad_pcb',e);inc_png,inc_hash=preview(ib,ie)
   log=(Path(r['candidate'])/'router.log').read_text()
   termination='timeout' if execution.get('timeout') else 'router_returned; see native remaining pairs'
   if 'timed out' in log.lower() or 'timeout' in log.lower():termination='router effort limit; session imported and natively checked'
   subprocess.run([str(ROOT/'.venv/bin/python'),str(ROOT/'scripts/copperhead_route_evidence.py'),r['candidate']],check=True,capture_output=True)
   coverage=json.loads((Path(r['candidate'])/'routing-coverage.json').read_text());coverage_by_attempt[r['attempt']]=coverage
   metadata={'routing/exported_nets':coverage['exported_nets'],'routing/exported_pins':coverage['exported_assigned_pins'],'routing/exported_footprints':coverage['exported_footprints'],'routing/autoroute_started':coverage['autoroute_started'],'track':'copperhead','comparison_kind':r['comparison_kind'],'outer_index':index,'attempt_id':r['attempt'],'policy':policy,'baseline_hash':baseline,'loss/missing_pairs':e['unconnected'],'loss/physical_errors':e['errors'],'loss/warnings':e['warnings'],'incumbent/missing_pairs':ie['unconnected'],'incumbent/physical_errors':ie['errors'],'incumbent/warnings':ie['warnings'],'native/invariants_ok':e['invariants_ok'],'validity_gate':False,'retained':r.get('became_incumbent',False),'routing/scope':'whole_board','routing/elapsed_s':execution.get('elapsed_seconds'),'routing/termination':termination,'routing/effort_limit_s':route['effort_limit_seconds'],'routing/pass_limit':route['pass_limit'],'routing/net_filter':'none','routing/via_count_limit':'none','board/attempted_sha256':attempt_hash,'board/incumbent_sha256':inc_hash,'native/started_at':r['started_at'],'native/finished_at':r['finished_at']}
   if r['attempt'] not in existing:run.log({**metadata,'board/attempted':wandb.Image(str(attempt_png),caption=r['attempt']+'; '+str(e['unconnected'])+' missing; PARTIAL'),'board/incumbent':wandb.Image(str(inc_png),caption='Retained '+str(ie['unconnected'])+' missing; PARTIAL')})
   # Stable call identity + read-before-create permits retries after uncertain writes.
   call_id=str(uuid.uuid5(uuid.NAMESPACE_URL,'copperhead://'+run_id+'/'+r['attempt']))
   found=list(client.get_calls(filter={'call_ids':[call_id]},limit=1))
   if not found:
    call=client.create_call('copperhead.outer.native_evaluation_backfill',inputs={'attempt_id':r['attempt'],'placement':r.get('placement_delta'),'routing_scope':route,'routing_coverage':coverage,'baseline_hash':baseline,'evidence_sha256':hashlib.sha256(path.read_bytes()).hexdigest()},attributes={'track':'copperhead','policy':policy,'comparison_kind':r['comparison_kind'],'wb_run_id':run_id,'historical_backfill':True},display_name='Copperhead outer '+str(index)+' '+r['attempt'],_call_id_override=call_id,started_at=datetime.fromisoformat(r['started_at']))
    client.finish_call(call,output={**metadata,'attempted_board':Image.open(attempt_png),'incumbent_board':Image.open(inc_png)},ended_at=datetime.fromisoformat(r['finished_at']))
   entries.append({'attempt_id':r['attempt'],'outer_index':index,'call_id':call_id,'call_url':'https://wandb.ai/'+PROJECT+'/r/call/'+call_id,'board_sha256':attempt_hash})
  failure_entries=[]
  for path,r in failures:
   if (r['policy'],r['constraint_scope'])!=(policy,scope):continue
   e=r['after'];png,digest=preview(Path(r['candidate'])/'pcbgolf.kicad_pcb',e)
   subprocess.run([str(ROOT/'.venv/bin/python'),str(ROOT/'scripts/copperhead_route_evidence.py'),r['candidate']],check=True,capture_output=True)
   coverage=json.loads((Path(r['candidate'])/'routing-coverage.json').read_text());coverage_by_attempt[r['attempt']]=coverage
   item={'attempt_id':r['attempt'],'comparison_kind':'failed_outer_attempt','error':r['error'],'missing_pairs':e['unconnected'],'physical_errors':e['errors'],'warnings':e['warnings'],'invariants_ok':e['invariants_ok'],'retained':False,'board_sha256':digest,'routing_coverage':coverage}
   run.summary['failed_board/'+r['attempt']]=wandb.Image(str(png),caption='Failed routing; preserved placement, not a completed routing point')
   call_id=str(uuid.uuid5(uuid.NAMESPACE_URL,'copperhead://'+run_id+'/'+r['attempt']))
   if not list(client.get_calls(filter={'call_ids':[call_id]},limit=1)):
    call=client.create_call('copperhead.outer.failed_evaluation_backfill',inputs={'attempt_id':r['attempt'],'routing_scope':r['routing_scope'],'original_started_at':r['started_at']},attributes={'track':'copperhead','policy':policy,'historical_backfill':True,'comparison_kind':'failed_outer_attempt'},_call_id_override=call_id,started_at=datetime.fromisoformat(r['started_at']))
    client.finish_call(call,output=item,exception=RuntimeError(r['error']),ended_at=datetime.fromisoformat(r['finished_at']))
   failure_entries.append({**item,'call_id':call_id})
  run.summary['failed_outer_attempts']=failure_entries
  run.summary['routing_coverage_by_attempt']=coverage_by_attempt
  run.finish();client.flush()
  # Read back actual remote rows/media/calls. A successful local SDK exit is insufficient.
  for retry in range(6):
   api.flush();remote=api.run(run_path);raw_history=list(remote.scan_history());history=unique_remote_rows(raw_history)
   if all(any(h.get('attempt_id')==entry['attempt_id'] for h in history) for entry in entries):break
   time.sleep(2)
  files=[f.name for f in remote.files()];verified=[]
  for entry in entries:
   matches=[h for h in history if h.get('attempt_id')==entry['attempt_id']]
   row=verify_repeated_publications(matches);assert row['board/attempted_sha256']==entry['board_sha256']
   for upload in matches:
    for media in ['board/attempted','board/incumbent']:
     image_path=upload[media]['path'];assert image_path in files,'Remote image file missing'
   calls=list(client.get_calls(filter={'call_ids':[entry['call_id']]},limit=2));assert len(calls)==1 and calls[0].ended_at,'Missing remote finished Weave call'
   verified.append({**entry,'missing_pairs':row['loss/missing_pairs'],'physical_errors':row['loss/physical_errors'],'warnings':row['loss/warnings'],'media_verified':True,'weave_verified':True,'publication_rows':[{'step':u.get('_step'),'attempted_media':u['board/attempted'],'incumbent_media':u['board/incumbent']} for u in matches],'repeated_publications':len(matches)-1})
  for entry in failure_entries:
   calls=list(client.get_calls(filter={'call_ids':[entry['call_id']]},limit=2));assert len(calls)==1 and calls[0].ended_at
  assert len(remote.summary.get('failed_outer_attempts',[]))==len(failure_entries)
  report['runs'].append({'failed_outer_attempts':failure_entries,'run_id':run_id,'url':'https://wandb.ai/'+PROJECT+'/runs/'+run_id,'rows':verified,'history_rows':len(history),'raw_history_rows':len(raw_history),'identical_remote_duplicates':len(raw_history)-len(history)})
 (out/'verified.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
if __name__=='__main__':main()
