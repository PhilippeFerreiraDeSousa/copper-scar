"""Read actual native attachments of explicitly seeded vias without saving CAD."""
import argparse,hashlib,json
from pathlib import Path
import pcbnew as p

ap=argparse.ArgumentParser();ap.add_argument('board',type=Path);ap.add_argument('--proposal',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
path=a.board.resolve();cfg=json.loads(a.proposal.read_text());project=path.with_suffix('.kicad_pro')
manager=p.SETTINGS_MANAGER();manager.LoadProject(str(project));board=p.LoadBoard(str(path));board.SetProject(manager.GetProject(str(project)));assert p.ZONE_FILLER(board).Fill(board.Zones())
connectivity=board.GetConnectivity();connectivity.Build(board);connectivity.RecalculateRatsnest();rows=[]
for site in cfg['via_sites']:
 matches=[via for via in board.GetTracks() if isinstance(via,p.PCB_VIA) and via.GetPosition().x==p.FromMM(site['position_mm'][0]) and via.GetPosition().y==p.FromMM(site['position_mm'][1])]
 assert len(matches)==1,'Missing or ambiguous seeded via at explicit site'
 via=matches[0];pads=[item for item in connectivity.GetConnectedItems(via) if isinstance(item,p.PAD)]
 rows.append(dict(site=site,via_uuid=via.m_Uuid.AsString(),actual_net=via.GetNetname(),diameter_nm=via.GetWidth(p.F_Cu),drill_nm=via.GetDrillValue(),span=[board.GetLayerName(via.TopLayer()),board.GetLayerName(via.BottomLayer())],free=via.GetIsFree(),connected_pads=sorted(item.GetParentFootprint().GetReference()+'.'+item.GetNumber() for item in pads),target_pad_connected=site['target_pad_uuid'] in {item.m_Uuid.AsString() for item in pads}))
result=dict(board_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),project_sha256=hashlib.sha256(project.read_bytes()).hexdigest(),seeds=rows,all_seed_targets_connected=all(row['target_pad_connected'] for row in rows),CAD_saved=False)
a.output.write_text(json.dumps(result,indent=2));print(json.dumps(result))
