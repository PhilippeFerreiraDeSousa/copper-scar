"""Run one NEW diagnostic reduction with runtime cleanup and exact command log."""
import json
from pathlib import Path
import subprocess
import sys
HERE=Path(__file__).absolute().parent
root=Path(sys.argv[1]).absolute();refs=sys.argv[2];mode=sys.argv[3] if len(sys.argv)>3 else 'none'
cli='/Users/philippe/dev/copper-scar-jitx/.venv/bin/jitx';native='/Users/philippe/dev/copper-scar-jitx/.venv/bin/python';calls=[]
def call(args,**kwargs):
    calls.append({'args':list(map(str,args)),'cwd':str(kwargs.get('cwd',Path.cwd()))})
    return subprocess.run(list(map(str,args)),check=True,**kwargs)
if refs.startswith('pad:'):
    call([sys.executable,HERE/'prepare_single_pad.py',root,refs.removeprefix('pad:')])
else:
    call([sys.executable,HERE/'prepare_capture_reduction.py',root,refs,*sys.argv[4:]])
rt=root/'runtime'
call([cli,'runtime','start','--project',rt,'--bg'])
try:
    with (root/'run.stdout').open('w') as out,(root/'run.stderr').open('w') as err:
        call([native,HERE/'isolate_original_capture.py',mode],cwd=rt,env={**__import__('os').environ,'PYTHONPATH':'.'},stdout=out,stderr=err,timeout=150)
finally:
    call([cli,'runtime','stop','--project',rt]);(root/'commands.json').write_text(json.dumps(calls,indent=2))
print((root/'evidence/result.json').read_text())
