"""Explicit experimental land-pattern cleanup; no clearance-rule changes.

Manufacturer/assembly review is still required. Every pad identity is retained.
"""
from pathlib import Path
import argparse,json,shutil
import pcbnew as p
ap=argparse.ArgumentParser();ap.add_argument('source',type=Path);ap.add_argument('destination',type=Path);a=ap.parse_args();shutil.copytree(a.source,a.destination);b=p.LoadBoard(str(a.destination/'pcbgolf.kicad_pcb'));changes=[]
report=json.loads((a.source/'drc-placement.json').read_text());silkuids={i['uuid'] for v in report['violations'] if v['type'] in ['silk_over_copper','silk_overlap','text_height','text_thickness'] for i in v['items']}
for f in b.GetFootprints():
 ref=f.GetReference();pads={q.GetNumber():q for q in f.Pads()}
 for num,q in pads.items():
  if ref=='J3' and num.endswith('T') and num[:-1] in pads:
   base=pads[num[:-1]];changes.append(dict(ref=ref,pad=num,old_position_nm=[q.GetPosition().x,q.GetPosition().y],new_position_nm=[base.GetPosition().x,base.GetPosition().y],old_size_mm=[p.ToMM(q.GetSize().x),p.ToMM(q.GetSize().y)],new_size_mm=[p.ToMM(base.GetSize().x),p.ToMM(base.GetSize().y)],reason='Align surface overlay to same-terminal PTH land; preserves hole and 0.1mm annulus'))
   q.SetPosition(base.GetPosition());q.SetSize(base.GetSize());q.SetShape(p.PAD_SHAPE_CIRCLE)
  if (ref=='U4' and num.isdigit() and 1<=int(num)<=64) or (ref in ['J5','J6','J7','J8'] and num in ['S11','S12','S13','S14']):
   changes.append(dict(ref=ref,pad=num,shape='roundrect',ratio=(.5 if ref in ['J5','J6','J7','J8'] else .25),reason='Round corners while preserving centre, orientation and maximum land dimensions'))
   q.SetShape(p.PAD_SHAPE_ROUNDRECT);q.SetRoundRectRadiusRatio(.5 if ref in ['J5','J6','J7','J8'] else .25)
 for q in list(f.GraphicalItems())+[f.Reference(),f.Value()]:
  if q.m_Uuid.AsString() in silkuids and q.GetLayer()==p.F_SilkS:
   changes.append(dict(ref=ref,uuid=q.m_Uuid.AsString(),layer='F.Fab',reason='Preserve assembly marking on fabrication drawing instead of violating solder-mask clearance'))
   q.SetLayer(p.F_Fab)
# Save candidate-local libraries from its actual footprint geometry. Existing
# unmatched imported footprints are normalized without changing board copper.
for f in b.GetFootprints():
 lib=f.GetFPID().GetLibNickname();name=f.GetFPID().GetLibItemName()
 if lib=='pcbgolf':
  p.FootprintSave(str(a.destination/'pcbgolf.pretty'),f)
p.SaveBoard(str(a.destination/'pcbgolf.kicad_pcb'),b);assert p.ExportSpecctraDSN(b,str(a.destination/'pcbgolf.dsn'))
(a.destination/'footprint-repairs.json').write_text(json.dumps(dict(changes=changes,qualification='EXPERIMENTAL land patterns; manufacturer and assembly review outstanding; original design rules unchanged'),indent=2));print(len(changes),'explicit changes')
