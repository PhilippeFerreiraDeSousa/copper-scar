"""Executable negative controls against source-rule KiCad validation."""
from roundtrip import *
from collections import Counter
D=BASE/'runs/stage1/differential-v3';D.mkdir(exist_ok=False)
source=CAND/'hierarchy';cases=[]
def check(name,board,sch=False):
 out=D/name;shutil.copytree(source,out,ignore=shutil.ignore_patterns('*.lck','*.kicad_prl'));target=out/('pcbgolf.kicad_sch' if sch else 'pcbgolf.kicad_pcb')
 if not sch:write(target,board)
 else:
  changed=0
  for f in out.glob('*.kicad_sch'):
   d=parse(f)
   for lib in children(d,'lib_symbols'):
    def visit(x):
     nonlocal changed
     if not isinstance(x,list) or not x:return
     if str(x[0])=='pin' and len(x)>2 and str(x[1]) in ['passive','input','bidirectional']:
      x[1]=sx.Symbol('output');changed+=1
     for y in x:visit(y)
    visit(lib)
   write(f,d)
  assert changed>0
 report=out/'report.json';args=[KC,'sch' if sch else 'pcb','erc' if sch else 'drc','--format','json','--output',str(report),str(target)];t=time.monotonic();r=subprocess.run(args,capture_output=True,text=True,timeout=60);elapsed=time.monotonic()-t
 assert r.returncode==0 and report.exists(),r.stderr
 d=json.loads(report.read_text());v=d.get('violations',[]) if not sch else [v for sh in d['sheets'] for v in sh['violations']]
 result={'case':name,'elapsed_seconds':elapsed,'exit_code':r.returncode,'counts':dict(Counter(x['type'] for x in v)),'native_equivalence':'not demonstrated; structural pin model and capture unchanged for ERC metadata mutation' if sch else 'not tested'};cases.append(result);print(result,flush=True)
board=parse(source/'pcbgolf.kicad_pcb');check('control',board)
mut=copy.deepcopy(board);mut.append(sx.loads('(segment (start 200 200) (end 210 200) (width 0.05) (layer "F.Cu") (net "GND") (uuid "b195c52e-721d-4f8e-9d65-48c612990001"))'));check('thin-track',mut)
mut=copy.deepcopy(board)
for s in ['(segment (start 200 200) (end 210 200) (width 0.2) (layer "F.Cu") (net "GND") (uuid "b195c52e-721d-4f8e-9d65-48c612990002"))','(segment (start 205 195) (end 205 205) (width 0.2) (layer "F.Cu") (net "+3V3") (uuid "b195c52e-721d-4f8e-9d65-48c612990003"))']:mut.append(sx.loads(s))
for x,y,net,ref in [(200,200,'GND','TEST_A'),(205,195,'+3V3','TEST_B')]:
 mut.append(sx.loads(f'(footprint "Test" (layer "F.Cu") (at {x} {y}) (property "Reference" "{ref}" (at 0 0) (layer "F.SilkS") (effects (font (size 1 1)))) (pad "1" smd rect (at 0 0) (size 1 1) (layers "F.Cu") (net "{net}")))'))
check('cross-net-short',mut)
check('conflicting-output-pin-types',board,True)
assert cases[1]['counts'].get('track_width',0)>cases[0]['counts'].get('track_width',0)
assert cases[2]['counts'].get('tracks_crossing',0)>cases[0]['counts'].get('tracks_crossing',0)
assert cases[3]['counts'].get('pin_to_pin',0)>0
(D/'results.json').write_text(json.dumps(cases,indent=2))
