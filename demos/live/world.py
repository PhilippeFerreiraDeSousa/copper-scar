"""Normalize native SVG exports to one absolute KiCad world frame per family."""
import concurrent.futures,hashlib,html,json,re,subprocess
from pathlib import Path
from cad import inventory
CLI='/Users/philippe/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli'

def export(item):
 p,layer,dst,layers=item
 if not dst.exists():
  tmp=dst.with_suffix('.tmp.svg');subprocess.run([CLI,'pcb','export','svg','--layers',(','.join(layers) if layer=='Both' else layer)+',F.SilkS,Edge.Cuts','--mode-single','--page-size-mode','0','--exclude-drawing-sheet','-o',str(tmp),str(p)],check=True,capture_output=True);tmp.replace(dst)

def apply(data,out):
 jobs=[];boards={}
 for family in data['projects']:
  for s in family['states']+family.get('history_states',[]):boards[s['board']['sha256']]=s['board']
 for h,b in boards.items():
  p=out/b['cad'];layers=[k for k in b['images'] if k!='Both']
  for layer in b['images']:jobs.append((p,layer,p.parent/(layer+'-absolute.svg'),layers))
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(export,jobs))
 for family in data['projects']:
  unique={s['board']['sha256']:s['board'] for s in family['states']+family.get('history_states',[])};xs=[0.];ys=[0.];poses={}
  for h,b in unique.items():
   pp,_,_=inventory(out/b['cad']);poses[h]=pp
   for v in pp.values():xs.extend([v[0]-8,v[0]+8]);ys.extend([v[1]-8,v[1]+8])
   # KiCad mode0 exports its raw absolute coordinates, not per-board crop coordinates.
   text=(out/b['cad']).parent.joinpath('Both-absolute.svg').read_text()
   for path in re.findall(r'\bd="([^"]+)"',text):
    values=[float(v) for v in re.findall(r'[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?',path)]
    xs.extend(values[0::2]);ys.extend(values[1::2])
   for cx,cy,r in re.findall(r'<circle[^>]*cx="([^"]+)"[^>]*cy="([^"]+)"[^>]*r="([^"]+)"',text):xs.extend([float(cx)-float(r),float(cx)+float(r)]);ys.extend([float(cy)-float(r),float(cy)+float(r)])
  x0=min(xs)-5;y0=min(ys)-5;w=max(xs)-x0+5;hgt=max(ys)-y0+5;view=[round(v,4) for v in [x0,y0,w,hgt]];digest=hashlib.sha256(json.dumps(view).encode()).hexdigest()[:12];dest=out/'world'/family['id']/digest;dest.mkdir(parents=True,exist_ok=True);family['world_frame']={'viewBox':view,'units':'mm','export_page_size_mode':0,'coordinate_system':'absolute KiCad XY; origin and scale shared across every state/layer','preserveAspectRatio':'xMidYMid meet'}
  for h,b in unique.items():
   images={}
   for layer in b['images']:
    target=dest/(h+'-'+layer+'.svg')
    if not target.exists():
     text=(out/b['cad']).parent.joinpath(layer+'-absolute.svg').read_text();text=re.sub(r'width="[^"]+" height="[^"]+" viewBox="[^"]+"',f'width="{view[2]}mm" height="{view[3]}mm" viewBox="'+ ' '.join(map(str,view))+'" preserveAspectRatio="xMidYMid meet"',text,count=1)
     grid=f'<defs><pattern id="world-grid" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M10 0H0V10" fill="none" stroke="#284055" stroke-width="0.12"/></pattern></defs><rect x="{x0}" y="{y0}" width="{w}" height="{hgt}" fill="url(#world-grid)"/>'
     text=text.replace('<title>',grid+'<title>',1)
     labels=''.join(f'<text data-ref="{html.escape(ref)}" x="{v[0]:.4f}" y="{v[1]-1.8:.4f}" font-family="sans-serif" font-size="1" text-anchor="middle" fill="white" stroke="#091320" stroke-width="0.25" paint-order="stroke">{html.escape(ref)}</text><circle data-anchor="{html.escape(ref)}" cx="{v[0]:.6f}" cy="{v[1]:.6f}" r="0.001" opacity="0"/>' for ref,v in poses[h].items())
     bar=f'<path d="M{x0+8} {y0+hgt-5}h10" stroke="white" stroke-width="0.3"/><text x="{x0+8}" y="{y0+hgt-6}" fill="white" font-size="1.5">10 mm · fixed world XY</text><circle cx="0" cy="0" r="0.7" fill="#65ddc4"/>'
     target.write_text(text.replace('</svg>',labels+bar+'</svg>'))
    images[layer]=str(target.relative_to(out))
   b['images']=images;b['world_frame']=family['world_frame']
  for s in family['states']+family.get('history_states',[]):s['board'].update(unique[s['board']['sha256']])
 return data
