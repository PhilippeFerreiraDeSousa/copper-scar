"""Allowlisted synthetic proof upload, adapted from JITX wandb_backfill.py d1e545c.

Reads the existing credential only into process memory/environment. No native
control, arbitrary directory upload, automatic code capture, or product score.
"""
from pathlib import Path
import argparse
import datetime as dt
import hashlib
import json
import os
import uuid


def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def publish(output,key_file):
    bundle=read(output/'bundle.json');assert bundle['comparison_kind']=='synthetic_fixture_bridge'
    for name,value in bundle['media_sha256'].items():
        assert Path(name).name==name and sha(output/'media'/name)==value
    os.environ.update(WANDB_API_KEY=key_file.read_text().strip(),WANDB_CONSOLE='off',WANDB_DISABLE_CODE='true',WANDB_SILENT='true')
    import wandb
    import requests
    entity='philippe-fdesousa';project='copper-scar';run_id='fixture-bridge-'+bundle['result_sha256'][:12]
    run_path=f'{entity}/{project}/{run_id}';url=f'https://wandb.ai/{entity}/{project}/runs/{run_id}'
    api=wandb.Api(timeout=30)
    assert any(p.name==project for p in api.projects(entity)), 'existing authorized project inaccessible'
    session=requests.Session();session.auth=('api',os.environ['WANDB_API_KEY'])
    def trace(endpoint,body):
        response=session.post('https://trace.wandb.ai/'+endpoint,json=body,timeout=30)
        if endpoint=='call/read' and response.status_code==404:return {'call':None}
        if not response.ok:raise RuntimeError('Weave HTTP '+str(response.status_code))
        return response.json()
    traces=[]
    for row in bundle['rows']:
        call_id=str(uuid.uuid5(uuid.NAMESPACE_URL,run_path+'/'+str(row['step'])))
        previous=trace('call/read',{'project_id':f'{entity}/{project}','id':call_id}).get('call')
        if not previous or not previous.get('ended_at'):
            now=dt.datetime.now(dt.timezone.utc).isoformat()
            trace(f'v2/{entity}/{project}/calls/complete',{'batch':[{'project_id':f'{entity}/{project}','id':call_id,
                'op_name':'synthetic.fixture_bridge','display_name':'Synthetic fixture / '+row['stage'],'trace_id':call_id,
                'started_at':now,'ended_at':now,'attributes':{'comparison_kind':'synthetic_fixture_bridge','product_valid':False},
                'inputs':{'request_sha256':bundle['request_sha256'],'board_sha256':row['board_sha256']},
                'output':row,'wb_run_id':run_path,'wb_run_step':row['step'],
                'summary':{'fixture_realized_nets':row['realized_nets'],'product_valid':False}}]})
        traces.append(f'https://wandb.ai/{entity}/{project}/r/call/{call_id}')
    existing=next(iter(api.runs(f'{entity}/{project}',filters={'name':run_id})),None)
    seen=set()
    if existing:
        assert existing.config['result_sha256']==bundle['result_sha256']
        seen={r['fixture/step'] for r in existing.scan_history() if 'fixture/stage' in r}
    if len(seen)<4 or not existing.summary.get('proof_upload_complete'):
        sdk=output/'sdk';sdk.mkdir(exist_ok=True)
        run=wandb.init(entity=entity,project=project,id=run_id,resume='allow',name='Synthetic fixture · placement-routing bridge',
            job_type='synthetic-fixture-proof',group='synthetic-fixture-bridge',tags=['synthetic','fixture','not-pcbgolf-progress'],dir=str(sdk),
            config={k:bundle[k] for k in ('schema','comparison_kind','result_sha256','request_sha256','product_valid')},
            settings=wandb.Settings(disable_git=True,disable_code=True,x_disable_stats=True,console='off',init_timeout=60))
        try:
            run.define_metric('fixture/step');run.define_metric('fixture/*',step_metric='fixture/step')
            for row,trace_url in zip(bundle['rows'],traces):
                if row['step'] in seen:continue
                run.log({'fixture/step':row['step'],'fixture/stage':row['stage'],
                         'fixture/opens':row['opens'],'fixture/violations':row['violations'],
                         'fixture/realized_nets':row['realized_nets'],'fixture/vias':row['vias'],
                         'fixture/board_sha256':row['board_sha256'],'comparison_kind':'synthetic_fixture_bridge',
                         'fixture/board':wandb.Image(str(output/'media'/row['image']),caption='Synthetic fixture: '+row['stage']),
                         'weave/trace_url':trace_url},step=row['step'])
            run.log({'fixture/replay_5x':wandb.Video(str(output/'media/replay-5x.mp4'),format='mp4'),
                     'fixture/diagnostics':wandb.Image(str(output/'media/loss.png'))})
            artifact=wandb.Artifact(run_id+'-proof',type='synthetic-fixture-proof',metadata={'product_valid':False})
            artifact.add_file(str(output/'bundle.json'),name='bundle.json')
            # Only hash-allowlisted files, never runtime logs, cache or credentials.
            for name in bundle['media_sha256']:artifact.add_file(str(output/'media'/name),name='media/'+name)
            run.log_artifact(artifact)
            run.summary.update({'proof_upload_complete':True,'fixture_decision':bundle['decision'],'product_valid':False,
                               'routing_worker_running':False,'fixture_move_barrier_s':bundle['native_move_and_barrier_s']})
        finally:run.finish()
    api.flush();remote=api.run(run_path);rows=[r for r in remote.scan_history() if 'fixture/stage' in r]
    assert len(rows)==4
    for expected,actual in zip(bundle['rows'],rows):
        assert actual['fixture/opens']==expected['opens'] and actual['fixture/board_sha256']==expected['board_sha256']
    final=rows[-1];download=remote.file(final['fixture/board']['path']).download(root=str(output/'remote-verification'),replace=True)
    assert sha(Path(download.name))==sha(output/'media/board-03.png')
    last=trace('call/read',{'project_id':f'{entity}/{project}','id':traces[-1].split('/')[-1]})['call']
    assert last['output']['board_sha256']==bundle['rows'][-1]['board_sha256']
    artifacts=list(remote.logged_artifacts());assert artifacts
    artifact=next(a for a in artifacts if a.type=='synthetic-fixture-proof')
    location=Path(artifact.download(root=str(output/'remote-artifact-verification')))
    for name,value in bundle['media_sha256'].items():assert sha(location/'media'/name)==value
    receipt={'state':'verified','run_url':url,'trace_urls':traces,'history_rows':len(rows),
             'remote_artifact':artifact.qualified_name,'all_allowlisted_artifact_hashes_verified':True,
             'remote_final_image_sha256':sha(Path(download.name)),'product_valid':False}
    (output/'upload-receipt.json').write_text(json.dumps(receipt,indent=2))
    (output/'upload-error.json').unlink(missing_ok=True)
    return receipt

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('output',type=Path);p.add_argument('--key-file',type=Path,required=True);a=p.parse_args()
    try:print(json.dumps(publish(a.output.resolve(),a.key_file),indent=2))
    except Exception as error:
        (a.output/'upload-error.json').write_text(json.dumps({'state':'incomplete','type':type(error).__name__}))
        print('Upload incomplete: '+type(error).__name__);raise SystemExit(1)
