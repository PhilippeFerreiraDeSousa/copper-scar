"""Restore legacy net-0 metadata required to parse electrically unassigned keepouts."""
from import_experiments import *
b=CAND/'hierarchy-compatible';shutil.copytree(CAND/'hierarchy-unassigned-nc',b)
changes=[]
def visit(d,p):
 if not isinstance(d,list):return
 if d and str(d[0])=='zone':
  assert children(d,'keepout'), 'Only electrically unassigned keepouts may be normalized'
  for key,value in [('net',0),('net_name','')]:
   if not children(d,key):d.append([sx.Symbol(key),value]);changes.append(dict(file=str(p.relative_to(b)),field=key,value=value))
 for x in d:visit(x,p)
for p in [b/'pcbgolf.kicad_pcb',*b.rglob('*.kicad_mod')]:
 d=parse(p);visit(d,p);write(p,d)
p=b/'pcbgolf.net';d=parse(p)
for k in ['groups','variants']:
 for x in children(d,k):assert len(x)==1;d.remove(x)
write(p,d)
(RUN/'keepout-transform.json').write_text(json.dumps(changes,indent=2))
call('b-compatible-import',[CLI,'project','import','kicad',str(b),'--output',str(output('b-compatible-output'))],RUN)
