"""Read immutable local events; build only points established by completed records."""
import hashlib,json
from pathlib import Path

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'))
def cost(x):
 if not isinstance(x,dict):return None
 return {'opens':x.get('opens',x.get('unconnected',x.get('missing_pairs'))),'physical_errors':x.get('physical_errors',x.get('errors')),'warnings':x.get('warnings'),'manufacturing_findings':x.get('manufacturing_findings_count',x.get('manufacturing_findings')),'pad_groups_preserved':x.get('pad_groups_preserved',x.get('no_connected_pad_group_split')),'invariants_ok':x.get('invariants_ok'),'validity_gate':x.get('validity_gate')}
def read_events(path):
 raw=Path(path).read_bytes();end=raw.rfind(b'\n')+1;raw=raw[:end];events=[];ids={}
 for line in raw.splitlines():
  if not line.strip():continue
  event=json.loads(line);id=event['event_id']
  if id in ids:
   assert canon(ids[id])==canon(event),'Conflicting event ID';continue
  ids[id]=event;events.append(event)
 return raw,events

def fold(manifest,events):
 policies={};fixture=manifest.get('fixture',False);experiment=manifest.get('experiment_id');protocol=manifest.get('common_protocol',{});budget=protocol.get('attempt_budget',protocol.get('n_attempts',protocol.get('N',3)))
 def policy(p):
  if isinstance(p,str):p={'id':p}
  id=p.get('id',p.get('policy_id'))
  if not id:return None
  if id not in policies:policies[id]={'id':id,'points':[],'events':[],'state':'not_started','decision':None}
  policies[id].update({k:v for k,v in p.items() if k not in ('points','events','state','decision')});return policies[id]
 for p in manifest.get('policies',[]):policy(p)
 decisions=[]
 for event in events:
  assert event['experiment_id']==experiment
  assert not event.get('fixture',False) or fixture,'Fixture in actual experiment'
  if event.get('common_protocol'):
   if not protocol:protocol=event['common_protocol']
  p=policy(event.get('policy',{}));typ=event['type'];lower=event.get('lower') or {}
  if p:p['events'].append(event['event_id'])
  if typ=='policy_started' and p:p.update(state='running',started_at=event['timestamp_utc'])
  if typ in ('lower_started','lower_running') and p:p.update(state=lower.get('status','running'),active_index=lower.get('index'),heartbeat=event['timestamp_utc'])
  if typ=='lower_started' and p:p['active_input']=lower
  if typ=='candidate_screened' and p:p.setdefault('screened',[]).append({'event_id':event['event_id'],'timestamp':event['timestamp_utc'],**lower})
  if typ=='proposal_selected' and p:p['active_proposal']=lower
  if typ=='proposal_selected' and p:p.update(state='routing_requested' if lower.get('feasible') else 'precheck_rejected')
  if typ=='heartbeat' and p:p.update(heartbeat=event['timestamp_utc'])
  if p and (typ in ('baseline','baseline_evaluated','policy_baseline','lower_completed') or lower.get('index')==0):
   record=None;receipt=lower.get('receipt_path',lower.get('attempt_receipt'))
   if receipt:
    rp=Path(receipt);record=json.loads(rp.read_text())
    if lower.get('receipt_sha256'):assert sha(rp)==lower['receipt_sha256']
   index=lower.get('index');status=lower.get('status',record.get('status') if record else 'completed')
   attempted=cost(lower.get('nativecost',lower.get('attempted_cost',record.get('after') if record else {})))
   best=cost(lower.get('retainedbest',lower.get('retained_best',lower.get('best_cost',{}))))
   retained=lower.get('retained',record.get('became_incumbent') if record else None)
   previous=p['points'][-1] if p['points'] else None
   if best is None or best.get('opens') is None:
    best=attempted if retained or index==0 else previous.get('best') if previous else None
   point={'index':index,'event_id':event['event_id'],'timestamp':event['timestamp_utc'],'status':status,'attempted':attempted,'best':best,'retained':retained,'elapsed_seconds':lower.get('elapsed_seconds',lower.get('elapsed')),'receipt':receipt,'attempt_id':lower.get('attempt_id',record.get('attempt') if record else None),'record':record,'raw_lower':lower,'completed':index==0 or typ=='lower_completed','routed_completed':bool(record and record.get('status')=='completed' and record.get('routing_scope',{}).get('execution'))}
   if any(x['index']==index for x in p['points']):raise AssertionError('Repeated lower index')
   p['points'].append(point);p['state']='evaluated' if point['completed'] else 'failed';p['active_index']=None
  if typ=='policy_completed' and p:p.update(state='completed',finished_at=event['timestamp_utc'],summary=event.get('lower') or event.get('summary'))
  if typ in ('policy_decision','experiment_completed'):
   decisions.append({'event_id':event['event_id'],'timestamp':event['timestamp_utc'],'decision':event.get('decision'),'type':typ})
   if p:p['decision']=event.get('decision')
 for p in policies.values():
  completed={x['index']:x for x in p['points'] if x['completed'] and x['index']!=0};p['completed_attempts']=len(completed);p['completed_decisions']=len(completed);p['routed_completed']=sum(x['routed_completed'] for x in p['points']);p['routed_dispatch_count']=max([x['raw_lower'].get('routed_dispatch_count',0) for x in p['points']] or [0])
  p['cost_at_n']=completed[budget]['best'] if all(i in completed for i in range(1,budget+1)) else None
  p['decision_wall_seconds']=sum(x['elapsed_seconds'] or 0 for x in p['points'] if x['index']!=0);p['route_wall_seconds']=0
 return {'fixture':fixture,'started_at':events[0]['timestamp_utc'] if events else manifest.get('created_at'),'experiment_id':experiment,'common_protocol':protocol,'attempt_budget':budget,'policies':list(policies.values()),'decisions':decisions,'event_count':len(events),'latest_event_at':events[-1]['timestamp_utc'] if events else None,'manifest':manifest}
