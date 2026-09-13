"""Compare the runtime's materialized pin-to-pad net graph to original KiCad."""
from import_experiments import *
from collections import defaultdict
import xml.etree.ElementTree as ET
import re
def padname(s):
 s=str(s);s={'A[0]':'A', 'A[1]':"A'", 'B[0]':'B', 'B[1]':"B'"}.get(s,s);m=re.fullmatch(r"p\[(\d+)\]",s);return m[1] if m else s
cache=BASE/'designs/pcbgolf_import.current.PcbgolfFull/cache'
tree=json.loads((cache/'design-explorer.json').read_text());nets=json.loads((cache/'netlist.json').read_text())
components=[]
def walk(m):
 components.extend(m['component-instances'])
 for child in m['module-instances']:walk(child)
walk(tree['module'])
pinmap={};nc=set();allpads=set();refs=[];unknown=[]
for c in components:
 ref=c['reference-designator'];refs.append(ref)
 for pad in c['package']['pads']:allpads.add((ref,padname(pad['ref'])))
 for entry in c['package']['mapping']['entries']:
  v=entry['value'];vs=v if isinstance(v,list) else [v]
  endpoints={(ref,padname(p['ref'])) for p in vs}
  pinmap.setdefault(c['ref']+'.'+entry['key']['ref'],set()).update(endpoints)
 for p in c['no-connect-pins']:
  key=c['ref']+'.'+(p['ref'] if isinstance(p,dict) else p)
  if key in pinmap:nc.update(pinmap[key])
  else:unknown.append(key)
# Resolve noConnects from the actual translated payload: per-component explorer
# defaults do not include circuit-level no-connect declarations.
payload=json.loads((cache/'load-cache.json').read_text())['v1']
mods={m['id']:m for m in payload['modules']}
cs={c['id']:c for c in payload['components']}
root=mods[payload['module']]
def resolve(start,ids):
 obj=start;names=[]
 for i in ids:
  if 'instances' in obj:
   inst=next(x for x in obj['instances'] if x['id']==i);names.append(inst['name']);obj=mods.get(inst['instantiable'],cs.get(inst['instantiable']))
  else:
   names.append(next(x['name'] for x in obj['ports'] if x['id']==i))
 return '.'.join(names)
for m in payload['modules']:
 # The imported full design declares every no-connect on its root.
 if m.get('noConnects'):
  assert m['id']==root['id']
  for n in m['noConnects']:
   key=resolve(m,n['path']);nc.update(pinmap[key])
jgroups=[]
for n in nets:
 eps=set()
 for p in n['pins']:
  if p not in pinmap:unknown.append(p)
  else:eps.update(pinmap[p])
 if eps:jgroups.append((n['name'],eps))
xml=ET.parse(RUN/'hierarchy-netlist.xml').getroot()
expected_nc={(n.attrib['ref'],n.attrib['pin']) for n in xml.findall('./nets/net/node') if 'no_connect' in n.attrib.get('pintype','')}
bp=defaultdict(set);brefs=[];bpad=set()
for f in children(parse(SRC/'pcbgolf.kicad_pcb'),'footprint'):
 ref=next(p[2] for p in children(f,'property') if p[1]=='Reference');brefs.append(ref)
 for pad in children(f,'pad'):
  if str(pad[1]):bpad.add((ref,str(pad[1])))
  ns=children(pad,'net')
  if ns:bp[str(ns[0][-1])].add((ref,str(pad[1])))
active=[(n,ps-expected_nc) for n,ps in bp.items() if ps-expected_nc]
actual=[(n,ps-expected_nc) for n,ps in jgroups if ps-expected_nc]
exp_sets={frozenset(ps):n for n,ps in active};act_sets={frozenset(ps):n for n,ps in actual}
result=dict(components=len(components),missing_components=sorted(set(brefs)-set(refs)),extra_components=sorted(set(refs)-set(brefs)),original_unique_named_pads=len(bpad),runtime_unique_named_pads=len(allpads),missing_pads=sorted(bpad-allpads),extra_pads=sorted(allpads-bpad),expected_nc_count=len(expected_nc),runtime_nc_count=len(nc),missing_no_connects=sorted(expected_nc-nc),extra_no_connects=sorted(nc-expected_nc),expected_active_nets=len(active),runtime_active_nets=len(actual),missing_active_groups=[dict(name=n,pins=sorted(ps)) for ps,n in exp_sets.items() if ps not in act_sets],extra_active_groups=[dict(name=n,pins=sorted(ps)) for ps,n in act_sets.items() if ps not in exp_sets],unknown_runtime_pin_paths=unknown)
(RUN/'runtime-preservation.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:(len(v) if isinstance(v,list) else v) for k,v in result.items()},indent=2))
