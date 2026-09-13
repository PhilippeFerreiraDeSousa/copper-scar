"""Bounded GND escape proposal, admitted only after independent native DRC.

Places ordinary through vias outside pad bounds, never blind vias or via-in-pad.
Bounding-box/segment screening is conservative; native DRC remains authoritative.
"""
import argparse,json,math
from pathlib import Path
import pcbnew as p
ap=argparse.ArgumentParser();ap.add_argument('candidate',type=Path);ap.add_argument('report',type=Path);ap.add_argument('--limit',type=int,default=20);a=ap.parse_args();b=p.LoadBoard(str(a.candidate/'pcbgolf.kicad_pcb'));d=json.loads(a.report.read_text())
targets={i['uuid'] for v in d['unconnected_items'] for i in v['items'] if '[GND]' in i['description'] and 'pad ' in i['description'].lower()}
pads=[q for f in b.GetFootprints() for q in f.Pads()];tracks=list(b.GetTracks());point=lambda q:(p.ToMM(q.x),p.ToMM(q.y))
def distance(pt,u,v):
 dx=v[0]-u[0];dy=v[1]-u[1];z=dx*dx+dy*dy;t=max(0,min(1,((pt[0]-u[0])*dx+(pt[1]-u[1])*dy)/z)) if z else 0
 return math.hypot(pt[0]-u[0]-t*dx,pt[1]-u[1]-t*dy)
def bbox(q):
 z=q.GetBoundingBox();return tuple(p.ToMM(v) for v in (z.GetX(),z.GetY(),z.GetRight(),z.GetBottom()))
boxes=[(q,bbox(q)) for q in pads]
def rectdist(pt,r):return math.hypot(max(r[0]-pt[0],0,pt[0]-r[2]),max(r[1]-pt[1],0,pt[1]-r[3]))
def safe(center,start,own):
 # Extra 0.01 mm buffer accounts for export quantization and geometric screening.
 for q,r in boxes:
  if rectdist(center,r)<.51:return False  # no via in any component pad
  if q is not own and q.GetNetname()!='GND':
   for step in range(11):
    pt=(start[0]+(center[0]-start[0])*step/10,start[1]+(center[1]-start[1])*step/10)
    if rectdist(pt,r)<.31:return False
 for t in tracks:
  if t.GetNetname()=='GND':continue
  u=point(t.GetStart());v=point(t.GetEnd());rad=p.ToMM(t.GetWidth())/2
  if distance(center,u,v)<.51+rad:return False
  if t.IsOnLayer(p.F_Cu):
   if any(distance((start[0]+(center[0]-start[0])*i/10,start[1]+(center[1]-start[1])*i/10),u,v)<.31+rad for i in range(11)):return False
 return True
added=[];skipped=[]
for q in pads:
 if q.m_Uuid.AsString() not in targets or q.GetNetname()!='GND' or not q.IsOnLayer(p.F_Cu):continue
 if len(added)>=a.limit:break
 start=point(q.GetPosition());selected=None
 for radius in [.9,1.2,1.5,2,2.5,3]:
  for i in range(16):
   xy=(round(start[0]+radius*math.cos(i*math.pi/8),4),round(start[1]+radius*math.sin(i*math.pi/8),4))
   if safe(xy,start,q):selected=xy;break
  if selected:break
 if not selected:skipped.append(q.m_Uuid.AsString());continue
 via=p.PCB_VIA(b);via.SetPosition(p.VECTOR2I(p.FromMM(selected[0]),p.FromMM(selected[1])));via.SetWidth(p.FromMM(.6));via.SetDrill(p.FromMM(.3));via.SetViaType(p.VIATYPE_THROUGH);via.SetLayerPair(p.F_Cu,p.B_Cu);via.SetNetCode(q.GetNetCode());b.Add(via)
 track=p.PCB_TRACK(b);track.SetStart(q.GetPosition());track.SetEnd(via.GetPosition());track.SetLayer(p.F_Cu);track.SetWidth(p.FromMM(.2));track.SetNetCode(q.GetNetCode());b.Add(track);tracks.extend([via,track]);added.append(dict(pad_uuid=q.m_Uuid.AsString(),ref=q.GetParentFootprint().GetReference(),pad=q.GetNumber(),via_mm=selected,trace_width_mm=.2,via_diameter_mm=.6,drill_mm=.3))
p.SaveBoard(str(a.candidate/'pcbgolf.kicad_pcb'),b);(a.candidate/'ground-escape.json').write_text(json.dumps(dict(added=added,skipped=skipped,policy='Experimental GND-only escapes outside all component pads; independent DRC required'),indent=2));print('Added',len(added),'GND escape proposals')
