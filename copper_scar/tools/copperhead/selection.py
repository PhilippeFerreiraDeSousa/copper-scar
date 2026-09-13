"""Explicit manufacturing-repair selection, separate from historical v1 metrics."""
from collections import Counter
from .manufacturing import findings

VERSION='native-selection-v2'


def manufacturing_repair_decision(before,after,incumbent,*,backend_ok,pad_partitions_preserved):
    old=Counter(v['type'] for v in findings({'violations':before['violations']}))
    new=Counter(v['type'] for v in findings({'violations':after['violations']}))
    scope=before.get('constraint_scope')
    checks={
        'same_original_scope':bool(scope) and scope==after.get('constraint_scope')==incumbent.get('scope'),
        'fresh_same_incumbent':before['design_sha256']==incumbent.get('design_sha256'),
        'native_invariants':before['invariants_ok'] and after['invariants_ok'],
        'backend_completed':backend_ok,
        'pad_partitions_preserved':pad_partitions_preserved,
        'shorts_nonworsening':after['counts'].get('shorting_items',0)<=before['counts'].get('shorting_items',0),
        'physical_errors_nonworsening':after['errors']<=before['errors'],
        'missing_pairs_nonworsening':after['unconnected']<=before['unconnected'],
        'manufacturing_categories_nonworsening':all(new[k]<=old[k] for k in set(old)|set(new)),
        'manufacturing_strictly_improved':sum(new.values())<sum(old.values()),
    }
    return dict(policy_version=VERSION,basis='manufacturing_repair',eligible=all(checks.values()),checks=checks,
                manufacturing_before=dict(old),manufacturing_after=dict(new),
                reason='Strict original-rule manufacturing improvement with substantive counts and connectivity nonworsening; airwire remains diagnostic only')
