"""Whole-board pose/copper and project-rule comparison on external exports."""
import json
from pathlib import Path
import sys
import sexpdata as sx
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'placement_bridge'))
from verify_incremental_fixture import children,one,without_ids

def inv(stage):
    board=next((stage/'normalized').glob('*.kicad_pcb'));tree=sx.loads(board.read_text());nets={int(n[1]):str(n[2]) for n in children(tree,'net')};data=json.loads((stage/'inventory.json').read_text());copper={}
    for kind in ('segment','arc','via','gr_poly','zone'):
        for item in children(tree,kind):
            fields=children(item,'net')
            if not fields:continue
            net=nets.get(int(fields[0][1]),'');record=without_ids(item);one(record,'net')[1]=net;copper.setdefault(net,[]).append(sx.dumps(record))
    def clean(value):
        if isinstance(value,dict):return {k:clean(v) for k,v in value.items() if k not in ('uuid','pose')}
        if isinstance(value,list):return [clean(v) for v in value]
        return value
    physical={r:clean(f) for r,f in data['footprints'].items()}
    return {r:f['pose'] for r,f in data['footprints'].items()},{n:sorted(v) for n,v in copper.items()},json.loads(board.with_suffix('.kicad_pro').read_text())['board']['design_settings'],physical
def drc(stage):
    summary=json.loads((stage/'whole-board-check/summary.json').read_text())
    # Wall time varies; compare every reported check/count and both repetitions.
    return summary['repeated_agreement'],[{k:v for k,v in run.items() if k!='elapsed_s'} for run in summary['runs']]

stages=list(map(Path,sys.argv[1:3]))
a,b=map(inv,stages);changed=sorted(n for n in a[1].keys()|b[1].keys() if a[1].get(n)!=b[1].get(n));refs=sorted(r for r in a[0] if a[0][r]!=b[0].get(r));result={'all_geometry_and_poses_equal':a[0]==b[0] and a[1]==b[1] and a[3]==b[3],'native_footprint_inventory_equal':a[3]==b[3],'changed_refs':refs,'changed_copper_nets':changed,'project_rules_equal':a[2]==b[2]}
da,db=map(drc,stages)
result['twice_drc_equal']=da[0] and db[0] and len(da[1])==2 and da==db
result['common_parent_equal']=all(result[k] for k in ('all_geometry_and_poses_equal','project_rules_equal','twice_drc_equal'))
Path(sys.argv[3]).write_text(json.dumps(result,indent=2))
