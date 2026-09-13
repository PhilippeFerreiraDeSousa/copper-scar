import importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location('policy_experiment',Path(__file__).parents[1]/'scripts/copperhead_policy_experiment.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def row(kind,split,distance,introduced=0):
 return dict(action=dict(id=kind,kind=kind,local_approach_mm=distance),split_group_count=split,introduced_islands=introduced)
def test_only_comparator_changes():
 pose=row('group_pose',1,1);anchor=row('local_topology_replan',0,21)
 assert min([pose,anchor],key=lambda r:m.rank(dict(ranking='placement_then_endpoint'),r)) is pose
 assert min([pose,anchor],key=lambda r:m.rank(dict(ranking='split_burden_then_topology_then_endpoint'),r)) is anchor

def test_primary_tie_keeps_baseline_even_if_distance_improved():
 a=dict(opens=45,physical_errors=0,manufacturing_findings=0,invariants_ok=True,airwire_distance_mm=900)
 b={**a,'airwire_distance_mm':800}
 assert m.winner(a,b)=='placement_first'
 assert m.winner(a,{**b,'opens':44})=='island_first'
 assert m.winner(a,{**b,'opens':44,'physical_errors':1})=='placement_first'
 assert m.winner(a,{**b,'opens':44,'manufacturing_findings':1})=='placement_first'
