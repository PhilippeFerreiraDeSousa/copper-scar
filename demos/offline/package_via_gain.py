#!/usr/bin/env python3
"""Freeze the new-via plus full-routing result and independently reviewed evidence."""
import argparse, hashlib, json, shutil
from pathlib import Path

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def verify(dst):
 summary=json.loads((dst/'summary.json').read_text())
 for name,digest in summary['files'].items(): assert sha(dst/name)==digest,name
 attempt=json.loads((dst/'original-attempt.json').read_text());graph=json.loads((dst/'final-pad-partitions.json').read_text());geometry=json.loads((dst/'final-via-geometry.json').read_text())
 assert attempt['status']=='completed' and attempt['became_incumbent'] is True
 assert [attempt['after'][k] for k in ['unconnected','errors','warnings','invariants_ok']]==[52,0,18,True]
 assert summary['final_board_sha256']==attempt['after']['files']['pcbgolf.kicad_pcb']==graph['after']['board_sha256']==geometry['after_sha256']
 assert summary['parent_board_sha256']==attempt['before']['files']['pcbgolf.kicad_pcb']==graph['before']['board_sha256']==geometry['before_sha256']
 old=[frozenset(x) for x in graph['before']['groups']];new=[frozenset(x) for x in graph['after']['groups']]
 assert set().union(*old)==set().union(*new) and all(any(x<=y for y in new) for x in old)
 assert len(old)-len(new)==1 and graph['before']['project_sha256']==graph['after']['project_sha256']
 assert geometry['existing_via_geometry_preserved'] and not geometry['missing_existing']
 assert geometry['added']==[{'geometry':['GND',137238000,82442700,450000,200000,'F.Cu','B.Cu'],'count':1}]
 assert geometry['new_vias_use_only_allowed_definitions']
 independent=json.loads((dst/'independent-proof.json').read_text());ig=independent['geometry']
 assert independent['attempt']==summary['attempt'] and independent['native_opens']==[53,52] and [independent['drc_errors'],independent['drc_warnings']]==[0,18]
 assert ig['before']['board_sha256']==summary['parent_board_sha256'] and ig['after']['board_sha256']==summary['final_board_sha256']
 assert ig['before']['via_count']==668 and ig['after']['via_count']==669 and ig['new_native_via_count']==1
 assert ig['all_existing_via_net_site_drill_span_and_all_layer_diameters_preserved'] and ig['all_footprint_pad_identities_poses_nets_layers_unchanged'] and ig['project_bytes_equal']
 assert independent['changed_pad_partition_nets']=={'GND':{'before':10,'after':9}} and not independent['old_pad_group_splits'] and independent['joined_terminal']=='R66.1'
 remote=json.loads((dst/'observability-verified.json').read_text());row=next(row for run in remote['runs'] for row in run['rows'] if row['attempt_id']==summary['attempt'])
 assert row['board_sha256']==summary['final_board_sha256'] and [row[k] for k in ['missing_pairs','physical_errors','warnings']]==[52,0,18] and row['media_verified'] and row['weave_verified']
 scope=json.loads((dst/'terminal-scope-correction.json').read_text())
 assert scope['historical_proposal_nets']==attempt['action']['nets'] and scope['actual_terminal_nets']==['GND','CAN0_H','CH4_D_P'] and scope['original_proposal_preserved']
 return summary

def build(run,proof,report,receipt,out):
 attempt=json.loads((run/'attempt.json').read_text());dst=out/'via-gain';dst.mkdir(parents=True,exist_ok=True)
 board=Path(attempt['candidate'])/'pcbgolf.kicad_pcb';parent=Path(attempt['input'])/'pcbgolf.kicad_pcb'
 assert sha(board)==attempt['after']['files']['pcbgolf.kicad_pcb'] and sha(parent)==attempt['before']['files']['pcbgolf.kicad_pcb']
 files={}
 sources={name:run/name for name in ['final-pad-partitions.json','final-via-geometry.json','terminal-fanout-proposal.json','terminal-scope-correction.json']}
 sources.update({'original-attempt.json':run/'attempt.json','independent-proof.json':proof,'independent-report.md':report,'observability-verified.json':receipt})
 sources['via-definition-final-audit.json']=proof
 independent=json.loads(proof.read_text());evidence_index={}
 for raw_path in independent['evidence']:
  path=Path(raw_path);name='independent-'+path.name;sources[name]=path;evidence_index[raw_path]=name
 for name,path in sources.items():shutil.copy2(path,dst/name);files[name]=sha(dst/name)
 (dst/'independent-evidence-index.json').write_text(json.dumps(evidence_index,indent=2)+'\n');files['independent-evidence-index.json']=sha(dst/'independent-evidence-index.json')
 assert sha(board) in proof.read_text() and sha(parent) in proof.read_text()
 record=next(r for r in json.loads((out/'data.json').read_text())['history'] if r['id']==attempt['attempt'])
 assert record['board_sha256']==sha(board) and record['retained'] is True
 summary=dict(attempt=attempt['attempt'],finished_at=attempt['finished_at'],parent_board_sha256=sha(parent),final_board_sha256=sha(board),final_evaluation=record['evaluation'],metrics=[52,0,18],files=files,qualification='Actual additional via geometry plus full routing; no fresh unchanged53 control. Full fabrication profile remains unverified; product board incomplete.')
 (dst/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');verify(dst)
 (out/'via-data.js').write_text('window.VIA='+json.dumps(summary)+';\n')
 (dst/'README.md').write_text(f"# New via geometry plus full routing\n\nCompleted `{attempt['attempt']}` retains52opens,0physical errors,18warnings. Final board `{sha(board)}`; parent `{sha(parent)}`.\n\nThe completed board contains one new GND through-via at137.238,82.4427mm, diameter0.45mm/drill0.20mm, F.Cu to B.Cu. All668previous via geometries remain and no old connected pad group splits. Original project bytes remain unchanged. All eight targeted fanouts failed. The actual new via and R66.1 join occur during the following full600second routing budget; GND missing pairs fall9to8. Detailed independent artifacts are mapped by independent-evidence-index.json.\n\n[Independent final audit](independent-report.md), [machine-readable audit](independent-proof.json), [owner geometry proof](final-via-geometry.json), [pad partitions](final-pad-partitions.json), [publication receipt](observability-verified.json).\n\nNo fresh unchanged53-parent control exists: this is not isolated causal proof of via diameter. The full fabrication profile remains unverified and the product board is incomplete.\n\nThe original proposal mislabeled J8.A6 as CH2_SBU2. The separate [target-scope correction](terminal-scope-correction.json) identifies actual CH4_D_P and preserves the [immutable attempt](original-attempt.json). The preceding R71 trial is rejected at56/0/21 and remains in the history.\n")
 print(json.dumps(summary))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--run',type=Path,required=True);p.add_argument('--proof',type=Path,required=True);p.add_argument('--report',type=Path,required=True);p.add_argument('--receipt',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();build(a.run,a.proof,a.report,a.receipt,a.output)
