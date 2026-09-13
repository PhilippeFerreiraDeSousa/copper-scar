"""Native bridge for isolated small-circuit experiments; never changes rules."""
from pathlib import Path
import argparse,json,hashlib
import pcbnew as p
ap=argparse.ArgumentParser();ap.add_argument('action',choices=['export','import','audit']);ap.add_argument('folder',type=Path);a=ap.parse_args();f=a.folder.resolve();path=f/'pcbgolf.kicad_pcb';manager=p.SETTINGS_MANAGER();manager.LoadProject(str(f/'pcbgolf.kicad_pro'));b=p.LoadBoard(str(path));b.SetProject(manager.GetProject(str(f/'pcbgolf.kicad_pro')))
def identity():return {fp.GetReference():{'pose':[fp.GetPosition().x,fp.GetPosition().y,fp.GetOrientationDegrees()],'pads':sorted((pad.GetNumber(),pad.GetNetname()) for pad in fp.Pads())} for fp in b.GetFootprints()}
before=identity()
if a.action=='export':
 # Repair only the original undersized LED polarity marking, preserving electrical land pattern.
 for fp in b.GetFootprints():
  for item in fp.GraphicalItems():
   if isinstance(item,p.PCB_TEXT) and item.GetLayer() in (p.F_SilkS,p.B_SilkS):
    item.SetTextThickness(max(item.GetTextThickness(),p.FromMM(.08)))
    sz=item.GetTextSize();item.SetTextSize(p.VECTOR2I(max(sz.x,p.FromMM(.8)),max(sz.y,p.FromMM(.8))))
 p.SaveBoard(str(path),b);assert p.ExportSpecctraDSN(b,str(f/'pcbgolf.dsn'))
if a.action=='import':
 assert p.ImportSpecctraSES(b,str(f/'pcbgolf.ses'))
 for fp in b.GetFootprints():
  pos=before[fp.GetReference()]['pose'];fp.SetPosition(p.VECTOR2I(pos[0],pos[1]))
 assert before==identity(),'SES changed placement or electrical identity'
 p.SaveBoard(str(path),b)
if a.action=='audit':
 con=b.GetConnectivity();con.Build(b);con.RecalculateRatsnest();groups=[];seen=set()
 for fp in b.GetFootprints():
  for pad in fp.Pads():
   if not pad.GetNumber():continue
   key=pad.m_Uuid.AsString()
   if key in seen:continue
   ps=[x for x in con.GetConnectedItems(pad) if isinstance(x,p.PAD)];ps.append(pad)
   seen.update(x.m_Uuid.AsString() for x in ps)
   groups.append({'net':pad.GetNetname(),'pads':sorted(set(x.GetParentFootprint().GetReference()+'.'+x.GetNumber() for x in ps))})
 result={'identity':identity(),'groups':groups,'native_open_count':con.GetUnconnectedCount(False),'track_widths_mm':sorted(set(p.ToMM(t.GetWidth()) for t in b.GetTracks() if not isinstance(t,p.PCB_VIA))),'wire_length_mm':sum(p.ToMM(t.GetLength()) for t in b.GetTracks() if not isinstance(t,p.PCB_VIA)),'vias':[{'uuid':t.m_Uuid.AsString(),'layers':[t.TopLayer(),t.BottomLayer()],'layer_names':[b.GetLayerName(t.TopLayer()),b.GetLayerName(t.BottomLayer())],'net':t.GetNetname(),'x':p.ToMM(t.GetPosition().x),'y':p.ToMM(t.GetPosition().y),'drill':p.ToMM(t.GetDrillValue()),'diameter':p.ToMM(t.GetWidth(p.F_Cu))} for t in b.GetTracks() if isinstance(t,p.PCB_VIA)],'copper_layers':b.GetCopperLayerCount(),'board_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
 (f/'native-audit.json').write_text(json.dumps(result,indent=2))
