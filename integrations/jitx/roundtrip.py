"""Restore source identity/rules around real JITX copper; never repair geometry.
Requires sexpdata. Refuses topology changes before relabeling. Every normalization logged.
"""
from import_experiments import *
from collections import defaultdict
import copy, xml.etree.ElementTree as ET, argparse, time, uuid
ALIASES={'A0':'A','A1':"A'",'B0':'B','B1':"B'"}
def ref(fp):
 return next((str(p[2]) for p in children(fp,'property') if p[1]=='Reference'),None) or next(str(p[2]) for p in children(fp,'fp_text') if str(p[1])=='reference')
def group_inventory(board,nc):
 groups=defaultdict(set);pads=set()
 for fp in children(board,'footprint'):
  r=ref(fp)
  for p in children(fp,'pad'):
   if not str(p[1]):continue
   pin=ALIASES.get(str(p[1]),str(p[1])) if r=='SW1' else str(p[1]);ep=(r,pin)
   if ep in pads:raise ValueError(f'duplicate named physical pad {ep}')
   pads.add(ep);n=children(p,'net')
   if n and n[0][1]!=0 and ep not in nc:groups[str(n[0][-1])].add(ep)
 return pads,{frozenset(v):k for k,v in groups.items()}
def adapt(export_path,out):
 start=time.monotonic();xml=ET.parse(RUN/'hierarchy-netlist.xml').getroot();nodes={};nc=set()
 for n in xml.findall('./nets/net'):
  for x in n.findall('node'):
   ep=(x.attrib['ref'],x.attrib['pin']);nodes[ep]=n.attrib['name'].replace('CD/DAT3','CD{slash}DAT3')
   if 'no_connect' in x.attrib.get('pintype',''):nc.add(ep)
 original=parse(CAND/'hierarchy/pcbgolf.kicad_pcb');export=parse(export_path)
 op,og=group_inventory(original,nc);ep,eg=group_inventory(export,nc)
 assert op==ep,('pad inventory changed',op-ep,ep-op)
 assert set(og)==set(eg),'active electrical partition changed; cannot relabel'
 refs={ref(f):f for f in children(original,'footprint')};assert set(refs)=={ref(f) for f in children(export,'footprint')}
 # Exact membership match provides a reversible name map for routes/vias as well as pads.
 name_map={eg[g]:og[g] for g in eg};canonical={}
 for g in og:
  names={nodes[e] for e in g};assert len(names)==1,(g,names)
  canonical[eg[g]]=next(iter(names))
 nets=sorted(set(nodes.values())|set(canonical.values()));ids={n:i+1 for i,n in enumerate(nets)}
 old_ids={int(n[1]):str(n[2]) for n in children(export,'net')}
 changes=[]
 def translate(item):
  if not isinstance(item,list) or not item:return
  if str(item[0])=='net' and len(item)>1:
   old=old_ids.get(int(item[1]));new=canonical.get(old)
   if int(item[1]) and new is None:raise ValueError(f'unmapped copper net {old}')
   if new:item[:]=[sx.Symbol('net'),ids[new]]+([new] if len(item)>2 else [])
  else:
   for v in item:translate(v)
 export=[v for v in export if not(isinstance(v,list) and v and str(v[0]) in {'net','net_class'})]
 for f in children(export,'footprint'):
  r=ref(f);src=refs[r]
  changes.append({'ref':r,'footprint_library_from':str(f[1]),'footprint_library_to':str(src[1])});f[1]=src[1]
  # Labels and schematic identity only. All pads, graphics, mask, models and placement remain exported.
  keys={'path','sheetname','sheetfile','attr'}
  f[:]=[v for v in f if not(isinstance(v,list) and v and (str(v[0]) in keys or str(v[0])=='property'))]
  f.extend(copy.deepcopy(v) for v in src if isinstance(v,list) and v and str(v[0]) in keys)
  props={str(v[1]):v for v in children(src,'property')}
  for v in children(f,'fp_text'):
   k={'reference':'Reference','value':'Value'}.get(str(v[1]))
   if k and k in props:
    if v[2]!=props[k][2]:changes.append({'ref':r,'field':k,'from':str(v[2]),'to':str(props[k][2])})
    v[2]=props[k][2]
  # Extra source fields retain their original values; hidden and do not change physical copper.
  f.extend(copy.deepcopy(v) for k,v in props.items() if k not in {'Reference','Value'})
  for p in children(f,'pad'):
   if r=='SW1' and str(p[1]) in ALIASES:
    old=str(p[1]);p[1]=ALIASES[old];changes.append({'ref':r,'pad_from':old,'pad_to':p[1]})
   endpoint=(r,str(p[1]));p[:]=[v for v in p if not(isinstance(v,list) and v and str(v[0]) in {'net','net_class'})]
   if endpoint in nodes:p.append([sx.Symbol('net'),ids[nodes[endpoint]],nodes[endpoint]])
 # Translate copper outside footprints; pad nets already replaced with canonical IDs.
 for v in export:
  if isinstance(v,list) and v and str(v[0])!='footprint':translate(v)
 first_fp=next(i for i,v in enumerate(export) if isinstance(v,list) and v and str(v[0])=='footprint')
 export[first_fp:first_fp]=[[sx.Symbol('net'),i,n] for n,i in ids.items()]
 # Preserve exported stackup but restore source mask/other setup controls.
 setup=one(export,'setup');stack=children(setup,'stackup');setup[:]=copy.deepcopy(one(original,'setup'));setup.extend(stack)
 # Raw JITX exports can reuse footprint UUIDs for routed copper. Give each
 # subsequent occurrence a deterministic unique identity; geometry stays exact.
 seen=set();id_changes=[]
 def unique_ids(item,path):
  if not isinstance(item,list):return
  if item and str(item[0]) in {'uuid','tstamp'}:
   old=str(item[1])
   if old in seen:
    new=str(uuid.uuid5(uuid.NAMESPACE_URL,'jitx-export-object/'+old+'/'+path))
    assert new not in seen
    item[1]=sx.Symbol(new) if isinstance(item[1],sx.Symbol) else new
    id_changes.append({'path':path,'from':old,'to':new})
   seen.add(str(item[1]))
  for index,v in enumerate(item):
   if isinstance(v,list):unique_ids(v,path+'/'+str(index))
 unique_ids(export,'board')
 shutil.copytree(CAND/'hierarchy',out,ignore=shutil.ignore_patterns('*.kicad_pcb','*.net','*.kicad_prl','*.lck'))
 write(out/'pcbgolf.kicad_pcb',export)
 # Verify metadata changes did not alter active membership or named pads.
 ap,ag=group_inventory(export,nc);assert ap==op and set(ag)==set(og)
 report={'source':str(export_path),'topology_equal':True,'named_pads':len(ap),'active_nets':len(ag),'footprints':len(refs),'pad_aliases':ALIASES,'changes':changes,'net_name_map':canonical,'nc_pads_restored_from_original_schematic':len(nc),'source_rules_restored':True,'embedded_legacy_netclasses_removed':True,'unique_object_ids':True,'duplicate_object_ids_reassigned':len(id_changes),'geometry_certified':False,'elapsed_seconds':time.monotonic()-start}
 (out/'object-id-map.json').write_text(json.dumps(id_changes,indent=2))
 (out/'normalization.json').write_text(json.dumps(report,indent=2));return report
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('export',type=Path);p.add_argument('out',type=Path);a=p.parse_args();r=adapt(a.export,a.out);print(json.dumps({k:v for k,v in r.items() if k not in ['changes','net_name_map']},indent=2))
