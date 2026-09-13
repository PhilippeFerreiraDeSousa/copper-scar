"""Copperhead-side fixed proposal emission and independently checked consumption."""
import argparse
from pathlib import Path
from contract import *
from verify_incremental_fixture import check, EXPECTED

def emit(parent, source, output):
    inv = inventory(pcb(parent)); qualify(inv)
    request={'schema':'copperhead-jitx-fixture-pose-v1','comparison_kind':'synthetic_fixture_bridge',
             'parent':{'board_sha256':sha(pcb(parent)), 'state_sha256':state_sha(pcb(parent)), 'project_sha256':sha(pcb(parent).with_suffix('.kicad_pro')),
                       'source_sha256':sha(source)}, 'inventory':inv, 'frame':FRAME, 'fixed_refs':FIXED,
             'target':{'ref':'TP4','pose':[149.5,100.0,0.0],'side':'F.Cu'},
             'net_memberships':{n:[r+'.p' for r in sorted(rs)] for n,rs in EXPECTED.items()},
             'copper_policy':{'preserve_exactly':['CROSS_B','CROSS_C','HOLD'],'may_change':['CROSS_A']},
             'intent':'Fixed correspondence-qualified exchange proof; no placement-quality claim'}
    validate_request(request,parent,source)
    write(output,request)
    return request

def evaluate(request_path, parent, candidate, source, output):
    request=read(request_path);validate_request(request,parent,source)
    # Fresh external copies: consumer never trusts producer summaries or rewrites them.
    import shutil
    output=Path(output);output.mkdir(parents=True,exist_ok=False)
    before=check_copy(parent,output/'parent')
    after=check_copy(candidate,output/'candidate')
    actual=inventory(pcb(candidate));expected=read(request_path)['inventory']
    expected['refs']['TP4']['pose']=request['target']['pose']
    require(actual==expected,'undeclared pose, pad, outline or stack change')
    require(sha(pcb(parent).with_suffix('.kicad_pro')) == sha(pcb(candidate).with_suffix('.kicad_pro')), 'rules changed')
    preserved={n:before['copper_by_net'][n]==after['copper_by_net'][n] for n in request['copper_policy']['preserve_exactly']}
    topology=coverage(pcb(candidate))
    clean=lambda s:s['opens']==0 and s['violations']==[] and s['via_count']==6
    retain=clean(before) and clean(after) and all(preserved.values()) and all(n['realized'] for n in topology.values())
    result={'request_sha256':sha(request_path),'parent_sha256':sha(pcb(parent)), 'output_sha256':sha(pcb(candidate)),
            'decision':'retain_fixture' if retain else 'reject_fixture', 'whole_product_board_qualified':False,
            'independent_whole_fixture_drc':{'opens':after['opens'],'violations':after['violations'],'runs':2},
            'per_net_realization':topology,'unrelated_copper_preserved':preserved,
            'actual_pose_delta':{'TP4':{'before':before['poses']['TP4'],'after':after['poses']['TP4']}},
            'actual_changed_copper_nets':[n for n in EXPECTED if before['copper_by_net'][n]!=after['copper_by_net'][n]],
            'via_count':after['via_count']}
    write(output/'evaluation.json',result)
    return result

def check_copy(stage,dest):
    import shutil
    shutil.copytree(Path(stage)/'export',dest/'export')
    return check(dest)

def consume(request_path, result_path, parent, candidate, source, output):
    claimed=read(result_path)
    require(claimed['schema']=='copperhead-jitx-fixture-result-v1','unsupported result schema')
    for name,value in claimed['artifact_sha256'].items():
        path=(Path(candidate)/name).resolve()
        require(path.is_relative_to(Path(candidate).resolve()),'artifact escapes candidate')
        require(sha(path)==value,'changed producer artifact: '+name)
    require(claimed['termination']==read(Path(candidate)/'completion.json'),'completion evidence differs')
    require(claimed['request_sha256']==sha(request_path),'wrong result request hash')
    require(claimed['parent_sha256']==sha(pcb(parent)),'wrong result parent hash')
    require(claimed['output_sha256']==sha(pcb(candidate)),'wrong result board hash')
    require(claimed['termination']['export_barrier'] is True and claimed['termination']['native_worker_state']=='completed', 'native completion unknown')
    result=evaluate(request_path,parent,candidate,source,output)
    for key in ('per_net_realization','actual_pose_delta','actual_changed_copper_nets','unrelated_copper_preserved'):
        require(result[key]==claimed[key], 'producer/consumer disagreement: '+key)
    result['result_sha256']=sha(result_path)
    write(Path(output)/'decision.json',result)
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('command',choices=['emit','evaluate','consume'])
    p.add_argument('--request',type=Path,required=True);p.add_argument('--parent',type=Path,required=True)
    p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--candidate',type=Path);p.add_argument('--result',type=Path)
    a=p.parse_args()
    if a.command=='emit':r=emit(a.parent,a.source,a.request)
    elif a.command=='evaluate':r=evaluate(a.request,a.parent,a.candidate,a.source,a.output)
    else:r=consume(a.request,a.result,a.parent,a.candidate,a.source,a.output)
    print(json.dumps(r,indent=2))
