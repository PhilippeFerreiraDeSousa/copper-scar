#!/usr/bin/env python3
"""Refresh the live mirror only when owner checkpoint metadata changes."""
import argparse,hashlib,subprocess,sys,time
from pathlib import Path

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args();small=Path('/Users/philippe/.codex/worktrees/d991/copper-scar/.local/small-loop');medium=Path('/Users/philippe/.codex/worktrees/3bde/copper-scar/.local/medium-loop');paths=[small/'stage2/live-status.json',small/'stage2/final-accepted/frozen.json',medium/'accepted-best/handoff.json',medium/'observability/verified.json',medium/'stage2/compact-v1/live-status.json',medium/'stage2/compact-v1/events.json',medium/'stage2/status.json',medium/'stage2/continuation-01/events.json'];last=None
 while True:
  fingerprint=hashlib.sha256(b''.join(p.read_bytes() for p in paths if p.exists())).hexdigest()
  if fingerprint!=last:
   subprocess.run([sys.executable,str(Path(__file__).with_name('build.py')),'--small',str(small),'--medium',str(medium),'--out',a.out,'--medium-completed','baseline-parity','relay-group-01'],check=True);last=fingerprint
  time.sleep(10)
if __name__=='__main__':main()
