"""Durable feasibility loop over real KiCad projects.

The controller is intentionally small and explicit. Diagnostic progress is not
PCBGolf score or engineering qualification. All attempts survive rejection.
"""
from __future__ import annotations
import argparse
import collections
import fcntl
import hashlib
import json
import os
import re
from pathlib import Path
import shutil
import signal
import subprocess
import time
import uuid
from datetime import datetime, timezone
from copper_scar.real import design_files, design_digest, board_inventory, native_report
from copper_scar.loop.weave_trace import WeaveTracer
from .metrics import measure, ordering, VERSION
from .effects import compare as compare_effects, missing_by_net, geometry_scope

ROOT = Path(__file__).resolve().parents[3]
LOCAL = ROOT / '.local/copperhead'
KICAD = '/Users/philippe/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli'
KIPY = '/Users/philippe/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3.9'
PYTHON = str(ROOT / '.venv/bin/python')
REFERENCE = ROOT / '.local/pcbgolf-source'
POLICY = 'native-feasibility-v9'
DEADLINE = None

def now(): return datetime.now(timezone.utc).isoformat()
def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + '.tmp')
    temp.write_text(json.dumps(data, indent=2) + '\n')
    os.replace(temp, path)
def support(path):
    return {k:v for k,v in design_files(path).items() if k != 'pcbgolf.kicad_pcb'}
def copy_project(source, dest):
    # Runtime/report files are retained in their originating attempt, not reused.
    shutil.copytree(source, dest, ignore=shutil.ignore_patterns('.git', '*.lck',
                    '*-backups', 'router-userdata', '*.ses', '*.dsn', 'router.log',
                    'router-result.json', 'execution.json', 'board.svg', 'board.png',
                    'erc.json', 'reference.net.xml', 'reference-check.json',
                    'stage1-drc.json', 'placement-collisions', 'terminal-fanout', 'krt-*.json', 'placement-search.json', 'ground-escape.json'))
def command(argv, directory, label, timeout):
    if DEADLINE is not None:
        remaining = DEADLINE-time.monotonic()
        if remaining <= 0: raise TimeoutError('Explicit campaign wall-time budget exhausted')
        timeout = min(timeout, remaining)
    started = time.monotonic()
    record = dict(argv=argv, started_at=now(), timeout_seconds=timeout)
    with (directory/(label+'.stdout')).open('w') as out, (directory/(label+'.stderr')).open('w') as err:
        p = subprocess.Popen(argv,cwd=ROOT,stdout=out,stderr=err,start_new_session=True)
        record.update(pid=p.pid,state='running',heartbeat_at=now())
        write(directory/(label+'.command.json'),record)
        last_beat=0
        while p.poll() is None:
            if time.monotonic()-started >= timeout:
                os.killpg(p.pid,signal.SIGKILL);p.wait()
                record.update(returncode=None,timed_out=True,state='timed_out');break
            if time.monotonic()-last_beat>=5:
                record.update(heartbeat_at=now(),elapsed_seconds=time.monotonic()-started)
                write(directory/(label+'.command.json'),record);last_beat=time.monotonic()
            try:p.wait(timeout=1)
            except subprocess.TimeoutExpired:pass
        else:record.update(returncode=p.returncode,timed_out=False,state='completed')
        record['heartbeat_at']=now()
    record['elapsed_seconds'] = time.monotonic()-started
    write(directory/(label+'.command.json'), record)
    return record

def priority(result):
    """Diagnostic priority only; invalid designs never receive official score."""
    return ordering(result['search_cost'],result['invariants_ok'])

def classify_action(initial, after):
    same=after['design_sha256']==initial['design_sha256']
    decreased=priority(after)<priority(initial)
    improved=not same and decreased
    label=('measurement_variation' if same and priority(after)!=priority(initial)
           else 'no_change' if same else 'improvement' if improved
           else 'no_progress' if priority(after)==priority(initial) else 'regression')
    return same,decreased,improved,label

def choose_action(result, feedback, scope):
    all_feedback=feedback
    if result.get('geometry_scope'):
        feedback=[f for f in feedback if f.get('geometry_scope')==result['geometry_scope']]
    if not result['invariants_ok']:
        return dict(kind='stop', reason='Reference/constraint invariant failure requires a scoped repair proposal')
    if result['counts'].get('shorting_items',0) or result['counts'].get('clearance',0):
        return dict(kind='stop', reason='Copper regression requires targeted repair; do not reroute blindly')
    if result['unconnected']:
        previous=[f for f in feedback if f.get('scope')==scope and f.get('action')=='route_continue']
        ground=[f for f in feedback if f.get('scope')==scope and f.get('action')=='ground_escape']
        backend=[f for f in feedback if f.get('scope')==scope and f.get('action')=='krt_reconnect']
        if any(f.get('scope')==scope and f.get('action')=='krt_reconnect' and f.get('classification')!='execution_failure' for f in all_feedback):
            tried={f.get('action_parameters',{}).get('net') for f in backend}
            missing=collections.Counter()
            for v in result['violations']:
                if v['type']=='unconnected_items':
                    missing.update({n for item in v.get('items',[]) for n in re.findall(r'\[([^\]]+)\]',item.get('description',''))})
            options=[(count,net) for net,count in missing.items() if net not in tried]
            if options:
                count,net=max(options)
                return dict(kind='krt_reconnect',net=net,reason=f'{count} remaining native pairs on {net}; bounded alternative backend after validated pilot and placement experiment',hypothesis='Repair the largest untreated missing-net scope at unchanged rules; retain incumbent if this action regresses',feedback_used=[f['attempt'] for f in backend[-2:]])
        ground_missing=sum(v['type']=='unconnected_items' and any('[GND]' in i.get('description','') for i in v.get('items',[])) for v in result['violations'])
        if ground_missing>=5 and len(previous)>=2 and (not ground or ground[-1]['diagnostic_improved']):
            return dict(kind='ground_escape',reason=f'{ground_missing} native missing endpoint pairs involve GND after repeated bulk routing',hypothesis='Add at most 20 screened through-via GND escapes outside component pads, then reject any native copper regression',feedback_used=[f['attempt'] for f in (ground[-1:]+previous[-2:])])
        stagnant=sum(not f.get('diagnostic_improved',False) for f in previous[-2:])
        if len(previous)>=2 and stagnant==2:
            return dict(kind='stop', reason='Two measured routing attempts without diagnostic improvement; placement/backend proposal needed',feedback_used=[f['attempt'] for f in previous[-2:]])
        return dict(kind='route_continue',reason='Connectivity remains incomplete without native short/clearance regressions',hypothesis='Continue routing from retained copper, preserving rules, placement and planes',feedback_used=[f['attempt'] for f in previous[-2:]])
    return dict(kind='stop', reason='Routing complete; remaining native/model/engineering requirements need explicit closure before Stage 2')

def evaluate(candidate, run, label, frozen_support):
    d=run/label;d.mkdir()
    before=design_files(candidate)
    invocations={}
    jobs=[('netlist',[KICAD,'sch','export','netlist','--format','kicadxml','-o',str(candidate/'reference.net.xml'),str(candidate/'pcbgolf.kicad_sch')]),
          ('erc',[KICAD,'sch','erc','--format','json','-o',str(candidate/'erc.json'),str(candidate/'pcbgolf.kicad_sch')]),
          ('drc',[KICAD,'pcb','drc','--format','json','--schematic-parity','--refill-zones','-o',str(d/'drc.json'),str(candidate/'pcbgolf.kicad_pcb')]),
          ('reference',[PYTHON,str(ROOT/'scripts/copperhead_check_reference.py'),str(REFERENCE),str(candidate)])]
    for name,argv in jobs:invocations[name]=command(argv,d,name,120)
    erc=native_report(json.loads((candidate/'erc.json').read_text()),'erc',invocations['erc']['returncode'],'pcbgolf.kicad_sch')
    drc=native_report(json.loads((d/'drc.json').read_text()),'drc',invocations['drc']['returncode'],'pcbgolf.kicad_pcb')
    raw=json.loads((d/'drc.json').read_text());ref=json.loads((candidate/'reference-check.json').read_text())
    stable=before==design_files(candidate)
    invariant=(all(v['returncode']==0 for v in invocations.values()) and stable and support(candidate)==frozen_support and ref['pin_partition_equivalent'] and ref['whole_project_erc_coverage'] and ref['all_physical_pad_uuid_identity_preserved'])
    items=raw['violations']+raw['schematic_parity'];counts=dict(collections.Counter(v['type'] for v in items))
    inventory=board_inventory(candidate/'pcbgolf.kicad_pcb')
    result=dict(geometry_scope=geometry_scope(candidate/'pcbgolf.kicad_pcb'),native_kicad_version=raw.get('kicad_version'),search_cost=measure(raw),design_sha256=design_digest(before),invariants_ok=invariant,counts=counts,unconnected=len(raw['unconnected_items']),errors=sum(v['severity']=='error' for v in items),warnings=sum(v['severity']=='warning' for v in items),erc_ok=erc['ok'],native_cad_ok=erc['ok'] and drc['ok'] and invariant,missing_model_assignments=inventory['missing_models'],engineering_review='unknown',hardware_proof='unknown',assembly_completeness='unknown',validity_gate=False,stage2_enabled=False,official_score=None,report=str(d/'drc.json'),files=before,violations=items+raw['unconnected_items'])
    # This implementation has no authority to invent engineering acceptance.
    write(d/'evaluation.json',result)
    return result

def validate_proposal(proposal, result):
    if proposal.get('kind') not in ('krt_reconnect','placement_repair','placement_group','placement_trial','global_expand','group_pose','terminal_fanout') or not isinstance(proposal.get('net'),str):
        raise ValueError('Only a scoped native repair proposal is supported')
    if not result['invariants_ok'] or result['errors']:
        raise ValueError('Backend proposal requires preserved invariants and no physical errors')
    if not all(proposal.get(k) for k in ('reason','hypothesis','feedback_used')):
        raise ValueError('Proposal requires rationale and measured feedback references')
    if proposal['kind']=='placement_group':
        if not proposal.get('refs') or len(set(proposal['refs']))<2 or not proposal.get('anchors') or not proposal.get('nets'):
            raise ValueError('Group proposal requires explicit members, interface anchors and net scope')
    if proposal['kind'] in ('global_expand','group_pose'):return proposal
    needle='['+proposal['net']+']'
    if not any(v['type']=='unconnected_items' and any(needle in i.get('description','') for i in v.get('items',[])) for v in result['violations']):
        raise ValueError('Proposed net has no current native missing connection')
    return proposal

def execute(source, iterations, route_seconds, budget, proposal=None, legacy_inner=False):
    global DEADLINE
    DEADLINE=time.monotonic()+budget
    (LOCAL/'loop').mkdir(parents=True,exist_ok=True)
    lock=(LOCAL/'loop/runner.lock').open('a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    statepath=LOCAL/'loop/state.json';feedbackpath=LOCAL/'loop/feedback.json'
    state=json.loads(statepath.read_text()) if statepath.exists() else dict(stage='feasibility',attempts=[],best_feasibility=None,accepted_baseline=None)
    feedback=json.loads(feedbackpath.read_text()) if feedbackpath.exists() else []
    tracer=WeaveTracer.maybe_init(enable=None)
    start=time.monotonic();current=source.resolve();frozen=support(current);scope=design_digest(frozen)
    state.pop('stop_reason',None)
    if (state.get('best_feasibility') or {}).get('metric_version') not in (None,VERSION):
        raise RuntimeError('Metric version changed; explicitly reevaluate incumbent before resuming')
    write(LOCAL/'loop/constraints.json',dict(scope=scope,support_files=frozen,reference_source=str(REFERENCE),policy=POLICY,qualification='Engineering/model requirements unknown; no relaxation permitted'))
    for _ in range(iterations):
        if time.monotonic()-start+route_seconds+40>budget:
            state['stop_reason']='explicit wall-time budget';break
        uid='stage1-'+datetime.now().strftime('%Y%m%d-%H%M%S')+'-'+uuid.uuid4().hex[:6]
        run=LOCAL/'runs'/uid;run.mkdir();candidate=LOCAL/'candidates'/uid
        record=dict(schema_version=1,attempt=uid,policy=POLICY,stage=1,started_at=now(),input=str(current),constraint_scope=scope,status='running',candidate=str(candidate))
        source_paths=[Path(__file__)]+sorted((ROOT/'scripts').glob('copperhead_*.py'))+sorted((ROOT/'scripts/native').glob('Copperhead*.java'))
        record['implementation_sources']={}
        for source in source_paths:
            relative=source.relative_to(ROOT);snapshot=run/'implementation'/relative;snapshot.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,snapshot)
            record['implementation_sources'][str(relative)]=hashlib.sha256(source.read_bytes()).hexdigest()
        record['source_revision']=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
        archive=run/'tool-source';archive.mkdir()
        codepaths=list((ROOT/'scripts').glob('copperhead_*.py'))+list(Path(__file__).parent.glob('*.py'))+[ROOT/'copper_scar/real.py',ROOT/'copper_scar/loop/weave_trace.py']
        record['tool_source_hashes']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in codepaths}
        for p in codepaths:
            dest=archive/p.relative_to(ROOT);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
        record['runner_pid']=os.getpid()
        record['incumbent_before']=state.get('best_feasibility')
        record['incumbent_after']=state.get('best_feasibility')
        record['became_incumbent']=False
        write(run/'attempt.json',record)
        viewpath=LOCAL/'current-status.json'
        if viewpath.exists():
            view=json.loads(viewpath.read_text());view.update(actively_generating=str(candidate),phase='Stage 1: evaluate, select bounded action, recheck',updated_at=now());write(viewpath,view)
        try:
            copy_project(current,run/'input');copy_project(current,candidate)
            with tracer.span('native.stage1.evaluate_before',attributes={'policy_version':POLICY,'attempt':uid}) as span:
                initial=evaluate(run/'input',run,'before',frozen);span.set_output({k:v for k,v in initial.items() if k not in ['files','violations']})
            if not state.get('best_feasibility') or state['best_feasibility'].get('scope')!=scope:
                state['best_feasibility']=dict(candidate=str(current),priority=priority(initial),scope=scope,metric_version=VERSION,design_sha256=initial['design_sha256']) if initial['invariants_ok'] else None
            record['incumbent_before']=state.get('best_feasibility')
            if not legacy_inner and (not initial['invariants_ok'] or initial['errors']):raise ValueError('Whole-board routing requires preserved native invariants and no physical errors')
            action=validate_proposal(proposal,initial) if proposal else choose_action(initial,feedback,scope) if legacy_inner else dict(kind='initial_route',reason='Initial whole-board autoroute from preserved starting placement',hypothesis='Attempt all remaining connections with legal multilayer vias and explicit effort limit',feedback_used=[]);record.update(action=action,before=initial,metric_version=VERSION)
            write(run/'attempt.json',record)
            if action['kind']=='stop':
                record.update(status='needs_proposal',stop_reason=action['reason']);state['stop_reason']=action['reason'];write(run/'attempt.json',record);state['attempts'].append(str(run));break
            commands=[('export',[KIPY,'-c',"import pcbnew as p,sys;b=p.LoadBoard(sys.argv[1]);assert p.ExportSpecctraDSN(b,sys.argv[2])",str(candidate/'pcbgolf.kicad_pcb'),str(candidate/'pcbgolf.dsn')],60),
                      ('route',[PYTHON,str(ROOT/'scripts/copperhead_route.py'),str(candidate),'--seconds',str(route_seconds),'--passes','10'],route_seconds+40),
                      ('import',[KIPY,str(ROOT/'scripts/copperhead_native_board.py'),'import',str(candidate)],60)]
            if action['kind']=='ground_escape':
                commands=[('ground_escape',[KIPY,str(ROOT/'scripts/copperhead_ground_escape.py'),str(candidate),initial['report'],'--limit','20'],120)]
            if action['kind']=='krt_reconnect':
                commands=[('krt_reconnect',[PYTHON,str(ROOT/'scripts/copperhead_krt.py'),str(candidate),'--net',action['net']],route_seconds+40)]
            if action['kind']=='placement_repair':
                commands=[('placement',[KIPY,str(ROOT/'scripts/copperhead_move.py'),str(candidate),'--ref',action['ref']],120),('krt_reconnect',[PYTHON,str(ROOT/'scripts/copperhead_krt.py'),str(candidate),*[v for n in action['nets'] for v in ('--net',n)]],route_seconds+40)]
            if action['kind'] in ('placement_group','placement_trial'):
                group_proposal=run/'placement-proposal.json';write(group_proposal,action)
                commands=[('placement',[KIPY,str(ROOT/'scripts'/('copperhead_spacing_trial.py' if action['kind']=='placement_trial' else 'copperhead_group_move.py')),str(candidate),'--proposal',str(group_proposal)],300),('krt_reconnect',[PYTHON,str(ROOT/'scripts/copperhead_krt.py'),str(candidate),*[v for n in action['nets'] for v in ('--net',n)]],route_seconds+40)]
            if action['kind'] in ('global_expand','group_pose'):
                group_proposal=run/'placement-proposal.json';write(group_proposal,action)
                commands=[('placement',[KIPY,str(ROOT/'scripts'/('copperhead_global_expand.py' if action['kind']=='global_expand' else 'copperhead_apply_pose.py')),str(candidate),'--proposal',str(group_proposal)],300)]
            if not legacy_inner:
                full_commands=[('export',[KIPY,'-c',"import pcbnew as p,sys;b=p.LoadBoard(sys.argv[1]);assert p.ExportSpecctraDSN(b,sys.argv[2])",str(candidate/'pcbgolf.kicad_pcb'),str(candidate/'pcbgolf.dsn')],60),('route',[PYTHON,str(ROOT/'scripts/copperhead_route.py'),str(candidate),'--seconds',str(route_seconds),'--passes','100','--whole-board','--skip-fanout'],route_seconds+40),('import',[KIPY,str(ROOT/'scripts/copperhead_native_board.py'),'import',str(candidate)],60)]
                commands=[c for c in commands if c[0]=='placement']+full_commands
                if action['kind']=='terminal_fanout':
                    fanout_proposal=run/'terminal-fanout-proposal.json';write(fanout_proposal,action)
                    commands=[('fanout_export',full_commands[0][1],60),('terminal_fanout',[PYTHON,str(ROOT/'scripts/copperhead_terminal_fanout.py'),str(candidate),'--proposal',str(fanout_proposal)],420),('fanout_import',full_commands[2][1],60)]+full_commands
                record['comparison_kind']='initial_routed_placement' if action['kind']=='initial_route' else 'routed_placement'
                if action['kind']=='terminal_fanout':record['comparison_kind']='terminal_topology_then_full_routing'
                record['routing_scope']=dict(kind='whole_board',net_filter=None,fanout_enabled=False,via_count_limit=None,effort_limit_seconds=route_seconds,pass_limit=100,completion='pending')
            else:record['comparison_kind']='legacy_inner'
            record['action_level']='outer_placement' if action['kind'] in ('placement_repair','placement_group','placement_trial','global_expand','group_pose') else 'inner_routing'
            if action['kind']=='terminal_fanout':record['action_level']='outer_topology'
            record['outer_candidate']=uid if record['action_level'] in ('outer_placement','outer_topology') else 'geometry:'+initial['geometry_scope']
            record['inner_effort']=[]
            record['commands']=[]
            with tracer.span('native.stage1.act',attributes={'attempt':uid,'action':action['kind'],'policy_version':POLICY}) as span:
                for name,argv,limit in commands:
                    item=command(argv,run,name,limit);record['commands'].append(item);write(run/'attempt.json',record)
                    if name in ('route','krt_reconnect','ground_escape'):
                        record['inner_effort'].append(dict(command=name,elapsed_seconds=item['elapsed_seconds'],returncode=item['returncode'],timed_out=item.get('timed_out',False)))
                    if item['returncode']!=0:raise RuntimeError(name+' failed; see command record')
                    if name=='fanout_import':
                        record['fanout_result']=json.loads((candidate/'terminal-fanout/result.json').read_text())
                        snapshot=run/'fanout-project';copy_project(candidate,snapshot)
                        record['fanout_evaluation']=evaluate(snapshot,run,'after_fanout',frozen)
                        write(run/'attempt.json',record)
                        if not record['fanout_evaluation']['invariants_ok'] or record['fanout_evaluation']['errors']:raise RuntimeError('Fanout failed native physical/invariant check before routing')
                    if name=='placement':
                        if action.get('copper_policy')=='detach_moved_pad_incident':
                            clearance=command([KIPY,str(ROOT/'scripts/copperhead_clear_placement_collisions.py'),str(candidate)],run,'placement_collision_ripup',300)
                            record['commands'].append(clearance)
                            if clearance['returncode']!=0:raise RuntimeError('Placement collision ripup failed')
                        record['placement_delta']=json.loads((candidate/'placement-search.json').read_text())
                        if set(record['placement_delta']['affected_nets'])!=set(action['nets']):raise RuntimeError('Placement net scope differs from proposal')
                        placement_snapshot=run/'placement-project';copy_project(candidate,placement_snapshot)
                        record['placement_snapshot']=str(placement_snapshot)
                        record['placement_evaluation']=evaluate(placement_snapshot,run,'after_placement',frozen)
                        record['placement_geometry']=record['placement_evaluation']['geometry_scope']
                        write(run/'attempt.json',record)
                        if not record['placement_evaluation']['invariants_ok'] or record['placement_evaluation']['errors']:raise RuntimeError('Placement failed native physical/invariant check before routing')
                span.set_output({'commands':record['commands']})
            with tracer.span('native.stage1.evaluate_after',attributes={'attempt':uid,'policy_version':POLICY}) as span:
                after=evaluate(candidate,run,'after',frozen);span.set_output({k:v for k,v in after.items() if k not in ['files','violations']})
            if not legacy_inner:
                record['routing_scope']['execution']=json.loads((candidate/'execution.json').read_text())
                record['routing_scope']['completion']='routed_and_natively_evaluated'
            same_design,raw_decrease,improved,classification=classify_action(initial,after)
            selected=['*'] if not legacy_inner else action.get('nets') or ([action['net']] if action.get('net') else ['GND'] if action['kind']=='ground_escape' else ['*'])
            effects=compare_effects(run/'input/pcbgolf.kicad_pcb',candidate/'pcbgolf.kicad_pcb',selected)
            effects.update(missing_before=missing_by_net(initial),missing_after=missing_by_net(after))
            write(run/'effects.json',effects)
            record.update(effects=str(run/'effects.json'),same_design_hash=same_design,raw_cost_decreased=raw_decrease,classification=classification)
            if (candidate/'krt-provenance.json').exists():record['backend_provenance']=dict(path=str(candidate/'krt-provenance.json'),sha256=hashlib.sha256((candidate/'krt-provenance.json').read_bytes()).hexdigest())
            record.update(status='completed',after=after,diagnostic_improved=improved,diagnostic_priority_before=priority(initial),diagnostic_priority_after=priority(after),official_score=None,validity_gate=False,finished_at=now())
            oldbest=state.get('best_feasibility')
            if not same_design and after['invariants_ok'] and (oldbest is None or priority(after)<tuple(oldbest['priority'])):
                state['best_feasibility']=dict(candidate=str(candidate),priority=priority(after),attempt=uid,scope=scope,metric_version=VERSION,design_sha256=after['design_sha256'])
                record['became_incumbent']=True
            record['incumbent_after']=state.get('best_feasibility')
            state['exploratory_candidate']=dict(candidate=str(candidate),priority=priority(after),scope=scope,metric_version=VERSION)
            fact=dict(attempt=uid,scope=scope,geometry_scope=initial['geometry_scope'],input_design=initial['design_sha256'],output_design=after['design_sha256'],action=action['kind'],diagnostic_improved=improved,counts_before={k:initial[k] for k in ['unconnected','counts']},counts_after={k:after[k] for k in ['unconnected','counts']},objects=[dict(type=v['type'],items=v.get('items',[])) for v in after['violations']],hypothesis=action['hypothesis'],action_parameters=action,metric_version=VERSION,classification=classification,search_cost_before=initial['search_cost'],search_cost_after=after['search_cost'],interpretation='Diagnostic change only; no functional or official-score claim')
            feedback.append(fact);write(feedbackpath,feedback)
            write(run/'attempt.json',record);state['attempts'].append(str(run));state['stage']='feasibility';state['updated_at']=now();write(statepath,state)
            # Publish only after native recheck; viewer helper never opens another window.
            rel=Path(after['report']);shutil.copyfile(rel,candidate/'stage1-drc.json')
            command([PYTHON,str(ROOT/'scripts/copperhead_publish.py'),str(candidate),'stage1-drc.json','--phase','Stage 1 feasibility loop: checked partial candidate'],run,'publish',60)
            command([PYTHON,str(ROOT/'scripts/copperhead_viewer.py')],run,'viewer',30)
            with (LOCAL/'loop/eval-rows.jsonl').open('a') as rows:
                rows.write(json.dumps(dict(attempt=uid,stage=1,policy_version=POLICY,invariants_ok=after['invariants_ok'],unconnected=after['unconnected'],native_cad_ok=after['native_cad_ok'],validity_gate=False,official_score=None,diagnostic_improved=improved,search_cost=after['search_cost']))+'\n')
            # Keep incumbent separately. One safe exploratory continuation can
            # recover a connectivity tradeoff; never explore broken invariants/shorts.
            explore=(not same_design and after['invariants_ok'] and not after['counts'].get('shorting_items',0) and not improved and not state.get('exploration_used',False))
            state['exploration_used']=explore
            current=candidate if explore else Path(state['best_feasibility']['candidate']) if state.get('best_feasibility') else current
        except Exception as exc:
            # A producer failure still gets a fresh inspection when budget permits.
            # Failed actions never promote, even if partial copper looks better.
            record.update(status='failed',error=repr(exc))
            if record.get('routing_scope') and (candidate/'execution.json').exists():
                record['routing_scope'].update(execution=json.loads((candidate/'execution.json').read_text()),completion='failed_no_evaluated_session')
            if record.get('before') and candidate.exists():
                try:record['after']=evaluate(candidate,run,'after_failure',frozen)
                except Exception as check_exc:record['after_failure_error']=repr(check_exc)
            record['incumbent_after']=state.get('best_feasibility')
            if record.get('before') and record.get('after'):
                selected=record.get('action',{}).get('nets') or ([record['action']['net']] if record.get('action',{}).get('net') else [])
                write(run/'effects.json',compare_effects(run/'input/pcbgolf.kicad_pcb',candidate/'pcbgolf.kicad_pcb',selected))
                record['effects']=str(run/'effects.json')
            failure=dict(attempt=uid,scope=scope,geometry_scope=record.get('before',{}).get('geometry_scope'),action=record.get('action',{}).get('kind'),classification='execution_failure',action_parameters=record.get('action',{}),diagnostic_improved=False,error=repr(exc),metric_version=VERSION,interpretation='Failed producer or evaluation; never promoted')
            feedback.append(failure);write(feedbackpath,feedback)
            record['finished_at']=now();write(run/'attempt.json',record);state['attempts'].append(str(run));state['stop_reason']='execution/evaluation failure; inspect preserved attempt';break
    else:state['stop_reason']='explicit iteration budget'
    viewpath=LOCAL/'current-status.json'
    if viewpath.exists():
        view=json.loads(viewpath.read_text());view.update(actively_generating=None,phase='Stage 1 runner stopped: '+state.get('stop_reason','unknown'),updated_at=now());write(viewpath,view)
    state['updated_at']=now();state['weave_enabled']=tracer.enabled;write(statepath,state);tracer.finish()
    config_path=LOCAL/'observability/config.json'
    if config_path.exists():
        config=json.loads(config_path.read_text())
        with (LOCAL/'observability/latest-publication.log').open('w') as log:
            publisher=subprocess.Popen([config['python'],str(ROOT/'scripts/copperhead_observability.py'),'--credential-file',config['credential_file']],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
        write(LOCAL/'observability/worker.json',dict(pid=publisher.pid,started_at=now(),mode='historical backfill after native evaluation'))
    print(json.dumps(state,indent=2))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,required=True);ap.add_argument('--iterations',type=int,default=1);ap.add_argument('--route-seconds',type=int,default=120);ap.add_argument('--budget',type=int,default=600);ap.add_argument('--proposal',type=Path);ap.add_argument('--legacy-inner',action='store_true');a=ap.parse_args()
    if not a.source.resolve().is_relative_to(LOCAL/'candidates'):raise SystemExit('Source must be a Copperhead candidate')
    if not 1<=a.iterations<=100 or not 10<=a.route_seconds<=900:raise SystemExit('Explicit bounded parameters required')
    proposal=None
    if a.proposal:
        if a.iterations!=1:raise SystemExit('A proposal is one measured action; reassess feedback before repeating')
        if not a.proposal.resolve().is_relative_to(LOCAL/'proposals'):raise SystemExit('Proposal must be in the owned proposal directory')
        proposal=json.loads(a.proposal.read_text())
        proposal['proposal_sha256']=hashlib.sha256(a.proposal.read_bytes()).hexdigest()
    if not a.legacy_inner and a.iterations!=1:raise SystemExit('Each outer invocation is one placement plus whole-board autoroute; propose the next placement after evaluation')
    execute(a.source,a.iterations,a.route_seconds,a.budget,proposal,a.legacy_inner)
if __name__=='__main__':main()
