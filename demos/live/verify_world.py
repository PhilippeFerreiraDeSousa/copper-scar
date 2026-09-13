#!/usr/bin/env python3
"""Check native absolute export, invariant anchor pixels and shared SVG frames."""
import argparse,json,re,sys,xml.etree.ElementTree as ET
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'autoresearch'))
from cad import inventory,parse,nodes,one
from playwright.sync_api import sync_playwright

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();out=a.out;data=json.loads((out/'data.json').read_text());ns={'s':'http://www.w3.org/2000/svg'};count=0
 for p in data['projects']:
  expected=' '.join(map(str,p['world_frame']['viewBox']))
  for s in p['states']+p['history_states']:
   for rel in s['board']['images'].values():
    root=ET.parse(out/rel).getroot();assert root.attrib['viewBox']==expected;assert root.attrib['width']==str(p['world_frame']['viewBox'][2])+'mm';assert root.attrib['height']==str(p['world_frame']['viewBox'][3])+'mm';assert root.attrib['preserveAspectRatio']=='xMidYMid meet';count+=1
 m=next(p for p in data['projects'] if p['id']=='medium');before=next(s for s in m['states'] if s['title']=='baseline-parity · evaluated');after=next(s for s in m['states'] if s['title']=='relay-group-01 · evaluated');pa=inventory(out/before['board']['cad'])[0];pb=inventory(out/after['board']['cad'])[0];same=[r for r in pa if pa[r]==pb[r]][:3];moved=next(r for r in pa if pa[r]!=pb[r]);assert len(same)==3
 # Verify the first native exported copper pad against its exact CAD pad coordinates.
 board=parse(out/before['board']['cad']);fp=nodes(board,'footprint')[0];at=one(fp,'at');pad=nodes(fp,'pad')[0];padat=one(pad,'at');assert len(at)<3 or float(at[2])==0
 expectedpad=[float(at[i])+float(padat[i]) for i in range(2)];raw=(out/before['board']['cad']).parent/'Both-absolute.svg';d=re.search(r'<path[^>]*\bd="([^"]+)"',raw.read_text(),re.S).group(1);coords=[float(v) for v in re.findall(r'-?\d+\.\d+',d)];actualpad=[(min(coords[i::2])+max(coords[i::2]))/2 for i in range(2)];assert max(abs(x-y) for x,y in zip(expectedpad,actualpad))<1e-4,(expectedpad,actualpad)
 with sync_playwright() as pw:
  browser=pw.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True);page=browser.new_page(viewport={'width':900,'height':650});pixels=[];matrices=[]
  for s in [before,after]:
   text=(out/s['board']['images']['Both']).read_text();text=text[text.index('<svg'):];text=re.sub(r'width="[^"]+" height="[^"]+"','width="800" height="560"',text,count=1);page.set_content('<style>body{margin:0;background:#091320}</style>'+text);measure=page.evaluate('''() => {let svg=document.querySelector('svg'),m=svg.getScreenCTM(),points={};document.querySelectorAll('[data-anchor]').forEach(el=>{let p=new DOMPoint(+el.getAttribute('cx'),+el.getAttribute('cy')).matrixTransform(m);points[el.dataset.anchor]=[p.x,p.y]});return {points,matrix:[m.a,m.b,m.c,m.d,m.e,m.f]}}''');pixels.append(measure['points']);matrices.append(measure['matrix']);page.screenshot(path=str(out/('world-before.png' if s is before else 'world-after.png')))
  assert matrices[0]==matrices[1]
  for ref in same:assert pixels[0][ref]==pixels[1][ref],ref
  dx=pb[moved][0]-pa[moved][0];dy=pb[moved][1]-pa[moved][1];actual=[pixels[1][moved][i]-pixels[0][moved][i] for i in range(2)];expected=[dx*matrices[0][0],dy*matrices[0][3]];assert max(abs(x-y) for x,y in zip(actual,expected))<1e-6
  page.goto('http://127.0.0.1:53927/noon-live/index.html#medium/functional-probe-01');page.set_viewport_size({'width':390,'height':844});assert page.evaluate('document.documentElement.scrollWidth<=innerWidth');browser.close()
 edge=next(s for s in m['states'] if s.get('score') and 'edge-x-01' in s.get('proposal_context',{}).get('folder',''));parent=next(s for s in m['states'] if s['board']['sha256']==edge['action']['parent_board_sha256']);ep=inventory(out/edge['board']['cad'])[0];pp=inventory(out/parent['board']['cad'])[0];assert ep==pp
 result={'outline_only_unchanged_components':len(ep),'outline_before_mm':parent['board']['size_mm'],'outline_after_mm':edge['board']['size_mm'],'svg_frames_checked':count,'unchanged_anchors':{r:{'before_pixel':pixels[0][r],'after_pixel':pixels[1][r]} for r in same},'moved_anchor':{'reference':moved,'world_delta_mm':[dx,dy],'pixel_delta':actual,'expected_pixel_delta':expected},'native_first_pad':{'expected_absolute_mm':expectedpad,'exported_absolute_mm':actualpad},'identical_matrix':matrices[0],'families':{p['id']:p['world_frame'] for p in data['projects']}};(out/'world-frame-verified.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
if __name__=='__main__':main()
