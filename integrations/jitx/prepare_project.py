"""Prepare a NEW source-only project from the checkpoint; never touch native state.
Uses hash-verified local STEP assets. Does not build, route, export or launch JITX.
"""
from pathlib import Path
import argparse,hashlib,json,shutil
HERE=Path(__file__).resolve().parent

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def prepare(destination,asset_source,accepted009=False,via_proposal=False):
 destination=destination.resolve();asset_source=asset_source.resolve()
 if destination.exists() or 'designs' in destination.parts or '.jitx' in destination.parts:
  raise ValueError('Destination must be new and outside native designs/ and .jitx/')
 if via_proposal and not accepted009:raise ValueError('Via proposal requires accepted009 source inputs')
 source=HERE/'project';manifest=json.loads((source/'source-manifest.json').read_text())
 # Validate every input before creating the destination. No silent model substitution.
 for item in manifest['sources']:
  if sha(source/item['path'])!=item['sha256']:raise ValueError('Source hash mismatch: '+item['path'])
 for item in manifest['excluded_step_assets']:
  path=asset_source/item['destination']
  if not path.is_file() or sha(path)!=item['sha256']:raise ValueError('Missing/mismatched local model asset: '+str(path))
 shutil.copytree(source,destination,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
 for item in manifest['excluded_step_assets']:
  target=destination/item['destination'];target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(asset_source/item['destination'],target)
 if accepted009:shutil.copy2(HERE/'checkpoints/009/Pcbgolf-accepted.py',destination/'pcbgolf_import/Pcbgolf.py')
 if via_proposal:shutil.copy2(HERE/'checkpoints/009/stage_one_002-with-via.py',destination/'pcbgolf_import/stage_one_002.py')
 record={'accepted009_source_inputs':accepted009,'via_source_proposal_only':via_proposal,'native_state_restored':False,'source_manifest_sha256':sha(source/'source-manifest.json'),'asset_count':len(manifest['excluded_step_assets'])}
 (destination/'preparation.json').write_text(json.dumps(record,indent=2));return record

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('destination',type=Path);p.add_argument('--asset-source',required=True,type=Path);p.add_argument('--accepted009',action='store_true');p.add_argument('--via-proposal',action='store_true');a=p.parse_args();print(json.dumps(prepare(a.destination,a.asset_source,a.accepted009,a.via_proposal),indent=2))
