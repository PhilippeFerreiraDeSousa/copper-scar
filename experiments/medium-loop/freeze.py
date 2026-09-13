"""Copy a completed incumbent, independently rerun native gates, and freeze evidence."""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess,sys
from campaign import KICAD,KIPY,ROOT,command,write,now
from audit import audit
from stage2 import score
ap=argparse.ArgumentParser();ap.add_argument('source',type=Path);ap.add_argument('out',type=Path);ap.add_argument('--manifest',type=Path,required=True);ap.add_argument('--reference',type=Path,required=True);ap.add_argument('--family',required=True);a=ap.parse_args();src=a.source.resolve();f=a.out.resolve();assert not f.exists();expected=json.loads((src/'score.json').read_text());assert expected['valid'];shutil.copytree(src,f,ignore=shutil.ignore_patterns('router-userdata','*.lck','*.kicad_prl'));before=hashlib.sha256((f/'pcbgolf.kicad_pcb').read_bytes()).hexdigest();project=(f/'pcbgolf.kicad_pro').read_bytes()
command([KICAD,'pcb','drc','--schematic-parity','--format','json','-o',f/'drc.json',f/'pcbgolf.kicad_pcb'],f,'independent-drc');command([KICAD,'sch','erc','--format','json','-o',f/'erc.json',f/'pcbgolf.kicad_sch'],f,'independent-erc');command([KIPY,ROOT/'experiments/medium-loop/native_stage.py','audit',f],f,'independent-connectivity');assert (f/'pcbgolf.kicad_pro').read_bytes()==project
result=audit(f,a.manifest,a.reference);assert result['accepted'];command([KICAD,'pcb','export','step','-f','-o',f/'independent-assembly.step',f/'pcbgolf.kicad_pcb'],f,'independent-step');original_step=f/'assembly.step';old=original_step.read_bytes();original_step.write_bytes((f/'independent-assembly.step').read_bytes());measured=score(f);original_step.write_bytes(old)
assert measured['valid'] and abs(measured['official_formula_score']-expected['official_formula_score'])<1e-7
assert hashlib.sha256((f/'pcbgolf.kicad_pcb').read_bytes()).hexdigest()==before==expected['board_sha256']
# Score's STEP hash describes the independent export. Preserve that exact export
# as the authoritative frozen assembly alongside the earlier execution export.
(f/'execution-assembly.step').write_bytes(old);original_step.write_bytes((f/'independent-assembly.step').read_bytes())
receipt={'size_family':a.family,'stage':'stage2','frozen_at':now(),'source_candidate':str(src),'source_sha':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'independent_native_acceptance':True,'score':measured,'board_unchanged':True,'full_project':'pcbgolf.kicad_pro','model_qualification':'Complete nominal component models; header body/pin extrema from manufacturer dimensions; no powered hardware or official challenge submission claim.'};write(f/'frozen.json',receipt)
hashes={str(p.relative_to(f)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(f.rglob('*')) if p.is_file()};write(f/'sha256-manifest.json',hashes);print(json.dumps(receipt))
