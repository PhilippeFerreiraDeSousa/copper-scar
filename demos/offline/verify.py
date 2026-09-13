#!/usr/bin/env python3
"""Verify portable evidence joins and native board hashes, then freeze inventory."""
import argparse, hashlib, json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('package',type=Path);a=p.parse_args();root=a.package.resolve()
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
d=json.loads((root/'data.json').read_text());checked=0
for r in d['history']:
 if not r.get('board'): continue
 board=root/r['board'];e=json.loads((root/r['evaluation']).read_text())
 assert sha(board)==r['board_sha256']==e['files']['pcbgolf.kicad_pcb'],r['id']
 assert [r[k] for k in ['opens','errors','warnings']]==[e[k] for k in ['unconnected','errors','warnings']],r['id']
 assert (root/r['receipt']).is_file()
 if r.get('retention_correction'):
  correction=json.loads((root/r['retention_correction']).read_text());original=root/r['original_attempt'];historical=json.loads(original.read_text())
  assert sha(original)==r['original_attempt_sha256'] and historical['became_incumbent']==r['historical_retained']
  assert correction['attempt']==r['id'] and r['retained'] is False
  assert correction['fresh_before']==historical['diagnostic_priority_before'] and correction['after']==historical['diagnostic_priority_after']
 if r.get('selection_confirmation'):
  confirmation=json.loads((root/r['selection_confirmation']).read_text());original=root/r['original_attempt'];historical=json.loads(original.read_text())
  assert sha(original)==r['original_attempt_sha256'] and historical['became_incumbent'] is True and r['retained'] is True
  assert confirmation['attempt']==r['id'] and confirmation['effective_retained'] and confirmation['selection_decision']['eligible']
  proof=json.loads((root/r['pad_partition_proof']).read_text())
  assert proof['before']['board_sha256']==historical['before']['files']['pcbgolf.kicad_pcb'] and proof['after']['board_sha256']==r['board_sha256']
  assert {frozenset(x) for x in proof['before']['groups']}=={frozenset(x) for x in proof['after']['groups']}
  assert proof['before']['project_sha256']==proof['after']['project_sha256']
  decision=confirmation['selection_decision'];assert decision['basis']=='manufacturing_repair'
  assert [x['type'] for x in historical['before']['manufacturing_findings']]==['hole_to_hole']
  assert historical['after']['manufacturing_findings']==[] and historical['after']['manufacturing_rules_clear'] is True
  assert [historical['before'][k] for k in ['unconnected','errors','warnings']]==[53,0,19] and [r[k] for k in ['opens','errors','warnings']]==[53,0,18]
  remote=json.loads((original.parent/'observability-verified.json').read_text());row=next(row for run in remote['runs'] for row in run['rows'] if row['attempt_id']==r['id'])
  assert row['board_sha256']==r['board_sha256'] and [row[k] for k in ['missing_pairs','physical_errors','warnings']]==[r[k] for k in ['opens','errors','warnings']] and row['media_verified'] and row['weave_verified']
 if r.get('scope_correction'):
  original=root/r['original_attempt'];historical=json.loads(original.read_text());scope=json.loads((root/r['scope_correction']).read_text())
  assert sha(original)==r['original_attempt_sha256'] and scope['original_proposal_preserved']
  assert scope['historical_proposal_nets']==historical['action']['nets'] and scope['actual_terminal_nets']==['GND','CAN0_H','CH4_D_P']
 if r.get('image'):
  assert (root/r['image']).is_file()
  receipt=(root/r['image']).parent/'render-receipt.json'
  if receipt.exists():
   rendered=json.loads(receipt.read_text()); assert rendered['board_sha256']==r['board_sha256']; assert rendered['image_sha256']==sha(root/r['image'])
 checked+=1
for f in ['index.html','data.js','docs/3-minute-demo-script.md','docs/submission-draft.md','docs/architecture.svg','docs/copperhead-placement-results.md','docs/jitx-topology-capture-integration-report.md','jitx/index.html']:
 assert (root/f).is_file(),f
publication=root/'publication/summary.json'
if publication.exists():
 from package_publication import verify as verify_publication
 verify_publication(root)
seed=root/'seed-gain/summary.json'
if seed.exists():
 from package_seed_gain import verify as verify_seed
 verify_seed(seed.parent)
selector=root/'selector-audit/selector-feedback-audit.json'
if selector.exists():
 audit=json.loads(selector.read_text())
 for path,digest in audit['hashes'].items():assert sha(selector.parent/'source'/path)==digest
 assert audit['without_R71']['eligible'] is True and audit['with_R71']['eligible'] is False
 assert abs(audit['with_R71']['score']-audit['without_R71']['score']-100000)<1e-6
 assert all(row['with_R71']==row['without_R71'] for row in audit['live_checks'])
via=root/'via-gain/summary.json'
if via.exists():
 from package_via_gain import verify as verify_via
 v=verify_via(via.parent);assert v['final_board_sha256'] in {r.get('board_sha256') for r in d['history']}
placement=root/'placement-gain/summary.json'
if placement.exists():
 p=json.loads(placement.read_text());assert p['final_board_sha256'] in {r.get('board_sha256') for r in d['history']}
 for name,digest in p['files'].items():assert sha(root/'placement-gain'/name)==digest
 assert p['independent_pose_and_graph_verified'] and p['observability']['final_row']['media_verified'] and p['observability']['final_row']['weave_verified']
gain=root/'topology-gain/summary.json'
if gain.exists():
 g=json.loads(gain.read_text());assert g['final_board_sha256'] in {r.get('board_sha256') for r in d['history']}
 for name,digest in g['files'].items():assert sha(root/'topology-gain'/name)==digest
 assert g['final_graph_verified']
 if g['observability']:assert g['observability']['final_row']['media_verified'] and g['observability']['final_row']['weave_verified']
diagnostics=root/'diagnostics/summary.json'
if diagnostics.exists():
 diag=json.loads(diagnostics.read_text()); assert diag['parent_board_sha256'] in {r.get('board_sha256') for r in d['history']}
 assert sha(root/'diagnostics/connectivity-islands.json')==diag['source_json_sha256']
 assert sha(root/'diagnostics/connectivity-island-review.md')==diag['source_review_sha256']
 assert sha(root/'diagnostics/parent.kicad_pro')==diag['parent_project_sha256']
 assert sum(r['pairs'] for r in diag['rows'])==diag['covered_pairs']==32
feedback=root/'feedback-chain/portable.json'
if feedback.exists():
 chain=json.loads(feedback.read_text())
 for ref in chain['files'].values():assert sha(root/ref['path'])==ref['sha256']
 for key in ['prior_id','following_id']:assert (root/'evidence'/chain[key]/'evaluation.json').exists()
for f in ['copper-scar-demo-normal.mp4','copper-scar-demo-5x.mp4']:
 m=json.loads((root/'video-manifest.json').read_text());assert sha(root/f)==m['video_sha256'][f]
 if publication.exists():
  published=json.loads(publication.read_text());shown=[frame for frame in m['frames'] if frame.get('attempt')==published['attempt']];assert shown and all(frame.get('displayed_board_sha256')==published['board_sha256'] for frame in shown)
report=dict(refilled_publication_and_STEP_verified=publication.exists(),guarded_seed_expansion_verified=seed.exists(),selector_private_replay_verified=selector.exists(),new_via_independent_proof_verified=via.exists(),selection_confirmations_verified=sum(bool(r.get('selection_confirmation')) for r in d['history']),placement_pose_graph_verified=placement.exists(),retention_corrections_verified=sum(bool(r.get('retention_correction')) for r in d['history']),final_topology_graph_verified=gain.exists(),additive_diagnostic_pairs_verified=32 if diagnostics.exists() else None,board_evaluation_joins_verified=checked,completed_records=len(d['history']),excluded=d['excluded'],native_checks='Historical joins use stored native reports; separate refilled publication has fresh saved-file DRC and independent STEP checks.' if publication.exists() else 'Stored native evaluation reports; packaging does not rerun DRC.',status='pass')
(root/'package-QA.json').write_text(json.dumps(report,indent=2)+'\n')
files={str(f.relative_to(root)):sha(f) for f in sorted(root.rglob('*')) if f.is_file() and f != root/'SHA256SUMS.json'}
(root/'SHA256SUMS.json').write_text(json.dumps(files,indent=2)+'\n');print(json.dumps(report))
