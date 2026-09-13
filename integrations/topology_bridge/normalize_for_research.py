"""Native reserialization of an external parser copy, with semantic readback."""
import json
import sys
import pcbnew as k
source,target=sys.argv[1:]
def signature(b):
    return {'footprints':sorted((f.GetReference(),f.GetPosition().x,f.GetPosition().y,f.GetOrientationDegrees(),sorted((p.GetNumber(),p.GetNetname(),p.GetPosition().x,p.GetPosition().y,p.GetSize().x,p.GetSize().y,p.GetLayerSet().FmtBin()) for p in f.Pads())) for f in b.GetFootprints()),'tracks':sorted((t.GetClass(),t.GetNetname(),t.GetLayer(),t.GetStart().x,t.GetStart().y,t.GetEnd().x,t.GetEnd().y,t.GetWidth(t.GetLayer()) if isinstance(t,k.PCB_VIA) else t.GetWidth()) for t in b.GetTracks()),'zones':b.GetAreaCount()}
b=k.LoadBoard(source);before=signature(b);k.SaveBoard(target,b);after=signature(k.LoadBoard(target));assert before==after
print(json.dumps({'native_readback_geometry_and_nets_equal':True,'source':source,'parser_copy':target}))
