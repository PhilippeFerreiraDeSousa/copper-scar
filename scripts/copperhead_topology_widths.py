"""Check scoped minimum trace widths in the final native topology candidate."""
import argparse,hashlib,json
from pathlib import Path
import pcbnew as p
ap=argparse.ArgumentParser();ap.add_argument('board',type=Path);ap.add_argument('--proposal',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
cfg=json.loads(a.proposal.read_text());required=cfg['required_original_track_width_mm'];board=p.LoadBoard(str(a.board));violations=[];counts={net:0 for net in required}
assert required and set(required)==set(cfg['nets']) and all(width>0 for width in required.values()),'Width requirements must cover every touched net'
for item in board.GetTracks():
    net=item.GetNetname()
    if net not in required or isinstance(item,p.PCB_VIA):continue
    counts[net]+=1
    if item.GetWidth()<p.FromMM(required[net]):violations.append(dict(uuid=item.m_Uuid.AsString(),net=net,width_nm=item.GetWidth(),minimum_mm=required[net]))
result=dict(board_sha256=hashlib.sha256(a.board.read_bytes()).hexdigest(),required_widths_mm=required,checked_tracks=counts,violations=violations,ok=not violations and all(counts.values()),CAD_saved=False)
a.output.write_text(json.dumps(result,indent=2));print(json.dumps(result))
