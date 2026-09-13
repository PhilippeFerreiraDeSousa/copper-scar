"""Track-local native outline/layer and SES bridge; no rule relaxation."""
import argparse,json,shutil
from pathlib import Path
import pcbnew as p

def snap(b):return {f.GetReference():{'uuid':f.m_Uuid.AsString(),'x':f.GetPosition().x,'y':f.GetPosition().y,'angle':f.GetOrientationDegrees(),'pads':sorted((q.GetNumber(),q.m_Uuid.AsString(),q.GetNetname()) for q in f.Pads())} for f in b.GetFootprints()}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('action',choices=['prepare','import']);ap.add_argument('folder',type=Path);ap.add_argument('--layers',type=int,default=4);a=ap.parse_args();path=a.folder/'pcbgolf.kicad_pcb';b=p.LoadBoard(str(path));before=snap(b)
 if a.action=='prepare':
  b.SetCopperLayerCount(a.layers)
  enabled=b.GetEnabledLayers(); enabled.AddLayer(p.In1_Cu);enabled.AddLayer(p.In2_Cu);b.SetEnabledLayers(enabled)
  # Generous routing envelope around existing placement; mechanical review outstanding.
  bounds=(108,48,196,127)
  for x,y,xx,yy in [(108,48,196,48),(196,48,196,127),(196,127,108,127),(108,127,108,48)]:
   q=p.PCB_SHAPE();q.SetShape(p.SHAPE_T_SEGMENT);q.SetLayer(p.Edge_Cuts);q.SetStart(p.VECTOR2I(p.FromMM(x),p.FromMM(y)));q.SetEnd(p.VECTOR2I(p.FromMM(xx),p.FromMM(yy)));q.SetWidth(p.FromMM(.05));b.Add(q)
  assert before==snap(b)
  p.SaveBoard(str(path),b);assert p.ExportSpecctraDSN(b,str(a.folder/'pcbgolf.dsn'))
  result=dict(action=a.action,outline_mm=bounds,copper_layers=a.layers,placement_preserved=True,manufacturing_stackup='provisional, not qualified',critical_routes='not yet established')
 else:
  assert p.ImportSpecctraSES(b,str(a.folder/'pcbgolf.ses'))
  # SES quantization must not displace original footprint anchors.
  adjustments=[]
  for f in b.GetFootprints():
   v=before[f.GetReference()]
   if (f.GetPosition().x,f.GetPosition().y)!=(v['x'],v['y']):
    adjustments.append(dict(ref=f.GetReference(),dx=f.GetPosition().x-v['x'],dy=f.GetPosition().y-v['y']))
    f.SetPosition(p.VECTOR2I(v['x'],v['y']))
  assert before==snap(b)
  p.SaveBoard(str(path),b)
  result=dict(action=a.action,anchor_restoration_nm=adjustments,pin_uuid_net_identity_preserved=True,segments=sum(not isinstance(t,p.PCB_VIA) for t in b.GetTracks()),vias=sum(isinstance(t,p.PCB_VIA) for t in b.GetTracks()))
 (a.folder/(a.action+'-native.json')).write_text(json.dumps(result,indent=2));print(json.dumps(result))
if __name__=='__main__':main()
