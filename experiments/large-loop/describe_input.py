"""Write explicit populated BOM, boundary pinout and resolvable model inventory."""
import argparse,csv,hashlib,json
from pathlib import Path
from audit import nodes,first
import sexpdata as sx
ap=argparse.ArgumentParser();ap.add_argument('input',type=Path);ap.add_argument('output',type=Path);a=ap.parse_args();p=a.input.resolve();a.output.mkdir(parents=True,exist_ok=False);d=sx.loads((p/'large-loop.kicad_pcb').read_text());rows=[];models=[]
for f in nodes(d,'footprint'):
 props={v[1]:v[2] for v in nodes(f,'property')};ref=props['Reference'];attr=[str(x) for x in first(f,'attr')[1:]] if nodes(f,'attr') else []
 rows.append({'reference':ref,'value':props['Value'],'mpn':props.get('MPN',''),'footprint':f[1],'populated':not any(x in attr for x in ['dnp','exclude_from_bom','exclude_from_pos_files']),'model_contract':'Generic populated 2x4 2.54mm visualization, not manufacturer-qualified envelope' if ref=='J4' or ref.startswith('J10') else 'Original source model'})
 for m in nodes(f,'model'):
  rel=m[1].replace('${KIPRJMOD}/','');fpath=p/rel;models.append({'reference':ref,'path':rel,'exists':fpath.exists(),'sha256':hashlib.sha256(fpath.read_bytes()).hexdigest() if fpath.exists() else None})
with (a.output/'bom.csv').open('w') as stream:
 w=csv.DictWriter(stream,fieldnames=list(rows[0]));w.writeheader();w.writerows(sorted(rows,key=lambda v:v['reference']))
m=json.loads((p/'circuit.json').read_text());record={'component_count':len(rows),'all_populated':all(v['populated'] for v in rows),'model_reference_count':len(set(v['reference'] for v in models)),'all_model_files_resolve':all(v['exists'] for v in models),'models':models,'external_boundary_pinout':m['external_header_pinout'],'source_hashes':m['source_hashes'],'constraints':'Original native project rules unchanged; source footprint errors retained in acceptance.'};(a.output/'input-contract.json').write_text(json.dumps(record,indent=2));print({k:record[k] for k in ['component_count','all_populated','model_reference_count','all_model_files_resolve']})
