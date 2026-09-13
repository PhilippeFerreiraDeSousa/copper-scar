"""Finish native ERC and write source-bound replay records for saved stages."""
from pathlib import Path
import argparse,json,subprocess
from campaign import command,KICAD,KIPY,sha,write,now,ROOT
from audit import audit

def finish(base,folder,source,action,parent=None,retained=False):
 base,folder,source=map(Path,[base,folder,source])
 command([KICAD,'sch','erc','--format','json','-o',folder/'erc.json',folder/'pcbgolf.kicad_sch'],folder,'erc')
 command([KIPY,ROOT/'experiments/large-loop/native_geometry.py',source/'pcbgolf.kicad_pcb',folder/'pcbgolf.kicad_pcb',base/'input/circuit.json',folder/'full-geometry.json'],folder,'geometry')
 result=audit(folder,base/'input/circuit.json',source)
 existing=json.loads((folder/'evaluation.json').read_text())
 existing.update(result);result=existing
 erc=[v for sheet in json.loads((folder/'erc.json').read_text())['sheets'] for v in sheet['violations']]
 geometry=json.loads((folder/'full-geometry.json').read_text())['all_electrical_and_mechanical_pads_preserved']
 result['all_pad_geometry_preserved']=geometry
 result['feasibility_cost']+=0 if geometry else 10000
 result['accepted']=result['accepted'] and geometry
 result['erc_violations']=len(erc);result['feasibility_cost']+=len(erc);result['accepted']=result['accepted'] and not erc
 write(folder/'evaluation.json',result);write(folder/'acceptance.json',result)
 commands=sorted([json.loads(f.read_text()) for f in folder.glob('*.command.json')],key=lambda c:c['started_at'])
 rec={'id':'large-loop-'+folder.name,'source_sha':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'source_files':{str(p.relative_to(ROOT)):sha(p) for p in (ROOT/'experiments/large-loop').rglob('*.py')},'started_at':commands[0]['started_at'],'finished_at':now(),'action':action,'parent_board_sha256':sha(Path(parent)/'pcbgolf.kicad_pcb') if parent else None,'after':result,'commands':commands,'retained':retained,'preview_sha256':sha(folder/'preview.kicad_pcb'),'folder':str(folder.resolve()),'loss_components':{'opens':result['drc_opens'],'required_physical_findings':len(result['required_violations']),'schematic_parity':result['schematic_parity_issues'],'erc':len(erc)},'limitations':'Intrinsic original footprint errors retained; no claim of native feasibility until all acceptance gates pass.'}
 write(folder/'completed.json',rec);return rec

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('base',type=Path);ap.add_argument('folder',type=Path);ap.add_argument('source',type=Path);ap.add_argument('--kind',default='routing_only');a=ap.parse_args();r=finish(a.base,a.folder,a.source,{'kind':a.kind});print({k:r['after'][k] for k in ['native_open_count','feasibility_cost','accepted','erc_violations']})
