"""Resolve explicit terminal names against frozen native net attachments."""
import argparse,hashlib,json
from pathlib import Path
import pcbnew as p

ap=argparse.ArgumentParser();ap.add_argument('board',type=Path);ap.add_argument('--proposal',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
cfg=json.loads(a.proposal.read_text());path=a.board.resolve();assert hashlib.sha256(path.read_bytes()).hexdigest()==cfg['parent_board_sha256']
board=p.LoadBoard(str(path));pads={}
for footprint in board.GetFootprints():
 for pad in footprint.Pads():pads.setdefault(footprint.GetReference()+'.'+pad.GetNumber(),[]).append(pad)
bindings=[]
for name in cfg['terminals']:
 assert len(pads.get(name,[]))==1,'Missing or ambiguous terminal '+name
 pad=pads[name][0];bindings.append(dict(terminal=name,uuid=pad.m_Uuid.AsString(),net=pad.GetNetname()))
actual=sorted({b['net'] for b in bindings});declared=sorted(set(cfg['nets']));result=dict(parent_board_sha256=cfg['parent_board_sha256'],bindings=bindings,actual_nets=actual,declared_nets=declared,net_scope_matches=actual==declared,CAD_saved=False)
a.output.write_text(json.dumps(result,indent=2));assert result['net_scope_matches'],'Proposal nets disagree with native terminal attachments; see binding report'
