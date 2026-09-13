"""Reproduce source-only geometry qualification; never starts placement/routing."""
from pathlib import Path
import argparse
import json
import os
import subprocess
import time
HERE=Path(__file__).resolve().parent

def reproduce(a):
    root=a.root.absolute();root.mkdir(parents=True,exist_ok=False);inv=root/'physical-inventories';inv.mkdir();logs=root/'commands';logs.mkdir();commands=[]
    def run(args,cwd=None):
        start=time.monotonic();env=dict(os.environ,PYTHONPATH=str(cwd or HERE))
        r=subprocess.run(list(map(str,args)),cwd=cwd,env=env,capture_output=True,text=True,timeout=180)
        i=len(commands);(logs/f'{i:02}.stdout').write_text(r.stdout);(logs/f'{i:02}.stderr').write_text(r.stderr)
        commands.append({'argv':list(map(str,args)),'cwd':str(cwd) if cwd else None,'returncode':r.returncode,'elapsed_s':time.monotonic()-start})
        (logs/'commands.json').write_text(json.dumps(commands,indent=2))
        if r.returncode:raise RuntimeError(f'Qualification command {i} failed; inspect {logs}')
    def census(board,name):run([a.kicad_python,HERE/'native_inventory.py',board,inv/name])
    census(a.parent/'pcbgolf.kicad_pcb','copperhead-native.json');census(a.jitx/'pcbgolf.kicad_pcb','jitx-native.json')
    for stage,corrected in [('before',False),('corrected',True)]:
        runtime=root/('probe-'+stage)
        run([a.audit_python,HERE/'prepare_geometry_probe.py','--root',runtime,'--source',a.source,'--assets',a.assets,'--inventory',inv/'copperhead-native.json',*(['--correct-mask'] if corrected else [])])
        cli=a.native_python.parent/'jitx';run([cli,'runtime','start','--project',runtime,'--bg'])
        run([cli,'design','build','original_interface.design.InterfaceQualification','--no-dependency-check'],runtime)
        run([a.native_python,HERE/'capture_geometry_probe.py',runtime,root/(stage+'-export')])
        run([a.audit_python,HERE/'normalize_probe_export.py',root/(stage+'-export')/'export',root/(stage+'-normalized')])
        census(root/(stage+'-normalized')/'original_interface.design.InterfaceQualification.kicad_pcb',stage+'-native-normalized.json')
        run([cli,'runtime','stop','--project',runtime])
    for label,source in [('copperhead',a.parent),('jitx',a.jitx),('probe-before',root/'before-normalized'),('probe-corrected',root/'corrected-normalized')]:
        run([a.audit_python,HERE/'check_project_copies.py',source,root/('drc-'+label+'-refilled')])
    run([a.audit_python,HERE/'qualify.py','--root',root,'--parent',a.parent,'--jitx',a.jitx,'--native-checkpoint',a.native_checkpoint,'--output',root/'final'])
    return root/'final/qualification.json'

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ('root','parent','jitx','source','assets','native-checkpoint','native-python','kicad-python','audit-python'):p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args()
    for key,value in vars(a).items():setattr(a,key,value.absolute())  # Preserve venv symlinks.
    print(reproduce(a))
