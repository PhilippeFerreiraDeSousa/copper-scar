"""JITX immutable previews and measured commands; adapted from Copperhead's local contract.
Independent evaluator remains authoritative. No network/credential dependency.
"""
from pathlib import Path
import hashlib,json,os,signal,subprocess,time,shutil
KC='/Users/philippe/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli'
VERSION='jitx-record-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,data):
 p.parent.mkdir(parents=True,exist_ok=True);temp=p.with_name(p.name+'.tmp');temp.write_text(json.dumps(data,indent=2));temp.replace(p)
def command(args,cwd,out,label,timeout):
 start=time.monotonic();r={'phase':label,'argv':[str(x) for x in args],'started_at':time.time(),'timeout_seconds':timeout,'record_version':VERSION}
 r['invoked_python_sources_sha256']={str(x):sha(Path(x)) for x in args if str(x).endswith('.py') and Path(x).is_file()}
 with (out/(label+'.stdout')).open('w') as stdout,(out/(label+'.stderr')).open('w') as stderr:
  p=subprocess.Popen(args,cwd=cwd,stdout=stdout,stderr=stderr,start_new_session=True)
  r.update(pid=p.pid,state='running');last=0
  while p.poll() is None:
   if time.monotonic()-start>timeout:
    os.killpg(p.pid,signal.SIGKILL);p.wait();r.update(timed_out=True,state='timed_out');break
   if time.monotonic()-last>=5:
    r.update(heartbeat_at=time.time(),elapsed_seconds=time.monotonic()-start);write(out/(label+'.command.json'),r);last=time.monotonic()
   try:p.wait(timeout=1)
   except subprocess.TimeoutExpired:pass
  r.update(exit_code=p.returncode,finished_at=time.time(),heartbeat_at=time.time(),elapsed_seconds=time.monotonic()-start)
  if r['state']=='running':r['state']='completed' if p.returncode==0 else 'failed'
  write(out/(label+'.command.json'),r)
 return r

def publish(candidate,ledger,evaluation):
 board=candidate/'pcbgolf.kicad_pcb';digest=sha(board)
 if evaluation.get('artifacts',{}).get('pcbgolf.kicad_pcb')!=digest:raise ValueError('preview board differs from evaluated bytes')
 key=digest+'-'+hashlib.sha256(json.dumps(evaluation,sort_keys=True).encode()).hexdigest()[:12]
 dest=ledger/'previews'/key
 if (dest/'snapshot.json').exists():return json.loads((dest/'snapshot.json').read_text())
 dest.mkdir(parents=True,exist_ok=False)
 shutil.copy2(board,dest/board.name)
 write(dest/'evaluation.json',evaluation)
 reports={}
 for label in ['drc','erc','normalization','object-id-map']:
  source=candidate/(label+'.json')
  if source.exists():
   shutil.copy2(source,dest/source.name);reports[label]={'path':str(dest/source.name),'sha256':sha(dest/source.name)}
 args=[KC,'pcb','export','svg','--mode-single','--layers','F.Cu,B.Cu,F.SilkS,Edge.Cuts','--page-size-mode','2','--exclude-drawing-sheet','--output',str(dest/'board.svg'),str(dest/board.name)]
 r=command(args,candidate,dest,'render',60)
 if r['exit_code']!=0 or not (dest/'board.svg').exists():raise ValueError('actual board preview failed; no snapshot published')
 if sha(board)!=digest or sha(dest/board.name)!=digest:raise ValueError('board changed while rendering')
 provenance={p.name:sha(p) for p in Path(__file__).parent.glob('*.py')}
 record={'version':VERSION,'candidate':str(candidate),'board_sha256':digest,'preview_sha256':sha(dest/'board.svg'),'evaluation_sha256':sha(dest/'evaluation.json'),'preview':str(dest/'board.svg'),'board':str(dest/board.name),'record':str(dest/'evaluation.json'),'created_at':time.time(),'policy':evaluation.get('policy_version'),'evaluated':evaluation.get('evaluation_reliable') is True,'invariants_ok':evaluation.get('invariants_ok') is True,'valid':evaluation.get('valid') is True,'tools_sha256':provenance,'view_layers':['F.Cu','B.Cu','F.SilkS','Edge.Cuts'],'note':'Actual outer-copper SVG only; inner copper and unrouted airwires not shown. Completed capture, not engineering acceptance.'}
 record['reports']=reports
 inventory=subprocess.run(['/Users/philippe/dev/copper-scar-demo/.venv/bin/python',str(Path(__file__).with_name('copper_audit.py')),'--inventory',str(dest/board.name)],capture_output=True,text=True,check=True,timeout=60)
 write(ledger/'board-inventories'/(candidate.name+'.json'),json.loads(inventory.stdout))
 write(dest/'snapshot.json',record);return record
