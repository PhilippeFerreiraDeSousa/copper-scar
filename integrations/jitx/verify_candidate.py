"""Fresh immutable-input check, independent of prior normalization success flags."""
from roundtrip import *
import sys
p=Path(sys.argv[1]);src=CAND/'hierarchy';xml=ET.parse(RUN/'hierarchy-netlist.xml').getroot()
nc={(x.attrib['ref'],x.attrib['pin']) for x in xml.findall('./nets/net/node') if 'no_connect' in x.attrib.get('pintype','')}
a=parse(src/'pcbgolf.kicad_pcb');b=parse(p/'pcbgolf.kicad_pcb');ap,ag=group_inventory(a,nc);bp,bg=group_inventory(b,nc)
assert ap==bp and set(ag)==set(bg),'electrical topology drift'
assert not children(b,'net_class'),'legacy embedded rule override'
seen=set()
def verify_ids(item):
 if not isinstance(item,list):return
 if item and str(item[0]) in {'uuid','tstamp'}:
  value=str(item[1]);assert value not in seen,'duplicate object UUID';seen.add(value)
 for child in item:verify_ids(child)
verify_ids(b)
for f in list(src.glob('*.kicad_sch'))+[src/'pcbgolf.kicad_pro']:
 assert (p/f.name).read_bytes()==f.read_bytes(),f'source support changed: {f.name}'
def values(fp):
 d={str(x[1]):str(x[2]) for x in children(fp,'property')}
 for x in children(fp,'fp_text'):
  k={'reference':'Reference','value':'Value'}.get(str(x[1]))
  if k:d[k]=str(x[2])
 return d
orig={ref(f):f for f in children(a,'footprint')};export={ref(f):f for f in children(b,'footprint')};assert set(orig)==set(export)
for r,f in orig.items():
 v,w=values(f),values(export[r])
 for key in ['Reference','Value','MPN']:
  assert v.get(key)==w.get(key),(r,key,'component identity drift')
print(json.dumps({'passed':True,'components':len(orig),'named_pads':len(bp),'active_partitions':len(bg),'source_schematics_and_rules_identical':True,'geometry_qualified':False}))
