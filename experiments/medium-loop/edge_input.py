"""Trim independent outline axes while preserving accepted component poses."""
from pathlib import Path
import argparse,json,uuid
import sexpdata as sx
from audit import nodes,first
from stage2 import proposal
from campaign import write,sha
ap=argparse.ArgumentParser();ap.add_argument('parent',type=Path);ap.add_argument('out',type=Path);ap.add_argument('--x-margin',type=float,required=True);ap.add_argument('--y-margin',type=float,required=True);a=ap.parse_args();a.out.mkdir();board=a.parent/'pcbgolf.kicad_pcb';dx,ax=proposal(board,1,a.x_margin);dy,ay=proposal(board,1,a.y_margin);d=sx.loads(dx);x0,_,x1,_=ax['outline_mm'];_,y0,_,y1=ay['outline_mm'];d[:]=[v for v in d if not(isinstance(v,list) and v and str(v[0])=='gr_line' and first(v,'layer')[1]=='Edge.Cuts')]
for x,y,xx,yy in [(x0,y0,x1,y0),(x1,y0,x1,y1),(x1,y1,x0,y1),(x0,y1,x0,y0)]:d.append(sx.loads(f'(gr_line (start {x} {y}) (end {xx} {yy}) (stroke (width 0.05) (type default)) (layer "Edge.Cuts") (uuid "{uuid.uuid4()}"))'))
(a.out/'pcbgolf.kicad_pcb').write_text(sx.dumps(d));inc=json.loads((a.parent/'score.json').read_text());volume=(x1-x0)*(y1-y0)*inc['assembly']['dimensions_mm'][2];write(a.out/'proposal.json',{'kind':'independent_outline_margin','parent_board_sha256':sha(board),'component_poses_changed':False,'outline_mm':[x0,y0,x1,y1],'x_margin_mm':a.x_margin,'y_margin_mm':a.y_margin,'rationale':'Prior all-edge trim lost one CH2 relay header connection. Preserve top/bottom header escape margin while trimming side whitespace; all routing and native gates rerun.','expected_score_terms':{'forecast_only':True,'volume_mm3':volume,'via_count_assumption':inc['terms']['via_count'],'layer_penalty':10000,'score_if_vias_unchanged':volume+inc['terms']['via_penalty']+10000}})
