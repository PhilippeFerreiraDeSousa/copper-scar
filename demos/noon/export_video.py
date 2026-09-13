#!/usr/bin/env python3
"""Render a chronological, source-bound video from the frozen viewer."""
import argparse,hashlib,json,subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();out=a.out.resolve();data=json.loads((out/'data.json').read_text());frames=out/'video-frames';frames.mkdir(exist_ok=True);schedule=[]
 # Show medium feasibility first, then small routing control and official objective.
 order=sorted(range(len(data['projects'])),key=lambda i:{'medium':0,'small':1,'stage2':2,'large':3}.get(data['projects'][i]['id'],4))
 for pi in order:
  p=data['projects'][pi]
  indices=list(range(len(p['states'])))
  if p['id']=='small':indices=[0,1,2,3,6,7,len(p['states'])-2,len(p['states'])-1]
  for i in sorted(set(indices)):schedule.append({'project_index':pi,'project':p['id'],'state':i,'title':p['states'][i]['title'],'seconds':2})
 with sync_playwright() as pw:
  b=pw.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True);page=b.new_page(viewport={'width':1920,'height':1080},device_scale_factor=1);page.goto((out/'index.html').as_uri());page.add_style_tag(content='header{padding:12px 3%}header h1{font-size:30px}header p{margin:0}nav{padding-top:10px}main{padding-top:8px}h2{font-size:23px}.banner{margin:8px 0;padding:10px 15px}.layout{margin-top:10px;gap:16px}.panel{padding:14px}.board{height:400px}.footer,main>details,#remote{display:none}.panel details{display:none}.panel h3{margin:10px 0}.chart{height:155px!important}.metric{padding:8px}.state{font-size:12px}#scoreNote{font-size:11px;max-height:64px;overflow:hidden}')
  for n,item in enumerate(schedule):
   page.evaluate('([p,i])=>window.demo.select(p,i)',[item['project_index'],item['state']]);page.wait_for_function('document.querySelector("#board").complete&&document.querySelector("#board").naturalWidth>0');page.screenshot(path=str(frames/f'frame-{n:03}.png'))
  b.close()
 video=out/'pcb-loop-noon.mp4';subprocess.run(['ffmpeg','-y','-v','error','-framerate','1/2','-i',str(frames/'frame-%03d.png'),'-frames:v',str(len(schedule)*60),'-c:v','libx264','-r','30','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],check=True);subprocess.run(['ffmpeg','-v','error','-i',str(video),'-f','null','-'],check=True)
 report={'data_sha256':sha(out/'data.json'),'video_sha256':sha(video),'duration_seconds':2*len(schedule),'frames':schedule,'full_decode_pass':True};(out/'video-verified.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='frames'}))
if __name__=='__main__':main()
