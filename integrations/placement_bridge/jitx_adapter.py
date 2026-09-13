"""Translate one fully qualified immutable request to fresh JITX IDs."""
from pathlib import Path
import argparse
import asyncio
import hashlib
import json
import subprocess
import sys
import fixture_control as native

HERE=Path(__file__).resolve().parent

def require(value,message):
    if not value:raise ValueError(message)

def mapping(messages, request):
    board=next(m['body'] for m in messages if m['type']=='board')
    require(board['stackup']['numlayers']==2, 'native layer count differs')
    groups=board['module']['groups'];require(len(groups)==8, 'native group count differs')
    current={};pad_to_ref={}
    for g in groups:
        require(len(g['instances'])==1,'unsupported compound native group')
        i=g['instances'][0];ref=i['designator'];require(ref not in current,'duplicate native reference')
        require(ref in request['inventory']['refs'],'unknown native reference')
        expected=request['inventory']['refs'][ref];x,y,angle=expected['pose']
        require(g['side']=='top' and g['pose']=={'center':{'x':x-139.5,'y':108-y},'angle':angle,'flipx':False},'native parent pose differs: '+ref)
        pads=[o for o in i['objects'] if 'pad' in o]
        require(len(pads)==1 and pads[0]['padref']=='p','native pad mapping differs')
        require(pads[0]['shapes']==[{'layers':[0],'shape':{'type':'polygon','elements':[{'x':.6,'y':.6},{'x':-.6,'y':.6},{'x':-.6,'y':-.6},{'x':.6,'y':-.6}]}}], 'native pad geometry differs')
        current[ref]={'group':g['id'],'instance':i['id'],'pad':pads[0]['pad']}
        pad_to_ref[pads[0]['pad']]=ref+'.p'
    require(set(current)==set(request['inventory']['refs']),'native ref scope differs')
    nets=next(m['body']['nets'] for m in messages if m['type']=='nets' and m['body'].get('complete'))
    membership={n['name']:sorted(pad_to_ref[p] for c in n['connected'] for p in c['pads'] if p in pad_to_ref) for n in nets}
    require(membership==request['net_memberships'],'native net membership differs')
    return current

def preflight(request_path, parent, checker_python, output):
    def validate(messages):
        # Validate against a fresh native export, not the request's saved parent copy.
        current=native.BASE/'designs'/native.DESIGN
        script="from contract import *; import sys; r=read(sys.argv[1]); validate_request(r,Path(sys.argv[2]),Path(sys.argv[3])); require(state_sha(pcb(Path(sys.argv[4])))==r['parent']['state_sha256'],'live native state differs from exact immutable parent'); require(sha(pcb(Path(sys.argv[4])).with_suffix('.kicad_pro'))==r['parent']['project_sha256'],'live rules differ')"
        # The controller's export lives in kicad; make only an outward snapshot.
        import shutil
        snapshot=output/'current-parent'
        shutil.copytree(current/'kicad',snapshot/'export')
        subprocess.run([str(checker_python),'-c',script,str(request_path),str(parent),str(native.BASE/'bridge_fixture/design.py'),str(snapshot)],
                       cwd=HERE,check=True,capture_output=True,text=True,timeout=30)
        request=json.loads(request_path.read_text())
        ids=mapping(messages,request)
        (output/'qualified-mapping.json').write_text(json.dumps(ids,indent=2))
        x,y,angle=request['target']['pose']
        # All transitions already exist in this qualified parent. Native reposition
        # re-realizes the two incident routes; adding duplicates would be incorrect.
        vias=next(m['body']['vias'] for m in messages if m['type']=='via-info')
        require(len(vias)==6,'qualified parent must have six existing transitions')
        return [{'type':'reposition','body':{'groups':[{'id':ids['TP4']['group'],
            'pose':{'center':{'x':x-139.5,'y':108-y},'angle':angle,'flipx':False},'side':'top'}]}}]
    return validate

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('request',type=Path);p.add_argument('output',type=Path)
    p.add_argument('--checker-python',type=Path,required=True);p.add_argument('--parent',type=Path,required=True);a=p.parse_args()
    a.output=a.output.resolve();a.request=a.request.resolve()
    if a.output.exists():
        p.error('Output already exists; use a new immutable attempt directory')
    try:
        asyncio.run(native.execute([],a.output,preflight(a.request,a.parent.resolve(),a.checker_python,a.output)))
    except Exception as e:
        # Reject before mutation or retain uncertainty marker after mutation. Never
        # infer cancellation from a request timeout and never retry automatically.
        state='completion_unknown' if (native.BASE/'.bridge-uncertain.json').exists() else 'rejected_before_mutation'
        a.output.mkdir(parents=True,exist_ok=True)
        (a.output/'failure.json').write_text(json.dumps({'state':state,'error_type':type(e).__name__,
            'message':str(e) if not isinstance(e,subprocess.CalledProcessError) else e.stderr[-2000:]},indent=2))
        raise
