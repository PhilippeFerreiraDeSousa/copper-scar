"""Offline, source-bound research replay. Figures use saved native board exports."""
from pathlib import Path
import argparse,base64,json,subprocess,sys,html,textwrap
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from audit import inventory
KICAD='/Users/philippe/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli'
def main():
 ap=argparse.ArgumentParser();ap.add_argument('base',type=Path);a=ap.parse_args();base=a.base.resolve();c=base/'campaign';out=base/'replay';out.mkdir(exist_ok=True);records=json.loads((c/'records.json').read_text());initial=json.loads((c/'initial-routing-only/evaluation.json').read_text());frames=[]
 states=[('Initial legal placement: 29 opens',c/'initial-unrouted',None,'Unrouted placement. No optimization has occurred.'),('Routing alone solves the starting layout',c/'initial-routing-only',None,'29 → 0 opens. Placement was not needed for feasibility.')]
 for r in records[1:]:
  f=Path(r['folder']);pair=' ↔ '.join(r['action']['components']);states.append((r['arm']+' · proposal '+str(r['step']),f,r,'Swap '+pair+'. Preview before full-board routing.'))
  states.append((r['arm']+' · evaluated '+str(r['step']),f,r,('Retained' if r['retain'] else 'Rejected')+' after full-board routing: '+pair+'.'))
 for name,title in [('topology-trial','One-ended topology rejected'),('topology-two-ended','Two-ended topology feasible, longer')]:states.append((title,base/name,None,'Authored placement + via topology; separate follow-up, outside matched policy pilot.'))
 states.append(('Final selected board: baseline retained',c/'all-net-hpwl-3',records[3],'Both policies tied at native cost@3 = 0. Final selected wire length 436.57 mm.'))
 def board_image(folder,preview):
  board=folder/('preview.kicad_pcb' if preview else 'pcbgolf.kicad_pcb');dest=out/(folder.name+('-preview' if preview else '')+'.svg');png=dest.with_suffix('.png')
  subprocess.run([KICAD,'pcb','export','svg','--layers','F.Cu,B.Cu,F.SilkS,Edge.Cuts','--mode-single','--page-size-mode','2','--exclude-drawing-sheet','-o',str(dest),str(board)],check=True,capture_output=True)
  inv,_=inventory(board);labels=''
  for ref,v in inv.items():
   x,y=v['pose'][:2];labels+=f'<text x="{x-20:.4f}" y="{y-21.8:.4f}" font-family="sans-serif" font-size="1.0" text-anchor="middle" fill="white" stroke="black" stroke-width="0.25" paint-order="stroke">{ref}</text>'
  svg=dest.read_text().replace('</svg>',labels+'</svg>');dest.write_text(svg);subprocess.run(['/opt/homebrew/bin/rsvg-convert','-w','1500','-o',str(png),str(dest)],check=True)
  return png
 for i,(title,folder,r,note) in enumerate(states):
  preview='· proposal' in title;png=board_image(folder,preview)
  e=json.loads((folder/('evaluation.json' if (folder/'evaluation.json').exists() else 'acceptance.json')).read_text())
  fig=plt.figure(figsize=(16,9),facecolor='#101827');gs=fig.add_gridspec(2,2,width_ratios=[.9,1.9],left=.055,right=.98,top=.80,bottom=.14,hspace=.55,wspace=.12);ax=fig.add_subplot(gs[0,0]);wire=fig.add_subplot(gs[1,0]);pcb=fig.add_subplot(gs[:,1]);pcb.imshow(plt.imread(png));pcb.axis('off')
  for axis in [ax,wire]:
   axis.set_facecolor('#182538');axis.tick_params(colors='#dbe7f7');axis.spines[['top','right']].set_visible(False);axis.spines[['bottom','left']].set_color('#70849d');axis.grid(alpha=.15)
  step=max(0,r['step']-(1 if preview else 0)) if r else (3 if i==len(states)-1 else 0)
  if i==0:ax.plot([0],[29],'o',color='#ffc857');ax.set_ylim(-1,32);ax.set_title('Initial unrouted opens: 29',color='white',loc='left')
  else:
   for arm,color in [('all-net-hpwl','#43c6df'),('signal-net-hpwl','#ffc857')]:
    vals=[initial['feasibility_cost']]+[v['retained_cost'] for v in records if v['arm']==arm and v['step']<=step];ax.plot(range(len(vals)),vals,'o-' if arm=='all-net-hpwl' else 'x--',color=color,label=arm)
   ax.set_ylim(-.2,1.2);ax.set_title('Outer feasibility cost stays ZERO',color='white',loc='left');ax.legend(fontsize=8,facecolor='#182538',labelcolor='white')
  ax.set_xlabel('Placement decision (0 = routed control)',color='white');ax.set_ylabel('Native feasibility cost',color='white')
  for arm,color in [('all-net-hpwl','#43c6df'),('signal-net-hpwl','#ffc857')]:
   vals=[initial['wire_length_mm']]+[v['retained_wire_mm'] for v in records if v['arm']==arm and v['step']<=step];wire.plot(range(len(vals)),vals,'o-' if arm=='all-net-hpwl' else 'x--',color=color)
  wire.set_xlim(-.1,3.1);wire.set_ylim(420,510);wire.set_xticks([0,1,2,3]);wire.set_title('Secondary quality: routed wire length',color='white',loc='left');wire.set_ylabel('Millimeters',color='white');wire.set_xlabel('Placement decision',color='white')
  fig.text(.055,.93,'PCB LOOP  /  SMALL CIRCUIT',color='#65d9c5',fontsize=15,weight='bold');fig.text(.055,.875,title,color='white',fontsize=21,weight='bold');fig.text(.055,.82,'Routing-only initialization: 29 → 0. No claim that placement was required.',color='#ffc857',fontsize=13)
  native='Preview: unrouted' if preview else f"Native cost {e['feasibility_cost']}  |  wire {e['wire_length_mm']:.2f} mm  |  vias {e['vias']}"
  fig.text(.39,.10,native,color='white',fontsize=14);fig.text(.055,.045,'\n'.join(textwrap.wrap(note,145)),color='#cbd5e1',fontsize=11);fig.text(.97,.035,f'{i+1}/{len(states)}',color='#70849d',ha='right',fontsize=10)
  path=out/f'frame-{i:03}.png';fig.savefig(path,dpi=120);plt.close(fig);frames.append({'title':title,'note':note,'folder':str(folder),'preview':preview,'image':base64.b64encode(path.read_bytes()).decode()})
 write={'frames':frames,'protocol':json.loads((c/'protocol.json').read_text()),'higher_loop':json.loads((c/'higher-loop-decision.json').read_text())};data=json.dumps(write).replace('</','<\\/')
 page='''<!doctype html><html><meta charset="utf-8"><title>PCB Loop · Small circuit evidence</title><style>body{margin:0;background:#101827;color:white;font:16px system-ui}header{padding:12px 3%;display:flex;gap:14px;align-items:center}button,select{font:inherit;background:#263c53;color:white;border:1px solid #6b8299;border-radius:6px;padding:7px}img{display:block;width:100%;max-height:84vh;object-fit:contain}input{width:40%}details{padding:10px 3%}a{color:#65d9c5}pre{white-space:pre-wrap}</style><header><button id="play">Play</button><button id="prev">←</button><button id="next">→</button><input id="seek" type="range" min="0" value="0"><label>Speed <select id="speed"><option>.5</option><option selected>1</option><option>2</option><option>5</option></select>×</label><span id="count"></span></header><img id="frame"><details><summary>Evidence, protocol and limitations</summary><p>Offline replay of saved board states. Presentation holds each frame for3seconds at1×; actual execution timestamps and router effort are in the evidence files. Preview frames are not evaluated routed results.</p><p>Both policies produced identical swaps. Cost@3 ties0/0; no policy win. Wire length fell493.61→436.57mm (11.6%). The later explicit topology study is separate; the one-ended stub failed, the two-ended proposal was valid but longer.</p><pre id="details"></pre></details><script>const DATA=__DATA__;let idx=0,timer=null;const el=x=>document.getElementById(x);el('seek').max=DATA.frames.length-1;function show(){el('frame').src='data:image/png;base64,'+DATA.frames[idx].image;el('seek').value=idx;el('count').textContent=(idx+1)+' / '+DATA.frames.length;el('details').textContent=JSON.stringify({current:DATA.frames[idx].folder,protocol:DATA.protocol,decision:DATA.higher_loop},null,2)}function stop(){clearInterval(timer);timer=null;el('play').textContent='Play'}function run(){stop();el('play').textContent='Pause';timer=setInterval(()=>{if(idx>=DATA.frames.length-1){stop();return}idx++;show()},3000/Number(el('speed').value))}el('play').onclick=()=>timer?stop():run();el('prev').onclick=()=>{stop();idx=Math.max(0,idx-1);show()};el('next').onclick=()=>{stop();idx=Math.min(DATA.frames.length-1,idx+1);show()};el('seek').oninput=()=>{stop();idx=Number(el('seek').value);show()};el('speed').onchange=()=>{if(timer)run()};show();</script></html>'''.replace('__DATA__',data)
 (out/'index.html').write_text(page);(out/'replay-manifest.json').write_text(json.dumps([{k:v for k,v in f.items() if k!='image'} for f in frames],indent=2));subprocess.run(['/opt/homebrew/bin/ffmpeg','-y','-framerate','1/3','-i',str(out/'frame-%03d.png'),'-c:v','libx264','-r','30','-pix_fmt','yuv420p',str(out/'small-loop.mp4')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);print(out)
if __name__=='__main__':main()
