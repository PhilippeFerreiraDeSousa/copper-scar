"""Extract the original schematic coordinates used by the placement heuristic."""
import argparse,json
from pathlib import Path
import sexpdata as sx
ap=argparse.ArgumentParser();ap.add_argument('source',type=Path);ap.add_argument('output',type=Path);a=ap.parse_args()
project=json.loads((a.source/'pcbgolf.kicad_pro').read_text());positions={}
for sheet in project['schematic']['top_level_sheets']:
 tree=sx.loads((a.source/sheet['filename']).read_text())
 for symbol in tree:
  if not isinstance(symbol,list) or not symbol or str(symbol[0])!='symbol':continue
  props={str(n[1]):str(n[2]) for n in symbol if isinstance(n,list) and n and str(n[0])=='property'}
  at=next(n for n in symbol if isinstance(n,list) and n and str(n[0])=='at')
  if 'Reference' in props and not props['Reference'].startswith('#'):positions[props['Reference']]=dict(sheet=sheet['filename'],xy=at[1:3])
a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(positions,indent=2));print(len(positions),'schematic references')
