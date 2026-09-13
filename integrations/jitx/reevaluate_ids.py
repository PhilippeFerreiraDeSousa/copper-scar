from pathlib import Path
import json,subprocess,sys,shutil,time
from feasibility import evaluate
from observability import write
B=Path('/Users/philippe/dev/copper-scar-jitx');L=B/'runs/stage1';H=Path(__file__).parent.resolve();parser='/Users/philippe/dev/copper-scar-demo/.venv/bin/python'
previous=json.loads((L/'best-feasibility.json').read_text());write(L/'best-feasibility-before-object-id-gate.json',previous)
write(L/'policy-v2-object-id-invalidation.json',{'time':time.time(),'finding':'Raw JITX exported duplicate object UUIDs across footprints and copper; report object identities unreliable. Policyv3 requires unique IDs and fresh checks. Prior counts not assumed wrong, reevaluation determines differences. Geometry and electrical connectivity are not edited.'})
for old in ['stage1-baseline-v4','stage1-routed-001-v2','stage1-routed-002-v2','stage1-moved-004','stage1-moved-routed-005','iteration-006-jlc-four-layer','iteration-008-group-floorplan-input','iteration-008-group-floorplan-placed','iteration-008-group-floorplan-routed']:
 src=B/'candidates'/old;out=B/'candidates'/(old+'-ids-v3');normal=json.loads((src/'normalization.json').read_text())
 subprocess.run([parser,str(H/'roundtrip.py'),normal['source'],str(out)],check=True,stdout=subprocess.DEVNULL)
 subprocess.run([parser,str(H/'copper_audit.py'),str(src/'pcbgolf.kicad_pcb'),str(out/'pcbgolf.kicad_pcb'),str(out/'metadata-only-copper-audit.json')],check=True,stdout=subprocess.DEVNULL)
 audit=json.loads((out/'metadata-only-copper-audit.json').read_text());assert audit['totals']['removed']==audit['totals']['added']==0 and not audit['moved_refs']
 r=evaluate(out,L,'Metadata-only unique-object-ID reevaluation of '+old+'; geometry and copper proven unchanged. Original action: '+json.loads((src/'evaluation.json').read_text())['action'])
 inv=subprocess.check_output([parser,str(H/'copper_audit.py'),'--inventory',str(out/'pcbgolf.kicad_pcb')],text=True);write(L/'board-inventories'/(out.name+'.json'),json.loads(inv))
 print(old,r['metrics'],'retained',r['retain'],flush=True)
