"""Reapply candidate via eligibility after export and verify the loaded engine rule."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from copper_scar.tools.copperhead.routing_options import SMALL,context,dsn_context
from copperhead_via_definition import add_definition

ap=argparse.ArgumentParser();ap.add_argument('folder',type=Path);ap.add_argument('--phase',required=True);a=ap.parse_args();folder=a.folder.resolve()
options=json.loads((folder/'routing-options.json').read_text());expected=context(options['allowed_via_options'],options['constraint_scope'])
path=folder/'pcbgolf.dsn';before=path.read_text();rules=json.loads((folder/'pcbgolf.kicad_pro').read_text())['board']['design_settings']['rules']
after,change=add_definition(before,rules) if SMALL in options['allowed_via_options'] else (before,dict(existing_geometry_rewritten=False))
actual=dsn_context(after,options['constraint_scope']);assert actual['digest']==expected['digest'],'Exported use_via differs from declared routing options'
evidence=folder/'via-definition'/a.phase;evidence.mkdir(parents=True,exist_ok=False)
(evidence/'before.dsn').write_text(before);(evidence/'after.dsn').write_text(after);path.write_text(after)
jar=Path('/private/tmp/copper-router/freerouting-mount/freerouting.app/Contents/app/freerouting-executable.jar');jdk=ROOT/'.local/copperhead/tools/jdk25/jdk-25.0.4.1+1/Contents/Home/bin';source=ROOT/'scripts/native/CopperheadViaRules.java'
(evidence/source.name).write_bytes(source.read_bytes());subprocess.run([str(jdk/'javac'),'-proc:none','-cp',str(jar),'-d',str(evidence),str(source)],check=True,timeout=30)
with (evidence/'engine-readback.log').open('w') as log:
 subprocess.run([str(jdk/'java'),'-Djava.awt.headless=true','-Xmx2g','-cp',str(evidence)+':'+str(jar),'CopperheadViaRules',str(path),str(evidence/'loaded-via-rules.json')],stdout=log,stderr=subprocess.STDOUT,check=True,timeout=45)
loaded=json.loads((evidence/'loaded-via-rules.json').read_text());assert loaded['classes'] and not loaded['routing_started']
assert all(sorted(set(row['via_rule_padstacks']))==expected['allowed_via_options'] for row in loaded['classes']),'Engine loaded via rule differs from declared options'
report=dict(realization_context=actual,engine_rule_verified=True,loaded_via_rules=loaded,dsn_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),routing_options_sha256=hashlib.sha256((folder/'routing-options.json').read_bytes()).hexdigest(),java_source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),jar_sha256=hashlib.sha256(jar.read_bytes()).hexdigest(),change=change)
(evidence/'realization.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
