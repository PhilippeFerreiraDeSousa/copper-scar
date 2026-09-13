"""Repeat whole-project KiCad DRC on independent allowlisted support-file copies."""
from pathlib import Path
import argparse
import collections
import hashlib
import json
import shutil
import subprocess
import time
KC='/Users/philippe/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli'

def check(source,out):
    out.mkdir(parents=True,exist_ok=False);project=out/'project';project.mkdir()
    for p in source.iterdir():
        if p.is_file() and (p.suffix in ('.kicad_pcb','.kicad_pro','.kicad_sch','.kicad_sym','.lib','.kicad_dru') or p.name in ('fp-lib-table','sym-lib-table')):shutil.copy2(p,project/p.name)
        elif p.is_dir() and p.name.endswith('.pretty'):shutil.copytree(p,project/p.name)
    boards=list(project.glob('*.kicad_pcb'))
    if len(boards)!=1:raise ValueError('Expected one board')
    runs=[]
    for i in range(2):
        report=out/f'drc-{i}.json';start=time.monotonic()
        proc=subprocess.run([KC,'pcb','drc','--format','json','--refill-zones','--output',str(report.resolve()),str(boards[0].resolve())],capture_output=True,text=True,timeout=120)
        (out/f'drc-{i}.stdout').write_text(proc.stdout);(out/f'drc-{i}.stderr').write_text(proc.stderr)
        if proc.returncode or not report.exists():raise RuntimeError('DRC failed to produce a report')
        data=json.loads(report.read_text());runs.append({'opens':len(data['unconnected_items']),
            'counts':dict(collections.Counter(v['severity'] for v in data['violations'])),
            'by_type':dict(collections.Counter(v['type'] for v in data['violations'])),
            'ignored_checks':data['ignored_checks'],'elapsed_s':time.monotonic()-start})
    if {k:v for k,v in runs[0].items() if k!='elapsed_s'}!={k:v for k,v in runs[1].items() if k!='elapsed_s'}:raise ValueError('Repeated DRC disagreed')
    result={'source_board_sha256':hashlib.sha256(boards[0].read_bytes()).hexdigest(),'runs':runs,'repeated_agreement':True,'zones_refilled_in_memory':True,'board_saved':False,'scope':'all objects/terminals in supplied project copy; geometry probes have omitted external boundaries'}
    (out/'summary.json').write_text(json.dumps(result,indent=2));return result

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('source',type=Path);p.add_argument('output',type=Path);a=p.parse_args();print(json.dumps(check(a.source,a.output),indent=2))
