#!/usr/bin/env python3
"""Publish the actual selected-policy consumer separately from frozen N=3."""
import argparse,datetime,hashlib,json,os,tempfile,uuid
from pathlib import Path
from trace_io import start,finish,read
PROJECT='philippe-fdesousa/copper-scar'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def stable(s):return str(uuid.uuid5(uuid.NAMESPACE_URL,'copperhead-policy://'+s))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();out=a.output;state=json.loads((out/'data.json').read_text());assert not state['fixture'];n=state.get('next_campaign');assert n,'No consumer receipt exists';c=n['consumed'];r=n.get('result');remote=out/'remote'
 config=json.loads(Path('/Users/philippe/dev/copper-scar-demo/.local/copperhead/observability/config.json').read_text());key=Path(config['credential_file']);assert key.stat().st_mode&0o077==0;os.environ['WANDB_API_KEY']=key.read_text().strip();os.environ['WANDB_SILENT']='true';os.environ['WANDB_CONSOLE']='off'
 import wandb
 files={a['kind']:out/a['href'] for a in state['decision_artifacts']}
 for p in (out/'next-campaign').glob('*.json'):files['native/'+p.name]=p
 for i,s in enumerate(n.get('stages',[])):
  if s.get('board'):files['boards/'+str(i)+'-board.kicad_pcb']=out/s['board']
 hashes={name:digest(p) for name,p in files.items()};bundle=hashlib.sha256(json.dumps(hashes,sort_keys=True).encode()).hexdigest();receipt_path=remote/('campaign-'+bundle+'.verified.json')
 if receipt_path.exists():print(receipt_path.read_text());return
 rid='consumer-'+hashlib.sha256(state['experiment_id'].encode()).hexdigest()[:16];status=('completed_retained' if r.get('retained') else 'completed_rejected') if r and r['status']=='completed' else r['status'] if r else 'consumed_no_result'
 summary={'policy_loaded':c['policy_id'],'policy_version':c['policy_version'],'consumption_verified':c.get('verified') is True,'execution_status':status,'native_outcome':r.get('nativecost') if r else None,'qualification':'Separate subsequent campaign; excluded from the matched three-decision comparison. A consumption receipt alone does not establish route completion.','diagnostic_feedback':c.get('diagnostic_evidence',[]),'next_hypothesis':c.get('next_hypothesis'),'parent_to_preview_via_net_changes':n.get('via_net_changes',[]),'independent_audit':n.get('independent_audit')}
 run=wandb.init(entity='philippe-fdesousa',project='copper-scar',id=rid,resume='allow',name=state['experiment_id']+' / selected policy next campaign',group=state['experiment_id'],job_type='separate-selected-policy-consumer',dir=str(remote));artifact=wandb.Artifact(rid+'-complete-evidence',type='selected-policy-consumer-evidence',metadata={'sha256_files':hashes,'matched_comparison':False})
 for name,p in files.items():artifact.add_file(str(p),name=name)
 run.summary.update(summary);run.log({'evidence/bundle_sha256':bundle,'consumer/status':status,'consumer/verified':c.get('verified') is True});logged=run.log_artifact(artifact);logged.wait();qualified=logged.qualified_name;run.finish()
 api=wandb.Api()
 with tempfile.TemporaryDirectory(prefix='copper-consumer-readback-') as td:
  folder=Path(api.artifact(qualified).download(root=td))
  for name,expected in hashes.items():assert digest(folder/name)==expected,name
 at=datetime.datetime.fromisoformat(c['consumed_at'].replace('Z','+00:00'));root=start(stable(state['experiment_id']+'/next-campaign'),'copperhead.selected_policy_campaign',{'consumed_receipt':c,'source_experiment':state['experiment_id'],'outside_frozen_N3':True},None,at,display_name='Selected policy consumed by a separate campaign')
 links={'evidence_summary':summary,'artifact':qualified,'files_sha256':hashes,'wandb_url':'https://wandb.ai/'+PROJECT+'/runs/'+rid,'result':r}
 if r and not root.ended_at:finish(None,root,links,datetime.datetime.fromisoformat(r['finished_at'].replace('Z','+00:00')))
 child=start(stable(state['experiment_id']+'/next-campaign/evidence/'+bundle),'copperhead.consumer_evidence',{'bundle_sha256':bundle},root,datetime.datetime.now(datetime.timezone.utc),display_name='Next campaign evidence and decision summary')
 if not child.ended_at:finish(None,child,links)
 result={'run_id':rid,'artifact':qualified,'files_sha256':hashes,'downloaded_bytes_verified':True,'status':status,'consumption_verified':c.get('verified') is True,'source_events_sha256':state['events_sha256'],'trace':'https://wandb.ai/'+PROJECT+'/r/call/'+root.id,'evidence_trace':'https://wandb.ai/'+PROJECT+'/r/call/'+child.id,'summary':summary};receipt_path.write_text(json.dumps(result,indent=2));(remote/'campaign-verified.json').write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True);os._exit(0)
if __name__=='__main__':main()
