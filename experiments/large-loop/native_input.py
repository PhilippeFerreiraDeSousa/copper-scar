"""Retain original footprint geometry and project rules; reduce only declared circuit."""
import pcbnew as p
from pathlib import Path
import sys,json
source,out=map(Path,sys.argv[1:]);m=json.loads((out/'circuit.json').read_text());b=p.LoadBoard(str(out/'filtered.kicad_pcb'))
b.SetCopperLayerCount(2)

nets={}
for name in m['nets']:
 n=p.NETINFO_ITEM(b,name);b.Add(n);nets[name]=n
pn={v:k for k,vs in m['nets'].items() for v in vs}
for f in b.GetFootprints():
 ref=f.GetReference();x,y,angle=m['poses'][ref];f.SetOrientationDegrees(angle);f.SetPosition(p.VECTOR2I(p.FromMM(x),p.FromMM(y)))
 f.SetPath(p.KIID_PATH('/'+m['schematic_root']+'/'+m['symbol_uuids'][ref]))
 for pad in f.Pads():
  key=ref+'.'+pad.GetNumber()
  if key in pn:pad.SetNet(nets[pn[key]])
  else:pad.SetNetCode(0)
for x,y,xx,yy in [(20,20,125,20),(125,20,125,130),(125,130,20,130),(20,130,20,20)]:
 d=p.PCB_SHAPE();d.SetShape(p.SHAPE_T_SEGMENT);d.SetLayer(p.Edge_Cuts);d.SetStart(p.VECTOR2I(p.FromMM(x),p.FromMM(y)));d.SetEnd(p.VECTOR2I(p.FromMM(xx),p.FromMM(yy)));d.SetWidth(p.FromMM(.05));b.Add(d)
p.SaveBoard(str(out/'large-loop.kicad_pcb'),b)
