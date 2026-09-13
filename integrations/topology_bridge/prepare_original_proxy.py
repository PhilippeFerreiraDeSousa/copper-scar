"""Create a full-board native proxy from imported parts and a recorded pose seed.

No routed state or static copper is imported. The new native parent is evaluated
on its own terms and is never compared as incremental to the seed's routed board.
"""
import ast
import hashlib
import json
from pathlib import Path
import shutil
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'original_bridge'))
from prepare_geometry_probe import pad_ports
root=Path(sys.argv[1]).resolve();root.mkdir(exist_ok=False);rt=root/'runtime';rt.mkdir()
source=Path('/Users/philippe/dev/copper-scar-jitx-worktree/integrations/jitx/project/pcbgolf_import');assets=Path('/Users/philippe/dev/copper-scar-jitx/pcbgolf_import')
shutil.copytree(source,rt/'proxy_import',ignore=shutil.ignore_patterns('__pycache__'))
for p in assets.rglob('*.step'):shutil.copy2(p,rt/'proxy_import'/p.relative_to(assets))
seed=Path(__file__).resolve().parents[2]/'.local/original-board-qualification-reproduction/physical-inventories/jitx-native.json'
data=json.loads(seed.read_text());tree=ast.parse((source/'Pcbgolf.py').read_text());aliases={};refs={}
for node in tree.body:
    if isinstance(node,ast.ImportFrom) and node.module=='components.UNKNOWN':
        for a in node.names:aliases[a.asname or a.name]=a.name
    if isinstance(node,ast.ClassDef):
        for n in node.body:
            if isinstance(n,ast.Assign) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Attribute) and n.value.func.attr=='Device':refs[n.targets[0].id]=aliases[n.value.func.value.id]
lines=['from jitx.circuit import Circuit, Route','from jitx.design import Design','from jitx.net import Net','from proxy_import.stage_one_002 import FeasibilityBoard','from proxy_import.board import DesignRules, SubstratePcbgolf','class ProxyRules(DesignRules):','    min_copper_copper_space=.0762','class ProxySubstrate(SubstratePcbgolf):','    constraints=ProxyRules()']
for ref,device in sorted(refs.items()):lines.append(f'from proxy_import.components.UNKNOWN.{device} import Device as {ref}Device')
lines+=['class ProxyCircuit(Circuit):'];nets={};ports={};components={}
for ref,fp in sorted(data['footprints'].items()):
    x,y,angle=fp['pose'];xy=[x-432,279.5-y];components[ref]={'xy':xy,'angle_deg':angle}
    lines.append(f'    {ref} = {ref}Device().at({xy[0]!r},{xy[1]!r},rotate={angle!r})')
    mapping=pad_ports(source/'components/UNKNOWN'/f'{refs[ref]}.py')
    if ref=='SW1':mapping={'A':'P',"A'":'P1','B':'S',"B'":'S1'}
    for p in fp['pads']:
        if p['net']:
            target='self.'+ref+'.'+mapping[p['name']];nets.setdefault(p['net'],set()).add(target);ports[ref+'.'+p['name']]=target
lines+=['    def __init__(self):']
for ref in refs:lines.append(f'        self.{ref}.reference_designator = {ref!r}')
lines.append('        self.nets=[')
for net,members in sorted(nets.items()):lines.append(f'            Net([{", ".join(sorted(members))}],name={net!r}),')
lines+=['        ]']
route_nets=['Net-(J2-CMD)','SD_CMD','SD_D0'];route_manifest=[]
for net in route_nets:
    members=sorted(nets[net])
    for i,(a,b) in enumerate(zip(members,members[1:])):
        key='route_'+str(len(route_manifest));lines.append(f'        self.{key}=Route({a},{b},0)');route_manifest.append({'key':key,'net':net,'source':a,'destination':b,'layer':0})
lines+=['class FullBoardProxy(Design):','    circuit=ProxyCircuit()','    board=FeasibilityBoard()','    substrate=ProxySubstrate()','']
pkg=rt/'original_proxy';pkg.mkdir();(pkg/'__init__.py').write_text('');(pkg/'design.py').write_text('\n'.join(lines));(root/'source.py').write_text('\n'.join(lines))
(rt/'pyproject.toml').write_text('[project]\nname="original-captured-proxy"\nversion="0.1.0"\nrequires-python=">=3.12"\ndependencies=["jitx==4.4.0","jitxlib-standard==4.4.0"]\n')
manifest={'kind':'full-original-board-single-routing-layer-proxy','components':components,'complete_component_count':len(refs),'net_memberships':data['net_memberships'],'route_intent':route_manifest,'pose_seed_board_sha256':data['board_sha256'],'pose_seed_inventory_sha256':hashlib.sha256(seed.read_bytes()).hexdigest(),'comparison_parent':'new disposable native parent; seed routed state is NOT preserved or used as baseline','pad_aliases':{'SW1.A0':'SW1.A','SW1.A1':"SW1.A'",'SW1.B0':'SW1.B','SW1.B1':"SW1.B'"},'routing_layer':0,'min_copper_clearance_mm':.0762,'min_copper_width_mm':.1016,'stackup':'imported 2-conductor layer native profile; no vias','source_files_sha256':{str(p.relative_to(source)):hashlib.sha256(p.read_bytes()).hexdigest() for p in source.rglob('*.py')}}
(root/'preparation.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps({'components':len(refs),'explicit_routes':len(route_manifest),'output':str(root)}))
