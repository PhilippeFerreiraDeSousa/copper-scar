"""Test KiCad 6 centralized hierarchy metadata without changing electrical content."""
from import_experiments import *
import copy
b=CAND/'hierarchy-centralized-instances'
shutil.copytree(CAND/'hierarchy',b,ignore=shutil.ignore_patterns('*.lck','*.kicad_prl'))
mapping=json.loads((RUN/'hierarchy-mapping.json').read_text())
root=parse(b/'pcbgolf.kicad_sch');ru=one(root,'uuid')[1]
si=[sx.Symbol('sheet_instances'),[sx.Symbol('path'),'/',[sx.Symbol('page'),'1']]]
yi=[sx.Symbol('symbol_instances')]
for i,m in enumerate(mapping):
 p=b/m['file'];d=parse(p)
 d=[x for x in d if not (isinstance(x,list) and x and str(x[0])=='sheet_instances')]
 si.append([sx.Symbol('path'),'/'+m['instance_uuid'],[sx.Symbol('page'),str(i+2)]])
 for sym in children(d,'symbol'):
  props={x[1]:x[2] for x in children(sym,'property')}
  yi.append([sx.Symbol('path'),'/'+m['instance_uuid']+'/'+one(sym,'uuid')[1],[sx.Symbol('reference'),props['Reference']],[sx.Symbol('unit'),one(sym,'unit')[1]],[sx.Symbol('value'),props.get('Value','')],[sx.Symbol('footprint'),props.get('Footprint','')]])
 write(p,d)
root=[x for x in root if not(isinstance(x,list) and x and str(x[0]) in ['sheet_instances','symbol_instances'])]+[si,yi];write(b/'pcbgolf.kicad_sch',root)
call('b-centralized-netlist',[KC,'sch','export','netlist','--format','kicadxml','-o',str(RUN/'centralized-netlist.xml'),str(b/'pcbgolf.kicad_sch')],b)
call('b-centralized-import',[CLI,'project','import','kicad',str(b),'--output',str(output('b-centralized-output'))],RUN)
