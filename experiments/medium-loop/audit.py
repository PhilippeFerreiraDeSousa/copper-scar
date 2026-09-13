"""Independent saved-file acceptance; producer summaries do not decide validity."""
from pathlib import Path
import hashlib,json,sys,xml.etree.ElementTree as ET
import sexpdata as sx

def nodes(n,k):return [v for v in n if isinstance(v,list) and v and str(v[0])==k]
def first(n,k):return nodes(n,k)[0]
def inventory(path):
 d=sx.loads(Path(path).read_text());result={};groups={};netnames={v[1]:v[2] for v in nodes(d,"net")}
 for f in nodes(d,'footprint'):
  ref=next((v[2] for v in nodes(f,'property') if v[1]=='Reference'),None)
  if ref is None:ref=next(v[2] for v in nodes(f,'fp_text') if str(v[1])=='reference')
  pads={}
  for pad in nodes(f,'pad'):
   if not str(pad[1]):continue
   nv=first(pad,'net') if nodes(pad,'net') else [None,0];net=nv[2] if len(nv)>2 else nv[1] if isinstance(nv[1],str) else netnames.get(nv[1],'')
   if net:groups.setdefault(net,[]).append(ref+'.'+str(pad[1]))
   pads[str(pad[1])]=sx.dumps([pad[1:4]]+[v for v in pad[4:] if isinstance(v,list) and str(v[0]) in ['size','drill','layers','primitives','roundrect_rratio','chamfer_ratio','chamfer']]+[[sx.Symbol('offset'),*first(pad,'at')[1:3]]])
  result[ref]={'library':f[1],'pads':pads,'pose':first(f,'at')[1:]}
 return result,{k:sorted(v) for k,v in groups.items()}

def audit(folder,manifest,original):
 f=Path(folder);m=json.loads(Path(manifest).read_text());src=Path(original)
 inv,nets=inventory(f/'pcbgolf.kicad_pcb');old,_=inventory(src/'pcbgolf.kicad_pcb');expected={k:sorted(v) for k,v in m['nets'].items()}
 drc=json.loads((f/'drc.json').read_text());native=json.loads((f/'native-audit.json').read_text());settings=json.loads((f/'pcbgolf.kicad_pro').read_text());orig=json.loads((src/'pcbgolf.kicad_pro').read_text())
 rules={k:settings[k]==orig[k] for k in ['erc','net_settings']};rules['drc']=settings['board']['design_settings']==orig['board']['design_settings']
 footprints={r:inv[r]['pads']==old[m.get('original_ref_aliases',{}).get(r,r)]['pads'] and inv[r]['library']==old[m.get('original_ref_aliases',{}).get(r,r)]['library'] for r in inv}
 required=[v for v in drc['violations'] if v['severity']=='error' or v['type'] in ['text_height','text_thickness','silk_overlap','silk_over_copper','hole_to_hole','isolated_copper','track_dangling','via_dangling']]
 invariants=hashlib.sha256((f/'pcbgolf.kicad_pcb').read_bytes()).hexdigest()==native['board_sha256'] and all(rules.values()) and set(inv)==set(m['refs']) and nets==expected and all(footprints.values()) and native['copper_layers']==m.get('expected_copper_layers',2)
 width_ok=all(w>=.2-1e-6 for w in native['track_widths_mm']);via_ok=all(abs(v['drill']-.3)<1e-6 and abs(v['diameter']-.6)<1e-6 and v['net'] in expected for v in native['vias'])
 cost=len(drc['unconnected_items'])+len(required)+len(drc.get('schematic_parity',[{'missing':'check'}]))+(0 if invariants and width_ok and via_ok else 10000)
 result={'accepted':cost==0 and native['native_open_count']==0,'feasibility_cost':cost,'native_open_count':native['native_open_count'],'drc_opens':len(drc['unconnected_items']),'schematic_parity_issues':len(drc.get('schematic_parity',[{'missing':'check'}])),'required_violations':required,'all_drc_violations':len(drc['violations']),'rules_preserved':rules,'footprints_preserved':footprints,'netlist_parity':nets==expected,'component_count':len(inv),'net_count':len(nets),'widths_ok':width_ok,'via_rules_ok':via_ok,'wire_length_mm':native['wire_length_mm'],'vias':len(native['vias']),'board_sha256':native['board_sha256']}
 (f/'acceptance.json').write_text(json.dumps(result,indent=2));return result
if __name__=='__main__':print(json.dumps(audit(*sys.argv[1:]),indent=2))
