"""One diagnosed group placement followed by a complete routing/evaluation budget."""
import argparse,collections,hashlib,importlib.util,json,shutil,subprocess,time
from pathlib import Path
HERE=Path(__file__).parent
spec=importlib.util.spec_from_file_location('spacious',HERE/'campaign.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
ap=argparse.ArgumentParser();ap.add_argument('root',type=Path);ap.add_argument('--seconds',type=int,default=600);a=ap.parse_args();root=a.root.resolve()
out=root/'outer-group-route';out.mkdir();start=time.monotonic()
pre=root/'outer-group-preflight';old=root/'spacious-baseline-r2/reimport-exact';folder=out/'project'
before=json.loads((pre/'before/evaluation.json').read_text());incumbent=json.loads((old/'result.json').read_text());old_eval=json.loads((old/'after/evaluation.json').read_text())
def keys(e):return collections.Counter(m.signature(v) for v in e['violations'] if v['type']!='unconnected_items')
assert before['invariants_ok'] and not (keys(before)-keys(old_eval)),'New native preflight findings'
assert before['unconnected']==499,'Unexpected changed input connectivity'
m.s.copy_project(pre/'input',folder)
m.write(out/'source.json',dict(commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=m.ROOT,text=True).strip(),sources={str(p.relative_to(m.ROOT)):m.sha(p) for p in HERE.glob('*.py')},proposal=str(root/'outer-group-order-proposal.json'),proposal_sha256=m.sha(root/'outer-group-order-proposal.json'),native_preflight_board_sha256=m.sha(pre/'input/pcbgolf.kicad_pcb'),retained_before=incumbent,route_budget_seconds=a.seconds,started_at=m.s.now()))
m.write(out/'status.json',dict(status='routing',before_missing=140,proposal='whole-functional-group reorder',started_at=m.s.now()))
m.run([m.s.KIPY,HERE/'native.py','export',folder],out,'export')
m.run([m.s.PYTHON,m.ROOT/'scripts/copperhead_effective_options.py',folder,'--phase','export'],out,'effective-vias')
route=m.run([m.s.PYTHON,m.ROOT/'scripts/copperhead_route.py',folder,'--seconds',a.seconds,'--passes',100,'--whole-board','--skip-fanout'],out,'route',a.seconds+50)
m.run([m.s.KIPY,HERE/'native.py','import',folder],out,'import')
after=m.evaluate(folder,out,'after')
pre_audit=json.loads((pre/'before-audit.json').read_text());post_audit=json.loads((out/'after-audit.json').read_text());old_audit=json.loads((old/'after-audit.json').read_text())
identical=pre_audit['identity']==post_audit['identity'] and pre_audit['poses']==post_audit['poses']
groups=[set(g['pads']) for g in post_audit['pad_groups']]
splits=[g for g in old_audit['pad_groups'] if len(g['pads'])>1 and not any(set(g['pads'])<=v for v in groups)]
legal=all((v['diameter'],v['drill']) in [(.45,.2),(.6,.3)] and v['layers']==['F.Cu','B.Cu'] for v in post_audit['vias'])
added=keys(after)-keys(old_eval)
retained=identical and after['invariants_ok'] and not added and not splits and legal and after['unconnected']<incumbent['after_missing']
native_valid=bool(identical and legal and after['invariants_ok'] and after['erc_ok'] and after['unconnected']==0 and after['errors']==0 and after['manufacturing_rules_clear'] and not any(v['type']=='footprint_symbol_mismatch' for v in after['violations']))
result=dict(status='completed',primitive='functional_group_reorder',retained=retained,incumbent_before_missing=incumbent['after_missing'],attempted_missing=after['unconnected'],retained_after_missing=after['unconnected'] if retained else incumbent['after_missing'],errors=after['errors'],warnings_including_parity=after['warnings'],invariants_ok=after['invariants_ok'],exact_pose_identity_preserved=identical,via_definitions_legal=legal,via_count=len(post_audit['vias']),restoration_split_groups=splits,added_findings=[dict(signature=str(k),count=v) for k,v in added.items()],missing_by_net=m.s.missing_by_net(after),route_elapsed_seconds=route['elapsed_seconds'],elapsed_seconds=time.monotonic()-start,board=str(folder/'pcbgolf.kicad_pcb'),board_sha256=m.sha(folder/'pcbgolf.kicad_pcb'),stage1_native_valid=native_valid,stage1_stop=native_valid,stage2_handoff=native_valid,official_score=None,qualification='Whole-board realization after group-placement update. Previously connected groups from the retained140-open result must all be restored. Immutable original footprint errors remain unwaived; no official score without assembly qualification.')
m.write(out/'result.json',result);m.write(out/'status.json',result)
m.run([m.s.KICAD,'pcb','export','svg','--layers','F.Cu,B.Cu,Edge.Cuts','--mode-single','--page-size-mode','2','-o',out/'board.svg',folder/'pcbgolf.kicad_pcb'],out,'visual')
print(json.dumps(result,indent=2))
