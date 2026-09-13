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
from .manufacturing import findings as manufacturing_findings
from .selection import manufacturing_repair_decision, VERSION as SELECTION_VERSION
from .routing_options import candidate_options,context as routing_context,SMALL,verify_after_exports
from .topology_contract import check as check_topology_contract
from .placement_contacts import check as check_placement_via_nets

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
                    'stage1-drc.json', 'placement-collisions', 'terminal-fanout', 'via-definition', 'via-seed.json', 'via-consolidation.json', 'topology-replan.json', 'krt-*.json', 'placement-search.json', 'ground-escape.json'))
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

def should_retain(initial, after, incumbent):
    # A stale incumbent tie-break must not override the fresh same-parent result.
    old_manufacturing=collections.Counter(v['type'] for v in manufacturing_findings({'violations':initial.get('violations',[])}))
    new_manufacturing=collections.Counter(v['type'] for v in manufacturing_findings({'violations':after.get('violations',[])}))
    if any(new_manufacturing[k]>old_manufacturing[k] for k in new_manufacturing):return False
    incumbent_priority=(priority(initial) if incumbent and incumbent.get('design_sha256')==initial['design_sha256']
                        else tuple(incumbent['priority']) if incumbent else None)
    return (classify_action(initial,after)[2] and after['invariants_ok']
            and (incumbent_priority is None or priority(after)<incumbent_priority))

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

def finalize_board(candidate, run):
    """Persist native zone fills before hashing and checking the delivered board."""
    board=candidate/'pcbgolf.kicad_pcb'
    before=hashlib.sha256(board.read_bytes()).hexdigest()
    invocation=command([KICAD,'pcb','drc','--format','json','--schematic-parity','--refill-zones','--save-board','-o',str(run/'saved-fill-drc.json'),str(board)],run,'persist_zone_fills',120)
    if invocation['returncode']!=0:raise RuntimeError('Persisting native zone fills failed')
    result=dict(before_board_sha256=before,after_board_sha256=hashlib.sha256(board.read_bytes()).hexdigest(),invocation=invocation,subsequent_check='Fresh saved-file DRC without refill required')
    write(run/'saved-fill.json',result)
    return result

def evaluate(candidate, run, label, frozen_support, *, saved_board=False):
    d=run/label;d.mkdir()
    before=design_files(candidate)
    invocations={}
    jobs=[('netlist',[KICAD,'sch','export','netlist','--format','kicadxml','-o',str(candidate/'reference.net.xml'),str(candidate/'pcbgolf.kicad_sch')]),
          ('erc',[KICAD,'sch','erc','--format','json','-o',str(candidate/'erc.json'),str(candidate/'pcbgolf.kicad_sch')]),
          ('drc',[KICAD,'pcb','drc','--format','json','--schematic-parity',*([] if saved_board else ['--refill-zones']),'-o',str(d/'drc.json'),str(candidate/'pcbgolf.kicad_pcb')]),
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
    manufacturing=manufacturing_findings(raw)
    result.update(manufacturing_findings=manufacturing,manufacturing_findings_count=len(manufacturing),manufacturing_rules_clear=not manufacturing)
    result['constraint_scope']=design_digest(frozen_support)
    result['zone_fill_check']='saved_file_without_refill' if saved_board else 'unsaved_native_refill'
    result['native_cad_ok']=result['native_cad_ok'] and not manufacturing
    # This implementation has no authority to invent engineering acceptance.
    write(d/'evaluation.json',result)
    return result

def validate_proposal(proposal, result):
    if proposal.get('kind') not in ('krt_reconnect','placement_repair','placement_group','placement_trial','global_expand','group_pose','terminal_fanout','via_seed','via_consolidation','local_topology_replan') or not isinstance(proposal.get('net'),str):
        raise ValueError('Only a scoped native repair proposal is supported')
    if not result['invariants_ok'] or result['errors']:
        raise ValueError('Backend proposal requires preserved invariants and no physical errors')
    if not all(proposal.get(k) for k in ('reason','hypothesis','feedback_used')):
        raise ValueError('Proposal requires rationale and measured feedback references')
    if proposal['kind']=='local_topology_replan' and not proposal.get('realization_context_digest'):
        raise ValueError('Topology replan requires an explicit qualified realization context')
    if proposal['kind']=='placement_group':
        if not proposal.get('refs') or len(set(proposal['refs']))<2 or not proposal.get('anchors') or not proposal.get('nets'):
            raise ValueError('Group proposal requires explicit members, interface anchors and net scope')
    if proposal['kind'] in ('global_expand','group_pose'):return proposal
    if proposal['kind']=='via_consolidation':
        targets={proposal['keep_via']['uuid'],proposal['remove_via']['uuid']}
        if len(targets)!=2 or not any(v['type']=='hole_to_hole' and targets<={i.get('uuid') for i in v.get('items',[])} for v in result['violations']):
            raise ValueError('Via consolidation requires the exact current native overlapping-hole pair')
        return proposal
    needle='['+proposal['net']+']'
    if not any(v['type']=='unconnected_items' and any(needle in i.get('description','') for i in v.get('items',[])) for v in result['violations']):
        raise ValueError('Proposed net has no current native missing connection')
    return proposal

def execute(source, iterations, route_seconds, budget, proposal=None, legacy_inner=False, state_dir=None):
    global DEADLINE
    DEADLINE=time.monotonic()+budget
    (LOCAL/'loop').mkdir(parents=True,exist_ok=True)
    lock=(LOCAL/'loop/runner.lock').open('a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    loopdir=Path(state_dir).resolve() if state_dir else LOCAL/'loop'
    if state_dir and not loopdir.is_relative_to(LOCAL/'policy-experiment'):raise ValueError('Isolated state must belong to policy-experiment')
    loopdir.mkdir(parents=True,exist_ok=True)
    statepath=loopdir/'state.json';feedbackpath=loopdir/'feedback.json'
    state=json.loads(statepath.read_text()) if statepath.exists() else dict(stage='feasibility',attempts=[],best_feasibility=None,accepted_baseline=None)
    feedback=json.loads(feedbackpath.read_text()) if feedbackpath.exists() else []
    tracer=WeaveTracer.maybe_init(enable=None)
    start=time.monotonic();current=source.resolve();frozen=support(current);scope=design_digest(frozen)
    state.pop('stop_reason',None)
    if (state.get('best_feasibility') or {}).get('metric_version') not in (None,VERSION):
        raise RuntimeError('Metric version changed; explicitly reevaluate incumbent before resuming')
    write(loopdir/'constraints.json',dict(scope=scope,support_files=frozen,reference_source=str(REFERENCE),policy=POLICY,qualification='Engineering/model requirements unknown; no relaxation permitted'))
    for _ in range(iterations):
        if time.monotonic()-start+route_seconds+40>budget:
            state['stop_reason']='explicit wall-time budget';break
        uid='stage1-'+datetime.now().strftime('%Y%m%d-%H%M%S')+'-'+uuid.uuid4().hex[:6]
        run=LOCAL/'runs'/uid;run.mkdir();candidate=LOCAL/'candidates'/uid
        record=dict(schema_version=1,attempt=uid,policy=POLICY,selection_policy_version=SELECTION_VERSION,stage=1,started_at=now(),input=str(current),constraint_scope=scope,status='running',candidate=str(candidate))
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
        if not state_dir and viewpath.exists():
            view=json.loads(viewpath.read_text());view.update(actively_generating=str(candidate),phase='Stage 1: evaluate, select bounded action, recheck',updated_at=now());write(viewpath,view)
        try:
            copy_project(current,run/'input');copy_project(current,candidate)
            options,expected_context=candidate_options(current,LOCAL,scope)
            if proposal and proposal.get('new_via_definition') and SMALL not in options['allowed_via_options']:
                options={**options,'allowed_via_options':options['allowed_via_options']+[SMALL],'qualification':'Explicit experimental proposal; native gate required'};expected_context=routing_context(options['allowed_via_options'],scope,options.get('dsn_contact_normalization'))
            write(candidate/'routing-options.json',options)
            record.update(routing_options=options,realization_context=expected_context,realization_context_verified=False)
            with tracer.span('native.stage1.evaluate_before',attributes={'policy_version':POLICY,'attempt':uid}) as span:
                initial=evaluate(run/'input',run,'before',frozen);span.set_output({k:v for k,v in initial.items() if k not in ['files','violations']})
            if not state.get('best_feasibility') or state['best_feasibility'].get('scope')!=scope:
                state['best_feasibility']=dict(candidate=str(current),priority=priority(initial),scope=scope,metric_version=VERSION,design_sha256=initial['design_sha256']) if initial['invariants_ok'] else None
            if initial['invariants_ok'] and state.get('best_feasibility',{}).get('design_sha256')==initial['design_sha256']:
                record['incumbent_measurement_refresh']=dict(stored_priority=state['best_feasibility']['priority'],fresh_priority=priority(initial),design_sha256=initial['design_sha256'])
                state['best_feasibility']=dict(state['best_feasibility'],priority=priority(initial))
            record['incumbent_before']=state.get('best_feasibility')
            if not legacy_inner and (not initial['invariants_ok'] or initial['errors']):raise ValueError('Whole-board routing requires preserved native invariants and no physical errors')
            action=validate_proposal(proposal,initial) if proposal else choose_action(initial,feedback,scope) if legacy_inner else dict(kind='initial_route',reason='Initial whole-board autoroute from preserved starting placement',hypothesis='Attempt all remaining connections with legal multilayer vias and explicit effort limit',feedback_used=[]);record.update(action=action,before=initial,metric_version=VERSION)
            if action.get('realization_context_digest') and action['realization_context_digest']!=expected_context['digest']:raise ValueError('Proposal was selected for a different realization context')
            action['realization_context_digest']=expected_context['digest']
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
                if action['kind']=='via_consolidation':
                    via_proposal=run/'via-consolidation-proposal.json';write(via_proposal,action)
                    commands=[('via_consolidation',[KIPY,str(ROOT/'scripts/copperhead_consolidate_vias.py'),str(candidate),'--proposal',str(via_proposal)],120)]+full_commands
                if action['kind']=='via_seed':
                    via_proposal=run/'via-seed-proposal.json';write(via_proposal,action)
                    commands=[('via_seed',[KIPY,str(ROOT/'scripts/copperhead_seed_via.py'),str(candidate),'--proposal',str(via_proposal)],120)]+full_commands
                if action['kind']=='local_topology_replan':
                    topology_proposal=run/'topology-proposal.json';write(topology_proposal,action)
                    commands=[('local_topology_replan',[KIPY,str(ROOT/'scripts/copperhead_topology_replan.py'),str(candidate),'--proposal',str(topology_proposal)],120)]+full_commands
                if action['kind']=='terminal_fanout':
                    fanout_proposal=run/'terminal-fanout-proposal.json';write(fanout_proposal,action)
                    commands=[('fanout_export',full_commands[0][1],60),('terminal_fanout',[PYTHON,str(ROOT/'scripts/copperhead_terminal_fanout.py'),str(candidate),'--proposal',str(fanout_proposal)],420),('fanout_import',full_commands[2][1],60)]+full_commands
                    if action.get('new_via_definition'):
                        if action['new_via_definition']!={'diameter_mm':.45,'drill_mm':.2,'span':['F.Cu','B.Cu']}:raise ValueError('Only the reviewed additional through-via definition is supported')
                commands=verify_after_exports(commands,PYTHON,ROOT/'scripts/copperhead_effective_options.py',candidate)
                record['comparison_kind']='initial_routed_placement' if action['kind']=='initial_route' else 'routed_placement'
                if action['kind'] in ('terminal_fanout','via_consolidation','via_seed','local_topology_replan'):record['comparison_kind']='terminal_topology_then_full_routing'
                record['routing_scope']=dict(kind='whole_board',net_filter=None,fanout_enabled=False,via_count_limit=None,effort_limit_seconds=route_seconds,pass_limit=100,completion='pending')
            else:record['comparison_kind']='legacy_inner'
            record['action_level']='outer_placement' if action['kind'] in ('placement_repair','placement_group','placement_trial','global_expand','group_pose') else 'inner_routing'
            if action['kind'] in ('terminal_fanout','via_consolidation','via_seed','local_topology_replan'):record['action_level']='outer_topology'
            record['outer_candidate']=uid if record['action_level'] in ('outer_placement','outer_topology') else 'geometry:'+initial['geometry_scope']
            record['inner_effort']=[]
            record['commands']=[]
            with tracer.span('native.stage1.act',attributes={'attempt':uid,'action':action['kind'],'policy_version':POLICY}) as span:
                for name,argv,limit in commands:
                    item=command(argv,run,name,limit);record['commands'].append(item);write(run/'attempt.json',record)
                    if name in ('route','krt_reconnect','ground_escape'):
                        record['inner_effort'].append(dict(command=name,elapsed_seconds=item['elapsed_seconds'],returncode=item['returncode'],timed_out=item.get('timed_out',False)))
                    if item['returncode']!=0:raise RuntimeError(name+' failed; see command record')
                    if name.endswith('_effective_options'):
                        phase=name.removesuffix('_effective_options');actual=json.loads((candidate/'via-definition'/phase/'realization.json').read_text())
                        if actual['realization_context']['digest']!=expected_context['digest'] or not actual['engine_rule_verified']:raise RuntimeError('Loaded engine routing options differ from declared candidate context')
                        record.setdefault('effective_routing_options',{})[phase]=actual;record['realization_context_verified']=True;write(run/'attempt.json',record)
                    if name=='route':
                        execution=json.loads((candidate/'execution.json').read_text())
                        if execution.get('returncode')!=0 or execution.get('timeout') or not execution.get('session_exists'):
                            raise RuntimeError('Router backend failed or exceeded external timeout; preserve partial session without promotion')
                    if name=='fanout_import':
                        record['fanout_result']=json.loads((candidate/'terminal-fanout/result.json').read_text())
                        snapshot=run/'fanout-project';copy_project(candidate,snapshot)
                        record['fanout_evaluation']=evaluate(snapshot,run,'after_fanout',frozen)
                        write(run/'attempt.json',record)
                        if not record['fanout_evaluation']['invariants_ok'] or record['fanout_evaluation']['errors']:raise RuntimeError('Fanout failed native physical/invariant check before routing')
                        if action.get('new_via_definition'):
                            proof_path=run/'fanout-via-geometry.json'
                            check=command([KIPY,str(ROOT/'scripts/copperhead_via_geometry.py'),'--before',str(run/'input/pcbgolf.kicad_pcb'),'--after',str(candidate/'pcbgolf.kicad_pcb'),'--output',str(proof_path)],run,'fanout_via_geometry',60)
                            if check['returncode']!=0:raise RuntimeError('Native fanout via geometry check failed')
                            proof=json.loads(proof_path.read_text());record['fanout_via_geometry']=str(proof_path)
                            if not proof['existing_via_geometry_preserved'] or not proof['new_vias_use_only_allowed_definitions'] or not record['fanout_evaluation']['manufacturing_rules_clear']:raise RuntimeError('New via trial failed existing geometry or manufacturing gate')
                    if name=='via_consolidation':
                        record['via_consolidation']=json.loads((candidate/'via-consolidation.json').read_text())
                        snapshot=run/'via-consolidation-project';copy_project(candidate,snapshot)
                        record['via_consolidation_evaluation']=evaluate(snapshot,run,'after_via_consolidation',frozen)
                        write(run/'attempt.json',record)
                        if not record['via_consolidation_evaluation']['invariants_ok'] or record['via_consolidation_evaluation']['errors'] or record['via_consolidation_evaluation']['counts'].get('hole_to_hole',0):raise RuntimeError('Via consolidation failed native physical/invariant/hole check')
                    if name=='via_seed':
                        snapshot=run/'via-seed-project';copy_project(candidate,snapshot)
                        record['via_seed']=json.loads((candidate/'via-seed.json').read_text());record['via_seed_evaluation']=evaluate(snapshot,run,'after_via_seed',frozen)
                        proof_path=run/'seed-via-geometry.json'
                        check=command([KIPY,str(ROOT/'scripts/copperhead_via_geometry.py'),'--before',str(run/'input/pcbgolf.kicad_pcb'),'--after',str(candidate/'pcbgolf.kicad_pcb'),'--output',str(proof_path)],run,'seed_via_geometry',60)
                        if check['returncode']!=0:raise RuntimeError('Native seed via geometry check failed')
                        proof=json.loads(proof_path.read_text());gate=record['via_seed_evaluation'];write(run/'attempt.json',record)
                        if not gate['invariants_ok'] or gate['errors'] or not gate['manufacturing_rules_clear'] or not proof['existing_via_geometry_preserved'] or not proof['new_vias_use_only_allowed_definitions']:raise RuntimeError('Via seed failed native physical/invariant/geometry gate')
                    if name=='local_topology_replan':
                        snapshot=run/'topology-replan-project';copy_project(candidate,snapshot)
                        record['topology_replan']=json.loads((candidate/'topology-replan.json').read_text())
                        record['topology_authored_items']=check_topology_contract(run/'input/pcbgolf.kicad_pcb',candidate/'pcbgolf.kicad_pcb',[row['uuid'] for row in action['remove_items']],[row['uuid'] for row in record['topology_replan']['created_vias']])
                        gate=evaluate(snapshot,run,'after_topology_replan',frozen);record['topology_preflight']=gate
                        write(run/'attempt.json',record)
                        if not gate['invariants_ok'] or gate['errors'] or not gate['manufacturing_rules_clear']:raise RuntimeError('Topology replan failed native physical/invariant/manufacturing gate')
                    if name=='placement':
                        if action.get('copper_policy')=='detach_moved_pad_incident' and not action.get('preserve_foreign_copper',False):
                            clearance=command([KIPY,str(ROOT/'scripts/copperhead_clear_placement_collisions.py'),str(candidate)],run,'placement_collision_ripup',300)
                            record['commands'].append(clearance)
                            if clearance['returncode']!=0:raise RuntimeError('Placement collision ripup failed')
                        record['placement_delta']=json.loads((candidate/'placement-search.json').read_text())
                        via_contacts=check_placement_via_nets(run/'input/pcbgolf.kicad_pcb',candidate/'pcbgolf.kicad_pcb');write(run/'placement-via-net-attachments.json',via_contacts);record['placement_via_net_attachments']=via_contacts
                        if not via_contacts['existing_via_net_attachments_preserved']:raise RuntimeError('Placement implicitly reassigned an existing via net')
                        if set(record['placement_delta']['affected_nets'])!=set(action['nets']):raise RuntimeError('Placement net scope differs from proposal')
                        placement_snapshot=run/'placement-project';copy_project(candidate,placement_snapshot)
                        record['placement_snapshot']=str(placement_snapshot)
                        record['placement_evaluation']=evaluate(placement_snapshot,run,'after_placement',frozen)
                        record['placement_geometry']=record['placement_evaluation']['geometry_scope']
                        write(run/'attempt.json',record)
                        if not record['placement_evaluation']['invariants_ok'] or record['placement_evaluation']['errors']:raise RuntimeError('Placement failed native physical/invariant check before routing')
                span.set_output({'commands':record['commands']})
            with tracer.span('native.stage1.evaluate_after',attributes={'attempt':uid,'policy_version':POLICY}) as span:
                record['saved_fill']=finalize_board(candidate,run)
                after=evaluate(candidate,run,'after',frozen,saved_board=True);span.set_output({k:v for k,v in after.items() if k not in ['files','violations']})
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
            oldbest=state.get('best_feasibility')
            retain=should_retain(initial,after,oldbest)
            record['selection_decision']=dict(policy_version=SELECTION_VERSION,basis='fresh_feasibility_with_manufacturing_nonregression',eligible=retain,legacy_v1_priority_before=priority(initial),legacy_v1_priority_after=priority(after))
            if action['kind'] in ('via_consolidation','group_pose','terminal_fanout','via_seed','local_topology_replan'):
                proof_path=run/'final-pad-partitions.json'
                check=command([KIPY,str(ROOT/'scripts/copperhead_pad_partitions.py'),'--before',str(run/'input/pcbgolf.kicad_pcb'),'--after',str(candidate/'pcbgolf.kicad_pcb'),'--output',str(proof_path)],run,'final_pad_partitions',60)
                if check['returncode']!=0:raise RuntimeError('Final native pad partition proof failed')
                proof=json.loads(proof_path.read_text())
                record['selection_decision'].update(pad_partition_proof=str(proof_path),no_connected_pad_group_split=proof['no_connected_pad_group_split'])
                retain=retain and proof['no_connected_pad_group_split']
                record['selection_decision']['eligible']=retain
            if action['kind']=='via_consolidation':
                execution=record['routing_scope']['execution']
                decision=manufacturing_repair_decision(initial,after,oldbest or {},backend_ok=execution.get('returncode')==0 and not execution.get('timeout') and execution.get('session_exists',False),pad_partitions_preserved=proof['no_connected_pad_group_split'])
                decision.update(legacy_v1_priority_before=priority(initial),legacy_v1_priority_after=priority(after),pad_partition_proof=str(proof_path));record['selection_decision']=decision;retain=decision['eligible']
            if action.get('new_via_definition') or action['kind'] in ('via_seed','local_topology_replan') or (state_dir and action['kind']=='group_pose'):
                proof_path=run/'final-via-geometry.json'
                via_reference=run/('topology-replan-project' if action['kind']=='local_topology_replan' else 'via-seed-project' if action['kind']=='via_seed' else 'placement-project' if state_dir and action['kind']=='group_pose' else 'input')/'pcbgolf.kicad_pcb'
                check=command([KIPY,str(ROOT/'scripts/copperhead_via_geometry.py'),'--before',str(via_reference),'--after',str(candidate/'pcbgolf.kicad_pcb'),'--output',str(proof_path)],run,'final_via_geometry',60)
                if check['returncode']!=0:raise RuntimeError('Final native via geometry check failed')
                proof=json.loads(proof_path.read_text());retain=retain and proof['existing_via_geometry_preserved'] and proof['new_vias_use_only_allowed_definitions']
                record['selection_decision'].update(via_geometry_proof=str(proof_path),existing_via_geometry_preserved=proof['existing_via_geometry_preserved'],eligible=retain)
            if action['kind']=='local_topology_replan':
                width_path=run/'final-topology-widths.json'
                check=command([KIPY,str(ROOT/'scripts/copperhead_topology_widths.py'),str(candidate/'pcbgolf.kicad_pcb'),'--proposal',str(run/'topology-proposal.json'),'--output',str(width_path)],run,'final_topology_widths',60)
                if check['returncode']!=0:raise RuntimeError('Final topology width inspection failed')
                widths=json.loads(width_path.read_text());partitions=json.loads((run/'final-pad-partitions.json').read_text())
                target_pads={site['target_pad_uuid'] for site in action['via_sites'] if site.get('target_pad_uuid')}
                target_joined=bool(target_pads) and any(target_pads<=set(group) for group in partitions['after']['groups'])
                cap=action['final_acceptance']['maximum_retained_missing_links']
                retain=retain and widths['ok'] and target_joined and after['unconnected']<=cap
                record['selection_decision'].update(eligible=retain,scoped_widths_preserved=widths['ok'],width_proof=str(width_path),target_islands_joined=target_joined,maximum_retained_missing_links=cap)
            record.update(status='completed',after=after,diagnostic_improved=improved,diagnostic_priority_before=priority(initial),diagnostic_priority_after=priority(after),official_score=None,validity_gate=False,finished_at=now())
            if retain:
                state['best_feasibility']=dict(candidate=str(candidate),priority=priority(after),attempt=uid,scope=scope,metric_version=VERSION,design_sha256=after['design_sha256'])
                record['became_incumbent']=True
            record['incumbent_after']=state.get('best_feasibility')
            state['exploratory_candidate']=dict(candidate=str(candidate),priority=priority(after),scope=scope,metric_version=VERSION)
            fact=dict(attempt=uid,scope=scope,geometry_scope=initial['geometry_scope'],input_design=initial['design_sha256'],output_design=after['design_sha256'],action=action['kind'],diagnostic_improved=improved,counts_before={k:initial[k] for k in ['unconnected','counts']},counts_after={k:after[k] for k in ['unconnected','counts']},objects=[dict(type=v['type'],items=v.get('items',[])) for v in after['violations']],hypothesis=action['hypothesis'],action_parameters=action,metric_version=VERSION,classification=classification,search_cost_before=initial['search_cost'],search_cost_after=after['search_cost'],interpretation='Diagnostic change only; no functional or official-score claim')
            fact.update(parent_board_sha256=initial['files']['pcbgolf.kicad_pcb'],retained=retain,runtime_seconds=sum(x['elapsed_seconds'] for x in record['commands']),collision_removals=record.get('placement_delta',{}).get('collision_ripup',{}).get('removed',[]),selection_decision=record['selection_decision'])
            fact['realization_context']=record['realization_context']
            fact['connectivity_gain']=initial['unconnected']-after['unconnected']
            fact['rejection_reasons']=[]
            if not retain:
                if not record['selection_decision'].get('no_connected_pad_group_split',True):fact['rejection_reasons'].append('Previously connected pad group split')
                if not record['selection_decision'].get('existing_via_geometry_preserved',True):fact['rejection_reasons'].append('Exact existing or seeded via geometry changed')
                if not record['selection_decision'].get('scoped_widths_preserved',True):fact['rejection_reasons'].append('Scoped minimum trace width not preserved')
                if not record['selection_decision'].get('target_islands_joined',True):fact['rejection_reasons'].append('Declared target islands remain disconnected')
                if after['unconnected']>record['selection_decision'].get('maximum_retained_missing_links',after['unconnected']):fact['rejection_reasons'].append('Required native open-count improvement not achieved')
                if not fact['rejection_reasons']:fact['rejection_reasons'].append('Did not pass native feasibility and improvement selection')
            if (run/'final-via-geometry.json').exists():
                via_proof=json.loads((run/'final-via-geometry.json').read_text())
                fact['via_geometry_delta']={k:via_proof[k] for k in ('missing_existing','added')}
            if (run/'final-pad-partitions.json').exists():
                proof=json.loads((run/'final-pad-partitions.json').read_text())
                fact['native_pad_connectivity']=dict(proof=str(run/'final-pad-partitions.json'),no_connected_pad_group_split=proof['no_connected_pad_group_split'],split_groups=proof['split_groups'],before_group_count=len(proof['before']['groups']),after_group_count=len(proof['after']['groups']))
                fact['native_pad_connectivity']['pad_partitions_equal']=proof['pad_partitions_equal']
            feedback.append(fact);write(feedbackpath,feedback)
            write(run/'attempt.json',record);state['attempts'].append(str(run));state['stage']='feasibility';state['updated_at']=now();write(statepath,state)
            # Publish only after native recheck; viewer helper never opens another window.
            rel=Path(after['report']);shutil.copyfile(rel,candidate/'stage1-drc.json')
            if not state_dir:command([PYTHON,str(ROOT/'scripts/copperhead_publish.py'),str(candidate),'stage1-drc.json','--phase','Stage 1 feasibility loop: checked partial candidate'],run,'publish',60)
            if not state_dir:command([PYTHON,str(ROOT/'scripts/copperhead_viewer.py')],run,'viewer',30)
            with (loopdir/'eval-rows.jsonl').open('a') as rows:
                rows.write(json.dumps(dict(attempt=uid,stage=1,policy_version=POLICY,invariants_ok=after['invariants_ok'],unconnected=after['unconnected'],native_cad_ok=after['native_cad_ok'],validity_gate=False,official_score=None,diagnostic_improved=improved,search_cost=after['search_cost']))+'\n')
            # Keep incumbent separately. One safe exploratory continuation can
            # recover a connectivity tradeoff; never explore broken invariants/shorts.
            explore=(not same_design and after['invariants_ok'] and not after['counts'].get('shorting_items',0) and not improved and not state.get('exploration_used',False))
            state['exploration_used']=explore
            current=candidate if explore else Path(state['best_feasibility']['candidate']) if state.get('best_feasibility') else current
        except Exception as exc:
            if record.get('status')=='completed':
                # Native evaluation/selection has finished. A viewer, publication,
                # or delivery-budget failure must not rewrite that native result.
                record['postprocessing_error']=repr(exc)
                write(run/'attempt.json',record)
                if str(run) not in state['attempts']:state['attempts'].append(str(run))
                state['stop_reason']='native evaluation completed; postprocessing needs retry'
                break
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
    if not state_dir and viewpath.exists():
        view=json.loads(viewpath.read_text());view.update(actively_generating=None,phase='Stage 1 runner stopped: '+state.get('stop_reason','unknown'),updated_at=now());write(viewpath,view)
    state['updated_at']=now();state['weave_enabled']=tracer.enabled;write(statepath,state);tracer.finish()
    config_path=LOCAL/'observability/config.json'
    if not state_dir and config_path.exists():
        config=json.loads(config_path.read_text())
        with (LOCAL/'observability/latest-publication.log').open('w') as log:
            publisher=subprocess.Popen([config['python'],str(ROOT/'scripts/copperhead_observability.py'),'--credential-file',config['credential_file']],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
        write(LOCAL/'observability/worker.json',dict(pid=publisher.pid,started_at=now(),mode='historical backfill after native evaluation'))
    print(json.dumps(state,indent=2))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,required=True);ap.add_argument('--iterations',type=int,default=1);ap.add_argument('--route-seconds',type=int,default=120);ap.add_argument('--budget',type=int,default=600);ap.add_argument('--proposal',type=Path);ap.add_argument('--legacy-inner',action='store_true');ap.add_argument('--state-dir',type=Path);a=ap.parse_args()
    if not a.source.resolve().is_relative_to(LOCAL/'candidates'):raise SystemExit('Source must be a Copperhead candidate')
    if not 1<=a.iterations<=100 or not 10<=a.route_seconds<=900:raise SystemExit('Explicit bounded parameters required')
    proposal=None
    if a.proposal:
        if a.iterations!=1:raise SystemExit('A proposal is one measured action; reassess feedback before repeating')
        if not a.proposal.resolve().is_relative_to(LOCAL/'proposals'):raise SystemExit('Proposal must be in the owned proposal directory')
        proposal=json.loads(a.proposal.read_text())
        proposal['proposal_sha256']=hashlib.sha256(a.proposal.read_bytes()).hexdigest()
    if not a.legacy_inner and a.iterations!=1:raise SystemExit('Each outer invocation is one placement plus whole-board autoroute; propose the next placement after evaluation')
    execute(a.source,a.iterations,a.route_seconds,a.budget,proposal,a.legacy_inner,a.state_dir)
if __name__=='__main__':main()
