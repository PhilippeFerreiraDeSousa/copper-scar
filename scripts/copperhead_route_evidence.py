"""Extract exported routing scope and termination without changing CAD or DSN."""
from pathlib import Path
import argparse,hashlib,json,re
import sexpdata

def evidence(folder):
 path=folder/'pcbgolf.dsn';raw=path.read_text()
 # Specctra's quote-character declaration is not a Lisp string.
 d=sexpdata.loads(raw.replace('(string_quote ")','(string_quote quote)'))
 def children(node,name):return [x for x in node if isinstance(x,list) and x and str(x[0])==name]
 structure=children(d,'structure')[0];network=children(d,'network')[0];placement=children(d,'placement')[0]
 nets=children(network,'net');pins=sum(len(x)-1 for n in nets for x in children(n,'pins'))
 refs=[str(y[1]) for x in children(placement,'component') for y in children(x,'place')]
 logs=(folder/'router.log').read_text();execution=json.loads((folder/'execution.json').read_text()) if (folder/'execution.json').exists() else {}
 result={'dsn_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'exported_nets':len(nets),'exported_net_names':[str(n[1]) for n in nets],'exported_assigned_pins':pins,'exported_footprints':len(refs),'footprint_refs':refs,'layers':[str(x[1]) for x in children(structure,'layer')],'planes':[sexpdata.dumps(x) for x in children(structure,'plane')],'via_definitions':[sexpdata.dumps(x) for x in children(structure,'via')],'rules':[sexpdata.dumps(x) for x in children(structure,'rule')],'net_filter':None,'all_exported_nets_eligible':True,'per_net_attempt_coverage':'not exposed by this backend; eligible scope does not prove every net was searched','autoroute_started':'Auto-routing stage started' in logs or 'Auto-routing pass' in logs,'fanout_started':'Fanout stage started' in logs,'termination':'effort_limit' if 'timeout' in logs.lower() or execution.get('timeout') else 'returned' if execution else 'running','elapsed_seconds':execution.get('elapsed_seconds'),'backend_summary_lines':[x for x in logs.splitlines() if 'stage completed' in x or 'Job ' in x and 'finished' in x], 'rule_caveat':'KiCad export emits 50um smd_smd exception alongside200um clearance. Original native rule files remain unchanged and determine final acceptance.'}
 return result
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('folder',type=Path);a=ap.parse_args();r=evidence(a.folder);(a.folder/'routing-coverage.json').write_text(json.dumps(r,indent=2));print(json.dumps({k:v for k,v in r.items() if k not in ['exported_net_names','footprint_refs','planes']},indent=2))
