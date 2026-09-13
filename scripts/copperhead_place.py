"""Conservative block-floorplan experiment; preserves parts/pads and all rules.

This is placement assistance, not electrical layout qualification. Parts are
assigned to schematic-local IC blocks; physical collision avoidance precedes
routing. Critical power/pair geometry still requires explicit closure.
"""
from pathlib import Path
import argparse,json,math,shutil
import pcbnew as p
ap=argparse.ArgumentParser();ap.add_argument('source',type=Path);ap.add_argument('destination',type=Path);a=ap.parse_args();shutil.copytree(a.source,a.destination);b=p.LoadBoard(str(a.destination/'pcbgolf.kicad_pcb'));fps={f.GetReference():f for f in b.GetFootprints()}
spos=json.loads(Path('.local/copperhead/runs/schematic-positions.json').read_text())
anchors={'U3':(135,105),'U4':(175,105),'U1':(207,100),'U2':(207,120),'J1':(216,78),'J2':(130,134),'J3':(178,141),'J4':(109,90),'BH1':(105,55),'BH2':(220,55),'BH3':(105,145),'BH4':(220,145)}
for i in range(4):
 x=125+24*i
 anchors['J'+str(i+5)]=(x,59)
 anchors['U'+str(i+5)]=(x,72)
 anchors['U'+str(i+9)]=(x,81)
 anchors['U'+str(i+13)]=(x,87.5)
# Model/body envelope uses all non-text footprint graphics and pad geometry.
boxes={};placed={};groups={};moves=[]
for ref,f in fps.items():
 box=f.GetBoundingBox(False,False);pos=f.GetPosition()
 boxes[ref]=(p.ToMM(box.GetX()-pos.x)-.6,p.ToMM(box.GetY()-pos.y)-.6,p.ToMM(box.GetRight()-pos.x)+.6,p.ToMM(box.GetBottom()-pos.y)+.6)

def rect(ref,xy):
 x,y=xy;u=boxes[ref];return (x+u[0],y+u[1],x+u[2],y+u[3])
def valid(ref,xy):
 q=rect(ref,xy)
 if q[0]<102 or q[1]<52 or q[2]>238 or q[3]>153:return False
 for r,z in placed.items():
  v=rect(r,z)
  if q[0]<v[2] and q[2]>v[0] and q[1]<v[3] and q[3]>v[1]:return False
 return True
for ref,xy in anchors.items():
 if not valid(ref,xy):raise RuntimeError('Anchor collision '+ref)
 placed[ref]=xy
# Proximity on the unchanged schematic is only a grouping heuristic, recorded.
for ref in fps:
 if ref in anchors:continue
 src=spos[ref];opts=[r for r in anchors if r.startswith('U') and spos.get(r,{}).get('sheet')==src['sheet']]
 groups[ref]=min(opts,key=lambda r:sum((spos[r]['xy'][i]-src['xy'][i])**2 for i in (0,1))) if opts else 'U3'
# Place larger support parts first to preserve local space; then fill with passives.
for ref in sorted(groups,key=lambda r:-(boxes[r][2]-boxes[r][0])*(boxes[r][3]-boxes[r][1])):
 center=anchors[groups[ref]];found=None
 for radius in range(2,101):
  options=[]
  for step in range(max(12,radius*4)):
   angle=2*math.pi*step/max(12,radius*4)
   xy=(round((center[0]+radius*.5*math.cos(angle))*4)/4,round((center[1]+radius*.5*math.sin(angle))*4)/4)
   if valid(ref,xy):options.append(xy)
  if options:
   found=min(options,key=lambda z:(z[0]-center[0])**2+(z[1]-center[1])**2);break
 if found is None:raise RuntimeError('No collision-free placement '+ref)
 placed[ref]=found
for ref,xy in placed.items():
 f=fps[ref];old=f.GetPosition();f.SetPosition(p.VECTOR2I(p.FromMM(xy[0]),p.FromMM(xy[1])));moves.append(dict(ref=ref,from_mm=[p.ToMM(old.x),p.ToMM(old.y)],to_mm=xy,block=groups.get(ref,ref)))
for d in list(b.GetDrawings()):
 if d.GetLayer()==p.Edge_Cuts:b.Remove(d)
for x,y,xx,yy in [(100,50,240,50),(240,50,240,155),(240,155,100,155),(100,155,100,50)]:
 q=p.PCB_SHAPE();q.SetShape(p.SHAPE_T_SEGMENT);q.SetLayer(p.Edge_Cuts);q.SetStart(p.VECTOR2I(p.FromMM(x),p.FromMM(y)));q.SetEnd(p.VECTOR2I(p.FromMM(xx),p.FromMM(yy)));q.SetWidth(p.FromMM(.05));b.Add(q)
p.SaveBoard(str(a.destination/'pcbgolf.kicad_pcb'),b);assert p.ExportSpecctraDSN(b,str(a.destination/'pcbgolf.dsn'))
(a.destination/'placement.json').write_text(json.dumps(dict(outline_mm=[100,50,240,155],moves=moves,body_margin_mm=.6,method='schematic-local IC grouping plus collision-free ring placement',qualification='EXPERIMENTAL: electrical geometry and connector access not yet qualified'),indent=2));print('Placed',len(placed),'footprints; exported DSN')
