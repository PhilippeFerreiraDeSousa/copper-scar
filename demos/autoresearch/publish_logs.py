#!/usr/bin/env python3
"""Publish truthful snapshots of existing router output; never operate the router."""
import argparse, datetime, hashlib, json, os
from pathlib import Path
ROOT=Path('/Users/philippe/dev/copper-scar-demo/.local/copperhead')
PROJECT='philippe-fdesousa/copper-scar'
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--run-id',required=True);ap.add_argument('--attempt',required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
 assert a.attempt.startswith('stage1-') and '/' not in a.attempt
 config=json.loads((ROOT/'observability/config.json').read_text());key=Path(config['credential_file']);assert key.stat().st_mode&0o077==0
 os.environ['WANDB_API_KEY']=key.read_text().strip();os.environ['WANDB_SILENT']='true';os.environ['WANDB_CONSOLE']='wrap'
 import wandb
 now=datetime.datetime.now(datetime.timezone.utc).isoformat();dest=a.output/'router-logs'/a.attempt;dest.mkdir(parents=True,exist_ok=True);entries=[]
 for source in [ROOT/'candidates'/a.attempt/'router.log',ROOT/'runs'/a.attempt/'route.command.json']:
  if source.exists():
   raw=source.read_bytes();target=dest/source.name;target.write_bytes(raw);entries.append({'source':str(source),'file':target.name,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'snapshot_at':now})
 assert entries
 manifest=dest/'snapshot.json';manifest.write_text(json.dumps(entries,indent=2))
 run=wandb.init(entity='philippe-fdesousa',project='copper-scar',id=a.run_id,resume='must',dir=str(a.output),settings=wandb.Settings(console='wrap'))
 print(f'ROUTER LOG SNAPSHOT | captured {now} | attempt {a.attempt}',flush=True)
 print('Read-only publication of existing output. Original timestamps below; this is not a newly executed routing job. Freerouting internal counts are not native KiCad acceptance results.',flush=True)
 for e in entries:
  target=dest/e['file'];run.save(str(target),base_path=str(a.output),policy='now')
  print(f"SOURCE {e['source']} | SHA256 {e['sha256']}",flush=True)
  if target.suffix=='.log':
   for line in target.read_text(errors='replace').splitlines()[-60:]:print('[actual router stdout] '+line,flush=True)
  else:
   obj=json.loads(target.read_text());print('[observed command heartbeat; not router stdout] '+json.dumps({k:obj[k] for k in ['started_at','heartbeat_at','state','elapsed_seconds','returncode','timeout_seconds'] if k in obj}),flush=True)
 run.save(str(manifest),base_path=str(a.output),policy='now')
 artifact=wandb.Artifact(a.run_id+'-router-logs',type='router-log-snapshots',metadata={'attempt_id':a.attempt,'snapshot_at':now,'read_only_snapshot':True});artifact.add_dir(str(dest),name=a.attempt);logged=run.log_artifact(artifact);logged.wait();artifact_name=logged.qualified_name
 run.finish();api=wandb.Api();remote=api.run(PROJECT+'/'+a.run_id);files={f.name:f for f in remote.files()}
 expected=[str((dest/e['file']).relative_to(a.output)) for e in entries];assert all(n in files for n in expected)
 receipt={'run_id':a.run_id,'attempt_id':a.attempt,'logs_url':'https://wandb.ai/'+PROJECT+'/runs/'+a.run_id+'/logs','files_url':'https://wandb.ai/'+PROJECT+'/runs/'+a.run_id+'/files','artifact':artifact_name,'files':expected,'output_log_present':'output.log' in files,'snapshot_at':now,'sources':entries}
 with (a.output/'router-log-publications.jsonl').open('a') as journal:journal.write(json.dumps(receipt)+'\n');journal.flush();os.fsync(journal.fileno())
 (dest/'remote-verified.json').write_text(json.dumps(receipt,indent=2));print(json.dumps(receipt))
if __name__=='__main__':main()
