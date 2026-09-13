"""Publish real deterministic experiment evidence, explicitly as historical backfill."""
from pathlib import Path
import argparse,hashlib,json,os,uuid

def main():
 ap=argparse.ArgumentParser();ap.add_argument('base',type=Path);ap.add_argument('--credential-file',type=Path,required=True);a=ap.parse_args();base=a.base.resolve();c=base/'campaign';out=base/'observability';out.mkdir(exist_ok=True)
 os.environ['WANDB_API_KEY']=a.credential_file.read_text().strip();os.environ['WANDB_SILENT']='true';os.environ['WANDB_CONSOLE']='off'
 import requests,wandb,weave
 project='philippe-fdesousa/copper-scar';r=requests.post('https://api.wandb.ai/graphql',auth=('api',os.environ['WANDB_API_KEY']),json={'query':'{project(name:"copper-scar",entityName:"philippe-fdesousa"){name}}'},timeout=30);r.raise_for_status();assert r.json().get('data',{}).get('project')
 client=weave.init(project);api=wandb.Api();records=json.loads((c/'records.json').read_text());protocol=json.loads((c/'protocol.json').read_text());decision=json.loads((c/'higher-loop-decision.json').read_text());receipt={'project':project,'mode':'historical deterministic execution evidence; no LLM calls','runs':[]}
 groups={arm:[v for v in records if v['arm']==arm] for arm in ['all-net-hpwl','signal-net-hpwl']}
 for arm in groups:
  first=dict(records[0]);first['arm']=arm;first['retained_cost']=first['after']['feasibility_cost'];first['retained_wire_mm']=first['after']['wire_length_mm'];groups[arm].insert(0,first)
 groups['explicit-topology']=[]
 for step,name in enumerate(['topology-trial','topology-two-ended'],1):
  f=base/name;groups['explicit-topology'].append({'arm':'explicit-topology','step':step,'folder':str(f),'action':json.loads((f/'topology-proposal.json').read_text()),'after':json.loads((f/'acceptance.json').read_text()),'retain':False,'source_sha':'f46c40c' if step==1 else '1608f8d','qualification':'Separate topology follow-up. First rejected for dangling copper; revised board feasible but rejected for longer wire.'})
 for arm,items in groups.items():
  rid='small-'+hashlib.sha256((protocol['source_sha']+arm).encode()).hexdigest()[:15];run=wandb.init(entity='philippe-fdesousa',project='copper-scar',id=rid,resume='allow',name='Small PCB Loop · '+arm,group='small-pcb-loop-baedc40',job_type='native-placement-research',tags=['small-circuit','native-checked','deterministic','historical-backfill'],config={'protocol':protocol,'higher_loop_decision':decision,'arm':arm},dir=str(out))
  run.define_metric('decision');run.define_metric('native/*',step_metric='decision');run.define_metric('quality/*',step_metric='decision');rows=[]
  for item in items:
   f=Path(item['folder']);e=item['after'];png=base/'replay'/(f.name+'.png');summary=('Routing-only control' if item['step']==0 else json.dumps(item['action'],ensure_ascii=False));row={'decision':item['step'],'native/cost':e['feasibility_cost'],'native/opens':e['drc_opens'],'native/violations':e['all_drc_violations'],'native/accepted':e['accepted'],'native/retained_cost':item.get('retained_cost',e['feasibility_cost']),'quality/wire_length_mm':e['wire_length_mm'],'quality/vias':e['vias'],'quality/retained_wire_mm':item.get('retained_wire_mm',e['wire_length_mm']),'action_summary':summary,'retained':item.get('retain',False),'board_sha256':e['board_sha256'],'board':wandb.Image(str(png),caption=summary),'source_sha':item['source_sha']};run.log(row)
   cid=str(uuid.uuid5(uuid.NAMESPACE_URL,'small-loop/'+rid+'/'+str(item['step'])))
   if not list(client.get_calls(filter={'call_ids':[cid]},limit=1)):
    call=client.create_call('copper_scar.small_loop.deterministic_evidence_backfill',inputs={'action':item['action'],'recorded_commands':item.get('commands',[]),'source_sha':item['source_sha'],'router_log':(f/'router.log').read_text() if (f/'router.log').exists() else None,'protocol':protocol,'native_acceptance':e},attributes={'wb_run_id':rid,'kind':'historical_evidence_backfill','llm_involved':False},_call_id_override=cid)
    client.finish_call(call,output={'acceptance':e,'retained':item.get('retain',False),'topology_verification':json.loads((f/'topology-verification.json').read_text()) if (f/'topology-verification.json').exists() else None})
   rows.append({'decision':item['step'],'cost':e['feasibility_cost'],'board_sha256':e['board_sha256'],'call_id':cid})
  artifact=wandb.Artifact('small-loop-'+arm+'-evidence',type='native-board-evidence',metadata={'source_sha':protocol['source_sha'],'deterministic':True})
  for f in [c/'protocol.json',c/'higher-loop-decision.json',base/'jitx-parity-audit.json']:artifact.add_file(str(f),name=f.name)
  for item in items:
   f=Path(item['folder'])
   for name in ['pcbgolf.kicad_pcb','pcbgolf.kicad_pro','preview.kicad_pcb','native-audit.json','acceptance.json','drc.json','preflight.json','router.log','execution.json','decision.json','topology-proposal.json','topology-verification.json','pcbgolf.dsn','pcbgolf.ses']:
    if (f/name).exists():artifact.add_file(str(f/name),name=f.name+'/'+name)
  run.log_artifact(artifact);run.summary.update({'higher_loop_selected':'all-net-hpwl','policy_win':False,'sample_size_boards':1,'routing_only_initial_opens':29,'routing_only_final_opens':0,'qualification':'KiCad native accepted results; hardware untested. Placement not needed for feasibility.'});url=run.url;run.finish()
  remote=api.run(project+'/'+rid);history=list(remote.scan_history());verified=[]
  for row in rows:
   matches=[r for r in history if r.get('decision')==row['decision'] and r.get('board_sha256')==row['board_sha256']];assert matches and all(r['native/cost']==row['cost'] for r in matches)
   assert any(r.get('board',{}).get('sha256') for r in matches),'Missing remote board media hash'
   calls=list(client.get_calls(filter={'call_ids':[row['call_id']]},limit=2));assert len(calls)==1 and calls[0].ended_at
   verified.append(row)
  receipt['runs'].append({'id':rid,'url':url,'verified_rows':verified,'artifact':artifact.name});(out/'verified.json').write_text(json.dumps(receipt,indent=2));print(url,flush=True)
if __name__=='__main__':main()
