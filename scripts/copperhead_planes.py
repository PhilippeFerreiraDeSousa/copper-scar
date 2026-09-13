"""Add continuous inner ground zones to a fresh four-layer routing experiment."""
from pathlib import Path
import argparse,shutil,json
import pcbnew as p
ap=argparse.ArgumentParser();ap.add_argument('source',type=Path);ap.add_argument('destination',type=Path);a=ap.parse_args();shutil.copytree(a.source,a.destination);b=p.LoadBoard(str(a.destination/'pcbgolf.kicad_pcb'))
net=b.FindNet('GND');assert net
for layer in [p.In1_Cu,p.In2_Cu]:
 z=p.ZONE(b);z.SetLayer(layer);z.SetNetCode(net.GetNetCode());z.SetLocalClearance(p.FromMM(.2));z.SetThermalReliefGap(p.FromMM(.3));z.SetThermalReliefSpokeWidth(p.FromMM(.3));z.SetPadConnection(p.ZONE_CONNECTION_FULL)
 poly=z.Outline();poly.NewOutline()
 for xy in [(100.5,50.5),(239.5,50.5),(239.5,154.5),(100.5,154.5)]:poly.Append(p.FromMM(xy[0]),p.FromMM(xy[1]))
 b.Add(z)
p.SaveBoard(str(a.destination/'pcbgolf.kicad_pcb'),b)
(a.destination/'plane-assumptions.json').write_text(json.dumps(dict(layers=['In1.Cu','In2.Cu'],net='GND',copper_edge_margin_mm=.5,clearance_mm=.2,qualification='Routing experiment; actual dielectric/copper stackup and plane connectivity pending native fill/check'),indent=2))
