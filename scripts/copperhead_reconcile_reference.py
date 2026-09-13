"""Apply only native-netlist-backed J3 aliases and schematic BOM attributes."""
from pathlib import Path
import argparse, json, shutil, xml.etree.ElementTree as E
import sexpdata as s

def ns(n,k):return [v for v in n if isinstance(v,list) and v and str(v[0])==k]
ap=argparse.ArgumentParser();ap.add_argument('source',type=Path);ap.add_argument('destination',type=Path);a=ap.parse_args();shutil.copytree(a.source,a.destination)
x=E.parse(a.source/'reference.net.xml');pin={}
for net in x.findall('./nets/net'):
 for n in net.findall('node'):pin[(n.attrib['ref'],n.attrib['pin'])]=net.attrib['name']
b=s.loads((a.destination/'pcbgolf.kicad_pcb').read_text());changes=[]
for fp in ns(b,'footprint'):
 ref=next(v[2] for v in ns(fp,'property') if v[1]=='Reference')
 if ref=='J3':
  for pad in ns(fp,'pad'):
   for net in ns(pad,'net'):
    name=pin.get((ref,str(pad[1])))
    if name and name!=net[-1]:
     assert name.startswith('unconnected-') and str(net[-1]).startswith('unconnected-')
     changes.append(dict(ref=ref,pad=pad[1],old=net[-1],new=name,reason='Native schematic groups overlapping physical aliases of the same NC terminal'))
     net[-1]=name
 if ref in ['BH1','BH2','BH3','BH4','C6','C10','J4']:
  for attr in ns(fp,'attr'):
   if s.Symbol('exclude_from_bom') in attr:attr.remove(s.Symbol('exclude_from_bom'));changes.append(dict(ref=ref,attribute='exclude_from_bom',new=False,reason='Match original schematic in_bom yes; DNP and all physical parts preserved'))
(a.destination/'pcbgolf.kicad_pcb').write_text(s.dumps(b));(a.destination/'reference-reconciliation.json').write_text(json.dumps(changes,indent=2));print(json.dumps(changes))
