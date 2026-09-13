"""Native spacious initialization; footprint shapes and electrical identity stay fixed."""
import argparse, collections, hashlib, json, math
from pathlib import Path
import pcbnew as p

ap=argparse.ArgumentParser()
ap.add_argument('action',choices=['prepare','export','import','audit'])
ap.add_argument('folder',type=Path)
ap.add_argument('--groups',type=Path)
ap.add_argument('--mode',choices=['spacious','original','compact'],default='spacious')
ap.add_argument('--gap',type=float,default=3)
a=ap.parse_args(); folder=a.folder; path=folder/'pcbgolf.kicad_pcb'
project=folder/'pcbgolf.kicad_pro'; project_bytes=project.read_bytes()
manager=p.SETTINGS_MANAGER();manager.LoadProject(str(project))
b=p.LoadBoard(str(path));b.SetProject(manager.GetProject(str(project)))
fs={f.GetReference():f for f in b.GetFootprints()}
def pos(f):return [p.ToMM(f.GetPosition().x),p.ToMM(f.GetPosition().y),f.GetOrientationDegrees()]
def identity():
 return {r:dict(uuid=f.m_Uuid.AsString(),pads=sorted((q.m_Uuid.AsString(),q.GetNumber(),q.GetNetname(),q.GetSize().x,q.GetSize().y,q.GetDrillSize().x,q.GetDrillSize().y,str(q.GetShape()),q.GetLayerSet().FmtHex()) for q in f.Pads())) for r,f in fs.items()}
def bounds(f):
 z=f.GetBoundingBox(False,False)
 return [p.ToMM(z.GetX()),p.ToMM(z.GetY()),p.ToMM(z.GetRight()),p.ToMM(z.GetBottom())]
def save():
 p.SaveBoard(str(path),b)
 # KiCad may serialize settings as a side effect; retain exact frozen support.
 project.write_bytes(project_bytes)
before=identity();poses={r:pos(f) for r,f in fs.items()}
if a.action=='prepare':
 assert len(fs)==245 and len(list(b.GetTracks()))==0 and len(list(b.Zones()))==0
 b.SetCopperLayerCount(6)
 enabled=b.GetEnabledLayers()
 for layer in [p.F_Cu,p.In1_Cu,p.In2_Cu,p.In3_Cu,p.In4_Cu,p.B_Cu]:enabled.AddLayer(layer)
 b.SetEnabledLayers(enabled)
 groups=json.loads(a.groups.read_text());flat=[r for rs in groups.values() for r in rs]
 assert len(flat)==245 and set(flat)==set(fs)
 records=[]
 if a.mode!='original':
  # Package-aware shelf cells adapt the demo grids. Original angles are retained.
  # Functional group membership is fixed; within each group preserve spatial order.
  gx,gy=25.,25.;rowh=0.;group_gap=8.;column=0
  for name,refs in groups.items():
   if name.startswith('mechanical_'):continue
   refs=sorted(refs,key=lambda r:(round(poses[r][1]/5),poses[r][0],r))
   cols=max(2,math.ceil(math.sqrt(len(refs))))
   x,y=0.,0.;h=0.;extent=0.;local=[]
   for i,r in enumerate(refs):
    if i and i%cols==0:x=0.;y+=h;h=0.
    z=bounds(fs[r]);w=max(6.,z[2]-z[0]+a.gap);hh=max(5.,z[3]-z[1]+a.gap)
    xy=[gx+x+a.gap/2-z[0]+poses[r][0],gy+y+a.gap/2-z[1]+poses[r][1]]
    fs[r].SetPosition(p.VECTOR2I(p.FromMM(xy[0]),p.FromMM(xy[1])))
    local.append(dict(ref=r,envelope_before_mm=z,cell_size_mm=[w,hh]))
    x+=w;extent=max(extent,x);h=max(h,hh)
   height=y+h;records.append(dict(group=name,refs=refs,origin_mm=[gx,gy],size_mm=[extent,height],cells=local))
   gx+=extent+group_gap;rowh=max(rowh,height);column+=1
   if column==3:gx=25.;gy+=rowh+group_gap;rowh=0.;column=0
  zs=[bounds(f) for r,f in fs.items() if not r.startswith('BH')]
  outline=[15.,15.,math.ceil(max(z[2] for z in zs)+10),math.ceil(max(z[3] for z in zs)+10)]
  for r,xy in zip(['BH1','BH2','BH3','BH4'],[(19,19),(outline[2]-4,19),(outline[2]-4,outline[3]-4),(19,outline[3]-4)]):fs[r].SetPosition(p.VECTOR2I(p.FromMM(xy[0]),p.FromMM(xy[1])))
 else:
  zs=[bounds(f) for f in fs.values()]
  outline=[math.floor(min(z[0] for z in zs)-10),math.floor(min(z[1] for z in zs)-10),math.ceil(max(z[2] for z in zs)+10),math.ceil(max(z[3] for z in zs)+10)]
 for d in list(b.GetDrawings()):
  if d.GetLayer()==p.Edge_Cuts:b.Delete(d)
 corners=[(outline[0],outline[1]),(outline[2],outline[1]),(outline[2],outline[3]),(outline[0],outline[3])]
 for i,start in enumerate(corners):
  d=p.PCB_SHAPE();d.SetShape(p.SHAPE_T_SEGMENT);d.SetLayer(p.Edge_Cuts);d.SetWidth(p.FromMM(.05));d.SetStart(p.VECTOR2I(p.FromMM(start[0]),p.FromMM(start[1])));end=corners[(i+1)%4];d.SetEnd(p.VECTOR2I(p.FromMM(end[0]),p.FromMM(end[1])));b.Add(d)
 assert before==identity()
 save()
 result=dict(mode=a.mode,gap_mm=a.gap,groups=records,outline_mm=outline,copper_layers=6,original_copper_layers=2,layer_choice='Same six-layer capacity as prior full-board campaign; explicit feasibility design choice, no stackup qualification',moves=[dict(ref=r,before=poses[r],after=pos(fs[r])) for r in sorted(fs)],identity=before,qualification='Full original electrical design. Positions changed, footprints not scaled; schematic groups are not engineering signoff. No copper or nets removed from original un-routed input.')
 (folder/'initialization.json').write_text(json.dumps(result,indent=2))
elif a.action=='export':
 assert p.ExportSpecctraDSN(b,str(folder/'pcbgolf.dsn'))
elif a.action=='import':
 assert p.ImportSpecctraSES(b,str(folder/'pcbgolf.ses'))
 for r,f in fs.items():
  x,y,angle=poses[r];f.SetPosition(p.VECTOR2I(p.FromMM(x),p.FromMM(y)));f.SetOrientationDegrees(angle)
 assert before==identity()
 save()
else:
 con=b.GetConnectivity();con.Build(b);con.RecalculateRatsnest();groups=[];seen=set()
 for f in fs.values():
  for pad in f.Pads():
   key=pad.m_Uuid.AsString()
   if key in seen or not pad.GetNumber():continue
   ps=[x for x in con.GetConnectedItems(pad) if isinstance(x,p.PAD)]+[pad]
   seen.update(x.m_Uuid.AsString() for x in ps)
   groups.append(dict(net=pad.GetNetname(),pads=sorted(set(x.m_Uuid.AsString() for x in ps))))
 vias=[dict(uuid=t.m_Uuid.AsString(),net=t.GetNetname(),x=p.ToMM(t.GetPosition().x),y=p.ToMM(t.GetPosition().y),diameter=p.ToMM(t.GetWidth(p.F_Cu)),drill=p.ToMM(t.GetDrillValue()),layers=[b.GetLayerName(t.TopLayer()),b.GetLayerName(t.BottomLayer())]) for t in b.GetTracks() if isinstance(t,p.PCB_VIA)]
 result=dict(identity=identity(),poses={r:pos(f) for r,f in fs.items()},pad_groups=groups,vias=vias,track_widths=sorted(set(p.ToMM(t.GetWidth()) for t in b.GetTracks() if not isinstance(t,p.PCB_VIA))),board_sha256=hashlib.sha256(path.read_bytes()).hexdigest())
 (folder/'native-audit.json').write_text(json.dumps(result,indent=2))
assert project.read_bytes()==project_bytes
