#!/usr/bin/env python3
"""Exercise the offline replay without foreground UI or external requests."""
import argparse,json
from pathlib import Path
from playwright.sync_api import sync_playwright
p=argparse.ArgumentParser();p.add_argument('package',type=Path);p.add_argument('--browser',default='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome');a=p.parse_args();out=a.package.resolve();data=json.loads((out/'data.json').read_text());errors=[];external=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=a.browser,headless=True)
 page=b.new_page(viewport={'width':1440,'height':1100});page.on('pageerror',lambda e:errors.append(str(e)));page.on('request',lambda r:external.append(r.url) if r.url.startswith('http') else None)
 page.goto((out/'index.html').as_uri());page.wait_for_function('document.querySelector("#board").complete');page.screenshot(path=str(out/'initial-dashboard.png'),full_page=True)
 retained=[r for r in data['history'] if r.get('retained') and r.get('image') and not r.get('failed')]
 if retained: assert page.locator('#opens').inner_text()==str(retained[-1]['opens'])
 for i,r in enumerate(data['history']):
  page.evaluate('(i)=>showAttempt(i)',i);page.wait_for_function('document.querySelector("#board").hidden || (document.querySelector("#board").complete && document.querySelector("#board").naturalWidth>0)')
  assert page.locator('#opens').inner_text()==str(r.get('opens','—'))
 page.locator('#play').click();assert page.locator('#slider').input_value()=='0';page.locator('#play').click()
 page.set_viewport_size({'width':390,'height':844});page.screenshot(path=str(out/'mobile-dashboard.png'),full_page=True)
 assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), 'Mobile horizontal overflow'
 page.set_viewport_size({'width':1920,'height':1080});page.goto((out/'topology-fixture/index.html').as_uri())
 for i in range(5): page.evaluate('(i)=>showFixture(i)',i)
 assert not errors,errors;assert not external,external;b.close()
report=dict(status='pass',images_checked=len(data['history']),fixture_states_checked=5,javascript_errors=errors,external_requests=external,play_from_start=True,desktop_viewport=[1440,1100],mobile_viewport=[390,844])
(out/'browser-QA.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
