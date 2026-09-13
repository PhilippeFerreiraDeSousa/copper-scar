"""Read-only localhost observability for actual native Stage 1 records."""
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import unquote,urlparse,parse_qs
from datetime import datetime,timezone
import argparse,json,mimetypes,os,statistics,time
from .records import load_record
ROOT=Path(__file__).resolve().parents[3];LOCAL=ROOT/'.local/copperhead'
def read(p,default=None):
 try:return json.loads(p.read_text())
 except (OSError,ValueError):return default

def state():
 rows=[]
 for p in sorted((LOCAL/'runs').glob('stage1-*/attempt.json')):
  r=load_record(p)
  if not r:continue
  row={k:r.get(k) for k in ['attempt','status','stage','started_at','finished_at','action','candidate','error','stop_reason','diagnostic_improved','metric_version','constraint_scope','diagnostic_priority_before','diagnostic_priority_after','placement_delta','classification','became_incumbent','incumbent_before','incumbent_after','comparison_kind','routing_scope','action_level','policy']}
  row['mtime']=p.stat().st_mtime;row['record']=str(p.relative_to(LOCAL));row['running_process']=False
  if r.get('runner_pid'):
   try:os.kill(r['runner_pid'],0);row['running_process']=True
   except ProcessLookupError:pass
  for key in ['before','after','placement_evaluation']:
   e=r.get(key)
   row[key]={k:e.get(k) for k in ['search_cost','unconnected','errors','warnings','invariants_ok','native_cad_ok','validity_gate','engineering_review','assembly_completeness','hardware_proof','report','design_sha256']} if e else None
  cp=Path(r['candidate']);row['preview']=str((cp/'board.svg').relative_to(LOCAL)) if r.get('status')=='completed' and r.get('after') and (cp/'board.svg').exists() and (cp/'board.svg').stat().st_mtime>=datetime.fromisoformat(r['finished_at']).timestamp() else None
  row['phases']={};row['phase']='between commands';row['phase_elapsed']=0;row['worker_alive']=False;row['heartbeat']=None
  for cp in sorted(p.parent.rglob('*.command.json'),key=lambda x:x.stat().st_mtime):
   cr=read(cp,{})
   group=cp.parent.name if cp.parent.name in ('before','after') else cp.name.removesuffix('.command.json')
   row['phases'][group]=row['phases'].get(group,0)+cr.get('elapsed_seconds',0)
   if cr.get('state')=='running':
    row['phase']=group;row['phase_elapsed']=max(0,time.time()-datetime.fromisoformat(cr['started_at']).timestamp());row['heartbeat']=cr.get('heartbeat_at');row['worker_pid']=cr.get('pid')
    try:os.kill(cr['pid'],0);row['worker_alive']=True
    except (ProcessLookupError,KeyError):pass
  row['duration']=max(0,datetime.fromisoformat(row['finished_at']).timestamp()-datetime.fromisoformat(row['started_at']).timestamp()) if row.get('finished_at') else None
  rows.append(row)
 timings={}
 for action in {r.get('action',{}).get('kind') for r in rows if r.get('action')}:
  durations=[r['duration'] for r in rows if r.get('action',{}).get('kind')==action and r['status']=='completed' and r['duration'] is not None]
  if durations:timings[action]=dict(n=len(durations),median=statistics.median(durations),minimum=min(durations),maximum=max(durations))
 return dict(campaign=read(LOCAL/'campaign/state.json',{}),observability=read(LOCAL/'observability/verified.json',{}),controller=read(LOCAL/'controller-state.json',{}),timings=timings,now=datetime.now(timezone.utc).isoformat(),root=str(LOCAL),rows=rows,loop=read(LOCAL/'loop/state.json',{}),current=read(LOCAL/'current-status.json',{}),viewer=read(LOCAL/'viewer-state.json',{}))
class Handler(BaseHTTPRequestHandler):
 def do_POST(self):
  if urlparse(self.path).path!="/api/replay/build":self.send_error(404);return
  from .replay_service import start
  try:data=json.dumps(start(parse_qs(urlparse(self.path).query).get('view',['outer'])[0])).encode()
  except Exception as e:data=json.dumps(dict(state="error",error=str(e))).encode()
  self.send_response(200);self.send_header("Content-Type","application/json");self.end_headers();self.wfile.write(data)
 def do_GET(self):
  path=unquote(urlparse(self.path).path)
  if path=='/replay/latest':
   from .replay_service import PAGE
   data=PAGE.encode();kind='text/html; charset=utf-8'
  elif path=='/api/replay/status':
   from .replay_service import status
   try:data=json.dumps(status(parse_qs(urlparse(self.path).query)['key'][0])).encode()
   except Exception as e:data=json.dumps(dict(state='error',error=str(e))).encode()
   kind='application/json'
  elif path=='/api/state':data=json.dumps(state()).encode();kind='application/json'
  elif path=='/':data=Path(__file__).with_name('dashboard.html').read_bytes();kind='text/html; charset=utf-8'
  elif path.startswith('/file/'):
   p=(LOCAL/path[6:]).resolve()
   if not p.is_relative_to(LOCAL) or not p.is_file():self.send_error(404);return
   data=p.read_bytes();kind=mimetypes.guess_type(p.name)[0] or 'application/octet-stream'
  else:self.send_error(404);return
  self.send_response(200);self.send_header('Content-Type',kind);self.send_header('Cache-Control','no-store');self.send_header('Content-Length',str(len(data)));self.end_headers()
  try:self.wfile.write(data)
  except (BrokenPipeError,ConnectionResetError):pass
 def log_message(self,*args):pass
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--port',type=int,default=0);a=ap.parse_args();server=ThreadingHTTPServer(('127.0.0.1',a.port),Handler);url=f'http://127.0.0.1:{server.server_port}/';(LOCAL/'dashboard-server.json').write_text(json.dumps(dict(url=url,pid=os.getpid())));print(url,flush=True);server.serve_forever()
