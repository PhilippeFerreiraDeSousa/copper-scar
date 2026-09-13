"""Serial placement/topology campaign using native failures to select each action.

The incumbent is re-read after every full route. Native preview collisions and
pad partitions rank finite pose candidates; only final native checks can retain.
"""
import argparse
import collections
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import time
from datetime import datetime

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from copper_scar.tools.copperhead.stage1 import LOCAL,KIPY,copy_project,write,now
from copper_scar.tools.copperhead.records import load_record
from copper_scar.tools.copperhead.campaign_feedback import load_failures,score_preview
from copper_scar.scars.store import save_scar


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--until',required=True)
    ap.add_argument('--route-seconds',type=int,default=600)
    ap.add_argument('--catalog',type=Path,required=True)
    ap.add_argument('--preview-only',action='store_true',help='Verify finite native previews in isolated state without starting a router')
    a=ap.parse_args();deadline=datetime.fromisoformat(a.until).timestamp()
    work=LOCAL/'campaign'
    if a.preview_only:work=work/'verification'/str(int(time.time()))
    work.mkdir(parents=True,exist_ok=True)
    lock=(work/'supervisor.lock').open('a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    path=work/'state.json';state=json.loads(path.read_text()) if path.exists() else dict(decisions=[])
    state.update(selector_version='native-feedback-v2',pid=os.getpid(),status='running',worker_pid=None,until=a.until,catalog=str(a.catalog.resolve()))
    state.pop('finished_at',None)
    state.pop('reason',None)
    python=str(ROOT/'.venv/bin/python');krt=str(LOCAL/'tools/krt-venv/bin/python')
    manifest=LOCAL/'proposals/global-expanded.json';groups=json.loads(manifest.read_text())['groups']
    membership={ref:group for group,refs in groups.items() for ref in refs}

    def run(argv,label,timeout):
        started=time.time()
        with (work/(label+'.log')).open('w') as log:
            child=subprocess.Popen(argv,cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
            while child.poll() is None:
                state.update(heartbeat_at=now(),worker_pid=child.pid,phase=label);write(path,state)
                if time.time()-started>timeout or time.time()>deadline:
                    os.killpg(child.pid,signal.SIGKILL);child.wait();break
                time.sleep(2)
        state.update(worker_pid=None,heartbeat_at=now());write(path,state)
        return child.returncode

    # Wait for the existing authorized writer; never kill or duplicate it.
    with (LOCAL/'loop/runner.lock').open('a') as runner:
        while time.time()<deadline:
            try:
                fcntl.flock(runner,fcntl.LOCK_EX|fcntl.LOCK_NB);fcntl.flock(runner,fcntl.LOCK_UN);break
            except BlockingIOError:
                state.update(phase='waiting for existing native worker',heartbeat_at=now());write(path,state);time.sleep(5)

    while time.time()+a.route_seconds+240<deadline:
        catalog=json.loads(a.catalog.read_text())
        loop=json.loads((LOCAL/'loop/state.json').read_text());parent=Path(loop['best_feasibility']['candidate'])
        board_hash=hashlib.sha256((parent/'pcbgolf.kicad_pcb').read_bytes()).hexdigest()
        records=[load_record(p) for p in sorted((LOCAL/'runs').glob('stage1-*/attempt.json'))]
        for pending in state['decisions']:
            if pending.get('attempt') or not pending.get('proposal'):continue
            digest=hashlib.sha256(Path(pending['proposal']).read_bytes()).hexdigest()
            result=next((r for r in reversed(records) if r.get('action',{}).get('proposal_sha256')==digest and r['status']!='running'),None)
            if result:
                pending.update(attempt=result['attempt'],status=result['status'],finished_at=result.get('finished_at'),became_incumbent=result.get('became_incumbent',False),after={k:result.get('after',{}).get(k) for k in ('unconnected','errors','warnings')},selection_decision=result.get('selection_decision'))
                if result.get('effects'):pending['effects']=json.loads(Path(result['effects']).read_text())
        evaluation=next((r.get(k) for r in reversed(records) for k in ('after','before') if r.get(k,{}).get('files',{}).get('pcbgolf.kicad_pcb')==board_hash),None)
        if not evaluation:state.update(status='needs_attention',reason='No native report for current retained board');break
        if evaluation['unconnected']==0:state.update(status='native_connectivity_complete',reason='Full engineering qualification remains separate');break
        failures=load_failures(LOCAL/'runs');feedback_ids=[f['attempt'] for f in failures]
        # Native diagnostic scars reuse the store without fabricating official metrics.
        for failure in failures:
            save_scar(dict(schema_version='native-feedback-v1',created_at=now(),scar_id='scar_native_'+failure['attempt'],official_score=None,source_attempt=failure['attempt'],failure=failure),work/'scars'/('scar_native_'+failure['attempt']+'.json'))
        used={d.get('catalog_id') for d in state['decisions']}|{s['id'] for s in state.get('screen_failures',[]) if s['parent_board_sha256']==board_hash}
        queued=[s for s in catalog if s['id'] not in used]
        endpoint_counts=collections.Counter()
        for finding in evaluation['violations']:
            if finding['type']=='unconnected_items':
                for item in finding.get('items',[]):
                    match=re.search(r' of (R\d+) on ',item.get('description',''))
                    # C28/C32/R26/Y2/U4 form the oscillator network. Capacitors,
                    # inductors and protected oscillator parts need reviewed roles.
                    if match and match[1] not in {'R26'}:endpoint_counts[match[1]]+=1
        component_priority=[dict(ref=ref,native_missing_endpoint_pairs=count,prior_failed_attempts=[f['attempt'] for f in failures if ref in f['action'].get('refs',[])],score=count/(1+sum(ref in f['action'].get('refs',[]) for f in failures))) for ref,count in endpoint_counts.items()]
        if queued:
            specs=[spec for spec in queued if spec['kind']!='group_pose' or endpoint_counts[spec['ref']]][:2]
            for spec in queued:
                if spec['kind']=='group_pose' and not endpoint_counts[spec['ref']]:
                    state.setdefault('screen_failures',[]).append(dict(id=spec['id'],parent_board_sha256=board_hash,reason='Current retained native report no longer has a missing endpoint on this component',feedback_record_ids=[r['attempt'] for r in records if r.get('after',{}).get('files',{}).get('pcbgolf.kicad_pcb')==board_hash]))
        else:
            specs=[]
        if not specs:
            unavailable={row['id'] for row in state.get('screen_failures',[]) if row['parent_board_sha256']==board_hash}
            ranked=sorted([row for row in component_priority if 'adaptive-'+row['ref'] not in unavailable],key=lambda row:(-row['score'],row['ref']))
            specs=[dict(id='adaptive-'+row['ref'],kind='group_pose',group=membership[row['ref']],ref=row['ref'],steps='-.5,.5,-1,1,-2,2',rotations='0,90,180',component_priority=row) for row in ranked[:3]]
        index=len(state['decisions']);prefix=f'{index:03d}-{board_hash[:8]}-{int(time.time())}'
        previews=[];screened_specs=[]
        for spec in specs:
            if time.time()+a.route_seconds+180>=deadline:break
            label=prefix+'-'+spec['id'];proposal=LOCAL/'proposals'/('campaign-'+label+'.json')
            if spec['kind'] in ('terminal_fanout','via_seed'):
                action={**spec['action'],'parent_board_sha256':board_hash,'feedback_used':sorted(set(feedback_ids+spec['action']['feedback_used']))}
                if spec.get('requires_successful_seed'):
                    precedent=next((r for r in records if r['attempt']==spec['requires_successful_seed']),None)
                    proof_path=LOCAL/'runs'/spec['requires_successful_seed']/'final-seed-connectivity.json'
                    proof=json.loads(proof_path.read_text()) if proof_path.exists() else {}
                    if not precedent or not precedent.get('became_incumbent') or precedent.get('after',{}).get('unconnected',99999)>=precedent.get('before',{}).get('unconnected',0) or not proof.get('all_seed_targets_connected') or proof.get('board_sha256')!=precedent['after']['files']['pcbgolf.kicad_pcb']:
                        state.setdefault('screen_failures',[]).append(dict(id=spec['id'],parent_board_sha256=board_hash,reason='Required retained seed connection gain is not proved'));continue
                    action['strategy_evidence']=dict(attempt=precedent['attempt'],before_opens=precedent['before']['unconnected'],after_opens=precedent['after']['unconnected'],target_attachment_proof=str(proof_path),board_sha256=proof['board_sha256'],rule='Expand the successfully realized explicit-seed strategy to currently isolated connector pads only after joint native geometry revalidation.')
                if spec['kind']=='via_seed':
                    write(proposal,action);target_proof=work/(label+'-target-revalidation.json')
                    if run([KIPY,str(ROOT/'scripts/copperhead_seed_targets.py'),str(parent/'pcbgolf.kicad_pcb'),'--proposal',str(proposal),'--output',str(target_proof)],label+'-targets',60):
                        state.setdefault('screen_failures',[]).append(dict(id=spec['id'],parent_board_sha256=board_hash,reason='Native seed target binding failed'));continue
                    targets=json.loads(target_proof.read_text())
                    if not targets['kept_sites']:
                        state.setdefault('screen_failures',[]).append(dict(id=spec['id'],parent_board_sha256=board_hash,reason='No remaining isolated unseeded target',proof=str(target_proof)));continue
                    action.update(via_sites=targets['kept_sites'],nets=sorted({site['net'] for site in targets['kept_sites']}),target_revalidation=str(target_proof),excluded_seed_sites=targets['excluded_sites'])
                    action['net']=action['nets'][0]
                write(proposal,action);previews.append(dict(action=action,proposal=str(proposal),catalog_id=spec['id'],score=0,eligible=True,feedback_record_ids=feedback_ids,reason='Untried distinct topology hypothesis from measured failures; native fanout and full-route gates required'));continue
            argv=[krt,str(ROOT/'scripts/copperhead_pose_proposals.py'),str(parent),'--manifest',str(manifest),'--output',str(proposal),'--group',spec['group'],'--move-refs',spec['ref'],'--rotations',spec.get('rotations','0'),'--feedback',str(LOCAL/'loop/feedback.json'),'--allow-proxy-regression']
            if 'translation_mm' in spec:
                argv.extend(['--x-steps='+str(spec['translation_mm'][0]),'--y-steps='+str(spec['translation_mm'][1])])
            else:argv.append('--steps='+spec.get('steps','-.5,.5,-1,1,-2,2'))
            if run(argv,label+'-generate',90):
                state.setdefault('screen_failures',[]).append(dict(id=spec['id'],parent_board_sha256=board_hash,reason='No untried geometry-screened proposal',feedback_record_ids=feedback_ids));write(path,state);continue
            generated=json.loads(proposal.read_text());screened_specs.append(spec['id'])
            for n,variant in enumerate(generated['finalists'][:2]):
                if time.time()+a.route_seconds+150>=deadline:break
                action={**generated,'translation_mm':variant['translation_mm'],'rotation_deg':variant['rotation_deg'],'proxy_after':variant['proxy'],'boundary_via_policy':'preserve_existing_sites','feedback_used':sorted(set(generated['feedback_used']+feedback_ids)),'research_context':spec,'matched_control':None,'causal_qualification':'No fresh unchanged-parent control; realized pose plus full-router outcome.'}
                action['local_approach']={**generated['local_approach'],'after_mm':variant['local_approach_mm']}
                trial=work/'previews'/(label+'-'+str(n));trial.mkdir(parents=True,exist_ok=False)
                prepared=trial/'project';copy_project(parent,prepared);candidate_proposal=trial/'proposal.json';write(candidate_proposal,action)
                if run([KIPY,str(ROOT/'scripts/copperhead_apply_pose.py'),str(prepared),'--proposal',str(candidate_proposal)],label+f'-{n}-apply',90):continue
                if run([KIPY,str(ROOT/'scripts/copperhead_clear_placement_collisions.py'),str(prepared)],label+f'-{n}-collisions',300):continue
                partition_path=trial/'pad-partitions.json'
                if run([KIPY,str(ROOT/'scripts/copperhead_preview_partitions.py'),'--before',str(parent/'pcbgolf.kicad_pcb'),'--after',str(prepared/'pcbgolf.kicad_pcb'),'--output',str(partition_path)],label+f'-{n}-partitions',60):continue
                collisions=json.loads((prepared/'placement-collisions/result.json').read_text());partitions=json.loads(partition_path.read_text())
                labels=partitions['before']['pad_labels'];source_islands=[]
                for uid,pad_label in labels.items():
                    if pad_label['terminal'].split('.')[0] in action['refs']:
                        members=next(g for g in partitions['before']['groups'] if uid in g)
                        source_islands.append(dict(**pad_label,pad_uuid=uid,connected_pad_uuids=members,connected_pad_terminals=[labels[x]['terminal'] for x in members]))
                action['native_source_pad_islands']=source_islands
                rank=score_preview(action,collisions,partitions,failures)
                rank.update(action=action,proposal=str(candidate_proposal),catalog_id=spec['id'],native_preview=str(trial),collision_removals=collisions['removed'],split_groups=partitions['split_groups'])
                previews.append(rank)
        selection=work/(prefix+'-selection.json')
        eligible=[p for p in previews if p['eligible']]
        excluded=[dict(attempt=f['attempt'],refs=f['action'].get('refs'),translation_mm=f['action'].get('translation_mm'),rotation_deg=f['action'].get('rotation_deg',0),reason='Already evaluated unsuccessful pose on exact current parent') for f in failures if f['parent_board_sha256']==board_hash]
        trace=dict(parent=str(parent),parent_board_sha256=board_hash,created_at=now(),feedback_record_ids=feedback_ids,component_priority=component_priority,circuit_role_filter='Adaptive moves limited to resistors; protected oscillator R26 excluded. Capacitors/inductors require explicit reviewed placement intent.',exact_parent_exclusions=excluded,screened_specs=screened_specs,previews=previews,selection_policy='native-feedback-v2')
        if not eligible:
            write(selection,trace)
            if specs:
                for spec in specs:state.setdefault('screen_failures',[]).append(dict(id=spec['id'],parent_board_sha256=board_hash,reason='No eligible preview in this finite candidate subset',selection=str(selection)))
                write(path,state);continue
            state.update(status='needs_attention',reason='Finite candidate pool has no eligible native preview',selection=str(selection));break
        chosen=min(eligible,key=lambda p:p['score']);trace['chosen']={k:v for k,v in chosen.items() if k!='action'};write(selection,trace)
        if a.preview_only:
            state.update(status='preview_verified',reason='Native finalist previews completed without routing',selection=str(selection),preview_count=len(previews));break
        action=chosen['action'];action['campaign_selection']=str(selection);action['feedback_used']=sorted(set(action['feedback_used']+feedback_ids));proposal=LOCAL/'proposals'/('campaign-selected-'+prefix+'.json');write(proposal,action)
        decision=dict(index=index,catalog_id=chosen['catalog_id'],parent=str(parent),parent_board_sha256=board_hash,proposal=str(proposal),selection=str(selection),feedback_record_ids=feedback_ids,started_at=now());state['decisions'].append(decision);write(path,state)
        run([python,'-m','copper_scar.tools.copperhead.stage1','--source',str(parent),'--proposal',str(proposal),'--route-seconds',str(a.route_seconds),'--budget',str(a.route_seconds+420)],prefix+'-evaluate',a.route_seconds+450)
        digest=hashlib.sha256(proposal.read_bytes()).hexdigest()
        matches=[load_record(p) for p in sorted((LOCAL/'runs').glob('stage1-*/attempt.json')) if json.loads(p.read_text()).get('action',{}).get('proposal_sha256')==digest]
        if not matches:state.update(status='needs_attention',reason='No attributable native attempt');break
        result=matches[-1];decision.update(attempt=result['attempt'],status=result['status'],finished_at=now(),became_incumbent=result.get('became_incumbent',False),after={k:result.get('after',{}).get(k) for k in ('unconnected','errors','warnings')},error=result.get('error'),selection_decision=result.get('selection_decision'))
        if result.get('effects'):decision['effects']=json.loads(Path(result['effects']).read_text())
        write(path,state)
        try:
            from copper_scar.tools.copperhead.replay_service import start
            state['replay']=start('outer')
        except Exception as error:state['replay_error']=repr(error)
        if result['status']=='failed' and not any(x in result.get('error','') for x in ('Placement failed native','Fanout failed native','New via trial failed','Via seed failed native')):
            state.update(status='needs_attention',reason='Execution failure requires inspection');break
    else:state.update(status='routing_cutoff',reason='No full routing evaluation fits before the deadline')
    state.update(heartbeat_at=now(),finished_at=now(),worker_pid=None);write(path,state)
    print(json.dumps({k:state.get(k) for k in ('status','reason','finished_at')},indent=2))


if __name__=='__main__':main()
