"""Run local Freerouting with explicit controls and preserve native evidence."""
from pathlib import Path
import argparse,json,os,subprocess,time
ap=argparse.ArgumentParser();ap.add_argument('folder',type=Path);ap.add_argument('--seconds',type=int,default=300);ap.add_argument('--passes',type=int,default=10);a=ap.parse_args();f=a.folder.resolve()
cmd=['/private/tmp/copper-router/freerouting-mount/freerouting.app/Contents/MacOS/freerouting','--gui.enabled=false','--api_server.enabled=false','-da','--user_data_path='+str(f/'router-userdata'),'-de',str(f/'pcbgolf.dsn'),'-do',str(f/'pcbgolf.ses'),'-mp',str(a.passes),'-mt','1','-is','sequential','--router.fanout.enabled=false','--router.optimizer.enabled=false','--router.optimizer.max_threads=1','--router.job_timeout=00:%02d:%02d'%(a.seconds//60,a.seconds%60),'--router.strict_drc=true','--router.result_json='+str(f/'router-result.json')]
t=time.monotonic();result={'command':cmd}
with (f/'router.log').open('w') as log:
 try:
  r=subprocess.run(cmd,env={**os.environ,'JAVA_TOOL_OPTIONS':'-Djava.awt.headless=true -Xmx2g'},stdout=log,stderr=subprocess.STDOUT,timeout=a.seconds+20);result.update(returncode=r.returncode,timeout=False)
 except subprocess.TimeoutExpired:result.update(returncode=None,timeout=True)
result.update(elapsed_seconds=time.monotonic()-t,session_exists=(f/'pcbgolf.ses').exists());(f/'execution.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
