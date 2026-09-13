"""Render a frozen, evidence-linked checkpoint replay; no routing is run."""
import json,hashlib,shutil,subprocess,argparse
from pathlib import Path
from datetime import datetime,timezone
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
ROOT=Path(__file__).resolve().parents[1];LOCAL=ROOT/'.local/copperhead';OUT=Path('/Users/philippe/Documents/Codex/2026-09-12/realtime-voice-chat/outputs')
ap=argparse.ArgumentParser();ap.add_argument('--snapshot',type=Path);ap.add_argument('--output-dir',type=Path);args=ap.parse_args()
snapshot=json.loads(args.snapshot.read_text()) if args.snapshot else None
cutoff=datetime.fromisoformat(snapshot['cutoff']) if snapshot else datetime.now(timezone.utc);run=args.output_dir or LOCAL/'replays'/cutoff.strftime('%Y%m%d-%H%M%S');run.mkdir(exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
kicad='/Users/philippe/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli'
records=[]
for p in ([] if snapshot else sorted((LOCAL/'runs').glob('stage1-*/attempt.json'))):
 a=json.loads(p.read_text())
 if a.get('status') in ('completed','failed') and a.get('before'):
  records.append((p,a))
if snapshot:records=[(Path(x['path']),x['record']) for x in snapshot['records']]
assert records
frames=[]
def checkpoint(label,board,evaluation,record=None):
 expected=evaluation['files']['pcbgolf.kicad_pcb'];actual=hashlib.sha256(board.read_bytes()).hexdigest()
 assert actual==expected, 'Board drift since native evaluation: '+str(board)
 i=len(frames);d=run/f'checkpoint-{i:02d}';d.mkdir();shutil.copyfile(board,d/'pcbgolf.kicad_pcb')
 shutil.copyfile(evaluation['report'],d/'drc.json');(d/'evaluation.json').write_text(json.dumps(evaluation,indent=2))
 if record:(d/'attempt.json').write_text(json.dumps(record,indent=2))
 subprocess.run([kicad,'pcb','export','svg','--layers','F.Cu,B.Cu,F.SilkS,Edge.Cuts','--mode-single','--page-size-mode','2','--exclude-drawing-sheet','-o',str(d/'board.svg'),str(d/'pcbgolf.kicad_pcb')],check=True,capture_output=True)
 subprocess.run(['/opt/homebrew/bin/rsvg-convert','-w','1000','-o',str(d/'board.png'),str(d/'board.svg')],check=True)
 frames.append(dict(label=label,directory=d,evaluation=evaluation,record=record,board_sha256=actual,source=str(board)))
p,a=records[0];checkpoint('Earliest available native checkpoint',p.parent/'input/pcbgolf.kicad_pcb',a['before'])
for p,a in records:
 e=a.get('after')
 if e and e.get('files') and e.get('report'):
  checkpoint(a['attempt'],Path(a['candidate'])/'pcbgolf.kicad_pcb',e,a)
 else:
  previous=frames[-1];frames.append(dict(previous,label=a['attempt'],record=a,held=True))
colors=dict(bg='#0c141b',panel='#14232e',text='#e6eef3',muted='#9fb3c2',teal='#77ddcb',amber='#f3bb70',red='#f69b97')
plt.rcParams.update({'font.family':'DejaVu Sans','text.color':colors['text'],'axes.labelcolor':colors['muted'],'xtick.color':colors['muted'],'ytick.color':colors['muted']})
missing=[f['evaluation']['unconnected'] for f in frames];incumbent=frames[0];best=[]
def priority(f):
 e=f['evaluation'];r=f.get('record')
 return tuple(r['diagnostic_priority_after']) if r and r.get('diagnostic_priority_after') else (0,0,0,0,0,e['unconnected'],e['search_cost']['total_missing_endpoint_distance_mm'],e['warnings'])
for i,f in enumerate(frames):
 r=f.get('record');e=f['evaluation']
 if i and (r.get('became_incumbent') is True or ('became_incumbent' not in r and r['status']=='completed' and e['invariants_ok'] and priority(f)<priority(incumbent))):incumbent=f
 best.append(incumbent['evaluation']['unconnected'])
 fig=plt.figure(figsize=(19.2,10.8),dpi=100,facecolor=colors['bg'])
 fig.text(.055,.93,'COPPERHEAD  /  STAGE ONE',fontsize=16,color=colors['teal'],weight='bold')
 fig.text(.055,.882,'Searching for a valid board',fontsize=34,weight='bold')
 fig.text(.055,.835,'Accelerated checkpoint replay · native KiCad outer-copper views · no interpolated geometry',fontsize=15,color=colors['muted'])
 fig.text(.95,.93,'PARTIAL  /  NO VALID BOARD',fontsize=16,color=colors['amber'],ha='right',weight='bold')
 ax=fig.add_axes([.06,.28,.42,.46],facecolor=colors['panel']);ax.set_xlim(-.3,len(frames)-.7);ax.set_ylim(0,max(missing)*1.15)
 ax.plot(range(i+1),missing[:i+1],color=colors['teal'],lw=2.5,label='Attempted checkpoint')
 ax.plot(range(i+1),best[:i+1],color=colors['amber'],lw=2,ls='--',label='Retained incumbent')
 for j in range(i+1):
  rr=frames[j].get('record');failed=rr and rr['status']=='failed';regressed=rr and rr.get('diagnostic_improved') is False
  ax.scatter(j,missing[j],s=70 if j==i else 28,marker='x' if failed else 'o',color=colors['red'] if failed else colors['amber'] if regressed else colors['teal'],zorder=5)
 ax.annotate(str(missing[i]),(i,missing[i]),xytext=(0,15),textcoords='offset points',ha='center',fontsize=18,weight='bold',color=colors['text'])
 ax.set_xlabel('Saved attempt (0 = starting checkpoint)',fontsize=15,labelpad=14);ax.set_ylabel('Native missing connections (endpoint pairs)',fontsize=15,labelpad=12)
 ax.set_xticks(list(range(0,len(frames),max(1,len(frames)//8))));ax.grid(axis='y',alpha=.15);ax.tick_params(labelsize=12)
 for spine in ax.spines.values():spine.set_color('#355061')
 leg=ax.legend(loc='lower left',fontsize=13,frameon=False)
 for text in leg.get_texts():text.set_color(colors['muted'])
 bx=fig.add_axes([.53,.265,.43,.50],facecolor=colors['panel']);bx.imshow(mpimg.imread(f['directory']/'board.png'));bx.set_axis_off()
 action=r.get('action',{}).get('kind','Starting checkpoint') if r else 'Starting checkpoint'
 state='Producer failed · independently rechecked; not promoted' if r and r['status']=='failed' else 'Regression retained separately' if r and r.get('diagnostic_improved') is False else 'Checked partial candidate'
 if r and r.get('classification'):state=r['classification'].replace('_',' ')+' · trial board; incumbent shown at left'
 if f.get('held'):state='Failed attempt · previous verified board held'
 fig.text(.54,.785,f'CHECKPOINT {i:02d}  ·  {action.replace("_"," ")}',fontsize=17,color=colors['muted'])
 fig.text(.54,.24,state,fontsize=16,color=colors['red'] if r and r['status']=='failed' else colors['amber'])
 fig.text(.06,.17,f'{missing[i]} missing connections    /    incumbent {best[i]}',fontsize=22,weight='bold')
 fig.text(.06,.125,f'Physical errors {e["errors"]}   ·   warnings {e["warnings"]}   ·   reference invariants {"passed" if e["invariants_ok"] else "FAILED"}',fontsize=16,color=colors['muted'])
 move=r.get('placement_delta',{}).get('moves',[]) if r else []
 if move:
  m=move[0];caption=f'{len(move)} moved/rotated: '+', '.join(x['ref'] for x in move)+'; first '+f'{m["ref"]}: {tuple(m["from_mm"])} → {tuple(m["to_mm"])} mm; {m["from_degrees"]:g}° → {m["to_degrees"]:g}°'
 elif not r:caption='Starting board from the first preserved native evaluation'
 else:caption='Saved copper state; component placements unchanged in this action' if r and action!='placement_repair' else 'Placement producer failed; see preserved native inspection'
 fig.text(.54,.17,caption,fontsize=14,color=colors['muted'],wrap=True)
 fig.text(.06,.055,f'Cutoff {cutoff.strftime("%Y-%m-%d %H:%M:%S UTC")}  ·  {len(records)} finalized attempts  ·  native-defects-v1',fontsize=12,color=colors['muted'])
 fig.text(.95,.055,f'{i+1} / {len(frames)}',fontsize=14,ha='right',color=colors['muted'])
 fig.savefig(run/f'frame-{i:02d}.png',facecolor=fig.get_facecolor());plt.close(fig)
concat=run/'frames.txt';concat.write_text(''.join(f"file 'frame-{i:02d}.png'\nduration {(5 if i==len(frames)-1 else min(2.6,33/max(1,len(frames)-1)))/(5 if snapshot else 1)}\n" for i in range(len(frames)))+f"file 'frame-{len(frames)-1:02d}.png'\n")
video=run/('copperhead-latest-replay-5x.mp4' if snapshot else 'copperhead-stage-one-replay.mp4');subprocess.run(['/opt/homebrew/bin/ffmpeg','-hide_banner','-loglevel','error','-f','concat','-safe','0','-i',str(concat),'-vf','fps=30','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],check=True)
manifest=dict(cutoff=cutoff.isoformat(),frames=[{k:str(v) if isinstance(v,Path) else v for k,v in f.items() if k not in ('evaluation','record')} for f in frames],attempt_count=len(records),video_sha256=hashlib.sha256(video.read_bytes()).hexdigest(),latest_attempt=records[-1][1]['attempt'],latest_completed_at=records[-1][1]['finished_at'],earliest='First preserved native evaluation; earlier preparation has no replay snapshots',method='Discrete verified board snapshots fitted to view; no geometry interpolation')
(run/'manifest.json').write_text(json.dumps(manifest,indent=2));shutil.copyfile(video,OUT/video.name);shutil.copyfile(run/'manifest.json',OUT/('copperhead-latest-replay-manifest.json' if snapshot else 'copperhead-stage-one-replay-manifest.json'))
(run/'index.html').write_text('<!doctype html><html><head><meta name="viewport" content="width=device-width"><title>Copperhead checkpoint replay</title><style>html,body{margin:0;background:#0c141b;height:100%}video{width:100%;height:100%;object-fit:contain}</style></head><body><video controls autoplay muted loop playsinline src="' + video.name + '"></video></body></html>')
print(json.dumps(dict(run=str(run),video=str(OUT/video.name),url='http://127.0.0.1:53918/file/'+str(run.relative_to(LOCAL))+'/index.html',frames=len(frames)),indent=2))
