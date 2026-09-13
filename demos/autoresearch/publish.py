#!/usr/bin/env python3
"""Event-sourced W&B/Weave adapter. Credentials stay in protected process memory."""
import argparse,datetime,fcntl,hashlib,json,os,subprocess,uuid
from pathlib import Path
from model import read_events,canon,sha
PROJECT='philippe-fdesousa/copper-scar'
def stamp(s):return datetime.datetime.fromisoformat(s)
def stable(s):return str(uuid.uuid5(uuid.NAMESPACE_URL,'copperhead-policy://'+s))
def append(p,obj):
 with p.open('a') as f:f.write(json.dumps(obj)+'\n');f.flush();os.fsync(f.fileno())
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);ap.add_argument('--auth-config',type=Path,default=Path('/Users/philippe/dev/copper-scar-demo/.local/copperhead/observability/config.json'));a=ap.parse_args();out=a.output;state=json.loads((out/'data.json').read_text());assert not state['fixture'],'Fixtures must never be remotely published'
 raw,events=read_events(out/'events.jsonl');assert hashlib.sha256(raw).hexdigest()==state['events_sha256'];remote=out/'remote';remote.mkdir(exist_ok=True);lock=(remote/'publish.lock').open('a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 config=json.loads(a.auth_config.read_text());key=Path(config['credential_file']);assert key.stat().st_mode&0o077==0,'Credential file must remain private'
 os.environ['WANDB_API_KEY']=key.read_text().strip();os.environ['WANDB_SILENT']='true';os.environ['WANDB_CONSOLE']='wrap'
 import requests,wandb,weave
 from PIL import Image
 response=requests.post('https://api.wandb.ai/graphql',auth=('api',os.environ['WANDB_API_KEY']),json={'query':'{ project(name:"copper-scar", entityName:"philippe-fdesousa") { name } }'},timeout=30);response.raise_for_status();assert response.json().get('data',{}).get('project')
 api=wandb.Api();client=weave.init(PROJECT);experiment=state['experiment_id'];policies={p['id']:p for p in state['policies']};calls={}
 def call(id,name,inputs,parent,at,attributes=None):
  cid=stable(id)
  if cid in calls:return calls[cid]
  found=list(client.get_calls(filter={'call_ids':[cid]},limit=1))
  c=found[0] if found else client.create_call(name,inputs,parent=parent,attributes={'experiment_id':experiment,'event_sourced':True,**(attributes or {})},display_name=name.split('.')[-1],use_stack=False,_call_id_override=cid,started_at=stamp(at))
  calls[cid]=c;return c
 root=call(experiment,'copperhead.policy_experiment',{'common_protocol':state['common_protocol'],'manifest_sha256':state['manifest_sha256']},None,events[0]['timestamp_utc'])
 parents={};lowercalls={}
 for event in events:
  pol=event.get('policy') or {};pid=pol.get('id');typ=event['type'];lower=event.get('lower') or {};idx=lower.get('index')
  if typ=='policy_started':parents[pid]=call(experiment+'/'+pid,'copperhead.policy_version',pol,root,event['timestamp_utc'])
  if typ=='lower_started' and pid:lowercalls[pid,idx]=call(experiment+'/'+pid+'/'+str(idx),'copperhead.lower_decision',{'policy':pol,'index':idx,'input':lower},parents[pid],event['timestamp_utc'])
 groups={}
 for i,event in enumerate(events):groups.setdefault((event.get('policy') or {}).get('id','experiment'),[]).append((i,event))
 verified=[];runlinks=[]
 for pid,items in groups.items():
  run_id='policy-'+hashlib.sha256((experiment+'/'+pid).encode()).hexdigest()[:16];run_path=PROJECT+'/'+run_id
  try:r=api.run(run_path);history=list(r.scan_history())
  except wandb.errors.CommError as exc:
   if 'not found' not in str(exc).lower() and 'could not find' not in str(exc).lower():raise
   history=[]
  byid={}
  for row in history:
   if row.get('event_id'):byid.setdefault(row['event_id'],[]).append(row)
  run=wandb.init(entity=PROJECT.split('/')[0],project=PROJECT.split('/')[1],id=run_id,resume='allow',name=experiment+' / '+pid,group=experiment,job_type='higher-level-policy-experiment',dir=str(remote),config={'experiment_id':experiment,'policy':policies.get(pid),'common_protocol':state['common_protocol'],'event_source':'durable local append-only events; not reconstructed historical control','fixture':False})
  run.define_metric('decision_index');run.define_metric('cost/*',step_metric='decision_index');run.define_metric('validity/*',step_metric='decision_index');run.define_metric('time/*',step_metric='decision_index')
  new_events=[]
  for seq,event in items:
   id=event['event_id'];digest=hashlib.sha256(canon(event).encode()).hexdigest();typ=event['type'];lower=event.get('lower') or {};idx=lower.get('index');point=next((p for p in policies.get(pid,{}).get('points',[]) if p['event_id']==id),None)
   metadata={'event_id':id,'event_sha256':digest,'event_type':typ,'event_sequence':seq,'event_timestamp':event['timestamp_utc'],'policy_id':pid,'experiment_id':experiment,'event_payload_json':canon(event)}
   if point and point['completed']:
    metadata.update(decision_index=idx,lower_status=point['status'],retained=point['retained'])
    for prefix,cost in [('attempted',point['attempted']),('best',point['best'])]:
     if cost:
      for k,v in cost.items():
       if isinstance(v,(int,float,bool)) and v is not None:metadata[('cost/' if k=='opens' else 'validity/')+prefix+'_'+k]=v
    metadata['time/decision_seconds']=point['elapsed_seconds'];metadata['time/router_seconds']=point.get('route_elapsed_seconds');metadata['routed_dispatch_count']=lower.get('routed_dispatch_count',0)
    for kind,board in [('attempted',next((s for s in reversed(point['stages']) if s.get('board')),None)),('best',point.get('incumbent'))]:
     if board:
      svg=out/board['base']/'F.Cu.svg';png=svg.with_suffix('.png')
      if not png.exists():subprocess.run(['/opt/homebrew/bin/rsvg-convert','-w','1200','-o',str(png),str(svg)],check=True,capture_output=True)
      metadata['board/'+kind+'_sha256']=board['sha256'];metadata['board/'+kind]=wandb.Image(str(png),caption=pid+' '+str(idx)+' '+kind+'; exact saved board, partial/unqualified')
   if id not in byid:
    append(remote/'publication-journal.jsonl',{'state':'upload_intent','event_id':id,'event_sha256':digest,'run_id':run_id,'at':datetime.datetime.now(datetime.timezone.utc).isoformat()});run.log(metadata);new_events.append(event);print('[recorded experiment event] '+json.dumps({'timestamp':event['timestamp_utc'],'type':typ,'policy':pid,'decision':idx,'status':lower.get('status'),'attempted':lower.get('nativecost'),'retained':lower.get('retained'),'retained_best':lower.get('retainedbest')}),flush=True)
   else:assert all(row['event_sha256']==digest for row in byid[id]),'Conflicting remote event'
   parent=lowercalls.get((pid,idx),parents.get(pid,root));eventcall=call(experiment+'/event/'+id,'copperhead.policy_event',{'event_id':id,'event_sha256':digest,'type':typ},parent,event['timestamp_utc'])
   if not eventcall.ended_at:client.finish_call(eventcall,output=event,ended_at=stamp(event['timestamp_utc']))
   if typ=='lower_completed' and (pid,idx) in lowercalls:
    c=lowercalls[pid,idx]
    if not c.ended_at:client.finish_call(c,output=lower,ended_at=stamp(event['timestamp_utc']))
   if typ=='policy_completed' and pid in parents:
    c=parents[pid]
    if not c.ended_at:client.finish_call(c,output=lower,ended_at=stamp(event['timestamp_utc']))
   if typ=='policy_decision' and not root.ended_at:client.finish_call(root,output=event['decision'],ended_at=stamp(event['timestamp_utc']))
  if new_events:
   snapshot=remote/(run_id+'-'+state['events_sha256'][:12]+'.jsonl');snapshot.write_text(''.join(json.dumps(e)+'\n' for e in new_events));artifact=wandb.Artifact(run_id+'-events',type='policy-experiment-events',metadata={'experiment_id':experiment,'source_events_sha256':state['events_sha256']});artifact.add_file(str(snapshot),name='events.jsonl');artifact.add_file(str(out/'manifests'/(state['manifest_sha256']+'.json')),name='manifest.json')
   for e in new_events:
    lower=e.get('lower') or {};rp=lower.get('receipt_path')
    if rp:
     rp=Path(rp);artifact.add_file(str(rp),name='attempts/'+rp.parent.name+'/attempt.json')
     proof=rp.parent/'final-pad-partitions.json'
     if proof.exists():artifact.add_file(str(proof),name='attempts/'+rp.parent.name+'/final-pad-partitions.json')
   logged=run.log_artifact(artifact);logged.wait();append(remote/'publication-journal.jsonl',{'state':'artifact_uploaded','run_id':run_id,'artifact':logged.qualified_name,'digest':logged.digest,'local_sha256':sha(snapshot)})
  if pid in policies:
   p=policies[pid];run.summary.update({'completed_decisions':p['completed_decisions'],'routed_dispatch_count':p['routed_dispatch_count'],'routed_completed':p['routed_completed'],'cost_at_N_decisions':p['cost_at_n'],'decision_wall_seconds':p['decision_wall_seconds'],'router_wall_seconds':p['route_wall_seconds'],'policy_state':p['state']})
  else:run.summary.update({'policy_decisions':state['decisions'],'common_protocol_sha256':hashlib.sha256(canon(state['common_protocol']).encode()).hexdigest()})
  run.finish();fresh=api.run(run_path);history=list(fresh.scan_history());files={f.name for f in fresh.files()}
  for _,event in items:
   digest=hashlib.sha256(canon(event).encode()).hexdigest();matches=[x for x in history if x.get('event_id')==event['event_id']];assert matches and all(x['event_sha256']==digest for x in matches)
   for row in matches:
    for name in ['board/attempted','board/best']:
     if name in row:assert row[name]['path'] in files and row[name].get('sha256')
   cid=stable(experiment+'/event/'+event['event_id']);found=list(client.get_calls(filter={'call_ids':[cid]},limit=2));assert len(found)==1 and found[0].ended_at;assert dict(found[0].output)['event_id']==event['event_id']
   receipt={'event_id':event['event_id'],'event_sha256':digest,'wandb_run_id':run_id,'wandb_url':'https://wandb.ai/'+PROJECT+'/runs/'+run_id,'weave_call_id':cid,'weave_url':'https://wandb.ai/'+PROJECT+'/r/call/'+cid,'remote_history_rows':len(matches),'media_verified':True,'weave_verified':True};verified.append(receipt)
  runlinks.append({'policy_id':pid,'run_id':run_id,'url':'https://wandb.ai/'+PROJECT+'/runs/'+run_id})
 receipt={'experiment_id':experiment,'verified_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'verified_events':len(verified),'source_events_sha256':state['events_sha256'],'runs':runlinks,'events':verified,'root_weave_call_id':stable(experiment),'root_weave_url':'https://wandb.ai/'+PROJECT+'/r/call/'+stable(experiment)}
 (remote/'verified.json').write_text(json.dumps(receipt,indent=2));append(remote/'publication-journal.jsonl',{'state':'verified','verified_events':len(verified),'events_sha256':state['events_sha256'],'at':receipt['verified_at']});print(json.dumps({'verified_events':len(verified),'runs':runlinks}),flush=True);weave.finish()
if __name__=='__main__':main()
