"""Read-only native comparison of every pad, including unnumbered mechanical holes."""
import pcbnew as p
import json,sys
from pathlib import Path
source,board,manifest,output=map(Path,sys.argv[1:]);m=json.loads(manifest.read_text())
def geometry(path):
 b=p.LoadBoard(str(path));out={}
 for f in b.GetFootprints():
  pads=[]
  for d in f.Pads():
   at=d.GetFPRelativePosition();sz=d.GetSize();hole=d.GetDrillSize()
   pads.append({'number':d.GetNumber(),'relative_nm':[at.x,at.y],'relative_angle':round(d.GetFPRelativeOrientation().AsDegrees()%360,6),'size_nm':[sz.x,sz.y],'drill_nm':[hole.x,hole.y],'shape':int(d.GetShape()),'attribute':int(d.GetAttribute()),'layers':str(d.GetLayerSet().FmtBin())})
  out[f.GetReference()]=sorted(pads,key=lambda v:json.dumps(v,sort_keys=True))
 return out
old=geometry(source);new=geometry(board);checks={r:new[r]==old[m.get('original_ref_aliases',{}).get(r,r)] for r in new};result={'source_board':str(source),'board':str(board),'all_electrical_and_mechanical_pads_preserved':all(checks.values()),'per_reference':checks,'mismatches':{r:{'source':old[m.get('original_ref_aliases',{}).get(r,r)],'candidate':new[r]} for r,v in checks.items() if not v}}
output.write_text(json.dumps(result,indent=2));print({'passed':all(checks.values()),'mismatch_refs':[r for r,v in checks.items() if not v]})
