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
 if r.get('image'): assert (root/r['image']).is_file()
 checked+=1
for f in ['index.html','data.js','docs/3-minute-demo-script.md','docs/submission-draft.md','docs/architecture.svg','docs/copperhead-placement-results.md','docs/jitx-topology-capture-integration-report.md','jitx/index.html']:
 assert (root/f).is_file(),f
for f in ['copper-scar-demo-normal.mp4','copper-scar-demo-5x.mp4']:
 m=json.loads((root/'video-manifest.json').read_text());assert sha(root/f)==m['video_sha256'][f]
report=dict(board_evaluation_joins_verified=checked,completed_records=len(d['history']),excluded=d['excluded'],native_checks='Stored native evaluation reports; packaging does not rerun DRC.',status='pass')
(root/'package-QA.json').write_text(json.dumps(report,indent=2)+'\n')
files={str(f.relative_to(root)):sha(f) for f in sorted(root.rglob('*')) if f.is_file() and f.name!='SHA256SUMS.json'}
(root/'SHA256SUMS.json').write_text(json.dumps(files,indent=2)+'\n');print(json.dumps(report))
