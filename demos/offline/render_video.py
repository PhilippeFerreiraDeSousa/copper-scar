#!/usr/bin/env python3
"""Render a narrated-by-presenter snapshot edit (not solver wall-clock time).
Requires Playwright, a Chromium executable, and ffmpeg on PATH.
"""
import argparse, hashlib, json, subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright
p=argparse.ArgumentParser();p.add_argument('package',type=Path);p.add_argument('--browser',default='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome');a=p.parse_args();out=a.package.resolve();frames=out/'video-frames';frames.mkdir(exist_ok=True)
d=json.loads((out/'data.json').read_text());hist=d['history'];manifest=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path=a.browser,headless=True);page=b.new_page(viewport={'width':1920,'height':1080},device_scale_factor=1)
 errors=[];page.on('pageerror',lambda e: errors.append(str(e)));page.goto((out/'index.html').as_uri())
 # Fit the synchronized dashboard and loop diagram into the video canvas.
 page.add_style_tag(content='main{padding:24px 42px}.intro{margin-bottom:18px}header{margin-bottom:18px}.board{height:470px}.lower,details,footer{display:none}.flow{margin:16px 0}h1{font-size:38px}')
 for i,r in enumerate(hist):
  page.evaluate('(i)=>showAttempt(i)',i)
  page.wait_for_function('document.querySelector("#board").hidden || (document.querySelector("#board").complete && document.querySelector("#board").naturalWidth>0)')
  page.screenshot(path=str(frames/f'{i:03}.png'))
  manifest.append(dict(frame=f'video-frames/{i:03}.png',attempt=r['id'],board_sha256=r.get('board_sha256'),seconds=150/len(hist)))
 page.goto((out/'index.html').as_uri());page.add_style_tag(content='.layout,.intro,.flow,details,footer{display:none}.lower{margin-top:100px}.lower h2{font-size:48px}.lower p{font-size:22px}.lower .panel{padding:35px}.eyebrow{font-size:15px}')
 page.screenshot(path=str(frames/'fixture-scope.png'));manifest.append(dict(frame='video-frames/fixture-scope.png',seconds=15,scope='Separate bounded fixture and explicit whole-board limitations'))
 if (out/'docs/architecture.svg').exists():
  page.goto((out/'index.html').as_uri());page.evaluate("document.body.innerHTML='<img src=\"docs/architecture.svg\" style=\"width:100vw;height:100vh;object-fit:contain\">'");page.wait_for_function("document.querySelector('img').complete");page.screenshot(path=str(frames/'architecture.png'));manifest.append(dict(frame='video-frames/architecture.png',seconds=15,scope='Architecture diagram, no numerical inference'))
 else: manifest[-1]['seconds']+=15
 if errors: raise RuntimeError(errors)
 b.close()
concat=out/'video-frames/concat.txt';concat.write_text(''.join(f"file '{Path(x['frame']).name}'\nduration {x['seconds']:.9f}\n" for x in manifest)+f"file '{Path(manifest[-1]['frame']).name}'\n")
subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(concat),'-vf','fps=30,format=yuv420p','-c:v','libx264','-preset','fast','-crf','21','-t','180','-movflags','+faststart',str(out/'copper-scar-demo-normal.mp4')],check=True)
subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(out/'copper-scar-demo-normal.mp4'),'-vf','setpts=PTS/5,fps=30','-an','-c:v','libx264','-preset','fast','-crf','21','-movflags','+faststart',str(out/'copper-scar-demo-5x.mp4')],check=True)
for name in ['copper-scar-demo-normal.mp4','copper-scar-demo-5x.mp4']:
 subprocess.run(['ffmpeg','-v','error','-i',str(out/name),'-f','null','-'],check=True)
 receipt=json.loads(subprocess.check_output(['ffprobe','-v','quiet','-show_streams','-show_format','-of','json',str(out/name)]))
 (out/(name+'.probe.json')).write_text(json.dumps(receipt,indent=2))
(out/'video-manifest.json').write_text(json.dumps(dict(method='Edited native snapshot presentation, not real elapsed solver time. All history at equal dwell, no geometry interpolation; final scope and architecture cards. Silent: use presenter script.',normal_duration_seconds=180,speedup=5,frames=manifest,video_sha256={name:hashlib.sha256((out/name).read_bytes()).hexdigest() for name in ['copper-scar-demo-normal.mp4','copper-scar-demo-5x.mp4']}),indent=2))
print(json.dumps(dict(frames=len(manifest),browser_errors=errors,decoded=True)))
