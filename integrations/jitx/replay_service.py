"""On-demand immutable replay jobs. No native JITX operations."""
from pathlib import Path
import hashlib,json,threading,subprocess,time,os
from observability import write
B=Path('/Users/philippe/dev/copper-scar-jitx');L=B/'runs/stage1';H=Path(__file__).parent;LOCK=threading.Lock()
PYTHON='/Users/philippe/dev/copper-scar-demo/.venv/bin/python'
def read(p,default=None):
 try:return json.loads(p.read_text())
 except (ValueError,OSError):return default

def logical(name):
 name=name.removesuffix('-ids-v3')
 if name.startswith('stage1-baseline-'):return 'stage1-baseline'
 return name.removesuffix('-v2')

def completed_records(data):
 # Only newline-terminated ledger records: a concurrent append may be incomplete.
 return [json.loads(line) for line in data.splitlines(keepends=True) if line.endswith(b'\n') and line.strip()]

def select_history(records,snapshots):
 first={};latest={};failures=[]
 for i,r in enumerate(records):
  if r.get('candidate'):
   key=logical(Path(r['candidate']).name);first.setdefault(key,i)
   if r.get('policy_version')=='jitx-feasibility-v3':latest[key]=(i,r)
  elif r.get('error'):failures.append((i,r))
 result=[]
 for key,(i,r) in latest.items():
  digest=hashlib.sha256(json.dumps(r,indent=2).encode()).hexdigest()
  snap=snapshots.get(digest)
  if not snap:continue # Evaluation may be complete while its preview is still being published.
  result.append({'order':-1 if key=='stage1-baseline' else first[key],'record_index':i,'source_action':key,'evaluation':r,'snapshot':snap,'label':Path(r['candidate']).name.removesuffix('-ids-v3'),'caption':'Completed checkpoint; original rules checked','held':False})
 for i,r in failures:result.append({'order':i,'record_index':i,'source_action':r.get('proposal',{}).get('id'),'label':r.get('proposal',{}).get('id','Failed attempt'),'caption':r['error'],'held':True,'failure':r})
 result.sort(key=lambda x:x['order'])
 while result and result[0]['held']:result.pop(0)
 if not result:raise ValueError('No completed v3 board checkpoint available')
 return result

def freeze():
 data=(L/'iterations.jsonl').read_bytes();snapshots={}
 for p in (L/'previews').glob('*/snapshot.json'):
  s=read(p)
  if s:snapshots[s['evaluation_sha256']]=s
 steps=select_history(completed_records(data),snapshots)
 fingerprint=[{'record_index':s['record_index'],'evaluation':s.get('snapshot',{}).get('evaluation_sha256'),'failure':s.get('failure')} for s in steps]
 key=hashlib.sha256(json.dumps(fingerprint,sort_keys=True).encode()+(H/'replay.py').read_bytes()+b'replay-only-5x-v1').hexdigest()[:20]
 path=L/'replays'/('latest-'+key);last=steps[-1];r=last.get('evaluation',last.get('failure',{}))
 request={'key':key,'run':str(path),'captured_at':time.time(),'cutoff_checkpoint':last['label'],'cutoff_record_index':last['record_index'],'cutoff_time':r.get('started_at',r.get('time')),'earliest':'Earliest available full-board baseline; placement preparation before recording is unavailable.','policy':'jitx-feasibility-v3','steps':steps,'ledger_sha256':hashlib.sha256(data).hexdigest()}
 path.mkdir(parents=True,exist_ok=True)
 if not (path/'request.json').exists():write(path/'request.json',request)
 return read(path/'request.json')

def status():
 s=read(L/'replay-latest.json',{'state':'not_built'})
 if s.get('state')=='building' and s.get('pid'):
  try:os.kill(s['pid'],0)
  except ProcessLookupError:s={**s,'state':'error','error':'Replay worker exited before reporting completion'}
 return s

def build(request):
 p=Path(request['run']);s={k:request[k] for k in ['key','run','captured_at','cutoff_checkpoint','cutoff_record_index','cutoff_time','earliest']};s.update(state='building')
 with (p/'worker.stdout').open('w') as stdout,(p/'worker.stderr').open('w') as stderr:
  proc=subprocess.Popen([PYTHON,str(H/'replay.py'),'--request',str(p/'request.json')],stdout=stdout,stderr=stderr,start_new_session=True)
  s['pid']=proc.pid;write(L/'replay-latest.json',s)
  rc=proc.wait()
 if rc==0:
  s.update(state='ready',ready_at=time.time(),video='/file/'+str((p/'jitx-stage-one-replay-5x.mp4').relative_to(B)),playback='5x',manifest='/file/'+str((p/'manifest.json').relative_to(B)))
 else:s.update(state='error',error=f'Replay rendering failed (exit {rc}); see saved worker.stderr')
 write(p/'job.json',s)
 with LOCK:
  queued=read(L/'replay-pending.json')
  if queued:
   (L/'replay-pending.json').unlink()
   next_state={k:queued[k] for k in ['key','run','captured_at','cutoff_checkpoint','cutoff_record_index','cutoff_time','earliest']};next_state['state']='building';write(L/'replay-latest.json',next_state)
   threading.Thread(target=build,args=(queued,),daemon=True).start()
  else:write(L/'replay-latest.json',s)

def start():
 with LOCK:
  current=status()
  request=freeze()
  if current['state']=='building':
   if request['key']!=current['key']:
    write(L/'replay-pending.json',request)
    current.update(queued_cutoff=request['cutoff_checkpoint'],queued_key=request['key'])
    write(L/'replay-latest.json',current)
   return current
  cached=read(Path(request['run'])/'job.json')
  if cached and cached.get('state')=='ready':write(L/'replay-latest.json',cached);return cached
  # Publish building before releasing the lock, avoiding duplicate requests.
  s={k:request[k] for k in ['key','run','captured_at','cutoff_checkpoint','cutoff_record_index','cutoff_time','earliest']};s['state']='building';write(L/'replay-latest.json',s)
  threading.Thread(target=build,args=(request,),daemon=True).start();return s
