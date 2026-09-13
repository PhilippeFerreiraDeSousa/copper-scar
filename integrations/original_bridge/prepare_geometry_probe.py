"""Prepare four real imported components for geometry-only export qualification.

No placement/routing experiment: external terminal inventory stays in a complete
boundary manifest. This subset never claims to model the omitted board obstacles.
"""
from pathlib import Path
import argparse
import ast
import hashlib
import json
import shutil

COMPONENTS={'R37':'RC0402FR_0710KL','R42':'RMCF0402ZT0R00','J2':'Comp_47219_2001','U3':'STM32H725ZGT'}

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def pad_ports(path):
    result={}
    tree=ast.parse(path.read_text())
    for node in ast.walk(tree):
        if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id=='PadMapping':
            d=node.args[0]
            for port,pads in zip(d.keys,d.values):
                for pad in pads.elts if isinstance(pads,(ast.List,ast.Tuple)) else [pads]:
                    name=str(ast.literal_eval(pad.slice)) if isinstance(pad,ast.Subscript) else pad.attr
                    result[name]=ast.unparse(port)
    return result

def prepare(root,source,assets,inventory,correct_mask):
    root.mkdir(parents=True,exist_ok=False);module=root/'qualified_import'
    shutil.copytree(source,module,ignore=shutil.ignore_patterns('__pycache__'))
    manifest={'source_files':{},'external_assets':{},'changes':[]}
    for p in source.rglob('*.py'):manifest['source_files'][str(p.relative_to(source))]=sha(p)
    for p in assets.rglob('*.step'):
        target=module/p.relative_to(assets);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
        manifest['external_assets'][str(p.relative_to(assets))]=sha(p)
    if correct_mask:
        for relative in ('landpatterns/LandpatternU0402_R.py','components/UNKNOWN/Comp_47219_2001.py'):
            p=module/relative;before=p.read_text();after=before.replace('join_style=JOIN_STYLE.mitre','join_style=JOIN_STYLE.round')
            if before==after:raise ValueError('Expected specific mask-expansion helper not found')
            p.write_text(after);manifest['changes'].append({'file':relative,'before_sha256':hashlib.sha256(before.encode()).hexdigest(),'after_sha256':sha(p),'change':'Round mask offset corners to match native KiCad margin semantics; copper and pad poses unchanged'})
    data=json.loads(inventory.read_text());fps=data['footprints'];by_net={};members={}
    lines=['from jitx.design import Design','from jitx.circuit import Circuit','from jitx.net import Net',
           'from qualified_import.board import BoardPcbgolf, SubstratePcbgolf']
    for ref,c in COMPONENTS.items():lines.append(f'from qualified_import.components.UNKNOWN.{c} import Device as {ref}Device')
    lines+=['','class InterfaceCircuit(Circuit):']
    for ref,c in COMPONENTS.items():
        x,y,angle=fps[ref]['pose']
        if angle!=0:raise ValueError('Geometry probe supports these four unrotated parent poses only')
        lines.append(f'    {ref} = {ref}Device().at({x-150}, {150-y})')
        mapping=pad_ports(module/'components/UNKNOWN'/f'{c}.py')
        for p in fps[ref]['pads']:
            if p['net']:
                if p['name'] not in mapping:raise ValueError('Unmapped physical pin '+ref+'.'+p['name'])
                by_net.setdefault(p['net'],set()).add('self.'+ref+'.'+mapping[p['name']]);members.setdefault(p['net'],[]).append(ref+'.'+p['name'])
    lines+=['    def __init__(self):']
    for ref in COMPONENTS:lines.append(f'        self.{ref}.reference_designator = {ref!r}')
    lines.append('        self.nets = [')
    for net,ports in sorted(by_net.items()):lines.append(f'            Net([{", ".join(sorted(ports))}], name={net!r}),')
    lines+=['        ]','','class InterfaceQualification(Design):','    circuit = InterfaceCircuit()',
            '    board = BoardPcbgolf()','    substrate = SubstratePcbgolf()']
    pkg=root/'original_interface';pkg.mkdir();(pkg/'__init__.py').write_text('');(pkg/'design.py').write_text('\n'.join(lines)+'\n')
    boundary={n:{'included':sorted(members[n]),'external':sorted(set(data['net_memberships'][n])-set(members[n]))} for n in members}
    manifest.update(kind='geometry_only_original_component_qualification',parent_sha256=data['board_sha256'],
        complete_interface_pad_count=sum(len(fps[r]['pads']) for r in COMPONENTS),boundaries=boundary,
        routing_authorized=False,omitted_board_obstacles=sorted(set(fps)-set(COMPONENTS)),
        stack_scope='Imported two-layer geometry probe only; does not qualify six-layer parent',source_sha256=sha(pkg/'design.py'))
    (root/'preparation.json').write_text(json.dumps(manifest,indent=2))
    (root/'pyproject.toml').write_text('[project]\nname="original-interface-geometry"\nversion="0.1.0"\ndependencies=["jitx==4.4.0","jitxlib-standard==4.4.0"]\nrequires-python=">=3.12"\n')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for key in ('root','source','assets','inventory'):p.add_argument('--'+key,type=Path,required=True)
    p.add_argument('--correct-mask',action='store_true');a=p.parse_args();prepare(a.root,a.source,a.assets,a.inventory,a.correct_mask)
