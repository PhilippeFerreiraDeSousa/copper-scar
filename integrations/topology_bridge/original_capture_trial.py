"""Bounded full-board capture/KRT/move/evaluate trial; no imported legacy copper."""
import asyncio
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
from jitx.run.runtime import Runtime
from jitx._runtime._legacy_plugins import do_export
from jitx._websocket import Message
from jitx.inspect import extract
from jitx.circuit import Route
from original_proxy.design import FullBoardProxy

HERE=Path(__file__).resolve().parent
ORIGINAL=HERE.parent/'original_bridge'
CHECKER=Path('/Users/philippe/dev/copper-scar-demo/.venv/bin/python')
KPY='/Users/philippe/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3'
DESIGN='original_proxy.design.FullBoardProxy'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
async def main(root):
    evidence=root/'evidence';evidence.mkdir(exist_ok=False);manifest=json.loads((root/'preparation.json').read_text());ops=[]
    def command(args,label):
        t=time.monotonic();p=subprocess.run(list(map(str,args)),capture_output=True,text=True,timeout=180)
        (evidence/(label+'.stdout')).write_text(p.stdout);(evidence/(label+'.stderr')).write_text(p.stderr)
        ops.append({'command':list(map(str,args)),'elapsed_s':time.monotonic()-t,'returncode':p.returncode});(evidence/'operations.json').write_text(json.dumps(ops,indent=2))
        if p.returncode:raise RuntimeError(label+' failed')
    uri=json.loads(Path('.jitx/runtime.json').read_text())['websocket_uri'].rstrip('/')
    async with Runtime(uri=uri) as runtime:
        async def submit(design,label):
            Path('.capture-uncertain.json').write_text(json.dumps({'operation':label,'evidence':str(evidence)}))
            t=time.monotonic();rd=await asyncio.wait_for(runtime.submit(design),180)
            ops.append({'operation':label,'elapsed_s':time.monotonic()-t});(evidence/'operations.json').write_text(json.dumps(ops,indent=2));return rd
        async def snapshot(label):
            stage=evidence/label;stage.mkdir()
            await asyncio.wait_for(do_export('kicad',DESIGN),180)
            replies=[]
            async def read():
                conv=await runtime._client.route('design/'+DESIGN).request(Message('phd','load',{}))
                async for m in conv:replies.append({'type':m.type,'body':m.body})
            await asyncio.wait_for(read(),60)
            (stage/'final.json').write_text(json.dumps(replies,indent=2));shutil.copytree(Path('designs')/DESIGN/'kicad',stage/'export')
            (stage/'completion.json').write_text(json.dumps({'export_barrier':True,'timestamp':time.time(),'native_worker_state':'completed'}));Path('.capture-uncertain.json').unlink(missing_ok=True)
            command([CHECKER,ORIGINAL/'normalize_probe_export.py',stage/'export',stage/'normalized'],label+'-normalize')
            board=next((stage/'normalized').glob('*.kicad_pcb'))
            command([KPY,ORIGINAL/'native_inventory.py',board,stage/'inventory.json'],label+'-inventory')
            command([CHECKER,ORIGINAL/'check_project_copies.py',stage/'normalized',stage/'whole-board-check'],label+'-drc')
            inv=json.loads((stage/'inventory.json').read_text());drc=json.loads((stage/'whole-board-check/summary.json').read_text())
            # Every original physical net boundary and obstacle component is present.
            canonical_members={n:sorted(manifest['pad_aliases'].get(p,p) for p in ps) for n,ps in inv['net_memberships'].items()}
            if set(inv['footprints'])!=set(manifest['components']) or canonical_members!=manifest['net_memberships']:
                (stage/'gate-failure.json').write_text(json.dumps({'components_equal':set(inv['footprints'])==set(manifest['components']),'net_memberships_equal':canonical_members==manifest['net_memberships']},indent=2));raise ValueError('Full parent mapping gate failed')
            measurement=json.loads(subprocess.check_output([KPY,str(HERE/'measure.py'),str(board)],text=True))
            return stage,inv,drc,measurement
        async def capture(rd):
            prior=list(extract(rd.root,Route));await asyncio.wait_for(rd.capture(),120)
            present=list(extract(rd.root,Route));lost=[r for r in prior if not any(r is p for p in present)]
            if lost:rd.root.circuit.retained_routes=[*getattr(rd.root.circuit,'retained_routes',[]),*lost]
            return {'route_count':len(list(extract(rd.root,Route))),'restored_objects':len(lost)}
        rd=await submit(FullBoardProxy,'submit_new_native_parent');parent=await snapshot('00-parent')
        cap=await capture(rd);(evidence/'00-capture.json').write_text(json.dumps(cap,indent=2))
        rd=await submit(rd.root,'captured_parent_roundtrip');roundtrip=await snapshot('01-roundtrip')
        # Compare parsed records excluding regenerated UUIDs and numeric net IDs.
        command([CHECKER,HERE/'compare_original.py',parent[0],roundtrip[0],evidence/'roundtrip-comparison.json'],'roundtrip-compare')
        if not json.loads((evidence/'roundtrip-comparison.json').read_text())['common_parent_equal']:raise ValueError('Captured native parent geometry, rules or twice-DRC changed on roundtrip')
        config={'groups':{r:[r] for r in manifest['components'] if r not in ('R37','R42')},'translation_candidates_mm':[[-2,0],[2,0],[0,-2],[0,2]],'proxy_ignored_nets':[],'clearance_mm':.25,'board_edge_clearance_mm':.025}
        config['groups']['interface_pair']=['R37','R42'];cfg=evidence/'research-config.json';cfg.write_text(json.dumps(config,indent=2));proposal_file=evidence/'research-proposal.json';board=next((roundtrip[0]/'normalized').glob('*.kicad_pcb'))
        command([CHECKER,HERE/'research_proposals.py',board.parent,'--board-name',board.name,'--group','interface_pair','--manifest',cfg,'--output',proposal_file],'research')
        proposal=json.loads(proposal_file.read_text());assert proposal['parent_board_sha256']==sha(board)
        dx,dy=proposal['translation_mm'];await capture(rd)
        for ref in proposal['refs']:
            actual=roundtrip[1]['footprints'][ref]['pose'];claimed=proposal['from_poses'][ref]
            assert all(abs(claimed[k]-v)<1e-6 for k,v in zip(('x_mm','y_mm','angle_deg'),actual))
            c=manifest['components'][ref];getattr(rd.root.circuit,ref).at(c['xy'][0]+dx,c['xy'][1]-dy,rotate=c['angle_deg'])
        rd=await submit(rd.root,'captured_group_move');candidate=await snapshot('02-candidate')
        command([CHECKER,HERE/'compare_original.py',roundtrip[0],candidate[0],evidence/'candidate-comparison.json'],'candidate-compare')
        comparison=json.loads((evidence/'candidate-comparison.json').read_text());affected=set(proposal['nets']);unchanged=all(n in affected for n in comparison['changed_copper_nets'])
        p=roundtrip[2]['runs'][0];c=candidate[2]['runs'][0]
        def errors(stage):
            report=json.loads((stage/'whole-board-check/drc-0.json').read_text())
            return {(v['type'],tuple(sorted(i['description'] for i in v.get('items',[])))) for v in report['violations'] if v['severity']=='error'}
        new_errors=errors(candidate[0])-errors(roundtrip[0])
        retain=not new_errors and c['opens']<=p['opens'] and c['counts'].get('error',0)<=p['counts'].get('error',0) and unchanged and comparison['changed_refs']==sorted(proposal['refs']) and candidate[3]['wire_length_mm']<roundtrip[3]['wire_length_mm'] and comparison['project_rules_equal']
        result={'scope':'complete245-component original-board proxy','comparison':'new native parent only, not seed legacy routed parent','single_layer_routes':True,'dielectric_or_product_qualification':False,'new_error_signatures':[list(x) for x in sorted(new_errors)],'capture_parent_equal':True,'proposal_sha256':sha(proposal_file),'translation_mm':[dx,dy],'parent_drc':p,'candidate_drc':c,'parent_metrics':roundtrip[3],'candidate_metrics':candidate[3],'comparison_details':comparison,'unaffected_copper_preserved':unchanged,'decision':'retain' if retain else 'reject'}
        (evidence/'result.json').write_text(json.dumps(result,indent=2))
        if not retain:
            # Revert only the two public placement fields, never managed files.
            await capture(rd)
            for ref in proposal['refs']:
                p=manifest['components'][ref];getattr(rd.root.circuit,ref).at(*p['xy'],rotate=p['angle_deg'])
            rd=await submit(rd.root,'restore_parent_after_reject');restored=await snapshot('03-restored-parent')
            command([CHECKER,HERE/'compare_original.py',roundtrip[0],restored[0],evidence/'restored-parent-comparison.json'],'restored-parent-compare')
            if not json.loads((evidence/'restored-parent-comparison.json').read_text())['common_parent_equal']:raise ValueError('Rejected candidate did not restore common parent')
asyncio.run(main(Path(sys.argv[1]).resolve()))
