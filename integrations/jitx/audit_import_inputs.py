from import_experiments import *
from collections import defaultdict,Counter
import xml.etree.ElementTree as ET,copy
xml=ET.parse(RUN/'hierarchy-netlist.xml').getroot()
board=parse(SRC/'pcbgolf.kicad_pcb');bp=defaultdict(set)
for fp in children(board,'footprint'):
 ref=next(x[2] for x in children(fp,'property') if x[1]=='Reference')
 for pad in children(fp,'pad'):
  ns=children(pad,'net')
  if ns:bp[str(ns[0][-1])].add((ref,str(pad[1])))
xp={n.attrib['name']:{(x.attrib['ref'],x.attrib['pin']) for x in n.findall('node')} for n in xml.findall('./nets/net')}
binv={p:n for n,ps in bp.items() for p in ps};xinv={p:n for n,ps in xp.items() for p in ps}
missing=sorted(set(binv)-set(xinv));extra=sorted(set(xinv)-set(binv));shared=set(binv)&set(xinv)
# Compare entire connectivity partitions, not names of auto-generated nets.
splits=[];merges=[]
for n,pins in bp.items():
 groups={xinv[p] for p in pins if p in shared}
 if len(groups)>1:splits.append(dict(board_net=n,hierarchy_nets=sorted(groups)))
for n,pins in xp.items():
 groups={binv[p] for p in pins if p in shared}
 if len(groups)>1:merges.append(dict(hierarchy_net=n,board_nets=sorted(groups)))
mapdata=json.loads((RUN/'hierarchy-mapping.json').read_text());preservation=[]
for m in mapdata:
 orig=parse(SRC/m['original']);new=parse(CAND/'hierarchy'/m['file'])
 def electrical(d):
  d=copy.deepcopy(d)
  d=[x for x in d if not(isinstance(x,list) and x and str(x[0])=='sheet_instances')]
  for sym in children(d,'symbol'):
   sym[:]=[x for x in sym if not(isinstance(x,list) and x and str(x[0])=='instances')]
  return d
 preservation.append(dict(file=m['original'],all_content_except_instance_context_equal=electrical(orig)==electrical(new),symbols=len(children(orig,'symbol')),no_connects=len(children(orig,'no_connect')),local_labels=len(children(orig,'label')),global_labels=len(children(orig,'global_label'))))
original_pro=json.loads((SRC/'pcbgolf.kicad_pro').read_text());new_pro=json.loads((CAND/'hierarchy/pcbgolf.kicad_pro').read_text())
new_pro['schematic']['top_level_sheets']=original_pro['schematic']['top_level_sheets'];new_pro['sheets']=original_pro['sheets']
newboard=parse(CAND/'hierarchy/pcbgolf.kicad_pcb')
for a,b in zip(children(board,'footprint'),children(newboard,'footprint')):
 one(b,'path')[1]=one(a,'path')[1];one(b,'sheetfile')[1]=one(a,'sheetfile')[1]
result=dict(board_nets=len(bp),board_pin_memberships=sum(map(len,bp.values())),hierarchy_nets=len(xp),hierarchy_pin_memberships=sum(map(len,xp.values())),hierarchy_components=len(xml.findall('./components/comp')),missing_pins=missing,extra_pins=extra,splits=splits,merges=merges,preserved_sheet_content=preservation,pro_equal_except_hierarchy_metadata=original_pro==new_pro,board_equal_except_schematic_paths=board==newboard,named_net_changes=[dict(pin=p,board=binv[p],hierarchy=xinv[p]) for p in sorted(shared) if binv[p]!=xinv[p]],reference_unchanged=hashes(SRC)==json.loads((RUN/'reference-hashes.json').read_text()))
(RUN/'input-equivalence.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k!='named_net_changes'},indent=2));print('net name differences',len(result['named_net_changes']))
