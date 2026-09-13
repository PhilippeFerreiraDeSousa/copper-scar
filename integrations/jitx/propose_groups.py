"""A deterministic circuit-block floorplan proposal from actual inter-group net topology.
Ranks a small five-block slot catalog; internal part relationships stay rigid.
Component-center HPWL is a proposal heuristic, not SI/DRC/route validity.
"""
from pathlib import Path
import itertools,json,math,sys
from placement_audit import inventory
B=Path('/Users/philippe/dev/copper-scar-jitx');L=B/'runs/stage1'
def rotate(p,a):
 a=math.radians(a);return(p[0]*round(math.cos(a),10)-p[1]*round(math.sin(a),10),p[0]*round(math.sin(a),10)+p[1]*round(math.cos(a),10))
def propose(capture,out):
 messages=json.loads(capture.read_text());poses,board=inventory(messages);groups=sorted({p['path'].split('.')[0] for p in poses.values()})
 old={'CAN_FD':(16.1654,30.6281),'Channels':(14.69102,36.8226),'Power':(13.1686,29.4321),'STM32H7':(13.1686,30.0951),'USB__SD':(16.1654,34.9591)}
 centers={}
 for g in groups:
  pts=[(p['x'],p['y']) for p in poses.values() if p['path'].split('.')[0]==g];centers[g]=tuple((min(p[i] for p in pts)+max(p[i] for p in pts))/2 for i in [0,1])
 padref={ob['pad']:i['designator'] for g in board['module']['groups'] for i in g['instances'] for ob in i['objects'] if 'pad' in ob}
 nets=next(m['body']['nets'] for m in messages if m['type']=='nets' and m['body'].get('complete'))
 cross=[]
 for n in nets:
  refs={padref[p] for c in n['connected'] for p in c.get('pads',[]) if p in padref};local={}
  for ref in refs:
   p=poses[ref];local.setdefault(p['path'].split('.')[0],[]).append((p['x'],p['y']))
  if len(local)<2:continue
  endpoints={g:tuple(sum(p[i] for p in pts)/len(pts)-centers[g][i] for i in [0,1]) for g,pts in local.items()}
  cross.append({'name':n['name'],'endpoints':endpoints,'weight':0.1 if len(refs)>30 else 1.0,'refs':len(refs)})
 slots=[(-80,40),(0,40),(80,40),(-40,-45),(40,-45)]
 def score(assignment,angles):
  total=0
  for n in cross:
   pts=[]
   for g,v in n['endpoints'].items():
    v=rotate(v,angles[g]);s=assignment[g];pts.append((v[0]+s[0],v[1]+s[1]))
   total+=n['weight']*sum(max(p[i] for p in pts)-min(p[i] for p in pts) for i in [0,1])
  return total
 best=None
 for perm in itertools.permutations(slots):
  ass=dict(zip(groups,perm));ang={g:0 for g in groups}
  for _ in range(2):
   for g in groups:ang[g]=min([0,90,180,270],key=lambda a:score(ass,{**ang,g:a}))
  s=score(ass,ang)
  if best is None or s<best[0]:best=(s,ass,ang.copy())
 value,assignment,angles=best;params={};moves={}
 for g in groups:
  v=rotate((centers[g][0]-old[g][0],centers[g][1]-old[g][1]),angles[g]);origin=(assignment[g][0]-v[0],assignment[g][1]-v[1]);params['Main.'+g]={'x':round(origin[0],6),'y':round(origin[1],6),'angle':angles[g],'side':'top'}
  for ref,p in poses.items():
   if p['path'].split('.')[0]!=g:continue
   v=rotate((p['x']-old[g][0],p['y']-old[g][1]),angles[g]);moves[ref]={'x':round(v[0]+origin[0],6),'y':round(v[1]+origin[1],6),'angle':(p['angle']+angles[g])%360,'side':p['side']}
 result={'action_kind':'multiple circuit-group translations and rotations','capture':str(capture),'groups':groups,'component_count':len(moves),'overrides':params,'moves':moves,'heuristic':{'name':'weighted component-center intergroup HPWL','value_mm':value,'intergroup_nets':cross,'slots':slots,'assignment':assignment,'angles':angles,'notes':'Global nets with >30 component references weight .1; others1. Local component relationships preserved exactly. 120 slot permutations with two deterministic rotation sweeps. No claim that distance proxy improves route/SI.'},'rationale':'Imported five circuit groups occupy interleaved bounding boxes. Separate blocks with routing corridors, choose block assignments from actual cross-group nets. Explicit floorplan exploration; connector access/assembly and signal integrity remain unqualified.'}
 out.write_text(json.dumps(result,indent=2));return result
if __name__=='__main__':
 r=propose(Path(sys.argv[1]),Path(sys.argv[2]));print(json.dumps({k:r[k] for k in ['groups','component_count','overrides','rationale']},indent=2))
