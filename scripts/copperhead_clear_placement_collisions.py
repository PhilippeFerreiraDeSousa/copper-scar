"""Remove only DRC-identified track/via obstacles after a recorded group move.

Pads, footprints, zones, rules and nets are never deleted or changed. Every removed
route item and its triggering native finding is retained for independent audit.
"""
import argparse,json,subprocess
from pathlib import Path
import pcbnew as p
ap=argparse.ArgumentParser();ap.add_argument('candidate',type=Path);ap.add_argument('--max-items',type=int,default=150);a=ap.parse_args()
board=a.candidate/'pcbgolf.kicad_pcb';evidence=a.candidate/'placement-collisions';evidence.mkdir(exist_ok=False)
kicad='/Users/philippe/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli'
removed=[];phases=[]
for iteration in range(5):
 report=evidence/f'{iteration:02d}-drc.json'
 command=[kicad,'pcb','drc','--format','json','--refill-zones','-o',str(report),str(board)]
 result=subprocess.run(command,capture_output=True,text=True,timeout=90)
 (evidence/f'{iteration:02d}-command.json').write_text(json.dumps(dict(argv=command,returncode=result.returncode,stdout=result.stdout,stderr=result.stderr),indent=2))
 assert result.returncode==0 and report.exists(),'Native collision check failed'
 raw=json.loads(report.read_text());errors=[v for v in raw['violations']+raw.get('schematic_parity',[]) if v['severity']=='error'];phases.append(dict(report=str(report),errors=len(errors)))
 if not errors:break
 b=p.LoadBoard(str(board));tracks={t.m_Uuid.AsString():t for t in b.GetTracks()};causes={}
 for v in errors:
  for item in v.get('items',[]):
   if item.get('uuid') in tracks:causes.setdefault(item['uuid'],[]).append(v)
 if iteration==4 or not causes or len(removed)+len(causes)>a.max_items:break
 for uid,findings in causes.items():
  t=tracks[uid];removed.append(dict(uuid=uid,net=t.GetNetname(),kind='via' if isinstance(t,p.PCB_VIA) else 'track',start_mm=[p.ToMM(t.GetStart().x),p.ToMM(t.GetStart().y)],end_mm=[p.ToMM(t.GetEnd().x),p.ToMM(t.GetEnd().y)],native_findings=findings));b.Delete(t)
 p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(board),b)
record=dict(policy='native_reported_track_via_collisions_only',phases=phases,removed=removed,removed_count=len(removed),removed_nets=sorted({x['net'] for x in removed}),limit=a.max_items,native_errors_remaining=phases[-1]['errors'],qualification='Only tracks/vias explicitly named in native physical-error findings were removed; final independent placement gate and all-net routing remain required.')
(evidence/'result.json').write_text(json.dumps(record,indent=2))
path=a.candidate/'placement-search.json';delta=json.loads(path.read_text());delta['collision_ripup']=record;delta['reroute_nets']=sorted(set(delta['affected_nets'])|set(record['removed_nets']));path.write_text(json.dumps(delta,indent=2));print(json.dumps({k:v for k,v in record.items() if k not in ('removed','phases')},indent=2))
