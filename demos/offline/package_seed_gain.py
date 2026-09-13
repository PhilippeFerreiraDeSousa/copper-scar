#!/usr/bin/env python3
"""Freeze a completed seed success, its guarded expansion, and native evidence."""
import argparse,hashlib,json,re,shutil
from pathlib import Path

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def verify(dst):
 s=read(dst/'summary.json')
 for name,h in s['files'].items():assert sha(dst/name)==h,name
 final=read(dst/'batch-attempt.json');first=read(dst/'first-attempt.json');proof=read(dst/'first-seed-connectivity.json');graph=read(dst/'final-pad-partitions.json');seeds=read(dst/'final-seed-connectivity.json')
 assert final['attempt']==s['attempt'] and final['status']=='completed' and final['became_incumbent'] is True
 assert [final['after'][k] for k in ['unconnected','errors','warnings','invariants_ok']]==[45,0,18,True]
 assert s['final_board_sha256']==final['after']['files']['pcbgolf.kicad_pcb']==graph['after']['board_sha256']==seeds['board_sha256']
 assert graph['before']['board_sha256']==final['before']['files']['pcbgolf.kicad_pcb'] and graph['before']['project_sha256']==graph['after']['project_sha256']
 old=[frozenset(x) for x in graph['before']['groups']];new=[frozenset(x) for x in graph['after']['groups']]
 assert set().union(*old)==set().union(*new) and all(any(x<=y for y in new) for x in old) and len(old)-len(new)==6
 assert first['became_incumbent'] and first['after']['unconnected']==51 and first['before']['unconnected']==52
 assert proof['all_seed_targets_connected'] and proof['board_sha256']==first['after']['files']['pcbgolf.kicad_pcb']
 strategy=final['action']['strategy_evidence'];assert strategy['attempt']==first['attempt'] and strategy['board_sha256']==proof['board_sha256']
 assert sha(dst/'campaign-frozen.py')==final['tool_source_hashes']['scripts/copperhead_campaign.py']
 source=(dst/'campaign-frozen.py').read_text();assert "if spec.get('requires_successful_seed'):" in source and "not proof.get('all_seed_targets_connected')" in source and "action['strategy_evidence']=" in source
 selection=read(dst/'production006-selection.json');chosen=read(dst/'production006-proposal.json')
 assert selection['chosen']['catalog_id']=='can-high-compatible-seven-seed-expansion' and selection['parent_board_sha256']==graph['before']['board_sha256'] and chosen['strategy_evidence']==strategy
 targets=read(dst/'target-revalidation.json');assert targets['parent_board_sha256']==graph['before']['board_sha256'] and len(targets['kept_sites'])==7
 assert len(seeds['seeds'])==7 and seeds['all_seed_targets_connected']
 for row in seeds['seeds']:
  assert row['target_pad_connected'] and row['diameter_nm']==450000 and row['drill_nm']==200000 and row['span']==['F.Cu','B.Cu']
  target=row['site']['target_pad'];pads=set(row['connected_pads'])
  if target in ['J5.B2','J6.B2']:assert pads=={'J5.B2','J6.B2'}
  elif target in ['J7.B2','J8.B2']:assert pads=={'J4.6','J7.B2','J8.B2','L7.4','R48.2','R56.1'}
  else:assert pads=={'J4.2','J5.A2','J6.A2','J7.A2','J8.A2','L5.4','R46.2','R50.1'}
 uses=re.findall(r'\(use_via\s+([^)]*)\)',(dst/'batch.dsn').read_text());assert uses and all(re.findall(r'"([^"]+)"',x)==['Via[0-5]_600:300_um'] for x in uses)
 geometry=read(dst/'final-via-geometry.json');assert geometry['after_sha256']==s['final_board_sha256'] and geometry['existing_via_geometry_preserved'] and not geometry['missing_existing'] and not geometry['added']
 r12=read(dst/'r12-attempt.json');assert r12['became_incumbent'] and all(r12['before'][k]==r12['after'][k] for k in ['unconnected','errors','warnings'])
 remote=read(dst/'observability-verified.json')
 for attempt in [first,r12,final]:
  row=next(row for run in remote['runs'] for row in run['rows'] if row['attempt_id']==attempt['attempt']);assert row['board_sha256']==attempt['after']['files']['pcbgolf.kicad_pcb'] and [row[k] for k in ['missing_pairs','physical_errors','warnings']]==[attempt['after'][k] for k in ['unconnected','errors','warnings']] and row['media_verified'] and row['weave_verified']
 independent=read(dst/'final-independent-audit.json');assert independent['final_board_sha256']==s['final_board_sha256']
 assert independent['refilled_unsaved_DRC']=={'opens':45,'errors':0,'warnings':18} and independent['raw_saved_DRC']['errors']==8
 ig=independent['native-islands.json'];assert ig['changed_pad_partition_nets']=={'CAN0_H':{'before':4,'after':1},'CAN2_H':{'before':5,'after':2}} and not ig['pad_connectivity_regressions']
 for net,rows in ig['before']['pad_islands'].items():
  old=[frozenset(x['pads']) for x in rows];new=[frozenset(x['pads']) for x in ig['after']['pad_islands'][net]]
  assert set().union(*old)==set().union(*new) and all(any(x<=y for y in new) for x in old),net
 vg=independent['final-native-geometry-proof.json'];assert vg['before']['via_count']==670 and vg['after']['via_count']==677 and vg['all_existing_via_net_site_drill_span_and_all_layer_diameters_preserved'] and vg['project_bytes_equal']
 assert independent['footprint-geometry-proof.json']=={'complete_footprints_equal':True,'count':245}
 return s

def build(root,reviews,proof,report,independent_root,out):
 run=root/'runs/stage1-20260913-061700-fbe016';first_run=root/'runs/stage1-20260913-055432-134c1a';r12_run=root/'runs/stage1-20260913-060615-28bd51';d=read(run/'attempt.json');dst=out/'seed-gain';dst.mkdir(parents=True,exist_ok=True)
 sources={'batch-attempt.json':run/'attempt.json','batch-proposal.json':run/'via-seed-proposal.json','final-pad-partitions.json':run/'final-pad-partitions.json','final-seed-connectivity.json':run/'final-seed-connectivity.json','final-via-geometry.json':run/'final-via-geometry.json','batch.dsn':Path(d['candidate'])/'pcbgolf.dsn','first-attempt.json':first_run/'attempt.json','first-seed-connectivity.json':first_run/'final-seed-connectivity.json','first-independent-audit.json':reviews/'j5-seed-final-audit.json','first-independent-report.md':reviews/'j5-seed-final-audit.md','r12-attempt.json':r12_run/'attempt.json','r12-pad-partitions.json':r12_run/'final-pad-partitions.json','production004-selection.json':root/'campaign/004-0940a715-1789304071-selection.json','production006-selection.json':Path(d['action']['campaign_selection']),'target-revalidation.json':Path(d['action']['target_revalidation']),'campaign-frozen.py':run/'tool-source/scripts/copperhead_campaign.py','reviewed-catalog-snapshot.json':root/'campaign/reviewed-catalog.json','final-independent-audit.json':proof,'final-independent-report.md':report,'observability-verified.json':root/'observability/verified.json'}
 selection=read(sources['production006-selection.json']);sources['production006-proposal.json']=Path(selection['chosen']['proposal'])
 sources[proof.name]=proof;sources['j5-seed-final-audit.json']=reviews/'j5-seed-final-audit.json'
 for name,source in sources.items():shutil.copy2(source,dst/name)
 independent=read(proof)
 for filename in ['native-islands.json','final-native-geometry-proof.json','footprint-geometry-proof.json','final-new-via-join.json','independent-drc.json','refilled-drc.json']:
  source=independent_root/filename;target=dst/'independent'/filename;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,target)
  if filename in independent:assert read(source)==independent[filename]
 for rel,h in independent.get('evidence_hashes',{}).items():
  source=independent_root/rel;assert sha(source)==h,rel;target=dst/'independent'/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,target)
 record=next(r for r in read(out/'data.json')['history'] if r['id']==d['attempt']);assert record['board_sha256']==sha(Path(d['candidate'])/'pcbgolf.kicad_pcb')
 payload=dict(attempt=d['attempt'],first_attempt=read(first_run/'attempt.json')['attempt'],finished_at=d['finished_at'],final_board_sha256=record['board_sha256'],parent_board_sha256=d['before']['files']['pcbgolf.kicad_pcb'],final_evaluation=record['evaluation'],metrics=[45,0,18],files={str(p.relative_to(dst)):sha(p) for p in dst.rglob('*') if p.is_file() and p.name not in ['summary.json','README.md']})
 (dst/'summary.json').write_text(json.dumps(payload,indent=2)+'\n');verify(dst);(out/'seed-data.js').write_text('window.SEED='+json.dumps(payload)+';\n')
 (dst/'README.md').write_text('''# A proved seed connection gates a bounded expansion

First completed055432places one explicitCAN0_H seed at122.75,58.93mm and full routing joins originalJ5.A2 to its trunk,52→51opens. Its retained result and matching native attachment proof satisfy the guard in the frozen controller before the seven-site catalog expansion becomes eligible. Production006 carries that strategy_evidence and current-parent target revalidation. This is a heuristic policy with a reviewed catalog, not a trained model or proof the evidence alone chose the winning action.

Completed061700finishes45opens/0physical errors/18warnings. All seven target pads join their seeds, but six missing pairs disappear. CAN0_H J6/J7/J8.A2 join the existing trunk. CAN2_H J7/J8.B2 join its trunk; J5/J6.B2 join only each other, retaining a separate island. No old connected pad group splits. The owner geometry check compares the already-seeded board with the final result; independent evidence separately checks original-parent geometry.

The frozen source has stale saved zone fills: raw DRC reports8clearance errors, while independent unsaved refill reports45/0/18. The publication/ directory contains a separately refilled/saved board with its own hash, fresh saved-file DRC and preservation proof. Historical CAD and W&B receipts remain bound to the original source hash.

The batch DSN contains both padstack definitions, but its use_via rule allows only600/300um new router vias. Explicit450/200um seed geometry is preserved. The later persistence fix was not part of this execution. Do not describe both sizes as eligible for new creation in this batch.

Intervening R12 remains51/0/18, retained on diagnostic distance with no electrical count gain. Production004 excludes the failed R123 pose, but its priority catalog chooses the J5 seed; do not attribute the winner solely to the failure. No fresh unchanged-parent control isolates seed placement from full routing. The board is incomplete and not fully manufacturing-qualified.

Inspect [independent final report](final-independent-report.md), [independent audit](final-independent-audit.json), [seven final seed connections](final-seed-connectivity.json), [first attachment proof](first-seed-connectivity.json), [frozen controller](campaign-frozen.py), [production006](production006-selection.json), [target revalidation](target-revalidation.json), [production004](production004-selection.json), [R12 immutable attempt](r12-attempt.json), and [publication receipt](observability-verified.json). The current catalog copy is labeled a snapshot; strategy_evidence and the source hash are bound to the completed attempt.
''')
 print(json.dumps({'attempt':d['attempt'],'metrics':[45,0,18],'files':len(payload['files']),'verified':True}))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--reviews',type=Path,required=True);p.add_argument('--proof',type=Path,required=True);p.add_argument('--report',type=Path,required=True);p.add_argument('--independent-root',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();build(a.source,a.reviews,a.proof,a.report,a.independent_root,a.output)
