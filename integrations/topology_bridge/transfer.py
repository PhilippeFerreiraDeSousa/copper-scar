"""Transfer exported straight copper and through vias to fixed source Copper.

Creates a new fixture project. Records primitive provenance and tests source
Copper separately from mutable Route requests; never changes the input board.
"""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
import sexpdata as sx
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'placement_bridge'))
from verify_incremental_fixture import children, one
from planner import fixture_parent

HERE=Path(__file__).resolve().parent

def transfer(parent, root, native, checker):
    root=root.resolve();root.mkdir(parents=True,exist_ok=False);rt=root/'runtime';rt.mkdir();(rt/'bridge_fixture').mkdir();(rt/'bridge_fixture/__init__.py').write_text('')
    shutil.copy2(parent.parent/'runtime/pyproject.toml',rt/'pyproject.toml')
    board=sx.loads(next((parent/'export').glob('*.kicad_pcb')).read_text())
    if children(board,'arc'): raise ValueError('Arc transfer not qualified by this proof')
    nets={int(n[1]):str(n[2]) for n in children(board,'net')}
    manifest=fixture_parent();footprints=children(board,'footprint');first=next(f for f in footprints if next(str(t[2]) for t in children(f,'fp_text') if str(t[1])=='reference')=='TP1')
    x,y=one(first,'at')[1:3];dx=float(x)+12;dy=float(y)+10
    def local(point): return [float(point[0])-dx,dy-float(point[1])]
    records=[]
    for i,s in enumerate(children(board,'segment')):
        records.append({'key':f'copper_{i}','net':nets[int(one(s,'net')[1])],'layer':0 if str(one(s,'layer')[1])=='F.Cu' else 1,'start':local(one(s,'start')[1:]),'end':local(one(s,'end')[1:]),'width':float(one(s,'width')[1])})
    vias=[{'key':f'via_{i}','net':nets[int(one(v,'net')[1])],'xy':local(one(v,'at')[1:]),'diameter':float(one(v,'size')[1]),'drill':float(one(v,'drill')[1])} for i,v in enumerate(children(board,'via'))]
    base=(HERE.parent/'placement_bridge/incremental_fixture/design.py').read_text()
    lines=['from jitx.copper import Copper as FixedCopper, Pour','from jitx.shapes.shapely import ShapelyGeometry','from shapely.geometry import LineString, box','','class Transferred(ProofCircuit):','    def __init__(self):']
    for r in records:
        lines.append(f"        self.{r['key']} = FixedCopper(ShapelyGeometry(LineString({[r['start'],r['end']]!r}).buffer({r['width']/2!r}, quad_segs=64)), {r['layer']})")
    for v in vias:
        if v['diameter']!=.6 or v['drill']!=.3: raise ValueError('Unsupported via dimensions')
        lines.append(f"        self.{v['key']} = ProofSubstrate.ThroughVia().at({v['xy'][0]!r}, {v['xy'][1]!r})")
    for net,n in manifest['nets'].items():
        ref=n['ports'][0].split('.')[0];port='self.'+manifest['components'][ref]['attribute']+'.p'
        objects=[port]+['self.'+r['key'] for r in records+vias if r['net']==net]
        lines.append(f"        self.fixed_{net.lower()} = Net([{', '.join(objects)}])")
    # Separate exact rectangular fixed-plane region attached to HOLD through a
    # concrete via. Its declared and exported polygon can be audited independently.
    lines += ["        self.plane = FixedCopper(ShapelyGeometry(box(-13,9,-11,11)), 1)","        self.plane_via = ProofSubstrate.ThroughVia().at(-12,10)","        self.plane_net = Net([self.hold_left.p, self.plane, self.plane_via])",'', 'class BridgeProof(Design):','    circuit = Transferred()','    board = ProofBoard()','    substrate = ProofSubstrate()','']
    source=base+'\n'+'\n'.join(lines);(rt/'bridge_fixture/design.py').write_text(source);(root/'source.py').write_text(source)
    (root/'transfer-manifest.json').write_text(json.dumps({'source_board':str(next((parent/'export').glob('*.kicad_pcb'))),'frame':{'dx':dx,'dy':dy},'segments':records,'vias':vias,'added_plane':{'net':'HOLD','layer':1,'bounds':[-13,9,-11,11]},'maximum_round_cap_sagitta_mm':.1*(1-__import__('math').cos(__import__('math').pi/256))},indent=2))
    commands=[]
    def command(args):
        t=time.monotonic();r=subprocess.run(list(map(str,args)),cwd=rt,env=dict(os.environ,PYTHONPATH=str(rt)),capture_output=True,text=True,timeout=360)
        i=len(commands);(root/f'{i:02}.stdout').write_text(r.stdout);(root/f'{i:02}.stderr').write_text(r.stderr);commands.append({'argv':list(map(str,args)),'returncode':r.returncode,'elapsed_s':time.monotonic()-t});(root/'commands.json').write_text(json.dumps(commands,indent=2))
        if r.returncode: raise RuntimeError(f'Command {i} failed')
    cli=native.parent/'jitx';command([cli,'runtime','start','--project',rt,'--bg']);command([cli,'design','build','bridge_fixture.design.BridgeProof','--no-dependency-check'])
    plan=root/'empty.json';plan.write_text('[]');command([native,HERE.parent/'placement_bridge/fixture_control.py',plan,root/'01-transferred']);command([checker,HERE/'evaluate.py',root/'01-transferred']);command([cli,'runtime','stop','--project',rt])

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('parent',type=Path);p.add_argument('root',type=Path);p.add_argument('--native-python',type=Path,required=True);p.add_argument('--checker-python',type=Path,required=True);a=p.parse_args();transfer(a.parent.resolve(),a.root,a.native_python.absolute(),a.checker_python.absolute())
