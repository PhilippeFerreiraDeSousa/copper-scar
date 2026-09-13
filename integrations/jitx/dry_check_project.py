"""Translate checkpoint source without connecting to native JITX or creating designs/."""
from pathlib import Path
import argparse,importlib,json,sys

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('project',type=Path);p.add_argument('--design',default='pcbgolf_import.stage_one_002.StageOne002');p.add_argument('--expect-via',action='store_true');a=p.parse_args();root=a.project.resolve();sys.path.insert(0,str(root))
 module,name=a.design.rsplit('.',1);m=importlib.import_module(module)
 assert Path(m.__file__).resolve().is_relative_to(root),'Resolved installed editable source instead of prepared project'
 from jitx.run.discover import DryRunBuilder
 def formatter(value,file=sys.stdout):print(json.dumps(value,indent=2),file=file)
 result=DryRunBuilder().build(getattr(m,name),dump=str(root/'dry-design.json'),formatter=formatter)
 assert result.get('status')=='ok',result
 design=json.loads((root/'dry-design.json').read_text());vias=design['v1'].get('vias',[])
 if a.expect_via:
  assert len(vias)==1 and vias[0]['diameter']==0.6 and vias[0]['holeDiameter']==0.3,vias
 assert not (root/'designs').exists(),'Dry validation unexpectedly created native state'
 print(json.dumps({'result':result,'loaded_module':m.__file__,'via_definitions':vias,'native_connection':False},indent=2))
if __name__=='__main__':main()
