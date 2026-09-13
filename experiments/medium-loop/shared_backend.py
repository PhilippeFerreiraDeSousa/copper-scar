"""Medium native adapter for the shared candidate executor; no family rules inferred."""
from pathlib import Path
import json,re,shutil,sys,threading,time
import sexpdata as sx
from campaign import ROOT,KICAD,KIPY,command,write
from audit import audit,nodes,first
from stage2 import score,assembly_clearance

def evaluate(request,folder,emit):
    template=Path(request['project_template']);source=Path(request['original_reference']);manifest=Path(request['manifest']);commands=[]
    for name in ['pcbgolf.kicad_pro','pcbgolf.kicad_sch','pcbgolf.kicad_sym','fp-lib-table','sym-lib-table']:
        shutil.copy2(template/name,folder/name)
    for name in ['pcbgolf.pretty','pcbgolf.3dshapes','models']:
        shutil.copytree(template/name,folder/name)
    board=sx.loads(Path(request['proposal_board']).read_text());board[:]=[v for v in board if not(isinstance(v,list) and v and str(v[0]) in ['segment','via','arc','zone'])];(folder/'pcbgolf.kicad_pcb').write_text(sx.dumps(board));project=(folder/'pcbgolf.kicad_pro').read_bytes()
    def run(argv,label):
        stop=threading.Event();tick=time.monotonic()
        def pulse():
            while not stop.is_set():emit(label,operation_elapsed_seconds=time.monotonic()-tick);stop.wait(2)
        thread=threading.Thread(target=pulse,daemon=True);thread.start()
        try:commands.append(command(argv,folder,label))
        finally:stop.set();thread.join()
    def native(action):
        run([KIPY,ROOT/'experiments/medium-loop/native_stage.py',action,folder],action)
        current=(folder/'pcbgolf.kicad_pro').read_bytes()
        if current!=project:(folder/(action+'-producer-project.json')).write_bytes(current)
        (folder/'pcbgolf.kicad_pro').write_bytes(project)
    native('export');dsn=sx.loads((folder/'pcbgolf.dsn').read_text());structure=first(dsn,'structure');dsn_layers=[str(v[1]) for v in nodes(structure,'layer')];via_names=[str(v) for v in first(structure,'via')[1:]];via_sizes=[list(map(lambda x:float(x)/1000,re.search(r'_(\d+):(\d+)_um$',v).groups())) for v in via_names];scope={'layers':dsn_layers,'via_options':via_sizes,'passed':dsn_layers==request['eligible_layers'] and sorted(via_sizes)==sorted(request['via_options'])};write(folder/'dsn-scope.json',scope);shutil.copy2(folder/'pcbgolf.kicad_pcb',folder/'preview.kicad_pcb');run([KICAD,'pcb','drc','--schematic-parity','--format','json','-o',folder/'preflight.json',folder/'pcbgolf.kicad_pcb'],'preflight');pre=json.loads((folder/'preflight.json').read_text());physical=assembly_clearance(folder);write(folder/'preflight-assembly.json',physical);legal=scope['passed'] and not pre['violations'] and not pre.get('schematic_parity',[{}]) and physical['ok']
    if legal:
        budget=request['route_budget'];run([sys.executable,ROOT/'scripts/copperhead_route.py',folder,'--seconds',str(budget['seconds']),'--passes',str(budget['passes']),'--whole-board','--skip-fanout'],'full-route');native('import')
    native('audit');run([KIPY,ROOT/'experiments/pcb-loop/native_geometry.py',source/'pcbgolf.kicad_pcb',folder/'pcbgolf.kicad_pcb',manifest,folder/'all-pad-geometry.json'],'all-pad-geometry');run([KICAD,'pcb','drc','--schematic-parity','--format','json','-o',folder/'drc.json',folder/'pcbgolf.kicad_pcb'],'drc');run([KICAD,'sch','erc','--format','json','-o',folder/'erc.json',folder/'pcbgolf.kicad_sch'],'erc');accepted=audit(folder,manifest,source);run([KICAD,'pcb','export','step','-f','-o',folder/'assembly.step',folder/'pcbgolf.kicad_pcb'],'step-export');result=score(folder)
    run([KICAD,'pcb','export','svg','--layers',','.join(request['eligible_layers'])+',F.SilkS,Edge.Cuts','--mode-single','--page-size-mode','2','--exclude-drawing-sheet','-o',folder/'board.svg',folder/'pcbgolf.kicad_pcb'],'render');run(['/opt/homebrew/bin/rsvg-convert','-w','1400','-o',folder/'board.png',folder/'board.svg'],'raster')
    native_result=json.loads((folder/'native-audit.json').read_text());drc=json.loads((folder/'drc.json').read_text());erc=json.loads((folder/'erc.json').read_text());allpads=json.loads((folder/'all-pad-geometry.json').read_text());saved=sx.loads((folder/'pcbgolf.kicad_pcb').read_text());layers=[v[1] for v in first(saved,'layers')[1:] if str(v[1]).endswith('.Cu')]
    checks={'dsn_scope':(scope['passed'],'dsn-scope.json'),'connectivity':(not drc['unconnected_items'] and native_result['native_open_count']==0,'native-audit.json'),'physical':(not drc['violations'],'drc.json'),'parity':('schematic_parity' in drc and not drc['schematic_parity'],'drc.json'),'erc':(bool(erc.get('sheets')) and not any(s['violations'] for s in erc['sheets']),'erc.json'),'rules':(all(accepted['rules_preserved'].values()),'acceptance.json'),'net_partition':(accepted['netlist_parity'],'acceptance.json'),'electrical_geometry':(all(accepted['footprints_preserved'].values()),'acceptance.json'),'all_pad_geometry':(allpads['all_electrical_and_mechanical_pads_preserved'],'all-pad-geometry.json'),'layers':(layers==request['eligible_layers'],'native-audit.json'),'width_vias':(accepted['widths_ok'] and accepted['via_rules_ok'],'acceptance.json'),'assembly':(result['assembly_clearance']['ok'] and not result['model_coverage']['missing'],'score.json')}
    gates={k:{'passed':bool(v),'report':str(folder/name)} for k,(v,name) in checks.items()};return {'gates':gates,'diagnostics':{'native':result['native'],'routing_attempted':legal,'score_receipt':str(folder/'score.json'),'result':result},'official_score':result['official_formula_score'],'official_score_qualified':bool(request.get('official_model_contract_qualified')) and result['valid'],'commands':commands}
