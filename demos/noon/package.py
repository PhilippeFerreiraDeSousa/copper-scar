#!/usr/bin/env python3
"""Freeze and archive a verified noon viewer without changing earlier packages."""
import argparse,hashlib,json,shutil,subprocess,zipfile
from pathlib import Path

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--zip',type=Path,required=True);a=ap.parse_args();out=a.out.resolve();data=json.loads((out/'data.json').read_text());dh=sha(out/'data.json');assert json.loads((out/'ui-verified.json').read_text())['data_sha256']==dh;video=json.loads((out/'video-verified.json').read_text());assert video['data_sha256']==dh and video['video_sha256']==sha(out/'pcb-loop-noon.mp4')
 sources=out/'source';sources.mkdir(exist_ok=True);repos={'small':'/Users/philippe/.codex/worktrees/d991/copper-scar','stage2':'/Users/philippe/.codex/worktrees/d991/copper-scar','medium':'/Users/philippe/.codex/worktrees/3bde/copper-scar'};source_records=[]
 for p in data['projects']:
  if p['id'] not in repos:continue
  revisions={s['source'] for s in p['states'] if s.get('source')};rev=p.get('protocol',{}).get('source_sha');revisions|={rev} if rev else set()
  for rev in sorted(revisions):
   full=subprocess.check_output(['git','-C',repos[p['id']],'rev-parse',rev],text=True).strip();dest=sources/(full+'.tar.gz')
   if not dest.exists():subprocess.run(['git','-C',repos[p['id']],'archive','--format=tar.gz','--prefix='+full+'/','-o',str(dest),full],check=True)
   source_records.append({'project':p['id'],'revision':full,'archive':str(dest.relative_to(out)),'sha256':sha(dest)})
 demo_rev=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();dest=sources/('demo-'+demo_rev+'.tar.gz');subprocess.run(['git','archive','--format=tar.gz','--prefix=demo-source/','-o',str(dest),demo_rev],check=True)
 (sources/'revisions.json').write_text(json.dumps({'demo_revision':demo_rev,'experiments':source_records},indent=2))
 for name in ['DEMO-SCRIPT.md','REPRODUCE.md','SUBMISSION-DRAFT.md']:shutil.copy2(Path(__file__).with_name(name),out/name)
 files={str(p.relative_to(out)):sha(p) for p in out.rglob('*') if p.is_file() and p.name!='package-manifest.json' and 'video-frames' not in p.parts and 'wandb' not in p.parts and p.suffix not in ['.wandb']}
 manifest={'presentation':'PCB Loop','board_size_names':['small-loop','medium-loop','large-loop'],'data_sha256':dh,'video_sha256':video['video_sha256'],'demo_revision':demo_rev,'files':files};(out/'package-manifest.json').write_text(json.dumps(manifest,indent=2))
 with zipfile.ZipFile(a.zip,'w',zipfile.ZIP_DEFLATED,compresslevel=5) as z:
  for n in files:z.write(out/n,n)
  z.write(out/'package-manifest.json','package-manifest.json')
 with zipfile.ZipFile(a.zip) as z:
  assert z.testzip() is None
  for n,h in files.items():assert hashlib.sha256(z.read(n)).hexdigest()==h,n
 result={'zip':str(a.zip),'sha256':sha(a.zip),'bytes':a.zip.stat().st_size,'files':len(files),'data_sha256':dh,'video_sha256':video['video_sha256'],'demo_revision':demo_rev};a.zip.with_suffix('.verified.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
if __name__=='__main__':main()
