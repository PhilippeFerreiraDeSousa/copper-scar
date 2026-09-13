"""Original-full adapter: shared lifecycle, existing full-project native pipeline."""
import argparse,hashlib,importlib.util,json,subprocess,sys,threading,time
from pathlib import Path
HERE=Path(__file__).parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'experiments/pcb-loop'))
from executor import execute_candidate
spec=importlib.util.spec_from_file_location('full_pipeline',HERE/'campaign.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def backend(request,folder,emit):
    out=Path(request['prepared_trial']);argv=[m.s.PYTHON,str(HERE/'run_uniform_trial.py'),str(out),'--seconds',str(request['route_budget']['seconds'])]
    record=dict(argv=argv,started_at=m.s.now(),script_sha256=m.sha(HERE/'run_uniform_trial.py'),frozen_source_bundle=request['source_file_sha256'])
    stop=threading.Event()
    def pulse():
        while not stop.is_set():
            phase=json.loads((out/'status.json').read_text()) if (out/'status.json').exists() else {'status':'preparing'}
            emit('full-board native pipeline',candidate_status=phase);stop.wait(2)
    thread=threading.Thread(target=pulse,daemon=True);thread.start()
    try:
        with (folder/'native-pipeline.stdout').open('w') as stdout,(folder/'native-pipeline.stderr').open('w') as stderr:
            proc=subprocess.run(argv,cwd=ROOT,stdout=stdout,stderr=stderr,timeout=request['route_budget']['seconds']+180)
        record.update(returncode=proc.returncode,finished_at=m.s.now());m.write(folder/'pipeline-command.json',record)
        if proc.returncode:raise RuntimeError('Full native pipeline failed; see preserved command logs')
    finally:stop.set();thread.join()
    result=json.loads((out/'result.json').read_text());e=json.loads((out/'after/evaluation.json').read_text());raw=json.loads((out/'after/drc.json').read_text());ref=json.loads((out/'routed/reference-check.json').read_text())
    checks={
        'full_schematic_partition':(ref['pin_partition_equivalent'] and ref['whole_project_erc_coverage'],out/'routed/reference-check.json'),
        'original_rules':(ref['original_board_rules_preserved'] and ref['original_netclasses_preserved'] and e['invariants_ok'],out/'after/evaluation.json'),
        'all_pad_identity':(ref['all_physical_pad_uuid_identity_preserved'] and result['exact_pose_identity_preserved'],out/'result.json'),
        'physical':(not any(v['severity']=='error' for v in raw['violations']),out/'after/drc.json'),
        'connectivity':(not raw['unconnected_items'],out/'after/drc.json'),
        'parity':(not raw['schematic_parity'],out/'after/drc.json'),
        'erc':(e['erc_ok'],out/'after/evaluation.json'),
        'manufacturing':(e['manufacturing_rules_clear'],out/'after/evaluation.json'),
        'legal_vias':(result['via_definitions_legal'],out/'after-audit.json'),
        'initial_groups_preserved':(not result['initial_connected_group_splits'],out/'result.json'),
    }
    # The source-bound six-layer input and native identity gates preserve layers.
    import sexpdata as sx
    tree=sx.loads((out/'routed/pcbgolf.kicad_pcb').read_text());layers=[v[1] for v in m.nodes(tree,'layers')[0][1:] if str(v[1]).endswith('.Cu')]
    checks['layers']=(layers==request['eligible_layers'],out/'after-audit.json')
    original=sx.loads((out/'input/pcbgolf.kicad_pcb').read_text())
    footprint_map=lambda t:{m.ref(fp):fp for fp in m.nodes(t,'footprint')}
    old_fp,new_fp=footprint_map(original),footprint_map(tree)
    exact_geometry=old_fp==new_fp and len(new_fp)==245
    m.write(folder/'whole-footprint-geometry.json',dict(exact_whole_footprints=exact_geometry,input_sha256=m.sha(out/'input/pcbgolf.kicad_pcb'),output_sha256=m.sha(out/'routed/pcbgolf.kicad_pcb'),changed_refs=sorted(r for r in old_fp.keys()|new_fp.keys() if old_fp.get(r)!=new_fp.get(r))))
    checks['whole_footprint_geometry']=(exact_geometry,folder/'whole-footprint-geometry.json')
    return dict(gates={k:dict(passed=bool(value),report=str(report)) for k,(value,report) in checks.items()},diagnostics=dict(result=result,raw_native=e,nested_command_receipts=[str(p) for p in out.glob('*.command.json')],assembly_qualification='not established; official score unavailable'),official_score=None,official_score_qualified=False,diagnostic_retained=result['strict_incumbent_replacement'],commands=[record])

def main():
    ap=argparse.ArgumentParser();ap.add_argument('folder',type=Path);ap.add_argument('--seconds',type=int,default=600);a=ap.parse_args();out=a.folder.resolve();scale=json.loads((out/'input/uniform-scale.json').read_text());control=out.parent/'prior-floorplan-control/result.json'
    sources=list(HERE.glob('*.py'))+[ROOT/'experiments/pcb-loop/executor.py']+list((ROOT/'copper_scar/tools/copperhead').glob('*.py'))+list((ROOT/'scripts').glob('copperhead_*.py'))+list((ROOT/'scripts/native').glob('Copperhead*.java'))+[ROOT/'copper_scar/real.py',out/'input/pcbgolf.kicad_pcb',out/'input/uniform-scale.json',out/'input/hierarchy-conversion.json',out/'input/routing-options.json',out/'before/evaluation.json',out/'before-audit.json',control]
    sources += [out/'input'/name for name in m.s.support(out/'input')]
    request=dict(size_family='original-full',stage=1,source_epoch='raw-original-footprints-uniform-position-scale-v1',source_sha=m.sha(out/'input/pcbgolf.kicad_pcb'),required_gates=['full_schematic_partition','original_rules','all_pad_identity','physical','connectivity','parity','erc','manufacturing','legal_vias','initial_groups_preserved','layers'],eligible_layers=['F.Cu','In1.Cu','In2.Cu','In3.Cu','In4.Cu','B.Cu'],via_options=[[.6,.3],[.45,.2]],route_budget=dict(seconds=a.seconds,passes=100,threads=1),action=dict(primitive='uniform_position_and_outline_scale',scale=scale['scale'],center_nm=scale['center_nm'],rationale='User-requested exact uniform spacing test at matched complete-board budget',expected_score_terms=dict(official_score=None,area_scale=float(__import__('fractions').Fraction(scale['scale']))**2,via_delta='measured after routing',copper_layer_delta=0,part_geometry_delta=0)),source_files=sorted(set(map(str,sources))),incumbent=dict(valid=False,official_score=None,folder=str(control.parent/'routed')),prepared_trial=str(out))
    request['required_gates'].append('whole_footprint_geometry')
    result=execute_candidate(request,backend,out/'shared-executor');print(json.dumps({k:result[k] for k in ['valid','failed_gates','diagnostic_retained','stop_stage_one','official_score']}))
if __name__=='__main__':main()
