#!/usr/bin/env python3
"""Verify a portable ZIP and its extracted local HTML without network access."""
import argparse,hashlib,json,subprocess,zipfile
from pathlib import Path
from urllib.parse import unquote,urlsplit
from playwright.sync_api import sync_playwright

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--zip',type=Path,required=True);ap.add_argument('--extract',type=Path,required=True);a=ap.parse_args();root=a.extract.resolve();root.mkdir(parents=True,exist_ok=True)
 with zipfile.ZipFile(a.zip) as z:
  manifest=json.loads(z.read('package-manifest.json'))
  for name,expected in manifest['files'].items():assert hashlib.sha256(z.read(name)).hexdigest()==expected,name
  for name in z.namelist():assert (root/name).resolve().is_relative_to(root)
  z.extractall(root)
 checks=[];errors=[];missing=[]
 with sync_playwright() as pw:
  browser=pw.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True);context=browser.new_context(offline=True,viewport={'width':1440,'height':1100});page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
  for relative in ['index.html','two-level-autoresearch/index.html','latest-loop-experiments/index.html','optimizer-research-ledger/index.html']:
   path=root/relative;page.goto(path.as_uri());page.wait_for_function('Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0)');assert '${' not in page.locator('body').inner_text(),'Unexpanded template in '+relative
   for element in page.locator('a[href],script[src],img[src]').all():
    href=element.get_attribute('href') or element.get_attribute('src');parts=urlsplit(href)
    if parts.scheme or parts.netloc or href.startswith('#'):continue
    if not (path.parent/unquote(parts.path)).exists():missing.append(relative+': '+href)
   checks.append(relative);page.screenshot(path=str(root/(relative.split('/')[0]+'-qa.png')),full_page=True)
  browser.close()
 assert not errors,errors;assert not missing,missing
 subprocess.run(['ffmpeg','-v','error','-i',str(root/'two-level-autoresearch/two-level-replay.mp4'),'-f','null','-'],check=True)
 result={'zip':str(a.zip),'zip_sha256':hashlib.sha256(a.zip.read_bytes()).hexdigest(),'extracted':str(root),'archive_files_verified':len(manifest['files']),'offline_pages_verified':checks,'javascript_errors':errors,'missing_local_resources':missing,'video_full_decode':True,'events_sha256':manifest['events_sha256'],'demo_source_revision':manifest['demo_source_revision']};a.zip.with_suffix('.offline-verified.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
if __name__=='__main__':main()
