#!/usr/bin/env python3
"""Rebrand presentation text without changing frozen experiment evidence or video."""
import argparse,hashlib,json,zipfile
from pathlib import Path
TAGLINE='An agent-driven PCB optimization loop that proposes layout changes, autoroutes the board, and learns from verified results.'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 with zipfile.ZipFile(a.source) as z:files={n:z.read(n) for n in z.namelist()}
 original=json.loads(files['package-manifest.json']);changed=[]
 for name,body in list(files.items()):
  if name in ['index.html','two-level-autoresearch/index.html','demo-material/SUBMISSION-DRAFT.md','demo-material/DEMO-SCRIPT.md']:
   s=body.decode().replace('Copper Scar','PCB Loop')
   if name=='index.html':
    s=s.replace('<h1>Improve the board.<br>Measure the optimizer.</h1>',f'<h1>PCB Loop</h1><p>{TAGLINE}</p>')
    s=s.replace('<hr>','<p class="small">Presentation branding updated to PCB Loop. The unchanged recorded video and historical evidence retain the original Copper Scar name. Repository and W&amp;B identifiers are unchanged.</p><hr>')
   if name.endswith('SUBMISSION-DRAFT.md'):
    lines=s.splitlines();lines=[('One-line description: '+TAGLINE) if x.startswith('One-line description:') else x for x in lines];s='\n'.join(lines)+'\n\nPresentation name: PCB Loop. Repository and W&B identifiers remain copper-scar. The unchanged recorded video retains the earlier Copper Scar branding.\n'
   files[name]=s.encode();changed.append(name)
 provenance={'presentation_name':'PCB Loop','tagline':TAGLINE,'original_zip_sha256':sha(a.source.read_bytes()),'changed_files':changed,'experiment_evidence_unchanged':True,'video_unchanged':True,'repository_and_wandb_identifiers_unchanged':True}
 files['branding-provenance.json']=json.dumps(provenance,indent=2).encode();manifest={**original,'branding':provenance,'files':{n:sha(b) for n,b in files.items() if n!='package-manifest.json'}};files['package-manifest.json']=json.dumps(manifest,indent=2).encode()
 a.output.parent.mkdir(parents=True,exist_ok=True)
 with zipfile.ZipFile(a.output,'w',zipfile.ZIP_DEFLATED,compresslevel=5) as z:
  for n,b in files.items():z.writestr(n,b)
 with zipfile.ZipFile(a.output) as z:
  assert z.testzip() is None
  for n,h in manifest['files'].items():assert sha(z.read(n))==h,n
 result={**provenance,'zip':str(a.output),'zip_sha256':sha(a.output.read_bytes()),'bytes':a.output.stat().st_size,'files':len(manifest['files'])};a.output.with_suffix('.branding-verified.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
if __name__=='__main__':main()
