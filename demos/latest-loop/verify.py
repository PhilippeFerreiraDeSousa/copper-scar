#!/usr/bin/env python3
import asyncio,hashlib,json
from pathlib import Path
from playwright.async_api import async_playwright
OUT=Path('/Users/philippe/Documents/Codex/2026-09-12/realtime-voice-chat/outputs/latest-loop-experiments')
async def main():
 d=json.loads((OUT/'data.json').read_text());assert len(d['rows'])==11
 for r in d['rows']:
  assert r['budget']==600 and r['pass_limit']==100
  for s in r['states']:assert hashlib.sha256((OUT/s['board']).read_bytes()).hexdigest()==s['sha256']
 frames=OUT/'replay-frames';frames.mkdir(exist_ok=True);errors=[];external=[]
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True)
  page=await b.new_page(viewport={'width':1600,'height':1080},device_scale_factor=1)
  page.on('pageerror',lambda e:errors.append(str(e)));page.on('request',lambda r:external.append(r.url) if r.url.startswith(('http:','https:')) else None)
  await page.goto((OUT/'index.html').as_uri());await page.wait_for_function('window.LOOP && document.querySelectorAll(".card").length===3')
  for i,r in enumerate(d['rows']):
   for phase in range(3):
    await page.evaluate('([i,p])=>window.showExperiment(i,p)',[i,phase]);await page.wait_for_timeout(160)
    assert await page.locator('.card').count()==3
    await page.screenshot(path=str(frames/f'{i*3+phase:03}.png'))
   for layer in d['layers']:
    await page.select_option('#layer',layer);await page.wait_for_timeout(40)
    assert await page.locator('svg image').count()==3
   await page.select_option('#layer','F.Cu')
  await page.evaluate('window.showExperiment(0)');await page.check('#zoom');await page.screenshot(path=str(OUT/'qa-zoom.png'))
  await page.uncheck('#zoom');await page.screenshot(path=str(OUT/'qa-desktop.png'))
  await page.set_viewport_size({'width':390,'height':844});await page.screenshot(path=str(OUT/'qa-mobile.png'),full_page=True)
  assert await page.evaluate('document.documentElement.scrollWidth<=innerWidth'), 'Mobile overflow'
  assert not errors,errors;assert not external,external
  await b.close()
 result={'status':'pass','experiments':len(d['rows']),'board_hash_joins':len(d['rows'])*3,'layers_checked':7,'replay_frames':len(d['rows'])*3,'mobile_no_overflow':True,'javascript_errors':errors,'external_requests':external}
 (OUT/'QA.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
asyncio.run(main())
