"""Synchronous JSON-safe trace completion, with bounded remote readback."""
import datetime, os, time
import requests
PROJECT='philippe-fdesousa/copper-scar'
def request(path,payload):
 r=requests.post('https://trace.wandb.ai'+path,auth=('api',os.environ['WANDB_API_KEY']),json=payload,timeout=30)
 if not r.ok:raise RuntimeError('Trace '+path+' '+str(r.status_code)+' '+r.text[:1200])
 return r.json()
def read(cid):return request('/call/read',{'project_id':PROJECT,'id':cid}).get('call')
def finish(client,call,output,ended_at=None):
 at=ended_at or datetime.datetime.now(datetime.timezone.utc)
 payload={'project_id':PROJECT,'id':call.id,'ended_at':at.isoformat(),'output':output,'summary':{}}
 if getattr(call,'trace_id',None):payload['trace_id']=call.trace_id
 if getattr(call,'started_at',None):payload['started_at']=call.started_at.isoformat()
 request('/v2/'+PROJECT+'/call/end',{'end':payload})
 for _ in range(20):
  result=read(call.id)
  if result and result.get('ended_at') and result.get('output')==output:
   call.ended_at=at;return result
  time.sleep(1)
 raise AssertionError('Trace completion not read back: '+call.id)
def as_call(r):
 from types import SimpleNamespace
 return SimpleNamespace(id=r['id'],trace_id=r['trace_id'],started_at=datetime.datetime.fromisoformat(r['started_at'].replace('Z','+00:00')),ended_at=datetime.datetime.fromisoformat(r['ended_at'].replace('Z','+00:00')) if r.get('ended_at') else None,output=r.get('output'))
def start(cid,name,inputs,parent,at,attributes=None,display_name=None):
 existing=read(cid)
 if existing:return as_call(existing)
 payload={'project_id':PROJECT,'id':cid,'op_name':name,'display_name':display_name or name.split('.')[-1],'trace_id':parent.trace_id if parent else cid,'parent_id':parent.id if parent else None,'started_at':at.isoformat(),'attributes':attributes or {},'inputs':inputs}
 request('/v2/'+PROJECT+'/call/start',{'start':payload})
 for _ in range(20):
  result=read(cid)
  if result:return as_call(result)
  time.sleep(1)
 raise AssertionError('Trace start not read back: '+cid)
