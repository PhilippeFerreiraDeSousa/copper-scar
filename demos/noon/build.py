#!/usr/bin/env python3
"""Read owner snapshots into a portable two-project presentation."""
import argparse,datetime,hashlib,json,shutil,subprocess,sys,html,re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'autoresearch'))
from cad import parse,nodes,one,inventory
CLI='/Users/philippe/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def copytree(src,dst):
 shutil.copytree(src,dst,dirs_exist_ok=True,ignore=shutil.ignore_patterns('router-userdata','*.kicad_prl','__pycache__','.DS_Store','*.lck','.history','.git'))
def board(src,out):
 h=sha(src);dest=out/'boards'/h;dest.mkdir(parents=True,exist_ok=True);p=dest/'board.kicad_pcb'
 if not p.exists():shutil.copy2(src,p)
 images={}
 poses,_,_=inventory(p);root=parse(p);edgepoints=[]
 for el in root:
  if isinstance(el,list) and el and el[0] in ['gr_line','gr_rect'] and one(el,'layer')==['Edge.Cuts']:
   edgepoints += [list(map(float,one(el,k)[:2])) for k in ['start','end'] if one(el,k)]
 ox=min(x[0] for x in edgepoints) if edgepoints else 0;oy=min(x[1] for x in edgepoints) if edgepoints else 0
 for layer in ['F.Cu','B.Cu','Both']:
  svg=dest/(layer+'.svg')
  if not svg.exists():subprocess.run([CLI,'pcb','export','svg','--layers',(layer if layer!='Both' else 'F.Cu,B.Cu')+',F.SilkS,Edge.Cuts','--mode-single','--page-size-mode','2','--exclude-drawing-sheet','-o',str(svg),str(p)],capture_output=True,check=True)
  labeled=dest/(layer+'-labels.svg')
  text=svg.read_text();labels=''.join(f'<text x="{v[0]-ox:.4f}" y="{v[1]-oy-1.8:.4f}" font-family="sans-serif" font-size="1.0" text-anchor="middle" fill="white" stroke="#091320" stroke-width="0.3" paint-order="stroke">{html.escape(ref)}</text>' for ref,v in poses.items());labeled.write_text(text.replace('</svg>',labels+'</svg>'));images[layer]=str(labeled.relative_to(out))
 assert sha(src)==h
 return {'cad':str(p.relative_to(out)),'sha256':h,'images':images}
def state(folder,out,title,phase,receipt=None,preview=False,action=None,retained=None,source=None,at=None):
 p=folder/('preview.kicad_pcb' if preview else 'pcbgolf.kicad_pcb');e=read(receipt) if receipt else None
 if not p.exists():p=folder/'medium-loop.kicad_pcb'
 d={'title':title,'phase':phase,'board':board(p,out),'evaluation':None if preview else e,'action':action,'retained':retained,'source':source,'at':at,'receipt':str(receipt.relative_to(out)) if receipt else None}
 if e and not preview and e.get('board_sha256'):assert e['board_sha256']==d['board']['sha256'],str(folder)
 return d

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--small',type=Path,required=True);ap.add_argument('--medium',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--medium-completed',nargs='*',default=[]);ap.add_argument('--status',type=Path);a=ap.parse_args();out=a.out.resolve();out.mkdir(parents=True,exist_ok=True);raw=out/'evidence';raw.mkdir(exist_ok=True)
 small=raw/'small';small.mkdir(exist_ok=True)
 for name in ['campaign','topology-trial','topology-two-ended','input']:
  copytree(a.small/name,small/name)
 for name in ['jitx-parity-audit.json','authoritative-project.json']:
  if (a.small/name).exists():shutil.copy2(a.small/name,small/name)
 c=small/'campaign';protocol=read(c/'protocol.json');records=read(c/'records.json');decision=read(c/'higher-loop-decision.json');states=[]
 states.append(state(c/'initial-unrouted',out,'Initial placement: 29 opens','Routing-only initialization',c/'initial-unrouted/evaluation.json',source=protocol['source_sha']))
 for r in records:
  f=c/Path(r['folder']).name;action=r['action'];pair=' ↔ '.join(action.get('components',[]));label=('Route the unchanged layout' if r['step']==0 else r['arm']+' · '+str(r['step'])+' · Swap '+pair)
  if r['step']>0:states.append(state(f,out,label+' · proposed','Placement preview',f/'acceptance.json',True,action,source=r['source_sha'],at=r.get('started_at')))
  states.append(state(f,out,label+' · evaluated','Routing-only initialization' if r['step']==0 else 'Matched placement pilot',f/'acceptance.json',action=action,retained=r.get('retain'),source=r['source_sha'],at=r.get('finished_at')))
  states[-1]['retained_cost']=r.get('retained_cost',0);states[-1]['retained_wire_mm']=r.get('retained_wire_mm',r['after']['wire_length_mm']);states[-1]['arm']=r['arm'];states[-1]['step']=r['step'];states[-1]['commands']=r.get('commands',[])
 for name,label in [('topology-trial','Reject dangling authored topology'),('topology-two-ended','Valid two-ended topology: reject longer wiring')]:
  f=small/name;states.append(state(f,out,label,'Separate topology trial',f/'acceptance.json',action=read(f/'topology-proposal.json'),retained=False));states[-1]['qualification']='Outside matched N=3 comparison. No official Stage 2 score claim.'
 projects=[{'id':'small','title':'small-loop · 15 components / 11 nets','stage':'Stage 1 pilot complete · Stage 2 validation pending','summary':'Routing alone solved the starting placement (29 → 0). Both placement policies tie at zero. Wire length 493.61 → 436.57 mm is a secondary metric, not the official Stage 2 score.','states':states,'protocol':protocol,'decision':decision,'limitations':'One board and one deterministic placement seed. Authored deterministic ranking; no per-step LLM calls or hidden reasoning traces. Native pilot gates do not imply hardware qualification. Complete-assembly Stage 2 scoring is a separate epoch.'}]
 medium=raw/'medium';medium.mkdir(exist_ok=True);copytree(a.medium/'input',medium/'input');circuit=read(medium/'input/circuit.json');states=[]
 if (a.medium/'input-preflight.json').exists():
  shutil.copy2(a.medium/'input-preflight.json',medium/'input-preflight.json');drc=read(medium/'input-preflight.json');ev={'drc_opens':len(drc.get('unconnected_items',[])),'all_drc_violations':len(drc.get('violations',[])),'accepted':False};(medium/'input-evaluation.json').write_text(json.dumps(ev));states.append(state(medium/'input',out,'Original-inspired legal input','Unrouted input',medium/'input-evaluation.json'))
 for name in a.medium_completed:
  f=a.medium/name;assert (f/'acceptance.json').exists(),str(f);copytree(f,medium/name);dst=medium/name;rec=read(dst/'completed.json') if (dst/'completed.json').exists() else read(dst/'decision.json') if (dst/'decision.json').exists() else {};
  if rec.get('action') and (dst/'preview.kicad_pcb').exists():states.append(state(dst,out,name+' · proposed','Placement preview',dst/'acceptance.json',True,action=rec.get('action'),source=rec.get('source_sha'),at=rec.get('started_at')))
  states.append(state(dst,out,name+' · evaluated','Completed native attempt',dst/'acceptance.json',action=rec.get('action'),retained=rec.get('retained',rec.get('retain')),source=rec.get('source_sha'),at=rec.get('finished_at')));states[-1]['commands']=rec.get('commands',[])
 pilot=a.medium/'policy-pilot'
 if (pilot/'outcome.json').exists():
  pd=medium/'policy-pilot';copytree(pilot,pd)
  for rec in read(pd/'records.json'):
   folder=pd/Path(rec.get('folder',rec['id'])).name
   states.append(state(folder,out,rec['id']+' · proposed','Separate matched policy pilot · preview',folder/'acceptance.json',True,action=rec['action'],source=rec['source_sha'],at=rec.get('started_at')))
   st=state(folder,out,rec['id']+' · evaluated','Separate matched policy pilot',folder/'acceptance.json',action=rec['action'],retained=rec.get('retained'),source=rec['source_sha'],at=rec.get('finished_at'));st['commands']=rec.get('commands',[]);st['qualification']='Separate preregistered N=2 policy comparison. Both arms produce identical swaps and tie at zero; baseline kept.';states.append(st)
 if (a.medium/'accepted-handoff/handoff.json').exists():
  copytree(a.medium/'accepted-handoff',medium/'accepted-handoff');h=read(medium/'accepted-handoff/handoff.json');f=medium/'accepted-handoff';(f/'demo-native-summary.json').write_text(json.dumps(h['evaluation']));st=state(f,out,'Accepted Stage 1 handoff · complete models','Model-complete native handoff',f/'demo-native-summary.json',retained=True,source=h['source_sha'],at=h['created_at']);st['qualification']='ERC 0, schematic parity 0, native opens 0 and DRC 0; 85 resolved component models. Model-only copy preserves routed copper. No medium-loop Stage 2 score has been computed.';st['handoff_receipt']=str((f/'handoff.json').relative_to(out));states.append(st)
 if (a.medium/'accepted-best/handoff.json').exists():
  f=medium/'accepted-best';copytree(a.medium/'accepted-best',f);h=read(f/'handoff.json');(f/'demo-native-summary.json').write_text(json.dumps(h['evaluation']));st=state(f,out,'Best native-accepted medium-loop handoff','Model-complete policy incumbent',f/'demo-native-summary.json',retained=True,source=h['source_sha'],at=h['created_at']);st['qualification']='Native0/0/parity0/ERC0;85models. Policy comparison tied; no algorithm winner.';st['handoff_receipt']=str((f/'handoff.json').relative_to(out));states.append(st)
 projects.append({'id':'medium','title':'medium-loop · 85 components / 67 nets','stage':'Stage 1 · feasibility search','summary':'Eight original-inspired SBU switching, LED and sense blocks. Both copper layers are routed under the declared rules. The latest completed native result is shown below; ERC and full stage handoff status are reported separately.','states':states,'protocol':{'route_budget':'240 seconds / 100 passes / 1 thread, both layers, no fanout optimization','goal':'Zero native opens and required violations, preserved netlist/rules; no weakened gates'},'decision':read(medium/'policy-pilot/outcome.json') if (medium/'policy-pilot/outcome.json').exists() else None,'limitations':'Native Stage 1 acceptance is separate from powered hardware or manufacturing qualification. Only completed records determine feasibility; model-only handoff does not add routing performance.'})
 stage2src=a.small/'stage2'
 if (stage2src/'protocol.json').exists() and (stage2src/'baseline/score.json').exists():
  s2=small/'stage2';s2.mkdir(exist_ok=True);s2protocol=read(stage2src/'protocol.json');events=read(stage2src/'events.json') if (stage2src/'events.json').exists() else [];s2states=[]
  for name in ['protocol.json','assembly-contract.json','current.json','events.json','policy-comparison.json']:
   if (stage2src/name).exists():shutil.copy2(stage2src/name,s2/name)
  copytree(stage2src/'baseline',s2/'baseline')
  def scorestate(folder,title,score,event=None,preview=False):
   native=score['native'];evaluation={'accepted':score['valid'],'drc_opens':native['opens'],'all_drc_violations':native['violations'],'parity_findings':native['parity_findings'],'erc_findings':native['erc_findings'],'board_sha256':score['board_sha256']}
   (folder/'demo-native-summary.json').write_text(json.dumps(evaluation));st=state(folder,out,title,'Stage 2 preview' if preview else 'Stage 2 official formula',folder/'demo-native-summary.json',preview=preview,action=event.get('action') if event else None,retained=event.get('retained') if event else True,source=event.get('source_sha') if event else s2protocol['source_sha'],at=event.get('finished_at') if event else None)
   st.update({'score':None if preview else score,'score_receipt':str((folder/'score.json').relative_to(out)),'incumbent_score':event.get('incumbent_score') if event else score['official_formula_score'],'routing_attempted':event.get('routing_attempted') if event else None,'commands':event.get('commands') if event else [],'qualification':'Stage 2 uses complete nominal assembly and stricter native parity/ERC gates. Invalid candidates have no accepted score.'});return st
  baseline_score=read(s2/'baseline/score.json');s2states.append(scorestate(s2/'baseline','Complete-assembly valid baseline',baseline_score))
  for epoch in ['margin3','closer-packing','margin2']:
   ep=stage2src/epoch
   if (ep/'events.json').exists():
    (s2/epoch).mkdir(exist_ok=True)
    for name in ['protocol.json','events.json','current.json']:shutil.copy2(ep/name,s2/epoch/name)
    events += read(ep/'events.json')
  for event in events:
   src=Path(event['folder']);dst=s2/src.relative_to(stage2src);copytree(src,dst);score=event['result'];assert read(dst/'score.json')==score
   title=(src.parent.name+' · ' if src.parent!=stage2src else 'Initial epoch · ')+'Candidate '+str(event['index'])+' · spacing '+str(event['action'].get('spacing_factor'))
   if (dst/'preview.kicad_pcb').exists():s2states.append(scorestate(dst,title+' · proposed',score,event,True))
   s2states.append(scorestate(dst,title+(' · routed and evaluated' if event['routing_attempted'] else ' · rejected before routing'),score,event))
  current=read(s2/'current.json')
  for epoch in ['margin3','closer-packing','margin2']:
   if (s2/epoch/'current.json').exists():current=read(s2/epoch/'current.json')
  selected=s2/Path(current['folder']).relative_to(stage2src)
  if (selected/'score.json').exists():s2states.append(scorestate(selected,'Retained valid incumbent',read(selected/'score.json')))
  if (stage2src/'final-accepted/frozen.json').exists():
   copytree(stage2src/'final-accepted',s2/'final-accepted');frozen=read(s2/'final-accepted/frozen.json');score=read(s2/'final-accepted/score.json');st=scorestate(s2/'final-accepted','Frozen final · independently accepted',score);st['source']=frozen['source_sha'];st['at']=frozen['frozen_at'];st['qualification']='Frozen final. Independent native checks passed; search is completed and idle.';s2states.append(st);current={'score':score,'source_sha':frozen['source_sha'],'frozen_at':frozen['frozen_at'],'status':'completed_idle'}
  projects.insert(1,{'id':'stage2','title':'small-loop · Stage 2 score','stage':'Official formula after native and assembly gates','summary':'Baseline '+str(baseline_score['official_formula_score'])+'; last retained score '+str(current['score']['official_formula_score'])+'. All invalid proposals are rejected regardless of their smaller outline. Wire length is not the selection objective.','states':s2states,'protocol':s2protocol,'decision':{'final':current,'adaptive_margin_comparison':read(s2/'policy-comparison.json') if (s2/'policy-comparison.json').exists() else None},'limitations':'Reduced original-inspired circuit. J4 was explicitly populated with a nominal Harwin header model; complete 15-component nominal assembly. Not an official competition submission or hardware qualification. Stage 2 is separate from the earlier matched placement pilot. Candidate geometry is generated from the known valid baseline; parent_incumbent names the score comparator, not necessarily the source of the before poses.'})
 large=Path('/Users/philippe/.codex/worktrees/dc68/copper-scar/.local/large-loop');lp=large/'initial-preflight'
 if (lp/'acceptance.json').exists():
  target=raw/'large';copytree(lp,target/'initial-preflight')
  if (large/'input').exists():copytree(large/'input',target/'input')
  st=state(target/'initial-preflight',out,'large-loop · initial native screen','Input preview · no routed result',target/'initial-preflight/acceptance.json');st['qualification']='Ongoing additional size. Initial native screen is invalid; inherited header hole-clearance errors and silkscreen findings remain. No routing convergence or zero claim.'
  projects.append({'id':'large','title':'large-loop · 156 components / 164 nets','stage':'Stage 1 · input screening','summary':'472 native opens at initial screen. Additional large-loop experiment is ongoing and is not needed to release the verified small-loop and medium-loop results.','states':[st],'protocol':{'status':'initial preflight only'},'decision':None,'limitations':st['qualification']})
 m2src=a.medium/'stage2';m2=medium/'stage2';mp=next(p for p in projects if p['id']=='medium')
 if (m2src/'lineage.json').exists():
  m2.mkdir(exist_ok=True);shutil.copy2(m2src/'lineage.json',m2/'lineage.json');mp['lineage']=read(m2/'lineage.json');mp['lineage_receipt']=str((m2/'lineage.json').relative_to(out));mp['summary']='Stage 1: 183 opens → routing-only 1 → placement 0. Stage 2 starts from the explicitly selected policy incumbent; the diagnostic first-zero branch is preserved separately. Exact transition hashes are in the lineage receipt.'
 if (m2src/'baseline/score.json').exists():
  copytree(m2src/'baseline',m2/'baseline');sc=read(m2/'baseline/score.json');st=scorestate(m2/'baseline','Stage boundary · accepted-best becomes Stage 2 baseline',sc);st['source']=mp['states'][-1]['source'];st['phase']='Stage 2 official formula · same accepted circuit';st['qualification']='Explicit selected-policy branch → model-only accepted-best → identical board SHA at Stage 2 baseline. Diagnostic first-zero branch is not silently substituted.';mp['states'].append(st)
  for study_name in ['compact-v1','edge-space-v1']:
   study=m2src/study_name
   if not (study/'events.json').exists():continue
   if (study/'events.json').exists():
    dst=m2/study_name;dst.mkdir(exist_ok=True)
    for name in ['protocol.json','events.json','current.json','live-status.json']:
     if (study/name).exists():shutil.copy2(study/name,dst/name)
    for event in read(study/'events.json'):
     f=Path(event['folder']);target=dst/f.name;copytree(f,target);score=event['result'];title='medium-loop Stage 2 · '+str(event['index'])
     if (target/'preview.kicad_pcb').exists():mp['states'].append(scorestate(target,title+' · proposed',score,event,True))
     mp['states'].append(scorestate(target,title+' · evaluated',score,event))
    if (dst/'current.json').exists():mp['stage2_current']=read(dst/'current.json')
 if (large/'v1/routing-control-01/completed.json').exists():
  target=raw/'large/v1';target.mkdir(parents=True,exist_ok=True);lp=next(p for p in projects if p['id']=='large');lp['states']=[]
  for name in ['input-verified','routing-control-01','placement-01']:
   src=large/'v1'/name
   if not (src/'completed.json').exists():continue
   copytree(src,target/name);f=target/name;rec=read(f/'completed.json')
   if name=='placement-01' and (f/'preview.kicad_pcb').exists():lp['states'].append(state(f,out,'large-loop · six-swap proposal','Placement preview',f/'acceptance.json',True,action=rec.get('action'),source=rec.get('source_sha')))
   st=state(f,out,'large-loop · '+name,'Ongoing Stage 1 · saved completed record',f/'acceptance.json',action=rec.get('action'),retained=rec.get('retained'),source=rec.get('source_sha'),at=rec.get('finished_at'));st['commands']=rec.get('commands',[]);st['qualification']='Still invalid. Routing-only109 opens retained; placement proposal worsened connectivity and was rejected.';lp['states'].append(st)
  lp['summary']='472 → 109 opens from routing alone. The subsequent six-swap placement trial worsened opens to 345 and was rejected. 84 inherited required findings remain; no accepted large-loop result.'
 if (m2src/'final-accepted/frozen.json').exists():
  f=m2/'final-accepted';copytree(m2src/'final-accepted',f);fr=read(f/'frozen.json');sc=read(f/'score.json');st=scorestate(f,'medium-loop · independently frozen Stage 2 final',sc);st['source']=fr['source_sha'];st['phase']='Stage 2 official formula · frozen final';st['qualification']='Stage 1 accepted-best → identical Stage 2 seed → valid score improvement. Fresh independent native + complete assembly checks passed. Search completed.';mp['states'].append(st)
 status=read(a.status) if a.status else {}
 if 'current' in locals() and current.get('status')=='completed_idle':status['stage2']={'state':'completed_idle','operation':'Search frozen; replay available','last_completed_at':current['frozen_at'],'text':'COMPLETED / IDLE · search frozen · retained official score '+str(current['score']['official_formula_score'])+' · last completed '+current['frozen_at']}
 if (stage2src/'live-status.json').exists():
  source_status=read(stage2src/'live-status.json');shutil.copy2(stage2src/'live-status.json',small/'stage2/live-status.json');status['stage2'].update({'native_status':source_status})
 status['medium']={'state':'completed_checkpoint','text':'Last completed native checkpoint: 0 opens / 0 DRC / ERC 0. Subsequent work, if any, is outside this saved checkpoint.'}
 if (m2src/'compact-v1/live-status.json').exists():status['medium']['stage2_status']=read(m2src/'compact-v1/live-status.json')
 if (out/'remote').exists():
  remote_links=[]
  for name in ['small-verified.json','stage2-chapter-verified.json']:
   if (out/'remote'/name).exists():
    r=read(out/'remote'/name);remote_links += [{'label':name.replace('-verified.json','')+' · W&B','url':r['run_url']},{'label':name.replace('-verified.json','')+' · Weave','url':r['trace_url']}]
 else:remote_links=[]
 if (a.medium/'observability/verified.json').exists():
  r=read(a.medium/'observability/verified.json');(out/'remote').mkdir(exist_ok=True);shutil.copy2(a.medium/'observability/verified.json',out/'remote/medium-verified.json')
  for run in r['runs']:
   remote_links.append({'label':'medium-loop · '+run['id'],'url':run['url']})
   for row in run['verified_rows']:
    remote_links.append({'label':'medium-loop · decision '+str(row['decision'])+' · trace','url':'https://wandb.ai/philippe-fdesousa/copper-scar/r/call/'+row['call_id']})
 data={'remote':remote_links,'live':True,'title':'PCB Loop','generated_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'snapshot':True,'projects':projects,'status':status,'official_formula':'PCBA bounding-box volume (mm³) + 50 × vias + 5000 × copper layers','qualification':'Stage 2 score is considered only after native feasibility and complete-assembly validation. Lower is better. Wire length is a separate proxy.'}
 (out/'data.json.tmp').write_text(json.dumps(data,indent=2));(out/'data.json.tmp').replace(out/'data.json');(out/'data.js.tmp').write_text('window.DATA='+json.dumps(data)+';');(out/'data.js.tmp').replace(out/'data.js');shutil.copy2(Path(__file__).with_name('index.html'),out/'index.html');print(json.dumps({'out':str(out),'states':{p['id']:len(p['states']) for p in projects},'data_sha256':sha(out/'data.json')}))
if __name__=='__main__':main()
