"""Verify new via realization and preserve every pre-existing native via site."""
import argparse
import collections
import hashlib
import json
from pathlib import Path
import pcbnew as p


def inspect(path):
    board=p.LoadBoard(str(path));rows=[]
    for item in board.GetTracks():
        if isinstance(item,p.PCB_VIA):
            rows.append(dict(uuid=item.m_Uuid.AsString(),net=item.GetNetname(),x_nm=item.GetPosition().x,y_nm=item.GetPosition().y,diameter_nm=item.GetWidth(p.F_Cu),drill_nm=item.GetDrillValue(),layers=[board.GetLayerName(item.TopLayer()),board.GetLayerName(item.BottomLayer())]))
    return rows


def key(row):
    return tuple(row[x] for x in ('net','x_nm','y_nm','diameter_nm','drill_nm'))+tuple(row['layers'])


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--before',type=Path,required=True);ap.add_argument('--after',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
    before=inspect(a.before);after=inspect(a.after);old=collections.Counter(map(key,before));new=collections.Counter(map(key,after));missing=old-new;added=new-old
    result=dict(before_sha256=hashlib.sha256(a.before.read_bytes()).hexdigest(),after_sha256=hashlib.sha256(a.after.read_bytes()).hexdigest(),existing_via_geometry_preserved=not missing,missing_existing=[dict(geometry=list(k),count=n) for k,n in missing.items()],added=[dict(geometry=list(k),count=n) for k,n in added.items()],new_definition_vias=[r for r in after if r['diameter_nm']==450000 and r['drill_nm']==200000],new_vias_use_only_allowed_definitions=all(k[3:5] in ((600000,300000),(450000,200000)) and k[5:]==('F.Cu','B.Cu') for k in added),CAD_saved=False)
    a.output.write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k not in ('added','missing_existing','new_definition_vias')}))


if __name__=='__main__':main()
