"""Apply a bounded local placement repair to the four measured LED/Q conflicts."""
from pathlib import Path
import argparse,json
import sexpdata as sx
from audit import nodes,first
from campaign import write,sha
ap=argparse.ArgumentParser();ap.add_argument('failed',type=Path);ap.add_argument('out',type=Path);a=ap.parse_args();drc=json.loads((a.failed/'preflight.json').read_text());assert len(drc['violations'])==4 and all(v['type']=='clearance' for v in drc['violations']);d=sx.loads((a.failed/'preview.kicad_pcb').read_text());moves={}
for f in nodes(d,'footprint'):
 ref=next(p[2] for p in nodes(f,'property') if p[1]=='Reference')
 if ref in ['LED14','LED15','LED16','LED17']:
  at=first(f,'at');before=at[1:];at[1]=round(at[1]-.2,4);moves[ref]={'before':before,'after':at[1:]}
assert len(moves)==4;a.out.mkdir();(a.out/'pcbgolf.kicad_pcb').write_text(sx.dumps(d));action=json.loads((a.failed/'request.json').read_text())['action'];action.update(kind='vertical_contraction_with_local_clearance_repair',rationale='Native preflight measured four repeated lower-bank LED/Q gaps at0.125mm versus0.2mm rule. Native rectangular-pad geometry shows horizontal gap controls clearance; move each implicated LED0.2mm left away from Q, retaining the contracted outline and all electrical geometry; full preflight and routing required.',local_moves=moves,diagnostic_report=str(a.failed/'preflight.json'),diagnostic_sha256=sha(a.failed/'preflight.json'));write(a.out/'proposal.json',action)
