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
 return str(uuid.uuid5(uuid.NAMESPACE_URL,"copper-medium-loop-v1/"+str(counter)))
def prop(n,k):return next(x for x in nodes(n,'property') if x[1]==k)
ap=argparse.ArgumentParser();ap.add_argument('source',type=Path);ap.add_argument('out',type=Path);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=False)
# Select the complete original eight SBU switching/sense blocks by connectivity.
board=sx.loads((a.source/'pcbgolf.kicad_pcb').read_text())
allfp={prop(f,'Reference')[2]:f for f in nodes(board,'footprint')}
refs=['Q'+str(i) for i in range(2,10)]+['LED'+str(i) for i in range(10,18)]+['R'+str(i) for i in range(78,126)]+['R'+str(i) for i in range(12,20)]+['LED6','R74','C46','C50','C5']
# Sense resistors in original channel order are not consecutively numbered.
refs=[r for r in refs if r not in ['R12','R15','R16']]+['R20']
# Derive sense refs from their SBU connection to avoid assumptions about numbering.
refs=[r for r in refs if not (r.startswith('R') and int(r[1:])<30)]
refs += [r for r,f in allfp.items() if r.startswith('R') and int(r[1:])<30 and any(nodes(p,'net') and str(one(p,'net')[-1]).startswith('CH') and '_SBU' in str(one(p,'net')[-1]) for p in nodes(f,'pad'))]
netgroups={}
for r in refs:
 for pad in nodes(allfp[r],'pad'):
  if not pad[1]:continue
  net=one(pad,'net')[-1]
  if r in ['LED6','R74','C46','C50','C5'] and net!='GND' and not (r=='LED6' or (r=='R74' and pad[1]=='2')):net='EXT_5V'
  netgroups.setdefault(net,[]).append(r+'.'+pad[1])
# Eight copies of original J4 connector expose each block's controls, load and sense.
aliases={}
for i in range(8):
 ref='J'+str(101+i);refs.append(ref);aliases[ref]='J4'
 ch=i%4+1;sbu=i//4+1;prefix=f'CH{ch}_SBU{sbu}'
 sense=next(n for n,ps in netgroups.items() if any(p.split('.')[0] in [r for r in refs if r.startswith('R') and int(r[1:])<30] for p in ps) and n!=prefix and n!='GND' and any(p.split('.')[0] in [v.split('.')[0] for v in netgroups[prefix]] for p in ps))
 for pin,net in {1:'GND',2:'EXT_5V',3:prefix+'_IGN',4:prefix+'_RELAY',5:prefix,6:sense,7:'EXT_5V',8:'GND'}.items():netgroups.setdefault(net,[]).append(f'{ref}.{pin}')
padnets={p:n for n,ps in netgroups.items() for p in ps}
root=uid();sch=sx.loads(f'(kicad_sch (version 20260306) (generator eeschema) (uuid "{root}") (paper "A0") (lib_symbols))')
lib=one(sch,'lib_symbols');syms={};libs={}
for file in a.source.glob('*.kicad_sch'):
 d=sx.loads(file.read_text())
 for l in nodes(one(d,'lib_symbols'),'symbol'):libs[l[1]]=l
 for s in nodes(d,'symbol'):
  ref=prop(s,'Reference')[2]
  if ref in refs or ref=='J4':syms[ref]=s
for ref,original in aliases.items():
 syms[ref]=copy.deepcopy(syms[original]);prop(syms[ref],'Reference')[2]=ref;one(syms[ref],'uuid')[1]=uid()
 prop(syms[ref],'Value')[2]='HEADER_2x04_2.54mm_POPULATED'
 for key,val in [('in_bom','yes'),('on_board','yes'),('dnp','no')]:
  if nodes(syms[ref],key):one(syms[ref],key)[1]=S(val)
poses={}
for i,ref in enumerate(refs):
 s=copy.deepcopy(syms[ref]);lid=one(s,'lib_id')[1]
 if not any(x[1]==lid for x in nodes(lib,'symbol')):lib.append(copy.deepcopy(libs[lid]))
 x,y=35+(i%10)*65,35+(i//10)*55;one(s,'at')[1:]=[x,y,0]
 s[:]=[v for v in s if not(isinstance(v,list) and v and str(v[0]) in ('mirror','instances'))]
 su=one(s,'uuid')[1];s.append(sx.loads(f'(instances (project "medium-loop" (path "/{root}" (reference "{ref}") (unit 1))))'))
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
  sch.append(sx.loads(f'(global_label "{net}" (shape bidirectional) (at {xx} {yy} 0) (effects (font (size 1 1)) (justify left bottom)) (uuid "{uid()}"))'))
 poses[ref]=[28+(i%10)*6,32+(i//10)*5,0]
# Headers sit in two fixed accessible banks; passives are initially distributed.
for i,ref in enumerate(aliases):poses[ref]=[28+(i%4)*18,25 if i<4 else 75,0]
sch.append(sx.loads('(sheet_instances (path "/" (page "1")))'))
(a.out/'medium-loop.kicad_sch').write_text(sx.dumps(sch))
project=json.loads((a.source/'pcbgolf.kicad_pro').read_text());project['schematic']['top_level_sheets']=[{'filename':'medium-loop.kicad_sch','uuid':root}]
(a.out/'medium-loop.kicad_pro').write_text(json.dumps(project,indent=2))
manifest={'label':'PCB Golf-inspired demo circuit','refs':refs,'original_ref_aliases':aliases,'outline_mm':[20,20,90,80],'nets':netgroups,'poses':poses,'schematic_root':root,'symbol_uuids':{r:one(syms[r],'uuid')[1] for r in refs},'source_hashes':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in a.source.glob('*.kicad*')}}
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
d=[v for v in d if keep(v)]
for ref,original in aliases.items():
 f=copy.deepcopy(allfp[original]);prop(f,'Reference')[2]=ref
 prop(f,'Value')[2]='HEADER_2x04_2.54mm_POPULATED'
 one(f,'attr')[1:]=[S('through_hole')]
 f.append(sx.loads('(model "${KIPRJMOD}/models/PinHeader_2x04_P2.54mm_Vertical.step" (offset (xyz -3.81 -1.27 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 90)))'))
 for v in nodes(f,'uuid'):v[1]=uid()
 for pad in nodes(f,'pad'):
  for v in nodes(pad,'uuid'):v[1]=uid()
 d.append(f)
(a.out/'filtered.kicad_pcb').write_text(sx.dumps(d))

(a.out/'models').mkdir()
shutil.copy2('/Users/philippe/Applications/KiCad/KiCad.app/Contents/SharedSupport/3dmodels/Connector_PinHeader_2.54mm.3dshapes/PinHeader_2x04_P2.54mm_Vertical.step',a.out/'models')

# Populate the retained header library consistently with board instances.
libpath=a.out/'pcbgolf.pretty/2X04.kicad_mod'
f=sx.loads(libpath.read_text())
if nodes(f,'attr'):one(f,'attr')[1:]=[S('through_hole')]
else:f.append([S('attr'),S('through_hole')])
f.append(sx.loads('(model "${KIPRJMOD}/models/PinHeader_2x04_P2.54mm_Vertical.step" (offset (xyz -3.81 -1.27 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 90)))'))
libpath.write_text(sx.dumps(f))
