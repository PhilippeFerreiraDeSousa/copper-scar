"""Run local Freerouting with explicit controls and preserve native evidence."""
from pathlib import Path
import argparse,json,os,subprocess,time
ap=argparse.ArgumentParser();ap.add_argument('folder',type=Path);ap.add_argument('--seconds',type=int,default=300);ap.add_argument('--passes',type=int,default=10);ap.add_argument('--whole-board',action='store_true');ap.add_argument('--skip-fanout',action='store_true');a=ap.parse_args();f=a.folder.resolve()
cmd=['/private/tmp/copper-router/freerouting-mount/freerouting.app/Contents/MacOS/freerouting','--gui.enabled=false','--api_server.enabled=false','-da','--user_data_path='+str(f/'router-userdata'),'-de',str(f/'pcbgolf.dsn'),'-do',str(f/'pcbgolf.ses'),'-mp',str(a.passes),'-mt','1','-is','sequential','--router.fanout.enabled='+str(a.whole_board and not a.skip_fanout).lower(),'--router.optimizer.enabled=false','--router.optimizer.max_threads=1','--router.job_timeout=00:%02d:%02d'%(a.seconds//60,a.seconds%60),'--router.strict_drc=true','--router.result_json='+str(f/'router-result.json')]
t=time.monotonic();result={'command':cmd,'scope':'whole_board' if a.whole_board else 'legacy_whole_board','net_filter':None,'fanout_enabled':a.whole_board and not a.skip_fanout,'via_count_limit':None,'optimization_enabled':False,'effort_limit_seconds':a.seconds,'pass_limit':a.passes}
with (f/'router.log').open('w') as log:
 try:
  r=subprocess.run(cmd,env={**os.environ,'JAVA_TOOL_OPTIONS':'-Djava.awt.headless=true -Xmx2g'},stdout=log,stderr=subprocess.STDOUT,timeout=a.seconds+20);result.update(returncode=r.returncode,timeout=False)
 except subprocess.TimeoutExpired:result.update(returncode=None,timeout=True)
result.update(elapsed_seconds=time.monotonic()-t,session_exists=(f/'pcbgolf.ses').exists());(f/'execution.json').write_text(json.dumps(result,indent=2));
from copperhead_route_evidence import evidence
result['coverage']=evidence(f);(f/'routing-coverage.json').write_text(json.dumps(result['coverage'],indent=2));(f/'execution.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
if result['timeout']:raise SystemExit(124)
if result['returncode']!=0:raise SystemExit(result['returncode'] or 1)
if not result['session_exists']:raise SystemExit('Backend returned without an importable session')
