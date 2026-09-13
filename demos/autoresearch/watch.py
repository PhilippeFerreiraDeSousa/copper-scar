#!/usr/bin/env python3
"""Foreground read-only observability worker. Does not launch CAD experiments."""
import argparse,fcntl,hashlib,json,subprocess,sys,time
from pathlib import Path
from build import build
from model import sha

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--stop-after-decision',action='store_true');a=ap.parse_args();a.output.mkdir(parents=True,exist_ok=True);lock=(a.output/'build.lock').open('a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB);scripts=Path(__file__).parent;seen={}
 while True:
  state=build(a.source,a.output);assert not state['fixture'];remote=a.output/'remote';receipt=remote/'verified.json';verified=json.loads(receipt.read_text()) if receipt.exists() else {}
  if verified.get('source_events_sha256')!=state['events_sha256']:
   subprocess.run([sys.executable,str(scripts/'publish.py'),'--output',str(a.output)],check=True,timeout=180)
   state=build(a.source,a.output)
  root=a.source.parent
  for rp in sorted((root/'runs').glob('stage1-*/attempt.json')):
   # Exact experiment-owned input identity; unrelated historical runs are excluded.
   try:record=json.loads(rp.read_text())
   except json.JSONDecodeError:continue
   pid=next((p['id'] for p in state['policies'] if any(x.get('attempt_id')==record.get('attempt') for x in p['points'])),None)
   if not pid:continue
   log=root/'candidates'/record['attempt']/'router.log';command=rp.parent/'route.command.json'
   if not log.exists():continue
   digest=sha(log);heartbeat=json.loads(command.read_text()) if command.exists() else {};signature=(digest,heartbeat.get('state'));prior=seen.get(record['attempt'])
   if not prior:
    saved=remote/'router-logs'/record['attempt']/'remote-verified.json'
    if saved.exists():
     receipt=json.loads(saved.read_text());hashes={e['file']:e['sha256'] for e in receipt.get('sources',[])}
     if hashes.get('router.log')==digest and command.exists() and hashes.get('route.command.json')==sha(command):seen[record['attempt']]=(signature,time.monotonic());continue
   if prior and prior[0]==signature and (heartbeat.get('state')!='running' or time.monotonic()-prior[1]<120):continue
   run_id='policy-'+hashlib.sha256((state['experiment_id']+'/'+pid).encode()).hexdigest()[:16]
   subprocess.run([sys.executable,str(scripts/'publish_logs.py'),'--run-id',run_id,'--attempt',record['attempt'],'--output',str(remote)],check=True,timeout=90)
   seen[record['attempt']]=(signature,time.monotonic())
  if state['decisions'] and a.stop_after_decision:break
  time.sleep(30)
if __name__=='__main__':main()
