#!/usr/bin/env python3
"""Refresh the live mirror only when owner checkpoint metadata changes."""
import argparse,hashlib,subprocess,sys,time
from pathlib import Path

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args();small=Path('/Users/philippe/.codex/worktrees/d991/copper-scar/.local/small-loop');medium=Path('/Users/philippe/.codex/worktrees/3bde/copper-scar/.local/medium-loop');paths=[small/'stage2/live-status.json',small/'stage2/final-accepted/frozen.json',medium/'accepted-best/handoff.json',medium/'observability/verified.json',medium/'stage2/compact-v1/live-status.json',medium/'stage2/compact-v1/events.json',medium/'stage2/status.json',medium/'stage2/continuation-01/events.json'];last=None
 while True:
  paths += [p for p in list(Path(__file__).parent.glob('*.py'))+list((Path(__file__).resolve().parents[1]/'live').glob('*')) if p.is_file() and p not in paths]
  paths += [p for p in medium.glob('stage2/*/events.json') if p not in paths]
  paths += [p for p in Path('/Users/philippe/.codex/worktrees/dc68/copper-scar/.local/large-loop/v1').glob('*/completed.json') if p not in paths]
  paths += [p for p in [Path('/Users/philippe/.codex/worktrees/dc68/copper-scar/.local/large-loop/v1/live-status.json'),Path('/Users/philippe/dev/copper-scar-demo/.local/copperhead/full-spacious/v1/family-manifest.json')] if p not in paths]
  fingerprint=hashlib.sha256(b''.join(p.read_bytes() for p in paths if p.exists())).hexdigest()
  if fingerprint!=last:
   result=subprocess.run([sys.executable,str(Path(__file__).with_name('build.py')),'--small',str(small),'--medium',str(medium),'--out',a.out,'--medium-completed','baseline-parity','relay-group-01'],check=False)
   if result.returncode==0:last=fingerprint
  time.sleep(10)
if __name__=='__main__':main()
