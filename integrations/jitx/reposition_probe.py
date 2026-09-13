"""Real viewer reposition request against complete design; capture all pose deltas.
No float/unlock semantics assumed. Exact installed components/board/calc.ts protocol.
"""
from pathlib import Path
import asyncio,json,time,shutil,argparse
from jitx.run.runtime import Runtime
from jitx._websocket import Message
from placement_audit import inventory,audit
B=Path('/Users/philippe/dev/copper-scar-jitx')
async def run(name,out,ref,x,y,angle):
 out.mkdir(exist_ok=False,parents=True);shutil.copytree(B/'designs'/name,out/'native-before')
 uri=json.loads((B/'.jitx/runtime.json').read_text())['websocket_uri'].rstrip('/')
 async with Runtime(uri=uri) as r:
  c=r._client.route('design/'+name)
  async def request(kind,body,label):
   t=time.monotonic();items=[]
   conv=await c.request(Message('phd',kind,body))
   async for m in conv:items.append({'namespace':m.ns,'type':m.type,'body':m.body})
   (out/(label+'.json')).write_text(json.dumps(items,indent=2));print(label,time.monotonic()-t,flush=True);return items
  before=await request('load',{},'before');poses,_=inventory(before);p=poses[ref]
  req={'groups':[{'id':p['group_id'],'side':p['side'],'pose':{'center':{'x':x,'y':y},'angle':angle,'flipx':False}}]}
  (out/'request.json').write_text(json.dumps(req,indent=2));await request('reposition',req,'reposition');after=await request('load',{},'after')
  result=audit(out/'before.json',out/'after.json',out/'placement-delta.json');print(json.dumps(result['moves'],indent=2),flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('design');p.add_argument('out',type=Path);p.add_argument('ref');p.add_argument('x',type=float);p.add_argument('y',type=float);p.add_argument('angle',type=float);a=p.parse_args();asyncio.run(asyncio.wait_for(run(a.design,a.out,a.ref,a.x,a.y,a.angle),120))
