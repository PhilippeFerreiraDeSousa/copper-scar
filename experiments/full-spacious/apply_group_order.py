"""Apply explicit integer translations to complete functional groups on unrouted input."""
import argparse,hashlib,json
from pathlib import Path
import pcbnew as p
ap=argparse.ArgumentParser();ap.add_argument('folder',type=Path);ap.add_argument('proposal',type=Path);a=ap.parse_args()
board=a.folder/'pcbgolf.kicad_pcb';cfg=json.loads(a.proposal.read_text());assert hashlib.sha256(board.read_bytes()).hexdigest()==cfg['source_board_sha256']
project=a.folder/'pcbgolf.kicad_pro';oldproject=project.read_bytes();b=p.LoadBoard(str(board));assert not list(b.GetTracks()) and not list(b.Zones())
fs={f.GetReference():f for f in b.GetFootprints()};before={r:[f.GetPosition().x,f.GetPosition().y,f.GetOrientationDegrees()] for r,f in fs.items()}
members=[r for g in cfg['groups'] for r in g['refs']];assert len(members)==len(set(members)) and set(members)|{'BH1','BH2','BH3','BH4'}==set(fs)
for group in cfg['groups']:
 dx,dy=group['translation_nm']
 for r in group['refs']:
  x,y,_=before[r];fs[r].SetPosition(p.VECTOR2I(x+dx,y+dy))
box=cfg['outline_mm'];corners=[(box[0],box[1]),(box[2],box[1]),(box[2],box[3]),(box[0],box[3])]
for r,(x,y) in zip(['BH1','BH2','BH3','BH4'],[(box[0]+4,box[1]+4),(box[2]-4,box[1]+4),(box[2]-4,box[3]-4),(box[0]+4,box[3]-4)]):fs[r].SetPosition(p.VECTOR2I(round(x*1e6),round(y*1e6)))
for d in list(b.GetDrawings()):
 if d.GetLayer()==p.Edge_Cuts:b.Delete(d)
for i,(x,y) in enumerate(corners):
 xx,yy=corners[(i+1)%4];d=p.PCB_SHAPE();d.SetShape(p.SHAPE_T_SEGMENT);d.SetLayer(p.Edge_Cuts);d.SetWidth(p.FromMM(.05));d.SetStart(p.VECTOR2I(round(x*1e6),round(y*1e6)));d.SetEnd(p.VECTOR2I(round(xx*1e6),round(yy*1e6)));b.Add(d)
p.SaveBoard(str(board),b);project.write_bytes(oldproject)
result=dict(before_nm=before,after_nm={r:[f.GetPosition().x,f.GetPosition().y,f.GetOrientationDegrees()] for r,f in fs.items()},proposal_sha256=hashlib.sha256(a.proposal.read_bytes()).hexdigest(),outline_mm=box,qualification='All integer group translations and mechanical-hole positions explicit; original footprint dimensions and orientations retained. Full native preflight required.')
(a.folder/'group-order-applied.json').write_text(json.dumps(result,indent=2)+'\n')
