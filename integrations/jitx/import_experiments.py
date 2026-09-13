"""Bounded, provenance-preserving JITX import experiments. Never modifies reference."""
from pathlib import Path
import json, shutil, hashlib, uuid, subprocess, os, signal
import sexpdata as sx
SRC=Path('/Users/philippe/dev/PCBGolf')
BASE=Path('/Users/philippe/dev/copper-scar-jitx')
RUN=BASE/'runs/import-ab-20260912'
CAND=BASE/'candidates/import-ab-20260912'
CLI='/Users/philippe/dev/copper-scar-jitx/.venv/bin/jitx'
KC='/Users/philippe/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli'
def children(d,k):return [x for x in d if isinstance(x,list) and x and str(x[0])==k]
def one(d,k):return children(d,k)[0]
def parse(p):return sx.loads(p.read_text())
def write(p,d):p.write_text(sx.dumps(d)+'\n')
def hashes(root):return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file() and '.git' not in p.parts}
def call(name,args,cwd,timeout=45):
 p=subprocess.Popen(args,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True,text=True)
 try:out,err=p.communicate(timeout=timeout);expired=False
 except subprocess.TimeoutExpired:
  os.killpg(p.pid,signal.SIGTERM);out,err=p.communicate();expired=True
 r=dict(argv=args,cwd=str(cwd),exit_code=p.returncode,timed_out=expired,stdout=out,stderr=err)
 (RUN/(name+'.json')).write_text(json.dumps(r,indent=2));print(name,p.returncode,out[:400],err[:200],flush=True);return r
def output(name):
 p=RUN/name; (p/'converted').mkdir(parents=True);(p/'converted/__init__.py').touch()
 (p/'pyproject.toml').write_text('[project]\nname="converted"\nversion="0.1"\nrequires-python=">=3.12"\ndependencies=["jitx==4.4.0","jitxlib-standard==4.4.0"]\n');return p
if __name__=='__main__':
 RUN.mkdir(parents=True,exist_ok=False);CAND.mkdir(parents=True,exist_ok=False)
 before=hashes(SRC);(RUN/'reference-hashes.json').write_text(json.dumps(before,indent=2))
 for name in ['board-only','hierarchy']:
  shutil.copytree(SRC,CAND/name,ignore=shutil.ignore_patterns('.git','*.kicad_sch') if name=='board-only' else shutil.ignore_patterns('.git'))
 a=CAND/'board-only'
 call('a-directory',[CLI,'project','import','kicad',str(a),'--output',str(output('a-output'))],RUN)
 call('a-project',[CLI,'project','import','kicad',str(a/'pcbgolf.kicad_pro'),'--output',str(output('a-project-output'))],RUN)
 b=CAND/'hierarchy'; pro=json.loads((b/'pcbgolf.kicad_pro').read_text());orig=pro['schematic']['top_level_sheets'];root=str(uuid.uuid5(uuid.NAMESPACE_URL,'copper-scar/pcbgolf/import-ab-root'))
 wrapper=f'(kicad_sch (version 20250114) (generator "eeschema") (uuid "{root}") (paper "A4") (lib_symbols)'
 mapping=[]
 for i,meta in enumerate(orig):
  old=b/meta['filename'];dest='power.kicad_sch' if i==0 else meta['filename'];d=parse(old); old_uuid=one(d,'uuid')[1];inst=meta['uuid'];path=f'/{root}/{inst}'
  for sym in children(d,'symbol'):
   for project in children(one(sym,'instances'),'project'):
    for item in children(project,'path'):item[1]=path
  d=[x for x in d if not(isinstance(x,list) and x and str(x[0])=='sheet_instances')]
  d.append([sx.Symbol('sheet_instances'),[sx.Symbol('path'),path,[sx.Symbol('page'),str(i+2)]]]);write(b/dest,d)
  mapping.append(dict(file=dest,original=meta['filename'],file_uuid=old_uuid,instance_uuid=inst,path=path))
  wrapper+=f'''(sheet (at {20+i*35} 30) (size 30 20) (fields_autoplaced)
   (stroke (width 0) (type default)) (fill (color 0 0 0 0)) (uuid "{inst}")
   (property "Sheetname" "{meta['name']}" (at {20+i*35} 29 0) (effects (font (size 1.27 1.27)) (justify left bottom)))
   (property "Sheetfile" "{dest}" (at {20+i*35} 51 0) (effects (font (size 1.27 1.27)) (justify left top)))
   (instances (project "pcbgolf" (path "/{root}" (page "{i+2}")))))'''
 wrapper+='(sheet_instances (path "/" (page "1"))))';(b/'pcbgolf.kicad_sch').write_text(wrapper)
 pro['schematic']['top_level_sheets']=[dict(filename='pcbgolf.kicad_sch',name='PCBGolf',uuid=root)]
 pro['sheets']=[[root,'PCBGolf']]+[[m['instance_uuid'],orig[i]['name']] for i,m in enumerate(mapping)]
 (b/'pcbgolf.kicad_pro').write_text(json.dumps(pro,indent=2));(RUN/'hierarchy-mapping.json').write_text(json.dumps(mapping,indent=2))
 # Adjust schematic path context only on the copied board; pad/geometry/net data unchanged.
 pcb=parse(b/'pcbgolf.kicad_pcb')
 for fp in children(pcb,'footprint'):
  oldfile=one(fp,'sheetfile')[1];m=next(m for m in mapping if m['original']==oldfile)
  one(fp,'path')[1]=m['path']+one(fp,'path')[1];one(fp,'sheetfile')[1]=m['file']
 write(b/'pcbgolf.kicad_pcb',pcb)
 call('b-netlist',[KC,'sch','export','netlist','--format','kicadxml','--output',str(b/'pcbgolf.net'),str(b/'pcbgolf.kicad_sch')],b)
 call('b-erc',[KC,'sch','erc','--format','json','--output',str(RUN/'hierarchy-erc.json'),str(b/'pcbgolf.kicad_sch')],b)
 call('b-import',[CLI,'project','import','kicad',str(b),'--output',str(output('b-output'))],RUN)
 assert hashes(SRC)==before
