"""Isolate supported Runtime.submit(root) behavior before and after capture."""
import asyncio
import json
from pathlib import Path
import sys
import traceback
from jitx.run.runtime import Runtime
from jitx._runtime._legacy_plugins import do_export
from jitx.circuit import Route
from jitx.via import Via,ViaType
from jitx.proxy import typeof
from bridge_fixture.design import BridgeProof
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'placement_bridge'))
import fixture_control
async def main(out):
    out.mkdir(exist_ok=False);name='bridge_fixture.design.BridgeProof'
    uri=json.loads(Path('.jitx/runtime.json').read_text())['websocket_uri'].rstrip('/')
    async with Runtime(uri=uri) as rt:
        rd=await asyncio.wait_for(rt.submit(BridgeProof,name=name),60)
        await fixture_control.execute([],out/'00-submitted')
        def record(label):
            rows=[{'path':str(p.path),'python_type':type(v).__name__,'jitx_type':typeof(v).__name__,'drill_type':repr(v.type),'is_enum':isinstance(v.type,ViaType),'diameter':v.diameter,'hole':v.hole_diameter} for p,v in rd.query(Via)]
            routes=[{'path':str(p.path),'layer':r.layer,'traces':len(r.traces or []),'endpoints':[{'jitx_type':typeof(v).__name__,'drill_type':repr(v.type) if isinstance(v,Via) else None} for v in (r.source,r.destination)]} for p,r in rd.query(Route)]
            (out/(label+'.json')).write_text(json.dumps({'vias':rows,'routes':routes,'direct_via_type':repr(rd.root.circuit.cross_a_escape_b.type)},indent=2))
        record('00-object')
        try:rd=await asyncio.wait_for(rt.submit(rd.root,name=name),60)
        except Exception:
            (out/'01-uncaptured-resubmit-error.txt').write_text(traceback.format_exc());return
        await fixture_control.execute([],out/'01-uncaptured-resubmitted')
        await asyncio.wait_for(rd.capture(),60);record('02-captured-object')
        try:rd=await asyncio.wait_for(rt.submit(rd.root,name=name),60)
        except Exception:
            (out/'03-captured-resubmit-error.txt').write_text(traceback.format_exc());return
        await fixture_control.execute([],out/'03-captured-resubmitted')
asyncio.run(main(Path(sys.argv[1]).resolve()))
