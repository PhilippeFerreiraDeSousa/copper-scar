#!/usr/bin/env python3
"""Verify exact source joins and locally rendered offline checkpoints."""
import argparse,hashlib,json
from pathlib import Path
from playwright.sync_api import sync_playwright

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();out=a.output;d=json.loads((out/'data.json').read_text());assert not d['fixture'];checks=0
 for p in d['policies']:
  completed=[x for x in p['points'] if x['index'] and x['completed']]
  assert p['cost_at_n'] is None or len(completed)==d['attempt_budget']
  for x in p['points']:
   for stage in x['stages']+([x['incumbent']] if x.get('incumbent') else []):
    if stage.get('board'):assert hashlib.sha256((out/stage['board']).read_bytes()).hexdigest()==stage['sha256'];checks+=1
   if x.get('receipt_href'):assert hashlib.sha256((out/x['receipt_href']).read_bytes()).hexdigest()==x['receipt_sha256'];checks+=1
   if x.get('retained') is False and x.get('attempted',{}).get('pad_groups_preserved') is False:assert x['best']['pad_groups_preserved'] is True
 with sync_playwright() as pw:
  browser=pw.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True);context=browser.new_context(offline=True,viewport={'width':1440,'height':1100});page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.goto((out/'index.html').as_uri());page.uncheck('#live')
  for p in d['policies']:
   for x in p['points']:
    page.evaluate('([p,i])=>selectCheckpoint(p,i)',[p['id'],x['index']]);page.wait_for_function('Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0)');checks+=1
    for layer in ['F.Cu','In1.Cu','In2.Cu','In3.Cu','In4.Cu','B.Cu']:
     page.select_option('#layer',layer);page.wait_for_function('Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0)');checks+=1
    for element in page.locator('a[href]').all():
     href=element.get_attribute('href')
     if not href.startswith(('http:','https:','#')):assert (out/href.split('?')[0]).exists(),href
  page.select_option('#layer','In4.Cu')
  page.click('#replay');assert page.evaluate('window.EXPERIMENT.policies.every(p=>p.cost_at_n===null)'), 'Replay leaks future cost at N'
  page.click('#replay')
  page.screenshot(path=str(out/'qa-desktop.png'),full_page=True);page.set_viewport_size({'width':390,'height':844});page.screenshot(path=str(out/'qa-mobile.png'),full_page=True);assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'), 'Mobile overflow';assert not errors,errors;browser.close()
 result={'event_count':d['event_count'],'events_sha256':d['events_sha256'],'checks':checks,'offline_browser':True,'javascript_errors':errors,'mobile_no_overflow':True};(out/'ui-verified.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
if __name__=='__main__':main()
