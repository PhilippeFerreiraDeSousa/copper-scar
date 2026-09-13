"""Reproducible full-design initialization comparison; every route is whole-board."""
import argparse, collections, hashlib, json, shutil, subprocess, sys, time
from pathlib import Path
import sexpdata as sx

ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from copper_scar.tools.copperhead import stage1 as s
from copper_scar.real import design_digest
HERE=Path(__file__).parent
def nodes(n,k):return [x for x in n if isinstance(x,list) and x and str(x[0])==k]
def ref(fp):return next(x[2] for x in nodes(fp,'property') if x[1]=='Reference')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v):s.write(p,v)
def run(argv,folder,label,timeout=120):
 r=s.command(list(map(str,argv)),folder,label,timeout)
 if r['returncode']!=0:raise RuntimeError(label+' failed: '+str(folder))
 return r
def signature(v):return (v['type'],v['severity'],tuple(sorted(x.get('uuid','') for x in v.get('items',[]))))
def freeze_support(folder):return {p:p.read_bytes() for p in folder.glob('*.kicad_pro')}
def restore(frozen):
 for p,data in frozen.items():p.write_bytes(data)
def evaluate(folder,out,label):
 frozen=freeze_support(folder)
 run([s.KICAD,'pcb','drc','--format','json','--schematic-parity','--refill-zones','--save-board','-o',out/(label+'-fill.json'),folder/'pcbgolf.kicad_pcb'],out,label+'-fill')
 restore(frozen)
 result=s.evaluate(folder,out,label,s.support(folder),saved_board=True)
 run([s.KIPY,HERE/'native.py','audit',folder],out,label+'-audit')
 shutil.copy2(folder/'native-audit.json',out/(label+'-audit.json'))
 return result
def prepare(out,mode,gap):
 parent=s.LOCAL/'candidates/stage1-20260913-084902-d79c29'
 folder=out/'input';s.copy_project(parent,folder)
 # Original, entirely unrouted board; reuse only verified hierarchy instance paths.
 original=sx.loads((s.REFERENCE/'pcbgolf.kicad_pcb').read_text())
 converted=sx.loads((parent/'pcbgolf.kicad_pcb').read_text())
 paths={ref(f):nodes(f,'path')[0] for f in nodes(converted,'footprint')}
 padnets={nodes(p,'uuid')[0][1]:nodes(p,'net') for f in nodes(converted,'footprint') for p in nodes(f,'pad')}
 net_bindings=[]
 for f in nodes(original,'footprint'):
  old=nodes(f,'path');f.remove(old[0]);f.append(paths[ref(f)])
  for pad in nodes(f,'pad'):
   target=padnets[nodes(pad,'uuid')[0][1]];current=nodes(pad,'net')
   if current!=target:
    net_bindings.append(dict(ref=ref(f),pad=pad[1],before=current,after=target))
    for n in current:pad.remove(n)
    pad.extend(target)
 write(out/'schematic-net-binding.json',dict(changes=json.loads(json.dumps(net_bindings,default=str)),qualification='Use the already independently verified full-schematic net partition; original J3 stacked pad unconnected-name aliases otherwise create five false shorts. No physical pad or schematic connection removed.'))
 (folder/'pcbgolf.kicad_pcb').write_text(sx.dumps(original))
 for stale in ['routing-options.json','native-audit.json','initialization.json']:
  (folder/stale).unlink(missing_ok=True)
 run([s.KIPY,HERE/'native.py','prepare',folder,'--groups',HERE/'groups.json','--mode',mode,'--gap',gap],out,'prepare')
 options=dict(schema_version=1,constraint_scope=design_digest(s.support(folder)),allowed_via_options=['Via[0-5]_600:300_um','Via[0-5]_450:200_um'],qualification='Original-rule legal through-via options; same six-layer capacity in both arms. No contact normalization needed for original no-copper board.')
 write(folder/'routing-options.json',options)
 return folder
def trial(root,name,mode,gap,seconds):
 out=root/name;out.mkdir();start=time.monotonic();write(out/'status.json',dict(status='preparing',started_at=s.now()))
 folder=prepare(out,mode,gap)
 before=evaluate(folder,out,'before')
 assert before['invariants_ok'],'Original component/pad/net/rule parity failed'
 write(out/'status.json',dict(status='routing',before={k:before[k] for k in ['unconnected','errors','warnings','invariants_ok']},started_at=s.now()))
 candidate=out/'routed';s.copy_project(folder,candidate)
 run([s.KIPY,HERE/'native.py','export',candidate],out,'export')
 run([s.PYTHON,ROOT/'scripts/copperhead_effective_options.py',candidate,'--phase','export'],out,'effective-vias')
 route=run([s.PYTHON,ROOT/'scripts/copperhead_route.py',candidate,'--seconds',seconds,'--passes',100,'--whole-board','--skip-fanout'],out,'route',seconds+50)
 run([s.KIPY,HERE/'native.py','import',candidate],out,'import')
 after=evaluate(candidate,out,'after')
 old=collections.Counter(signature(v) for v in before['violations'] if v['type']!='unconnected_items')
 new=[v for v in after['violations'] if v['type']!='unconnected_items']
 added=[]
 for v in new:
  key=signature(v)
  if old[key]:old[key]-=1
  else:added.append(v)
 a=json.loads((out/'before-audit.json').read_text());b=json.loads((out/'after-audit.json').read_text())
 assert a['identity']==b['identity'] and a['poses']==b['poses']
 newgroups=[set(g['pads']) for g in b['pad_groups']]
 splits=[g for g in a['pad_groups'] if len(g['pads'])>1 and not any(set(g['pads'])<=z for z in newgroups)]
 legalvias=all((v['diameter'],v['drill']) in [(.45,.2),(.6,.3)] and v['layers']==['F.Cu','B.Cu'] for v in b['vias'])
 result=dict(status='completed',name=name,before={k:before[k] for k in ['unconnected','errors','warnings','search_cost']},after={k:after[k] for k in ['unconnected','errors','warnings','search_cost','invariants_ok','manufacturing_rules_clear']},added_findings=added,split_groups=splits,via_definitions_legal=legalvias,via_count=len(b['vias']),route_elapsed_seconds=route['elapsed_seconds'],elapsed_seconds=time.monotonic()-start,board=str(candidate/'pcbgolf.kicad_pcb'),board_sha256=sha(candidate/'pcbgolf.kicad_pcb'),missing_by_net=s.missing_by_net(after),incomplete_diagnostic_retained=after['invariants_ok'] and not added and not splits and legalvias and after['unconnected']<before['unconnected'],valid_board=False,qualification='Inherited footprint-rule defects are reported, never waived. Diagnostic connectivity improvement is not native/manufacturing or engineering acceptance.')
 write(out/'result.json',result);write(out/'status.json',result)
 # Standalone original-layer SVGs are immutable checkpoint visuals.
 run([s.KICAD,'pcb','export','svg','--layers','F.Cu,B.Cu,Edge.Cuts','--mode-single','--page-size-mode','2','-o',out/'visual',candidate/'pcbgolf.kicad_pcb'],out,'visual')
 return result
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);ap.add_argument('--seconds',type=int,default=600);ap.add_argument('--mode',choices=['spacious','original','compact'],default='spacious');ap.add_argument('--gap',type=float,default=3);ap.add_argument('--name',required=True);a=ap.parse_args()
 a.root=a.root.resolve();a.root.mkdir(parents=True,exist_ok=True)
 write(a.root/(a.name+'-source.json'),dict(commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),sources={str(p.relative_to(ROOT)):sha(p) for p in HERE.glob('*') if p.is_file()},original_board_sha256=sha(s.REFERENCE/'pcbgolf.kicad_pcb'),route_seconds=a.seconds,net_filter=None,layers=6,passes=100,threads=1,fanout=False,created_at=s.now()))
 print(json.dumps(trial(a.root,a.name,a.mode,a.gap,a.seconds),indent=2))
if __name__=='__main__':main()
