"""Full-budget realization of one verified uniform-position input."""
import argparse,collections,importlib.util,json,subprocess,time
from pathlib import Path
HERE=Path(__file__).parent
spec=importlib.util.spec_from_file_location('spacious',HERE/'campaign.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
ap=argparse.ArgumentParser();ap.add_argument('folder',type=Path);ap.add_argument('--seconds',type=int,default=600);a=ap.parse_args();out=a.folder.resolve();start=time.monotonic()
before=json.loads((out/'before/evaluation.json').read_text());pre=json.loads((out/'before-audit.json').read_text());scale=json.loads((out/'input/uniform-scale.json').read_text());control=out.parent/'prior-floorplan-control';control_result=json.loads((control/'result.json').read_text());control_eval=json.loads((control/'before/evaluation.json').read_text())
def findings(e):return collections.Counter(m.signature(v) for v in e['violations'] if v['type']!='unconnected_items')
assert before['invariants_ok'] and before['unconnected']==control_eval['unconnected'] and not (findings(before)-findings(control_eval))
assert scale['part_count']==245 and scale['maximum_transform_residual_nm']<=1 and scale['physical_footprint_geometry_preserved'] and scale['rotations_and_sides_preserved']
folder=out/'routed';m.s.copy_project(out/'input',folder)
m.write(out/'source.json',dict(commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=m.ROOT,text=True).strip(),sources={str(p.relative_to(m.ROOT)):m.sha(p) for p in HERE.glob('*.py')},input_sha256=m.sha(out/'input/pcbgolf.kicad_pcb'),manifest_sha256=m.sha(out/'input/uniform-scale.json'),control_receipt_sha256=m.sha(control/'result.json'),route_seconds=a.seconds,started_at=m.s.now()))
m.write(out/'status.json',dict(status='routing',primitive='uniform_position_and_outline_scale',scale=scale['scale'],initial_missing=before['unconnected'],started_at=m.s.now()))
m.run([m.s.KIPY,HERE/'native.py','export',folder],out,'export')
m.run([m.s.PYTHON,m.ROOT/'scripts/copperhead_effective_options.py',folder,'--phase','export'],out,'effective-vias')
route=m.run([m.s.PYTHON,m.ROOT/'scripts/copperhead_route.py',folder,'--seconds',a.seconds,'--passes',100,'--whole-board','--skip-fanout'],out,'route',a.seconds+50)
m.run([m.s.KIPY,HERE/'native.py','import',folder],out,'import');after=m.evaluate(folder,out,'after');post=json.loads((out/'after-audit.json').read_text())
identical=pre['identity']==post['identity'] and pre['poses']==post['poses'];groups=[set(g['pads']) for g in post['pad_groups']]
split=lambda rows:[g for g in rows if len(g['pads'])>1 and not any(set(g['pads'])<=z for z in groups)]
initial_splits=split(pre['pad_groups']);control_splits=split(json.loads((control/'after-audit.json').read_text())['pad_groups'])
legal=all((v['diameter'],v['drill']) in [(.45,.2),(.6,.3)] and v['layers']==['F.Cu','B.Cu'] for v in post['vias']);added=findings(after)-findings(before)
qualified=after['invariants_ok'] and identical and legal and not added and not initial_splits
raw=json.loads((out/'after/drc.json').read_text());native_valid=bool(qualified and after['erc_ok'] and after['unconnected']==0 and after['errors']==0 and after['manufacturing_rules_clear'] and not raw['schematic_parity'])
result=dict(status='completed',primitive='uniform_position_and_outline_scale',scale=scale['scale'],center_nm=scale['center_nm'],outline_mm=scale['after_outline_mm'],part_count=245,initial_missing=before['unconnected'],missing=after['unconnected'],physical_errors=after['errors'],warnings_including_parity=after['warnings'],invariants_ok=after['invariants_ok'],exact_pose_identity_preserved=identical,initial_connected_group_splits=initial_splits,added_findings=[dict(signature=str(k),count=v) for k,v in added.items()],via_definitions_legal=legal,via_count=len(post['vias']),qualified_comparison_result=bool(qualified),control_missing=control_result['after']['unconnected'],missing_delta_vs_control=after['unconnected']-control_result['after']['unconnected'],via_delta_vs_control=len(post['vias'])-control_result['via_count'],control_connected_group_splits=control_splits,strict_incumbent_replacement=bool(qualified and not control_splits and after['unconnected']<control_result['after']['unconnected']),missing_by_net=m.s.missing_by_net(after),route_elapsed_seconds=route['elapsed_seconds'],elapsed_seconds=time.monotonic()-start,board=str(folder/'pcbgolf.kicad_pcb'),board_sha256=m.sha(folder/'pcbgolf.kicad_pcb'),stage1_native_valid=native_valid,stage1_stop=native_valid,stage2_handoff=native_valid,official_score=None,qualification='Independent fresh no-copper input and full-board realization matched to prior control. Only anchors and outline scaled uniformly; footprint geometry not scaled. Native51inheritederrorfloor unwaived. Comparison metric and strict retained-incumbent replacement are separate.')
m.write(out/'result.json',result);m.write(out/'status.json',result)
m.run([m.s.KICAD,'pcb','export','svg','--layers','F.Cu,B.Cu,Edge.Cuts','--mode-single','--page-size-mode','2','-o',out/'routed.svg',folder/'pcbgolf.kicad_pcb'],out,'visual')
print(json.dumps({k:v for k,v in result.items() if k not in ['control_connected_group_splits','missing_by_net']},indent=2))
