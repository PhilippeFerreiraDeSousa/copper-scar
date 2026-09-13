"""Incremental verified publication of completed continuation events, never frozen rewrites."""
from pathlib import Path
import argparse,hashlib,json,os,uuid
ap=argparse.ArgumentParser();ap.add_argument('base',type=Path);ap.add_argument('--credential-file',type=Path,required=True);a=ap.parse_args();base=a.base.resolve();root=base/'stage2';out=root/'continuation-observability';out.mkdir(exist_ok=True);os.environ['WANDB_API_KEY']=a.credential_file.read_text().strip();os.environ['WANDB_SILENT']='true';os.environ['WANDB_CONSOLE']='off'
import wandb,weave
project='philippe-fdesousa/copper-scar';rid='medium-stage2-continuation-20260913';api=wandb.Api();client=weave.init(project);frozen=json.loads((root/'final-accepted/frozen.json').read_text());initial=frozen['score'];events=[]
for p in root.glob('*/events.json'):
 events += [e for e in json.loads(p.read_text()) if e['started_at']>frozen['frozen_at']]
events.sort(key=lambda e:e['finished_at']);assert events
try:remote=api.run(project+'/'+rid);existing={r.get('event_id') for r in remote.scan_history()}
except wandb.errors.CommError as exc:
 if 'not found' not in str(exc).lower() and 'could not find' not in str(exc).lower():raise
 existing=set()
run=wandb.init(entity='philippe-fdesousa',project='copper-scar',id=rid,resume='allow',name='medium-loop · continuing official-score optimization',job_type='native-continuation-evidence',dir=str(out),config={'size_family':'medium-loop','stage':2,'frozen_noon_parent_sha256':initial['board_sha256'],'frozen_noon_score':initial['official_formula_score'],'llm_calls':0});global_score=initial['official_formula_score'];best=root/'final-accepted';rows=[]
for step,e in enumerate(events,1):
 f=Path(e['folder']);r=e['result'];assert hashlib.sha256((f/'pcbgolf.kicad_pcb').read_bytes()).hexdigest()==r['board_sha256'];eid=hashlib.sha256((str(f)+r['board_sha256']).encode()).hexdigest()[:24];cid=str(uuid.uuid5(uuid.NAMESPACE_URL,rid+'/'+eid))
 if r['valid'] and r['official_formula_score']<global_score:global_score=r['official_formula_score'];best=f
 if eid not in existing:
  action=e['action'];caption=f"{f.parent.name}/{f.name}: {action.get('kind',action.get('primitive','proposal'))}; valid={r['valid']}; score={r['official_formula_score']}";row={'decision':step,'event_id':eid,'official/incumbent_score':global_score,'native/valid':r['valid'],'native/opens':r['native']['opens'],'native/violations':r['native']['violations'],'native/parity':r['native']['parity_findings'],'native/erc':r['native']['erc_findings'],'quality/vias':r['terms']['via_count'],'quality/assembly_volume_mm3':r['terms']['pcba_bbox_volume_mm3'],'action_summary':caption,'action':json.dumps(action),'board_sha256':r['board_sha256'],'board':wandb.Image(str(f/'board.png'),caption=caption),'source_sha':e['source_sha'],'router/elapsed_seconds':sum(c['elapsed_seconds'] for c in e['commands'] if any(str(v).endswith('copperhead_route.py') for v in c['command']))}
  if r['valid']:row['official/valid_attempt_score']=r['official_formula_score']
  run.log(row)
 if not list(client.get_calls(filter={'call_ids':[cid]},limit=1)):
  call=client.create_call('copper_scar.medium_loop.continuation_native_evidence',inputs={'action':e['action'],'commands':e['commands'],'source_sha':e['source_sha'],'result':r,'router_log':(f/'router.log').read_text() if (f/'router.log').exists() else None},attributes={'wb_run_id':rid,'llm_involved':False,'historical_completed_evidence':True},_call_id_override=cid);client.finish_call(call,output={'result':r,'global_incumbent_score':global_score})
 rows.append({'event_id':eid,'decision':step,'board_sha256':r['board_sha256'],'incumbent_score':global_score,'call_id':cid})
artifact=wandb.Artifact('medium-loop-continuation-evidence',type='native-board-evidence',metadata={'best_score':global_score,'best_board_sha256':json.loads((best/'score.json').read_text())['board_sha256']})
for e in events:
 f=Path(e['folder']);prefix=str(f.relative_to(root))
 for name in ['event.json','completed.json','proposal.json','score.json','pcbgolf.kicad_pcb','preview.kicad_pcb','drc.json','erc.json','native-audit.json','acceptance.json','preflight.json','execution.json','router.log','board.png']:
  if (f/name).exists():artifact.add_file(str(f/name),name=prefix+'/'+name)
for name in ['pcbgolf.kicad_pcb','pcbgolf.kicad_pro','pcbgolf.kicad_sch','pcbgolf.kicad_sym','fp-lib-table','sym-lib-table']:artifact.add_file(str(best/name),name='best-project/'+name)
for name in ['models','pcbgolf.pretty','pcbgolf.3dshapes']:artifact.add_dir(str(best/name),name='best-project/'+name)
for p in root.glob('primitive-policy-*/outcome.json'):artifact.add_file(str(p),name=str(p.relative_to(root)))
run.log_artifact(artifact);run.summary.update({'best_valid_score':global_score,'best_candidate':str(best),'frozen_noon_score':initial['official_formula_score'],'frozen_noon_unchanged':True,'completed_events':len(events),'controller_status':'continuing; live operation status is separate from completed score points'});url=run.url;run.finish();history=list(api.run(project+'/'+rid).scan_history())
for row in rows:
 matches=[r for r in history if r.get('event_id')==row['event_id']];assert matches and all(r['official/incumbent_score']==row['incumbent_score'] and r['board_sha256']==row['board_sha256'] for r in matches);assert any(r.get('board',{}).get('sha256') for r in matches);calls=list(client.get_calls(filter={'call_ids':[row['call_id']]},limit=2));assert len(calls)==1 and calls[0].ended_at
receipt={'url':url,'verified_rows':rows,'best_score':global_score,'best_candidate':str(best),'frozen_noon_unchanged':True};(out/'verified.json').write_text(json.dumps(receipt,indent=2));print(json.dumps(receipt))
