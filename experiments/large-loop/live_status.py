"""Atomic status for the unified dashboard; completed records remain authority."""
from pathlib import Path
import argparse,json
from campaign import now,write,stage_one_terminal

def update(base,current=None,state='idle'):
 base=Path(base);records=[]
 for f in base.glob('*/completed.json'):
  records.append(json.loads(f.read_text()))
 eligible=[r for r in records if r.get('retained') or Path(r['folder']).name=='routing-control-01' or stage_one_terminal(r['after'])]
 best=min(eligible,key=lambda r:(r['after']['feasibility_cost'],r['after']['wire_length_mm'])) if eligible else None
 v=best['after'] if best else {};operation=None
 if current:
  f=base/current;receipt=json.loads((f/'source-receipt.json').read_text()) if (f/'source-receipt.json').exists() else {}
  operation={'id':current,'started_at':receipt.get('created_at',now()),'source_sha':receipt.get('source_sha'),'kind':'full-board native placement realization'}
 result={'schema':1,'family':'large-loop','stage':2 if v and stage_one_terminal(v) else 1,'state':'stage1-complete' if v and stage_one_terminal(v) else state,'current_operation':operation,'retained_incumbent':{'folder':Path(best['folder']).name,'opens':v['native_open_count'],'required_findings':len(v['required_violations']),'loss':v['feasibility_cost'],'accepted':v['accepted'],'board_sha256':v['board_sha256']} if best else None,'intrinsic_required_findings':84,'loss_units':'count: opens + required physical findings + schematic parity + ERC + invariant penalties','native_required_gate':'Stop Stage1 immediately at first fully accepted native checkpoint; 0 opens alone is insufficient.','discovery':{'root':str(base.resolve()),'pattern':'*/completed.json','only_completed_direct_children':True},'updated_at':now()}
 write(base/'live-status.json',result);return result

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('base',type=Path);ap.add_argument('--current');ap.add_argument('--state',default='idle');a=ap.parse_args();print(json.dumps(update(a.base,a.current,a.state),indent=2))
