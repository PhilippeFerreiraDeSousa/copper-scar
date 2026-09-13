"""Supported in-memory submit/capture/mutate/resubmit experiment in own runtime."""
import asyncio
import dataclasses
import json
from pathlib import Path
import shutil
import sys
import time
from jitx.run.runtime import Runtime
from jitx._runtime._legacy_plugins import do_export
from jitx._websocket import Message
from jitx.circuit import Route
from jitx.design import Design
from jitx.copper import Copper
from jitx.via import Via, ViaType
from jitx.proxy import typeof
from jitx.inspect import visit, extract
from bridge_fixture.design import BridgeProof
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'placement_bridge'))
import fixture_control

DESIGN='bridge_fixture.design.BridgeProof'

def serialize(x):
    if x is None or isinstance(x,(str,int,float,bool)):return x
    if isinstance(x,(list,tuple)):return [serialize(v) for v in x]
    if isinstance(x,dict):return {str(k):serialize(v) for k,v in x.items()}
    if dataclasses.is_dataclass(x):return {'type':type(x).__name__,**serialize(dataclasses.asdict(x))}
    if hasattr(x,'__dict__'):return {'type':type(x).__name__,**{k:serialize(v) for k,v in vars(x).items() if not k.startswith('_')}}
    return {'type':type(x).__name__,'representation':str(x)}

async def main(out):
    out.mkdir(exist_ok=False);uri=json.loads(Path('.jitx/runtime.json').read_text())['websocket_uri'].rstrip('/')
    operations=[]
    async with Runtime(uri=uri) as runtime:
        async def operation(label,coroutine):
            t=time.monotonic()
            Path('.capture-uncertain.json').write_text(json.dumps({'operation':label,'output':str(out)}))
            value=await asyncio.wait_for(coroutine,120)
            operations.append({'operation':label,'elapsed_s':time.monotonic()-t})
            (out/'operations.json').write_text(json.dumps(operations,indent=2));return value
        async def snapshot(label,name=DESIGN):
            stage=out/label;stage.mkdir()
            await asyncio.wait_for(do_export('kicad',name),120)
            replies=[]
            async def read():
                c=await runtime._client.route('design/'+name).request(Message('phd','load',{}))
                async for m in c:replies.append({'type':m.type,'body':m.body})
            await asyncio.wait_for(read(),60)
            (stage/'final.json').write_text(json.dumps(replies,indent=2));shutil.copytree(Path('designs')/name/'kicad',stage/'export')
            (stage/'completion.json').write_text(json.dumps({'export_barrier':True,'design':name,'native_worker_state':'completed','timestamp':time.time()}))
            Path('.capture-uncertain.json').unlink(missing_ok=True)
            return replies
        def record(rd,label):
            routes=[]
            for path,route in rd.query(Route):
                routes.append({'path':str(path.path),'layer':route.layer,'source_type':type(route.source).__name__,'destination_type':type(route.destination).__name__,'sketch':serialize(route.sketch),'traces':[{'shapes':[serialize(s.geometry.to_primitive()) for s in t.shapes]} for t in route.traces or []]})
            result={'routes':routes,'route_count':len(routes),'via_count':len(list(rd.query(Via))),'queried_copper_including_pad_via_trace_conversions':len(list(rd.query(Copper))),'source_file_automatically_rewritten':False}
            (out/(label+'.json')).write_text(json.dumps(result,indent=2));return result
        async def capture_owned(rd):
            prior=list(extract(rd.root,Route))
            await rd.capture()
            present=list(extract(rd.root,Route))
            dropped=[r for r in prior if not any(r is current for current in present)]
            if dropped:
                rd.root.circuit.retained_routes=[*getattr(rd.root.circuit,'retained_routes',[]),*dropped]
            (out/'retained-capture-events.jsonl').open('a').write(json.dumps({'prior':len(prior),'after_capture':len(present),'preserved_same_objects':len(dropped)})+'\n')
        rd=await operation('initial_public_submit',runtime.submit(BridgeProof,name=DESIGN))
        before=await snapshot('00-attachments')
        b=next(m['body'] for m in before if m['type']=='board');vias=next((m['body']['vias'] for m in before if m['type']=='via-info'),{})
        pads=[o['pad'] for g in b['module']['groups'] for i in g['instances'] for o in i['objects'] if 'pad' in o]
        plan=[{'type':'route','body':{'layer':0,'pads':sorted(pads+list(vias)),'force':False,'configure':None}},{'type':'route','body':{'layer':1,'pads':sorted(vias),'force':False,'configure':None}}]
        if any(m['type']=='routed' for m in before):plan=[]
        elif not vias:plan=plan[:1]
        await fixture_control.execute(plan,out/'01-native-routed')
        await operation('public_capture_generated_routes',capture_owned(rd));captured=record(rd,'01-captured-object')
        assert captured['route_count']==(10 if vias else 4) and all(r['traces'] for r in captured['routes'])
        # Bounded diagnostic correction for a verified 4.4 Proxy.type name
        # collision exposed when capture taints via diameter overrides. Preserve
        # the original declared drill enum; no trace/copper reconstruction.
        corrected=[]
        for path,via in visit(rd.root,Via):
            declared=typeof(via).type
            assert declared==ViaType.MechanicalDrill and via.diameter==.6 and via.hole_diameter==.3
            corrected.append({'path':str(path.path),'before':str(via.type),'declared':str(declared)})
            if via.type!=declared:via.type=declared
        (out/'capture-via-type-correction.json').write_text(json.dumps(corrected,indent=2))
        rd=await operation('resubmit_captured_root_same_identity',runtime.submit(rd.root,name=DESIGN))
        await snapshot('02-captured-resubmitted');await operation('capture_after_resubmit',capture_owned(rd));record(rd,'02-recaptured-object')
        for _,v in visit(rd.root,Via):
            if v.type!=typeof(v).type:v.type=typeof(v).type
        rd.root.circuit.a_right.at(10,8)
        if hasattr(rd.root.circuit,'cross_a_escape_b'):rd.root.circuit.cross_a_escape_b.at(8,8)
        rd=await operation('resubmit_captured_root_moved_component_and_via',runtime.submit(rd.root,name=DESIGN))
        await snapshot('03-moved-resubmitted');await operation('capture_after_move',capture_owned(rd));record(rd,'03-moved-captured-object')
        Path('.capture-uncertain.json').unlink(missing_ok=True)

asyncio.run(main(Path(sys.argv[1]).resolve()))
