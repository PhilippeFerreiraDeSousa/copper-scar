"""Audit hierarchy conversion and native schematic/board pin partitions."""
from pathlib import Path
import argparse,collections,json,xml.etree.ElementTree as E
import sexpdata as sx

def ns(n,k):return [v for v in n if isinstance(v,list) and v and str(v[0])==k]
def walk(n):
 if isinstance(n,list):
  yield n
  for v in n:yield from walk(v)
ap=argparse.ArgumentParser();ap.add_argument('source',type=Path);ap.add_argument('candidate',type=Path);a=ap.parse_args();c=a.candidate
m=json.loads((c/'hierarchy-conversion.json').read_text());preserved=[]
for r in m['sheets']:
 orig=sx.loads((a.source/r['source']).read_text());child=sx.loads((c/r['child']).read_text())
 for n in walk(child):
  if len(n)>1 and str(n[0])=='path' and n[1]==r['new_instance_path']:n[1]='/'+r['old_instance_root']
 preserved.append(dict(sheet=r['source'],equivalent=orig==child))
x=E.parse(c/'reference.net.xml');schem={frozenset((n.attrib['ref'],n.attrib['pin']) for n in net.findall('node')):net.attrib['name'] for net in x.findall('./nets/net')}
b=sx.loads((c/'pcbgolf.kicad_pcb').read_text());bn=collections.defaultdict(set);physical={}
for f in ns(b,'footprint'):
 ref=next(n[2] for n in ns(f,'property') if n[1]=='Reference')
 for pad in ns(f,'pad'):
  physical[str(ns(pad,'uuid')[0][1])]=(ref,str(pad[1]))
  for net in ns(pad,'net'):bn[str(net[-1])].add((ref,str(pad[1])))
board={frozenset(pins):name for name,pins in bn.items()}
origboard=sx.loads((a.source/'pcbgolf.kicad_pcb').read_text());origphysical={}
for f in ns(origboard,'footprint'):
 ref=next(n[2] for n in ns(f,'property') if n[1]=='Reference')
 for pad in ns(f,'pad'):origphysical[str(ns(pad,'uuid')[0][1])]=(ref,str(pad[1]))
project=json.loads((c/'pcbgolf.kicad_pro').read_text());origpro=json.loads((a.source/'pcbgolf.kicad_pro').read_text())
erc=json.loads((c/'erc.json').read_text());expected={'/'+m['root']}|{v['new_instance_path'] for v in m['sheets']};seen={v['uuid_path'] for v in erc['sheets']}
r=dict(sheet_ast_preservation=preserved,whole_project_erc_coverage=expected==seen,erc_violations=sum(len(v['violations']) for v in erc['sheets']),erc_ignored_checks=erc.get('ignored_checks',[]),board_partition_count=len(board),schematic_partition_count=len(schem),pin_partition_equivalent=board.keys()==schem.keys(),all_physical_pad_uuid_identity_preserved=physical==origphysical,physical_pad_count=len(physical),original_board_rules_preserved=project['board']['design_settings']==origpro['board']['design_settings'],original_netclasses_preserved=project['net_settings']==origpro['net_settings'],net_name_encoding_differences=[dict(board=board[k],schematic=schem[k]) for k in board.keys()&schem.keys() if board[k]!=schem[k]],board_only_partitions=[sorted(v) for v in board.keys()-schem.keys()],schematic_only_partitions=[sorted(v) for v in schem.keys()-board.keys()])
(c/'reference-check.json').write_text(json.dumps(r,indent=2));print(json.dumps({k:v for k,v in r.items() if k!='erc_ignored_checks'},indent=2))
assert all(v['equivalent'] for v in preserved) and r['whole_project_erc_coverage'] and r['pin_partition_equivalent'] and r['all_physical_pad_uuid_identity_preserved'] and r['original_board_rules_preserved'] and r['original_netclasses_preserved']
