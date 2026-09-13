#!/usr/bin/env python3
"""Stream a portable pilot-first ZIP, excluding publisher runtimes and credentials."""
import argparse,hashlib,json,zipfile
from pathlib import Path

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--outputs',type=Path,required=True);ap.add_argument('--allow-incomplete',action='store_true');a=ap.parse_args();root=a.outputs;pilot=root/'two-level-autoresearch';state=json.loads((pilot/'data.json').read_text());assert not state['fixture'];assert state['decisions'] or a.allow_incomplete,'Final package requires a recorded comparison decision';remote=json.loads((pilot/'remote/verified.json').read_text());assert remote['source_events_sha256']==state['events_sha256'],'Remote publication lags this freeze';video=json.loads((pilot/'replay-verified.json').read_text());assert video['source_events_sha256']==state['events_sha256'],'Replay lags this freeze'
 files={}
 for folder in ['boards','attempts','manifests','decisions']:
  for p in (pilot/folder).rglob('*'):
   if p.is_file():files['two-level-autoresearch/'+str(p.relative_to(pilot))]=p
 for name in ['index.html','data.js','data.json','events.jsonl','ingestion-receipts.jsonl','two-level-replay.mp4','replay-verified.json']:
  files['two-level-autoresearch/'+name]=pilot/name
 for p in (pilot/'remote').glob('*verified.json'):files['two-level-autoresearch/remote/'+p.name]=p
 for p in (pilot/'remote/router-logs').rglob('*'):
  if p.is_file():files['two-level-autoresearch/remote/'+str(p.relative_to(pilot/'remote'))]=p
 for folder in ['optimizer-research-ledger','latest-loop-experiments']:
  for p in (root/folder).rglob('*'):
   if p.is_file() and 'frames' not in p.parts and not p.name.startswith('qa-'):files[folder+'/'+str(p.relative_to(root/folder))]=p
 for p in Path(__file__).parent.glob('*'):
  if p.suffix in ['.py','.html','.md']:files['reproduce/'+p.name]=p
 # Hash files first and recheck while writing. No mutable file may silently change mid-freeze.
 hashes={name:hashlib.sha256(p.read_bytes()).hexdigest() for name,p in files.items()}
 title='Completed matched policy pilot' if state['decisions'] else 'IN PROGRESS — actual matched policy pilot'
 entry=f'''<!doctype html><meta charset="utf-8"><title>Copper Scar autoresearch demo</title><style>body{{font:18px/1.6 system-ui;background:#091320;color:#e8f0f8;max-width:850px;margin:70px auto;padding:20px}}a{{color:#8bd8ff}}h1{{font-size:38px}}</style><h1>{title}</h1><p>Two rankings, one frozen candidate library, the same native starting board and routing protocol.</p><p><a href="two-level-autoresearch/index.html">Open the actual two-level experiment</a> · <a href="two-level-autoresearch/two-level-replay.mp4">Play the checkpoint video</a></p><p>Costs count three decisions per arm. Screening rejections and routed results remain separate. Board qualification is not claimed.</p><hr><p>Supporting historical evidence: <a href="latest-loop-experiments/index.html">unmatched outer-loop experiments</a> · <a href="optimizer-research-ledger/index.html">research ledger</a>.</p><p>This package opens locally without an Internet connection. W&amp;B links are optional remote evidence.</p>'''
 receipt={'fixture':False,'comparison_complete':bool(state['decisions']),'events_sha256':state['events_sha256'],'source_revision':__import__('subprocess').check_output(['git','rev-parse','HEAD'],text=True).strip(),'files':hashes}
 name='two-level-autoresearch-final.zip' if state['decisions'] else 'two-level-autoresearch-in-progress.zip';target=root/name
 with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=5) as z:
  z.writestr('index.html',entry);z.writestr('package-manifest.json',json.dumps(receipt,indent=2))
  for name,p in files.items():
   data=p.read_bytes();assert hashlib.sha256(data).hexdigest()==hashes[name],('File changed during freeze',name);z.writestr(name,data)
 with zipfile.ZipFile(target) as z:
  assert z.testzip() is None
  for name,digest in hashes.items():assert hashlib.sha256(z.read(name)).hexdigest()==digest
 result={'path':str(target),'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'bytes':target.stat().st_size,'files':len(files),'comparison_complete':bool(state['decisions']),'all_archive_hashes_verified':True};target.with_suffix('.verified.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
if __name__=='__main__':main()
