#!/usr/bin/env python3
"""Check a frozen package, preserve the prior snapshot, and update a stable directory.
Files and the ZIP replace atomically; the directory itself is never renamed.
"""
import argparse, hashlib, json, os, shutil, tempfile, zipfile
from pathlib import Path

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def replace_file(source,destination):
 destination.parent.mkdir(parents=True,exist_ok=True)
 fd,tmp=tempfile.mkstemp(prefix='.demo-incoming-',dir=destination.parent)
 try:
  with os.fdopen(fd,'wb') as stream,source.open('rb') as incoming:
   shutil.copyfileobj(incoming,stream);stream.flush();os.fsync(stream.fileno())
  os.replace(tmp,destination)
 finally:
  if os.path.exists(tmp):os.unlink(tmp)

p=argparse.ArgumentParser();p.add_argument('staged',type=Path);p.add_argument('canonical',type=Path);p.add_argument('--backup',type=Path,required=True);a=p.parse_args()
stage=a.staged.resolve();canonical=a.canonical.resolve();archive=stage.parent/'demo-final-offline.zip';receipt_path=archive.with_suffix('.zip.json');receipt=json.loads(receipt_path.read_text())
assert stage!=canonical and canonical.is_dir() and not a.backup.exists()
assert archive.stat().st_size==receipt['bytes'] and sha(archive)==receipt['sha256']
with zipfile.ZipFile(archive) as z:
 assert z.testzip() is None
 for name in z.namelist():
  path=Path(name);assert path.parts[0]=='demo-final' and '..' not in path.parts
  if not name.endswith('/'):assert sha(stage.joinpath(*path.parts[1:]))==hashlib.sha256(z.read(name)).hexdigest(),name
assert json.loads((stage/'browser-QA.json').read_text())['status']=='pass'
assert json.loads((stage/'package-QA.json').read_text())['status']=='pass'
shutil.copytree(canonical,a.backup)
inode=canonical.stat().st_ino
# Publish UI entrypoints and inventories after their referenced files.
last={'data.json','data.js','via-data.js','index.html','SHA256SUMS.json','SOURCE-CHECKPOINT.json','METRICS-AS-OF.json'}
files=[f for f in stage.rglob('*') if f.is_file()]
for source in sorted(files,key=lambda f:(f.name in last,str(f.relative_to(stage)))):
 destination=canonical/source.relative_to(stage)
 if not destination.exists() or sha(source)!=sha(destination):replace_file(source,destination)
assert canonical.stat().st_ino==inode
for source in files:assert sha(source)==sha(canonical/source.relative_to(stage))
public_zip=canonical.parent/'demo-final-offline.zip';replace_file(archive,public_zip)
receipt['archive']=str(public_zip)
fd,tmp=tempfile.mkstemp(prefix='.receipt-',dir=stage.parent)
with os.fdopen(fd,'w') as f:json.dump(receipt,f,indent=2);f.write('\n')
try:replace_file(Path(tmp),public_zip.with_suffix('.zip.json'))
finally:os.unlink(tmp)
print(json.dumps(dict(**receipt,canonical_directory_inode_preserved=True,prior_package=str(a.backup),all_files_match_frozen_zip=True)))
