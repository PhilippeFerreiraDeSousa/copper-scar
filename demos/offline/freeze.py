#!/usr/bin/env python3
"""Freeze verified package metadata and atomically replace its portable ZIP."""
import argparse,hashlib,json,subprocess,sys,zipfile
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('package',type=Path);a=p.parse_args();out=a.package.resolve();d=json.loads((out/'data.json').read_text());h=d['history'];retained=[r for r in h if r.get('retained') and not r.get('failed')][-1];latest=h[-1]
qa=json.loads((out/'browser-QA.json').read_text());assert qa['status']=='pass' and qa['images_checked']==len(h)
video=json.loads((out/'video-manifest.json').read_text());assert {r['id'] for r in h}<={f['attempt'] for f in video['frames'] if f.get('attempt')}
diagnostic=json.loads((out/'diagnostics/summary.json').read_text()) if (out/'diagnostics/summary.json').exists() else None
commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
(out/'SOURCE-CHECKPOINT.json').write_text(json.dumps(dict(repository='https://github.com/PhilippeFerreiraDeSousa/copper-scar',branch='codex/offline-demo',commit=commit,evidence_built_at=d['built_at'],latest_completed_attempt=latest['id'],retained_attempt=retained['id'],retained_board_sha256=retained['board_sha256'],additive_diagnostic_packaged_at=diagnostic['packaged_at'] if diagnostic else None,source_scope='Offline demo source only; engines retain separately recorded tool source hashes.'),indent=2)+'\n')
(out/'METRICS-AS-OF.md').write_text(f"# Verified delivery checkpoint\n\nEvidence packaged: {d['built_at']}. Latest completed real-board record: `{latest['id']}` at {latest['time']}, {latest.get('opens')} opens / {latest.get('errors')} physical errors / {latest.get('warnings')} warnings.\n\nRetained board: `{retained['id']}` — {retained['opens']} missing endpoint pairs, {retained['errors']} physical errors, {retained['warnings']} warnings. No qualified product board or official score.\n\nReal-board records: {len(h)}. Joint fixture records: five; retained 53 → 51 → 49 mm, six vias, zero native opens/violations. Separate scopes.\n\nSource `{commit}` on `codex/offline-demo`. Read the exact source/evidence joins in SOURCE-CHECKPOINT.json, data.json and package-QA.json. Video timing is editorial, never measured solver throughput.\n")
if diagnostic:
 with (out/'METRICS-AS-OF.md').open('a') as f:f.write(f"\nAdditive native diagnostic packaged {diagnostic['packaged_at']}, bound to parent {diagnostic['parent_board_sha256']}: nine nets, 32 of55pairs. Existing MP4s retain the frozen attempt history above and have not been rerendered for this diagnostic addition.\n")
submission=out/'docs/submission-draft.md';text=submission.read_text();lines=text.splitlines();lines=[f'| Final source commit | `{commit}` on `codex/offline-demo` (offline packaging source) |' if l.startswith('| Final source commit |') else l for l in lines];submission.write_text('\n'.join(lines)+'\n')
subprocess.run([sys.executable,str(Path(__file__).with_name('verify.py')),str(out)],check=True)
target=out.parent/'demo-final-offline.zip';temp=target.with_suffix('.pending.zip')
with zipfile.ZipFile(temp,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for f in sorted(out.rglob('*')):
  if f.is_file():z.write(f,str(Path(out.name)/f.relative_to(out)))
with zipfile.ZipFile(temp) as z:assert z.testzip() is None
receipt=dict(archive=str(target),sha256=hashlib.sha256(temp.read_bytes()).hexdigest(),bytes=temp.stat().st_size,zip_integrity='pass',source_commit=commit,evidence_built_at=d['built_at'])
temp.replace(target);target.with_suffix('.zip.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt))
