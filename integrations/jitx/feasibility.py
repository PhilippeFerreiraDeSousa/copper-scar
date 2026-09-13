"""Independent JITX feasibility evaluator and durable checkpoint retention.
No paid model calls, no Copperhead checker dependency. Original KiCad checks are mandatory.
"""
from pathlib import Path
import argparse,collections,hashlib,json,math,os,subprocess,time,sys
KC='/Users/philippe/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli'
POLICY='jitx-feasibility-v3'
ENGINEERING=('footprint_geometry','manufacturing','assembly','electrical_functionality','connector_compatibility')
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def tree_digest(root):
 return {str(p.relative_to(root)):digest(p) for p in root.rglob('*') if p.is_file() and p.suffix not in {'.lck','.kicad_prl'} and p.name not in {'drc.json','erc.json','evaluation.json','drc-execution.json','erc-execution.json'}}
def decide(metrics,invariants,reliable,evidence,best=None,stage=1,volume=None,vias=None,layers=None):
 result={'policy_version':POLICY,'stage':stage,'evaluation_reliable':reliable,'invariants_ok':invariants,'metrics':metrics,'valid':False,'score':None,'retain':False,'reasons':[]}
 required=('incorrect_connections','missing_connections','physical_errors','physical_warnings','erc_errors','erc_warnings','parity_issues')
 if reliable is not True or invariants is not True or any(type(metrics.get(k)) is not int or metrics[k]<0 for k in required):
  result['cost']=None;result['reasons']=['missing/failed evaluation, invalid metrics, or immutable topology failure'];return result
 # Lexicographic priorities avoid invented conversion weights. No finite score for unknown checks.
 result['cost']=[metrics[k] for k in required]
 zero=all(metrics[k]==0 for k in required)
 qualified=all(isinstance(evidence.get(k),dict) and evidence[k].get('passed') is True and evidence[k].get('verified') is True and evidence[k].get('artifact_sha256') and evidence[k].get('reviewer') for k in ENGINEERING)
 result['valid']=bool(zero and qualified)
 if not qualified:result['reasons'].append('engineering/geometry evidence incomplete; never a valid board')
 if not zero:result['reasons'].append('check findings remain')
 if stage==2:
  if not result['valid'] or not isinstance(volume,(float,int)) or isinstance(volume,bool) or not math.isfinite(volume) or volume<=0 or type(vias) is not int or vias<0 or type(layers) is not int or layers<2:
   result['reasons'].append('stage two requires valid board and verified assembly volume/vias/layers');return result
  result['score']=volume+50*vias+5000*layers
  result['retain']=best is None or (best.get('valid') is True and best.get('score') is not None and result['score']<best['score'])
 else:
  better=best is None or best.get('cost') is None or result['cost']<best['cost']
  # Do not buy missing-connection progress by creating physical errors or ERC errors.
  regression=best is not None and best.get('cost') is not None and any(metrics[k]>best['metrics'][k] for k in ('incorrect_connections','physical_errors','erc_errors'))
  result['retain']=bool(better and not regression)
  if regression:result['reasons'].append('rejected safety-critical regression')
 return result

def evaluate(candidate,ledger,action,evidence=None):
 candidate=candidate.resolve();ledger.mkdir(parents=True,exist_ok=True);started=time.time();before=tree_digest(candidate);executions={};reliable=True;reports={}
 for kind,ext in [('drc','kicad_pcb'),('erc','kicad_sch')]:
  rec={}
  output=candidate/(kind+'.json');output.unlink(missing_ok=True)
  args=[KC,'pcb' if kind=='drc' else 'sch',kind,'--format','json','--output',str(output)]
  if kind=='drc':args+=['--schematic-parity']
  args+=[str(candidate/('pcbgolf.'+ext))];t=time.monotonic()
  try:
   r=subprocess.run(args,capture_output=True,text=True,timeout=90);rec={'argv':args,'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'elapsed_seconds':time.monotonic()-t}
   if r.returncode!=0:raise ValueError('checker execution failed')
   reports[kind]=json.loads(output.read_text())
  except Exception as e:reliable=False;rec=locals().get('rec',{});rec={**rec,'error':str(e),'elapsed_seconds':time.monotonic()-t}
  executions[kind]=rec;(candidate/(kind+'-execution.json')).write_text(json.dumps(rec,indent=2))
 # Native DRC has produced differing counts on unchanged bytes in this campaign.
 # Preserve a second report and fail closed on differing metric inventories.
 if 'drc' in reports:
  try:
   repeat_path=ledger/'repeat-checks'/(candidate.name+'-'+str(time.time_ns())+'.json');repeat_path.parent.mkdir(exist_ok=True)
   args=[KC,'pcb','drc','--format','json','--schematic-parity','--output',str(repeat_path),str(candidate/'pcbgolf.kicad_pcb')]
   t=time.monotonic();repeat=subprocess.run(args,capture_output=True,text=True,timeout=90)
   assert repeat.returncode==0,'repeat native DRC failed'
   repeated=json.loads(repeat_path.read_text())
   def signature(d):return {k:dict(collections.Counter((x['type'],x['severity']) for x in d[k])) for k in ['violations','schematic_parity','unconnected_items']}
   agrees=signature(reports['drc'])==signature(repeated)
   executions['drc_repeat']={'elapsed_seconds':time.monotonic()-t,'report':str(repeat_path),'agrees':agrees,'exit_code':repeat.returncode}
   reliable=reliable and agrees
  except Exception as e:reliable=False;executions['drc_repeat']={'error':str(e)}
 m={};counts={}
 try:
  drc=reports['drc'];erc=reports['erc'];v=drc['violations'];parity=drc['schematic_parity'];unconnected=drc['unconnected_items'];ev=[x for sheet in erc['sheets'] for x in sheet['violations']]
  assert all(isinstance(x,list) for x in [v,parity,unconnected,ev])
  assert all(x['severity'] in ['error','warning','exclusion'] for x in v+parity+unconnected+ev)
  m={'incorrect_connections':sum(x['type'] in {'shorting_items','tracks_crossing'} for x in v)+sum(x['type']=='net_conflict' for x in parity),'missing_connections':len(unconnected),'physical_errors':sum(x['severity']=='error' and x['type'] not in {'shorting_items','tracks_crossing'} for x in v),'physical_warnings':sum(x['severity']=='warning' for x in v),'erc_errors':sum(x['severity']=='error' for x in ev),'erc_warnings':sum(x['severity']=='warning' for x in ev),'parity_issues':len(parity)}
  counts={k:dict(collections.Counter(x['type'] for x in values)) for k,values in [('physical',v),('parity',parity),('erc',ev)]}
 except Exception as e:reliable=False;executions['parse_error']=str(e)
 normalization=json.loads((candidate/'normalization.json').read_text()) if (candidate/'normalization.json').exists() else {}
 invariant=normalization.get('unique_object_ids') is True and normalization.get('topology_equal') is True and normalization.get('source_rules_restored') is True and normalization.get('embedded_legacy_netclasses_removed') is True
 try:
  verification=subprocess.run(['/Users/philippe/dev/copper-scar-demo/.venv/bin/python',str(Path(__file__).with_name('verify_candidate.py')),str(candidate)],capture_output=True,text=True,timeout=30)
  executions['immutable_verification']={'exit_code':verification.returncode,'stdout':verification.stdout,'stderr':verification.stderr}
  invariant=invariant and verification.returncode==0 and json.loads(verification.stdout)['passed'] is True
 except Exception as e:invariant=False;executions['immutable_verification']={'error':str(e)}
 after=tree_digest(candidate);reliable=reliable and before==after
 bestpath=ledger/'best-feasibility.json';best=json.loads(bestpath.read_text()) if bestpath.exists() else None
 if best and best.get('policy_version')!=POLICY:best=None
 verified_evidence={}
 for key,claim in (evidence or {}).items():
  try:
   item=dict(claim);artifact=Path(item['artifact']);item['verified']=(digest(artifact)==item['artifact_sha256'] and item['candidate_board_sha256']==digest(candidate/'pcbgolf.kicad_pcb'))
   verified_evidence[key]=item
  except (KeyError,TypeError,OSError):verified_evidence[key]={'passed':False,'verified':False}
 result=decide(m,invariant,reliable,verified_evidence,best)
 result.update({'candidate':str(candidate),'action':action,'started_at':started,'elapsed_seconds':time.time()-started,'artifacts':after,'check_executions':executions,'counts':counts,'engineering_evidence':evidence or {},'feedback':{'next_actions':[]}})
 if m.get('missing_connections',0):result['feedback']['next_actions'].append('Connect remaining islands; inspect exported copper, not only native route representations.')
 if m.get('physical_errors',0):result['feedback']['next_actions'].append('Fix physical errors with original rules retained; inspect intrinsic footprint violations separately from placement/routing.')
 if m.get('parity_issues',0):result['feedback']['next_actions'].append('Resolve remaining parity through reversible identity mapping or source-intent evidence; do not suppress checks.')
 (candidate/'evaluation.json').write_text(json.dumps(result,indent=2))
 with (ledger/'iterations.jsonl').open('a') as f:f.write(json.dumps(result)+'\n');f.flush();os.fsync(f.fileno())
 if result['retain']:
  tmp=bestpath.with_suffix('.tmp');tmp.write_text(json.dumps(result,indent=2));tmp.replace(bestpath)
 # Best valid pointer is separate from best incomplete feasibility checkpoint.
 if result['valid']:(ledger/'best-valid.json').write_text(json.dumps(result,indent=2))
 try:
  from observability import publish
  publish(candidate,ledger,result)
 except Exception as e:
  with (ledger/'preview-failures.jsonl').open('a') as f:f.write(json.dumps({'candidate':str(candidate),'error':str(e),'time':time.time()})+'\n')
 try:
  sys.path.insert(0,str(Path(__file__).resolve().parents[2]));from copper_scar.loop.weave_trace import WeaveTracer
  tracer=WeaveTracer.maybe_init()
  with tracer.span('jitx.evaluate',inputs={'candidate':str(candidate),'action':action},attributes={'policy_version':POLICY}) as span:span.set_output(result)
 except Exception as e:
  with (ledger/'observability.jsonl').open('a') as f:f.write(json.dumps({'time':time.time(),'weave_unavailable':type(e).__name__})+'\n')
 return result
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('candidate',type=Path);p.add_argument('--ledger',type=Path,required=True);p.add_argument('--action',required=True);a=p.parse_args();r=evaluate(a.candidate,a.ledger,a.action);print(json.dumps({k:r[k] for k in ['candidate','evaluation_reliable','invariants_ok','metrics','cost','valid','retain','reasons','elapsed_seconds']},indent=2))
