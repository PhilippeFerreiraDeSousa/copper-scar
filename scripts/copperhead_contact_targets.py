"""Native expected pin groups for vias at normalized DSN junctions; no save."""
import argparse,hashlib,json
from decimal import Decimal
from pathlib import Path
import pcbnew as p
ap=argparse.ArgumentParser();ap.add_argument('board',type=Path);ap.add_argument('--normalization',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();path=a.board.resolve()
proof=json.loads(a.normalization.read_text());points={(row['net'],int(Decimal(str(x))*1000),int(-Decimal(str(y))*1000)) for row in proof['changes'] for x,y in row['existing_junctions']}
manager=p.SETTINGS_MANAGER();manager.LoadProject(str(path.with_suffix('.kicad_pro')));board=p.LoadBoard(str(path));board.SetProject(manager.GetProject(str(path.with_suffix('.kicad_pro'))));assert p.ZONE_FILLER(board).Fill(board.Zones());connection=board.GetConnectivity();connection.Build(board);connection.RecalculateRatsnest();rows=[];seen=set()
for via in board.GetTracks():
    if not isinstance(via,p.PCB_VIA):continue
    if via.GetNetname() not in proof['nets']:continue
    pins=sorted({pad.GetParentFootprint().GetReference()+'.'+pad.GetNumber() for pad in connection.GetConnectedItems(via) if isinstance(pad,p.PAD)})
    group=(via.GetNetname(),tuple(pins));junction=(via.GetNetname(),via.GetPosition().x,via.GetPosition().y) in points
    if not junction and (not pins or group in seen):continue
    seen.add(group)
    rows.append(dict(net=via.GetNetname(),xy_dsn_um=[via.GetPosition().x/1000,-via.GetPosition().y/1000],expected_pins=pins,role='normalized_junction' if junction else 'native_island_representative'))
result=dict(board_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),targets=rows,CAD_saved=False)
a.output.write_text(json.dumps(result,indent=2));print(json.dumps(result))
