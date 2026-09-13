"""Geometric copper identity, independent of generated UUID/net numbers.
Segment fragmentation is not merged: removed+added may be a re-expression, not loss.
"""
from pathlib import Path
import argparse,collections,hashlib,json,sys
import sexpdata as sx
from import_experiments import parse,children,one

def clean(x):
 if isinstance(x,list):return [clean(v) for v in x if not(isinstance(v,list) and v and str(v[0]) in {'uuid','tstamp'})]
 if isinstance(x,sx.Symbol):return str(x)
 if isinstance(x,float):return round(x,6)
 return x

def copper(board):
 d=parse(board);nets={int(n[1]):str(n[2]) for n in children(d,'net')};items={};counts=collections.Counter();layers=[]
 for layer in one(d,'layers')[1:]:
  if isinstance(layer,list) and len(layer)>2 and str(layer[2]) in {'signal','power','mixed'}:layers.append(str(layer[1]))
 for typ in ['segment','arc','via','zone']:
  for ob in children(d,typ):
   net=str(nets.get(int(one(ob,'net')[1]),'unknown'));v=clean(ob)
   v=[x for x in v if not(isinstance(x,list) and x and x[0] in {'net','net_name'})]
   if typ=='segment':
    ends=sorted([clean(one(ob,'start')[1:]),clean(one(ob,'end')[1:])]);v=[x for x in v if not(isinstance(x,list) and x and x[0] in {'start','end'})]+[['ends',ends]]
   key=json.dumps(v,sort_keys=True,separators=(',',':'));items.setdefault(net,collections.Counter())[key]+=1;counts[typ]+=1
 fp=[]
 for f in children(d,'footprint'):
  ref=next((str(x[2]) for x in children(f,'property') if str(x[1])=='Reference'),None)
  if ref is None:ref=next(str(x[2]) for x in children(f,'fp_text') if str(x[1])=='reference')
  fp.append({'ref':ref,'pose':clean(one(f,'at')[1:]),'layer':clean(one(f,'layer')[1:]),'pads':[clean(p) for p in children(f,'pad')]})
 edge=[]
 def points(x):
  if isinstance(x,list):
   if len(x)==3 and str(x[0]) in {'start','end','mid','xy'} and all(isinstance(v,(float,int)) for v in x[1:]):edge.append(x[1:])
   else:
    for v in x:points(v)
 for ob in d:
  if isinstance(ob,list) and children(ob,'layer') and str(one(ob,'layer')[1])=='Edge.Cuts':points(ob)
 bounds=[min(v[0] for v in edge),min(v[1] for v in edge),max(v[0] for v in edge),max(v[1] for v in edge)] if edge else None
 return {'sha256':hashlib.sha256(board.read_bytes()).hexdigest(),'counts':dict(counts),'copper_layers':layers,'outline_bounds_mm':bounds,'items':items,'placements':{f['ref']:f['pose']+f['layer'] for f in fp}}

def audit(a,b,out):
 x=copper(a);y=copper(b);nets={}
 for n in sorted(set(x['items'])|set(y['items'])):
  ca=x['items'].get(n,collections.Counter());cb=y['items'].get(n,collections.Counter());nets[n]={'preserved':sum((ca&cb).values()),'removed':sum((ca-cb).values()),'added':sum((cb-ca).values())}
 r={'version':'jitx-copper-geometry-v1','before':str(a),'after':str(b),'before_sha256':x['sha256'],'after_sha256':y['sha256'],'before_counts':x['counts'],'after_counts':y['counts'],'before_layers':x['copper_layers'],'after_layers':y['copper_layers'],'totals':{k:sum(v[k] for v in nets.values()) for k in ['preserved','removed','added']},'changed_nets':{n:v for n,v in nets.items() if v['removed'] or v['added']},'unchanged_net_count':sum(not(v['removed'] or v['added']) for v in nets.values()),'moved_refs':[ref for ref in x['placements'] if x['placements'][ref]!=y['placements'].get(ref)],'note':'Exact primitive geometry comparison ignoring UUID and net IDs. Segmentation changes count as removed+added; this is not an electrical-connectivity proof.'}
 out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(r,indent=2));return r
if __name__=='__main__':
 if len(sys.argv)==3 and sys.argv[1]=='--inventory':
  r=copper(Path(sys.argv[2]));print(json.dumps({k:v for k,v in r.items() if k not in {'items'}}));raise SystemExit
 p=argparse.ArgumentParser();p.add_argument('before',type=Path);p.add_argument('after',type=Path);p.add_argument('out',type=Path);a=p.parse_args();r=audit(a.before,a.after,a.out);print(json.dumps({k:v for k,v in r.items() if k!='changed_nets'},indent=2))
