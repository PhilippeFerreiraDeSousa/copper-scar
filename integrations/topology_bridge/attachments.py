"""Paired fresh-runtime comparison of attachment-only and authored Routes."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import time
from planner import fixture_parent, propose, render
HERE=Path(__file__).resolve().parent
BRIDGE=HERE.parent/'placement_bridge'

def run(root,native,checker):
    root=root.resolve();root.mkdir(parents=True,exist_ok=False);rows=[]
    for mode in ('attachments_only','explicit_routes'):
        output=root/mode;output.mkdir();rt=output/'runtime';rt.mkdir();(rt/'bridge_fixture').mkdir();(rt/'bridge_fixture/__init__.py').write_text('')
        (rt/'pyproject.toml').write_text('[project]\nname="attachment-proof"\nversion="0.1.0"\nrequires-python=">=3.12"\ndependencies=["jitx==4.4.0","jitxlib-standard==4.4.0"]\n')
        candidate=propose(fixture_parent(),{'TP4':[10,8]},offsets=(2,))[0]
        source=render((BRIDGE/'incremental_fixture/design.py').read_text(),candidate)
        if mode=='attachments_only': source='\n'.join(l for l in source.splitlines() if ' = Route(' not in l)+'\n'
        (rt/'bridge_fixture/design.py').write_text(source);(output/'source.py').write_text(source)
        commands=[]
        def command(args):
            t=time.monotonic();r=subprocess.run(list(map(str,args)),cwd=rt,env=dict(os.environ,PYTHONPATH=str(rt)),capture_output=True,text=True,timeout=360)
            i=len(commands);(output/f'{i:02}.stdout').write_text(r.stdout);(output/f'{i:02}.stderr').write_text(r.stderr);commands.append({'argv':list(map(str,args)),'returncode':r.returncode,'elapsed_s':time.monotonic()-t});(output/'commands.json').write_text(json.dumps(commands,indent=2))
            if r.returncode: raise RuntimeError(f'{mode} command {i} failed')
        cli=native.parent/'jitx';command([cli,'runtime','start','--project',rt,'--bg']);command([cli,'design','build','bridge_fixture.design.BridgeProof','--no-dependency-check'])
        def control(plan,name):
            p=output/(name+'-plan.json');p.write_text(json.dumps(plan,indent=2));stage=output/name
            command([native,BRIDGE/'fixture_control.py',p,stage]);command([checker,HERE/'evaluate.py',stage]);return json.loads((stage/'independent/summary.json').read_text())
        initial=control([],'00-build')
        messages=json.loads((output/'00-build/final.json').read_text());board=next(m['body'] for m in messages if m['type']=='board')
        pads=[o['pad'] for g in board['module']['groups'] for i in g['instances'] for o in i['objects'] if 'pad' in o]
        vias=next(m['body']['vias'] for m in messages if m['type']=='via-info')
        # Identical policy/number of calls in both modes; identifiers resolved per runtime.
        selected=sorted(pads+list(vias))
        final=control([{'type':'route','body':{'layer':0,'pads':selected,'force':False,'configure':None}},{'type':'route','body':{'layer':1,'pads':sorted(vias),'force':False,'configure':None}}],'01-layer-routed')
        rows.append({'mode':mode,'source_build':{k:initial[k] for k in ('opens','violations','via_count','copper_by_net')},'after_same_layer_calls':{k:final[k] for k in ('opens','violations','via_count','copper_by_net')},'policy':{'top':'all pads plus vias','bottom':'all vias','calls':2,'force':False}})
        (root/'results.json').write_text(json.dumps(rows,indent=2));command([cli,'runtime','stop','--project',rt])
    return rows
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('--native-python',type=Path,required=True);p.add_argument('--checker-python',type=Path,required=True);a=p.parse_args();run(a.root,a.native_python.absolute(),a.checker_python.absolute())
