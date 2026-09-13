"""Normalize only legacy netclass metadata in an external qualification copy.
JITX add_net names containing parentheses need quoting before KiCad can parse.
The modern exported project remains the rule authority; no geometry is edited.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import shutil
import sexpdata as sx

def normalize(source,out):
    shutil.copytree(source,out)
    pcb=next(out.glob('*.kicad_pcb'));raw=pcb.read_text();quoted=[]
    def quote(m):
        name=m.group(2).strip()
        if name.startswith('"'):return m.group(0)
        quoted.append(name);return m.group(1)+json.dumps(name)+')'
    text=re.sub(r'(?m)^(\s*\(add_net )(.+)\)\s*$',quote,raw)
    board=sx.loads(text)
    geometry=[v for v in board if not(isinstance(v,list) and v and str(v[0])=='net_class')]
    canonical=sx.dumps(geometry);pcb.write_text(canonical)
    assert sx.loads(pcb.read_text())==geometry
    report={'raw_board_sha256':hashlib.sha256(raw.encode()).hexdigest(),'output_board_sha256':hashlib.sha256(pcb.read_bytes()).hexdigest(),
            'quoted_add_net_count':len(quoted),'removed_legacy_netclasses':len(board)-len(geometry),
            'all_non_netclass_parsed_fields_exactly_preserved':True,'native_managed_state_edited':False}
    (out/'normalization.json').write_text(json.dumps(report,indent=2))
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('source',type=Path);p.add_argument('output',type=Path);a=p.parse_args();normalize(a.source,a.output)
