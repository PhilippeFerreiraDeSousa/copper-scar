"""Complete the declared demo BOM and model inventory before assembly scoring."""
from pathlib import Path
import argparse,shutil,json,hashlib
import sexpdata as sx
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCP.BRep import BRep_Builder
from OCP.TopoDS import TopoDS_Compound
from OCP.gp import gp_Pnt
from OCP.STEPControl import STEPControl_Writer,STEPControl_AsIs
from audit import nodes,first
ap=argparse.ArgumentParser();ap.add_argument('base',type=Path);ap.add_argument('source',type=Path);a=ap.parse_args();base=a.base.resolve();src=a.source.resolve();out=base/'stage2';out.mkdir();b=out/'baseline';b.mkdir();parent=base/'feasible-width200';shutil.copy2(parent/'pcbgolf.kicad_pcb',b/'pcbgolf.kicad_pcb');shutil.copy2(base/'authoritative-project.json',b/'pcbgolf.kicad_pro');shutil.copytree(base/'input/pcbgolf.pretty',b/'pcbgolf.pretty');shutil.copy2(base/'input/fp-lib-table',b/'fp-lib-table')
d=sx.loads((b/'pcbgolf.kicad_pcb').read_text());footprints=nodes(d,'footprint');header=next(f for f in footprints if next(x[2] for x in nodes(f,'property') if x[1]=='Reference')=='J4')
# Nominal envelope from manufacturer's current M20-9980446 page. Original pad
# centers and 0.64mm square pins retain the connector's 2.54mm physical interface.
model=b/'models/M20-9980446-nominal.step';model.parent.mkdir();compound=TopoDS_Compound();builder=BRep_Builder();builder.MakeCompound(compound);builder.Add(compound,BRepPrimAPI_MakeBox(gp_Pnt(-5.08,-2.54,0),10.16,5.08,2.54).Shape())
for pad in nodes(header,'pad'):
 x,y=first(pad,'at')[1:3];builder.Add(compound,BRepPrimAPI_MakeBox(gp_Pnt(x-.32,-y-.32,-3),.64,.64,11.64).Shape())
w=STEPControl_Writer();w.Transfer(compound,STEPControl_AsIs);w.Write(str(model))
attrs=first(header,'attr');attrs[:]=[sx.Symbol('attr'),sx.Symbol('through_hole')];header.append(sx.loads('(model "${KIPRJMOD}/models/M20-9980446-nominal.step" (offset (xyz 0 0 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0)))'))
models=[]
for f in footprints:
 ref=next(x[2] for x in nodes(f,'property') if x[1]=='Reference')
 for m in nodes(f,'model'):
  relative=m[1].replace('${KIPRJMOD}/','');dest=b/relative
  if not dest.exists():dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src/relative,dest)
  models.append({'reference':ref,'path':relative,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()})
(b/'pcbgolf.kicad_pcb').write_text(sx.dumps(d));shutil.copy2(base/'input/small-loop.kicad_sch',b/'pcbgolf.kicad_sch');shutil.copy2(base/'input/pcbgolf.kicad_sym',b/'pcbgolf.kicad_sym');shutil.copy2(base/'input/sym-lib-table',b/'sym-lib-table')
# Explicitly populate the same connector symbol in this Stage Two copy.
sch=sx.loads((b/'pcbgolf.kicad_sch').read_text())
for label in nodes(sch,'label'):
 label[0]=sx.Symbol('global_label');label.insert(2,[sx.Symbol('shape'),sx.Symbol('input')])
for s in nodes(sch,'symbol'):
 if next(x[2] for x in nodes(s,'property') if x[1]=='Reference')=='J4':
  for k in ['in_bom','on_board']:
   if nodes(s,k):first(s,k)[1]=sx.Symbol('yes')
  if nodes(s,'dnp'):first(s,'dnp')[1]=sx.Symbol('no')
(b/'pcbgolf.kicad_sch').write_text(sx.dumps(sch))
report={'official_formula':'PCBA bounding-box volume (mm^3) +50*vias +5000*copper_layers','official_source':'https://comma.ai/leaderboard','verified_date':'2026-09-13','parent_board_sha256':hashlib.sha256((parent/'pcbgolf.kicad_pcb').read_bytes()).hexdigest(),'BOM_change':'Populate previously DNP J4 with compatible Harwin M20-9980446; electrical footprint/pins unchanged','header_model':'Datasheet-dimensioned nominal body and pins; not vendor detailed STEP','header_source':'https://www.harwin.com/products/M20-9980446','header_dimensions_mm':[10.16,5.08,11.64],'height_above_pcb_mm':8.64,'tail_length_mm':3,'all_component_models':models,'qualified_for_original_challenge':False}
(out/'assembly-contract.json').write_text(json.dumps(report,indent=2));print(out)

lib=b/'pcbgolf.pretty/2X04.kicad_mod';ld=sx.loads(lib.read_text());ld[:]=[v for v in ld if not(isinstance(v,list) and v and str(v[0]) in ('attr','model'))];ld.append(sx.loads('(attr through_hole)'));ld.append(nodes(header,'model')[0]);lib.write_text(sx.dumps(ld))
