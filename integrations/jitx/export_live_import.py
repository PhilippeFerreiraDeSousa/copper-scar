"""Export the already loaded design without rebuilding or replacing its layout."""
import asyncio,json,logging
from pathlib import Path
from jitx.run.runtime import Runtime
from jitx._runtime._legacy_plugins import do_export
B=Path('/Users/philippe/dev/copper-scar-jitx')
logging.basicConfig(level=logging.INFO)
async def main():
 uri=json.loads((B/'.jitx/runtime.json').read_text())['websocket_uri'].rstrip('/')
 async with Runtime(uri=uri):
  print(await do_export('kicad','pcbgolf_import.main.PcbgolfImported'),flush=True)
asyncio.run(asyncio.wait_for(main(),55))
