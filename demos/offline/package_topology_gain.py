#!/usr/bin/env python3
"""Bind intermediate connectivity proof separately from the final routed board."""
import argparse,datetime,hashlib,json,shutil
from pathlib import Path

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def verify_partitions(graph):
 before=graph['before']['pad_islands'];after=graph['after']['pad_islands'];assert set(before)==set(after)
 changed={}
 for net in before:
  a=[frozenset(i['pads']) for i in before[net]];b=[frozenset(i['pads']) for i in after[net]]
  assert set().union(*a)==set().union(*b),net
  assert all(any(group<=target for target in b) for group in a),net
  if set(a)!=set(b):changed[net]={'before':len(a),'after':len(b)}
 assert changed=={'GND':{'before':11,'after':10}}

def build(run,review_source,output,receipt=None):
 d=json.loads((run/'attempt.json').read_text());g=json.loads((review_source/'terminal-fanout-native-island-gain.json').read_text());dst=output/'topology-gain';dst.mkdir(parents=True,exist_ok=True)
 assert d['status']=='completed' and d['became_incumbent'] and d['action']['component_placement_changed'] is False
 assert d['before']['geometry_scope']==d['after']['geometry_scope']
 intermediate=run/'fanout-project/pcbgolf.kicad_pcb';final=Path(d['candidate'])/'pcbgolf.kicad_pcb';parent=Path(d['input'])/'pcbgolf.kicad_pcb'
 assert sha(parent)==g['before']['board_sha256']==d['action']['parent_board_sha256']
 assert sha(intermediate)==g['after']['board_sha256']==d['fanout_evaluation']['files']['pcbgolf.kicad_pcb']
 assert sha(final)==d['after']['files']['pcbgolf.kicad_pcb']
 project=Path(d['candidate'])/'pcbgolf.kicad_pro';assert sha(project)==g['before']['project_sha256']==g['after']['project_sha256']
 assert d['after']['unconnected']==54 and d['after']['errors']==0 and d['after']['warnings']==18 and d['after']['invariants_ok']
 assert g['changed_pad_partition_nets']=={'GND':{'before':11,'after':10}} and g['pad_connectivity_regressions']==[]
 assert {'U15.3','U15.PAD'}<=set(g['U15_after_island']['pad_names']) and set(g['U15_after_island']['zones'].values())=={'In1.Cu','In4.Cu'}
 final_graph=json.loads((review_source/'terminal-fanout-final-native-islands.json').read_text())
 verify_partitions(g);verify_partitions(final_graph)
 assert final_graph['after']['board_sha256']==sha(final) and final_graph['before']['board_sha256']==sha(parent)
 assert final_graph['changed_pad_partition_nets']=={'GND':{'before':11,'after':10}} and final_graph['pad_connectivity_regressions']==[]
 assert {'U15.3','U15.PAD'}<=set(final_graph['U15_after_island']['pad_names']) and set(final_graph['U15_after_island']['zones'].values())=={'In1.Cu','In4.Cu'}
 copies={'final-native-islands.json':review_source/'terminal-fanout-final-native-islands.json','intermediate.kicad_pcb':intermediate,'parent.kicad_pro':project,'attempt-full.json':run/'attempt.json','proposal.json':run/'terminal-fanout-proposal.json','intermediate-evaluation.json':run/'after_fanout/evaluation.json','native-island-gain.json':review_source/'terminal-fanout-native-island-gain.json','wrapper-review.md':review_source/'terminal-fanout-wrapper-review.md'}
 files={}
 for name,src in copies.items():shutil.copy2(src,dst/name);files[name]=sha(dst/name)
 h=json.loads((output/'data.json').read_text())['history'];entry=next(r for r in h if r['id']==d['attempt']);assert entry['board_sha256']==sha(final)
 observability=None
 if receipt:
  raw=receipt.read_bytes();remote=json.loads(raw);rr=next(r for r in remote['runs'] if any(x['attempt_id']==d['attempt'] for x in r['rows']));row=next(x for x in rr['rows'] if x['attempt_id']==d['attempt'])
  assert row['board_sha256']==sha(final) and [row[k] for k in ['missing_pairs','physical_errors','warnings']]==[54,0,18] and row['media_verified'] and row['weave_verified']
  (dst/'observability-verified.json').write_bytes(raw);files['observability-verified.json']=sha(dst/'observability-verified.json');observability={'url':rr['url'],'unique_completed_attempts':len(rr['rows']),'history_rows':rr['history_rows'],'raw_history_rows':rr['raw_history_rows'],'final_row':row,'note':'Repeated publications are not additional attempts. Local owner readback receipt; anonymous judge access not tested.'}
 payload=dict(observability=observability,packaged_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),attempt=d['attempt'],finished_at=d['finished_at'],parent_board_sha256=sha(parent),intermediate_board_sha256=sha(intermediate),final_board_sha256=sha(final),final_evaluation=entry['evaluation'],final_board=entry['board'],final_image=entry['image'],final_outcome={k:d['after'][k] for k in ['unconnected','errors','warnings','invariants_ok']},component_placement_changed=False,geometry_scope_unchanged=True,terminal_results=[{'terminal':t['terminal'],'state':t['state']} for t in d['fanout_result']['terminals']],intermediate_connectivity='U15.3 and U15.PAD join both original GND planes; GND pad islands 11 to 10; no old named-net pad group splits.',final_graph_verified=True,scope='Separate independent native graph checks bind both the intermediate and final board hashes. Final54/0/18, U15 ground access and no old named-net pad group splits are checked on the final board. Copper geometry is not unchanged; the product remains incomplete.',files=files)
 (dst/'summary.json').write_text(json.dumps(payload,indent=2)+'\n');(output/'gain-data.js').write_text('window.GAIN='+json.dumps(payload)+';\n')
 (dst/'README.md').write_text(f"# Completed terminal-topology gain\n\nAttempt `{d['attempt']}`, completed {d['finished_at']}. Final retained outcome54missing endpoint pairs /0physical errors /18warnings, invariants pass; product still invalid. All component poses unchanged per saved action and equal native evaluation geometry scope.\n\nIntermediate board `{sha(intermediate)}` has the independent native graph proof in native-island-gain.json: U15.3+PAD join both original GND planes, GND islands11→10, no old named-net pad group splits.\n\nFinal board `{sha(final)}` differs from that intermediate. Final counts/media bind to its own exact board and native evaluation. The separate final-native-islands.json checks this exact final board: U15.3+PAD still join both GND planes, GND remains the only changed pad partition and no old connected pad group splits.\n\nTargets J5.A2 and J8.A6 returned FAILED; U15.3 returned ROUTED. These outcomes do not prove the connector routes impossible. Wrapper review records original-rule native acceptance and copper-preservation limitations. A full600second routing budget followed the intermediate gate. This is a terminal/topology operation followed by routing, not component-placement improvement.\n")
 print(json.dumps({'attempt':d['attempt'],'intermediate_hash':sha(intermediate),'final_hash':sha(final),'metrics':[54,0,18],'scope_separated':True}))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--run',type=Path,required=True);p.add_argument('--reviews',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--receipt',type=Path);a=p.parse_args();build(a.run,a.reviews,a.output,a.receipt)
