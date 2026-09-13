import json,shutil
from pathlib import Path

def extend(data,out,board,read,sha):
 large=Path('/Users/philippe/.codex/worktrees/dc68/copper-scar/.local/large-loop/v1/live-status.json')
 if large.exists():data['status']['large']=read(large)
 manifest=Path('/Users/philippe/dev/copper-scar-demo/.local/copperhead/full-spacious/v1/family-manifest.json')
 if manifest.exists():
  m=read(manifest);dst=out/'evidence/original';dst.mkdir(parents=True,exist_ok=True);shutil.copy2(manifest,dst/'family-manifest.json');states=[]
  for i,e in enumerate(m['completed_events']):
   receipt=Path(e['receipt']);target=dst/str(i);target.mkdir(exist_ok=True);shutil.copy2(receipt,target/'result.json');r=read(receipt)
   if not e.get('after_board'):continue
   if e.get('saved_native_report'):shutil.copy2(e['saved_native_report'],target/'drc.json')
   for before in [True,False]:
    b=board(Path(e['before_board' if before else 'after_board']),out);
    if not before and (e.get('after_board_sha256') or r.get('board_sha256')):assert b['sha256']==(e.get('after_board_sha256') or r['board_sha256'])
    opens=e['before_missing'] if before else e.get('after_missing',e.get('attempted_missing'));errors=e.get('physical_errors',r.get('errors'));ev={'drc_opens':opens,'errors':errors,'feasibility_cost':opens+errors,'accepted':False,'via_count':r.get('via_count') if not before else None}
    states.append({'title':('Spacious arm · re-layout + outline expansion' if e['kind']=='fullboard_routing_baseline' else e['kind'].replace('_',' '))+((' · independent arm input' if e['kind'] in ['fullboard_routing_baseline','prior_floorplan_control'] else ' · source checkpoint') if before else ' · completed routing'),'phase':'Stage 1 · independent baseline arm' if e['kind'] in ['fullboard_routing_baseline','prior_floorplan_control'] else 'Stage 1 · completed placement trial','board':b,'evaluation':ev,'action':{'kind':e['kind'],'baseline_arm':i,'scale':e.get('scale'),'pose_count':m['component_count'],'center_mm':e.get('center_mm'),'control_missing':e.get('control_missing'),'rationale':e.get('reason'),'before_missing':e['before_missing'],'after_missing':e.get('after_missing',e.get('attempted_missing'))},'retained':False if before else e.get('diagnostic_retained',e.get('retained',False)),'source':m['source_commit'],'receipt':str((target/'result.json').relative_to(out)),'qualification':('Independent baseline arm, not sequential placement convergence. ' if e['kind'] in ['fullboard_routing_baseline','prior_floorplan_control'] else 'Completed placement trial; source receipt decides retention. ')+'51 physical errors remain disqualifying. Historical repaired-geometry 44-open epoch is separate.'})
  preview=manifest.parent/'uniform-120/input/uniform-scale.json'
  if preview.exists() and not any('uniform' in e['kind'] for e in m['completed_events']):
   a=read(preview);f=preview.parent/'pcbgolf.kicad_pcb';shutil.copy2(preview,dst/'uniform-scale.json')
   if f.exists():states.append({'title':'Uniform placement scaling ×1.2 · input preview','phase':'Input preview · no routed result','board':board(f,out),'evaluation':None,'action':{'kind':'uniform_position_and_outline_scale','scale':a['scale'],'center_nm':a['center_nm'],'before_outline_mm':a['before_outline_mm'],'after_outline_mm':a['after_outline_mm'],'maximum_transform_residual_nm':a['maximum_transform_residual_nm'],'pose_count':len(a['poses'])},'retained':None,'source':m['source_commit'],'receipt':str((dst/'uniform-scale.json').relative_to(out)),'qualification':'True ×1.2 transform of 245 component anchors about (170,102.5)mm. Physical dimensions, angles and sides unchanged. Outline140×105→168×126mm. Saved input only; no routed result or validity claim.'})
  data['projects'].append({'id':'original','title':'original-full · 245 components / 297 nets','stage':'Stage 1 · invalid diagnostic search','summary':'Re-layout + outline expansion, not uniform scaling. Matched 600-second baseline arms: spacious 499 → 140 opens; prior floorplan 499 → 111. Both retain 51 physical errors. Historical repaired-geometry 44-open result is a separate epoch.','states':states,'protocol':m,'decision':m.get('baseline_comparison'),'limitations':m['qualification']})
  op=m.get('current_operation',{});status=read(Path(op['status'])) if op.get('status') and Path(op['status']).exists() else {};data['status']['original']={'running':status.get('status') in ['routing','running'],'current_operation':op,'producer_status':status,'retained_opens':min(e['after_missing'] for e in m['completed_events'] if 'after_missing' in e)}
 return data
