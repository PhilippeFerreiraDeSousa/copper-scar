#!/usr/bin/env python3
"""Publish an immutable family snapshot, then verify downloaded native files."""
import argparse,datetime,hashlib,json,os,sys,tempfile,uuid,subprocess,shutil,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'autoresearch'))
from trace_io import start,finish

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--family',required=True);a=ap.parse_args();out=a.out;data=json.loads((out/'data.json').read_text());p=next(x for x in data['projects'] if x['id']==a.family);payload=json.dumps(p,sort_keys=True);digest=hashlib.sha256(payload.encode()).hexdigest();rid='live-'+a.family+'-'+digest[:12];remote=out/'remote';remote.mkdir(exist_ok=True)
 cfg=json.loads(Path('/Users/philippe/dev/copper-scar-demo/.local/copperhead/observability/config.json').read_text());key=Path(cfg['credential_file']);assert key.stat().st_mode&0o077==0;os.environ.update(WANDB_API_KEY=key.read_text().strip(),WANDB_SILENT='true',WANDB_CONSOLE='off')
 import wandb
 now=datetime.datetime.now(datetime.timezone.utc);uid=lambda x:str(uuid.uuid5(uuid.NAMESPACE_URL,rid+x));root=start(uid('/root'),'pcb_loop.family_native_evidence',{'family':p['family'],'protocol':p['protocol'],'snapshot_sha256':digest,'mode':'historical evidence backfill; no LLM calls'},None,now,attributes={'wb_run_id':rid},display_name=p['title']);run=wandb.init(entity='philippe-fdesousa',project='copper-scar',id=rid,resume='allow',name='PCB Loop LIVE · '+p['title'],group='pcb-loop-live',dir=str(remote));rows=[]
 with tempfile.TemporaryDirectory(prefix='pcb-loop-publish-') as tmp:
  folder=Path(tmp);(folder/'family.json').write_text(payload)
  for i,s in enumerate(p['states']):
   for rel in [s['board']['cad'],*s['board']['images'].values(),s.get('receipt')]:
    if rel:dest=folder/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(out/rel,dest)
   if not s.get('candidate_native'):continue
   png=folder/(str(i)+'.png');subprocess.run(['/opt/homebrew/bin/rsvg-convert','-w','1200','-o',str(png),str(out/s['board']['images']['Both'])],check=True);n=s['candidate_native'];r=s['retained_native'];call=start(uid('/'+str(i)),'pcb_loop.checked_native_checkpoint',{'source_sha':s.get('source'),'action':s.get('action'),'native_receipt':s['evaluation'],'family_epoch':p['protocol'].get('epoch'),'qualification':s.get('qualification')},root,now,attributes={'wb_run_id':rid},display_name=s['title'])
   if not call.ended_at:finish(None,call,{'candidate_native':n,'retained_native':r,'board_sha256':s['board']['sha256'],'valid':s['full_gate_pass']})
   row={'checkpoint':i,'native/candidate_opens':n['opens'],'native/retained_opens':r['opens'],'native/required_findings':n['required_findings'],'native/candidate_loss':n['loss'],'native/fully_valid':s['full_gate_pass'],'board_sha256':s['board']['sha256'],'trace_call_id':call.id,'board':wandb.Image(str(png),caption=s['title'])};run.log(row);rows.append((i,s['board']['sha256']))
  # Preserve native reports and manifest alongside the saved boards.
  evidence=out/('evidence/original' if a.family=='original' else 'evidence/large/v1')
  for f in evidence.rglob('*.json'):
   dest=folder/f.relative_to(out);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,dest)
  files={str(f.relative_to(folder)):f for f in folder.rglob('*') if f.is_file()};hashes={n:sha(f) for n,f in files.items()};art=wandb.Artifact(rid+'-native',type='native-board-evidence',metadata={'snapshot_sha256':digest,'files_sha256':hashes})
  for name,f in files.items():art.add_file(str(f),name=name)
  logged=run.log_artifact(art);logged.wait();qualified=logged.qualified_name;run.summary.update({'qualification':p['limitations'],'fully_valid':False,'snapshot_sha256':digest});run.finish();api=wandb.Api()
  with tempfile.TemporaryDirectory(prefix='pcb-loop-readback-') as check:
   downloaded=Path(api.artifact(qualified).download(root=check))
   for name,h in hashes.items():assert sha(downloaded/name)==h,name
  remote_rows=[]
  for attempt in range(6):
   remote_rows=list(wandb.Api().run('philippe-fdesousa/copper-scar/'+rid).scan_history())
   if len(remote_rows)==len(rows):break
   time.sleep(5)
  assert len(remote_rows)==len(rows),(len(remote_rows),len(rows))
  for row,(i,h) in zip(remote_rows,rows):assert row['checkpoint']==i and row['board_sha256']==h and row.get('board'),row
 if not root.ended_at:finish(None,root,{'artifact':qualified,'files_verified':len(hashes),'rows_verified':len(rows)})
 result={'run_url':'https://wandb.ai/philippe-fdesousa/copper-scar/runs/'+rid,'trace_url':'https://wandb.ai/philippe-fdesousa/copper-scar/r/call/'+root.id,'artifact':qualified,'files_downloaded_sha256_verified':len(hashes),'metric_media_rows_verified':len(rows),'snapshot_sha256':digest};(remote/(a.family+'-live-verified.json')).write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True);os._exit(0)
if __name__=='__main__':main()
