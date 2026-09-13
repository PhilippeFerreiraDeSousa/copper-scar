"""Read-only export barrier after timeout; preserves uncertainty marker."""
import asyncio
import json
from pathlib import Path
import shutil
import sys
from jitx.run.runtime import Runtime
from jitx._runtime._legacy_plugins import do_export
from jitx._websocket import Message
async def main(out):
    out.mkdir(exist_ok=False)
    uri=json.loads(Path('.jitx/runtime.json').read_text())['websocket_uri'].rstrip('/')
    async with Runtime(uri=uri) as rt:
        await asyncio.wait_for(do_export('kicad','bridge_fixture.design.BridgeProof'),30)
        replies=[]
        async def read():
            conv=await rt._client.route('design/bridge_fixture.design.BridgeProof').request(Message('phd','load',{}))
            async for r in conv: replies.append({'type':r.type,'body':r.body})
        await asyncio.wait_for(read(),30)
        (out/'final.json').write_text(json.dumps(replies,indent=2))
        shutil.copytree('designs/bridge_fixture.design.BridgeProof/kicad',out/'export')
        (out/'completion.json').write_text(json.dumps({'export_barrier':True,'read_only_reconciliation':True,'original_operation_reply_timed_out':True}))
asyncio.run(main(Path(sys.argv[1])))
