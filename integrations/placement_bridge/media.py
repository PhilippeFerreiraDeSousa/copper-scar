"""Render actual exported fixture geometry and a timestamp-scaled 5x replay."""
import argparse
from pathlib import Path
import json
import shutil
import subprocess
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
import sexpdata as sx
from contract import pcb, read, write, sha, inventory, coverage
from copperhead import check_copy
from verify_incremental_fixture import children,one


def prepare(root,output):
    output.mkdir(parents=True,exist_ok=False);media=output/'media';media.mkdir()
    stages=['00-built','01-escapes','02-parent','03-moved']; rows=[]
    times=[]
    for i,name in enumerate(stages):
        stage=root/name
        times.append((stage/'completion.json').stat().st_mtime)
        checked=check_copy(stage,output/'checks'/name)
        board=sx.loads(pcb(stage).read_text()); inv=inventory(pcb(stage));c=coverage(pcb(stage))
        fig,ax=plt.subplots(figsize=(10,8));fig.set_facecolor('#101724');ax.set_facecolor('#101724')
        ax.add_patch(Rectangle((123.5,94),32,28,facecolor='#16312d',edgecolor='#9cc4ad',lw=2))
        ax.add_patch(Rectangle((138.5,94),2,28,facecolor='#b66150',alpha=.35,hatch='///'))
        for s in children(board,'segment'):
            a=one(s,'start')[1:];b=one(s,'end')[1:];layer=str(one(s,'layer')[1])
            ax.plot([a[0],b[0]],[a[1],b[1]],color='#ffa46b' if layer=='F.Cu' else '#70b7ff',lw=2.5,solid_capstyle='round')
        for v in children(board,'via'):
            x,y=one(v,'at')[1:];ax.add_patch(Circle((x,y),.3,fc='#f5d587',ec='white',lw=.6));ax.add_patch(Circle((x,y),.15,fc='#101724'))
        for ref,r in inv['refs'].items():
            x,y,_=r['pose'];ax.add_patch(Rectangle((x-.6,y-.6),1.2,1.2,fc='#ffa46b'))
            ax.text(x,y-1.05,ref,color='white',ha='center',fontsize=10)
        ax.set_xlim(121.5,157.5);ax.set_ylim(124,91.5);ax.set_aspect('equal');ax.axis('off')
        ax.set_title('SYNTHETIC FIXTURE · placement / routing bridge\n'+name,color='white',fontsize=17,pad=15)
        ax.text(.02,-.025,f"{checked['opens']} opens · {len(checked['violations'])} violations · {sum(v['realized'] for v in c.values())}/4 nets realized\nOrange: top copper · Blue: bottom copper · Stripe: top barrier",transform=ax.transAxes,color='#d6e2ee',fontsize=12)
        fig.text(.5,.015,'32 × 28 mm · Actual exported geometry · Not PCB Golf optimization progress',ha='center',color='#9bb1c7',fontsize=11)
        fig.savefig(media/f'board-{i:02}.png',dpi=120,facecolor=fig.get_facecolor());plt.close(fig)
        # Allowlist board + its exact project rules, not native cache/logs/runtime data.
        shutil.copy2(pcb(stage),media/f'board-{i:02}.kicad_pcb')
        shutil.copy2(pcb(stage).with_suffix('.kicad_pro'),media/f'board-{i:02}.kicad_pro')
        rows.append({'step':i,'stage':name,'comparison_kind':'synthetic_fixture_bridge','board_sha256':sha(pcb(stage)),
                     'opens':checked['opens'],'violations':len(checked['violations']),'realized_nets':sum(v['realized'] for v in c.values()),
                     'vias':checked['via_count'],'evaluation_scope':'whole eight-pad fixture','image':f'board-{i:02}.png',
                     'per_net_realization':c,'native_worker_running':False,'product_valid':False})
    # Time between completed snapshots is replayed at five times recorded speed.
    # It includes controller/check overhead, not an invented solver duration.
    timeline=[];lines=[]
    for i in range(len(stages)-1):
        duration=max(1/30,(times[i+1]-times[i])/5)
        timeline.append({'stage':stages[i],'recorded_interval_s':times[i+1]-times[i],'replay_s':duration})
        lines.extend([f"file '{(media/f'board-{i:02}.png').as_posix()}'",f'duration {duration:.9f}'])
    lines.extend([f"file '{(media/'board-03.png').as_posix()}'",'duration 1',f"file '{(media/'board-03.png').as_posix()}'"])
    (output/'frames.txt').write_text('\n'.join(lines)+'\n')
    subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(output/'frames.txt'),'-vf','fps=30,format=yuv420p','-c:v','libx264',str(media/'replay-5x.mp4')],check=True)
    fig,ax=plt.subplots(figsize=(9,4));ax.plot(range(4),[r['opens'] for r in rows],'o-',label='Native opens');ax.plot(range(4),[r['violations'] for r in rows],'s--',label='Native violations')
    ax.set_xticks(range(4),stages);ax.set_ylabel('Whole-fixture count');ax.set_title('Synthetic bridge diagnostics — not PCB Golf optimization');ax.legend();fig.tight_layout();fig.savefig(media/'loss.png',dpi=140);plt.close(fig)
    result=read(root/'sealed/result.json');decision=read(root/'consumer/decision.json')
    for source,name in [(root/'request-qualified.json','request.json'),(root/'sealed/result.json','result.json'),(root/'consumer/decision.json','decision.json')]:shutil.copy2(source,media/name)
    bundle={'schema':'synthetic-fixture-observability-v1','comparison_kind':'synthetic_fixture_bridge','rows':rows,
            'result_sha256':sha(root/'sealed/result.json'),'request_sha256':sha(root/'request-qualified.json'),
            'decision':decision['decision'],'product_valid':False,'native_move_and_barrier_s':result['termination']['elapsed_s'],
            'replay':{'speed':5,'time_basis':'completion-file wall timestamps','terminal_hold_s':1,'intervals':timeline},
            'media_sha256':{p.name:sha(p) for p in media.iterdir()}}
    write(output/'bundle.json',bundle);return bundle

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('output',type=Path);a=p.parse_args()
    prepare(a.root.resolve(),a.output.resolve())
