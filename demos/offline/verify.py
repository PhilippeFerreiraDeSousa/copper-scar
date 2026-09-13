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
 if r.get('image'):
  assert (root/r['image']).is_file()
  receipt=(root/r['image']).parent/'render-receipt.json'
  if receipt.exists():
   rendered=json.loads(receipt.read_text()); assert rendered['board_sha256']==r['board_sha256']; assert rendered['image_sha256']==sha(root/r['image'])
 checked+=1
for f in ['index.html','data.js','docs/3-minute-demo-script.md','docs/submission-draft.md','docs/architecture.svg','docs/copperhead-placement-results.md','docs/jitx-topology-capture-integration-report.md','jitx/index.html']:
 assert (root/f).is_file(),f
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
report=dict(final_topology_graph_verified=gain.exists(),additive_diagnostic_pairs_verified=32 if diagnostics.exists() else None,board_evaluation_joins_verified=checked,completed_records=len(d['history']),excluded=d['excluded'],native_checks='Stored native evaluation reports; packaging does not rerun DRC.',status='pass')
(root/'package-QA.json').write_text(json.dumps(report,indent=2)+'\n')
files={str(f.relative_to(root)):sha(f) for f in sorted(root.rglob('*')) if f.is_file() and f != root/'SHA256SUMS.json'}
(root/'SHA256SUMS.json').write_text(json.dumps(files,indent=2)+'\n');print(json.dumps(report))
