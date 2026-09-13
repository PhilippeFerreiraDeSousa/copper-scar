"""One presentation contract for native records across board sizes.

Stage 1 ends only at a source-backed full gate. Later feasibility records remain
in history. Candidate measurements and retained search incumbents are distinct.
"""
import copy,json
from pathlib import Path

def fully_valid(s,out):
 score=s.get('score')
 if score:
  n=score.get('native',{});return score.get('valid') is True and all(n.get(k)==0 for k in ['opens','violations','parity_findings','erc_findings'])
 if s.get('handoff_receipt'):
  h=json.loads((out/s['handoff_receipt']).read_text());e=h.get('evaluation',{})
  return h.get('accepted') is True and h.get('erc_violations')==0 and e.get('drc_opens')==0 and e.get('all_drc_violations')==0 and e.get('schematic_parity_issues')==0
 return False

def annotate(states,out):
 best=None;best_score=None
 for n,s in enumerate(states):
  s['checkpoint']=n;s['full_gate_pass']=fully_valid(s,out);e=s.get('evaluation');score=s.get('score')
  if score:
   s['stage_number']=2;s['candidate_score']=score.get('official_formula_score');s['score_valid']=score.get('valid')
   if score.get('valid') and (best_score is None or score['official_formula_score']<best_score['official_formula_score']):best_score=score
   s['retained_score']=best_score['official_formula_score'] if best_score else None
   s['retained_terms']=best_score.get('terms') if best_score else None
   ctx=s.get('proposal_context',{});parent=Path(ctx.get('parent_incumbent',''))/'score.json';geometry=Path(ctx.get('proposal_source',''))/'score.json'
   if parent.is_file():
    previous=json.loads(parent.read_text());s['comparison']={'before_score':previous['official_formula_score'],'before_terms':previous['terms'],'actual_term_deltas':{k:score['terms'][k]-previous['terms'][k] for k in ['pcba_bbox_volume_mm3','via_penalty','layer_penalty']},'score_delta':score['official_formula_score']-previous['official_formula_score'] if score.get('valid') else None}
   if geometry.is_file():
    g=json.loads(geometry.read_text());s['geometry_reference']={'source':ctx.get('proposal_source'),'assembly':g.get('assembly'),'board_sha256':g.get('board_sha256')}
    match=next((x for x in states if x['board']['sha256']==g.get('board_sha256')),None)
    if match:s['geometry_reference']['outline_mm']=match['board'].get('size_mm')
  else:s['stage_number']=2 if s['phase'].startswith('Stage 2') else 1
  if e:
   opens=e.get('drc_opens',e.get('native_open_count',e.get('unconnected')));required=len(e['required_violations']) if 'required_violations' in e else e.get('errors',e.get('all_drc_violations',0));loss=e.get('feasibility_cost',opens+required if opens is not None else None)
   s['candidate_native']={'opens':opens,'required_findings':required,'loss':loss,'all_drc_findings':e.get('all_drc_violations'),'fully_valid':s['full_gate_pass']}
   if best is None or s.get('retained') is True:best=s['candidate_native']
   s['retained_native']=copy.deepcopy(best)
  else:s['candidate_native']=None;s['retained_native']=copy.deepcopy(best)
 return states

def normalize(data,out):
 out=Path(out);by={p['id']:p for p in data['projects']};families=[]
 small=copy.deepcopy(by['small']);stage2=copy.deepcopy(by['stage2']);small['history_states']=small['states'][2:];small['states']=small['states'][:2]+stage2['states'];small['id']='small';small['family']='small-loop';small['title']='small-loop · 15 components / 11 nets';small['stage']='Stage 1 gate → Stage 2 official objective';small['status_key']='stage2';small['summary']='Routing alone reaches zero opens. Full current native and assembly gates are established at the explicitly documented complete-model baseline; then Stage 2 optimizes the official score. Earlier flat-zero ranking comparisons are history, not feasibility progress.';small['decision']={'historical_ranking':small.get('decision'),'stage2':stage2.get('decision')};small['phase_boundary']='The complete-model baseline includes the explicit populated-header/BOM and global-net-label metadata contract; no hidden circuit change is inferred.';families.append(small)
 medium=copy.deepcopy(by['medium']);main=[];history=[];boundary=False
 for s in medium['states']:
  is_history='policy pilot' in s['phase'].lower() or s['phase']=='Model-complete policy incumbent'
  if is_history:history.append(s);continue
  if s.get('handoff_receipt') and fully_valid(s,out) and not boundary:s['title']='Stage 1 stops here · first fully valid handoff';s['qualification']='All required native gates passed. Further feasibility optimization is historical, not part of this Stage 1 run.';boundary=True
  main.append(s)
 # The recorded Stage 2 seed came from the historical comparison; expose it as a selection transition.
 at=next((i for i,s in enumerate(main) if s.get('score')),len(main))
 chosen=next((s for s in history if s['phase']=='Model-complete policy incumbent'),None)
 if chosen:
  chosen=copy.deepcopy(chosen);chosen['title']='Historical variant explicitly selected as Stage 2 seed';chosen['phase']='Selection transition · not further Stage 1 search';chosen['qualification']='The first valid Stage 1 run already ended. This historical selected variant was used by the recorded Stage 2 experiment. See exact hashes in the lineage and comparison records.';main.insert(at,chosen)
 medium.update({'family':'medium-loop','history_states':history,'states':main,'status_key':'medium','stage':'Stage 1 first-valid stop → explicit selection → Stage 2','summary':'Stage 1 ends at its first full native gate. The recorded Stage 2 experiment used a later historical policy variant; that selection is shown explicitly. Flat-zero policy trials are separated into history.'});families.append(medium)
 for id in ['large','original']:
  if id in by:
   p=copy.deepcopy(by[id]);p['family']='large-loop' if id=='large' else 'original-full';p['status_key']=id;p.setdefault('history_states',[]);families.append(p)
 for p in families:
  annotate(p['states'],out);annotate(p['history_states'],out)
  valid=[s for s in p['states'] if s.get('score_valid')]
  if valid:p['global_best_score']=min(s['candidate_score'] for s in valid)
  catalog={}
  for s in p['states']+p['history_states']:
   a=s.get('action') or {};kind=(a.get('source_primitive') or {}).get('kind') or a.get('kind')
   if not kind:continue
   key=str(s['stage_number'])+'/'+kind;entry=catalog.setdefault(key,{'stage':s['stage_number'],'primitive':kind,'examples':[]})
   ex={k:a[k] for k in ['spacing_factor','x_factor','y_factor','edge_margin_mm','x_margin_mm','y_margin_mm','components','delta_mm','copper_layers','seed_copper'] if k in a}
   if ex and ex not in entry['examples'] and len(entry['examples'])<3:entry['examples'].append(ex)
  p['update_space']=catalog
 data['schema_version']=2;data['projects']=families;data['view_contract']={'stage1_stop':'first full source-backed native acceptance','native_plot':'candidate and retained missing connections are distinct','score_plot':'only valid official scores; invalid candidate score is null','history':'Later feasibility policy trials stay auditable outside the main Stage 1 timeline'}
 return data
