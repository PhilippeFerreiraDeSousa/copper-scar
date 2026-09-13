#!/usr/bin/env python3
"""Source-bound stage2 publication with native board media and complete files."""
import argparse,datetime,hashlib,json,os,sys,tempfile,uuid,subprocess
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'autoresearch'))
from trace_io import start,finish
PROJECT='philippe-fdesousa/copper-scar'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def uid(s):return str(uuid.uuid5(uuid.NAMESPACE_URL,'pcb-loop-chapter/'+s))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--chapter',default='stage2');a=ap.parse_args();out=a.out;data=json.loads((out/'data.json').read_text());p=next(x for x in data['projects'] if x['id']==a.chapter);remote=out/'remote';remote.mkdir(exist_ok=True);payload=json.dumps(p,sort_keys=True);bundle=hashlib.sha256(payload.encode()).hexdigest();rid='noon-'+a.chapter+'-'+bundle[:12];checkpoint=remote/(rid+'.json')
 if checkpoint.exists():print(checkpoint.read_text());return
 cfg=json.loads(Path('/Users/philippe/dev/copper-scar-demo/.local/copperhead/observability/config.json').read_text());key=Path(cfg['credential_file']);assert key.stat().st_mode&0o077==0;os.environ.update(WANDB_API_KEY=key.read_text().strip(),WANDB_SILENT='true',WANDB_CONSOLE='off')
 import wandb
 now=datetime.datetime.now(datetime.timezone.utc);root=start(uid(rid),'pcb_loop.'+a.chapter+'_evidence',{'protocol':p['protocol'],'summary':p['summary'],'mode':'historical native evidence backfill; no LLM calls'},None,now,attributes={'wb_run_id':rid},display_name=p['title']);run=wandb.init(entity='philippe-fdesousa',project='copper-scar',id=rid,resume='allow',name='PCB Loop · '+p['title'],group='pcb-loop-noon',job_type='native-board-evidence',dir=str(remote));rows=0
 for index,s in enumerate(p['states']):
  if not s['evaluation']:continue
  svg=out/s['board']['images']['Both'];png=remote/(s['board']['sha256']+'.png')
  if not png.exists():subprocess.run(['/opt/homebrew/bin/rsvg-convert','-w','1400','-o',str(png),str(svg)],check=True)
  e=s['evaluation'];score=s.get('score');action=s.get('action');cid=uid(rid+'/'+str(index));call=start(cid,'pcb_loop.checked_candidate',{'title':s['title'],'action':action,'source_sha':s.get('source'),'commands':s.get('commands'),'native_receipt':e,'score':score,'routing_attempted':s.get('routing_attempted')},root,now,attributes={'wb_run_id':rid},display_name=s['title'])
  if not call.ended_at:finish(None,call,{'native':e,'score':score,'retained':s.get('retained'),'retained_official_score':s.get('incumbent_score'),'board_sha256':s['board']['sha256']})
  run.log({'recorded_state':index,'native/opens':e['drc_opens'],'native/violations':e['all_drc_violations'],'native/accepted':e['accepted'],'official/candidate_score':score.get('official_formula_score') if score else None,'official/retained_score':s.get('incumbent_score'),'retained':s.get('retained'),'action':json.dumps(action),'source_sha':s.get('source'),'board_sha256':s['board']['sha256'],'board':wandb.Image(str(png),caption=s['title'])});rows+=1
 evidence=out/'evidence/small'/('stage2' if a.chapter=='stage2' else 'campaign');files={str(f.relative_to(evidence)):f for f in evidence.rglob('*') if f.is_file()};hashes={n:sha(f) for n,f in files.items()};art=wandb.Artifact(rid+'-evidence',type='native-board-evidence',metadata={'state_sha256':bundle,'files_sha256':hashes})
 for n,f in files.items():art.add_file(str(f),name=n)
 logged=run.log_artifact(art);logged.wait();qualified=logged.qualified_name;run.summary.update({'summary':p['summary'],'qualification':p['limitations'],'state_sha256':bundle,'lower_is_better':True});run.finish();api=wandb.Api()
 with tempfile.TemporaryDirectory(prefix='pcb-loop-stage2-verify-') as tmp:
  folder=Path(api.artifact(qualified).download(root=tmp))
  for n,h in hashes.items():assert sha(folder/n)==h,n
 if not root.ended_at:finish(None,root,{'artifact':qualified,'summary':p['summary'],'files_sha256':hashes})
 result={'chapter':a.chapter,'run_url':'https://wandb.ai/'+PROJECT+'/runs/'+rid,'trace_url':'https://wandb.ai/'+PROJECT+'/r/call/'+root.id,'artifact':qualified,'files_downloaded_sha256_verified':len(files),'rows':rows,'chapter_sha256':bundle};checkpoint.write_text(json.dumps(result,indent=2));(remote/(a.chapter+'-chapter-verified.json')).write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True);os._exit(0)
if __name__=='__main__':main()
