#!/usr/bin/env python3
"""Render the scripted three-minute edit; speed is presentation, not solver time.
Requires Playwright, Chromium, and ffmpeg. No foreground browser is used.
"""
import argparse, hashlib, json, subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright
p=argparse.ArgumentParser();p.add_argument('package',type=Path);p.add_argument('--browser',default='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome');a=p.parse_args();out=a.package.resolve();frames=out/'video-frames';frames.mkdir(exist_ok=True)
d=json.loads((out/'data.json').read_text());hist=d['history'];manifest=[]
def item(name,seconds,**extra): return dict(frame='video-frames/'+name,seconds=seconds,**extra)
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path=a.browser,headless=True);page=b.new_page(viewport={'width':1920,'height':1080},device_scale_factor=1)
 errors=[];page.on('pageerror',lambda e: errors.append(str(e)));page.goto((out/'index.html').as_uri())
 page.add_style_tag(content='main{padding:24px 42px}.intro{margin-bottom:18px}header{margin-bottom:18px}.board{height:470px}#placement-gain,#gain,#diagnostics,#feedback,.lower,details,footer{display:none}.flow{margin:16px 0}h1{font-size:38px}')
 retained=max((i for i,r in enumerate(hist) if r.get('retained') and r.get('image') and not r.get('failed')),default=0)
 for i,r in enumerate(hist):
  page.evaluate('(i)=>showAttempt(i)',i);page.wait_for_function('document.querySelector("#board").hidden || (document.querySelector("#board").complete && document.querySelector("#board").naturalWidth>0)')
  page.screenshot(path=str(frames/f'{i:03}.png'))
 manifest.append(item(f'{retained:03}.png',25,chapter='Introduction',attempt=hist[retained]['id'],board_sha256=hist[retained].get('board_sha256')))
 page.goto((out/'index.html').as_uri());page.evaluate("document.body.innerHTML='<img src=\"docs/architecture.svg\" style=\"width:100vw;height:100vh;object-fit:contain\">'");page.wait_for_function("document.querySelector('img').complete");page.screenshot(path=str(frames/'architecture.png'))
 manifest.append(item('architecture.png',25,chapter='Architecture'))
 manifest.extend(item(f'{i:03}.png',30/len(hist),chapter='Complete historical trajectory',attempt=r['id'],board_sha256=r.get('board_sha256')) for i,r in enumerate(hist))
 feedback_path=out/'feedback-chain/portable.json'
 gain_path=out/'topology-gain/summary.json'
 placement_path=out/'placement-gain/summary.json'
 if placement_path.exists():
  placement=json.loads(placement_path.read_text());before=next(i for i,r in enumerate(hist) if r.get('board_sha256')==placement['parent_board_sha256']);after=next(i for i,r in enumerate(hist) if r['id']==placement['attempt'])
  manifest.append(item(f'{before:03}.png',10,chapter='54-open parent: isolated R37 CMD pad',attempt=hist[before]['id'],board_sha256=hist[before]['board_sha256']))
  page.goto((out/'index.html').as_uri());page.add_style_tag(content='#gain,#diagnostics,#feedback,.intro,.layout,.flow,.lower,details,footer,nav{display:none}#placement-gain{margin-top:110px;padding:35px}#placement-gain h2{font-size:32px}#placement-gain p{font-size:20px}#placement-gain a{font-size:17px}')
  page.screenshot(path=str(frames/'placement-gain.png'));manifest.append(item('placement-gain.png',10,chapter='R37 pose change and independent final connectivity proof'))
  manifest.append(item(f'{after:03}.png',10,chapter='Retained53: combined placement and routing result; warnings19',attempt=hist[after]['id'],board_sha256=hist[after]['board_sha256']))
 elif gain_path.exists():
  gain=json.loads(gain_path.read_text());before=next(i for i,r in enumerate(hist) if r.get('board_sha256')==gain['parent_board_sha256']);after=next(i for i,r in enumerate(hist) if r['id']==gain['attempt'])
  manifest.append(item(f'{before:03}.png',10,chapter='Diagnostic parent: U15 ground island outside connected planes',attempt=hist[before]['id'],board_sha256=hist[before]['board_sha256']))
  page.goto((out/'index.html').as_uri());page.add_style_tag(content='#diagnostics,#feedback,.intro,.layout,.flow,.lower,details,footer,nav{display:none}#gain{margin-top:110px;padding:35px}#gain h2{font-size:32px}#gain p{font-size:20px}#gain a{font-size:17px}')
  page.screenshot(path=str(frames/'topology-gain.png'));manifest.append(item('topology-gain.png',10,chapter='Terminal operation and independent final graph proof'))
  manifest.append(item(f'{after:03}.png',10,chapter='Retained54 after full routing and native evaluation',attempt=hist[after]['id'],board_sha256=hist[after]['board_sha256']))
 elif feedback_path.exists():
  feedback=json.loads(feedback_path.read_text())
  for attempt_id in [feedback['prior_id'],feedback['following_id']]:
   i=next(i for i,r in enumerate(hist) if r['id']==attempt_id);manifest.append(item(f'{i:03}.png',10,chapter='Measured feedback chain: rejected placement result',attempt=hist[i]['id'],board_sha256=hist[i].get('board_sha256')))
  page.goto((out/'index.html').as_uri());page.add_style_tag(content='#diagnostics,.intro,.layout,.flow,.lower,details,footer,nav{display:none}#feedback{margin-top:110px;padding:35px}#feedback h2{font-size:32px}#feedback p{font-size:20px}#feedback a{font-size:17px}')
  page.screenshot(path=str(frames/'feedback-chain.png'));manifest.append(item('feedback-chain.png',10,chapter='Persisted diagnostics inform a changed proposal; both candidates rejected'))
 else:
  for suffix in ['183642-ca8dab','185217-d06b3b','185942-295ff2']:
   i=next(i for i,r in enumerate(hist) if r['id'].endswith(suffix));manifest.append(item(f'{i:03}.png',10,chapter='Historical rejected placement experiments',attempt=hist[i]['id'],board_sha256=hist[i].get('board_sha256')))
 if (out/'topology-fixture/index.html').exists():
  page.goto((out/'topology-fixture/index.html').as_uri())
  for n in [0,1,3]:
   page.evaluate('(i)=>window.showFixture(i)',n);page.wait_for_timeout(150);page.screenshot(path=str(frames/f'fixture-{n}.png'));manifest.append(item(f'fixture-{n}.png',10,chapter='Separate bounded JITX topology fixture',fixture_index=n))
 else:
  page.goto((out/'index.html').as_uri());page.add_style_tag(content='.layout,.intro,.flow,details,footer{display:none}.lower{margin-top:100px}.lower h2{font-size:48px}.lower p{font-size:22px}.lower .panel{padding:35px}.eyebrow{font-size:15px}')
  page.screenshot(path=str(frames/'fixture-scope.png'));manifest.append(item('fixture-scope.png',30,chapter='Separate fixture scope; report-derived'))
 page.goto((out/'index.html').as_uri());page.evaluate("document.querySelector('.layout').remove();document.querySelector('.intro').remove();document.querySelector('.flow').remove();document.querySelector('#feedback').remove();document.querySelector('#diagnostics').remove();document.querySelector('#gain').remove();document.querySelector('#placement-gain').remove();document.querySelector('details').remove();document.querySelector('footer').style.fontSize='18px';document.querySelector('.lower').insertAdjacentHTML('beforebegin','<div style=\"margin:65px 0 40px\"><div class=\"eyebrow\">Inspect the chain of evidence</div><h1>One board. One evaluation. One decision.</h1><p style=\"font-size:24px\">Native board hash → rendered image → exact metrics → proposal / decision receipt</p><p style=\"font-size:20px;margin-top:25px\">The offline package preserves the evidence. Online observability links are optional.</p></div>')")
 page.screenshot(path=str(frames/'provenance.png'));manifest.append(item('provenance.png',25,chapter='Evidence and limitations'))
 manifest.append(item(f'{retained:03}.png',15,chapter='Closing: incomplete product board',attempt=hist[retained]['id'],board_sha256=hist[retained].get('board_sha256')))
 if errors: raise RuntimeError(errors)
 b.close()
assert abs(sum(x['seconds'] for x in manifest)-180)<.001
concat=frames/'concat.txt';concat.write_text(''.join(f"file '{Path(x['frame']).name}'\nduration {x['seconds']:.9f}\n" for x in manifest)+f"file '{Path(manifest[-1]['frame']).name}'\n")
subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(concat),'-vf','fps=30,format=yuv420p','-c:v','libx264','-preset','fast','-crf','21','-t','180','-movflags','+faststart',str(out/'copper-scar-demo-normal.mp4')],check=True)
subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(out/'copper-scar-demo-normal.mp4'),'-vf','setpts=PTS/5,fps=30','-an','-c:v','libx264','-preset','fast','-crf','21','-movflags','+faststart',str(out/'copper-scar-demo-5x.mp4')],check=True)
for name in ['copper-scar-demo-normal.mp4','copper-scar-demo-5x.mp4']:
 subprocess.run(['ffmpeg','-v','error','-i',str(out/name),'-f','null','-'],check=True)
 receipt=json.loads(subprocess.check_output(['ffprobe','-v','quiet','-show_streams','-show_format','-of','json',str(out/name)]));(out/(name+'.probe.json')).write_text(json.dumps(receipt,indent=2))
(out/'video-manifest.json').write_text(json.dumps(dict(method='Scripted native snapshot presentation, not elapsed solver time; full history at equal dwell within 30-second chapter. No geometry interpolation. Silent: use presenter script.',evidence_built_at=d['built_at'],normal_duration_seconds=180,speedup=5,frames=manifest,video_sha256={name:hashlib.sha256((out/name).read_bytes()).hexdigest() for name in ['copper-scar-demo-normal.mp4','copper-scar-demo-5x.mp4']}),indent=2))
print(json.dumps(dict(frames=len(manifest),browser_errors=errors,decoded=True)))
