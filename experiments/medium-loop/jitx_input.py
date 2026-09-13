"""Create an isolated JITX import/build from the native medium-loop input."""
from pathlib import Path
import argparse,json,os,shutil,subprocess
ap=argparse.ArgumentParser();ap.add_argument('input',type=Path);ap.add_argument('project',type=Path);ap.add_argument('--jitx',type=Path,default=Path('/Users/philippe/dev/copper-scar-jitx/.venv/bin/jitx'));a=ap.parse_args();p=a.project.resolve();p.mkdir(parents=True,exist_ok=False);package=p/'medium_loop';package.mkdir();(package/'__init__.py').touch();templates=Path(__file__).parent/'jitx';shutil.copy2(templates/'pyproject.toml',p/'pyproject.toml');shutil.copy2(templates/'design.py',package/'design.py')
def run(args,label):
 r=subprocess.run([str(a.jitx),*map(str,args)],cwd=p,env={**os.environ,'PYTHONPATH':str(p)},capture_output=True,text=True);(p/(label+'.log')).write_text(r.stdout+r.stderr);assert r.returncode==0,(label,r.returncode);return r.stdout
result=run(['project','import','kicad',a.input.resolve(),'--output',p],'import');assert json.loads(result)['success'],'Importer returned failure despite exit0'
run(['runtime','start','--project',p,'--bg'],'runtime');result=run(['design','build','medium_loop.design.MediumLoopInput','--no-dependency-check'],'build');assert 'status: ok' in result
(p/'input-contract.json').write_text(json.dumps({'size_family':'medium-loop','native_input':str(a.input.resolve()),'design':'medium_loop.design.MediumLoopInput','constraints':'Effective0.20mm width/clearance and0.60/0.30mmvia restored explicitly; native constraints remain authority','scope':'Input import/build only; no routed round-trip equivalence claim'},indent=2));print(p)
