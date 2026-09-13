"""Bounded native operations for the isolated incremental fixture only."""
from pathlib import Path
import argparse
import asyncio
import json
import shutil
import time
from jitx._websocket import Message, ErrorMessage
from jitx.run.runtime import Runtime
from jitx._runtime._legacy_plugins import do_export

DESIGN = 'incremental_fixture.design.IncrementalProof'
BASE = Path('/Users/philippe/dev/copper-scar-jitx')


async def execute(plan, out):
    out.mkdir(parents=True, exist_ok=False)
    shutil.copytree(BASE / 'designs' / DESIGN, out / 'input-native-snapshot')
    (out / 'plan.json').write_text(json.dumps(plan, indent=2))
    uri = json.loads((BASE / '.jitx/runtime.json').read_text())['websocket_uri'].rstrip('/')
    started = time.monotonic()
    async with Runtime(uri=uri) as runtime:
        client = runtime._client.route('design/' + DESIGN)

        async def request(kind, body, label):
            replies = []
            t = time.monotonic()

            async def consume():
                conv = await client.request(Message('phd', kind, body))
                async for item in conv:
                    replies.append({'type': item.type, 'body': item.body})
            try:
                await asyncio.wait_for(consume(), 60)
            finally:
                (out / (label + '.json')).write_text(json.dumps(replies, indent=2))
                print(label, round(time.monotonic() - t, 3), flush=True)
            return replies

        await request('load', {}, 'before')
        for index, action in enumerate(plan):
            assert action['type'] in {'reposition', 'unroute', 'via-add', 'via-drop', 'route', 'load'}
            await request(action['type'], action['body'], f'action-{index:02}-{action["type"]}')
        attempts = []
        while True:
            try:
                remaining = 300 - (time.monotonic() - started)
                if remaining <= 0:
                    raise TimeoutError('Native completion unknown; do not start another mutation')
                await asyncio.wait_for(do_export('kicad', DESIGN), remaining)
                break
            except ErrorMessage as error:
                attempts.append({'elapsed_s': time.monotonic() - started, 'error': str(error)})
                (out / 'export-wait.json').write_text(json.dumps(attempts, indent=2))
                if 'physical design task' not in str(error) or 'in progress' not in str(error):
                    raise
                await asyncio.sleep(1)
        # Final load occurs only after the successful export completion barrier.
        await request('load', {}, 'final')
        shutil.copytree(BASE / 'designs' / DESIGN / 'kicad', out / 'export')
        shutil.copytree(BASE / 'designs' / DESIGN, out / 'output-native-snapshot')
        (out / 'completion.json').write_text(json.dumps({'design': DESIGN, 'elapsed_s': time.monotonic() - started,
            'export_barrier': True, 'native_worker_state': 'completed', 'whole_board_valid': 'requires independent checks'}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('plan', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    asyncio.run(execute(json.loads(args.plan.read_text()), args.output))
