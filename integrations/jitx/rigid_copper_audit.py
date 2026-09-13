"""Check exact copper primitives after measured rigid block motion, without editing boards."""
from pathlib import Path
import json,math,sys,collections
from copper_audit import copper
from import_experiments import parse,children,one
from placement_audit import inventory

def audit(before,after,capture,out):
 a,b=copper(before),copper(after);poses,_=inventory(json.loads(capture.read_text()));group={r:p['path'].split('.')[0] for r,p in poses.items()};transforms={};outliers=[]
 for g in set(group.values()):
  refs=[r for r,v in group.items() if v==g];r0=refs[0];pa=a['placements'][r0][:2];pb=b['placements'][r0][:2]
  r1=next(r for r in refs if math.dist(a['placements'][r][:2],pa)>1)
  va=[a['placements'][r1][i]-pa[i] for i in [0,1]];vb=[b['placements'][r1][i]-pb[i] for i in [0,1]];theta=math.atan2(vb[1],vb[0])-math.atan2(va[1],va[0]);co,si=round(math.cos(theta),8),round(math.sin(theta),8)
  def moved(p):return [pb[0]+co*(p[0]-pa[0])-si*(p[1]-pa[1]),pb[1]+si*(p[0]-pa[0])+co*(p[1]-pa[1])]
  for ref in refs:
   if math.dist(moved(a['placements'][ref][:2]),b['placements'][ref][:2])>1e-4:outliers.append(ref)
  transforms[g]=(pa,pb,co,si)
 d=parse(before);netgroups={};netrefs={}
 for f in children(d,'footprint'):
  ref=next((str(x[2]) for x in children(f,'property') if str(x[1])=='Reference'),None)
  if ref is None:ref=next(str(x[2]) for x in children(f,'fp_text') if str(x[1])=='reference')
  for pad in children(f,'pad'):
   for net in children(pad,'net'):netgroups.setdefault(str(net[2]),set()).add(group[ref]);netrefs.setdefault(str(net[2]),set()).add(ref)
 rows={}
 for net,ca in a['items'].items():
  gs=netgroups.get(net,set())
  if len(gs)!=1 or netrefs.get(net,set())&set(outliers):continue
  g=next(iter(gs));pa,pb,co,si=transforms[g]
  def movept(p):return [round(pb[0]+co*(p[0]-pa[0])-si*(p[1]-pa[1]),5),round(pb[1]+si*(p[0]-pa[0])+co*(p[1]-pa[1]),5)]
  def walk(v,do_move):
   if not isinstance(v,list):return round(v,5) if isinstance(v,float) else v
   if v and v[0]=='ends':return ['ends',sorted(movept(p) if do_move else [round(z,5) for z in p] for p in v[1])]
   if len(v)==3 and v[0] in ['start','end','mid','at','xy'] and all(isinstance(z,(int,float)) for z in v[1:]):return [v[0]]+(movept(v[1:]) if do_move else [round(z,5) for z in v[1:]])
   return [walk(z,do_move) for z in v]
  expected=collections.Counter()
  actual=collections.Counter()
  for key,count in ca.items():expected[json.dumps(walk(json.loads(key),True),sort_keys=True,separators=(',',':'))]+=count
  for key,count in b['items'].get(net,{}).items():actual[json.dumps(walk(json.loads(key),False),sort_keys=True,separators=(',',':'))]+=count
  rows[net]={'group':g,'before':sum(expected.values()),'after':sum(actual.values()),'preserved_after_rigid_transform':sum((expected&actual).values())}
 result={'version':'jitx-rigid-copper-v1','before':str(before),'after':str(after),'before_sha256':a['sha256'],'after_sha256':b['sha256'],'rigid_pose_outliers':outliers,'scoped_internal_nets':rows,'totals':{k:sum(r[k] for r in rows.values()) for k in ['before','after','preserved_after_rigid_transform']},'note':'Only nets wholly inside one rigidly moved circuit group, excluding nets touching pose outliers. 1e-5 mm rounding; primitive fragmentation differs from electrical topology. Cross-group routes excluded, not assumed preserved.'};out.write_text(json.dumps(result,indent=2));return result
if __name__=='__main__':
 r=audit(*map(Path,sys.argv[1:]));print(json.dumps({k:v for k,v in r.items() if k!='scoped_internal_nets'},indent=2))
