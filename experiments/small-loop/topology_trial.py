"""Explicit placement plus net-attached through-via proposal before full routing."""
from pathlib import Path
import json,sys
import pcbnew as p
folder=Path(sys.argv[1]).resolve();b=p.LoadBoard(str(folder/'pcbgolf.kicad_pcb'))
refs={f.GetReference():f for f in b.GetFootprints()};r=refs['R90'];before=[p.ToMM(r.GetPosition().x),p.ToMM(r.GetPosition().y)];r.Move(p.VECTOR2I(p.FromMM(-1),0))
pad=next(v for v in r.Pads() if v.GetNumber()=='1');pos=pad.GetPosition();target=p.VECTOR2I(pos.x-p.FromMM(1.5),pos.y)
via=p.PCB_VIA(b);via.SetPosition(target);via.SetWidth(p.FromMM(.6));via.SetDrill(p.FromMM(.3));via.SetViaType(p.VIATYPE_THROUGH);via.SetLayerPair(p.F_Cu,p.B_Cu);via.SetNetCode(pad.GetNetCode());b.Add(via)
for start,end,layer in [(pos,target,p.F_Cu),(target,p.VECTOR2I(target.x-p.FromMM(1),target.y),p.B_Cu)]:
 t=p.PCB_TRACK(b);t.SetStart(start);t.SetEnd(end);t.SetWidth(p.FromMM(.2));t.SetLayer(layer);t.SetNetCode(pad.GetNetCode());b.Add(t)
p.SaveBoard(str(folder/'pcbgolf.kicad_pcb'),b)
proposal={'kind':'placement_and_explicit_layer_transition','component':'R90','before_mm':before,'after_mm':[p.ToMM(r.GetPosition().x),p.ToMM(r.GetPosition().y)],'rationale':'Move the resistor west by1mm and provide its drain-side pad with explicit bottom-layer access toward the separated Q2 pad group. Test this local access hypothesis with complete routing; do not assume the authored via is needed.','authored_via':{'net':pad.GetNetname(),'x':p.ToMM(target.x),'y':p.ToMM(target.y),'diameter':.6,'drill':.3,'layers':['F.Cu','B.Cu']},'attachment':{'pad':'R90.1','front_track_width':.2,'back_access_stub_mm':1},'known_solution_used':False}
(folder/'topology-proposal.json').write_text(json.dumps(proposal,indent=2))
