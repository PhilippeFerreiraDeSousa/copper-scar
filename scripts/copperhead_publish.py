"""Publish a completed checkpoint by replacing status, never overwriting boards."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,json,os,subprocess,hashlib
ap=argparse.ArgumentParser();ap.add_argument('candidate',type=Path);ap.add_argument('report');ap.add_argument('--phase',required=True);ap.add_argument('--active',default='');a=ap.parse_args()
r=Path(__file__).resolve().parents[1]/'.local/copperhead';c=a.candidate.resolve();assert c.is_relative_to(r/'candidates');b=c/'pcbgolf.kicad_pcb';report=c/a.report;d=json.loads(report.read_text());before=hashlib.sha256(b.read_bytes()).hexdigest()
k='/Users/philippe/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli'
subprocess.run([k,'pcb','export','svg','--layers','F.Cu,B.Cu,F.SilkS,Edge.Cuts','--mode-single','--page-size-mode','2','--exclude-drawing-sheet','-o',str(c/'board.svg'),str(b)],check=True,capture_output=True)
assert hashlib.sha256(b.read_bytes()).hexdigest()==before
status=dict(updated_at=datetime.now(timezone.utc).isoformat(),phase=a.phase,state='PARTIAL — NOT VALID',latest_completed_board=str(b),latest_completed_project=str(c/'pcbgolf.kicad_pro'),preview=str(c/'board.svg'),safe_to_inspect=True,actively_generating=a.active or None,last_measured_unconnected=len(d['unconnected_items']),native_drc_violations=len(d['violations']),native_schematic_parity=len(d['schematic_parity']),report=str(report),board_sha256=before,view_action='Open listed board in KiCad PCB Editor, enable ratsnest. Use Save As for edits. Reopen newer checkpoint when status changes; live reload is not verified.')
for name,content in [('current-status.json',json.dumps(status,indent=2)),('CURRENT.md',f'''# Copperhead current board: PARTIAL, NOT VALID

Updated: {status['updated_at']}

Phase: {a.phase}

[View completed board preview]({c/'board.svg'}) · [Open KiCad board]({b}) · [Project]({c/'pcbgolf.kicad_pro'})

Native result: **{len(d['unconnected_items'])} unconnected**, {len(d['violations'])} DRC findings, {len(d['schematic_parity'])} schematic-parity findings. [Raw report]({report}). This is not an accepted baseline.

Completed board is safe to inspect. Open it in **KiCad PCB Editor**, enable ratsnest, and use **Save As** for your edits. This generator will not rewrite the published board. Open the new checkpoint listed here after a status update; automatic reload is unverified.

Active generation: {a.active or 'none'}.

[Machine-readable status]({r/'current-status.json'})
''')]:
 t=r/(name+'.tmp');t.write_text(content);os.replace(t,r/name)
print(json.dumps(status,indent=2))
