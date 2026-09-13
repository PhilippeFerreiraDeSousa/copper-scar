#!/usr/bin/env python3
"""Publish immutable native evidence with explicit historical backfill semantics."""
import argparse,datetime,hashlib,json,os,sys,tempfile,uuid
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'autoresearch'))
from trace_io import start,finish
PROJECT='philippe-fdesousa/copper-scar'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def uid(x):return str(uuid.uuid5(uuid.NAMESPACE_URL,'pcb-loop-noon/'+x))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();out=a.out;data=json.loads((out/'data.json').read_text());p=data['projects'][0];remote=out/'remote';remote.mkdir(exist_ok=True);keyfile=Path(json.loads(Path('/Users/philippe/dev/copper-scar-demo/.local/copperhead/observability/config.json').read_text())['credential_file']);assert keyfile.stat().st_mode&0o077==0;os.environ['WANDB_API_KEY']=keyfile.read_text().strip();os.environ['WANDB_SILENT']='true';os.environ['WANDB_CONSOLE']='off'
 import wandb
 bundle=sha(out/'evidence/small/campaign/records.json');rid='small-noon-'+bundle[:12];checkpoint=remote/(rid+'.json')
 if checkpoint.exists():print(checkpoint.read_text());return
 now=datetime.datetime.now(datetime.timezone.utc);root=start(uid(rid),'pcb_loop.small_matched_policy_evidence',{'protocol':p['protocol'],'source_sha':p['protocol']['source_sha'],'mode':'historical deterministic execution evidence; no LLM calls','initialization':'Routing alone29→0; placement not needed for feasibility'},None,now,attributes={'wb_run_id':rid,'llm_involved':False},display_name='Small board: routing-only zero, matched policies tie')
 parents={}
 run=wandb.init(entity='philippe-fdesousa',project='copper-scar',id=rid,resume='allow',name='PCB Loop · small matched pilot and topology',group='pcb-loop-noon',job_type='saved-native-evidence',dir=str(remote),config={'protocol':p['protocol'],'qualification':p['limitations']})
 for arm in ['all-net-hpwl','signal-net-hpwl','routing-only','topology']:
  parents[arm]=start(uid(rid+'/'+arm),'pcb_loop.policy_evidence',{'ranking':arm,'no_per_step_llm':True},root,now,attributes={'wb_run_id':rid},display_name=arm)
 hashes={};count=0
 for s in p['states']:
  if not s.get('evaluation') or s['phase']=='Routing-only initialization' and 'Initial placement' in s['title']:continue
  e=s['evaluation'];arm=s.get('arm','topology');action=s.get('action');receipt=json.loads((out/s['receipt']).read_text());assert receipt==e
  cid=uid(rid+'/'+s['board']['sha256']+'/'+s['title']);call=start(cid,'pcb_loop.native_attempt_evidence',{'action':action,'source_sha':s.get('source'),'commands':s.get('commands',[]),'board_sha256':s['board']['sha256'],'qualification':'Saved native evidence; no fabricated LLM reasoning','title':s['title']},parents[arm],now,attributes={'wb_run_id':rid},display_name=s['title']);output={'evaluation':e,'retained':s.get('retained'),'official_stage2_score':None}
  if not call.ended_at:finish(None,call,output)
  run.log({'evidence_index':count,'arm':arm,'native/opens':e['drc_opens'],'native/required_violations':len(e.get('required_violations',[])),'native/accepted':e['accepted'],'quality/wire_mm':e['wire_length_mm'],'quality/vias':e['vias'],'retained':s.get('retained'),'board_sha256':s['board']['sha256'],'action':json.dumps(action),'trace_url':'https://wandb.ai/'+PROJECT+'/r/call/'+cid});count+=1
 artifact=wandb.Artifact(rid+'-complete-evidence',type='native-board-evidence',metadata={'records_sha256':bundle,'no_llm_calls':True,'qualification':p['limitations']})
 for f in (out/'evidence/small').rglob('*'):
  if not f.is_file() or f.suffix.lower() not in ['.json','.log','.kicad_pcb','.kicad_pro','.kicad_sch','.dsn','.ses']:continue
  name=str(f.relative_to(out/'evidence/small'));hashes[name]=sha(f);artifact.add_file(str(f),name=name)
 logged=run.log_artifact(artifact);logged.wait();qualified=logged.qualified_name;run.summary.update({'policy_winner':False,'selected_policy':'all-net-hpwl','routing_only_initial_opens':29,'routing_only_final_opens':0,'official_stage2_score_claimed':False,'qualification':p['summary']});run.finish()
 api=wandb.Api()
 with tempfile.TemporaryDirectory(prefix='pcb-loop-remote-readback-') as tmp:
  folder=Path(api.artifact(qualified).download(root=tmp))
  for name,h in hashes.items():assert sha(folder/name)==h,name
 for arm,parent in parents.items():
  if not parent.ended_at:finish(None,parent,{'higher_loop_decision':p['decision'] if arm in ['all-net-hpwl','signal-net-hpwl'] else None,'artifact':qualified})
 if not root.ended_at:finish(None,root,{'higher_loop_decision':p['decision'],'artifact':qualified,'files_sha256':hashes,'qualification':p['summary']})
 result={'run_url':'https://wandb.ai/'+PROJECT+'/runs/'+rid,'trace_url':'https://wandb.ai/'+PROJECT+'/r/call/'+root.id,'artifact':qualified,'files_downloaded_sha256_verified':len(hashes),'rows':count,'record_sha256':bundle};checkpoint.write_text(json.dumps(result,indent=2));(remote/'small-verified.json').write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True);os._exit(0)
if __name__=='__main__':main()
