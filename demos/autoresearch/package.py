#!/usr/bin/env python3
"""Create one pilot-first portable ZIP from explicitly allowed evidence files."""
import argparse,hashlib,json,subprocess,zipfile
from pathlib import Path

def sha(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
 return h.hexdigest()

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--outputs',type=Path,required=True);ap.add_argument('--allow-incomplete',action='store_true');a=ap.parse_args();root=a.outputs;pilot=root/'two-level-autoresearch';state=json.loads((pilot/'data.json').read_text())
 assert not state['fixture'];assert state['decisions'] or a.allow_incomplete,'Final package requires recorded comparison decision'
 remote=json.loads((pilot/'remote/verified.json').read_text());assert remote['source_events_sha256']==state['events_sha256'],'Remote publication lags this freeze'
 video=json.loads((pilot/'replay-verified.json').read_text());assert video['source_events_sha256']==state['events_sha256'],'Replay lags this freeze'
 assert sha(pilot/'two-level-replay.mp4')==video['video_sha256']
 assert video['source_state_sha256']==sha(pilot/'data.json'),'Replay does not match the complete frozen state'
 ui=json.loads((pilot/'ui-verified.json').read_text());assert ui['events_sha256']==state['events_sha256'],'Offline UI QA lags this freeze'
 assert ui['source_state_sha256']==sha(pilot/'data.json'),'UI QA does not match complete frozen state'
 if (state.get('next_campaign') or {}).get('result'):
  campaign=json.loads((pilot/'remote/campaign-verified.json').read_text());assert campaign['downloaded_bytes_verified']
  for artifact in state['decision_artifacts']:
   assert campaign['files_sha256'][artifact['kind']]==artifact['sha256'],'Consumer remote evidence lags this freeze'
 files={}
 def add_tree(folder,prefix,skip=lambda p:False):
  for p in folder.rglob('*'):
   if p.is_file() and not skip(p):files[prefix+'/'+str(p.relative_to(folder))]=p
 for folder in ['boards','attempts','manifests','decisions','next-campaign']:add_tree(pilot/folder,'two-level-autoresearch/'+folder)
 for name in ['index.html','data.js','data.json','events.jsonl','ingestion-receipts.jsonl','two-level-replay.mp4','replay-verified.json','ui-verified.json']:files['two-level-autoresearch/'+name]=pilot/name
 for p in (pilot/'remote').glob('*verified.json'):files['two-level-autoresearch/remote/'+p.name]=p
 for folder in ['router-logs','complete-evidence']:add_tree(pilot/'remote'/folder,'two-level-autoresearch/remote/'+folder)
 for folder in ['optimizer-research-ledger','latest-loop-experiments','higher-loop-provenance-audit']:
  add_tree(root/folder,folder,lambda p:'frames' in p.parts or p.name.startswith('qa-') or p.suffix=='.pyc')
 scripts=Path(__file__).resolve().parent
 for p in scripts.glob('*'):
  if p.suffix in ['.py','.html','.md']:files['reproduce/'+p.name]=p
 material=root/'demo-material';material.mkdir(exist_ok=True)
 for name in ['DEMO-SCRIPT.md','SUBMISSION-DRAFT.md','REPRODUCE.md']:
  dest=material/name;dest.write_bytes((scripts/name).read_bytes());files['demo-material/'+name]=dest
 # Exact Git trees, not the execution owner's working edits or runtime directories.
 owner=Path(state['source_path']).parents[2];frozen=state['common_protocol']['source_commit'];revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=scripts,text=True).strip();source_dir=root/'demo-source';source_dir.mkdir(exist_ok=True)
 archives=[(owner,frozen,'frozen-experiment'),(scripts,revision,'demo-presentation')]
 consumer_commit=(state.get('next_campaign') or {}).get('consumed',{}).get('consumer_source_commit')
 if consumer_commit:archives.append((owner,consumer_commit,'next-campaign'))
 for repo,commit,label in archives:
  dest=source_dir/(label+'-'+commit+'.tar.gz')
  if not dest.exists():subprocess.run(['git','-C',str(repo),'archive','--format=tar.gz','--prefix='+label+'/','-o',str(dest),commit],check=True)
  files['source/'+dest.name]=dest
 # Include the exact source project and support required by the recorded protocol.
 source_board=Path(state['common_protocol']['source_board_path']);source_board=source_board if source_board.is_absolute() else owner/source_board;source_project=source_board.parent
 assert sha(source_board)==state['common_protocol']['source_board_sha256'];files['experiment-input/pcbgolf.kicad_pcb']=source_board
 for name,expected in state['common_protocol'].get('source_support',{}).items():
  p=source_project/name;assert sha(p)==expected,('Support drift',name);files['experiment-input/'+name]=p
 for name in ['pcbgolf.kicad_pro','pcbgolf.kicad_dru','pcbgolf.kicad_sch','routing-options.json']:
  p=source_project/name
  if p.exists():files['experiment-input/'+name]=p
 hashes={name:sha(p) for name,p in files.items()}
 title='Completed matched policy pilot' if state['decisions'] else 'IN PROGRESS — actual matched policy pilot'
 final=state['decisions'][-1]['decision'] if state['decisions'] else None
 result_text=('Recorded policy choice: '+final['kept_policy']+'. The predeclared primary rule compares retained missing pairs after exactly three decisions; ties keep baseline.') if final else 'No final policy choice has been recorded. Unfinished steps have no predicted result.'
 entry=f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Copper Scar · Agent Loops demo</title><style>body{{font:18px/1.65 system-ui;background:#091320;color:#e8f0f8;max-width:960px;margin:50px auto;padding:24px}}a{{color:#8bd8ff}}h1{{font-size:42px;line-height:1.15}}.card{{background:#14263b;border:1px solid #40556c;padding:24px;border-radius:12px;margin:24px 0}}.small{{font-size:15px;color:#acc1d7}}.button{{display:inline-block;background:#24536b;padding:12px 18px;border-radius:8px;margin-right:12px}}</style><p class="small">Copper Scar · CoreWeave Agent Loops demonstration</p><h1>Improve the board.<br>Measure the optimizer.</h1><p>Placement and via proposals → whole-board six-layer routing → native evaluation → retain or reject. A higher loop compares two authored ranking hypotheses under a frozen protocol.</p><div class="card"><h2>{title}</h2><p>{result_text}</p><p><a class="button" href="two-level-autoresearch/index.html">Open the experiment</a><a href="two-level-autoresearch/two-level-replay.mp4">Play the recorded replay</a></p></div><p>Read the <a href="demo-material/DEMO-SCRIPT.md">three-minute demo script</a>, <a href="demo-material/SUBMISSION-DRAFT.md">submission draft</a> and <a href="demo-material/REPRODUCE.md">reproduction guide</a>.</p><p class="small">This is a prior-informed single-board finite-library pilot. No per-lower-step LLM inference is claimed. Open connections remain; board qualification is not claimed. Any next-campaign receipt is shown separately from the matched comparison.</p><hr><p>Supplemental history: <a href="latest-loop-experiments/index.html">unmatched outer-loop experiments</a> · <a href="optimizer-research-ledger/index.html">research ledger</a> · <a href="higher-loop-provenance-audit/first-decision-causality.md">independent first-decision attribution</a>.</p><p class="small">The extracted package opens without Internet access. W&amp;B links are optional private remote evidence. No credentials or publisher runtime are included.</p></html>'''
 (root/'copper-scar-demo.html').write_text(entry)
 receipt={'fixture':False,'comparison_complete':bool(final),'events_sha256':state['events_sha256'],'experiment_source_revision':frozen,'demo_source_revision':revision,'files':hashes}
 target=root/('two-level-autoresearch-final.zip' if final else 'two-level-autoresearch-in-progress.zip');temporary=target.with_suffix('.zip.tmp')
 with zipfile.ZipFile(temporary,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=5) as z:
  z.writestr('index.html',entry);z.writestr('package-manifest.json',json.dumps(receipt,indent=2))
  for name,p in files.items():
   assert sha(p)==hashes[name],('File changed during freeze',name);z.write(p,name);assert sha(p)==hashes[name],('File changed while archived',name)
 with zipfile.ZipFile(temporary) as z:
  assert z.testzip() is None
  for name,digest in hashes.items():assert hashlib.sha256(z.read(name)).hexdigest()==digest,('Archive mismatch',name)
 temporary.replace(target)
 result={'path':str(target),'sha256':sha(target),'bytes':target.stat().st_size,'files':len(files),'comparison_complete':bool(final),'all_archive_hashes_verified':True,'events_sha256':state['events_sha256'],'demo_source_revision':revision};target.with_suffix('.verified.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
if __name__=='__main__':main()
