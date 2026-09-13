"""Export only our disposable geometry probe; never route or alter a pose."""
from pathlib import Path
import argparse
import asyncio
import fcntl
import json
import shutil
import time
from jitx.run.runtime import Runtime
from jitx._websocket import Message
from jitx._runtime._legacy_plugins import do_export
DESIGN='original_interface.design.InterfaceQualification'

async def capture(root,out):
    plan=json.loads((root/'preparation.json').read_text())
    if plan['kind']!='geometry_only_original_component_qualification' or plan['routing_authorized']:
        raise ValueError('Expected geometry-only disposable root')
    out.mkdir(parents=True,exist_ok=False)
    with (root/'.qualification-controller.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        uri=json.loads((root/'.jitx/runtime.json').read_text())['websocket_uri'].rstrip('/')
        started=time.monotonic()
        async with Runtime(uri=uri) as runtime:
            await do_export('kicad',DESIGN)
            client=runtime._client.route('design/'+DESIGN);conversation=await client.request(Message('phd','load',{}))
            messages=[]
            async for m in conversation:messages.append({'type':m.type,'body':m.body})
            (out/'native.json').write_text(json.dumps(messages,indent=2))
            shutil.copytree(root/'designs'/DESIGN/'kicad',out/'export')
            (out/'completion.json').write_text(json.dumps({'export_barrier':True,'elapsed_s':time.monotonic()-started,'native_routing_started':False,'scope':plan['kind']},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('output',type=Path);a=p.parse_args()
    asyncio.run(asyncio.wait_for(capture(a.root.resolve(),a.output.resolve()),60))
