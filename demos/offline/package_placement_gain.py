#!/usr/bin/env python3
"""Freeze the measured R37 placement-plus-routing result and its independent proof."""
import argparse,datetime,hashlib,json,shutil
from pathlib import Path

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def build(run,reviews,receipt,output):
 d=json.loads((run/'attempt.json').read_text());proof=json.loads((reviews/'r37-native-connectivity-proof.json').read_text());g=proof['graph'];poses=proof['pose_proof'];a=d['action'];dst=output/'placement-gain';dst.mkdir(parents=True,exist_ok=True)
 assert d['status']=='completed' and d['became_incumbent'] and a['refs']==['R37'] and a['translation_mm']==[-23.0,-3.0] and a['rotation_deg']==90
 final=Path(d['candidate'])/'pcbgolf.kicad_pcb';parent=Path(d['input'])/'pcbgolf.kicad_pcb'
 assert sha(final)==g['after']['board_sha256']==d['after']['files']['pcbgolf.kicad_pcb']
 assert sha(parent)==g['before']['board_sha256']==a['parent_board_sha256']
 assert [d['after'][k] for k in ['unconnected','errors','warnings','invariants_ok']]==[53,0,19,True]
 assert poses['unchanged_footprints']==244 and poses['only_R37_pose_changed'] and poses['R37_transform_verified'] and poses['all_pad_nets_layers_sizes_drills_preserved'] and poses['all_footprint_and_pad_UUIDs_preserved'] and poses['project_bytes_equal']
 before=g['before']['pad_islands'];after=g['after']['pad_islands'];assert set(before)==set(after);changes={}
 for net in before:
  old=[frozenset(i['pads']) for i in before[net]];new=[frozenset(i['pads']) for i in after[net]]
  assert set().union(*old)==set().union(*new) and all(any(x<=y for y in new) for x in old),net
  if set(old)!=set(new):changes[net]={'before':len(old),'after':len(new)}
 assert changes=={'Net-(J2-CMD)':{'before':2,'after':1}}
 assert set(after['Net-(J2-CMD)'][0]['pad_names'])=={'R37.2','J2.3','R42.2'}
 supply=next(i for i in after['+3V3'] if 'R37.1' in i['pad_names']);assert len(supply['pads'])==64
 raw=receipt.read_bytes();remote=json.loads(raw);rr=next(r for r in remote['runs'] if any(x['attempt_id']==d['attempt'] for x in r['rows']));row=next(x for x in rr['rows'] if x['attempt_id']==d['attempt'])
 assert row['board_sha256']==sha(final) and [row[k] for k in ['missing_pairs','physical_errors','warnings']]==[53,0,19] and row['media_verified'] and row['weave_verified']
 files={}
 for name,src in {'r37-native-connectivity-proof.json':reviews/'r37-native-connectivity-proof.json','attempt-full.json':run/'attempt.json','proposal.json':run/'placement-proposal.json','native-connectivity-proof.json':reviews/'r37-native-connectivity-proof.json','native-connectivity-proof.md':reviews/'r37-native-connectivity-proof.md'}.items():shutil.copy2(src,dst/name);files[name]=sha(dst/name)
 (dst/'observability-verified.json').write_bytes(raw);files['observability-verified.json']=sha(dst/'observability-verified.json')
 h=json.loads((output/'data.json').read_text())['history'];record=next(r for r in h if r['id']==d['attempt']);assert record['board_sha256']==sha(final)
 payload=dict(packaged_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),attempt=d['attempt'],finished_at=d['finished_at'],parent_board_sha256=sha(parent),final_board_sha256=sha(final),final_evaluation=record['evaluation'],translation_mm=[-23,-3],rotation_deg=90,unchanged_footprints=244,metrics=[53,0,19],changed_pad_partition=changes,independent_pose_and_graph_verified=True,warning_note='Warning count rose from18 to19; duplicate-via manufacturing warning remains in this frozen checkpoint.',qualification=proof['qualification'],observability={'url':rr['url'],'unique_completed_attempts':len(rr['rows']),'final_row':row},files=files)
 (dst/'summary.json').write_text(json.dumps(payload,indent=2)+'\n');(output/'placement-data.js').write_text('window.PLACEMENT='+json.dumps(payload)+';\n')
 (dst/'README.md').write_text(f"# R37 placement plus full-routing gain\n\nCompleted `{d['attempt']}` at {d['finished_at']}: retained54→53opens,0physical errors,19warnings. Exact finalboard `{sha(final)}`.\n\nR37 moved(-23,-3)mm and+90degrees;244other footprints and all pad identities/nets/layers/sizes/drills are preserved. Native graph proof binds that finalboard: CMD2→1islands; R37.2 joins J2.3/R42.2, R37.1 stays in the same64-pad +3V3 island, no old connected pad group splits.\n\nThis is a realized component-placement-plus600second-routing result. No fresh unchanged54-parent control exists, so it is not isolated causal proof of the placement alone. Warnings rose18→19; a duplicate-via manufacturing warning remains. No qualified product board or official score. Separate correction audit keeps043321effectively rejected while preserving its original historical promotion.\n")
 print(json.dumps({'attempt':d['attempt'],'final_hash':sha(final),'metrics':[53,0,19],'graph_pose_receipt_verified':True}))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--run',type=Path,required=True);p.add_argument('--reviews',type=Path,required=True);p.add_argument('--receipt',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();build(a.run,a.reviews,a.receipt,a.output)
