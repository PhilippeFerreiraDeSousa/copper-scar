"""Independent KiCad-file graph comparison after native JITX export."""
from import_experiments import *
from collections import defaultdict,Counter
import xml.etree.ElementTree as ET
export_path=BASE/'designs/pcbgolf_import.current.PcbgolfFull/kicad/pcbgolf_import.current.PcbgolfFull.kicad_pcb'
nc={(x.attrib['ref'],x.attrib['pin']) for x in ET.parse(RUN/'hierarchy-netlist.xml').getroot().findall('./nets/net/node') if 'no_connect' in x.attrib.get('pintype','')}
def inventory(p):
 d=parse(p);groups=defaultdict(set);pads=set();refs=set();count=0
 for fp in children(d,'footprint'):
  prs=children(fp,'property');ref=next((x[2] for x in prs if x[1]=='Reference'),None)
  if ref is None:ref=next(x[2] for x in children(fp,'fp_text') if str(x[1])=='reference')
  refs.add(ref)
  for pad in children(fp,'pad'):
   if not str(pad[1]):continue
   count+=1;ep=(ref,str(pad[1]));pads.add(ep)
   ns=children(pad,'net')
   if ns and ns[0][1]!=0 and ep not in nc:groups[str(ns[0][-1])].add(ep)
 return refs,pads,{frozenset(v):n for n,v in groups.items()},count
r,p,g,c=inventory(SRC/'pcbgolf.kicad_pcb');rr,pp,gg,cc=inventory(export_path)
drc=json.loads((RUN/'jitx-export-drc.json').read_text())
result=dict(footprints=len(rr),named_physical_pad_instances=cc,original_named_physical_pad_instances=c,missing_refs=sorted(r-rr),extra_refs=sorted(rr-r),missing_pad_names=sorted(p-pp),extra_pad_names=sorted(pp-p),active_groups_equal=set(g)==set(gg),missing_active_groups=len(set(g)-set(gg)),extra_active_groups=len(set(gg)-set(g)),drc_violations=len(drc['violations']),unconnected_items=len(drc['unconnected_items']),schematic_parity_types=dict(Counter(x['type'] for x in drc['schematic_parity'])))
(RUN/'export-preservation.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
