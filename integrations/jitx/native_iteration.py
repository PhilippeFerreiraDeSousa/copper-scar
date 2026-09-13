"""4.4 viewer capture/route/export, pinned to installed services/autoroute.ts."""
from pathlib import Path
import asyncio,json,time,argparse,shutil
from collections import Counter
from jitx._websocket import ErrorMessage
from jitx.run.runtime import Runtime
from jitx._websocket import Message
from jitx._runtime._legacy_plugins import do_export
B=Path('/Users/philippe/dev/copper-scar-jitx')
async def run(name,out,route,net_names=None):
 out.mkdir(parents=True,exist_ok=False);timings={};uri=json.loads((B/'.jitx/runtime.json').read_text())['websocket_uri'].rstrip('/')
 async with Runtime(uri=uri) as runtime:
  client=runtime._client.route('design/'+name)
  async def request(kind,body,file,limit=55):
   t=time.monotonic();replies=[]
   async def consume():
    conv=await client.request(Message('phd',kind,body))
    async for env in conv:replies.append({'namespace':env.ns,'type':env.type,'body':env.body})
   try:await asyncio.wait_for(consume(),limit)
   finally:
    timings[file]=time.monotonic()-t;(out/(file+'.json')).write_text(json.dumps(replies,indent=2));(out/'timings.json').write_text(json.dumps(timings,indent=2))
   print(file,round(timings[file],3),dict(Counter(m['type'] for m in replies)),flush=True);return replies
  before=await request('load',{},'before')
  if route:
   shutil.copytree(B/'designs'/name,out/'before-native-state')
   nets=next(m['body']['nets'] for m in before if m['type']=='nets' and m['body'].get('complete') is True)
   if net_names:
    selected=[n for n in nets if n['name'] in net_names]
    assert {n['name'] for n in selected}==set(net_names), 'requested net absent'
    nets=selected
   board=next(m['body'] for m in before if m['type']=='board')
   count=board['stackup']['numlayers']
   assert type(count) is int and count>=2, 'invalid copper-layer count'
   layers=list(range(count))
   (out/'routing-selection.json').write_text(json.dumps({'nets':[n['name'] for n in nets],'layers':layers,'force':False},indent=2))
   pads=sorted({p for n in nets for c in n['connected'] for p in c.get('pads',[])})
   for layer in layers:await request('route',{'layer':layer,'pads':pads,'force':False,'configure':None},f'route-layer-{layer}',55)
   await request('load',{},'after')
  t=time.monotonic();attempts=[]
  while True:
   try:
    result=await asyncio.wait_for(do_export('kicad',name),600);break
   except ErrorMessage as e:
    attempts.append({'elapsed_seconds':time.monotonic()-t,'error':str(e)})
    (out/'export-wait.json').write_text(json.dumps(attempts,indent=2))
    if not ('physical design task' in str(e) and 'in progress' in str(e)) or time.monotonic()-t>600:raise
    await asyncio.sleep(10)
  timings['export_including_wait']=time.monotonic()-t
  (out/'export-result.json').write_text(json.dumps(result,default=str,indent=2));(out/'timings.json').write_text(json.dumps(timings,indent=2))
  shutil.copytree(B/'designs'/name/'kicad',out/'export')
  # Evidence-only copy outward; the runtime exclusively owns the live directory.
  shutil.copytree(B/'designs'/name,out/'native-output-checkpoint')
  print('export',result,flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('design');p.add_argument('out',type=Path);p.add_argument('--route',action='store_true');p.add_argument('--net',action='append');a=p.parse_args();asyncio.run(run(a.design,a.out,a.route,a.net))
