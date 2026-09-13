"""Create a portable offline replay index from immutable native stage records."""
from pathlib import Path
import argparse,hashlib,json,re
from collections import Counter
ap=argparse.ArgumentParser();ap.add_argument('base',type=Path);ap.add_argument('output',type=Path);a=ap.parse_args();base=a.base.resolve();rows=[];incumbent=None;incumbent_cost=None
order=sorted([f.parent.name for f in base.glob('*/completed.json')],key=lambda name:(0 if name=='input-verified' else 1,json.loads((base/name/'completed.json').read_text())['started_at']))
for name in order:
 f=base/name
 if not (f/'completed.json').exists():continue
 r=json.loads((f/'completed.json').read_text());v=r['after'];is_control=name.startswith('routing-control');is_input=name=='input-verified'
 if is_input or (is_control and incumbent_cost is None) or (name=='routing-control-01') or r.get('retained'):
  incumbent=name;incumbent_cost=v['feasibility_cost']
 netopens=Counter()
 for issue in json.loads((f/'drc.json').read_text())['unconnected_items']:
  nets=set()
  for item in issue['items']:
   m=re.search(r'\[([^]]+)\]',item['description'])
   if m:nets.add(m.group(1))
  netopens.update(nets)
 rows.append({'id':r['id'],'stage':name,'source_sha':r['source_sha'],'action':r['action'],'started_at':r['started_at'],'finished_at':r['finished_at'],'opens':v['native_open_count'],'loss':v['feasibility_cost'],'required_findings':len(v['required_violations']),'erc':v.get('erc_violations'),'schematic_parity':v['schematic_parity_issues'],'accepted':v['accepted'],'retained':r.get('retained',False),'incumbent':incumbent,'retained_loss':incumbent_cost,'retained_opens':json.loads((base/incumbent/'evaluation.json').read_text())['native_open_count'] if incumbent else None,'wire_length_mm':v['wire_length_mm'],'vias':v['vias'],'net_opens':dict(netopens),'board_sha256':v['board_sha256'],'files':{k:str((f/k).relative_to(base)) for k in ['board.png','board.svg','pcbgolf.kicad_pcb','preview.kicad_pcb','acceptance.json','completed.json']},'command_elapsed_seconds':sum(c['elapsed_seconds'] for c in r['commands'])})
result={'schema':1,'family':'large-loop','title':'PCB Golf-inspired 156-part four-port automotive I/O','component_count':156,'net_count':164,'source_root':str(base),'steps':rows,'retained_stage':incumbent,'accepted':next((r['accepted'] for r in rows if r['stage']==incumbent),False),'limits':['84 inherited required footprint findings remain in native loss; no feasible board claim.','Routing-only gains are distinct from placement gains.','Fixed ceilings: 240 seconds, 100 passes, one thread, both layers. Backend may finish early.','Two controls test repeatability of this input only; no general policy superiority is claimed.'],'failures':[json.loads(f.read_text()) for f in base.glob('*-failure.json')]}
a.output.write_text(json.dumps(result,indent=2));print({'steps':len(rows),'retained_stage':incumbent,'accepted':result['accepted']})
