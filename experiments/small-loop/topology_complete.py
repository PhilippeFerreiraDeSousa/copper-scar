"""Revise failed one-ended access proposal to explicitly join two access sites."""
from pathlib import Path
import sys,json,pcbnew as p
f=Path(sys.argv[1]).resolve();b=p.LoadBoard(str(f/'pcbgolf.kicad_pcb'));q=next(fp for fp in b.GetFootprints() if fp.GetReference()=='Q2');pad=next(x for x in q.Pads() if x.GetNumber()=='5');end=p.VECTOR2I(pad.GetPosition().x-p.FromMM(1.5),pad.GetPosition().y);via=p.PCB_VIA(b);via.SetPosition(end);via.SetWidth(p.FromMM(.6));via.SetDrill(p.FromMM(.3));via.SetViaType(p.VIATYPE_THROUGH);via.SetLayerPair(p.F_Cu,p.B_Cu);via.SetNetCode(pad.GetNetCode());b.Add(via)
proposal=json.loads((f/'topology-proposal.json').read_text());v=proposal['authored_via'];start=p.VECTOR2I(p.FromMM(v['x']-1),p.FromMM(v['y']));bend=p.VECTOR2I(end.x,start.y)
for a,z,layer in [(pad.GetPosition(),end,p.F_Cu),(start,bend,p.B_Cu),(bend,end,p.B_Cu)]:
 if a==z:continue
 t=p.PCB_TRACK(b);t.SetStart(a);t.SetEnd(z);t.SetWidth(p.FromMM(.2));t.SetLayer(layer);t.SetNetCode(pad.GetNetCode());b.Add(t)
p.SaveBoard(str(f/'pcbgolf.kicad_pcb'),b);proposal.update(revision='two-ended-access',second_via={'net':pad.GetNetname(),'x':p.ToMM(end.x),'y':p.ToMM(end.y),'diameter':.6,'drill':.3},rationale='The previous fully routed result bypassed the one-ended bottom stub and left it dangling. Explicitly join drain-side access sites on B.Cu before full-board routing. This is authored topology, not claimed discovered routing or evidence placement was needed.');(f/'topology-proposal.json').write_text(json.dumps(proposal,indent=2))
