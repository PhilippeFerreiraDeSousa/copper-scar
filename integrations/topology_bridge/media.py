"""Actual exported research/topology trial snapshots and timestamp-based 5x replay."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Circle
import sexpdata as sx
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'placement_bridge'))
from verify_incremental_fixture import children,one
from contract import inventory

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def prepare(root,out):
    out.mkdir(parents=True,exist_ok=False);media=out/'media';media.mkdir();result=json.loads((root/'results.json').read_text());rows=[]
    for i,r in enumerate(result['rows']):
        pcb=next((root/r['stage']/'export').glob('*.kicad_pcb'));board=sx.loads(pcb.read_text());inv=inventory(pcb)
        fig,ax=plt.subplots(figsize=(10,8));fig.set_facecolor('#101724');ax.set_facecolor('#101724')
        ax.add_patch(Rectangle((123.5,94),32,28,facecolor='#16312d',edgecolor='#9cc4ad',lw=2));ax.add_patch(Rectangle((138.5,94),2,28,facecolor='#b66150',alpha=.35,hatch='///'))
        if children(board,'arc'):raise ValueError('Replay arc rendering not implemented; refuse omission')
        for s in children(board,'segment'):
            a=one(s,'start')[1:];b=one(s,'end')[1:];layer=str(one(s,'layer')[1]);ax.plot([a[0],b[0]],[a[1],b[1]],color='#ffa46b' if layer=='F.Cu' else '#70b7ff',lw=2.5)
        for v in children(board,'via'):
            x,y=one(v,'at')[1:];ax.add_patch(Circle((x,y),.3,fc='#f5d587'));ax.add_patch(Circle((x,y),.15,fc='#101724'))
        for ref,c in inv['refs'].items():
            x,y,_=c['pose'];ax.add_patch(Rectangle((x-.6,y-.6),1.2,1.2,fc='#ffa46b'));ax.text(x,y-1.05,ref,color='white',ha='center')
        ax.set_xlim(121.5,157.5);ax.set_ylim(124,91.5);ax.set_aspect('equal');ax.axis('off')
        ax.set_title('KRT placement + generated via sites + layer Routes\n'+r['stage']+' / '+r['decision'].upper(),color='white',fontsize=16)
        fig.text(.5,.045,f"{r['wire_length_mm']:.3f} mm actual copper length | {r['opens']} opens | {len(r['violations'])} violations",ha='center',color='white')
        fig.text(.5,.015,'Complete synthetic fixture; not PCB Golf optimization progress',ha='center',color='#9bb1c7')
        fig.savefig(media/f'board-{i:02}.png',dpi=120,facecolor=fig.get_facecolor());plt.close(fig)
        shutil.copy2(pcb,media/f'board-{i:02}.kicad_pcb');shutil.copy2(pcb.with_suffix('.kicad_pro'),media/f'board-{i:02}.kicad_pro')
        rows.append({**r,'step':i,'board_sha256':sha(pcb),'violations':len(r['violations']),'realized_nets':4,'vias':6,'image':f'board-{i:02}.png','evaluation_scope':'complete eight-pad four-net fixture'})
    concat=[];intervals=[]
    for i,r in enumerate(rows):
        duration=(rows[i+1]['completion_timestamp']-r['completion_timestamp'])/5 if i+1<len(rows) else 1
        concat += [f"file '{(media/r['image']).as_posix()}'",f'duration {duration:.9f}'];intervals.append({'stage':r['stage'],'replay_s':duration})
    concat.append(f"file '{(media/rows[-1]['image']).as_posix()}'");(out/'frames.txt').write_text('\n'.join(concat)+'\n')
    subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(out/'frames.txt'),'-vf','fps=30,format=yuv420p','-c:v','libx264',str(media/'replay-5x.mp4')],check=True)
    fig,ax=plt.subplots(figsize=(10,4));ax.plot([r['step'] for r in rows],[r['wire_length_mm'] for r in rows],'o-');ax.set_xticks(range(len(rows)),[r['stage'] for r in rows],rotation=15);ax.set_ylabel('Actual exported copper length (mm)');ax.set_title('Whole-fixture outcomes, including rejected alternatives');fig.tight_layout();fig.savefig(media/'loss.png',dpi=140);plt.close(fig)
    for p in [root/'results.json',root/'identity-audit.json',*root.glob('*research-proposal.json'),*root.glob('*-proposal.json')]:shutil.copy2(p,media/p.name)
    bundle={'schema':'synthetic-topology-observability-v1','comparison_kind':'synthetic_topology_search','product_valid':False,'rows':rows,'result_sha256':sha(root/'results.json'),'request_sha256':sha(root/'01-research-proposal.json'),'decision':'retain two successive KRT-selected moves','native_build_wall_s':sum(r['build_wall_s'] for r in rows),'replay':{'speed':5,'time_basis':'completed snapshot timestamps; includes source rebuild and evaluation overhead','terminal_hold_s':1,'intervals':intervals},'media_sha256':{p.name:sha(p) for p in media.iterdir()}}
    (out/'bundle.json').write_text(json.dumps(bundle,indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('output',type=Path);a=p.parse_args();prepare(a.root.resolve(),a.output.resolve())
