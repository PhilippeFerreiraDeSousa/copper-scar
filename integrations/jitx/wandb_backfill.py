"""Publish an immutable JITX replay to W&B; no native calls or evaluator dependency.

Preparation is offline. Upload is explicit, resumable, and uses only allowlisted
checkpoint data. Corrected histories get distinct runs; superseded values never
share a curve. Credentials are read into process memory, never serialized.
"""
from pathlib import Path
import argparse
import datetime as dt
import hashlib
import json
import os
import shutil
import uuid

POLICY = 'jitx-feasibility-v3'
METRICS = {'missing_connections': 'missing_pairs', 'incorrect_connections': 'incorrect_connections',
           'physical_errors': 'physical_errors', 'physical_warnings': 'warnings',
           'erc_errors': 'erc_errors', 'erc_warnings': 'erc_warnings', 'parity_issues': 'parity_issues'}


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, obj):
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(obj, indent=2))
    temporary.replace(path)


def choose_incumbent(evaluation, best):
    if not (evaluation.get('evaluation_reliable') and evaluation.get('invariants_ok') and evaluation.get('cost')):
        return False
    return best is None or (evaluation['cost'] < best['cost'] and all(
        evaluation['metrics'][key] <= best['metrics'][key]
        for key in ('physical_errors', 'incorrect_connections', 'erc_errors')))


def prepare(replay, ledger, output):
    request = read(replay / 'request.json')
    manifest = read(replay / 'manifest.json')
    assert request['key'] == manifest['key']
    assert request['policy'] == POLICY
    assert len(request['steps']) == len(manifest['frames'])
    output.mkdir(parents=True, exist_ok=True)
    media = output / 'media'
    media.mkdir(exist_ok=True)
    best = None
    best_image = None
    rows = []
    baseline = request['steps'][0]['snapshot']['board_sha256']
    for index, (step, frame) in enumerate(zip(request['steps'], manifest['frames'])):
        assert step['record_index'] == frame['record_index']
        e = step.get('evaluation', {})
        reliable = e.get('evaluation_reliable') is True and e.get('invariants_ok') is True
        retained = choose_incumbent(e, best)
        row = {'track': 'jitx', 'outer_index': index, 'attempt_id': step['label'],
               'ledger_record_index': step['record_index'], 'policy': POLICY,
               'baseline_hash': baseline, 'evaluation_reliable': reliable,
               'native/invariants_ok': e.get('invariants_ok') is True,
               'validity_gate': e.get('valid') is True, 'retained': retained,
               'recorded_retain': e.get('retain', False),
               'status': 'failed' if step['held'] else 'unreliable' if not reliable else 'retained' if retained else 'rejected',
               'comparison_kind': 'initial_placement' if index == 0 else 'failed_attempt' if step['held'] else
                   'placement_checkpoint' if step['label'].endswith(('-input', '-placed')) or 'moved-004' in step['label'] else 'routed_placement',
               'evaluation/elapsed_s': e.get('elapsed_seconds'),
               'evaluation/recorded_at': e.get('started_at'),
               'routing/scope': 'not audited for this checkpoint',
               'routing/termination': 'not established from this record',
               'routing/complete_multilayer_proof': False,
               'native/worker_running': False,
               'note': step.get('caption', '')}
        if step['held']:
            row['error'] = step['failure']['error']
            # No current board or loss is invented for a failed native operation.
        else:
            assert e['policy_version'] == POLICY
            snap = step['snapshot']
            for field, digest in [('board', 'board_sha256'), ('preview', 'preview_sha256'), ('record', 'evaluation_sha256')]:
                assert sha(Path(snap[field])) == snap[digest], f'Changed snapshot: {field}'
            assert e['artifacts']['pcbgolf.kicad_pcb'] == snap['board_sha256']
            assert sha(Path(frame['directory']) / 'pcbgolf.kicad_pcb') == snap['board_sha256']
            assert read(Path(frame['directory']) / 'evaluation.json') == e
            image = media / f'board-{index:02}.png'
            shutil.copy2(Path(frame['directory']) / 'board.png', image)
            row.update(board_sha256=snap['board_sha256'], evaluation_sha256=snap['evaluation_sha256'],
                       attempted_image=str(image), board_view='Actual outer copper and silkscreen; no airwires or inner copper')
            if reliable:
                row.update({f'loss/{dest}': e['metrics'][source] for source, dest in METRICS.items()})
                row['diagnostic_cost_vector'] = e['cost']
            else:
                row['unreliable_observed_counts'] = e.get('metrics', {})
            if retained:
                best, best_image = e, str(image)
        if best:
            row.update({f'incumbent/{dest}': best['metrics'][source] for source, dest in METRICS.items()})
            row['incumbent_image'] = best_image
            row['incumbent_board_sha256'] = best['artifacts']['pcbgolf.kicad_pcb']
        for number, name in [('008', 'group-floorplan'), ('009', 'power-neighborhood')]:
            if step['label'].startswith(f'iteration-{number}-{name}'):
                directory = ledger / f'iteration-{number}-{name}'
                delta = directory / 'placement-delta.json'
                if delta.exists() and not step['label'].endswith('-input'):
                    d = read(delta)
                    row['placement/moved_count'] = d['moved_or_rotated_count']
                    row['placement/deltas'] = d['moves']
                if step['label'].endswith('-routed'):
                    audit = read(ledger / 'via-workflow-diagnostics' / f'scope-{number}.json')
                    row['routing/scope'] = audit['conclusion']
                    for key in ('all_native_nets', 'selected_nets', 'all_native_terminals', 'selected_terminals', 'via_definitions', 'requested_layers', 'copper_layer_count'):
                        row[f'routing/{key}'] = audit[key]
                    row['routing/notifications'] = audit['notifications']
                    row['routing/via_instances'] = 0
                    row['routing/ack_elapsed_s'] = sum(v for k, v in audit['timings'].items() if k.startswith('route-layer-'))
                    row['routing/export_wait_s'] = audit['timings']['export_including_wait']
                    command = read(directory / 'routed.command.json')
                    row['routing/elapsed_s'] = command['elapsed_seconds']
                    row['routing/termination'] = 'Successful export barrier and independent checks; incomplete connectivity'
                    row['routing/completion_limits'] = '55s request / 600s export / 900s wrapper; not native effort or cancellation controls'
        rows.append(row)
    video = 'jitx-stage-one-replay-5x.mp4'
    assert sha(replay / video) == manifest['videos'][video]
    shutil.copy2(replay / video, media / video)
    # Include evaluation digests and all selected data in the immutable revision.
    canonical = [{k: v for k, v in r.items() if not k.endswith('_image')} for r in rows]
    revision = hashlib.sha256(json.dumps(canonical, sort_keys=True).encode()).hexdigest()
    bundle = {'schema': 'jitx-wandb-v1', 'policy': POLICY, 'track': 'jitx', 'revision': revision,
              'run_id': 'jitx-v3-' + revision[:16], 'baseline_hash': baseline,
              'cutoff_checkpoint': request['cutoff_checkpoint'], 'cutoff_record_index': request['cutoff_record_index'],
              'replay_key': request['key'], 'rows': rows, 'video': str(media / video),
              'limitations': ['Incomplete engineering qualification; no valid board or competition score.',
                 'Chronological checkpoint index includes input/placed/routed phases, not optimizer generations.',
                 'Corrected policy-v3 history only; older policies and older same-policy rechecks superseded.',
                 'JITX/Copperhead raw costs are not directly comparable.',
                 'Historical backfill, not new routing or evaluation execution.']}
    bundle['media_sha256'] = {p.name: sha(p) for p in media.iterdir() if p.is_file()}
    write(output / 'bundle.json', bundle)
    return bundle


def upload(output, key_file, entity, project):
    # SDKs and network are deliberately absent from prepare/evaluation/native paths.
    os.environ['WANDB_API_KEY'] = key_file.read_text().strip()
    os.environ['WANDB_CONSOLE'] = 'off'
    os.environ['WANDB_DISABLE_CODE'] = 'true'
    os.environ['WANDB_SILENT'] = 'true'
    import wandb
    import requests
    bundle = read(output / 'bundle.json')
    for name, digest in bundle['media_sha256'].items():
        assert sha(output / 'media' / name) == digest
    api = wandb.Api(timeout=30)
    if not any(p.name == project for p in api.projects(entity)):
        raise ValueError('Requested existing project is not accessible')
    run_path = f'{entity}/{project}/{bundle["run_id"]}'
    run_url = f'https://wandb.ai/{entity}/{project}/runs/{bundle["run_id"]}'
    existing = next(iter(api.runs(f'{entity}/{project}', filters={'name': bundle['run_id']})), None)
    seen = set()
    if existing:
        assert existing.config['revision'] == bundle['revision']
        seen = {int(r['outer_index']) for r in existing.scan_history(keys=['outer_index'])}
    trace = requests.Session()
    trace.auth = ('api', os.environ['WANDB_API_KEY'])

    def trace_request(endpoint, body):
        response = trace.post('https://trace.wandb.ai/' + endpoint, json=body, timeout=30)
        if endpoint == 'call/read' and response.status_code == 404:
            return {'call': None}
        if not response.ok:
            write(output / 'remote-error-status.json', {'endpoint': endpoint, 'http_status': response.status_code})
            raise RuntimeError(f'Weave {endpoint} HTTP {response.status_code}')
        return response.json()

    trace_urls = []
    # Stable call IDs make interrupted backfills repeatable without duplicate traces.
    for row in bundle['rows']:
        call_id = str(uuid.uuid5(uuid.NAMESPACE_URL, run_path + '/' + str(row['outer_index'])))
        previous = trace_request('call/read', {'project_id': f'{entity}/{project}', 'id': call_id}).get('call')
        if not previous or not previous.get('ended_at'):
            now = dt.datetime.now(dt.timezone.utc).isoformat()
            inputs = {k: row[k] for k in ('attempt_id', 'outer_index', 'policy', 'baseline_hash', 'ledger_record_index')}
            trace_request(f'v2/{entity}/{project}/calls/complete', {'batch': [{'project_id': f'{entity}/{project}', 'id': call_id,
                'op_name': 'jitx.checkpoint_backfill', 'display_name': row['attempt_id'], 'trace_id': call_id,
                'started_at': now, 'attributes': {'track': 'jitx', 'historical_backfill': True,
                    'original_evaluation_time': row.get('evaluation/recorded_at'), 'revision': bundle['revision']},
                'inputs': inputs, 'wb_run_id': run_path, 'wb_run_step': row['outer_index'],
                'ended_at': dt.datetime.now(dt.timezone.utc).isoformat(),
                'output': {k: v for k, v in row.items() if not k.endswith('_image')},
                'summary': {'status': row['status'], 'valid': row['validity_gate'], 'retained': row['retained']}}]})
        trace_urls.append(f'https://wandb.ai/{entity}/{project}/r/call/{call_id}')
    receipt = {'run_url': run_url, 'charts_url': run_url + '/workspace', 'files_url': run_url + '/files',
               'weave_url': f'https://wandb.ai/{entity}/{project}/weave/calls', 'trace_urls': trace_urls,
               'cutoff': bundle['cutoff_checkpoint'], 'record_index': bundle['cutoff_record_index']}
    if len(seen) < len(bundle['rows']) or not (existing and existing.summary.get('backfill_complete')):
        sdk_dir = output / 'sdk'
        sdk_dir.mkdir(exist_ok=True)
        run = wandb.init(entity=entity, project=project, id=bundle['run_id'], resume='allow',
            name=f'JITX policy v3 · through {bundle["cutoff_checkpoint"]}',
            job_type='immutable-checkpoint-backfill', group='jitx-feasibility-v3',
            tags=['jitx', 'incomplete', 'historical-backfill'], dir=str(sdk_dir),
            config={k: v for k, v in bundle.items() if k not in ('rows', 'video', 'media_sha256')},
            settings=wandb.Settings(disable_git=True, disable_code=True, x_disable_stats=True,
                                    console='off', init_timeout=60))
        run.define_metric('outer_index')
        for prefix in ('loss/*', 'incumbent/*', 'routing/*', 'placement/*', 'evaluation/*'):
            run.define_metric(prefix, step_metric='outer_index')
        try:
            for row, url in zip(bundle['rows'], trace_urls):
                if row['outer_index'] in seen:
                    continue
                data = {k: v for k, v in row.items() if not k.endswith('_image') and v is not None}
                data['weave/trace_url'] = url
                for field, name in [('attempted_image', 'board/attempted'), ('incumbent_image', 'board/incumbent')]:
                    if field in row:
                        caption = (row['attempt_id'] + ' / ' + row['status']) if field == 'attempted_image' else 'Retained incomplete board'
                        data[name] = wandb.Image(row[field], caption=caption)
                run.log(data, step=row['outer_index'])
            run.log({'replay/5x': wandb.Video(bundle['video'], format='mp4'), 'weave/url': receipt['weave_url']})
            artifact = wandb.Artifact(bundle['run_id'] + '-checkpoints', type='board-checkpoints',
                                      metadata={'revision': bundle['revision'], 'cutoff': bundle['cutoff_checkpoint']})
            artifact.add_file(str(output / 'bundle.json'), name='bundle.json')
            artifact.add_dir(str(output / 'media'), name='media')
            run.log_artifact(artifact)
            run.summary.update({'backfill_complete': True, 'checkpoint_count': len(bundle['rows']),
                'valid_board': False, 'routing_worker_running': False, 'cutoff': bundle['cutoff_checkpoint'],
                'cutoff_record_index': bundle['cutoff_record_index'], 'last_trace_url': trace_urls[-1]})
        finally:
            run.finish()
    api.flush()
    remote = api.run(run_path)
    history = list(remote.scan_history())
    indices = [int(r['outer_index']) for r in history if 'outer_index' in r]
    # The replay-only terminal row may have step_metric synchronization; compare unique checkpoint indices.
    assert set(indices) == set(range(len(bundle['rows'])))
    final = next(r for r in history if r.get('attempt_id') == bundle['cutoff_checkpoint'])
    checkpoints = [r for r in history if 'attempt_id' in r]
    assert len(checkpoints) == len(bundle['rows'])
    for expected in bundle['rows']:
        actual = next(r for r in checkpoints if r['outer_index'] == expected['outer_index'])
        assert actual['status'] == expected['status']
        if expected['status'] in ('failed', 'unreliable'):
            assert actual.get('loss/missing_pairs') is None
    assert final['loss/missing_pairs'] == bundle['rows'][-1]['loss/missing_pairs']
    assert final['incumbent/missing_pairs'] == bundle['rows'][-1]['incumbent/missing_pairs']
    image_path = final['board/attempted']['path']
    image_file = remote.file(image_path)
    download = image_file.download(root=str(output / 'remote-verification'), replace=True)
    downloaded = Path(download.name)
    assert sha(downloaded) == sha(Path(bundle['rows'][-1]['attempted_image']))
    last_call = trace_request('call/read', {'project_id': f'{entity}/{project}', 'id': trace_urls[-1].split('/')[-1]})['call']
    assert last_call['output']['loss/missing_pairs'] == final['loss/missing_pairs']
    receipt.update(state='verified', checkpoint_count=len(bundle['rows']), remote_history_rows=len(history),
                   remote_board_sha256=sha(downloaded), remote_board_image=image_path,
                   final_metrics={k: v for k, v in final.items() if k.startswith(('loss/', 'incumbent/'))},
                   verified_at=dt.datetime.now(dt.timezone.utc).isoformat())
    write(output / 'upload-receipt.json', receipt)
    for name in ('upload-error.json', 'remote-error-status.json'):
        (output / name).unlink(missing_ok=True)
    return receipt


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--replay', type=Path, required=True)
    parser.add_argument('--ledger', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--upload', action='store_true')
    parser.add_argument('--key-file', type=Path)
    parser.add_argument('--entity', default='philippe-fdesousa')
    parser.add_argument('--project', default='copper-scar')
    args = parser.parse_args()
    bundle = prepare(args.replay, args.ledger, args.output)
    print(json.dumps({'prepared': bundle['run_id'], 'checkpoints': len(bundle['rows'])}), flush=True)
    if args.upload:
        if not args.key_file:
            parser.error('--upload requires --key-file')
        try:
            print(json.dumps(upload(args.output, args.key_file, args.entity, args.project), indent=2))
        except Exception as error:
            # Never dump SDK exceptions/requests or environment containing authentication.
            write(args.output / 'upload-error.json', {'type': type(error).__name__, 'state': 'upload_incomplete',
                  'local_checkpoints_unchanged': True})
            print('Upload incomplete: ' + type(error).__name__ + '; local checkpoint bundle remains available.')
            raise SystemExit(1)
