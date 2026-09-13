"""Capture the same realized board response used by the installed JITX visualizer."""
from pathlib import Path
import asyncio,json
from jitx.run.runtime import Runtime
from jitx._websocket import Message
from jitx._runtime._legacy_plugins import do_export
B=Path('/Users/philippe/dev/copper-scar-jitx');R=B/'runs/import-ab-20260912';name='pcbgolf_import.current.PcbgolfFull'
async def main():
 uri=json.loads((B/'.jitx/runtime.json').read_text())['websocket_uri'].rstrip('/')
 async with Runtime(uri=uri) as r:
  conv=await r._client.route('design/'+name).request(Message('phd','load',{}))
  replies=[]
  async for env in conv:
   print(env.ns,env.type,flush=True);replies.append(dict(namespace=env.ns,type=env.type,body=env.body))
  (R/'captured-live-view.json').write_text(json.dumps(replies,indent=2))
  print('Export:',await do_export('kicad',name),flush=True)
asyncio.run(asyncio.wait_for(main(),55))
