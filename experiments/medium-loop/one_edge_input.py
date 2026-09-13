"""Trim bottom whitespace, retaining top escape space and explicit seed copper."""
from pathlib import Path
import argparse,json
import sexpdata as sx
from audit import nodes,first
from campaign import write,sha
ap=argparse.ArgumentParser();ap.add_argument('parent',type=Path);ap.add_argument('seed',type=Path);ap.add_argument('out',type=Path);ap.add_argument('--trim',type=float,required=True);a=ap.parse_args();d=sx.loads((a.parent/'pcbgolf.kicad_pcb').read_text());d[:]=[v for v in d if not(isinstance(v,list) and v and str(v[0]) in ['segment','via','arc','zone'])];lines=[v for v in nodes(d,'gr_line') if first(v,'layer')[1]=='Edge.Cuts'];bottom=max(first(v,t)[2] for v in lines for t in ['start','end']);new=bottom-a.trim
for v in lines:
 for t in ['start','end']:
  at=first(v,t)
  if at[2]==bottom:at[2]=new
seed=sx.loads(a.seed.read_text());d.extend(nodes(seed,'segment')+nodes(seed,'via'));a.out.mkdir();(a.out/'pcbgolf.kicad_pcb').write_text(sx.dumps(d));inc=json.loads((a.parent/'score.json').read_text());volume=inc['assembly']['dimensions_mm'][0]*(inc['assembly']['dimensions_mm'][1]-a.trim)*inc['assembly']['dimensions_mm'][2];write(a.out/'proposal.json',{'kind':'bottom_edge_trim_with_ground_escape','parent_board_sha256':sha(a.parent/'pcbgolf.kicad_pcb'),'seed_board_sha256':sha(a.seed),'bottom_edge_before_mm':bottom,'bottom_edge_after_mm':new,'component_poses_changed':False,'rationale':'Prior all-edge trim lost a top-header relay connection. Preserve top margin and qualified Q7ground escape; trim only bottom whitespace, then rerun full routing and all native gates.','expected_score_terms':{'forecast_only':True,'volume_mm3':volume,'via_count_assumption':inc['terms']['via_count'],'layer_penalty':10000,'score_if_vias_unchanged':volume+inc['terms']['via_penalty']+10000}})
