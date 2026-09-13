#!/usr/bin/env python3
"""Read-only native KiCad inventory for an isolated assembly export input."""
import argparse,hashlib,json
from pathlib import Path
import pcbnew

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def xyz(v):return [v.x,v.y,v.z]
p=argparse.ArgumentParser();p.add_argument('board',type=Path);p.add_argument('--original',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
b=pcbnew.LoadBoard(str(a.board));original=pcbnew.LoadBoard(str(a.original/'pcbgolf.kicad_pcb'));original_dnp={f.GetReference():f.IsDNP() for f in original.GetFootprints()};rows=[]
for f in sorted(b.GetFootprints(),key=lambda f:f.GetReference()):
 models=[]
 for m in f.Models():
  path=Path(m.m_Filename.replace('${KIPRJMOD}',str(a.board.parent)))
  supplied=Path(m.m_Filename.replace('${KIPRJMOD}',str(a.original)))
  models.append(dict(reference=m.m_Filename,resolved_path=str(path),exists=path.is_file(),sha256=sha(path) if path.is_file() else None,original_asset_sha256=sha(supplied) if supplied.is_file() else None,shown=m.m_Show,offset=xyz(m.m_Offset),scale=xyz(m.m_Scale),rotation=xyz(m.m_Rotation)))
 rows.append(dict(ref=f.GetReference(),value=f.GetValue(),footprint=str(f.GetFPID().GetLibItemName()),uuid=f.m_Uuid.AsString(),position_nm=[f.GetPosition().x,f.GetPosition().y],rotation_degrees=f.GetOrientationDegrees(),layer=f.GetLayerName(),dnp=f.IsDNP(),original_dnp=original_dnp[f.GetReference()],models=models,pads=[dict(number=p.GetNumber(),net=p.GetNetname(),drill_nm=[p.GetDrillSize().x,p.GetDrillSize().y],size_nm=[p.GetSize().x,p.GetSize().y],position_nm=[p.GetPosition().x,p.GetPosition().y]) for p in f.Pads()],properties={p.GetName():p.GetText() for p in f.GetFields()}))
assert len(rows)==245 and all(r['dnp']==r['original_dnp'] for r in rows)
resolved=[m for r in rows for m in r['models'] if m['exists'] and m['sha256']==m['original_asset_sha256'] and m['shown']]
summary=dict(total_footprints=len(rows),dnp_refs=[r['ref'] for r in rows if r['dnp']],populated_footprints=sum(not r['dnp'] for r in rows),model_references=sum(len(r['models']) for r in rows),resolved_original_models=len(resolved),unique_models=len({m['sha256'] for m in resolved}),populated_with_resolved_original_model=sum(not r['dnp'] and any(m['exists'] and m['sha256']==m['original_asset_sha256'] and m['shown'] for m in r['models']) for r in rows),without_model=[r['ref'] for r in rows if not r['models']],original_population_flags_preserved=True)
payload=dict(board_sha256=sha(a.board),project_sha256=sha(a.board.with_suffix('.kicad_pro')),original_board_sha256=sha(a.original/'pcbgolf.kicad_pcb'),summary=summary,footprints=rows,native_version=pcbnew.GetBuildVersion(),method='Native read only; no SaveBoard or geometry mutation')
a.output.write_text(json.dumps(payload,indent=2)+'\n');print(json.dumps(summary))
