"""Bind a pose-search target to two verified disconnected native pad islands."""
import argparse,hashlib,json
from pathlib import Path
import pcbnew as p
ap=argparse.ArgumentParser();ap.add_argument('board',type=Path);ap.add_argument('--moving',required=True);ap.add_argument('--target',required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();path=a.board.resolve()
manager=p.SETTINGS_MANAGER();manager.LoadProject(str(path.with_suffix('.kicad_pro')));board=p.LoadBoard(str(path));board.SetProject(manager.GetProject(str(path.with_suffix('.kicad_pro'))));assert p.ZONE_FILLER(board).Fill(board.Zones());c=board.GetConnectivity();c.Build(board);c.RecalculateRatsnest()
pads={f.GetReference()+'.'+q.GetNumber():q for f in board.GetFootprints() for q in f.Pads()};moving,target=pads[a.moving],pads[a.target];assert moving.GetNetname() and moving.GetNetname()==target.GetNetname()
connected={x.m_Uuid.AsString() for x in c.GetConnectedItems(moving)};assert target.m_Uuid.AsString() not in connected,'Pads are already connected'
def endpoint(q):return dict(ref=q.GetParentFootprint().GetReference(),position=dict(x=q.GetPosition().x/1e6,y=q.GetPosition().y/1e6),uuid=q.m_Uuid.AsString(),description='Native disconnected-island pad '+q.GetParentFootprint().GetReference()+'.'+q.GetNumber())
result=dict(parent_board_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),native_connectivity_verified=True,net=moving.GetNetname(),source_board=str(path),source_script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),targets=[[endpoint(moving),endpoint(target)]],CAD_saved=False)
a.output.write_text(json.dumps(result,indent=2));print(json.dumps(result))
