"""Reduce only newly generated disposable source; never managed design state."""
import ast
import json
from pathlib import Path
import subprocess
import sys
root=Path(sys.argv[1]).absolute();refs=set(sys.argv[2].split(','))
subprocess.run([sys.executable,str(Path(__file__).with_name('prepare_original_proxy.py')),str(root)],check=True)
source=root/'runtime/original_proxy/design.py';tree=ast.parse(source.read_text())
def ref(expr):
    while isinstance(expr,(ast.Attribute,ast.Subscript)):
        if isinstance(expr,ast.Attribute) and isinstance(expr.value,ast.Name) and expr.value.id=='self':return expr.attr
        expr=expr.value
    return None
for cls in tree.body:
    if isinstance(cls,ast.ClassDef) and cls.name=='ProxyCircuit':
        body=[]
        for node in cls.body:
            if isinstance(node,ast.Assign):
                if node.targets[0].id in refs:body.append(node)
            elif isinstance(node,ast.FunctionDef):
                statements=[]
                for n in node.body:
                    if ref(n.targets[0])=='nets':
                        new=[]
                        for net in n.value.elts:
                            net.args[0].elts=[p for p in net.args[0].elts if ref(p) in refs]
                            if net.args[0].elts:new.append(net)
                        n.value.elts=new;statements.append(n)
                    elif isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name) and n.value.func.id=='Route':
                        if all(ref(p) in refs for p in n.value.args[:2]):statements.append(n)
                    elif ref(n.targets[0]) in refs:statements.append(n)
                node.body=statements or [ast.Pass()];body.append(node)
        cls.body=body
source.write_text(ast.unparse(tree)+'\n');(root/'source.py').write_text(source.read_text())
manifest=json.loads((root/'preparation.json').read_text());manifest['diagnostic_reduction']={'refs':sorted(refs),'full_board':False};(root/'preparation.json').write_text(json.dumps(manifest,indent=2))
if len(sys.argv)>3:
    variant=sys.argv[3]
    assert variant in ('j3-no-standalone-cutouts','j3-no-bottom-pads','j3-no-landpattern-features','j3-single-pad-mapping','j3-split-pad-ports')
    path=root/'runtime/proxy_import/components/UNKNOWN/DX07S024XJ1R1100.py'
    tree=ast.parse(path.read_text())
    for cls in tree.body:
        if isinstance(cls,ast.ClassDef) and cls.name.startswith('Landpattern'):
            for n in cls.body:
                if variant=='j3-no-standalone-cutouts' and isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='cutout':n.value=ast.List(elts=[],ctx=ast.Load())
            if variant=='j3-no-bottom-pads':cls.body=[n for n in cls.body if not (isinstance(n,ast.Assign) and n.targets[0].id in ('S1B','S2B','S3B','S4B'))]
            if variant=='j3-no-landpattern-features':cls.body=[n for n in cls.body if not (isinstance(n,ast.Assign) and isinstance(n.value,ast.List))]
    if variant=='j3-no-bottom-pads':
        for n in ast.walk(tree):
            if isinstance(n,ast.List):n.elts=[v for v in n.elts if not (isinstance(v,ast.Attribute) and isinstance(v.value,ast.Name) and v.value.id=='landpattern' and v.attr in ('S1B','S2B','S3B','S4B'))]
    if variant=='j3-single-pad-mapping':
        for n in ast.walk(tree):
            if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='PadMapping':
                n.args[0].values=[v.elts[0] if isinstance(v,ast.List) else v for v in n.args[0].values]
    path.write_text(ast.unparse(tree)+'\n')
    if variant=='j3-split-pad-ports':
        import shutil
        shutil.copy2(Path(__file__).with_name('split_pad_ports.py'),root/'runtime/split_pad_ports.py')
        generated=ast.parse(source.read_text())
        generated.body.insert(0,ast.ImportFrom(module='split_pad_ports',names=[ast.alias(name='split_pad_ports')],level=0))
        for cls in generated.body:
            if isinstance(cls,ast.ClassDef) and cls.name=='ProxyCircuit':
                init=next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name=='__init__')
                init.body.extend(ast.parse('self.pad_port_ties=split_pad_ports(self.J3)').body)
        source.write_text(ast.unparse(generated)+'\n');(root/'source.py').write_text(source.read_text())
    (root/'diagnostic-variant.json').write_text(json.dumps({'variant':variant,'changes_geometry':True,'production_acceptable':False},indent=2))
