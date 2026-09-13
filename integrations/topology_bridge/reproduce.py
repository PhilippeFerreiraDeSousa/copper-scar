"""Successive authored placement/topology candidates in one disposable runtime."""
import argparse
import copy
import json
import os
from pathlib import Path
import shutil
import subprocess
import time
from planner import propose, render, fixture_parent, digest

HERE = Path(__file__).resolve().parent
BRIDGE = HERE.parent/'placement_bridge'

def run(root, native, checker, research=False):
    root = root.resolve(); root.mkdir(parents=True, exist_ok=False)
    rt = root/'runtime'; rt.mkdir(); (rt/'bridge_fixture').mkdir()
    (rt/'bridge_fixture/__init__.py').write_text('')
    (rt/'pyproject.toml').write_text('[project]\nname="topology-proposals"\nversion="0.1.0"\nrequires-python=">=3.12"\ndependencies=["jitx==4.4.0","jitxlib-standard==4.4.0"]\n')
    base = (BRIDGE/'incremental_fixture/design.py').read_text()
    source = rt/'bridge_fixture/design.py'; logs=root/'commands';logs.mkdir(); commands=[]
    def command(args):
        started=time.monotonic()
        r=subprocess.run(list(map(str,args)),cwd=rt,env=dict(os.environ,PYTHONPATH=str(rt)),capture_output=True,text=True,timeout=360)
        i=len(commands);(logs/f'{i:02}.stdout').write_text(r.stdout);(logs/f'{i:02}.stderr').write_text(r.stderr)
        commands.append({'argv':list(map(str,args)),'elapsed_s':time.monotonic()-started,'returncode':r.returncode})
        (logs/'commands.json').write_text(json.dumps(commands,indent=2))
        if r.returncode: raise RuntimeError(f'Command {i} failed; see {logs}')
        return commands[-1]['elapsed_s']
    cli=native.parent/'jitx'; rows=[]
    command([cli,'runtime','start','--project',rt,'--bg'])
    parent=fixture_parent()
    accepted=propose(parent,{'TP4':[8,6]},offsets=(2,))[0]
    before=None; retained=None
    def realize(name,p):
        source.write_text(render(base,p)); (root/(name+'-source.py')).write_text(source.read_text())
        (root/(name+'-proposal.json')).write_text(json.dumps(p,indent=2))
        build_s=command([cli,'design','build','bridge_fixture.design.BridgeProof','--no-dependency-check'])
        plan=root/'empty.json';plan.write_text('[]');stage=root/name
        command([native,BRIDGE/'fixture_control.py',plan,stage]);command([checker,HERE/'evaluate.py',stage])
        checked=json.loads((stage/'independent/summary.json').read_text())
        pcb=next((stage/'independent').glob('*.kicad_pcb'))
        kp='/Users/philippe/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3'
        metrics=json.loads(subprocess.check_output([kp,str(HERE/'measure.py'),str(pcb)],text=True))
        checked.update(metrics)
        return checked,build_s,stage
    before,elapsed,stage=realize('00-parent',accepted)
    retained=before;retained_stage=stage
    rows.append({'stage':'00-parent','decision':'parent','opens':before['opens'],'violations':before['violations'],'wire_length_mm':before['wire_length_mm'],'build_wall_s':elapsed,'completion_timestamp':(stage/'completion.json').stat().st_mtime})
    # Explicit synthetic move requests exercise reject and two successive retained
    # placements. Real placement research may supply the same moves dictionary.
    requests=('TP4','TP6') if research else ({'TP4':[10,8]},{'TP4':[6,6]},{'TP6':[6,0]})
    for iteration,request in enumerate(requests,1):
        parent['components']=copy.deepcopy(accepted['components']);parent['topology']=copy.deepcopy(accepted['topology'])
        parent['native_parent_board_sha256']=retained['source_board_sha256']
        parent['project_sha256']=retained['project_sha256']
        if research:
            from research_adapter import moves_from_research
            config=root/f'{iteration:02}-research-config.json'
            config.write_text(json.dumps({'groups':{r:[r] for r in parent['components']},'translation_candidates_mm':[[-2,0],[2,0],[0,-2],[0,2]],'proxy_ignored_nets':[],'clearance_mm':.25,'board_edge_clearance_mm':.5},indent=2))
            proposal_path=root/f'{iteration:02}-research-proposal.json'
            native_board=next((retained_stage/'independent').glob('*.kicad_pcb'))
            command([checker,HERE/'research_proposals.py',native_board.parent,'--board-name',native_board.name,'--manifest',config,'--group',request,'--output',proposal_path])
            research_proposal=json.loads(proposal_path.read_text())
            moves=moves_from_research(research_proposal,native_board,parent['components'],retained['poses'])
            parent['placement_research_sha256']=digest(research_proposal)
        else:
            moves=request
        options=propose(parent,moves);evaluated=[]
        for index,p in enumerate(options):
            name=f'{iteration:02}-{index}-candidate'
            restored,_,_=realize(name+'-parent',accepted)
            if restored['poses']!=retained['poses'] or restored['copper_by_net']!=retained['copper_by_net'] or restored['project_sha256']!=retained['project_sha256']:
                raise RuntimeError('Common parent not preserved by authored rebuild; alternatives not comparable')
            checked,build_s,stage=realize(name,p)
            unaffected=[n for n in retained['copper_by_net'] if n not in p['affected_nets']]
            preservation=all(retained['copper_by_net'][n]==checked['copper_by_net'][n] for n in unaffected)
            moved=sorted(r for r in retained['poses'] if retained['poses'][r]!=checked['poses'][r])
            valid=checked['opens']==0 and checked['violations']==[] and preservation and moved==sorted(moves) and checked['project_sha256']==retained['project_sha256']
            row={'stage':name,'candidate_sha256':p['candidate_sha256'],'parent_sha256':p['parent_sha256'],'parent_board_sha256':retained['source_board_sha256'],'choice':p['choice'],'build_wall_s':build_s,'completion_timestamp':(stage/'completion.json').stat().st_mtime,'opens':checked['opens'],'violations':checked['violations'],'changed_refs':moved,'unaffected_copper_preserved':preservation,'via_count':checked['via_count'],'wire_length_mm':checked['wire_length_mm'],'parent_wire_length_mm':retained['wire_length_mm'],'geometry_valid':valid,'board_sha256':checked['source_board_sha256'],'project_sha256':checked['project_sha256'],'decision':'reject'}
            rows.append(row);evaluated.append((p,checked,row))
        legal=[x for x in evaluated if x[2]['geometry_valid'] and x[1]['wire_length_mm']<retained['wire_length_mm']-1e-6 and x[1]['via_count']<=retained['via_count']]
        if legal:
            accepted,retained,winner=min(legal,key=lambda x:x[1]['wire_length_mm']);winner['decision']='retain';retained_stage=root/winner['stage']
        (root/'results.json').write_text(json.dumps({'kind':'research-driven-synthetic-topology-proposals' if research else 'synthetic-topology-proposals','whole_product_board_qualified':False,'objective':'strict wire length reduction; no added vias; zero opens and violations; unchanged other nets and rules','rows':rows},indent=2))
    final,_,_=realize('99-retained',accepted)
    if final['poses']!=retained['poses'] or final['copper_by_net']!=retained['copper_by_net']:
        raise RuntimeError('Retained candidate failed final source realization')
    command([cli,'runtime','stop','--project',rt])
    return rows

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('--native-python',type=Path,required=True);p.add_argument('--checker-python',type=Path,required=True);p.add_argument('--research',action='store_true');a=p.parse_args();print(json.dumps(run(a.root,a.native_python.absolute(),a.checker_python.absolute(),a.research),indent=2))
