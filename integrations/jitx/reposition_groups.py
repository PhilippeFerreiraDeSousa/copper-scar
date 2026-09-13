"""Batch live placement through JITX runtime only; never edit generated routing files."""
from pathlib import Path
import asyncio,json,time,shutil,argparse
from jitx.run.runtime import Runtime
from jitx._websocket import Message
from placement_audit import inventory,audit
B=Path('/Users/philippe/dev/copper-scar-jitx')
async def run(name,proposal,out):
 out.mkdir(exist_ok=False,parents=True);shutil.copytree(B/'designs'/name,out/'native-input-checkpoint')
 uri=json.loads((B/'.jitx/runtime.json').read_text())['websocket_uri'].rstrip('/')
 async with Runtime(uri=uri) as r:
  c=r._client.route('design/'+name)
  async def req(kind,body,label):
   start=time.monotonic();items=[]
   try:
    conv=await c.request(Message('phd',kind,body))
    async for m in conv:items.append({'namespace':m.ns,'type':m.type,'body':m.body})
   finally:(out/(label+'.json')).write_text(json.dumps(items,indent=2));(out/(label+'-time.json')).write_text(json.dumps({'elapsed_seconds':time.monotonic()-start}))
   return items
  before=await req('load',{},'before');poses,_=inventory(before);p=json.loads(proposal.read_text());assert set(p['moves'])<=set(poses)
  groups=[]
  for ref,target in p['moves'].items():
   assert target['side']==poses[ref]['side'],'side flips require an explicit separate proposal'
   groups.append({'id':poses[ref]['group_id'],'side':target['side'],'pose':{'center':{'x':target['x'],'y':target['y']},'angle':target['angle'],'flipx':False}})
  assert len({g['id'] for g in groups})==len(groups),'overlapping groups'
  body={'groups':groups};(out/'request.json').write_text(json.dumps(body,indent=2));await req('reposition',body,'reposition');await req('load',{},'after')
  result=audit(out/'before.json',out/'after.json',out/'placement-delta.json');print(json.dumps({k:v for k,v in result.items() if k not in ['moves','boundary_before','boundary_after']},indent=2),flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('design');p.add_argument('proposal',type=Path);p.add_argument('out',type=Path);a=p.parse_args();asyncio.run(asyncio.wait_for(run(a.design,a.proposal,a.out),180))
