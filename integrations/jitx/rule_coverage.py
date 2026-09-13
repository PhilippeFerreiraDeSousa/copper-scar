"""Inventory every source rule; equivalence is unproven until differential testing."""
from import_experiments import *
import ast,collections
p=json.loads((SRC/'pcbgolf.kicad_pro').read_text());board=p['board']['design_settings'];native={}
for n in ast.walk(ast.parse((BASE/'pcbgolf_import/board.py').read_text())):
 if isinstance(n,ast.ClassDef) and n.name=='DesignRules':
  for a in n.body:
   if isinstance(a,ast.Assign):native[a.targets[0].id]=ast.literal_eval(a.value)
mapping={'min_clearance':'min_copper_copper_space','min_track_width':'min_copper_width','min_copper_edge_clearance':'min_copper_edge_space','min_hole_clearance':'min_copper_hole_space','min_hole_to_hole':'min_hole_to_hole','min_via_annular_width':'min_annular_ring','min_through_hole_diameter':'min_drill_diameter','min_text_height':'min_silkscreen_text_height'}
rows=[]
for k,v in board['rules'].items():
 n=mapping.get(k);rows.append({'category':'physical_minimum','rule':k,'source':v,'native_field':n,'native_value':native.get(n),'status':'translatable-not-equivalence-tested' if n else 'external-only-unproven','enforcement':'KiCad original project; native generation supplemental'})
for k,v in board['rule_severities'].items():rows.append({'category':'drc_severity','rule':k,'source':v,'status':'external-only','enforcement':'KiCad original project; no proven native severity translation'})
for k,v in p['erc']['rule_severities'].items():rows.append({'category':'erc_severity','rule':k,'source':v,'status':'external-only','enforcement':'KiCad all six hierarchy sheets; original ignore settings retained'})
for c in p['net_settings']['classes']:
 for k,v in c.items():rows.append({'category':'netclass:'+c['name'],'rule':k,'source':v,'status':'translatable-not-equivalence-tested' if k=='clearance' else 'external-only-unproven','enforcement':'Original KiCad netclass; native global clearance strengthened to .2 mm'})
rows.extend([
 {'category':'erc','rule':'pin_map','source':p['erc']['pin_map'],'status':'missing-native','enforcement':'KiCad only; generated Port() does not retain KiCad electrical pin types'},
 {'category':'keepout','rule':'PJ-002AH pad exclusion','source':'tracks/vias/pads/pour prohibited; footprints allowed','status':'partial-native','enforcement':'Native route/pour/via flags corrected; native KeepOut lacks pad prohibition; source geometry audit required'},
 {'category':'custom_rules','rule':'.dru','source':list(str(x) for x in SRC.glob('*.dru')),'status':'source-absent','enforcement':'No source custom rule file; do not infer no engineering constraints'},
 *[{'category':'challenge','rule':k,'source':'PCBGolf README','status':'external-only','enforcement':'Evidence-backed independent qualification, missing evidence prevents validity'} for k in ['JLCPCB manufacturing','assembly feasibility','electrical functionality','mating connector compatibility','assembly volume/models']]])
out=BASE/'runs/stage1';out.mkdir(exist_ok=True)
(out/'rule-coverage.json').write_text(json.dumps({'source_project_sha256':hashes(SRC)['pcbgolf.kicad_pro'],'original_board':board,'original_erc':p['erc'],'original_net_settings':p['net_settings'],'current_native_rules':native,'matrix':rows},indent=2))
lines=['# Original-rule coverage inventory','','All faithful-native claims remain unproven. KiCad is authoritative for supported original DRC/ERC checks; independent engineering gates remain required.','','| Category | Rule | Source | Native status |','|---|---|---|---|']
for r in rows:lines.append('| '+r['category']+' | '+r['rule']+' | '+str(r['source']).replace('|','/').replace('\n',' ')+' | '+r['status']+' |')
Path('docs/jitx-rule-coverage.md').write_text('\n'.join(lines)+'\n');print(len(rows),'rules recorded')
