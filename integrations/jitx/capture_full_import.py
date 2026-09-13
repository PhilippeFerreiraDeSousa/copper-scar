"""Capture the full imported runtime design and request independent KiCad export."""
from pathlib import Path
import sys,json,asyncio,logging
BASE=Path('/Users/philippe/dev/copper-scar-jitx');RUN=BASE/'runs/import-ab-20260912'
sys.path.insert(0,str(BASE))
from pcbgolf_import.main import PcbgolfImported
from jitx.run.runtime import Runtime
from jitx.component import Component
from jitx._runtime._legacy_plugins import do_export
logging.basicConfig(level=logging.INFO)
async def main():
 uri=json.loads((BASE/'.jitx/runtime.json').read_text())['websocket_uri'].rstrip('/')
 async with Runtime(uri=uri) as r:
  print('Submitting',flush=True);d=await r.submit(PcbgolfImported)
  print('Capturing',flush=True);await d.capture()
  comps=[dict(path=str(t.path),reference=str(c.reference_designator),mpn=str(c.mpn),transform=str(t.transform)) for t,c in d.query(Component)]
  (RUN/'runtime-components.json').write_text(json.dumps(comps,indent=2));print('Captured components',len(comps),flush=True)
  print('Export result:',await do_export('kicad',d.name),flush=True)
asyncio.run(asyncio.wait_for(main(),timeout=100))
