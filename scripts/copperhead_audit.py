"""Snapshot audit of finalized lower-level action records; no CAD mutations."""
from pathlib import Path
import json,hashlib
from datetime import datetime,timezone
from copper_scar.real import design_files
from copper_scar.tools.copperhead.effects import compare,missing_by_net
root=Path(__file__).resolve().parents[1];local=root/'.local/copperhead';out=local/'audits'/datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S');out.mkdir(parents=True)
rows=[]
for p in sorted((local/'runs').glob('stage1-*/attempt.json')):
 a=json.loads(p.read_text())
 if a.get('status') not in ('completed','failed'):continue
 row=dict(attempt=a['attempt'],status=a['status'],gaps=[],checks={});run=p.parent
 for key,path in [('before',run/'input'),('after',Path(a['candidate']))]:
  e=a.get(key)
  if not e:row['gaps'].append(key+' evaluation absent');continue
  row['checks'][key+'_file_hashes_match']=design_files(path)==e['files']
  report=Path(e['report']);raw=json.loads(report.read_text());row['checks'][key+'_native_report_exists']=report.is_file();row.setdefault('native_versions',{})[key]=raw.get('kicad_version')
 if a.get('placement_evaluation'):
  q=run/'placement-project'
  row['placement_snapshot_origin']='original'
  if not q.exists():
   q=local/'audits/reconstructed-placement'/a['attempt'];row['placement_snapshot_origin']='reconstructed and matched to original hash'
  row['checks']['placement_snapshot_matches']=q.exists() and design_files(q)==a['placement_evaluation']['files']
  if not row['checks']['placement_snapshot_matches']:row['gaps'].append('intermediate placement board not preserved')
 row['checks']['archived_tool_hashes_match']=bool(a.get('tool_source_hashes')) and all((run/'tool-source'/n).exists() and hashlib.sha256((run/'tool-source'/n).read_bytes()).hexdigest()==v for n,v in a.get('tool_source_hashes',{}).items())
 if not a.get('tool_source_hashes'):row['gaps'].append('early v1 attempt predates controller-source archiving')
 row['checks']['score_not_claimed']=a.get('official_score') is None and not a.get('validity_gate',False)
 row['checks']['commands_have_timing']=all(all(k in d for k in ('argv','started_at','elapsed_seconds','returncode')) for q in run.rglob('*.command.json') for d in [json.loads(q.read_text())])
 if a.get('before') and a.get('after'):
  row['same_design_hash']=a['before']['design_sha256']==a['after']['design_sha256']
  if row['same_design_hash'] and a.get('diagnostic_improved'):row['gaps'].append('identical board labeled diagnostic improvement from measurement variation')
  action=a.get('action',{});selected=action.get('nets') or ([action['net']] if action.get('net') else [])
  effects=compare(run/'input/pcbgolf.kicad_pcb',Path(a['candidate'])/'pcbgolf.kicad_pcb',selected)
  effects['missing_before']=missing_by_net(a['before']);effects['missing_after']=missing_by_net(a['after'])
  (out/(a['attempt']+'-effects.json')).write_text(json.dumps(effects,indent=2));row['changed_unselected_nets']=effects['changed_unselected_nets'];row['moves']=effects['moves']
  row['effects']=str(out/(a['attempt']+'-effects.json'))
 if 'incumbent_before' not in a or 'incumbent_after' not in a:row['gaps'].append('incumbent linkage is reconstructable history, not explicit per-attempt fields')
 rows.append(row)
(out/'audit.json').write_text(json.dumps(dict(cutoff=datetime.now(timezone.utc).isoformat(),attempts=rows),indent=2));print(out)
print(json.dumps(dict(attempts=len(rows),failed_checks=[(r['attempt'],k) for r in rows for k,v in r['checks'].items() if not v],same_design_improvements=[r['attempt'] for r in rows if r.get('same_design_hash') and any('identical' in g for g in r['gaps'])],wider_scope_actions=[dict(attempt=r['attempt'],nets=r.get('changed_unselected_nets')) for r in rows if r.get('changed_unselected_nets')]),indent=2))
