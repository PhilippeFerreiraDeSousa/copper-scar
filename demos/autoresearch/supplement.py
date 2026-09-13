#!/usr/bin/env python3
"""Build a separately labeled late native attempt; never modify the primary ZIP."""
import argparse,hashlib,json,shutil,subprocess,zipfile
from pathlib import Path
from build import asset,focus_stages

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--receipt',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--owner-repo',type=Path,required=True);ap.add_argument('--source-commit',required=True);ap.add_argument('--audit',type=Path);a=ap.parse_args();out=a.output;out.mkdir(parents=True,exist_ok=True);r=json.loads(a.receipt.read_text());assert r['status']=='completed','No completed late result';run=a.receipt.parent;stages=[]
 for name,path,ev in [('Original',run/'input/pcbgolf.kicad_pcb',r['before']),('Updated before routing',run/'placement-project/pcbgolf.kicad_pcb',r['placement_evaluation']),('After routing',Path(r['candidate'])/'pcbgolf.kicad_pcb',r['after'])]:
  stages.append({'name':name,**asset(path,ev['files']['pcbgolf.kicad_pcb'],out)})
 focus_stages(stages,out);shutil.copy2(a.receipt,out/'attempt.json')
 for name in ['final-pad-partitions.json','final-via-geometry.json','route.command.json']:
  if (run/name).exists():shutil.copy2(run/name,out/name)
 log=Path(r['candidate'])/'router.log'
 if log.exists():shutil.copy2(log,out/'router.log')
 if a.audit:shutil.copy2(a.audit,out/'independent-audit.json')
 commit=subprocess.check_output(['git','-C',str(a.owner_repo),'rev-parse',a.source_commit],text=True).strip();subprocess.run(['git','-C',str(a.owner_repo),'archive','--format=tar.gz','--prefix=late-native-source/','-o',str(out/'native-source.tar.gz'),commit],check=True)
 reproduce=out/'reproduce';reproduce.mkdir(exist_ok=True)
 for name in ['supplement.py','build.py','cad.py','model.py','summaries.py']:shutil.copy2(Path(__file__).with_name(name),reproduce/name)
 before=r['before'];after=r['after'];retained=r.get('became_incumbent',False)
 d={'separate_from_matched_N3':True,'separate_from_R89_consumer':True,'attempt':r['attempt'],'source_commit':commit,'receipt_sha256':sha(out/'attempt.json'),'before':{k:before.get(k) for k in ['unconnected','errors','warnings']},'after':{k:after.get(k) for k in ['unconnected','errors','warnings','validity_gate']},'retained':retained,'action':r.get('action'),'selection_decision':r.get('selection_decision'),'stages':stages,'qualification':'Late anchored R79 trial, outside the frozen matched comparison and R89 consumer. Retention was proxy-only: airwire distance 855.821522 → 838.189573 mm. All 366 pad groups remained identical; no electrical connection was added. The primary selected board remains unchanged. An unfinished board is not engineering-qualified.'}
 (out/'data.json').write_text(json.dumps(d,indent=2));(out/'data.js').write_text('window.SUPPLEMENT='+json.dumps(d)+';')
 html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>PCB Loop · separate late R79 trial</title><style>body{background:#091320;color:#e8f0f8;font:17px/1.6 system-ui;max-width:1500px;margin:auto;padding:28px}a{color:#8bd8ff}.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}img{width:100%;aspect-ratio:4/3;object-fit:contain;background:#07101c}select{font:inherit}.note{background:#172b42;padding:20px;margin:20px 0;border:1px solid #47617b}.hash{font:11px monospace;overflow-wrap:anywhere}@media(max-width:800px){.cards{grid-template-columns:1fr}}</style><h1>Separate late R79 anchored-pivot trial</h1><p>This trial ran after the completed N=3 comparison and the rejected R89 consumer. It does not change either frozen result.</p><div class="note" id="result"></div><label>Layer <select id="layer"><option>F.Cu</option><option>In1.Cu</option><option>In2.Cu</option><option>In3.Cu</option><option>In4.Cu</option><option>B.Cu</option></select></label><label><input id="focus" type="checkbox" checked>Focus on actual edit</label><div class="cards" id="boards"></div><p><a href="attempt.json">Complete native receipt</a> · <a href="data.json">Summary and source hashes</a> · <a href="native-source.tar.gz">Exact native source</a></p><div id="audit"></div><p id="qualification"></p><script src="data.js"></script><script>const d=window.SUPPLEMENT;document.getElementById('result').textContent=`Recorded result: ${d.before.unconnected} → ${d.after.unconnected} missing pairs; ${d.after.errors} physical errors; ${d.after.warnings} warnings. ${d.retained?'Retained only by the secondary distance proxy; no electrical improvement.':'Rejected; prior incumbent preserved.'}`;document.getElementById('qualification').textContent=d.qualification;function draw(){let layer=document.getElementById('layer').value,focus=document.getElementById('focus').checked;document.getElementById('boards').innerHTML=d.stages.map(s=>`<div><h2>${s.name}</h2><img src="${focus&&s.focus_svg?.[layer]||s.base+'/'+layer+'.svg'}"><p class="hash">${s.sha256}</p><a href="${s.board}">Exact CAD</a></div>`).join('')}document.getElementById('layer').onchange=draw;document.getElementById('focus').onchange=draw;draw();</script></html>'''
 if a.audit:html=html.replace('<div id="audit"></div>','<p><a href="independent-audit.json">Independent late-trial audit</a></p>')
 (out/'index.html').write_text(html);files={str(p.relative_to(out)):sha(p) for p in out.rglob('*') if p.is_file() and p.name!='SHA256SUMS.json' and '__pycache__' not in p.parts};(out/'SHA256SUMS.json').write_text(json.dumps(files,indent=2))
 target=out.parent/(out.name+'.zip')
 with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=5) as z:
  for name in files:z.write(out/name,name)
  z.write(out/'SHA256SUMS.json','SHA256SUMS.json')
 with zipfile.ZipFile(target) as z:
  assert z.testzip() is None
  for name,h in files.items():assert hashlib.sha256(z.read(name)).hexdigest()==h
 result={'zip':str(target),'sha256':sha(target),'bytes':target.stat().st_size,'files':len(files),'attempt':d['attempt'],'source_commit':commit,'retained':retained,'native_outcome':d['after'],'primary_package_unchanged':True};target.with_suffix('.verified.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
if __name__=='__main__':main()
