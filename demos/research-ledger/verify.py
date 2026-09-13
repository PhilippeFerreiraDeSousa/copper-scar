#!/usr/bin/env python3
import asyncio,hashlib,json
from pathlib import Path
from playwright.async_api import async_playwright
OUT=Path('/Users/philippe/Documents/Codex/2026-09-12/realtime-voice-chat/outputs/optimizer-research-ledger')
async def main():
 d=json.loads((OUT/'ledger.json').read_text());assert len(d['rows'])==10
 paths=set()
 for r in d['rows']:
  assert not r['matched_performance_comparison'] and not r['trained_model_update']
  for e in r['inputs']+r['artifacts']:
   p=(OUT/e['href']).resolve();assert p==Path(e['path']);assert hashlib.sha256(p.read_bytes()).hexdigest()==e['sha256'];paths.add(str(p))
  for s in r['implementation']['source_hashes']:assert hashlib.sha256((OUT/s['snapshot_href']).read_bytes()).hexdigest()==s['sha256']
 errors=[];external=[]
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True)
  page=await browser.new_page(viewport={'width':1440,'height':1000});page.on('pageerror',lambda e:errors.append(str(e)));page.on('request',lambda r:external.append(r.url) if r.url.startswith(('https:','http:')) else None)
  await page.goto((OUT/'index.html').as_uri());assert await page.locator('#list button').count()==10
  for r in d['rows']:
   await page.evaluate('(id)=>window.showResearch(id)',r['id']);assert await page.locator('#detail h2').inner_text()==r['title'];assert await page.locator('#detail').get_by_text(r['result'],exact=True).count()==1
  await page.evaluate("window.showResearch('dsn-contacts')");await page.screenshot(path=str(OUT/'qa-desktop.png'))
  await page.select_option('#filter','Full-route observation');assert await page.locator('#list button').count()==2
  await page.fill('#search','NO_SUCH_RESEARCH');assert await page.locator('#list button').count()==0
  await page.evaluate("window.showResearch('placement-coverage')");await page.set_viewport_size({'width':390,'height':844});assert await page.evaluate('document.documentElement.scrollWidth<=innerWidth');await page.screenshot(path=str(OUT/'qa-mobile.png'),full_page=True)
  assert not errors and not external,(errors,external);await browser.close()
 result={'status':'pass','records':10,'unique_linked_artifacts_verified':len(paths),'source_snapshot_hashes':'pass','all_record_views':'pass','filter_and_search':'pass','mobile_overflow':False,'javascript_errors':errors,'external_requests':external};(OUT/'QA.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
asyncio.run(main())
