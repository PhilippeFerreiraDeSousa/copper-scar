"""Frozen JITX checkpoint replay, adapted from Copperhead's actual-board rendering approach."""
from pathlib import Path
import json,hashlib,subprocess,shutil,time,sys,xml.etree.ElementTree as ET
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
B=Path('/Users/philippe/dev/copper-scar-jitx');L=B/'runs/stage1';OUT=Path('/Users/philippe/Documents/Codex/2026-09-12/realtime-voice-chat/outputs');OUT.mkdir(parents=True,exist_ok=True)
import argparse,textwrap
from copper_audit import copper
parser=argparse.ArgumentParser();parser.add_argument('--request',type=Path,required=True);args=parser.parse_args()
request=json.loads(args.request.read_text());run=Path(request['run']);cutoff=request['captured_at'];frames=[]
for step in request['steps']:
 if step['held']:
  if frames:frames.append({**frames[-1],**step,'held':True})
  continue
 e=step['evaluation'];snap=step['snapshot'];board=Path(snap['board']);assert hashlib.sha256(board.read_bytes()).hexdigest()==e['artifacts']['pcbgolf.kicad_pcb']
 assert hashlib.sha256(Path(snap['preview']).read_bytes()).hexdigest()==snap['preview_sha256']
 assert hashlib.sha256(Path(snap['record']).read_bytes()).hexdigest()==snap['evaluation_sha256']
 d=run/f'checkpoint-{len(frames):02}';d.mkdir(exist_ok=True);shutil.copy2(board,d/'pcbgolf.kicad_pcb');shutil.copy2(snap['preview'],d/'board.svg');shutil.copy2(snap['record'],d/'evaluation.json')
 inv=copper(d/'pcbgolf.kicad_pcb');edge=inv['outline_bounds_mm'];points=list(inv['placements'].values());xs=[p[0]-edge[0] for p in points];ys=[p[1]-edge[1] for p in points];x,y=min(xs)-16,min(ys)-16;w,h=max(xs)-x+16,max(ys)-y+16
 tree=ET.parse(d/'board.svg');root=tree.getroot();root.set('viewBox',f'{x} {y} {w} {h}');root.set('width',str(w));root.set('height',str(h));tree.write(d/'focused.svg',encoding='utf-8',xml_declaration=True)
 subprocess.run(['/opt/homebrew/bin/rsvg-convert','-w','1000','-o',str(d/'board.png'),str(d/'focused.svg')],check=True)
 frames.append({**step,'directory':str(d),'layers':len(inv['copper_layers'])})
colors={'bg':'#0c141b','panel':'#14232e','text':'#e6eef3','muted':'#a4b7c6','teal':'#77ddcb','amber':'#f3bb70','red':'#f69b97'}
plt.rcParams.update({'font.family':'DejaVu Sans','text.color':colors['text'],'axes.labelcolor':colors['muted'],'xtick.color':colors['muted'],'ytick.color':colors['muted']})
xs=[];ys=[];bests=[];best=None
for i,f in enumerate(frames):
 e=f['evaluation'];m=e['metrics']
 if not f['held'] and e.get('evaluation_reliable') and e.get('invariants_ok'):
  if best is None or (e['cost']<best['cost'] and all(m[k]<=best['metrics'][k] for k in ['physical_errors','incorrect_connections','erc_errors'])):best=e
  xs.append(i);ys.append(m['missing_connections']);bests.append(best['metrics']['missing_connections'])
 fig=plt.figure(figsize=(19.2,10.8),dpi=100,facecolor=colors['bg']);fig.text(.05,.94,'JITX  /  STAGE ONE',fontsize=16,color=colors['teal'],weight='bold');fig.text(.05,.885,'Placement → retained-copper routing → checks',fontsize=29,weight='bold');fig.text(.05,.84,'Rechecked checkpoint history · policy v3 · earlier v1/v2 reports superseded',fontsize=15,color=colors['muted']);fig.text(.96,.94,'INCOMPLETE / NO VALID BOARD',fontsize=15,color=colors['amber'],ha='right')
 ax=fig.add_axes([.055,.29,.425,.46],facecolor=colors['panel']);ax.set_xlim(-.3,len(frames)-.6);ax.set_ylim(0,max(550,max(x['evaluation']['metrics']['missing_connections'] for x in frames if x.get('evaluation'))*1.1));ax.plot(xs,ys,color=colors['teal'],lw=2.5,label='Attempted opens');ax.plot(xs,bests,color=colors['amber'],lw=2,ls='--',label='Retained incumbent')
 for j,n in zip(xs,ys):ax.scatter(j,n,s=85 if j==i else 30,color=colors['teal'],zorder=4);ax.annotate(str(n),(j,n),xytext=(0,12),textcoords='offset points',ha='center',fontsize=10,color=colors['text'])
 if f['held']:ax.axvline(i,color=colors['red'],ls=':',label='Failed; no evaluated output')
 ax.set_xlabel('Recorded physical action / checkpoint',fontsize=13,labelpad=12);ax.set_ylabel('Missing connections (KiCad DRC)',fontsize=13,labelpad=10);ax.set_xticks(range(len(frames)));ax.grid(axis='y',alpha=.15)
 for sp in ax.spines.values():sp.set_color('#355061')
 leg=ax.legend(loc='lower left',frameon=False,fontsize=12)
 for text in leg.get_texts():text.set_color(colors['muted'])
 bx=fig.add_axes([.53,.29,.43,.47],facecolor=colors['panel']);bx.imshow(mpimg.imread(Path(f['directory'])/'board.png'));bx.set_axis_off();fig.text(.54,.785,textwrap.fill(f'{i+1:02d} · {f["label"]}',55),fontsize=14,color=colors['muted'])
 status='FAILED / no evaluated output; previous captured board held' if f['held'] else 'UNRELIABLE CHECK / excluded from curve' if not e.get('evaluation_reliable') else 'RETAINED INCOMPLETE' if e['candidate']==best['candidate'] else 'REJECTED / incomplete candidate'
 fig.text(.54,.25,status,fontsize=16,color=colors['red'] if f['held'] else colors['amber']);fig.text(.055,.20,f'Board: {m["missing_connections"] if e.get("evaluation_reliable") else "unknown"} opens   /   incumbent {best["metrics"]["missing_connections"]}',fontsize=21,weight='bold');fig.text(.055,.155,f'Physical errors {m["physical_errors"]} · warnings {m["physical_warnings"]} · parity {m["parity_issues"]} · ERC {m["erc_errors"]}' if e.get('evaluation_reliable') else 'Repeated DRC disagreed; counts not accepted',fontsize=15,color=colors['muted']);fig.text(.055,.112,f'{f["layers"]} copper layers · circuit invariants passed · footprint / assembly / SI gates unqualified',fontsize=14,color=colors['muted']);fig.text(.54,.20,textwrap.fill(f['caption'],53),fontsize=12,color=colors['muted']);fig.text(.54,.155,'Actual outer-copper view; empty area cropped.',fontsize=13,color=colors['muted']);fig.text(.54,.115,'No synthetic geometry or interpolated routing.',fontsize=13,color=colors['muted']);fig.text(.055,.045,'JITX and Copperhead raw costs are not directly comparable. Layer/footprint/check coverage differs.',fontsize=12,color=colors['muted']);fig.text(.96,.045,f'{i+1} / {len(frames)}',fontsize=13,ha='right');fig.savefig(run/f'frame-{i:02}.png',facecolor=fig.get_facecolor());plt.close(fig)
for label,total in [('5x',6)]:
 last=0.8;each=(total-last)/(len(frames)-1);concat=run/(label+'.txt');concat.write_text(''.join(f"file 'frame-{i:02}.png'\nduration {last if i==len(frames)-1 else each}\n" for i in range(len(frames)))+f"file 'frame-{len(frames)-1:02}.png'\n")
 video=run/'jitx-stage-one-replay-5x.mp4';subprocess.run(['/opt/homebrew/bin/ffmpeg','-y','-hide_banner','-loglevel','error','-f','concat','-safe','0','-i',str(concat),'-vf','fps=30','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart','-t',str(total),str(video)],check=True);target=OUT/'jitx-latest-replay-5x.mp4';temp=target.with_suffix('.tmp');shutil.copy2(video,temp);temp.replace(target)
manifest={'key':request['key'],'cutoff_checkpoint':request['cutoff_checkpoint'],'cutoff_record_index':request['cutoff_record_index'],'cutoff_time':request['cutoff_time'],'earliest':request['earliest'],'cutoff_unix':cutoff,'policy':'jitx-feasibility-v3','method':'Rechecked immutable physical action chronology, including held prior boards for failed attempts and excluding unreliable checks from the curve. No rerouting or geometry interpolation. Older policy-v1/v2 measurements are superseded, not connected into this curve. 5x playback:30seconds of checkpoint history condensed to6seconds.', 'frames':[{k:v for k,v in f.items() if k!='evaluation'} for f in frames],'videos':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in run.glob('*.mp4')}};(run/'manifest.json').write_text(json.dumps(manifest,indent=2));shutil.copy2(run/'manifest.json',OUT/'jitx-latest-replay-5x-manifest.json');(run/'index.html').write_text('<!doctype html><html><meta charset="utf-8"><title>JITX replay 5x</title><body style="margin:0;background:#0c141b"><video style="width:100%;height:100vh" controls autoplay muted playsinline src="jitx-stage-one-replay-5x.mp4"></video></body></html>');print(json.dumps({'run':str(run),'url':'http://127.0.0.1:53919/file/'+str(run.relative_to(B))+'/index.html','video':str(OUT/'jitx-latest-replay-5x.mp4')},indent=2),flush=True)
