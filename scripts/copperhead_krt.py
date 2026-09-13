"""Run a pinned local KRT trial without lowering rules or rewriting support files."""
import argparse,hashlib,json,os,subprocess
from pathlib import Path
from copperhead_krt_rules import project_audit
root=Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser();ap.add_argument('candidate',type=Path);ap.add_argument('--net',required=True,action='append');a=ap.parse_args()
c=a.candidate.resolve();assert c.is_relative_to(root/'.local/copperhead/candidates')
t=root/'.local/copperhead/tools';repo=t/'KiCadRoutingTools'
provenance=json.loads((t/'krt-provenance.json').read_text())
for name,digest in provenance['files'].items():
    assert hashlib.sha256((repo/name).read_bytes()).hexdigest()==digest, 'KRT source drift: '+name
(c/'krt-provenance.json').write_text(json.dumps(provenance,indent=2))
artifacts=root/'.local/copperhead/runs'/c.name/'krt-output';artifacts.mkdir()
board=c/'pcbgolf.kicad_pcb';output=artifacts/'pcbgolf.kicad_pcb'
project=c/'pcbgolf.kicad_pro';original_project=project.read_bytes()
argv=[str(t/'krt-venv/bin/python'),'-u',str(repo/'py_router/route.py'),str(board),str(output),'--nets',*a.net,'--layers','F.Cu','In2.Cu','In3.Cu','B.Cu','--track-width','0.2','--via-size','0.6','--via-drill','0.3','--escalation','off','--strict-sizes','--fab-tier','standard','--no-fix-drc-settings','--no-stub-layer-swap','--max-iterations','200000','--max-ripup','0']
env=os.environ.copy();env['KICAD_CLI']='/Users/philippe/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli';env['KICAD_PYTHON']='/Users/philippe/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3.9'
env['KICAD_INRUN_FLOOR_SYNC']='0'
(c/'krt-invocation.json').write_text(json.dumps(dict(argv=argv,environment={k:env[k] for k in ['KICAD_CLI','KICAD_PYTHON','KICAD_INRUN_FLOOR_SYNC']},qualification='Diagnostic routing trial only; independent original-rule DRC required'),indent=2))
result=subprocess.run(argv,cwd=repo,env=env)
producer_project=output.with_suffix('.kicad_pro')
audit=project_audit(original_project,producer_project.read_bytes()) if producer_project.exists() else dict(producer_project_written=False,producer_rule_preservation='not demonstrated',authoritative_rules='original project bytes only')
audit['input_project_changed_by_producer']=project.read_bytes()!=original_project
if audit['input_project_changed_by_producer']:
    (artifacts/'producer-mutated-input.kicad_pro').write_bytes(project.read_bytes())
project.write_bytes(original_project)
(artifacts/'project-rule-audit.json').write_text(json.dumps(audit,indent=2))
assert project.read_bytes()==original_project
if result.returncode:raise SystemExit(result.returncode)
assert output.is_file(),'KRT returned without an output board'
# Keep producer output intact and copy its bytes to the candidate for evaluation.
board.write_bytes(output.read_bytes())
