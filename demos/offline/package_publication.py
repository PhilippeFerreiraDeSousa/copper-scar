#!/usr/bin/env python3
"""Bind separately refilled publication CAD and STEP to immutable historical evidence."""
import argparse,hashlib,json,subprocess
from pathlib import Path

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def verify(root):
 p=read(root/'publication/summary.json');board=root/p['board'];assert sha(board)==p['board_sha256']
 original=next(r for r in read(root/'data.json')['history'] if r['id']==p['attempt']);assert original['board_sha256']==p['source_board_sha256']
 evaluation=read(root/original['evaluation']);assert sha(root/'publication/pcbgolf.kicad_pro')==evaluation['files']['pcbgolf.kicad_pro']
 for rel in read(root/'publication/library-resolution.json')['files']:assert sha(root/'publication'/rel)==evaluation['files'][rel]
 preservation=read(root/'publication/refill-preservation.json');assert preservation['source_board_sha256']==p['source_board_sha256'] and preservation['published_board_sha256']==p['board_sha256'] and preservation['all_authored_subtrees_preserved']
 report=read(root/p['drc']);assert [len(report['unconnected_items']),sum(v['severity']=='error' for v in report['violations']),sum(v['severity']=='warning' for v in report['violations'])]==[45,0,18]
 image=read(root/'publication/render-receipt.json');assert image['board_sha256']==p['board_sha256'] and image['image_sha256']==sha(root/p['image'])
 coverage=read(root/'assembly/model-coverage.json');geometry=read(root/'assembly/step-geometry-check.json');assert coverage['board_sha256']==p['board_sha256'] and coverage['summary']['populated_with_resolved_original_model']==238
 assert geometry['step_sha256']==sha(root/p['step']) and geometry['component_names_exact_match'] and geometry['whole_shape_valid'] and geometry['invalid_solids']==0
 assert sha(root/'assembly/input/pcbgolf.kicad_pcb')==p['board_sha256']
 for rel,h in read(root/'assembly/input-hashes.json').items():assert sha(root/'assembly/input'/rel)==h
 return p

def build(root,cli):
 pub=root/'publication';preservation=read(pub/'refill-preservation.json');r=next(r for r in read(root/'data.json')['history'] if r['board_sha256']==preservation['source_board_sha256'])
 cmd=[str(cli),'pcb','export','svg','--layers','F.Cu,B.Cu,F.SilkS,Edge.Cuts','--mode-single','--page-size-mode','2','--exclude-drawing-sheet','-o',str(pub/'board.svg'),str(pub/'pcbgolf.kicad_pcb')];subprocess.run(cmd,check=True,capture_output=True)
 (pub/'render-receipt.json').write_text(json.dumps({'board_sha256':sha(pub/'pcbgolf.kicad_pcb'),'image_sha256':sha(pub/'board.svg'),'argv':cmd},indent=2)+'\n')
 p=dict(attempt=r['id'],source_board_sha256=preservation['source_board_sha256'],board_sha256=sha(pub/'pcbgolf.kicad_pcb'),board='publication/pcbgolf.kicad_pcb',drc='publication/saved-recheck-drc.json',image='publication/board.svg',step='assembly/accepted45-recorded-population-unqualified.step',metrics=[45,0,18],transformation='KiCad10.0.6 refill/save of generated zone fill; all authored CAD subtrees and project bytes preserved',qualification='Historical source had stale fills. This separately hashed saved-file publication rechecks45/0/18 without refilling. Product remains incomplete and unqualified.')
 (pub/'summary.json').write_text(json.dumps(p,indent=2)+'\n');verify(root);(root/'publication-data.js').write_text('window.PUBLICATION='+json.dumps(p)+';\n')
 (pub/'README.md').write_text(f"# Refilled publication CAD — still incomplete\n\nHistorical source `{p['source_board_sha256']}` remains in evidence/ and its original receipt. Its stale stored zone fills produced8clearance errors; independent unsaved refill produced45/0/18.\n\nThis private publication copy was refilled and saved as `{p['board_sha256']}`. Fresh saved-file DRC, without another refill, reports45opens/0errors/18warnings. Exact tokenized authored root subtrees are preserved, excluding only generated zone filled_polygon/fill_segments; footprints, tracks, vias, outlines and rules are unchanged. Project bytes are unchanged.\n\nThe candidate's exact footprint library is copied by the after.files hashes. The original PCBGolf library initially produced extra mismatches; that intermediate report is retained and no footprint library was authored or warning suppressed. The publication and assembly use the frozen candidate library and original supplied models.\n\n[Saved board](pcbgolf.kicad_pcb), [fresh DRC](saved-recheck-drc.json), [refill preservation](refill-preservation.json), [commands](refill-commands.json), [library resolution](library-resolution.json), [assembly](../assembly/README.md). This is a derived publication artifact, not another optimization attempt, a new W&B result, or a qualified product.\n")
 print(json.dumps(p))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('package',type=Path);p.add_argument('--kicad',type=Path,required=True);a=p.parse_args();build(a.package,a.kicad)
