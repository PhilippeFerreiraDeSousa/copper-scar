"""Apply explicit, diagnosed placement actions, then route and independently retain/reject."""
from pathlib import Path
import argparse,json,subprocess
from campaign import realize,poses,write,now,sha,ROOT,require_stage_one_work
from record import finish
from live_status import update as update_live
ap=argparse.ArgumentParser();ap.add_argument('base',type=Path);ap.add_argument('source',type=Path);ap.add_argument('parent');ap.add_argument('output');ap.add_argument('proposal',type=Path);a=ap.parse_args();base=a.base.resolve();parent=base/a.parent;out=base/a.output;require_stage_one_work(parent);action=json.loads(a.proposal.read_text());ps=poses(parent/'pcbgolf.kicad_pcb');m=json.loads((base/'input/circuit.json').read_text());action['before']={r:ps[r] for r in action['after']};action['affected_nets']={n:pads for n,pads in m['nets'].items() if any(p.split('.')[0] in action['after'] for p in pads)};action['diagnostic_source_sha256']=sha(parent/'drc.json');ps.update(action['after']);write(base/(a.output+'-proposal.json'),{'source_sha':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'created_at':now(),'parent_board_sha256':sha(parent/'pcbgolf.kicad_pcb'),'action':action,'poses':ps})
try:
 result,commands=realize(base,out,ps,base/'input/circuit.json',a.source.resolve());record=finish(base,out,a.source.resolve(),action,parent,publish=False);result=record['after'];before=json.loads((parent/'evaluation.json').read_text());retain=result['placement_legal'] and result['all_pad_geometry_preserved'] and (result['feasibility_cost'],result['wire_length_mm'])<(before['feasibility_cost'],before['wire_length_mm']);record['retained']=retain;record['decision_reason']='Strictly lower native loss, then shorter copper at equal loss; original geometry/rules must pass';write(out/'completed.json',record);update_live(base,state='idle');print(json.dumps({'retained':retain,'opens':result['native_open_count'],'cost':result['feasibility_cost'],'folder':str(out)}),flush=True)
except Exception as error:
 write(base/(a.output+'-failure.json'),{'action':action,'error':repr(error),'finished_at':now()});raise
