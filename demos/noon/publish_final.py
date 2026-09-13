#!/usr/bin/env python3
"""Publish the frozen video and exact replay data, then verify downloaded bytes."""
import argparse,datetime,hashlib,json,os,sys,tempfile,uuid
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'autoresearch'))
from trace_io import start,finish
PROJECT='philippe-fdesousa/copper-scar'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();out=a.out;data=json.loads((out/'data.json').read_text());video=json.loads((out/'video-verified.json').read_text());assert video['data_sha256']==sha(out/'data.json');cfg=json.loads(Path('/Users/philippe/dev/copper-scar-demo/.local/copperhead/observability/config.json').read_text());key=Path(cfg['credential_file']);assert key.stat().st_mode&0o077==0;os.environ.update(WANDB_API_KEY=key.read_text().strip(),WANDB_SILENT='true',WANDB_CONSOLE='off')
 import wandb
 remote=out/'remote';remote.mkdir(exist_ok=True);rid='pcb-loop-noon-'+video['data_sha256'][:12];run=wandb.init(entity='philippe-fdesousa',project='copper-scar',id=rid,resume='allow',name='PCB Loop · frozen multi-size demo',group='pcb-loop-noon',job_type='verified-replay',dir=str(remote));files={n:out/n for n in ['pcb-loop-noon.mp4','data.json','video-verified.json','ui-verified.json']};comparison=out/'evidence/small/stage2/policy-comparison.json'
 if comparison.exists():files['adaptive-margin-comparison.json']=comparison
 hashes={n:sha(p) for n,p in files.items()};artifact=wandb.Artifact(rid+'-replay',type='verified-demo-replay',metadata={'files_sha256':hashes,'data_sha256':video['data_sha256']})
 for n,p in files.items():artifact.add_file(str(p),name=n)
 run.log({'replay':wandb.Video(str(out/'pcb-loop-noon.mp4'),format='mp4'),'data_sha256':video['data_sha256']});logged=run.log_artifact(artifact);logged.wait();qualified=logged.qualified_name;run.summary.update({'qualification':'Frozen saved-native replay. Sizes small-loop/medium-loop/large-loop. No public submission. No fabricated LLM calls.','data_sha256':video['data_sha256']});run.finish()
 with tempfile.TemporaryDirectory(prefix='pcb-noon-video-readback-') as tmp:
  folder=Path(wandb.Api().artifact(qualified).download(root=tmp))
  for n,h in hashes.items():assert sha(folder/n)==h,n
 cid=str(uuid.uuid5(uuid.NAMESPACE_URL,rid));root=start(cid,'pcb_loop.frozen_demo',{'data_sha256':video['data_sha256'],'projects':[{'title':p['title'],'summary':p['summary']} for p in data['projects']]},None,datetime.datetime.now(datetime.timezone.utc),attributes={'wb_run_id':rid},display_name='PCB Loop frozen demo · verified native states')
 if not root.ended_at:finish(None,root,{'artifact':qualified,'files_sha256':hashes,'adaptive_margin_comparison':json.loads(comparison.read_text()) if comparison.exists() else None})
 result={'run_url':'https://wandb.ai/'+PROJECT+'/runs/'+rid,'trace_url':'https://wandb.ai/'+PROJECT+'/r/call/'+cid,'artifact':qualified,'downloaded_files_sha256_verified':hashes,'data_sha256':video['data_sha256'],'video_sha256':video['video_sha256']};(remote/'final-replay-verified.json').write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True);os._exit(0)
if __name__=='__main__':main()
