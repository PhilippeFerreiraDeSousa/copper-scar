#!/usr/bin/env python3
"""Package saved native connectivity evidence without running or changing CAD."""
import argparse,datetime,hashlib,json,shutil
from pathlib import Path

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def build(source,output):
 original=source/'connectivity-islands.json';review=source/'connectivity-island-review.md';d=json.loads(original.read_text());dst=output/'diagnostics';dst.mkdir(parents=True,exist_ok=True)
 hashes=d['source_hashes'];board=next(Path(p) for p in hashes if p.endswith('.kicad_pcb'));project=next(Path(p) for p in hashes if p.endswith('.kicad_pro'))
 assert sha(board)==hashes[str(board)] and sha(project)==hashes[str(project)]
 h=json.loads((output/'data.json').read_text())['history'];matches=[r for r in h if r.get('board_sha256')==hashes[str(board)]];assert matches
 parent=matches[0];assert sha(output/parent['board'])==sha(board)
 assert d['native_open_count_after_memory_refill']==55 and d['zones_filled_in_memory'] and not d['saved_CAD'] and not d['routing_performed']
 rows=[];can_pads=0
 for net,n in d['nets'].items():
  islands=n['islands'];assert n['island_count']==len(islands)==n['pair_count']+1
  assert len(n['reported_pairs'])==n['pair_count']
  ids={i['index'] for i in islands}
  for pair in n['reported_pairs']:assert len(pair['islands'])==2 and pair['islands'][0]!=pair['islands'][1] and set(pair['islands'])<=ids
  single=[i for i in islands if i['isolated_single_pad']]
  pads=[f"{p['ref']}.{p['pad']}" for i in single for p in i['pads']]
  main=max(islands,key=lambda i:sum(i['item_counts'].values()))
  if net.startswith('CAN'):
   assert all(i['item_counts']=={'PAD':1} and i['pads'][0]['copper_layers']==['F.Cu'] and i['pads'][0]['drill_mm']==[0.0,0.0] for i in single)
   can_pads+=len(pads);finding='Main trunk connected; isolated connector pads have no attached track or via.';action='Inspect supported terminal escape while preserving the connected trunk.'
  elif net=='GND':
   assert len(main['zone_parents'])==2 and set(main['zone_parents'].values())=={'In1.Cu','In4.Cu'}
   assert len(single)==9 and len(islands)-1==10
   finding='Both planes share one main island; nine lone pads and the U15.3 + U15.PAD island lack access.';action='Check legal access to plane-connected copper; joining two isolated pads alone is insufficient.'
  elif net=='CH2_D_P':
   assert len(single)==3 and all(i['item_counts']=={'PAD':1} for i in islands)
   finding='Three separate pads; no attached route copper on the net.';action='Evaluate connector join plus hub path as a three-terminal routing request.'
  elif net=='CH4_D_P':
   assert pads==['J8.A6'] and main['item_counts']=={'PAD':2,'TRACK':16,'VIA':4}
   finding='J8.A6 is isolated; the other two pads already share routed copper.';action='Inspect one terminal escape while preserving the existing route.'
  else:raise AssertionError(net)
  rows.append(dict(net=net,islands=n['island_count'],pairs=n['pair_count'],isolated_pads=pads,main_counts=main['item_counts'],finding=finding,next_investigation=action,attempt_status=n['attempt_status'],legality=n['new_attachment_legality']))
 assert can_pads==19 and sum(r['pairs'] for r in rows)==32 and len(rows)==9
 shutil.copy2(original,dst/original.name);shutil.copy2(review,dst/review.name);shutil.copy2(project,dst/'parent.kicad_pro')
 payload=dict(packaged_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),parent_board_sha256=sha(board),parent_project_sha256=sha(project),parent_attempt=parent['id'],parent_board='../'+parent['board'],source_json_sha256=sha(original),source_review_sha256=sha(review),recorded_drc_sha256=d['drc_sha256'],native_version=d['kicad_version'],covered_pairs=32,total_pairs=55,rows=rows,scope='Nine-net native connectivity review of the hash-bound retained parent. Existing copper access is measured; new-route legality and blocking cause are unknown.',method=d['method'],zone_refill='Both zones refilled in unsaved memory before connectivity analysis; input board/project bytes preserved.',cad_changed=False,routing_performed=False)
 (dst/'summary.json').write_text(json.dumps(payload,indent=2)+'\n');(output/'diagnostics-data.js').write_text('window.DIAGNOSTICS='+json.dumps(payload)+';\n')
 shutil.copy2(Path(__file__).with_name('diagnostics.html'),dst/'index.html')
 print(json.dumps(dict(diagnostic_parent_hash=sha(board),covered_pairs=32,nets=len(rows),can_connector_pad_islands=can_pads,native_rerun=False)))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();build(a.source,a.output)
