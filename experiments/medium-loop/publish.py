"""Publish verified native evidence; deterministic history, never fabricated LLM spans."""
from pathlib import Path
import argparse,hashlib,json,os,uuid
ap=argparse.ArgumentParser();ap.add_argument('base',type=Path);ap.add_argument('--credential-file',type=Path,required=True);a=ap.parse_args();base=a.base.resolve();out=base/'observability';out.mkdir(exist_ok=True)
os.environ['WANDB_API_KEY']=a.credential_file.read_text().strip();os.environ['WANDB_SILENT']='true';os.environ['WANDB_CONSOLE']='off'
import requests,wandb,weave
project='philippe-fdesousa/copper-scar';response=requests.post('https://api.wandb.ai/graphql',auth=('api',os.environ['WANDB_API_KEY']),json={'query':'{project(name:"copper-scar",entityName:"philippe-fdesousa"){name}}'},timeout=30);response.raise_for_status();assert response.json().get('data',{}).get('project')
client=weave.init(project);api=wandb.Api();receipt={'project':project,'mode':'historical deterministic native evidence backfill','llm_calls':0,'runs':[]};initial=json.loads((base/'baseline-parity/completed.json').read_text());groups={'diagnostic-placement':[initial,json.loads((base/'relay-group-01/completed.json').read_text())]};protocol=json.loads((base/'policy-pilot/protocol.json').read_text());outcome=json.loads((base/'policy-pilot/outcome.json').read_text())
for policy in protocol['policies']:groups[policy]=[initial]+[json.loads((base/'policy-pilot'/f'{policy}-{i}'/'completed.json').read_text()) for i in (1,2)]
for arm,records in groups.items():
 rid='medium-'+hashlib.sha256((initial['after']['board_sha256']+arm).encode()).hexdigest()[:15];run=wandb.init(entity='philippe-fdesousa',project='copper-scar',id=rid,resume='allow',name='medium-loop · '+arm,group='medium-pcb-loop-85',job_type='native-placement-evaluation',tags=['medium-circuit','native-validated','historical-backfill','no-llm'],config={'protocol':protocol,'outcome':outcome,'arm':arm,'input_components':85,'input_nets':67},dir=str(out));rows=[]
 for step,item in enumerate(records):
  f=Path(item['folder']);e=item['after'];assert hashlib.sha256((f/'pcbgolf.kicad_pcb').read_bytes()).hexdigest()==e['board_sha256'];summary=json.dumps(item['action'],ensure_ascii=False);router=next((c['elapsed_seconds'] for c in item['commands'] if any(str(v).endswith('/copperhead_route.py') for v in c['command'])),0);row={'decision':step,'native/cost':e['feasibility_cost'],'native/opens':e['native_open_count'],'native/drc_violations':e['all_drc_violations'],'native/schematic_parity':e['schematic_parity_issues'],'native/accepted':e['accepted'],'quality/wire_length_mm':e['wire_length_mm'],'quality/vias':e['vias'],'router/elapsed_seconds':router,'action_summary':summary,'retained':item['retained'],'board_sha256':e['board_sha256'],'board':wandb.Image(str(f/'board.png'),caption=summary),'source_sha':item['source_sha']};run.log(row)
  cid=str(uuid.uuid5(uuid.NAMESPACE_URL,'medium-loop/'+rid+'/'+str(step)))
  if not list(client.get_calls(filter={'call_ids':[cid]},limit=1)):
   call=client.create_call('copper_scar.medium_loop.deterministic_native_evidence',inputs={'action':item['action'],'commands':item['commands'],'source_sha':item['source_sha'],'router_log':(f/'router.log').read_text(),'native_evaluation':e,'protocol':protocol},attributes={'wb_run_id':rid,'kind':'historical_evidence_backfill','llm_involved':False},_call_id_override=cid);client.finish_call(call,output={'evaluation':e,'retained':item['retained']})
  rows.append({'decision':step,'cost':e['feasibility_cost'],'board_sha256':e['board_sha256'],'call_id':cid})
 artifact=wandb.Artifact('medium-loop-'+arm+'-evidence',type='native-board-evidence',metadata={'components':85,'nets':67,'deterministic':True})
 for item in records:
  f=Path(item['folder'])
  for name in ['pcbgolf.kicad_pcb','pcbgolf.kicad_pro','pcbgolf.kicad_sch','preview.kicad_pcb','completed.json','native-audit.json','acceptance.json','drc.json','erc.json','preflight.json','router.log','execution.json','pcbgolf.dsn','pcbgolf.ses','board.png']:
   if (f/name).exists():artifact.add_file(str(f/name),name=f.name+'/'+name)
 for name in ['protocol.json','outcome.json']:artifact.add_file(str(base/'policy-pilot'/name),name=name)
 if arm=='diagnostic-placement':artifact.add_dir(str(base/'accepted-handoff'),name='accepted-handoff')
 run.log_artifact(artifact);run.summary.update({'native_initial_opens':1,'native_final_opens':records[-1]['after']['native_open_count'],'policy_win':False,'qualification':'Single previously observed board; physical native checks pass. Hardware untested. No original challenge submission.'});url=run.url;run.finish();remote=api.run(project+'/'+rid);history=list(remote.scan_history())
 for row in rows:
  matches=[r for r in history if r.get('decision')==row['decision'] and r.get('board_sha256')==row['board_sha256']];assert matches and all(r['native/cost']==row['cost'] for r in matches);assert any(r.get('board',{}).get('sha256') for r in matches);calls=list(client.get_calls(filter={'call_ids':[row['call_id']]},limit=2));assert len(calls)==1 and calls[0].ended_at
 receipt['runs'].append({'id':rid,'url':url,'verified_rows':rows,'artifact':artifact.name});(out/'verified.json').write_text(json.dumps(receipt,indent=2));print(url,flush=True)
