"""Read-only KiCad inventories for exact board differences."""
import json,re
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
