"""Remove one explicitly named redundant native via only if pad partitions survive."""
import argparse,hashlib,json,math
from pathlib import Path
import pcbnew as p

ap=argparse.ArgumentParser();ap.add_argument('folder',type=Path);ap.add_argument('--proposal',required=True,type=Path);a=ap.parse_args()
folder=a.folder.resolve();path=folder/'pcbgolf.kicad_pcb';proposal=json.loads(a.proposal.read_text())
assert hashlib.sha256(path.read_bytes()).hexdigest()==proposal['parent_board_sha256'],'Wrong consolidation parent'
manager=p.SETTINGS_MANAGER();manager.LoadProject(str(path.with_suffix('.kicad_pro')))
board=p.LoadBoard(str(path));board.SetProject(manager.GetProject(str(path.with_suffix('.kicad_pro'))))

def via_info(v):
 return dict(uuid=v.m_Uuid.AsString(),net=v.GetNetname(),position_nm=[v.GetPosition().x,v.GetPosition().y],diameter_nm=v.GetWidth(p.F_Cu),drill_nm=v.GetDrillValue(),layers=[board.GetLayerName(v.TopLayer()),board.GetLayerName(v.BottomLayer())])

def partitions():
 assert p.ZONE_FILLER(board).Fill(board.Zones())
 c=board.GetConnectivity();c.Build(board);c.RecalculateRatsnest();seen=set();groups=[]
 for footprint in board.GetFootprints():
  for pad in footprint.Pads():
   key=pad.m_Uuid.AsString()
   if key in seen:continue
   connected={x.m_Uuid.AsString() for x in c.GetConnectedItems(pad) if isinstance(x,p.PAD)};connected.add(key);seen.update(connected)
   groups.append((pad.GetNetname(),tuple(sorted(connected))))
 return sorted(groups)

def identities():
 return sorted((f.m_Uuid.AsString(),f.GetReference(),f.GetPosition().x,f.GetPosition().y,f.GetOrientationDegrees(),tuple(sorted((q.m_Uuid.AsString(),q.GetNumber(),q.GetNetname(),q.GetPosition().x,q.GetPosition().y) for q in f.Pads()))) for f in board.GetFootprints())

vias={v.m_Uuid.AsString():v for v in board.GetTracks() if isinstance(v,p.PCB_VIA)}
keep=vias[proposal['keep_via']['uuid']];remove=vias[proposal['remove_via']['uuid']]
assert keep is not remove
assert via_info(keep)==proposal['keep_via'] and via_info(remove)==proposal['remove_via'],'Via geometry differs from proposal'
for key in ['net','diameter_nm','drill_nm','layers']:assert via_info(keep)[key]==via_info(remove)[key]
assert keep.GetNetname()==proposal['net']
separation=math.dist(via_info(keep)['position_nm'],via_info(remove)['position_nm'])/1e6
assert separation<=proposal['max_center_separation_mm']
before=partitions();identity=identities();removed=via_info(remove);count=len(list(board.GetTracks()));board.Delete(remove)
after=partitions();assert before==after,'Removing via splits or changes a native pad partition'
assert identities()==identity,'Footprint or pad identity/pose changed'
assert len(list(board.GetTracks()))==count-1
p.SaveBoard(str(path),board)
report=dict(operation='pcbnew.BOARD.Delete one explicitly named duplicate via',removed=removed,kept=via_info(keep),center_separation_mm=separation,removed_items=1,added_items=0,all_native_pad_partitions_preserved=True,footprint_pad_identity_pose_preserved=True,pad_partition_sha256=hashlib.sha256(json.dumps(before).encode()).hexdigest(),native_drc_required=True)
(folder/'via-consolidation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
