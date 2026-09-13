"""On-demand, cutoff-keyed replay builds in the owned local output directory."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess,sys,threading
ROOT=Path(__file__).resolve().parents[3];LOCAL=ROOT/'.local/copperhead';BASE=LOCAL/'replays/on-demand';LOCK=threading.Lock()
def write(p,d):
 q=p.with_suffix('.tmp');q.write_text(json.dumps(d,indent=2));q.replace(p)
def start():
 with LOCK:
  records=[]
  for p in sorted((LOCAL/'runs').glob('stage1-*/attempt.json')):
   a=json.loads(p.read_text())
   if a.get('status') in ('completed','failed') and a.get('finished_at') and a.get('before'):records.append(dict(path=str(p),record=a))
  assert records,'No completed native checkpoint is available'
  signature=[(x['record']['attempt'],x['record']['status'],x['record'].get('after',{}).get('design_sha256')) for x in records]
  signature.append(hashlib.sha256((ROOT/'scripts/copperhead_replay.py').read_bytes()).hexdigest());key=hashlib.sha256(json.dumps(signature).encode()).hexdigest()[:20];d=BASE/key;d.mkdir(parents=True,exist_ok=True)
  if (d/'state.json').exists():return status(key)
  snapshot=dict(cutoff=datetime.now(timezone.utc).isoformat(),records=records);write(d/'snapshot.json',snapshot)
  state=dict(key=key,state='building',cutoff=snapshot['cutoff'],latest_attempt=records[-1]['record']['attempt'],latest_completed_at=records[-1]['record']['finished_at'],attempt_count=len(records));write(d/'state.json',state)
  with (d/'build.log').open('w') as log:
   process=subprocess.Popen([str(ROOT/'.venv/bin/python'),'-m','copper_scar.tools.copperhead.replay_service',key],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
  state['pid']=process.pid;write(d/'state.json',state);return state
def status(key):
 if len(key)!=20 or any(c not in '0123456789abcdef' for c in key):raise ValueError('Invalid replay key')
 return json.loads((BASE/key/'state.json').read_text())
def build(key):
 d=BASE/key
 try:
  subprocess.run([str(ROOT/'.venv/bin/python'),str(ROOT/'scripts/copperhead_replay.py'),'--snapshot',str(d/'snapshot.json'),'--output-dir',str(d)],cwd=ROOT,check=True)
  state=status(key);state.update(state='ready',fast='/file/'+str((d/'copperhead-latest-replay-5x.mp4').relative_to(LOCAL)));write(d/'state.json',state)
 except Exception as e:
  state=status(key);state.update(state='error',error=str(e),log='/file/'+str((d/'build.log').relative_to(LOCAL)));write(d/'state.json',state)
if __name__=='__main__':build(sys.argv[1])
PAGE='''<!doctype html><html><meta charset="utf-8"><title>Copperhead · Replay to latest</title><style>body{margin:24px;background:#0c141b;color:#e6eef3;font:17px system-ui}a,button{color:#77ddcb}button{background:#14232e;border:1px solid #77ddcb;padding:10px;margin-right:10px;cursor:pointer}video{width:100%;max-height:76vh}small{color:#b5c9d7}</style><h1>Copperhead · Replay to latest</h1><button id="refresh">Snapshot latest and replay from start</button><strong>5× replay</strong><a href="/">Live dashboard</a><p id="status">Loading…</p><small>Earliest available native checkpoint through the displayed cutoff; earlier placement preparation was not recorded. Trial board at right, attempted and retained-best trajectory at left.</small><video hidden id="video" controls muted autoplay playsinline></video><script>
const v=document.getElementById('video'),s=document.getElementById('status');let ready=null,request=0;
function play(speed){if(!ready)return;v.hidden=false;v.src=ready[speed];v.load();v.currentTime=0;v.play().catch(()=>{});}
async function poll(d,id){if(id!==request)return;s.textContent=d.state+' · '+d.attempt_count+' finalized attempts · latest '+d.latest_attempt+' · completed '+d.latest_completed_at+' · snapshot '+d.cutoff;if(d.state==='ready'){ready=d;play('fast');return;}if(d.state==='error'){s.textContent+=' · '+d.error;return;}setTimeout(async()=>{try{poll(await(await fetch('/api/replay/status?key='+d.key)).json(),id)}catch(e){s.textContent='error · '+e}},1500)}
async function start(){const id=++request;ready=null;v.pause();v.hidden=true;s.textContent='Snapshotting completed checkpoints…';try{poll(await(await fetch('/api/replay/build',{method:'POST'})).json(),id)}catch(e){s.textContent='error · '+e}}
document.getElementById('refresh').onclick=start;start();</script></html>'''
