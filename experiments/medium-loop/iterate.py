"""Diagnostic group moves followed by fresh complete routing and native acceptance."""
from pathlib import Path
import argparse,copy,json,subprocess,time
from campaign import realize,sha,write,now
ap=argparse.ArgumentParser();ap.add_argument('base',type=Path);ap.add_argument('source',type=Path);ap.add_argument('--name',required=True);ap.add_argument('--parent',default='baseline-parity');ap.add_argument('--moves',required=True,help='JSON ref to [dx,dy,angle_delta]');ap.add_argument('--reason',required=True);a=ap.parse_args();base=a.base.resolve();parent=base/a.parent;folder=base/a.name;manifest=base/'input/circuit.json'
old=json.loads((parent/'native-audit.json').read_text());ps={r:[v['pose'][0]/1e6,v['pose'][1]/1e6,v['pose'][2]] for r,v in old['identity'].items()};moves=json.loads(a.moves);candidate=copy.deepcopy(ps)
for r,delta in moves.items():candidate[r]=[ps[r][i]+delta[i] for i in range(3)]
action={'kind':'relative_group_move','deltas_mm_degrees':moves,'components':list(moves),'before':{r:ps[r] for r in moves},'after':{r:candidate[r] for r in moves},'reason':a.reason,'diagnostic_drc':str(parent/'drc.json'),'fresh_full_board_routing':True,'inherited_vias':0}
commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();record={'id':a.name,'stage':'stage1','source_sha':commit,'started_at':now(),'parent':str(parent),'parent_board_sha256':sha(parent/'pcbgolf.kicad_pcb'),'action':action,'route_budget':{'seconds':240,'passes':100,'threads':1,'enabled_layers':['F.Cu','B.Cu']}}
write(base/(a.name+'-proposal.json'),record);write(base/'status.json',{'running':record,'last_completed':str(parent),'updated_at':now()})
r,commands=realize(base,folder,candidate,manifest,a.source.resolve());previous=json.loads((parent/'evaluation.json').read_text());keep=r['placement_legal'] and (r['feasibility_cost'],r['wire_length_mm'])<(previous['feasibility_cost'],previous['wire_length_mm']);record.update(finished_at=now(),after=r,commands=commands,retained=keep,decision='keep' if keep else 'reject',preview_sha256=sha(folder/'preview.kicad_pcb'),folder=str(folder));write(folder/'completed.json',record)
with (base/'events.jsonl').open('a') as f:f.write(json.dumps(record)+'\n')
write(base/'status.json',{'running':None,'last_completed':str(folder),'incumbent':str(folder if keep else parent),'updated_at':now()});print(json.dumps(record),flush=True)
