#!/usr/bin/env python3
"""Package completed native evidence; never run or mutate an owner's CAD."""
import argparse, datetime, hashlib, json, shutil, subprocess
from pathlib import Path

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d): p.write_text(json.dumps(d,indent=2)+'\n')
def main():
 p=argparse.ArgumentParser(); p.add_argument('--kicad',type=Path); p.add_argument('--rerender',action='store_true'); p.add_argument('--feedback-chain',type=Path); p.add_argument('--diagnostic-source',type=Path); p.add_argument('--source',type=Path,required=True); p.add_argument('--output',type=Path,required=True); a=p.parse_args()
 out=a.output.resolve(); out.mkdir(parents=True,exist_ok=True)
 for f in ['index.html','README.md','serve.py']:
  src=Path(__file__).parent/f
  if src.exists(): shutil.copy2(src,out/f)
 history=[]; skipped=[]; best_observed=None
 paths=sorted((a.source/'runs').glob('*/attempt.json'))
 entries=[(path,json.loads(path.read_text())) for path in paths]
 if entries:
  first=entries[0][1]; baseline=dict(first); baseline.update(attempt='starting-six-layer-checkpoint',after=first['before'],candidate=first['input'],finished_at=first['started_at'],action={'kind':'starting native checkpoint'},action_level='baseline',status='completed',became_incumbent=False)
  entries.insert(0,(entries[0][0],baseline))
 for path,d in entries:
  if not d.get('finished_at'): continue
  e=d.get('after'); name=d['attempt']; candidate=Path(d.get('candidate',''))
  if not isinstance(e,dict):
   history.append(dict(id=name,time=d['finished_at'],kind=d.get('action_level','historical action'),action=d.get('action',{}).get('kind','unknown'),status=d.get('status'),failed=True,note=d.get('error','No completed native after-evaluation'),best=None)); continue
  board=candidate/'pcbgolf.kicad_pcb'; svg=candidate/'board.svg'
  expected=e.get('files',{}).get('pcbgolf.kicad_pcb')
  if not board.exists() or not expected or sha(board)!=expected:
   skipped.append(dict(id=name,reason='Missing board or native evaluation hash mismatch')); continue
  dest=out/'evidence'/name; dest.mkdir(parents=True,exist_ok=True)
  write(dest/'evaluation.json',e)
  # Keep exact action, parent, decision and source fingerprints; omit bulky command logs.
  receipt={k:d[k] for k in ['attempt','policy','started_at','finished_at','status','input','candidate','action','action_level','comparison_kind','incumbent_before','incumbent_after','became_incumbent','constraint_scope','routing_scope','classification','diagnostic_improved','tool_source_hashes'] if k in d}
  write(dest/'attempt.json',receipt)
  shutil.copy2(board,dest/board.name)
  img=None
  render_receipt=dest/'render-receipt.json'
  if render_receipt.exists() and (dest/'board.svg').exists():
   prior=json.loads(render_receipt.read_text())
   if prior.get('board_sha256')==expected and prior.get('image_sha256')==sha(dest/'board.svg'): img=f'evidence/{name}/board.svg'
  if a.kicad and (not img or a.rerender):
   subprocess.run([str(a.kicad),'pcb','export','svg','--layers','F.Cu,B.Cu,F.SilkS,Edge.Cuts','--mode-single','--page-size-mode','2','--exclude-drawing-sheet','-o',str(dest/'board.svg'),str(dest/board.name)],check=True,capture_output=True)
   img=f'evidence/{name}/board.svg'
   write(dest/'render-receipt.json',dict(board_sha256=expected,image_sha256=sha(dest/'board.svg'),method='kicad-cli pcb export svg; F.Cu,B.Cu,F.SilkS,Edge.Cuts; page-size-mode 2',source='packaged board bytes',note='Internal copper omitted in presentation view'))
  if svg.exists() and not img: shutil.copy2(svg,dest/'board.svg'); img=f'evidence/{name}/board.svg'
  inc=d.get('incumbent_after') or {}; priority=inc.get('priority') or []
  failed=d.get('status')!='completed'
  if not failed and e.get('invariants_ok') and e.get('errors')==0 and e.get('unconnected') is not None:
   best_observed=min(best_observed if best_observed is not None else e['unconnected'],e['unconnected'])
  history.append(dict(id=name,time=d['finished_at'],kind=d.get('action_level','historical action'),action=d.get('action',{}).get('kind','unknown'),status=d.get('status'),failed=failed,classification=d.get('classification'),opens=e.get('unconnected'),errors=e.get('errors'),warnings=e.get('warnings'),valid=e.get('validity_gate'),invariants=e.get('invariants_ok'),retained=d.get('became_incumbent'),best=best_observed,retained_best=priority[5] if len(priority)>5 else None,image=img,board_sha256=expected,evaluation=f'evidence/{name}/evaluation.json',receipt=f'evidence/{name}/attempt.json',board=f'evidence/{name}/pcbgolf.kicad_pcb',reason=d.get('action',{}).get('reason',''),hypothesis=d.get('action',{}).get('hypothesis',''),comparison=d.get('comparison_kind',''),source=str(path)))
 data=dict(schema=1,built_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),history=history,excluded=skipped,disclosure='Completed native snapshots. Opens are missing endpoint pairs, not a score. Inner routing is not placement optimization. No qualified product board.',source=str(a.source))
 write(out/'data.json',data); (out/'data.js').write_text('window.DEMO = '+json.dumps(data)+';\n')
 if a.feedback_chain:
  from package_feedback import build as feedback_build
  feedback_build(a.feedback_chain,out)
 elif not (out/'feedback-data.js').exists(): (out/'feedback-data.js').write_text('window.FEEDBACK=null;\n')
 if a.diagnostic_source:
  from package_diagnostics import build as diagnostics_build
  diagnostics_build(a.diagnostic_source,out)
 elif not (out/'diagnostics-data.js').exists(): (out/'diagnostics-data.js').write_text('window.DIAGNOSTICS=null;\n')
 docs=Path(__file__).parent/'docs'
 if docs.exists(): shutil.copytree(docs,out/'docs',dirs_exist_ok=True)
 hashes={str(f.relative_to(out)):sha(f) for f in sorted(out.rglob('*')) if f.is_file() and f != out/'SHA256SUMS.json'}
 write(out/'SHA256SUMS.json',hashes)
 print(json.dumps(dict(output=str(out),snapshots=len(history),excluded=skipped,files=len(hashes))))
if __name__=='__main__': main()
