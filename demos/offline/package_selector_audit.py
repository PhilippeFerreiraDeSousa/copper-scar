#!/usr/bin/env python3
"""Package a private selector replay without treating it as a live learning win."""
import argparse,hashlib,json,shutil
from pathlib import Path

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def verify(dst):
 d=json.loads((dst/'selector-feedback-audit.json').read_text())
 for path,digest in d['hashes'].items():assert sha(dst/'source'/path)==digest,path
 assert d['without_R71']['eligible'] is True and d['with_R71']['eligible'] is False
 assert abs(d['with_R71']['score']-d['without_R71']['score']-100000)<1e-6
 assert d['with_R71']['foreign_net_removals']==3
 for row in d['live_checks']:assert row['with_R71']==row['without_R71']
 return d
p=argparse.ArgumentParser();p.add_argument('--reviews',type=Path,required=True);p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
dst=a.output/'selector-audit';dst.mkdir(parents=True,exist_ok=True)
for name in ['selector-feedback-audit.json','selector-feedback-audit.md']:shutil.copy2(a.reviews/name,dst/name)
d=json.loads((dst/'selector-feedback-audit.json').read_text())
for path,digest in d['hashes'].items():
 src=a.source/path;assert sha(src)==digest,path;target=dst/'source'/path;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,target)
verify(dst)
(dst/'README.md').write_text('# Selector feedback audit\n\nThis is a private deterministic replay using frozen source and the real saved R71 rejection, not a live selection run. Same-parent eligibility changes true to false and the score adds100000 for three repeated collateral removals.\n\nThe actual live003 selection ranked R123 over R66 from native previews. Its scores are identical with and without R71 feedback. Do not claim R71 caused that ranking, or that the later stale-target filter ran then. This proves an implemented heuristic mechanism, not a trained model or a successful live learning episode.\n\n[Audit](selector-feedback-audit.md) and [machine evidence](selector-feedback-audit.json). Every hash-listed replay input and source file is preserved under source/. The replay does not qualify any later placement result.\n')
print(json.dumps({'selector_private_replay_verified':True,'live_ranking_unchanged_by_R71':True,'source_files':len(d['hashes'])}))
