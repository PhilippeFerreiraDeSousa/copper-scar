"""Compare realized instance-group poses, including interactive placement overrides."""
from pathlib import Path
import argparse,json,collections

def inventory(messages):
 board=next(m['body'] for m in messages if m['type']=='board');groups={g['id']:dict(g) for g in board['module']['groups']}
 for m in messages:
  if m['type']=='placements':
   for g in m['body']['groups']:groups[g['id']].update(g)
 poses={}
 for g in groups.values():
  for inst in g.get('instances',[]):
   assert inst['designator'] not in poses
   poses[inst['designator']]={'path':inst['ref'],'x':g['pose']['center']['x'],'y':g['pose']['center']['y'],'angle':g['pose']['angle'],'side':g['side'],'group_id':g['id']}
 return poses,board

def audit(before,after,out):
 a,ba=inventory(json.loads(before.read_text()));b,bb=inventory(json.loads(after.read_text()));assert set(a)==set(b)
 moves=[]
 for ref in a:
  if any(abs(a[ref][k]-b[ref][k])>1e-6 for k in ['x','y','angle']) or a[ref]['side']!=b[ref]['side']:moves.append({'ref':ref,'before':a[ref],'after':b[ref]})
 r={'components':len(a),'moved_or_rotated_count':len(moves),'unchanged_count':len(a)-len(moves),'moves':moves,'boundary_before':ba['boundary'],'boundary_after':bb['boundary'],'copper_layers_before':ba['stackup']['numlayers'],'copper_layers_after':bb['stackup']['numlayers'],'before':str(before),'after':str(after)}
 out.write_text(json.dumps(r,indent=2));return r
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('before',type=Path);p.add_argument('after',type=Path);p.add_argument('out',type=Path);a=p.parse_args();r=audit(a.before,a.after,a.out);print(json.dumps({k:v for k,v in r.items() if k not in ['boundary_before','boundary_after']},indent=2))
