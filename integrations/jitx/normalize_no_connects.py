"""Represent explicit no-connect board pads as unassigned during legacy import."""
from import_experiments import *
import xml.etree.ElementTree as ET
b=CAND/'hierarchy-unassigned-nc';shutil.copytree(CAND/'hierarchy-single-instance-source',b)
x=ET.parse(RUN/'hierarchy-netlist.xml').getroot()
nc={(n.attrib['ref'],n.attrib['pin']) for n in x.findall('./nets/net/node') if 'no_connect' in n.attrib.get('pintype','')}
p=b/'pcbgolf.kicad_pcb';d=parse(p);changes=[]
for f in children(d,'footprint'):
 ref=next(x[2] for x in children(f,'property') if x[1]=='Reference')
 for pad in children(f,'pad'):
  if (ref,str(pad[1])) in nc:
   for n in children(pad,'net'):
    changes.append(dict(ref=ref,pin=str(pad[1]),original_net=n[1:]));pad.remove(n)
write(p,d)
(RUN/'no-connect-pad-mapping.json').write_text(json.dumps(changes,indent=2))
call('b-unassigned-nc-import',[CLI,'project','import','kicad',str(b),'--output',str(output('b-unassigned-nc-output'))],RUN)
