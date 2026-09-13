"""Start one owned native editor; require guarded UI switch for later checkpoints.

Never kills/reloads another editor or overwrites checkpoint files. The controller
uses CUA File/Open after checking this owned window and any unsaved-edit dialog.
"""
from pathlib import Path
import json,os,subprocess
r=Path(__file__).resolve().parents[1]/'.local/copperhead';s=json.loads((r/'current-status.json').read_text());v=r/'viewer-state.json';b=Path(s['latest_completed_board']);assert b.is_relative_to(r/'candidates') and b.exists()
old=json.loads(v.read_text()) if v.exists() else {}
if old.get('pid'):
 try:os.kill(old['pid'],0)
 except ProcessLookupError:pass
 else:
  print(json.dumps(dict(action='guarded_ui_open_required',pid=old['pid'],last_opened=old.get('board'),next_board=str(b),policy='Use CUA to verify owned window, File/Open next board, cancel any unsaved-edit prompt. Never kill/reload automatically.')));raise SystemExit(0)
exe='/Users/philippe/Applications/KiCad/KiCad.app/Contents/Applications/pcbnew.app/Contents/MacOS/pcbnew'
with (r/'viewer.log').open('a') as log:p=subprocess.Popen([exe,str(b)],stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
record=dict(pid=p.pid,board=str(b),graphically_verified=False,update_mode='CUA guarded File/Open; automatic unattended reload not supported')
v.write_text(json.dumps(record,indent=2));print(json.dumps(record))
