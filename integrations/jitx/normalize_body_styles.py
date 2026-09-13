"""Materialize common symbol body style 0 into style 1, then verify native graph."""
from import_experiments import *
import xml.etree.ElementTree as ET
b=CAND/'hierarchy-explicit-body-style';shutil.copytree(CAND/'hierarchy-centralized-instances',b)
changes=[]
for p in list(b.glob('*.kicad_sch'))+list(b.glob('*.kicad_sym')):
 d=parse(p);libs=children(one(d,'lib_symbols'),'symbol') if p.suffix=='.kicad_sch' else children(d,'symbol')
 for lib in libs:
  for sub in list(children(lib,'symbol')):
   name,u,style=sub[1].rsplit('_',2)
   if style!='0':continue
   target=name+'_'+u+'_1';matches=[x for x in children(lib,'symbol') if x[1]==target]
   if matches:matches[0].extend(sub[2:]);lib.remove(sub)
   else:sub[1]=target
   changes.append(dict(file=p.name,symbol=lib[1],unit=u))
 write(p,d)
(RUN/'body-style-transform.json').write_text(json.dumps(changes,indent=2))
call('b-body-style-netlist',[KC,'sch','export','netlist','--format','kicadxml','-o',str(RUN/'body-style-netlist.xml'),str(b/'pcbgolf.kicad_sch')],b)
def graph(p):
 x=ET.parse(p).getroot();return {n.attrib['name']:sorted((p.attrib['ref'],p.attrib['pin']) for p in n.findall('node')) for n in x.findall('./nets/net')}
assert graph(RUN/'hierarchy-netlist.xml')==graph(RUN/'body-style-netlist.xml')
call('b-body-style-import',[CLI,'project','import','kicad',str(b),'--output',str(output('b-body-style-output'))],RUN)
