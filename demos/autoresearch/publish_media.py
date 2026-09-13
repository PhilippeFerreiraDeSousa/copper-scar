#!/usr/bin/env python3
"""Upload a verified actual replay as W&B video and immutable artifact."""
import argparse,hashlib,json,os,tempfile
from pathlib import Path

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();out=a.output;proof=json.loads((out/'replay-verified.json').read_text());assert not proof['fixture'] and proof['full_decode_pass'];video=out/'two-level-replay.mp4';assert hashlib.sha256(video.read_bytes()).hexdigest()==proof['video_sha256'];state=json.loads((out/'data.json').read_text());remote=out/'remote';rid='policy-'+hashlib.sha256((state['experiment_id']+'/experiment').encode()).hexdigest()[:16]
 config=json.loads(Path('/Users/philippe/dev/copper-scar-demo/.local/copperhead/observability/config.json').read_text());key=Path(config['credential_file']);assert key.stat().st_mode&0o077==0;os.environ['WANDB_API_KEY']=key.read_text().strip();os.environ['WANDB_SILENT']='true';os.environ['WANDB_CONSOLE']='off'
 import wandb
 api=wandb.Api();path='philippe-fdesousa/copper-scar/'+rid;prior=list(api.run(path).scan_history());digest=proof['video_sha256'];matches=[x for x in prior if x.get('replay_sha256')==digest]
 previous=json.loads((remote/'replay-verified.json').read_text()) if (remote/'replay-verified.json').exists() else {}
 artifact_name=previous.get('artifact') if previous.get('video_sha256')==digest else None
 if not matches:
  run=wandb.init(entity='philippe-fdesousa',project='copper-scar',id=rid,resume='must',dir=str(remote));run.log({'replay_sha256':digest,'replay/comparison_complete':proof['comparison_complete'],'replay/source_events_sha256':proof['source_events_sha256'],'replay/video':wandb.Video(str(video),format='mp4',caption='Actual chronological checkpoints. '+('Comparison decision recorded.' if proof['comparison_complete'] else 'IN PROGRESS: comparison incomplete; no cost at 3 decisions.'))});artifact=wandb.Artifact(rid+'-replay',type='actual-policy-replay',metadata=proof);artifact.add_file(str(video),name='two-level-replay.mp4');artifact.add_file(str(out/'replay-verified.json'),name='replay-verified.json');artifact.add_file(str(out/'replay-state.json'),name='replay-state.json');logged=run.log_artifact(artifact);logged.wait();artifact_name=logged.qualified_name;run.finish()
 assert artifact_name,'Missing artifact reference for verified video'
 with tempfile.TemporaryDirectory(prefix='copper-replay-readback-') as td:
  downloaded=Path(api.artifact(artifact_name).download(root=td));assert hashlib.sha256((downloaded/'two-level-replay.mp4').read_bytes()).hexdigest()==digest
  assert hashlib.sha256((downloaded/'replay-state.json').read_bytes()).hexdigest()==proof['source_state_sha256']
 fresh=api.run(path);rows=[x for x in fresh.scan_history() if x.get('replay_sha256')==digest];assert rows;files={f.name for f in fresh.files()};media=rows[-1]['replay/video'];assert media['path'] in files
 receipt={'run_id':rid,'video_sha256':digest,'source_events_sha256':proof['source_events_sha256'],'source_state_sha256':proof.get('source_state_sha256'),'comparison_complete':proof['comparison_complete'],'downloaded_bytes_verified':True,'remote_media_path':media['path'],'artifact':artifact_name,'url':'https://wandb.ai/philippe-fdesousa/copper-scar/runs/'+rid};(remote/'replay-verified.json').write_text(json.dumps(receipt,indent=2));print(json.dumps(receipt))
if __name__=='__main__':main()
