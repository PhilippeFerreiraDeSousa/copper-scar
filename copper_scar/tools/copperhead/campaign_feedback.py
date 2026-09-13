"""Measured failure features used by the existing serial native campaign."""
import json
from pathlib import Path
from .records import load_record
from .routing_options import record_context


def load_failures(runs):
    failures=[]
    for path in sorted(Path(runs).glob('stage1-*/attempt.json')):
        record=load_record(path)
        if record.get('status')!='completed' or record.get('became_incumbent') or record.get('action',{}).get('kind')!='group_pose':continue
        before=record.get('before',{});after=record.get('after',{})
        proof_path=path.parent/'final-pad-partitions.json'
        proof=json.loads(proof_path.read_text()) if proof_path.exists() else {}
        collision=record.get('placement_delta',{}).get('collision_ripup',{})
        failures.append(dict(attempt=record['attempt'],source=str(path),parent_board_sha256=before.get('files',{}).get('pcbgolf.kicad_pcb'),action=record['action'],realization_context=record_context(record),native_delta=after.get('unconnected',0)-before.get('unconnected',0),split_groups=proof.get('split_groups',[]),connectivity_proof=str(proof_path) if proof else None,collision_removals=collision.get('removed',[]),runtime_seconds=sum(c.get('elapsed_seconds',0) for c in record.get('commands',[]))))
    return failures


def score_preview(action, collisions, partitions, failures):
    """Hard exclusion of exact repeated failures; penalize measured collateral cuts."""
    exact=[];repeated=[]
    removed={x['uuid'] for x in collisions.get('removed',[])}
    for failure in failures:
        if action.get('realization_context_digest') and failure.get('realization_context',{}).get('digest')!=action['realization_context_digest']:continue
        prior=failure['action']
        if prior.get('parent_board_sha256')==action['parent_board_sha256'] and prior.get('refs')==action['refs'] and prior.get('translation_mm')==action['translation_mm'] and prior.get('rotation_deg',0)==action.get('rotation_deg',0):exact.append(failure['attempt'])
        if failure['split_groups'] or failure['native_delta']>0:
            hits=removed & {x['uuid'] for x in failure['collision_removals']}
            if hits:repeated.append(dict(attempt=failure['attempt'],feature_uuids=sorted(hits)))
    foreign=[x for x in collisions.get('removed',[]) if x['net'] not in action['nets']]
    score=100000*len(repeated)+1000*len(foreign)+100*len(partitions.get('split_groups',[]))+len(removed)+action['local_approach']['after_mm']
    return dict(eligible=not exact and not collisions.get('native_errors_remaining'),score=score,exact_failed_pose_records=exact,repeated_collateral_records=repeated,foreign_net_removals=len(foreign),preflight_split_groups=len(partitions.get('split_groups',[])),feedback_record_ids=sorted(set(exact+[x['attempt'] for x in repeated])),reason='Reject repeated exact-parent failed poses; rank repeated failed collateral cuts, foreign-net removals, native preflight splits, then approach distance. Heuristic selection, not a learned model.')
