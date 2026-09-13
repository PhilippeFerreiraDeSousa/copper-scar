"""Read-only localhost JITX view. Presentation/heartbeat patterns adapted from Copperhead.
No writes to Copperhead; no shared acceptance checker. Historical gaps remain unknown.
"""
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse,unquote
import argparse,json,mimetypes,os,statistics,time,subprocess,hashlib
from observability import write
import replay_service
B=Path('/Users/philippe/dev/copper-scar-jitx');L=B/'runs/stage1';HERE=Path(__file__).parent
MOVES={'stage1-moved-004':'iteration-004-runtime-move/placement-delta.json','stage1-moved-routed-005':'iteration-004-runtime-move/placement-delta.json'}
COPPER={'stage1-moved-004':'copper-audits/002-to-live-move-004.json','stage1-moved-routed-005':'copper-audits/004-to-targeted-005.json','iteration-006-jlc-four-layer':'copper-audits/002-to-fresh-006.json'}
def read(p,default=None):
 try:return json.loads(p.read_text())
 except (OSError,ValueError):return default

def alive(pid):
 try:os.kill(int(pid),0);return True
 except (ValueError,TypeError,ProcessLookupError,PermissionError):return False

def state():
 snapshots={}
 for p in (L/'previews').glob('*/snapshot.json'):
  r=read(p,{})
  if r.get('candidate'):snapshots[r.get('evaluation_sha256')]=r
 rows=[]
 for i,line in enumerate((L/'iterations.jsonl').read_text().splitlines()):
  try:r=json.loads(line)
  except ValueError:continue
  cp=r.get('candidate');name=Path(cp).name if cp else r.get('proposal',{}).get('id',f'failure-{i}')
  row={k:r.get(k) for k in ['candidate','policy_version','metrics','cost','valid','retain','reasons','error','action','invariants_ok','evaluation_reliable','elapsed_seconds','started_at','artifacts','counts','engineering_evidence']}
  row.update(id=str(i),name=name,record_index=i,superseded=r.get('policy_version') in {'jitx-feasibility-v1','jitx-feasibility-v2'},preview=snapshots.get(hashlib.sha256(json.dumps(r,indent=2).encode()).hexdigest()),phases={k:v.get('elapsed_seconds') for k,v in r.get('check_executions',{}).items() if isinstance(v,dict) and v.get('elapsed_seconds') is not None})
  base_name=name.removesuffix('-ids-v3')
  runname=base_name
  for suffix in ['-input','-placed','-routed']:
   if base_name.endswith(suffix) and (L/base_name.removesuffix(suffix)/'proposal.json').exists():runname=base_name.removesuffix(suffix)
  auditpath=L/MOVES[base_name] if base_name in MOVES else L/runname/'placement-delta.json'
  row['placement']=read(auditpath)
  row['parameters']=read(L/runname/'placement-parameters.json')
  row['proposal']=read(L/runname/'proposal.json',r.get('proposal'))
  row['attempt_provenance']=read(L/runname/'attempt-state.json')
  row['copper_delta']=read(L/COPPER[base_name]) if base_name in COPPER else read(L/runname/('placement-copper-delta.json' if base_name.endswith('-placed') else 'route-copper-delta.json' if base_name.endswith('-routed') else 'copper-delta.json'))
  row['rigid_copper_delta']=read(L/runname/'rigid-copper-delta.json')
  row['phase_records']=[read(p) for p in (L/runname).glob('*.command.json')]
  for phase in row['phase_records']:
   if phase and phase.get('elapsed_seconds') is not None:row['phases'][phase['phase']]=phase['elapsed_seconds']
  row['inventory']=read(L/'board-inventories'/(name+'.json'))
  row['warning_review']=read(L/runname/'warning-review.json')
  row['rule_sha256']=(r.get('artifacts') or {}).get('pcbgolf.kicad_pro')
  row['board_sha256']=(r.get('artifacts') or {}).get('pcbgolf.kicad_pcb')
  if cp:
   norm=read(Path(cp)/'normalization.json',{});row['normalization']=norm
  rows.append(row)
 history=replay_service.select_history(replay_service.completed_records((L/'iterations.jsonl').read_bytes()),snapshots)
 trajectory=[rows[h['record_index']] for h in history if not h['held']]
 current_ids={r['id'] for r in trajectory}
 for row in rows:
  if row['policy_version']=='jitx-feasibility-v3' and row['id'] not in current_ids:row['superseded']=True
 workers=[];durations={}
 for p in sorted(L.glob('iteration-*/proposal.json')):
  root=p.parent;st=read(root/'attempt-state.json',{});commands=read(root/'commands.json',[])
  livecommands=[read(c,{}) for c in root.glob('*.command.json')]
  commands={c['phase']:c for c in commands+livecommands if c.get('phase')}
  for c in commands.values():
   if c.get('state')=='completed' or c.get('exit_code')==0:
    if c.get('elapsed_seconds') is not None:durations.setdefault(c['phase'],[]).append(c['elapsed_seconds'])
  active=[c for c in commands.values() if c.get('state')=='running']
  if st.get('state')=='running' or active:
   for c in active or [{}]:workers.append({'attempt':root.name,'state':st.get('state'),'phase':c.get('phase'),'pid':c.get('pid'),'alive':alive(c.get('pid')),'heartbeat_at':c.get('heartbeat_at'),'phase_started_at':c.get('started_at'),'runner_alive':alive(st.get('runner_pid'))})
 # Legacy campaigns have no heartbeat. Report observed process presence, never invent one.
 ps=subprocess.run(['ps','-axo','pid=,command='],capture_output=True,text=True).stdout
 for line in ps.splitlines():
  if '/integrations/jitx/native_iteration.py ' in line:
   pid,cmd=line.strip().split(None,1)
   if not any(str(w['pid'])==pid for w in workers):workers.append({'attempt':'legacy worker (before heartbeat instrumentation)','phase':'native capture / route / export','pid':int(pid),'alive':True,'heartbeat_at':None,'command':cmd})
 for r in rows:
  for k,v in r['phases'].items():durations.setdefault(k,[]).append(v)
 return {'root':str(B),'now':time.time(),'rows':rows,'trajectory':trajectory,'best':read(L/'best-feasibility.json',{}),'controller':read(L/'controller-state.json',{}),'workers':workers,'timings':{k:{'median':statistics.median(v),'n':len(v),'min':min(v),'max':max(v)} for k,v in durations.items()},'policy_invalidation':{'v1':read(L/'policy-v1-invalidation.json',{}),'v2':read(L/'policy-v2-object-id-invalidation.json',{})},'comparison_note':'JITX raw cost is not comparable to Copperhead: different footprint revisions, layer counts, metric priorities and coverage. Stage Two locked; no valid board.'}
class Handler(BaseHTTPRequestHandler):
 def do_GET(self):
  path=unquote(urlparse(self.path).path)
  if path=='/api/replay/status':data=json.dumps(replay_service.status()).encode();kind='application/json'
  elif path=='/replay':data=(HERE/'replay.html').read_bytes();kind='text/html; charset=utf-8'
  elif path=='/api/state':data=json.dumps(state()).encode();kind='application/json'
  elif path=='/':data=(HERE/'dashboard.html').read_bytes();kind='text/html; charset=utf-8'
  elif path.startswith('/file/'):
   p=(B/path[6:]).resolve()
   if not p.is_relative_to(B) or not p.is_file():self.send_error(404);return
   # Only public task artifacts, never runtime/auth/config or dependency files.
   if not any(p.is_relative_to(B/x) for x in ['runs/stage1','candidates']):self.send_error(403);return
   data=p.read_bytes();kind=mimetypes.guess_type(p.name)[0] or 'application/octet-stream'
   if kind=='text/html':kind+='; charset=utf-8'
  else:self.send_error(404);return
  self.send_response(200);self.send_header('Content-Type',kind);self.send_header('Cache-Control','no-store');self.send_header('Content-Length',str(len(data)));self.end_headers()
  try:self.wfile.write(data)
  except (BrokenPipeError,ConnectionResetError):pass
 def do_POST(self):
  if self.path!='/api/replay/latest':self.send_error(404);return
  origin=self.headers.get('Origin')
  if origin and origin!='http://'+self.headers.get('Host',''):self.send_error(403);return
  try:result=replay_service.start();code=200
  except Exception as e:result={'state':'error','error':str(e)};code=500
  data=json.dumps(result).encode();self.send_response(code);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
 def log_message(self,*args):pass
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=53919);a=p.parse_args();s=ThreadingHTTPServer(('127.0.0.1',a.port),Handler);url=f'http://127.0.0.1:{s.server_port}/';write(L/'dashboard-server.json',{'url':url,'pid':os.getpid()});print(url,flush=True);s.serve_forever()
