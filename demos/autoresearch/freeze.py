#!/usr/bin/env python3
"""Freeze a consistent portable viewer without interrupting live ingestion."""
import argparse,hashlib,json,shutil
from pathlib import Path

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--outputs',type=Path,required=True);ap.add_argument('--destination',type=Path,required=True);a=ap.parse_args();live=a.outputs/'two-level-autoresearch';root=a.destination;out=root/'two-level-autoresearch';out.mkdir(parents=True,exist_ok=True)
 state=json.loads((live/'data.json').read_text());remote=json.loads((live/'remote/verified.json').read_text());assert remote['source_events_sha256']==state['events_sha256'],'Wait for verified remote publication'
 events=(live/state['events_snapshot_href']).read_bytes();assert hashlib.sha256(events).hexdigest()==state['events_sha256']
 for name in ['boards','attempts','manifests','decisions']:
  if (live/name).exists():shutil.copytree(live/name,out/name,dirs_exist_ok=True)
 for name in ['index.html','ingestion-receipts.jsonl','two-level-replay.mp4','replay-verified.json','ui-verified.json']:
  if (live/name).exists():shutil.copy2(live/name,out/name)
 (out/'remote').mkdir(exist_ok=True)
 for p in (live/'remote').glob('*verified.json'):shutil.copy2(p,out/'remote'/p.name)
 for name in ['router-logs','complete-evidence']:
  if (live/'remote'/name).exists():shutil.copytree(live/'remote'/name,out/'remote'/name,dirs_exist_ok=True)
 (out/'remote/verified.json').write_text(json.dumps(remote,indent=2))
 state['frozen']=True;state['remote_receipts']=remote
 (out/'data.json').write_text(json.dumps(state,indent=2));(out/'data.js').write_text('window.EXPERIMENT='+json.dumps(state)+';');(out/'events.jsonl').write_bytes(events)
 for folder in ['optimizer-research-ledger','latest-loop-experiments','higher-loop-provenance-audit']:
  if (a.outputs/folder).exists():shutil.copytree(a.outputs/folder,root/folder,dirs_exist_ok=True,ignore=shutil.ignore_patterns('frames','replay-frames','__pycache__','qa-*.png'))
 print(json.dumps({'destination':str(root),'events_sha256':state['events_sha256'],'event_count':state['event_count'],'comparison_complete':bool(state['decisions']),'live_writer_untouched':True}))
if __name__=='__main__':main()
