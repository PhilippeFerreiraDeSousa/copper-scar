"""Read the realized layout from the active design without resubmitting it."""
from pathlib import Path
import asyncio,json
from google.protobuf.json_format import MessageToDict
from jitx.run.runtime import Runtime
from jitx._websocket import Message
from jitxcore._proto import messages_pb2
from jitx._runtime._legacy_plugins import do_export
B=Path('/Users/philippe/dev/copper-scar-jitx');R=B/'runs/import-ab-20260912';name='pcbgolf_import.current.PcbgolfFull'
async def main():
 uri=json.loads((B/'.jitx/runtime.json').read_text())['websocket_uri'].rstrip('/')
 async with Runtime(uri=uri) as r:
  conv=await r._client.root().request(Message('des','request',messages_pb2.Request(design_name=name,physical_design=messages_pb2.PhysicalDesignRequest(get_layout_output=messages_pb2.GetLayoutOutputQuery()))))
  captured=False
  async for env in conv:
   print("response envelope",env.ns,env.type,str(env.body)[:700],flush=True)
   with env.process(namespace='des') as des:
    @des
    def response(response:messages_pb2.Response):
     nonlocal captured
     layout=response.physical_design.layout_output.output
     (R/'captured-layout.pb').write_bytes(layout.SerializeToString())
     (R/'captured-layout.json').write_text(json.dumps(MessageToDict(layout),indent=2))
     captured=True;print('Captured layout',len(layout.SerializeToString()),flush=True)
  assert captured
  print('Export:',await do_export('kicad',name),flush=True)
asyncio.run(asyncio.wait_for(main(),55))
