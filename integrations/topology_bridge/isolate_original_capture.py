"""Disposable capture isolation; public lifecycle, crash-aware bounded calls."""
import asyncio
import json
from pathlib import Path
import shutil
import sys
import time
import traceback
from jitx.run.runtime import Runtime
from jitx._runtime._legacy_plugins import do_export
from original_proxy.design import FullBoardProxy

async def main(mode):
    out=Path('../evidence');out.mkdir(exist_ok=False)
    uri=json.loads(Path('.jitx/runtime.json').read_text())['websocket_uri'].rstrip('/')
    log=Path('.jitx/logs/runtime.log');events=[]
    async def bounded(awaitable,label):
        start=time.monotonic();offset=log.stat().st_size if log.exists() else 0
        task=asyncio.create_task(awaitable)
        try:
            for _ in range(120):
                done,_=await asyncio.wait({task},timeout=.5)
                if done:
                    value=task.result();events.append({'operation':label,'status':'completed','seconds':time.monotonic()-start});return value
                with log.open() as stream:
                    stream.seek(offset);new=stream.read()
                if 'FATAL ERROR' in new:raise RuntimeError('Native FATAL ERROR during '+label)
            raise TimeoutError(label+' exceeded60s')
        finally:
            if not task.done():
                task.cancel()
                try:await task
                except asyncio.CancelledError:pass
            (out/'operations.json').write_text(json.dumps(events,indent=2))
    async with Runtime(uri=uri) as rt:
        try:
            rd=await bounded(rt.submit(FullBoardProxy),'initial_submit')
            await bounded(do_export('kicad',rd.name),'initial_export')
            shutil.copytree(Path('designs')/rd.name/'kicad',out/'00-parent')
            if mode=='capture':await bounded(rd.capture(),'capture')
            rd=await bounded(rt.submit(FullBoardProxy if mode=='fresh' else rd.root),'resubmit_'+mode)
            await bounded(do_export('kicad',rd.name),'roundtrip_export')
            shutil.copytree(Path('designs')/rd.name/'kicad',out/'01-roundtrip')
            result={'status':'completed','mode':mode}
        except Exception:
            result={'status':'failed','mode':mode,'error':traceback.format_exc()}
        (out/'result.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
asyncio.run(main(sys.argv[1]))
