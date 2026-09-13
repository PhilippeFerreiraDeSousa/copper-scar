"""Derive an explicitly reduced circuit from the frozen PCBGolf source."""
from pathlib import Path
import argparse,copy,json,uuid,hashlib
import sexpdata as sx
S=sx.Symbol
def nodes(n,k):return [x for x in n if isinstance(x,list) and x and str(x[0])==k]
def one(n,k):return nodes(n,k)[0]
counter=0
def uid():
 global counter
 counter+=1
 return str(uuid.uuid5(uuid.NAMESPACE_URL,"copper-small-loop-v1/"+str(counter)))
def prop(n,k):return next(x for x in nodes(n,'property') if x[1]==k)
ap=argparse.ArgumentParser();ap.add_argument('source',type=Path);ap.add_argument('out',type=Path);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=False)
refs=['J4','Q2','R78','R98','R82','R83','R90','R91','LED10','LED6','R74','C46','C50','R19','C5']
netgroups={
'GND':['J4.1','J4.8','Q2.2','R78.2','R98.1','LED10.3','LED6.C','C46.2','C50.2','C5.2'],
'EXT_5V':['J4.2','R74.1','C46.1','C50.1','C5.1'],
'CH1_SBU1_IGN':['J4.3','Q2.1','R78.1','R83.2'],
'CH1_SBU1_RELAY':['J4.4','Q2.3','R98.2','R82.2'],
'CH1_SBU1':['J4.5','R90.2','R91.2','R19.2'],
'EXT_SENSE':['J4.6','R19.1'],
'EXT_5V_MONITOR':['J4.7'],
'Net-(Q2-D1)':['Q2.5','R90.1'],'Net-(Q2-D2)':['Q2.4','R91.1'],
'Net-(LED10-AR)':['LED10.1','R83.1'],'Net-(LED10-AG)':['LED10.2','R82.1'],
'Net-(LED6-PadA)':['LED6.A','R74.2']}
# Header pin 7 is a second supply contact, not a floating unused net.
netgroups['EXT_5V'].append('J4.7');del netgroups['EXT_5V_MONITOR']
padnets={p:n for n,ps in netgroups.items() for p in ps}
root=uid();sch=sx.loads(f'(kicad_sch (version 20260306) (generator eeschema) (uuid "{root}") (paper "A3") (lib_symbols))')
lib=one(sch,'lib_symbols');syms={};libs={}
for file in a.source.glob('*.kicad_sch'):
 d=sx.loads(file.read_text())
 for l in nodes(one(d,'lib_symbols'),'symbol'):libs[l[1]]=l
 for s in nodes(d,'symbol'):
  ref=prop(s,'Reference')[2]
  if ref in refs:syms[ref]=s
poses={}
for i,ref in enumerate(refs):
 s=copy.deepcopy(syms[ref]);lid=one(s,'lib_id')[1]
 if not any(x[1]==lid for x in nodes(lib,'symbol')):lib.append(copy.deepcopy(libs[lid]))
 x,y=35+(i%5)*65,35+(i//5)*55;one(s,'at')[1:]=[x,y,0]
 s[:]=[v for v in s if not(isinstance(v,list) and v and str(v[0]) in ('mirror','instances'))]
 su=one(s,'uuid')[1];s.append(sx.loads(f'(instances (project "small-loop" (path "/{root}" (reference "{ref}") (unit 1))))'))
 for j,p in enumerate(nodes(s,'property')):
  if nodes(p,'at'):one(p,'at')[1:]=[x,y-8+j*2,0]
 sch.append(s)
 pins=[]
 for sub in nodes(libs[lid],'symbol'):
  pins+=nodes(sub,'pin')
 for pin in pins:
  num=one(pin,'number')[1];net=padnets.get(ref+'.'+num)
  if not net:raise ValueError((ref,num))
  px,py=one(pin,'at')[1:3];xx,yy=round(x+px,6),round(y-py,6)
  sch.append(sx.loads(f'(label "{net}" (at {xx} {yy} 0) (effects (font (size 1 1)) (justify left bottom)) (uuid "{uid()}"))'))
 poses[ref]=[30+(i%5)*8,30+(i//5)*9,0]
sch.append(sx.loads('(sheet_instances (path "/" (page "1")))'))
(a.out/'small-loop.kicad_sch').write_text(sx.dumps(sch))
project=json.loads((a.source/'pcbgolf.kicad_pro').read_text());project['schematic']['top_level_sheets']=[{'filename':'small-loop.kicad_sch','uuid':root}]
(a.out/'small-loop.kicad_pro').write_text(json.dumps(project,indent=2))
manifest={'label':'PCB Golf-inspired demo circuit','refs':refs,'nets':netgroups,'poses':poses,'schematic_root':root,'symbol_uuids':{r:one(syms[r],'uuid')[1] for r in refs},'source_hashes':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in a.source.glob('*.kicad*')}}
(a.out/'circuit.json').write_text(json.dumps(manifest,indent=2))
import shutil
for f in ['pcbgolf.pretty','pcbgolf.kicad_sym','fp-lib-table','sym-lib-table']:
 src=a.source/f
 if src.is_dir():shutil.copytree(src,a.out/f)
 else:shutil.copy2(src,a.out/f)

# Filter syntax first: bulk Remove in this KiCad SWIG version invalidates wrappers.
d=sx.loads((a.source/'pcbgolf.kicad_pcb').read_text())
def keep(v):
 if not isinstance(v,list) or not v:return True
 if str(v[0]) in ('segment','via','zone','gr_line','gr_rect','gr_text','gr_arc','gr_poly'):return False
 if str(v[0])=='footprint':return prop(v,'Reference')[2] in refs
 return True
(a.out/'filtered.kicad_pcb').write_text(sx.dumps([v for v in d if keep(v)]))
