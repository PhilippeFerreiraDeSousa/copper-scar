#!/usr/bin/env python3
"""Build an isolated, evidence-bound outer-loop view; never route or modify source CAD."""
import collections,datetime,hashlib,json,re,shutil,subprocess
from pathlib import Path
ROOT=Path('/Users/philippe/dev/copper-scar-demo/.local/copperhead')
OUT=Path('/Users/philippe/Documents/Codex/2026-09-12/realtime-voice-chat/outputs/latest-loop-experiments')
CLI='/Users/philippe/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli'
LAYERS=['F.Cu','In1.Cu','In2.Cu','In3.Cu','In4.Cu','B.Cu']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2))
def parse(path):
 stack=[]
 for t in re.findall(r'"(?:\\.|[^"\\])*"|[()]|[^\s()]+',path.read_text()):
  if t=='(':
   n=[]
   if stack:stack[-1].append(n)
   stack.append(n)
  elif t==')':root=stack.pop()
  else:stack[-1].append(json.loads(t) if t.startswith('"') else t)
 return root
 def_unused=None
def nodes(x,k):return [n for n in x if isinstance(n,list) and n and n[0]==k]
def one(x,k,default=None):return next(iter(nodes(x,k)),[k]+(default or []))[1:]
def inventory(p):
 root=parse(p);poses={};vias={};tracks={}
 for x in root[1:]:
  if not isinstance(x,list):continue
  if x[0]=='footprint':
   ref=next(n[2] for n in nodes(x,'property') if n[1]=='Reference');at=one(x,'at');poses[ref]=[float(at[0]),float(at[1]),float(at[2]) if len(at)>2 else 0,one(x,'layer')[0]]
  if x[0]=='via':
   uid=one(x,'uuid')[0];vias[uid]={'uuid':uid,'at':list(map(float,one(x,'at')[:2])),'diameter':float(one(x,'size')[0]),'drill':float(one(x,'drill')[0]),'layers':one(x,'layers'),'net':one(x,'net'),'raw':x}
  if x[0] in ('segment','arc'):tracks[one(x,'uuid')[0]]=x
 return poses,vias,tracks
cache={}
def stage(p,e):
 assert p.exists();h=sha(p)
 if e:assert e['files']['pcbgolf.kicad_pcb']==h,(p,h,e['files']['pcbgolf.kicad_pcb'])
 if h not in cache:
  dest=OUT/'boards'/h;dest.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest/'board.kicad_pcb');shutil.copy2(p.with_suffix('.kicad_pro'),dest/'board.kicad_pro')
  for layer in ['all']+LAYERS:
   svg=dest/(layer+'.svg')
   if not svg.exists():
    subprocess.run([CLI,'pcb','export','svg','--layers',','.join((LAYERS if layer=='all' else [layer])+['F.SilkS','Edge.Cuts']),'--mode-single','--page-size-mode','0','--exclude-drawing-sheet','-o',str(svg),str(dest/'board.kicad_pcb')],check=True,capture_output=True)
    s=svg.read_text();s=re.sub(r'width="[^"]+mm" height="[^"]+mm" viewBox="[^"]+"','width="140mm" height="105mm" viewBox="100 50 140 105"',s,count=1);svg.write_text(s)
  assert sha(p)==h and sha(dest/'board.kicad_pcb')==h
  cache[h]={'sha256':h,'board':str((dest/'board.kicad_pcb').relative_to(OUT)),'base':str(dest.relative_to(OUT)),'source':str(p)}
 return {**cache[h],'cost':{k:e[k] for k in ['unconnected','errors','warnings']} if e else None,'check':e.get('zone_fill_check','historical native unsaved refill') if e else 'No evaluation supplied'}
OUT.mkdir(parents=True,exist_ok=True)
rows=[];excluded=[];cutoff='stage1-20260913-073500-b3f12a'
for q in sorted((ROOT/'runs').glob('*/attempt.json')):
 d=json.loads(q.read_text());uid=d['attempt']
 if not ('stage1-20260913-044612-074e42'<=uid<=cutoff):continue
 kind=d.get('action',{}).get('kind');route=d.get('routing_scope',{})
 if d.get('status')!='completed' or kind not in ('group_pose','via_seed','via_consolidation','local_topology_replan') or route.get('kind')!='whole_board':
  excluded.append({'id':uid,'reason':'Not a completed component move or explicit via edit followed by whole-board routing'});continue
 assert route['net_filter'] is None and route['completion']=='routed_and_natively_evaluated'
 scope=route['execution'].get('scope_evidence',{})
 if not scope:scope=route['execution'].get('scope',{})
 # Scope proof can be nested in execution; locate native route coverage in candidate.
 cp=Path(d['candidate']);coverage=json.loads((cp/'routing-coverage.json').read_text()) if (cp/'routing-coverage.json').exists() else scope
 assert coverage.get('all_exported_nets_eligible') and coverage['layers']==LAYERS,(uid,coverage.keys())
 name,ev={'group_pose':('placement-project','placement_evaluation'),'via_seed':('via-seed-project','via_seed_evaluation'),'via_consolidation':('via-consolidation-project','via_consolidation_evaluation'),'local_topology_replan':('topology-replan-project','topology_preflight')}[kind]
 before=q.parent/'input/pcbgolf.kicad_pcb';pre=q.parent/name/'pcbgolf.kicad_pcb';after=cp/'pcbgolf.kicad_pcb'
 states=[stage(before,d['before']),stage(pre,d.get(ev)),stage(after,d['after'])]
 a,av,at=inventory(before);b,bv,bt=inventory(pre);c,cv,ct=inventory(after)
 moved=[{'ref':ref,'before':a[ref],'after':b[ref]} for ref in a if a[ref]!=b[ref]]
 added=[bv[k] for k in bv.keys()-av.keys()];removed=[av[k] for k in av.keys()-bv.keys()];changed=[{'before':av[k],'after':bv[k]} for k in av.keys()&bv.keys() if av[k]['raw']!=bv[k]['raw']]
 for v in added+removed:v.pop('raw',None)
 for v in changed:v['before'].pop('raw',None);v['after'].pop('raw',None)
 assert moved or added or removed or changed,uid
 evidence=OUT/'evidence'/uid;evidence.mkdir(parents=True,exist_ok=True);shutil.copy2(q,evidence/'attempt.json');write(evidence/'coverage.json',coverage)
 for label,e in [('before',d['before']),('pre-route',d.get(ev)),('after',d['after'])]:write(evidence/(label+'.json'),e)
 for f in ['retention-correction.json','final-pad-partitions.json','final-via-geometry.json','terminal-scope-correction.json','final-topology-widths.json','topology-proposal.json']:
  if (q.parent/f).exists():shutil.copy2(q.parent/f,evidence/f)
 command=next(x for x in d['commands'] if 'whole-board' in ' '.join(x.get('argv',[])) or x.get('argv',[])[1:2]==[str(Path('/Users/philippe/dev/copper-scar-demo/scripts/copperhead_route.py'))])
 assert command['returncode']==0 and not command['timed_out']
 rows.append({'id':uid,'kind':kind,'started':d['started_at'],'finished':d['finished_at'],'retained':d['became_incumbent'],'states':states,'poses':moved,'vias_added':added,'vias_removed':removed,'vias_changed':changed,'tracks_removed_pre':len(at.keys()-bt.keys()),'removed_track_segments':[{'start':list(map(float,one(at[k],'start'))),'end':list(map(float,one(at[k],'end'))),'layer':one(at[k],'layer')[0]} for k in at.keys()-bt.keys() if at[k][0]=='segment'],'tracks_added_pre':len(bt.keys()-at.keys()),'postroute_via_count':len(cv),'preroute_via_count':len(bv),'budget':route['effort_limit_seconds'],'elapsed':command['elapsed_seconds'],'pass_limit':route['pass_limit'],'evidence':str(evidence.relative_to(OUT)),'reason':d['action']['reason'],'decision':d.get('selection_decision'),'parent_is_retained':(d.get('incumbent_before') or {}).get('candidate')==d.get('input'),'after_check':d['after'].get('zone_fill_check','historical unsaved native refill')})
 print('verified',uid,len(moved),len(added),len(removed),flush=True)
pending_id='stage1-20260913-073500-b3f12a';pending_record=json.loads((ROOT/'runs'/pending_id/'attempt.json').read_text());write(OUT/'evidence/pending-at-snapshot.json',pending_record)
pending={'id':pending_id,'status_at_capture':pending_record['status'],'started':pending_record['started_at'],'note':'Completed and included as the final rejected experiment. No active result is inferred beyond this frozen cutoff.'}
data={'built_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'cutoff':cutoff,'rows':rows,'pending':pending,'excluded':excluded,'layers':LAYERS}
write(OUT/'data.json',data);(OUT/'data.js').write_text('window.LOOP='+json.dumps(data)+';');shutil.copy2(Path(__file__).with_name('index.html'),OUT/'index.html')
write(OUT/'SHA256SUMS.json',{str(p.relative_to(OUT)):sha(p) for p in OUT.rglob('*') if p.is_file() and p.name!='SHA256SUMS.json'})
print('DONE',len(rows),len(cache),flush=True)
