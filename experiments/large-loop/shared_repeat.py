"""Repeat a retained placement through the common executor and large native adapter."""
from pathlib import Path
import argparse,json,sys,subprocess,threading,time
import sexpdata as sx
from campaign import ROOT,realize,poses,write,sha,require_stage_one_work
from record import finish
from audit import nodes,first
from live_status import update
sys.path.insert(0,str(ROOT/'experiments/pcb-loop'))
from executor import execute_candidate


def backend(request,folder,emit):
    base=Path(request['base']);source=Path(request['original_reference']);native_folder=Path(request['native_folder']);parent=Path(request['incumbent_folder'])
    assert request['eligible_layers']==['F.Cu','B.Cu']
    assert request['route_budget']=={'seconds':240,'passes':100,'threads':1,'whole_board':True,'fanout':False}
    assert request['via_options']==[{'layers':['F.Cu','B.Cu'],'diameter_mm':0.6,'drill_mm':0.3}]
    stop=threading.Event();tick=time.monotonic()
    def pulse():
        while not stop.is_set():
            emit('large full-board native realization',operation_elapsed_seconds=time.monotonic()-tick)
            stop.wait(2)
    thread=threading.Thread(target=pulse,daemon=True);thread.start()
    try:
        realize(base,native_folder,poses(parent/'pcbgolf.kicad_pcb'),base/'input/circuit.json',source)
        record=finish(base,native_folder,source,request['action'],parent,publish=False)
    finally:stop.set();thread.join()
    v=record['after'];drc=json.loads((native_folder/'drc.json').read_text());native=json.loads((native_folder/'native-audit.json').read_text());erc=json.loads((native_folder/'erc.json').read_text());board=sx.loads((native_folder/'pcbgolf.kicad_pcb').read_text());models=[];populated=[]
    for fp in nodes(board,'footprint'):
        attr=[str(x) for x in first(fp,'attr')[1:]] if nodes(fp,'attr') else []
        populated.append(not any(x in attr for x in ['dnp','exclude_from_bom','exclude_from_pos_files']))
        models.append(bool(nodes(fp,'model')) and all((native_folder/m[1].replace('${KIPRJMOD}/','')).is_file() for m in nodes(fp,'model')))
    write(native_folder/'model-coverage.json',{'all_resolve':all(models),'all_populated':all(populated),'count':len(models),'official_model_contract_qualified':False,'reason':'Generic populated header models are visualization-only; original84physicalfindings remain.'})
    layer_names={x[0]:x[1] for x in first(board,'layers')[1:]}
    checks={'connectivity':(v['native_open_count']==0 and not drc['unconnected_items'],'native-audit.json'),'physical':(not v['required_violations'],'drc.json'),'parity':('schematic_parity' in drc and not drc['schematic_parity'],'drc.json'),'erc':(bool(erc.get('sheets')) and not any(s['violations'] for s in erc['sheets']),'erc.json'),'rules':(all(v['rules_preserved'].values()),'acceptance.json'),'net_partition':(v['netlist_parity'],'acceptance.json'),'electrical_geometry':(all(v['footprints_preserved'].values()),'acceptance.json'),'all_pad_geometry':(v['all_pad_geometry_preserved'],'full-geometry.json'),'layers':(native['copper_layers']==2,'native-audit.json'),'width_vias':(v['widths_ok'] and v['via_rules_ok'] and all([layer_names.get(layer) for layer in x['layers']]==request['eligible_layers'] for x in native['vias']),'native-audit.json'),'bom_models':(all(models) and all(populated) and len(models)==156,'model-coverage.json')}
    before=json.loads((parent/'evaluation.json').read_text());better=v['feasibility_cost']<before['feasibility_cost'] or (v['feasibility_cost']==before['feasibility_cost'] and v['wire_length_mm']<before['wire_length_mm']-0.001)
    record['retained']=bool(better and v['placement_legal']);record['repeat_of']=str(parent);write(native_folder/'candidate-record.json',record)
    return {'gates':{key:{'passed':bool(passed),'report':str(native_folder/report)} for key,(passed,report) in checks.items()},'diagnostics':{'native':v,'native_folder':str(native_folder),'retained_record':str(native_folder/'candidate-record.json')},'official_score':None,'official_score_qualified':False,'diagnostic_retained':record['retained'],'commands':record['commands']}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('base',type=Path);ap.add_argument('source',type=Path);ap.add_argument('parent');ap.add_argument('output');a=ap.parse_args();base=a.base.resolve();source=a.source.resolve();parent=base/a.parent;require_stage_one_work(parent);outer=base/'shared-results';outer.mkdir(exist_ok=True)
    source_files=[*list((ROOT/'experiments/large-loop').rglob('*.py')),*list((ROOT/'experiments/pcb-loop').glob('*.py')),ROOT/'scripts/copperhead_route.py',ROOT/'scripts/copperhead_route_evidence.py',base/'input/circuit.json',base/'input/large-loop.kicad_pcb',base/'authoritative-project.json',base/'intrinsic-violations.json']
    request={'size_family':'large-loop','stage':1,'source_epoch':sha(base/'input/circuit.json'),'source_sha':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'required_gates':['connectivity','physical','parity','erc','rules','net_partition','electrical_geometry','all_pad_geometry','layers','width_vias','bom_models'],'eligible_layers':['F.Cu','B.Cu'],'via_options':[{'layers':['F.Cu','B.Cu'],'diameter_mm':0.6,'drill_mm':0.3}],'route_budget':{'seconds':240,'passes':100,'threads':1,'whole_board':True,'fanout':False},'action':{'primitive':'unchanged_placement_repeat','kind':'routing_only_repeat','rationale':'Repeat the retained placement under the identical full-board budget while qualifying the common executor/large adapter boundary. No new placement improvement is inferred.','expected_score_terms':{'native_opens':'No intended placement change; measure repeat variability','required_findings':'Original84findings stay inloss','official_score':'Unqualified/invalid;null'}},'source_files':[str(p) for p in source_files],'incumbent':{'valid':False,'official_score':None},'incumbent_folder':str(parent),'base':str(base),'original_reference':str(source),'native_folder':str(base/a.output)}
    result=execute_candidate(request,backend,outer/a.output);record=json.loads((base/a.output/'candidate-record.json').read_text());record['shared_executor_result']=str(outer/a.output/'completed.json');record['retained']=result['diagnostic_retained'] and not result['source_drift'];record['after']['accepted']=result['valid'];record['after']['official_score']=result['official_score'];record['after']['official_score_qualified']=result['official_score_qualified'];record['shared_failed_gates']=result['failed_gates'];record['stop_stage_one']=result['stop_stage_one'];write(base/a.output/'completed.json',record);update(base,state='idle');print(json.dumps({'opens':record['after']['native_open_count'],'cost':record['after']['feasibility_cost'],'valid':result['valid'],'failed_gates':result['failed_gates'],'diagnostic_retained':record['retained'],'source_drift':result['source_drift']}))
