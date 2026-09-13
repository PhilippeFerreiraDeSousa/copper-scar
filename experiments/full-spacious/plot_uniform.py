"""Fixed-world-scale placement envelopes and a ghost overlay for a uniform trial."""
import argparse,json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
ap=argparse.ArgumentParser();ap.add_argument('manifest',type=Path);ap.add_argument('output',type=Path);a=ap.parse_args();m=json.loads(a.manifest.read_text());after=m['after_outline_mm'];before=m['before_outline_mm']
fig,axes=plt.subplots(1,3,figsize=(20,8),facecolor='#101820')
for ax,title,states in zip(axes,['Prior ring floorplan',f"Uniform position scale ×{float(__import__('fractions').Fraction(m['scale'])):g}",'Overlay: grey before, cyan after'],[['before'],['after'],['before','after']]):
 ax.set_facecolor('#101820')
 for state in states:
  color='#9badbc' if state=='before' else '#3be1cb';box=before if state=='before' else after
  ax.add_patch(Rectangle((box[0],box[1]),box[2]-box[0],box[3]-box[1],fill=False,edgecolor=color,lw=1.3,ls='--' if state=='before' else '-'))
  for row in m['poses']:
   z=[x/1e6 for x in row[state+'_envelope_nm']];ax.add_patch(Rectangle((z[0],z[1]),z[2]-z[0],z[3]-z[1],fill=False,edgecolor=color,lw=.45,alpha=.75))
   if len(states)==1 and row['ref'].startswith(('U','J')):ax.text(z[0],z[1]-.6,row['ref'],fontsize=5.5,color='white')
 cx,cy=[x/1e6 for x in m['center_nm']];ax.plot(cx,cy,'+',color='#ffbd69',ms=10);ax.set_title(title,color='white',fontsize=13);ax.set_xlim(after[0]-5,after[2]+5);ax.set_ylim(after[3]+5,after[1]-5);ax.set_aspect('equal');ax.tick_params(colors='#b5c4d0');ax.set_xlabel('mm — identical world scale in every panel',color='#b5c4d0',fontsize=9)
fig.suptitle('All 245 components: anchor positions scaled about (170, 102.5) mm\nFootprint envelopes retain their dimensions and orientations; no routing yet',color='white',fontsize=14)
fig.tight_layout(rect=(0,0,1,.90));a.output.parent.mkdir(parents=True,exist_ok=True);fig.savefig(a.output,dpi=180,facecolor=fig.get_facecolor())
