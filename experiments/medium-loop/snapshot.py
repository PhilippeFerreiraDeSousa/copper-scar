"""Create replay manifest and native per-layer previews without altering CAD."""
from pathlib import Path
import argparse,json,subprocess,hashlib
from campaign import KICAD,write,sha
ap=argparse.ArgumentParser();ap.add_argument('base',type=Path);a=ap.parse_args();base=a.base.resolve();out=base/'replay';out.mkdir(exist_ok=True);records=[json.loads((base/'baseline-parity/completed.json').read_text()),json.loads((base/'relay-group-01/completed.json').read_text())]+json.loads((base/'policy-pilot/records.json').read_text());states=[]
for record in records:
 folder=Path(record['folder']);sid=record['id'];assets={};dest=out/sid;dest.mkdir(exist_ok=True)
 for phase,filename in [('preview','preview.kicad_pcb'),('final','pcbgolf.kicad_pcb')]:
  for layer,layers in [('front','F.Cu,F.SilkS,Edge.Cuts'),('back','B.Cu,B.SilkS,Edge.Cuts'),('both','F.Cu,B.Cu,F.SilkS,Edge.Cuts')]:
   svg=dest/f'{phase}-{layer}.svg';subprocess.run([KICAD,'pcb','export','svg','--layers',layers,'--mode-single','--page-size-mode','2','--exclude-drawing-sheet','-o',str(svg),str(folder/filename)],check=True,capture_output=True);png=svg.with_suffix('.png');subprocess.run(['/opt/homebrew/bin/rsvg-convert','-w','1400','-o',str(png),str(svg)],check=True,capture_output=True);assets[phase+'-'+layer]={'svg':str(svg),'png':str(png),'sha256':sha(png)}
 states.append({'size_family':'medium-loop','optimization_stage':'stage-one-feasibility','id':sid,'record':record,'assets':assets})
manifest={'schema':1,'size_family':'medium-loop','source_commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'states':states,'best_handoff':str(base/'accepted-best/handoff.json'),'first_feasible_handoff':str(base/'accepted-handoff/handoff.json'),'policy_decision':json.loads((base/'policy-pilot/outcome.json').read_text()),'observability_receipt':str(base/'observability/verified.json'),'jitx':{'workspace':str(base/'jitx'),'design':'medium_loop.design.MediumLoopInput','status':'build succeeded; native acceptance remains authoritative','build_log':str(base/'jitx-build-cwd.log')}};write(out/'manifest.json',manifest);print(out/'manifest.json')
