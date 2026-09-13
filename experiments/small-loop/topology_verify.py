"""Check authored via identities and layer participation in saved native output."""
from pathlib import Path
import sys,json,hashlib
import sexpdata as sx
from audit import nodes,first
f=Path(sys.argv[1]);proposal=json.loads((f/'topology-proposal.json').read_text());d=sx.loads((f/'pcbgolf.kicad_pcb').read_text());vs=nodes(d,'via');segments=nodes(d,'segment');expected=[proposal['authored_via']]+([proposal['second_via']] if 'second_via' in proposal else []);checks=[]
for v in expected:
 matches=[q for q in vs if abs(first(q,'at')[1]-v['x'])<1e-6 and abs(first(q,'at')[2]-v['y'])<1e-6];assert len(matches)==1
 q=matches[0];assert first(q,'net')[1]==v['net'];layers=set()
 for t in segments:
  if first(t,'net')[1]!=v['net']:continue
  if any(abs(first(t,k)[1]-v['x'])<1e-6 and abs(first(t,k)[2]-v['y'])<1e-6 for k in ['start','end']):layers.add(first(t,'layer')[1])
 assert first(q,'size')[1]==v['diameter'] and first(q,'drill')[1]==v['drill']
 checks.append({'net':v['net'],'x':v['x'],'y':v['y'],'preserved':True,'attached_layers':sorted(layers),'used_on_both_layers':layers=={'F.Cu','B.Cu'}})
r={'authored_vias':checks,'net_identity_preserved':True,'all_authored_transitions_realized':json.loads((f/'acceptance.json').read_text())['accepted'] and all(v['used_on_both_layers'] for v in checks),'board_sha256':hashlib.sha256((f/'pcbgolf.kicad_pcb').read_bytes()).hexdigest()};(f/'topology-verification.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
