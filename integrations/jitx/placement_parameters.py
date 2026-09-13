"""Parameterize imported placement requests while retaining every unspecified pose.
Overrides are local to the named owning Circuit, never implicitly global coordinates.
"""
from pathlib import Path
import ast,json,math,argparse,hashlib

def render(source,overrides,destination):
 text=source.read_text();tree=ast.parse(text);lines=text.splitlines(keepends=True);starts=[0]
 for line in lines:starts.append(starts[-1]+len(line))
 catalog={};edits=[]
 for cls in tree.body:
  if not isinstance(cls,ast.ClassDef):continue
  for node in ast.walk(cls):
   if not isinstance(node,ast.Call) or not isinstance(node.func,ast.Attribute) or node.func.attr!='place' or ast.unparse(node.func.value)!='self':continue
   assert len(node.args)==2
   target=ast.unparse(node.args[0]);key=cls.name+'.'+target.removeprefix('self.');assert key not in catalog
   catalog[key]={'owner_class':cls.name,'target':target,'initial_expression':ast.unparse(node.args[1]),'frame':'owner circuit local','line':node.lineno}
   if key not in overrides:continue
   p=overrides[key];assert set(p)<= {'x','y','angle','side'} and all(k in p for k in ['x','y','angle'])
   assert all(type(p[k]) in (int,float) and math.isfinite(p[k]) for k in ['x','y','angle'])
   side=p.get('side','top');assert side in ['top','bottom']
   replacement=f'self.place({target}, Transform(({p["x"]!r}, {p["y"]!r}), rotate={p["angle"]!r}), on=Side.{side.title()})'
   edits.append((starts[node.lineno-1]+node.col_offset,starts[node.end_lineno-1]+node.end_col_offset,replacement))
 assert set(overrides)<=set(catalog),f'unknown placement keys: {set(overrides)-set(catalog)}'
 for start,end,replacement in sorted(edits,reverse=True):text=text[:start]+replacement+text[end:]
 if edits:text='from jitx.layerindex import Side\n'+text
 ast.parse(text);destination.write_text(text)
 return {'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'placement_requests':len(catalog),'changed_requests':len(edits),'preserved_requests':len(catalog)-len(edits),'catalog':catalog,'overrides':overrides,'generated_sha256':hashlib.sha256(destination.read_bytes()).hexdigest()}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('overrides',type=Path);p.add_argument('output',type=Path);p.add_argument('record',type=Path);a=p.parse_args();r=render(a.source,json.loads(a.overrides.read_text()),a.output);a.record.write_text(json.dumps(r,indent=2));print(json.dumps({k:v for k,v in r.items() if k not in ['catalog','overrides']},indent=2))
