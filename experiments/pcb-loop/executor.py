"""Family-neutral candidate lifecycle; native adapters own every physical check.

This module does not infer PCB rules, suppress findings, or calculate proxy scores.
A backend receives a source-bound request and reports mandatory gate receipts.
"""
from __future__ import annotations
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,math,os,time

def now():return datetime.now(timezone.utc).isoformat()
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def atomic(path,value):
    path=Path(path);tmp=path.with_name(path.name+'.tmp');tmp.write_text(json.dumps(value,indent=2)+'\n');os.replace(tmp,path)

def execute_candidate(request:dict, backend, folder:Path, progress=None):
    """backend(request, folder, emit) -> {gates,diagnostics,official_score,commands}.

    Backend must use the declared full-board budget and layer/via configuration,
    preserve authoritative project bytes, and independently read saved native CAD.
    Each gate is {passed: bool, report: str}; absent gates are failures.
    Stage1valid returns stop_stage_one=True immediately. No further Stage1proposal
    is permitted by a controller after this signal. Diagnostic retention stays
    separate from physical validity; Stage2retention requires a qualified score.
    """
    folder=Path(folder);folder.mkdir(exist_ok=False)
    for key in ['size_family','stage','source_epoch','source_sha','required_gates','eligible_layers','via_options','route_budget','action','source_files','incumbent']:
        if key not in request:raise ValueError('Missing request field: '+key)
    if not request['required_gates']:raise ValueError('required_gates must not be empty')
    if request['stage'] not in [1,2]:raise ValueError('stage must be1or2')
    if request['stage']==2:
        incumbent=request['incumbent'];baseline=incumbent.get('official_score')
        if not incumbent.get('valid'):raise ValueError('Stage2 requires valid incumbent')
        if incumbent.get('official_score_qualified') is not True or not isinstance(baseline,(float,int)) or isinstance(baseline,bool) or not math.isfinite(baseline):raise ValueError('Stage2 requires finite qualified incumbent score')
    sources={str(Path(p).resolve()):sha(p) for p in request['source_files']};started=now();tick=time.monotonic();packet={**request,'source_files':list(sources),'started_at':started,'source_file_sha256':sources};atomic(folder/'request.json',packet)
    def emit(operation,**fields):
        state={'size_family':request['size_family'],'stage':request['stage'],'running':True,'current_operation':operation,'started_at':started,'elapsed_seconds':time.monotonic()-tick,'heartbeat_at':now(),'worker_pid':os.getpid(),**fields};atomic(folder/'live-status.json',state)
        if progress:progress(state)
    emit('native adapter start')
    try:
        measured=backend(packet,folder,emit)
        gates=measured.get('gates',{});failed=[g for g in request['required_gates'] if gates.get(g,{}).get('passed') is not True or not Path(gates.get(g,{}).get('report','')).is_file()]
        drift=[p for p,digest in sources.items() if sha(p)!=digest]
        valid=not failed and not drift
        score=measured.get('official_score')
        score_qualified=valid and measured.get('official_score_qualified') is True and isinstance(score,(float,int)) and not isinstance(score,bool) and math.isfinite(score)
        if not score_qualified:score=None
        old=request['incumbent'];retain=valid if request['stage']==1 else score_qualified and score<old['official_score']
        result={'schema':1,'size_family':request['size_family'],'stage':request['stage'],'source_epoch':request['source_epoch'],'source_sha':request['source_sha'],'started_at':started,'finished_at':now(),'elapsed_seconds':time.monotonic()-tick,'action':request['action'],'request':str(folder/'request.json'),'source_file_sha256':sources,'source_drift':drift,'gates':gates,'failed_gates':failed,'valid':valid,'official_score':score,'official_score_qualified':score_qualified,'diagnostics':measured.get('diagnostics',{}),'commands':measured.get('commands',[]),'retained':retain,'diagnostic_retained':bool(measured.get('diagnostic_retained',False)),'stop_stage_one':request['stage']==1 and valid,'handoff_stage':2 if request['stage']==1 and valid else None,'folder':str(folder)}
        atomic(folder/'completed.json',result);emit('completed',running=False,valid=valid,official_score=score,retained=retain,stop_stage_one=result['stop_stage_one']);return result
    except Exception as exc:
        emit('failed',running=False,error=str(exc));atomic(folder/'failure.json',{'started_at':started,'finished_at':now(),'error':str(exc),'source_sha':request['source_sha']});raise
