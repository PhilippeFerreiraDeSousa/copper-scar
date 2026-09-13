"""Snapshot completed score events into separate, immutable replay assets."""
from pathlib import Path
import argparse,json,subprocess
from campaign import KICAD,sha,write
ap=argparse.ArgumentParser();ap.add_argument('base',type=Path);ap.add_argument('--name',required=True);a=ap.parse_args();base=a.base.resolve();root=base/'stage2';out=root/a.name;out.mkdir();events=[]
for p in root.glob('*/events.json'):events.extend(json.loads(p.read_text()))
events.sort(key=lambda e:e['finished_at']);states=[]
for e in events:
 f=Path(e['folder']);sid=f.parent.name+'-'+f.name;dest=out/sid;dest.mkdir();assets={}
 for phase,filename in [('preview','preview.kicad_pcb'),('final','pcbgolf.kicad_pcb')]:
  for layer,layers in [('front','F.Cu,F.SilkS,Edge.Cuts'),('back','B.Cu,B.SilkS,Edge.Cuts'),('both','F.Cu,B.Cu,F.SilkS,Edge.Cuts')]:
   svg=dest/f'{phase}-{layer}.svg';subprocess.run([KICAD,'pcb','export','svg','--layers',layers,'--mode-single','--page-size-mode','2','--exclude-drawing-sheet','-o',str(svg),str(f/filename)],check=True,capture_output=True);png=svg.with_suffix('.png');subprocess.run(['/opt/homebrew/bin/rsvg-convert','-w','1400','-o',str(png),str(svg)],check=True,capture_output=True);assets[phase+'-'+layer]={'svg':str(svg),'png':str(png),'sha256':sha(png)}
 states.append({'id':sid,'size_family':'medium-loop','stage':2,'event':e,'assets':assets})
valid=[(e['result']['official_formula_score'],e['folder']) for e in events if e['result']['valid']];write(out/'manifest.json',{'schema':1,'size_family':'medium-loop','stage':2,'stage1_replay':str(base/'replay/manifest.json'),'lineage':json.loads((root/'lineage.json').read_text()),'baseline':json.loads((root/'baseline/score.json').read_text()),'states':states,'best_completed':min(valid) if valid else None,'qualification':'Snapshot of completed events only; later experiments remain separate. Global retained score is minimum valid score seen, even when exploratory studies run independently.'});print(out/'manifest.json')
