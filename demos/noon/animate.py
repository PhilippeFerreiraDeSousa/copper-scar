#!/usr/bin/env python3
"""Render native CAD evidence as motion graphics, never synthetic router geometry."""
import argparse,hashlib,json,math,subprocess,sys,textwrap
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageChops,ImageFilter
from functools import lru_cache
W,H,FPS=1600,900,24
BG='#07111b';FG='#eff6fb';MUTED='#8ca8bd';CYAN='#64e0d0';AMBER='#ffc178'
FONT='/System/Library/Fonts/Supplemental/Arial.ttf'
BOLD='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
@lru_cache(maxsize=32)
def font(n,b=False):return ImageFont.truetype(BOLD if b else FONT,n)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def wrap(draw,text,xy,width,size=24,color=FG,bold=False):
 words=text.split();line='';y=xy[1]
 for word in words:
  trial=(line+' '+word).strip()
  if draw.textlength(trial,font=font(size,bold))>width and line:draw.text((xy[0],y),line,font=font(size,bold),fill=color);line=word;y+=size*1.32
  else:line=trial
 draw.text((xy[0],y),line,font=font(size,bold),fill=color);return y+size*1.32

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--sample-only',action='store_true');a=ap.parse_args();out=a.out.resolve();data=json.loads((out/'data.json').read_text());ps={p['id']:p for p in data['projects']};shots=[]
 def add(pid,i,title,kicker,caption,seconds=5):shots.append({'project':pid,'state':i,'title':title,'kicker':kicker,'caption':caption,'seconds':seconds})
 add('medium',0,'PCB LOOP','LAYOUTS ARE HYPOTHESES','Propose. Route every layer. Let native evidence decide.',5)
 add('medium',0,'Start with the real problem.','01 / FEASIBILITY · medium-loop','85 components. 67 nets. Eight original-inspired switching blocks.',5)
 add('medium',1,'Routing alone leaves one open.','FULL-BOARD REALIZATION','183 → 1 native opens. Both copper layers. The unchanged layout is still invalid.',5)
 mi=next(i for i,s in enumerate(ps['medium']['states']) if s.get('action',{} ) and s['action'].get('kind')=='swap_placements' and s['title'].startswith('all-net-hpwl-1') and s['evaluation'] is None)
 add('medium',mi,'Swap the placements. Keep the rules.','ACTUAL PLACEMENT PROPOSAL','R112 ↔ R91. The selected policy proposes an actual swap before all-layer realization.',5)
 add('medium',mi+1,'Zero, after native checks.','FULL REROUTE → EVALUATE','The selected all-net policy swap and full reroute close the last open. Native DRC and schematic parity are zero.',6)
 stage2indices=[i for i,s in enumerate(ps['medium']['states']) if s.get('score')]
 if stage2indices:
  add('medium',stage2indices[0],'The accepted board crosses the gate.','02 / OPTIMIZATION · SAME CIRCUIT','The selected policy branch becomes Stage 2 with the identical board hash. Its baseline score is 65,288.',6)
  rejected=next(i for i in stage2indices if not ps['medium']['states'][i]['score']['valid']);add('medium',rejected,'A smaller board is not enough.','VALIDITY IS A HARD GATE','Invalid proposals have score NULL. Keep the valid incumbent at 65,288.',5)
  add('medium',stage2indices[-1],'56,499.28. Still valid.','TWO STAGES / ONE CONNECTED LINEAGE','65,288 → 59,976.20 → 56,499.28. Native opens, DRC, parity and ERC remain zero; 85 models pass.',6)
 add('stage2',0,'Now measure the whole assembly.','small-loop / OFFICIAL FORMULA','Bounding-box volume + 50 × vias + 5,000 × copper layers. All 15 populated models are present.',6)
 reject=next(i for i,s in enumerate(ps['stage2']['states']) if s.get('score') and not s['score']['valid'])
 add('stage2',reject,'Reject the tempting shortcut.','OBSERVE THE FAILURE','A tighter outline reduces volume, but leaves an open. Candidate score: null. Keep the valid board.',5)
 valid=[i for i,s in enumerate(ps['stage2']['states']) if s.get('score',{} ) and s['score']['valid'] and s.get('action') and s.get('retained')]
 for j,i in enumerate(valid):
  s=ps['stage2']['states'][i];factor=s['action'].get('spacing_factor');add('stage2',i,'Trim margin.' if factor==1 else 'Compact the placement.','REVISE → REALIZE → VERIFY',('Outline only; no components moved.' if factor==1 else 'Actual component poses change; physical part sizes stay fixed.')+' Full-board routing and native + assembly gates pass.',4)
 add('stage2',len(ps['stage2']['states'])-1,'15,900.96. Valid and frozen.','52.54% LOWER OFFICIAL SCORE','16 trials. 10 full routing runs. Six retained improvements. Zero opens, DRC, parity and ERC findings.',6)
 if 'large' in ps:add('large',len(ps['large']['states'])-1,'The next size stays honest.','large-loop / ONGOING','Additional input and routing work. Native failures remain; no accepted large-loop result is claimed.',5)
 add('stage2',len(ps['stage2']['states'])-1,'Every improvement has a receipt.','PCB LOOP / REPRODUCIBLE RESEARCH','Exact CAD. Source revisions. Keep/reject records. W&B + Weave evidence. No invented LLM calls or hardware claims.',6)
 media=out/'animation-assets';media.mkdir(exist_ok=True);boards={}
 for shot in shots:
  st=ps[shot['project']]['states'][shot['state']];h=st['board']['sha256'];png=media/(h+'.png')
  if not png.exists():subprocess.run(['/opt/homebrew/bin/rsvg-convert','-w','1800','-o',str(png),str(out/st['board']['images']['Both'])],check=True)
  boards[h]=Image.open(png).convert('RGBA')
 tiles={};glows={}
 for h,b in boards.items():
  tile=Image.new('RGBA',(859,627),(11,26,39,255));fit=min(815/b.width,565/b.height);r=b.resize((round(b.width*fit),round(b.height*fit)),Image.Resampling.LANCZOS);tile.alpha_composite(r,((859-r.width)//2,(627-r.height)//2));tiles[h]=tile
 for i,shot in enumerate(shots):
  if i and shots[i-1]['project']==shot['project']:
   h=ps[shot['project']]['states'][shot['state']]['board']['sha256'];prev=shots[i-1];ph=ps[prev['project']]['states'][prev['state']]['board']['sha256'];shot['previous_board']=ph
   if h!=ph:glows[(ph,h)]=ImageChops.difference(tiles[ph],tiles[h]).convert('L').filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(3))
 total=sum(s['seconds'] for s in shots)
 def frame(shot,t,elapsed):
  st=ps[shot['project']]['states'][shot['state']];e=st.get('evaluation');score=st.get('score');im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
  for x in range(0,W,80):d.line((x,0,x,H),fill='#0b1b29')
  for y in range(0,H,80):d.line((0,y,W,y),fill='#0b1b29')
  d.text((56,38),'PCB LOOP',font=font(24,True),fill=CYAN);d.text((1170,42),'NATIVE EVIDENCE / SAVED STATES',font=font(13),fill=MUTED)
  d.text((56,108),shot['kicker'],font=font(17,True),fill=CYAN);wrap(d,shot['title'],(56,151),570,44,FG,True)
  d.rounded_rectangle((685,110,1544,737),radius=16,fill='#0b1a27',outline='#274356',width=2)
  h=st['board']['sha256'];tile=tiles[h];ph=shot.get('previous_board');fade=min(1,t*shot['seconds']/.6)
  if ph and ph!=h and fade<1:
   tile=Image.blend(tiles[ph],tile,fade);mask=glows[(ph,h)].point(lambda v:round(v*.45*(1-fade)));glow=Image.new('RGBA',tile.size,(100,224,208,0));glow.putalpha(mask);tile=Image.alpha_composite(tile,glow)
  im.paste(tile,(685,110),tile)
  d=ImageDraw.Draw(im);d.text((713,704),'SHA '+st['board']['sha256'][:20]+'…',font=font(13),fill=MUTED)
  d.text((713,130),shot['project'].replace('stage2','small')+'-loop',font=font(17,True),fill=MUTED)
  # Values remain exact; motion reveals the graph, never invents intermediate CAD.
  if score:
   value=f"{score['official_formula_score']:,.2f}" if score['valid'] else 'NULL';label='OFFICIAL FORMULA · LOWER IS BETTER';color=CYAN if score['valid'] else AMBER
  elif e:value=str(e.get('drc_opens','—'));label='NATIVE OPEN CONNECTIONS';color=CYAN if e.get('accepted') else AMBER
  else:value='PROPOSED';label='UNROUTED PREVIEW · NO SCORE';color=AMBER
  d.text((56,303),label,font=font(16,True),fill=MUTED);d.text((50,333),value,font=font(74,True),fill=color)
  seq=ps[shot['project']]['states'][:shot['state']+1];vals=[]
  if shot['project']=='medium' and not score:seq=[s for s in seq if s['phase']=='Unrouted input' or s['title'].startswith('baseline-parity') or s['title'].startswith('all-net-hpwl')]
  for s in seq:
   if score and s.get('score'):vals.append(s.get('incumbent_score') or s['score'].get('official_formula_score'))
   elif not score and s.get('evaluation'):vals.append(s['evaluation'].get('feasibility_cost',s['evaluation'].get('drc_opens',0)))
  vals=[v for v in vals if v is not None]
  if vals:
   vmax=max(1,max(vals));points=[(65+i*520/max(1,len(vals)-1),545-v/vmax*90) for i,v in enumerate(vals)];d.line((60,550,590,550),fill='#345062',width=1)
   if len(points)>1:
    stair=[]
    for i,point in enumerate(points):
     if i:stair.append((point[0],points[i-1][1]))
     stair.append(point)
    d.line(stair,fill=CYAN,width=3)
   d.text((60,430),f'{vmax:,.0f}',font=font(12),fill=MUTED);d.text((40,538),'0',font=font(12),fill=MUTED)
   for j in sorted(set([0,len(points)-1])):
    px,py=points[j];d.text((px,py-22),f'{vals[j]:,.2f}' if score else str(vals[j]),font=font(15,True),fill=FG)
   d.text((60,600),'Initial → recorded checkpoints → current',font=font(13),fill=MUTED)
   for px,py in points:d.ellipse((px-4,py-4,px+4,py+4),fill=CYAN)
   d.text((60,570),'Retained valid score' if score else 'Recorded native checks through this state',font=font(14),fill=MUTED)
  gates=['PROPOSE','ROUTE','CHECK','KEEP' if st.get('retained') is not False else 'REJECT'];active=0 if not e else 3
  for k,label in enumerate(gates):
   left=56+k*145;accent=(AMBER if label=='REJECT' else CYAN) if k==active else '#20384a';d.rounded_rectangle((left,645,left+130,683),radius=5,fill=accent);d.text((left+15,654),label,font=font(15,True),fill=BG if k==active else MUTED)
  gate='PENDING' if not e else ('VALID' if e.get('accepted') else 'INVALID');gc=CYAN if gate=='VALID' else AMBER;d.text((56,706),gate+'  /  opens + required DRC + parity',font=font(18,True),fill=gc)
  if score:d.text((713,750),f"Native: opens {score['native']['opens']} · DRC {score['native']['violations']} · parity {score['native']['parity_findings']} · ERC {score['native']['erc_findings']}",font=font(15,True),fill=gc)
  wrap(d,shot['caption'],(56,785),1460,25,FG)
  d.text((56,855),'Saved native checkpoints · camera / cross-fade motion is presentation only · no simulated routing',font=font(13),fill=MUTED);d.text((1340,855),f'{elapsed:05.1f} / {total:05.1f} s',font=font(13),fill=MUTED)
  d.rectangle((0,894,round(W*elapsed/total),899),fill=CYAN)
  return im
 storyboard={'concept':'Native Evidence / The Validity Gate','data_sha256':sha(out/'data.json'),'render':'Pillow motion graphics + native KiCad SVG + ffmpeg H.264','resolution':[W,H],'fps':FPS,'duration_seconds':total,'shots':shots,'claude':{'cli':'2.1.119','requested_model':'Fable 5.1','used':True,'exact_model':'claude-fable-5-1[1m]','route':'Authenticated Claude Desktop Code2.1.266 Max UI','session':'local_795529c0-cbff-42de-a8e5-ebb2f394e86d','contribution':'Native image diff glow/cross-dissolve, persistent validity latch, deliberate camera; evidence corrections confirmed together.'}}
 (out/'animation-storyboard.json').write_text(json.dumps(storyboard,indent=2));frame(shots[4],.5,22).save(out/'animation-style-sample.png')
 if a.sample_only:print(json.dumps({'sample':str(out/'animation-style-sample.png'),'seconds':total,'shots':len(shots)}));return
 video=out/'pcb-loop-noon.mp4';pipe=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],stdin=subprocess.PIPE)
 elapsed=0
 for shot in shots:
  for n in range(shot['seconds']*FPS):pipe.stdin.write(frame(shot,n/(shot['seconds']*FPS-1),elapsed+n/FPS).tobytes())
  elapsed+=shot['seconds'];print('Rendered',elapsed,'/',total,flush=True)
 pipe.stdin.close();assert pipe.wait()==0;subprocess.run(['ffmpeg','-v','error','-i',str(video),'-f','null','-'],check=True);r={'data_sha256':sha(out/'data.json'),'video_sha256':sha(video),'duration_seconds':total,'full_decode_pass':True,'motion_graphics':True,'storyboard_sha256':sha(out/'animation-storyboard.json')};(out/'video-verified.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
if __name__=='__main__':main()
