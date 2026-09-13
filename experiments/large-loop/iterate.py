"""Diagnostic-driven placement batches, each followed by fresh full-board routing."""
from pathlib import Path
import argparse,copy,json,re,subprocess
from collections import Counter
from campaign import realize,poses,hpwl,write,now,sha,ROOT,require_stage_one_work
from record import finish
from live_status import update as update_live
from audit import inventory

def propose(parent,manifest,variant=0):
 ps=poses(parent/'pcbgolf.kicad_pcb');inv,_=inventory(parent/'pcbgolf.kicad_pcb');d=json.loads((parent/'drc.json').read_text());weights=Counter()
 for issue in d['unconnected_items']:
  nets=set()
  for item in issue['items']:
   found=re.search(r'\[([^]]+)\]',item['description'])
   if found:nets.add(found.group(1))
  weights.update(nets)
 # Signal weighting is diagnostic-driven; supply nets stay in ranking at weight1.
 w={n:1+min(8,weights[n]) for n in manifest['nets']}
 def score(p):
  return sum(w[n]*(max(p[r][0] for r in rs)-min(p[r][0] for r in rs)+max(p[r][1] for r in rs)-min(p[r][1] for r in rs)) for n,rs in netrefs.items())
 netrefs={n:set(p.split('.')[0] for p in pads) for n,pads in manifest['nets'].items()}
 refs=sorted(r for r in ps if r.startswith('R'));candidate=copy.deepcopy(ps);used=set();changes=[];before_score=score(ps)
 for step in range(6):
  options=[];oldscore=score(candidate)
  for ia,a in enumerate(refs):
   if a in used:continue
   for b in refs[ia+1:]:
    if b in used or inv[a]['library']!=inv[b]['library'] or inv[a]['pads']!=inv[b]['pads']:continue
    p=copy.deepcopy(candidate);p[a],p[b]=p[b],p[a];after=score(p)
    if after<oldscore:options.append((after,a,b,p))
  if not options:break
  after,a,b,p=sorted(options,key=lambda x:x[:3])[min(variant,len(options)-1)];changes.append({'components':[a,b],'before':{r:candidate[r] for r in [a,b]},'after':{r:p[r] for r in [a,b]},'weighted_hpwl_delta':after-oldscore});candidate=p;used.update([a,b])
 return candidate,{'kind':'diagnostic_passive_group_placement','rationale':'Native unconnected-net incidence weights connected component groups; swap equal-footprint resistor locations to shorten congested net spans without shrinking spacing or altering rules. Six disjoint swaps form one outer proposal, followed by full-board routing.','diagnostic_net_counts':dict(weights),'weighted_hpwl_before':before_score,'weighted_hpwl_after':score(candidate),'swaps':changes,'signals_only':False,'routing_scope':'fresh whole board, both layers, no inherited copper'}

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('base',type=Path);ap.add_argument('source',type=Path);ap.add_argument('parent');ap.add_argument('output');ap.add_argument('--variant',type=int,default=0);a=ap.parse_args();base=a.base.resolve();parent=base/a.parent;out=base/a.output;require_stage_one_work(parent);m=json.loads((base/'input/circuit.json').read_text());candidate,action=propose(parent,m,a.variant);write(base/(a.output+'-proposal.json'),{'source_sha':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'parent_board_sha256':sha(parent/'pcbgolf.kicad_pcb'),'created_at':now(),'poses':candidate,'action':action});print(json.dumps(action),flush=True)
 try:
  result,commands=realize(base,out,candidate,base/'input/circuit.json',a.source.resolve())
  before=json.loads((parent/'evaluation.json').read_text());record=finish(base,out,a.source.resolve(),action,parent)
  result=record['after'];retain=result['placement_legal'] and (result['feasibility_cost'],result['wire_length_mm'])<(before['feasibility_cost'],before['wire_length_mm']);record['retained']=retain;record['decision_reason']='strictly lower native feasibility cost, then shorter copper at equal cost; unchanged original rule and pad/net gates mandatory';write(out/'completed.json',record);update_live(base,state='idle');print(json.dumps({'retained':retain,'opens':result['native_open_count'],'cost':result['feasibility_cost'],'folder':str(out)}),flush=True)
 except Exception as error:
  write(base/(a.output+'-failure.json'),{'action':action,'parent':str(parent),'error':repr(error),'finished_at':now()});raise
