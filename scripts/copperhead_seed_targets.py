"""Revalidate isolated seed targets on the current native parent without saving."""
import argparse,hashlib,json
from pathlib import Path
import pcbnew as p

ap=argparse.ArgumentParser();ap.add_argument('board',type=Path);ap.add_argument('--proposal',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
path=a.board.resolve();cfg=json.loads(a.proposal.read_text());project=path.with_suffix('.kicad_pro');manager=p.SETTINGS_MANAGER();manager.LoadProject(str(project));board=p.LoadBoard(str(path));board.SetProject(manager.GetProject(str(project)));assert p.ZONE_FILLER(board).Fill(board.Zones())
c=board.GetConnectivity();c.Build(board);c.RecalculateRatsnest();pads={q.m_Uuid.AsString():q for f in board.GetFootprints() for q in f.Pads()};kept=[];excluded=[]
assert hashlib.sha256(path.read_bytes()).hexdigest()==cfg['parent_board_sha256']
for site in cfg['via_sites']:
 pad=pads[site['target_pad_uuid']];assert pad.GetNetname()==site['net']
 assert [round(p.ToMM(pad.GetPosition().x),6),round(p.ToMM(pad.GetPosition().y),6)]==site['target_pad_position_mm']
 connected=[q for q in c.GetConnectedItems(pad) if isinstance(q,p.PAD) and q.m_Uuid.AsString()!=site['target_pad_uuid']]
 existing=[v for v in board.GetTracks() if isinstance(v,p.PCB_VIA) and [round(p.ToMM(v.GetPosition().x),6),round(p.ToMM(v.GetPosition().y),6)]==site['position_mm']]
 if connected or existing:
  excluded.append(dict(site=site,reason='Target already connects to other pads' if connected else 'Via already occupies proposed site',connected_other_pads=sorted(q.GetParentFootprint().GetReference()+'.'+q.GetNumber() for q in connected),existing_via_uuids=[v.m_Uuid.AsString() for v in existing]))
 else:kept.append(site)
report=dict(parent_board_sha256=cfg['parent_board_sha256'],kept_sites=kept,excluded_sites=excluded,CAD_saved=False,qualification='Preserved target UUID/net/pose and current singleton-pad state; whole-batch site legality still requires native preflight.')
a.output.write_text(json.dumps(report,indent=2));print(json.dumps(report))
