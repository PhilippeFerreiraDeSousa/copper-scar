#!/usr/bin/env python3
import argparse,json
from pathlib import Path
from playwright.sync_api import sync_playwright

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);out=ap.parse_args().out
 with sync_playwright() as pw:
  b=pw.chromium.launch(headless=True,executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome');page=b.new_page(viewport={'width':1500,'height':1200});errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.goto('http://127.0.0.1:53927/noon-live/index.html?verified=1#medium/functional-probe-01');data=page.evaluate('DATA');m=data['projects'][1];panels={}
  for label,folder in [('scaling','edge-space-v1'),('functional','functional-probe-01'),('rejected','primitive-axes-01'),('outline-only','edge-x-01'),('preflight','y-contract-01'),('ground-escape','ground-escape-02')]:
   matches=[i for i,s in enumerate(m['states']) if s.get('score') and folder in s.get('proposal_context',{}).get('folder','')];i=matches[-1] if label=='rejected' else matches[0];page.evaluate(f'window.demo.select(1,{i})');panels[label]={k:page.locator('#'+k).text_content() for k in ['action','why','result','proposer','geometry']};page.screenshot(path=str(out/(label+'-clarity.png')))
  assert 'Rejected before routing' in panels['preflight']['result'];assert '0.1250 mm' in panels['preflight']['result'];assert 'through-via at Q7.2' in panels['ground-escape']['action']
  assert '148→29' in panels['functional']['result'];assert 'Rejected' in panels['rejected']['result'];assert 'programmatic' in panels['functional']['proposer'];assert 'positions stayed unchanged' in panels['outline-only']['action'];assert '26→25' in panels['outline-only']['result']
  evaluated=[i for i,s in enumerate(m['states']) if s.get('score')];page.evaluate(f'window.demo.select(1,{evaluated[1]})');old=page.locator('[data-point]').evaluate_all('(els)=>els.map(e=>({i:e.dataset.point,x:e.dataset.x,y:e.dataset.y}))');rect1=page.locator('#board').bounding_box();page.evaluate(f'window.demo.select(1,{evaluated[-1]})');new=page.locator('[data-point]').evaluate_all('(els)=>els.map(e=>({i:e.dataset.point,x:e.dataset.x,y:e.dataset.y}))');rect2=page.locator('#board').bounding_box();assert old==new[:len(old)],(old,new);assert rect1==rect2,(rect1,rect2);assert page.locator('[data-status="accepted"] circle').count()>0;assert page.locator('[data-status="rejected"] path').count()>0;assert page.locator('[data-value="null"]').count()>0
  assert page.locator('#speed option').all_text_contents()==['2×','5×','10×'];assert page.locator('#speed').input_value()=='5';page.select_option('#speed','2');page.evaluate('window.intervalChecks=[];const oldSetInterval=window.setInterval;window.setInterval=(fn,ms)=>{window.intervalChecks.push(ms);return oldSetInterval(fn,ms)}');page.locator('#play').click();assert page.evaluate('window.intervalChecks.at(-1)')==1500;page.wait_for_timeout(1900);page.locator('#play').click();assert page.locator('#board').bounding_box()==rect1
  page.set_viewport_size({'width':390,'height':844});assert page.evaluate('document.documentElement.scrollWidth<=innerWidth');assert not errors,errors;b.close()
 result={'panels':panels,'fixed_chart_points':old,'fixed_board_rect':rect1,'accepted_circle':True,'rejected_cross':True,'invalid_null_rail':True,'browser_errors':errors};(out/'clarity-verified.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
if __name__=='__main__':main()
