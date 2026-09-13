#!/usr/bin/env python3
"""Verify every displayed board and receipt, offline chapter states and layers."""
import argparse,hashlib,json
from pathlib import Path
from playwright.sync_api import sync_playwright
from urllib.parse import urlsplit,unquote

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();out=a.out.resolve();data=json.loads((out/'data.json').read_text());hashes=[]
 for p in data['projects']:
  for s in p['states']:
   assert sha(out/s['board']['cad'])==s['board']['sha256'];hashes.append(s['board']['sha256'])
   if s.get('score'):
    score=json.loads((out/s['score_receipt']).read_text());assert score==s['score'];assert score['board_sha256']==s['board']['sha256']
    if score['valid']:
     t=score['terms'];assert abs(score['official_formula_score']-(t['pcba_bbox_volume_mm3']+50*t['via_count']+5000*t['copper_layers']))<1e-6
     assert all(score['native'][k]==0 for k in ['opens','violations','parity_findings','erc_findings']);assert score['model_coverage']['resolved_models']==score['model_coverage']['populated_components']
    else:assert score['official_formula_score'] is None
   if s.get('evaluation') and s['evaluation'].get('board_sha256'):assert s['evaluation']['board_sha256']==s['board']['sha256']
 errors=[];missing=[];checks=0
 with sync_playwright() as pw:
  b=pw.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True);c=b.new_context(offline=True,viewport={'width':1600,'height':1100});page=c.new_page();page.on('pageerror',lambda e:errors.append(str(e)));page.goto((out/'index.html').as_uri())
  for pi,p in enumerate(data['projects']):
   for i,s in enumerate(p['states']):
    page.evaluate('([p,i])=>window.demo.select(p,i)',[pi,i])
    for layer in ['Both','F.Cu','B.Cu']:
     page.locator('#layer').select_option(label=layer);page.wait_for_function('document.querySelector("#board").complete&&document.querySelector("#board").naturalWidth>0');checks+=1
    for link in page.locator('a[href]').all():
     href=link.get_attribute('href');parts=urlsplit(href)
     if not parts.scheme and not parts.netloc and not (out/unquote(parts.path)).exists():missing.append(href)
   page.locator('#layer').select_option(label='Both');page.wait_for_function('document.querySelector("#board").complete&&document.querySelector("#board").naturalWidth>0');page.screenshot(path=str(out/(p['id']+'-qa.png')),full_page=True)
  page.set_viewport_size({'width':390,'height':844});assert page.evaluate('document.documentElement.scrollWidth<=innerWidth');page.screenshot(path=str(out/'mobile-qa.png'),full_page=True);b.close()
 assert not errors,errors;assert not missing,missing
 report={'data_sha256':sha(out/'data.json'),'board_state_hash_checks':len(hashes),'offline_state_layer_checks':checks,'javascript_errors':errors,'missing_local_links':missing,'mobile_no_overflow':True};(out/'ui-verified.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
if __name__=='__main__':main()
