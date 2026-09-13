"""Position-only comparison; native SVGs remain the footprint/copper evidence."""
import argparse,json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
ap=argparse.ArgumentParser();ap.add_argument('root',type=Path);a=ap.parse_args()
groups=json.loads((Path(__file__).parent/'groups.json').read_text())
membership={r:i for i,rs in enumerate(groups.values()) for r in rs}
fig,axes=plt.subplots(1,2,figsize=(14,9),facecolor='#101820')
for ax,name,title in zip(axes,['original-control-preflight','spacious-baseline-r2'],['Original positions','Package-aware spacious grid']):
 data=json.loads((a.root/name/'input/initialization.json').read_text());box=data['outline_mm'];ax.set_facecolor('#101820')
 ax.add_patch(Rectangle((box[0],box[1]),box[2]-box[0],box[3]-box[1],fill=False,edgecolor='#94a8b8',lw=1))
 for move in data['moves']:
  x,y,_=move['after'];ref=move['ref'];ax.scatter(x,y,s=12,c=[plt.get_cmap('tab20')(membership[ref]%20)],edgecolors='none')
  if ref.startswith(('U','J')):ax.text(x+.5,y,ref,fontsize=6,color='white')
 ax.set_title(f'{title}\n{box[2]-box[0]:.0f} × {box[3]-box[1]:.0f} mm',color='white')
 ax.set_aspect('equal');ax.set_xlim(box[0]-4,box[2]+4);ax.set_ylim(box[3]+4,box[1]-4);ax.tick_params(colors='#b5c4d0');ax.set_xlabel('mm',color='#b5c4d0')
fig.suptitle('Complete PCB Golf design — all 245 components\nPosition overview; use native checks for footprint and routing geometry',color='white',fontsize=14)
fig.tight_layout(rect=(0,0,1,.90))
fig.savefig(a.root/'initial-placement-comparison.png',dpi=160,facecolor=fig.get_facecolor())
