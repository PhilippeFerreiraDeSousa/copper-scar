"""Prospective equal-budget policy pilot; not independent generalization evidence."""
from pathlib import Path
import argparse,copy,json,subprocess
from campaign import realize,propose,write,now,sha
ap=argparse.ArgumentParser();ap.add_argument('base',type=Path);ap.add_argument('source',type=Path);a=ap.parse_args();base=a.base.resolve();out=base/'policy-pilot';out.mkdir();m=json.loads((base/'input/circuit.json').read_text());initial=m['poses'];baseline=json.loads((base/'baseline-parity/evaluation.json').read_text());commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
protocol={'created_at':now(),'source_sha':commit,'N':2,'policies':['all-net-hpwl','signal-net-hpwl'],'primary':'retained feasibility_cost@2','tie_rule':'retain all-net-hpwl baseline on equal primary cost','lower_retention':'strict lower feasibility cost then shorter wire length','budget_per_decision':{'seconds':240,'passes':100,'threads':1,'layers':['F.Cu','B.Cu'],'full_board':True},'initial':str(base/'baseline-parity'),'initial_cost':baseline['feasibility_cost'],'limitations':'Previously observed board; deterministic proposals, no LLM calls, single board pilot, no generalization claim. Separate diagnostic relay move was already successful but is not supplied to either arm.'};write(out/'protocol.json',protocol)
records=[];outcomes={}
for policy in protocol['policies']:
 ps=copy.deepcopy(initial);inc=baseline;parent=base/'baseline-parity';tried=set();curve=[inc['feasibility_cost']]
 for step in range(1,3):
  candidate,action=propose(ps,m['nets'],policy,tried);name=f'{policy}-{step}';folder=out/name;record={'id':name,'stage':'stage1-policy','source_sha':commit,'started_at':now(),'parent':str(parent),'action':action,'route_budget':protocol['budget_per_decision']};write(out/(name+'-proposal.json'),record)
  r,cmds=realize(base,folder,candidate,base/'input/circuit.json',a.source.resolve());keep=r['placement_legal'] and (r['feasibility_cost'],r['wire_length_mm'])<(inc['feasibility_cost'],inc['wire_length_mm'])
  record.update(after=r,commands=cmds,finished_at=now(),retained=keep,decision='keep' if keep else 'reject',folder=str(folder),preview_sha256=sha(folder/'preview.kicad_pcb'));write(folder/'completed.json',record);records.append(record);write(out/'records.json',records)
  if keep:ps=candidate;inc=r;parent=folder
  curve.append(inc['feasibility_cost']);print(name,r['feasibility_cost'],keep,flush=True)
 outcomes[policy]={'cost_at_N':inc['feasibility_cost'],'curve':curve,'selected':str(parent),'wire_length_mm':inc['wire_length_mm']}
write(out/'outcome.json',{'outcomes':outcomes,'selected_policy':'signal-net-hpwl' if outcomes['signal-net-hpwl']['cost_at_N']<outcomes['all-net-hpwl']['cost_at_N'] else 'all-net-hpwl','tie_rule':protocol['tie_rule'],'limitations':protocol['limitations']})
