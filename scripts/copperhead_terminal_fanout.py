"""Call the installed Freerouting fanout API with explicit terminal scope."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
ap = argparse.ArgumentParser()
ap.add_argument('folder', type=Path)
ap.add_argument('--proposal', type=Path, required=True)
a = ap.parse_args()
folder = a.folder.resolve()
proposal = json.loads(a.proposal.read_text())
board = folder / 'pcbgolf.kicad_pcb'
if hashlib.sha256(board.read_bytes()).hexdigest() != proposal['parent_board_sha256']:
    raise ValueError('Fanout parent board does not match proposal')
terminals = proposal['terminals']
if not terminals or len(terminals) > 12 or len(set(terminals)) != len(terminals):
    raise ValueError('Fanout requires one to twelve distinct terminal names')
jar = Path('/private/tmp/copper-router/freerouting-mount/freerouting.app/Contents/app/freerouting-executable.jar')
jdk = ROOT / '.local/copperhead/tools/jdk25/jdk-25.0.4.1+1/Contents/Home/bin'
source = ROOT / 'scripts/native/CopperheadFanout.java'
evidence = folder / 'terminal-fanout'
evidence.mkdir()
kipy='/Users/philippe/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3.9'
subprocess.run([kipy,str(ROOT/'scripts/copperhead_terminal_targets.py'),str(board),'--proposal',str(a.proposal.resolve()),'--output',str(evidence/'terminal-bindings.json')],check=True,timeout=30)
(evidence / source.name).write_bytes(source.read_bytes())
(evidence/'input.dsn').write_bytes((folder/'pcbgolf.dsn').read_bytes())
subprocess.run([str(jdk / 'javac'), '-proc:none', '-cp', str(jar), '-d', str(evidence), str(source)], check=True, timeout=30)
rules=json.loads((folder/'pcbgolf.kicad_pro').read_text())['board']['design_settings']['rules']
edge_um=1000*rules['min_copper_edge_clearance']
hole_um=1000*rules['min_hole_clearance']
command = [str(jdk / 'java'), '-Djava.awt.headless=true', '-Xmx2g', '-cp', str(evidence)+':'+str(jar), 'CopperheadFanout', str(folder/'pcbgolf.dsn'), str(folder/'pcbgolf.ses'), str(evidence/'result.json'), str(edge_um), str(hole_um), *terminals]
(evidence/'provenance.json').write_text(json.dumps(dict(command=command, java_source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(), jar_sha256=hashlib.sha256(jar.read_bytes()).hexdigest(), input_dsn_sha256=hashlib.sha256((folder/'pcbgolf.dsn').read_bytes()).hexdigest()), indent=2))
with (evidence/'engine.log').open('w') as log:
    subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, check=True, timeout=30*len(terminals)+30)
(evidence/'output.ses').write_bytes((folder/'pcbgolf.ses').read_bytes())
print((evidence/'result.json').read_text())
