#!/usr/bin/env python3
"""Mirror durable experiment events and make a local replay without touching owner CAD."""
import argparse,datetime,fcntl,hashlib,json,os,re,shutil,subprocess,time
from pathlib import Path
from model import read_events,fold,sha,canon
from cad import parse,nodes,one,inventory
from summaries import summarize
LAYERS=('F.Cu','In1.Cu','In2.Cu','In3.Cu','In4.Cu','B.Cu')
CLI=os.environ.get('KICAD_CLI') or shutil.which('kicad-cli') or '/Users/philippe/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli'
def atomic(p,text):
 p.parent.mkdir(parents=True,exist_ok=True);temp=p.with_name(p.name+'.tmp');temp.write_text(text);os.replace(temp,p)
def append(p,text):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('a') as f:f.write(text);f.flush();os.fsync(f.fileno())
def asset(path,expected,out):
 p=Path(path);assert expected and sha(p)==expected,('Missing hash or board drift',str(p));dest=out/'boards'/expected;dest.mkdir(parents=True,exist_ok=True);board=dest/'board.kicad_pcb'
 if not board.exists():shutil.copy2(p,board)
 assert sha(board)==expected
 for layer in LAYERS:
  svg=dest/(layer+'.svg')
  if not svg.exists():
   subprocess.run([CLI,'pcb','export','svg','--layers',layer+',F.SilkS,Edge.Cuts','--mode-single','--page-size-mode','0','--exclude-drawing-sheet','-o',str(svg),str(board)],check=True,capture_output=True)
   s=svg.read_text();s=re.sub(r'width="[^"]+mm" height="[^"]+mm" viewBox="[^"]+"','width="140mm" height="105mm" viewBox="100 50 140 105"',s,count=1);svg.write_text(s)
 assert sha(p)==expected
 return {'board':str(board.relative_to(out)),'base':str(dest.relative_to(out)),'sha256':expected,'source':str(p)}
def focus_stages(stages,out):
 if len(stages)<2 or not all(s.get('board') for s in stages[:2]):return
 pa,va,_=inventory(out/stages[0]['board']);pb,vb,_=inventory(out/stages[1]['board']);refs=[r for r in pa if r in pb and pa[r]!=pb[r]];newvias=[vb[k] for k in vb.keys()-va.keys()]
 sites=[pos[:2] for r in refs for pos in (pa[r],pb[r])]+[v['at'] for v in newvias]
 if not sites:return
 xmin=min(p[0] for p in sites);xmax=max(p[0] for p in sites);ymin=min(p[1] for p in sites);ymax=max(p[1] for p in sites);w=max(30,xmax-xmin+20,(ymax-ymin+16)*4/3);h=w*3/4;box=[(xmin+xmax-w)/2,(ymin+ymax-h)/2,w,h];tag=hashlib.sha256(canon(box).encode()).hexdigest()[:10]
 for i,stage in enumerate(stages):
  if not stage.get('board'):continue
  poses=pa if i==0 else pb;marks=''.join(f'<circle cx="{poses[r][0]}" cy="{poses[r][1]}" r="1.8" fill="none" stroke="#56dbff" stroke-width="0.25"/>' for r in refs)
  if i:marks+=''.join(f'<circle cx="{v["at"][0]}" cy="{v["at"][1]}" r="1.4" fill="none" stroke="#ffd166" stroke-width="0.25"/>' for v in newvias)
  stage['focus_svg']={}
  for layer in LAYERS:
   source=out/stage['base']/(layer+'.svg');dest=source.with_name('focus-'+tag+'-'+layer+'.svg')
   if not dest.exists():
    text=source.read_text();text=re.sub(r'viewBox="[^"]+"','viewBox="'+' '.join(map(str,box))+'"',text,count=1);text=text.replace('</svg>',marks+'</svg>');dest.write_text(text)
   stage['focus_svg'][layer]=str(dest.relative_to(out))

def build(source,out):
 manifest=json.loads((source/'manifest.json').read_text());raw,events=read_events(source/'events.jsonl');mirror=out/'events.jsonl';old=mirror.read_bytes() if mirror.exists() else b'';assert raw.startswith(old),'Source event log rewritten/truncated'
 if len(raw)>len(old):append(mirror,raw[len(old):].decode())
 h=hashlib.sha256(canon(manifest).encode()).hexdigest();mp=out/'manifests'/f'{h}.json'
 if not mp.exists():atomic(mp,json.dumps(manifest,indent=2))
 state=fold(manifest,events);state['built_at']=datetime.datetime.now(datetime.timezone.utc).isoformat();state['manifest_sha256']=h;state['events_sha256']=hashlib.sha256(raw).hexdigest();state['source_path']=str(source)
 event_snapshot=out/'manifests'/('events-'+state['events_sha256']+'.jsonl')
 if not event_snapshot.exists():atomic(event_snapshot,raw.decode())
 state['events_snapshot_href']=str(event_snapshot.relative_to(out))
 for policy in state['policies']:
  incumbent=None
  active=policy.get('active_index')
  if active and not state['fixture']:
   commands=list((source/policy['id']/f'{active:02d}').rglob('*.command.json'))
   if commands:
    cp=max(commands,key=lambda p:p.stat().st_mtime)
    try:
     c=json.loads(cp.read_text());policy['runtime_observation']={k:c.get(k) for k in ['heartbeat_at','state','pid','started_at','elapsed_seconds']};policy['runtime_observation'].update(source=str(cp),observed_at=state['built_at'])
    except (OSError,json.JSONDecodeError):pass
  if active and not state['fixture']:
   original=policy.get('active_input',{});selected=policy.get('active_proposal',{}).get('action',{}).get('id')
   screened=next((r for r in reversed(policy.get('screened',[])) if r.get('index')==active and r.get('action',{}).get('id')==selected),None)
   policy['active_stages']=[]
   if original.get('input_board_path') and original.get('input_board_sha256'):policy['active_stages'].append({'name':'Original active decision input',**asset(original['input_board_path'],original['input_board_sha256'],out)})
   else:policy['active_stages'].append({'name':'Original input','missing':'No verified source yet'})
   if screened:
    path=screened.get('preview_after_board_path',screened.get('pre_board_path'));h=screened.get('preview_after_board_sha256',screened.get('pre_board_sha256'))
    if path and h:policy['active_stages'].append({'name':'Actual updated pre-route preview','nativecost':screened.get('nativecost'),**asset(path,h,out)})
   if len(policy['active_stages'])<2:policy['active_stages'].append({'name':'Updated pre-route','missing':'Screening or selection pending'})
   policy['active_stages'].append({'name':'After routing','missing':'PENDING: no completed full-route result'})
  for point in policy['points']:
   record=point.pop('record');point['stages']=[]
   if record and not state['fixture']:
    rp=Path(point['receipt']);run=rp.parent;evidence=out/'attempts'/record['attempt'];evidence.mkdir(parents=True,exist_ok=True);target=evidence/'attempt.json';text=rp.read_text()
    if target.exists():assert target.read_text()==text,'Completed receipt changed'
    else:target.write_text(text)
    point['receipt_href']=str(target.relative_to(out));point['receipt_sha256']=sha(target);point['decision']=record.get('selection_decision');point['action']=record.get('action');point['configured_seconds']=record.get('routing_scope',{}).get('effort_limit_seconds');point['realization_context']=record.get('realization_context')
    for name,p,ev in [('Original',run/'input/pcbgolf.kicad_pcb',record.get('before')),('Updated pre-route',run/'placement-project/pcbgolf.kicad_pcb',record.get('placement_evaluation'))]:
     if name=='Updated pre-route':
      for folder,key in [('topology-replan-project','topology_preflight'),('via-seed-project','via_seed_evaluation'),('via-consolidation-project','via_consolidation_evaluation'),('fanout-project','fanout_evaluation')]:
       if (run/folder/'pcbgolf.kicad_pcb').exists():p=run/folder/'pcbgolf.kicad_pcb';ev=record.get(key);break
     if p.exists() and ev:point['stages'].append({'name':name,'cost':ev,**asset(p,ev['files']['pcbgolf.kicad_pcb'],out)})
     else:point['stages'].append({'name':name,'missing':'No verified immutable snapshot supplied'})
    after=record.get('after')
    if after:point['stages'].append({'name':'After full routing','cost':after,**asset(Path(record['candidate'])/'pcbgolf.kicad_pcb',after['files']['pcbgolf.kicad_pcb'],out)})
    if incumbent is None and point['stages'] and point['stages'][0].get('board'):incumbent=point['stages'][0]
    if point['retained'] and after:incumbent=point['stages'][-1]
    cmd=next((x for x in record.get('commands',[]) if any(str(a).endswith('copperhead_route.py') for a in x.get('argv',[]))),None)
    point['route_elapsed_seconds']=cmd['elapsed_seconds'] if cmd else None
    via_proof=run/'final-via-geometry.json'
    if via_proof.exists():shutil.copy2(via_proof,evidence/via_proof.name)
    proof=run/'final-pad-partitions.json'
    if proof.exists():
     pp=json.loads(proof.read_text());shutil.copy2(proof,evidence/proof.name);point['pad_partition_proof_href']=str((evidence/proof.name).relative_to(out));point['split_groups']=pp.get('split_groups',[])
     pads={}
     for footprint in nodes(parse(run/'input/pcbgolf.kicad_pcb'),'footprint'):
      ref=next((n[2] for n in nodes(footprint,'property') if n[1]=='Reference'),'?')
      for pad in nodes(footprint,'pad'):
       uid=one(pad,'uuid');net=one(pad,'net');pads[uid[0]]={'pad':ref+'.'+pad[1],'net':net[-1] if net else '?'}
     point['split_pad_groups']=[[pads.get(uid,{'uuid':uid}) for uid in group] for group in point['split_groups']]
    if len(point['stages'])>=2 and all(t.get('board') for t in point['stages'][:2]):
     pa,va,ta=inventory(out/point['stages'][0]['board']);pb,vb,tb=inventory(out/point['stages'][1]['board']);point['actual_edits']={'poses':[{'ref':ref,'before':pa[ref],'after':pb[ref]} for ref in pa if ref in pb and pa[ref]!=pb[ref]],'vias_added':len(vb.keys()-va.keys()),'vias_removed':len(va.keys()-vb.keys()),'tracks_added':len(tb.keys()-ta.keys()),'tracks_removed':len(ta.keys()-tb.keys())}
    def normalized_warning(v):return {k:([{kk:vv for kk,vv in item.items() if kk!='uuid'} for item in value] if k=='items' else value) for k,value in v.items()}
    before_warnings={canon(normalized_warning(v)) for v in record.get('before',{}).get('violations',[]) if v.get('severity')=='warning'}
    point['new_warnings']=[normalized_warning(v) for v in record.get('after',{}).get('violations',[]) if v.get('severity')=='warning' and canon(normalized_warning(v)) not in before_warnings]
    point['updates']={'component_refs':record.get('action',{}).get('refs',[]),'pose':record.get('placement_delta'),'via_seed':record.get('via_seed'),'topology':record.get('topology_replan'),'effects':record.get('effects')}
   elif point['index']==0 and not state['fixture']:
    lower=point['raw_lower'];p=lower.get('retained_board_path',lower.get('board_path',lower.get('board')));expected=lower.get('retained_board_sha256',lower.get('board_sha256'))
    if p and expected:incumbent=asset(p,expected,out);point['stages']=[{'name':'Initial native baseline; no routing',**incumbent}]
   lower=point['raw_lower']
   if not state['fixture'] and lower.get('retained_board_path') and lower.get('retained_board_sha256'):incumbent=asset(lower['retained_board_path'],lower['retained_board_sha256'],out)
   if not point['stages'] and not state['fixture'] and lower.get('pre_board_path') and lower.get('pre_board_sha256'):point['stages']=[{'name':'Precheck only; no full routing',**asset(lower['pre_board_path'],lower['pre_board_sha256'],out)}]
   point['incumbent']=incumbent
   # Keep detailed evaluations once in the copied receipt, not repeated in live JSON.
   for stage in point['stages']:
    if isinstance(stage.get('cost'),dict):stage['cost']={k:stage['cost'].get(k) for k in ('unconnected','errors','warnings','invariants_ok','validity_gate','zone_fill_check')}
  focus_stages(policy.get('active_stages',[]),out)
  for point in policy['points']:focus_stages(point['stages'],out)
  for point in policy['points']:
   if point.get('receipt_href'):point['evidence_summary']=summarize(policy,point)
  policy['route_wall_seconds']=sum(p.get('route_elapsed_seconds') or 0 for p in policy['points'] if p['index']!=0)
 state['full_evidence_receipts']=json.loads((out/'remote/complete-evidence-verified.json').read_text()) if (out/'remote/complete-evidence-verified.json').exists() else []
 state['decision_artifacts']=[]
 for relative in ['decision.json','selected-policy.json','next-campaign/consumed-decision.json','next-campaign/screens.json','next-campaign/result.json']:
  source_file=source/relative
  if source_file.exists():
   artifact_raw=source_file.read_bytes()
   try:payload=json.loads(artifact_raw)
   except json.JSONDecodeError:continue
   digest=hashlib.sha256(artifact_raw).hexdigest();target=out/'decisions'/(source_file.stem+'-'+digest[:12]+'.json');atomic(target,artifact_raw.decode());state['decision_artifacts'].append({'kind':relative,'sha256':digest,'href':str(target.relative_to(out)),'payload':payload})
 state['remote_receipts']=json.loads((out/'remote/verified.json').read_text()) if (out/'remote/verified.json').exists() else None
 atomic(out/'data.json',json.dumps(state,indent=2));atomic(out/'data.js','window.EXPERIMENT='+json.dumps(state)+';');shutil.copy2(Path(__file__).with_name('index.html'),out/'index.html')
 append(out/'ingestion-receipts.jsonl',json.dumps({'at':state['built_at'],'source_event_bytes':len(raw),'events_sha256':state['events_sha256'],'manifest_sha256':state['manifest_sha256'],'event_count':len(events),'data_sha256':sha(out/'data.json')})+'\n')
 print(json.dumps({'at':state['built_at'],'fixture':state['fixture'],'events':len(events),'policies':[(p['id'],p['completed_attempts']) for p in state['policies']]}),flush=True);return state
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--watch',action='store_true');a=ap.parse_args();a.output.mkdir(parents=True,exist_ok=True);lock=(a.output/'build.lock').open('a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 while True:
  if (a.source/'manifest.json').exists() and (a.source/'events.jsonl').exists():build(a.source,a.output)
  if not a.watch:break
  time.sleep(30)
