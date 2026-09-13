"""Run proposals through persistent native state, optional build, route and evaluation.
Fresh design identities require an explicit recorded reset reason.
"""
from pathlib import Path
import argparse,json,subprocess,time,shutil,sys,os
from feasibility import evaluate
from placement_audit import audit
from placement_parameters import render
from observability import command as observed_command, write, sha
B=Path('/Users/philippe/dev/copper-scar-jitx');HERE=Path(__file__).resolve().parent
PYJ=B/'.venv/bin/python';JITX=B/'.venv/bin/jitx';PARSER=Path('/Users/philippe/dev/copper-scar-demo/.venv/bin/python')
def campaign(manifest):
 plan=json.loads(manifest.read_text());ledger=Path(plan['ledger']);ledger.mkdir(parents=True,exist_ok=True)
 for p in plan['proposals']:
  out=ledger/p['id'];out.mkdir(exist_ok=False);name=p['design'];candidate=B/'candidates'/p['id']
  if candidate.exists():raise ValueError('candidate output must be new')
  native=B/'designs'/name
  mode=p.get('mode','incremental')
  if mode=='fresh':
   if native.exists() or not p.get('reset_reason'):raise ValueError('fresh identity requires absent design and explicit reset reason')
  elif mode=='incremental':
   if not native.is_dir():raise ValueError('incremental proposal requires existing native design')
   shutil.copytree(native,out/'native-input-checkpoint')
  else:raise ValueError('unknown native-state mode')
  if p.get('placement_overrides') is not None:
   module=p['placement_module'];assert module.isidentifier() and module.startswith('Pcbgolf_')
   destination=B/'pcbgolf_import'/(module+'.py');assert not destination.exists(), 'never overwrite existing placement source'
   placement_record=render(B/'pcbgolf_import/Pcbgolf.py',p['placement_overrides'],destination)
   (out/'placement-parameters.json').write_text(json.dumps(placement_record,indent=2))
  shutil.copytree(B/'pcbgolf_import',out/'source' ,ignore=shutil.ignore_patterns('__pycache__'));(out/'proposal.json').write_text(json.dumps(p,indent=2));commands=[]
  write(out/'attempt-state.json',{'state':'running','runner_pid':os.getpid(),'started_at':time.time(),'proposal':p,'tools_sha256':{x.name:sha(x) for x in HERE.glob('*.py')},'source_sha256':{str(x.relative_to(out/'source')):sha(x) for x in (out/'source').rglob('*.py')}})
  def command(label,args,timeout):
   record=observed_command(args,B,out,label,timeout);commands.append(record);write(out/'commands.json',commands);print(p['id'],label,record['exit_code'],round(record['elapsed_seconds'],2),flush=True)
   if record['exit_code']!=0:raise RuntimeError(label+' failed; output remains an unevaluated checkpoint')
  try:
   if p.get('rebuild',mode=='fresh'):command('build',[str(JITX),'design','build',name,'--no-dependency-check'],90)
   args=[str(PYJ),str(HERE/'native_iteration.py'),name,str(out/'native')]
   if p.get('route'):args.append('--route')
   for net in p.get('nets',[]):args+=['--net',net]
   command('native',args,900)
   audit(B/'runs/import-ab-20260912/captured-live-view.json',out/'native/before.json',out/'placement-delta.json')
   export=out/'native/export'/(name+'.kicad_pcb')
   command('normalize',[str(PARSER),str(HERE/'roundtrip.py'),str(export),str(candidate)],60)
   r=evaluate(candidate,ledger,p['action']);
   if p.get('input_candidate'):
    command('copper-audit',[str(PARSER),str(HERE/'copper_audit.py'),str(Path(p['input_candidate'])/'pcbgolf.kicad_pcb'),str(candidate/'pcbgolf.kicad_pcb'),str(out/'copper-delta.json')],60)
   if r['retain'] and p.get('placement_overrides') is not None:(ledger/'best-placement-parameters.json').write_text(json.dumps({'candidate':str(candidate),'overrides':p['placement_overrides']},indent=2))
   print(p['id'],'retained',r['retain'],'valid',r['valid'],'cost',r['cost'],flush=True)
   state=json.loads((out/'attempt-state.json').read_text());state.update(state='completed',finished_at=time.time(),candidate=str(candidate));write(out/'attempt-state.json',state)
  except Exception as e:
   failure={'proposal':p,'error':str(e),'evaluation_reliable':False,'valid':False,'retain':False,'cost':None,'time':time.time(),'commands':commands}
   (out/'failure.json').write_text(json.dumps(failure,indent=2))
   state=json.loads((out/'attempt-state.json').read_text());state.update(state='failed',finished_at=time.time(),error=str(e));write(out/'attempt-state.json',state)
   with (ledger/'iterations.jsonl').open('a') as f:f.write(json.dumps(failure)+'\n');f.flush();os.fsync(f.fileno())
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('manifest',type=Path);a=p.parse_args();campaign(a.manifest)
