"""Reproduce the fixture bridge in a new directory; never restore managed state."""
from pathlib import Path
import argparse
import json
import os
import shutil
import subprocess
import time

HERE=Path(__file__).resolve().parent
DESIGN='bridge_fixture.design.BridgeProof'

def reproduce(root,native_python,checker_python):
    root=root.resolve();root.mkdir(parents=True,exist_ok=False)
    rt=root/'runtime';rt.mkdir()
    (rt/'pyproject.toml').write_text('[project]\nname="placement-bridge-proof"\nversion="0.1.0"\nrequires-python=">=3.12"\ndependencies=["jitx==4.4.0","jitxlib-standard==4.4.0"]\n')
    shutil.copytree(HERE/'incremental_fixture',rt/'bridge_fixture',ignore=shutil.ignore_patterns('__pycache__'))
    source=rt/'bridge_fixture/design.py'
    source.write_text(source.read_text().replace('class IncrementalProof(Design):','class BridgeProof(Design):'))
    logs=root/'commands';logs.mkdir();commands=[]
    def run(args,expected=0):
        started=time.monotonic()
        env=dict(os.environ,PYTHONPATH=str(rt))
        r=subprocess.run(list(map(str,args)),cwd=rt,env=env,capture_output=True,text=True,timeout=360)
        index=len(commands);(logs/f'{index:02}.stdout').write_text(r.stdout);(logs/f'{index:02}.stderr').write_text(r.stderr)
        commands.append({'argv':list(map(str,args)),'returncode':r.returncode,'elapsed_s':time.monotonic()-started})
        (logs/'commands.json').write_text(json.dumps(commands,indent=2))
        if (expected==0 and r.returncode!=0) or (expected!=0 and r.returncode==0):
            raise RuntimeError(f'Unexpected command result {index}; see {logs}')
    jitx=native_python.parent/'jitx'
    run([jitx,'runtime','start','--project',rt,'--bg'])
    run([jitx,'design','build',DESIGN,'--no-dependency-check'])
    def control(plan,stage):
        file=root/(stage+'-plan.json');file.write_text(json.dumps(plan,indent=2))
        run([native_python,HERE/'fixture_control.py',file,root/stage])
    control([],'00-built')
    messages=json.loads((root/'00-built/final.json').read_text())
    b=next(m['body'] for m in messages if m['type']=='board');hold=[];plan=[]
    for g in sorted(b['module']['groups'],key=lambda g:g['instances'][0]['designator']):
        i=g['instances'][0];pad=next(o['pad'] for o in i['objects'] if 'pad'in o);c=g['pose']['center']
        if i['designator'] in ('TP1','TP2'):hold.append(pad)
        else:plan.append({'type':'via-add','body':{'origin':pad,'layer':0,'instance':i['id'],
            'global-point':{'x':c['x']+(-2 if c['x']>0 else 2),'y':c['y']},'force-place':False,'def-name':'Proof through via 0.60-0.30'}})
    control([{'type':'route','body':{'layer':0,'pads':hold,'force':False,'configure':None}}]+plan,'01-escapes')
    m=json.loads((root/'01-escapes/final.json').read_text());vias=next(x['body']['vias'] for x in m if x['type']=='via-info')
    control([{'type':'route','body':{'layer':1,'pads':sorted(vias),'force':False,'configure':None}}],'02-parent')
    parent=root/'02-parent';candidate=root/'03-moved';request=root/'request-qualified.json'
    common=['--parent',parent,'--source',source,'--request',request]
    run([checker_python,HERE/'copperhead.py','emit',*common,'--output',root/'unused'])
    def adapter(req,out,expected=0):
        run([native_python,HERE/'jitx_adapter.py',req,out,'--parent',parent,'--checker-python',checker_python],expected)
    for name in ('stale','mapping'):
        r=json.loads(request.read_text())
        if name=='stale':r['parent']['board_sha256']='0'*64
        else:r['inventory']['refs']['TP4']['pads'][0]['net']='HOLD'
        rejected=root/(name+'-qualified.json');rejected.write_text(json.dumps(r,indent=2))
        rejected_output=root/('reject-'+name+'-qualified')
        adapter(rejected,rejected_output,1)
        failure=json.loads((rejected_output/'failure.json').read_text())
        reason='stale parent board' if name=='stale' else 'invalid reference/pad/geometry mapping'
        if failure['state']!='rejected_before_mutation' or reason not in failure['message'] or list(rejected_output.glob('action-*')):
            raise RuntimeError('Negative contract check did not fail at the intended pre-mutation gate')
    adapter(request,candidate)
    run([checker_python,HERE/'result.py',*common,'--candidate',candidate,'--output',root/'sealed'])
    run([checker_python,HERE/'copperhead.py','consume',*common,'--candidate',candidate,'--result',root/'sealed/result.json','--output',root/'consumer'])
    # Only this project/runtime is stopped, and only after a confirmed completion.
    run([jitx,'runtime','stop','--project',rt])
    return root/'consumer/decision.json'

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('new_root',type=Path)
    p.add_argument('--native-python',type=Path,required=True);p.add_argument('--checker-python',type=Path,required=True)
    a=p.parse_args();print(reproduce(a.new_root,a.native_python.absolute(),a.checker_python.absolute()))
