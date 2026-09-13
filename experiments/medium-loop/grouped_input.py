"""Place connected SBU blocks together; rank resistor slots by exact pad HPWL."""
from pathlib import Path
import argparse,copy,itertools,json
import sexpdata as sx
from audit import nodes,first
from campaign import write,sha
ap=argparse.ArgumentParser();ap.add_argument('base',type=Path);a=ap.parse_args();base=a.base.resolve();out=base/'stage2/grouped-input';out.mkdir();m=json.loads((base/'input/circuit.json').read_text());source=base/'stage2/baseline/pcbgolf.kicad_pcb';d=sx.loads(source.read_text());fps={next(p[2] for p in nodes(f,'property') if p[1]=='Reference'):f for f in nodes(d,'footprint')};netrefs={n:{p.split('.')[0] for p in ps} for n,ps in m['nets'].items() if n not in ['GND','EXT_5V']};offsets={r+'.'+str(p[1]):first(p,'at')[1:3] for r,f in fps.items() for p in nodes(f,'pad') if p[1]};groups={};placements={};records=[]
for idx,j in enumerate(sorted(m['original_ref_aliases'])):
 g={j}
 while True:
  nxt=set(g)
  for rs in netrefs.values():
   if g&rs:nxt|=rs
  if nxt==g:break
  g=nxt
 assert len(g)==10 and len([r for r in g if r.startswith('J')])==1
 groups[j]=sorted(g);x=27+12*(idx%4);y=25 if idx<4 else 65;direction=1 if idx<4 else-1;local={j:[x,y,0]};q=next(r for r in g if r.startswith('Q'));led=next(r for r in g if r.startswith('LED'));local[q]=[x,y+7*direction,0];local[led]=[x-3,y+11*direction,0];rs=sorted(r for r in g if r.startswith('R'));slots=[(x+dx,y+dy*direction,0) for dx,dy in [(-3,7),(3,7),(-3,15),(0,15),(-3,18),(0,18),(3,15)]];nets=[pads for n,pads in m['nets'].items() if n not in ['GND','EXT_5V'] and set(p.split('.')[0] for p in pads)<=g]
 def hpwl(ps):
  total=0
  for pads in nets:
   xs=[ps[p.split('.')[0]][0]+offsets[p][0] for p in pads];ys=[ps[p.split('.')[0]][1]+offsets[p][1] for p in pads];total+=max(xs)-min(xs)+max(ys)-min(ys)
  return total
 best=None
 for perm in itertools.permutations(slots):
  ps={**local,**dict(zip(rs,perm))};rank=(hpwl(ps),perm)
  if best is None or rank<best[0]:best=(rank,ps)
 placements.update(best[1]);records.append({'header':j,'members':sorted(g),'resistor_slot_permutations':5040,'selected_pad_hpwl_mm':best[0][0]})
extras=sorted(set(fps)-set(placements));assert extras==['C46','C5','C50','LED6','R74'];placements.update({'C46':[70,39,0],'C5':[70,42,0],'C50':[70,47,0],'LED6':[70,52,0],'R74':[70,56,0]})
for r,f in fps.items():first(f,'at')[1:]=placements[r]
d[:]=[v for v in d if not(isinstance(v,list) and v and str(v[0]) in ['segment','via','arc','zone'])];(out/'pcbgolf.kicad_pcb').write_text(sx.dumps(d));write(out/'proposal.json',{'kind':'connected_functional_block_placement','parent_board_sha256':sha(source),'groups':records,'placements':placements,'reason':'Keep all8independentlycontrolled SBU circuits near their own external headers; reduce cross-board signal paths. Preserve exactpads/nets/rules; reserve explicit sharedsupplysidecolumn. Fullrouting/nativeevaluation still required.','llm_calls':0,'copper_removed':True});print(out)
