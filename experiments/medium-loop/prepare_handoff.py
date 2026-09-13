"""Package accepted copper with complete original models and explicit populated headers."""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess,sys
import sexpdata as sx
from campaign import command,KIPY,KICAD,ROOT,write,sha,now
from audit import nodes,first,audit
ap=argparse.ArgumentParser();ap.add_argument('base',type=Path);ap.add_argument('source',type=Path);ap.add_argument('--parent',default='relay-group-01');ap.add_argument('--output',default='accepted-handoff');a=ap.parse_args();base=a.base.resolve();src=a.source.resolve();parent=base/a.parent;out=base/a.output;out.mkdir();assert json.loads((parent/'evaluation.json').read_text())['accepted']
for filename in ['pcbgolf.kicad_pcb','pcbgolf.kicad_pro','pcbgolf.kicad_sch','pcbgolf.kicad_sym','sym-lib-table','fp-lib-table'] :shutil.copy2(parent/filename,out/filename)
shutil.copytree(parent/'pcbgolf.pretty',out/'pcbgolf.pretty');shutil.copy2(base/'input/circuit.json',out/'circuit.json');(out/'models').mkdir();shutil.copy2(ROOT/'experiments/medium-loop/assets/M20-9980446-nominal.step',out/'models')
p=out/'pcbgolf.kicad_pcb';d=sx.loads(p.read_text());model=sx.loads('(model "${KIPRJMOD}/models/M20-9980446-nominal.step" (offset (xyz 0 0 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0)))');coverage=[]
for f in nodes(d,'footprint'):
 ref=next(x[2] for x in nodes(f,'property') if x[1]=='Reference')
 if ref.startswith('J1'):
  f[:]=[v for v in f if not(isinstance(v,list) and v and str(v[0])=='model')];f.append(model)
 for m in nodes(f,'model'):
  rel=m[1].replace('${KIPRJMOD}/','');dest=out/rel
  if not dest.exists():dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src/rel,dest)
  coverage.append({'reference':ref,'model':rel,'sha256':sha(dest)})
p.write_text(sx.dumps(d));lib=out/'pcbgolf.pretty/2X04.kicad_mod';ld=sx.loads(lib.read_text());ld[:]=[v for v in ld if not(isinstance(v,list) and v and str(v[0])=='model')];ld.append(model);lib.write_text(sx.dumps(ld))
project=(out/'pcbgolf.kicad_pro').read_bytes();command([KIPY,ROOT/'experiments/medium-loop/native_stage.py','audit',out],out,'audit');(out/'pcbgolf.kicad_pro').write_bytes(project)
command([KICAD,'pcb','drc','--schematic-parity','--format','json','-o',out/'drc.json',out/'pcbgolf.kicad_pcb'],out,'drc');command([KICAD,'sch','erc','--format','json','-o',out/'erc.json',out/'pcbgolf.kicad_sch'],out,'erc');result=audit(out,out/'circuit.json',src)
old=json.loads((parent/'native-audit.json').read_text());new=json.loads((out/'native-audit.json').read_text());assert old['vias']==new['vias'],'Model-only handoff changed routed via identity/geometry';assert old['identity']==new['identity'];assert old['wire_length_mm']==new['wire_length_mm'];assert not any(s['violations'] for s in json.loads((out/'erc.json').read_text())['sheets']);assert result['accepted'];write(out/'evaluation.json',result)
command([KICAD,'pcb','export','svg','--layers','F.Cu,B.Cu,F.SilkS,Edge.Cuts','--mode-single','--page-size-mode','2','--exclude-drawing-sheet','-o',out/'board.svg',out/'pcbgolf.kicad_pcb'],out,'render');command(['/opt/homebrew/bin/rsvg-convert','-w','1400','-o',out/'board.png',out/'board.svg'],out,'raster')
manifest={'schema':1,'stage':'stage1-accepted-medium','created_at':now(),'source_sha':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'parent':str(parent),'parent_board_sha256':sha(parent/'pcbgolf.kicad_pcb'),'board_sha256':sha(p),'accepted':True,'evaluation':result,'erc_violations':0,'populated_header':'Harwin M20-9980446','header_source':'https://www.harwin.com/products/M20-9980446','model_kind':'datasheet nominal body/pins, not detailed vendor STEP','header_dimensions_mm':[10.16,5.08,11.64],'header_height_above_pcb_mm':8.64,'header_tail_mm':3,'header_model_generator_source_commit':'ad7f166b11fba43eb0c9de16fa626d21686a8fe7','models':coverage,'model_reference_count':len(set(v['reference'] for v in coverage)),'via_identity_preserved':True,'stage_two_score':None,'not_original_challenge_submission':True,'files':{str(f.relative_to(out)):sha(f) for f in out.rglob('*') if f.is_file() and f.suffix not in ['.log','.kicad_prl']}}
write(out/'handoff.json',manifest);print(json.dumps({'accepted':True,'path':str(out),'models':manifest['model_reference_count'],'board_sha256':manifest['board_sha256']}))
