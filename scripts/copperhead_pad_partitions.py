"""Read native pad connectivity from original-project boards without saving CAD."""
import argparse,hashlib,json
from pathlib import Path
import pcbnew as p

def inspect(path):
 path=path.resolve()
 manager=p.SETTINGS_MANAGER();manager.LoadProject(str(path.with_suffix('.kicad_pro')))
 board=p.LoadBoard(str(path));board.SetProject(manager.GetProject(str(path.with_suffix('.kicad_pro'))));assert p.ZONE_FILLER(board).Fill(board.Zones())
 connectivity=board.GetConnectivity();connectivity.Build(board);connectivity.RecalculateRatsnest();seen=set();groups=[]
 for footprint in board.GetFootprints():
  for pad in footprint.Pads():
   uid=pad.m_Uuid.AsString()
   if uid in seen:continue
   members={x.m_Uuid.AsString() for x in connectivity.GetConnectedItems(pad) if isinstance(x,p.PAD)};members.add(uid);seen.update(members);groups.append(sorted(members))
 return dict(board_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),project_sha256=hashlib.sha256(path.with_suffix('.kicad_pro').read_bytes()).hexdigest(),groups=sorted(groups),native_open_count=connectivity.GetUnconnectedCount(False))

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--before',type=Path,required=True);ap.add_argument('--after',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
 before=inspect(a.before);after=inspect(a.after);new=[set(x) for x in after['groups']];splits=[x for x in before['groups'] if not any(set(x)<=g for g in new)]
 result=dict(before=before,after=after,pad_partitions_equal=before['groups']==after['groups'],no_connected_pad_group_split=not splits,split_groups=splits,CAD_saved=False)
 a.output.write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k not in ['before','after','split_groups']}))
if __name__=='__main__':main()
