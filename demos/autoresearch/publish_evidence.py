#!/usr/bin/env python3
"""Publish complete untruncated evidence and verify downloaded SHA256 bytes."""
import argparse,datetime,hashlib,json,os,tempfile,uuid
from pathlib import Path
from trace_io import finish, read as read_trace, start, as_call
from summaries import summarize
ROOT=Path('/Users/philippe/dev/copper-scar-demo/.local/copperhead');PROJECT='philippe-fdesousa/copper-scar'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def stable(s):return str(uuid.uuid5(uuid.NAMESPACE_URL,'copperhead-policy://'+s))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);ap.add_argument('--historical',action='store_true');a=ap.parse_args();out=a.output;remote=out/'remote';state=json.loads((out/'data.json').read_text());assert not state['fixture'];config=json.loads((ROOT/'observability/config.json').read_text());key=Path(config['credential_file']);assert key.stat().st_mode&0o077==0;os.environ['WANDB_API_KEY']=key.read_text().strip();os.environ['WANDB_SILENT']='true';os.environ['WANDB_CONSOLE']='off'
 import wandb,weave
 api=wandb.Api();client=None;jobs=[]
 if a.historical:
  attempt='stage1-20260913-073500-b3f12a';run=ROOT/'runs'/attempt;files={p.name:p for p in [run/'attempt.json',run/'final-pad-partitions.json',run/'final-via-geometry.json',run/'route.command.json'] if p.exists()};jobs.append(('ch-faf401a5149d0ba1',attempt,files,'c3c9373e-08bd-542f-b59c-8bdd8c3c8919'))
 else:
  for policy in state['policies']:
   rid='policy-'+hashlib.sha256((state['experiment_id']+'/'+policy['id']).encode()).hexdigest()[:16]
   for point in policy['points']:
    if not point.get('receipt_href'):continue
    summary_path=out/'attempts'/point['attempt_id']/'evidence-summary.json';summary_path.write_text(json.dumps(summarize(policy,point),indent=2));files={'attempt.json':out/point['receipt_href'],'evidence-summary.json':summary_path,'events.jsonl':out/state.get('events_snapshot_href','events.jsonl')}
    if point.get('pad_partition_proof_href'):files['final-pad-partitions.json']=out/point['pad_partition_proof_href']
    for i,stage in enumerate(point['stages']):
     if stage.get('board'):files[f'boards/{i}-'+['original','updated-pre-route','after-routing'][i]+'.kicad_pcb']=out/stage['board']
    if point.get('incumbent'):files['boards/retained-best.kicad_pcb']=out/point['incumbent']['board']
    rp=Path(point['receipt']);proof=rp.parent/'final-via-geometry.json'
    if proof.exists():files[proof.name]=proof
    files['manifest.json']=out/'manifests'/(state['manifest_sha256']+'.json');jobs.append((rid,point['attempt_id'],files,stable(state['experiment_id']+'/'+policy['id']+'/'+str(point['index']))))
 receipts=[]
 for rid,attempt,files,parentid in jobs:
  hashes={n:digest(p) for n,p in files.items()};bundle_hash=hashlib.sha256(json.dumps({'schema_version':2,'files':hashes},sort_keys=True).encode()).hexdigest();dest=remote/'complete-evidence'/attempt;dest.mkdir(parents=True,exist_ok=True);receipt_file=dest/(bundle_hash+'.verified.json')
  if receipt_file.exists():receipts.append(json.loads(receipt_file.read_text()));continue
  manifest=dest/'sha256-manifest.json';manifest.write_text(json.dumps({'attempt':attempt,'files':hashes,'complete_original_files':True},indent=2));files['sha256-manifest.json']=manifest;hashes['sha256-manifest.json']=digest(manifest)
  run=wandb.init(entity='philippe-fdesousa',project='copper-scar',id=rid,resume='must',dir=str(remote));artifact=wandb.Artifact(attempt+'-complete-evidence',type='complete-native-evidence',metadata={'attempt':attempt,'bundle_sha256':bundle_hash,'array_truncation':False})
  for name,p in files.items():artifact.add_file(str(p),name=name)
  # The full receipt is also available directly in the run Files tab.
  run.save(str(files['attempt.json']),base_path=str(files['attempt.json'].parent.parent),policy='now');logged=run.log_artifact(artifact);logged.wait();qualified=logged.qualified_name;run.finish()
  with tempfile.TemporaryDirectory(prefix='copper-evidence-readback-') as td:
   downloaded=Path(api.artifact(qualified).download(root=td))
   for name,h in hashes.items():assert digest(downloaded/name)==h,('Remote byte mismatch',name)
  parent=read_trace(parentid);assert parent,'Missing parent trace';cid=stable('complete-evidence/'+rid+'/'+bundle_hash);links={'artifact':qualified,'run_files':'https://wandb.ai/'+PROJECT+'/runs/'+rid+'/files','run_artifacts':'https://wandb.ai/'+PROJECT+'/runs/'+rid+'/artifacts','download_note':'Download complete-native-evidence artifact for full untruncated JSON and the listed exact CAD files. Run Files also contains the unique '+attempt+'/attempt.json record.','files_sha256':hashes,'evidence_summary':json.loads(files['evidence-summary.json'].read_text()) if 'evidence-summary.json' in files else 'Historical original record; see full download.'}
  c=start(cid,'copperhead.complete_evidence',{'attempt':attempt,'full_record_sha256':hashes['attempt.json'],'truncated_display_is_not_full_record':True},as_call(parent),datetime.datetime.now(datetime.timezone.utc),display_name='Evidence summary and complete original files')
  if not c.ended_at:finish(client,c,output=links)
  found=read_trace(cid);assert found and found.get('ended_at')
  receipt={'attempt':attempt,'run_id':rid,'bundle_sha256':bundle_hash,'artifact':qualified,'files_sha256':hashes,'downloaded_bytes_verified':True,'trace':'https://wandb.ai/'+PROJECT+'/r/call/'+cid,'links':links,'verified_at':datetime.datetime.now(datetime.timezone.utc).isoformat()};receipt_file.write_text(json.dumps(receipt,indent=2));receipts.append(receipt)
 (remote/('historical-complete-evidence-verified.json' if a.historical else 'complete-evidence-verified.json')).write_text(json.dumps(receipts,indent=2));print(json.dumps([{'attempt':r['attempt'],'artifact':r['artifact'],'verified_files':len(r['files_sha256']),'trace':r['trace']} for r in receipts]),flush=True);os._exit(0)
if __name__=='__main__':main()
