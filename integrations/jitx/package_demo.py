"""Package existing, hash-verified evidence; never contacts a JITX runtime."""
import argparse
import hashlib
import html
import json
from pathlib import Path
import re
import shutil


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_saved_drc(stage, summary):
    board = next((stage / 'independent').glob('*.kicad_pcb'))
    assert sha(board) == summary['normalized_board_sha256']
    assert sha(board.with_suffix('.kicad_pro')) == summary['project_sha256']
    for i in range(2):
        report = read(stage / 'independent' / f'drc-{i}.json')
        assert len(report['unconnected_items']) == summary['opens']
        assert report['violations'] == []


def fixture_svg(summary):
    """Render the checked fixture's exact exported segments/vias and pad poses."""
    shapes = []
    def fields(item, key):
        match = re.search(r'\(' + key + r' ([^()]*)\)', item)
        assert match, (key, item)
        return match[1].replace('"', '').split()
    for net, items in summary['copper_by_net'].items():
        for item in items:
            if item.startswith('(segment '):
                x, y = map(float, fields(item, 'start'))
                a, b = map(float, fields(item, 'end'))
                width = float(fields(item, 'width')[0])
                color = '#ed6b65' if fields(item, 'layer')[0] == 'F.Cu' else '#57b9ef'
                shapes.append(f'<path d="M{x} {y}L{a} {b}" stroke="{color}" stroke-width="{width}" stroke-linecap="round"><title>{html.escape(net)}</title></path>')
            elif item.startswith('(via '):
                x, y = map(float, fields(item, 'at'))
                radius = float(fields(item, 'size')[0]) / 2
                drill = float(fields(item, 'drill')[0]) / 2
                shapes.append(f'<circle cx="{x}" cy="{y}" r="{radius}" fill="#f5d773"/><circle cx="{x}" cy="{y}" r="{drill}" fill="#101a29"/>')
            else:
                raise ValueError('Fixture renderer only supports measured segments and vias')
    for ref, (x, y, angle) in summary['poses'].items():
        assert angle == 0
        shapes.append(f'<rect x="{x-.6}" y="{y-.6}" width="1.2" height="1.2" fill="#ed6b65"/><text x="{x}" y="{y-1}" text-anchor="middle" fill="#e9edf4" font-size=".8">{ref}</text>')
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="121 92 37 32" role="img" aria-label="Measured two-layer fixture copper"><rect x="123.5" y="94" width="32" height="28" rx=".2" fill="#101a29" stroke="#899db2" stroke-width=".15"/><rect x="138.5" y="94" width="2" height="28" fill="#4e3641"/>' + ''.join(shapes) + '</svg>'


def package(project, outputs, dest):
    dest.mkdir(parents=True, exist_ok=True)
    evidence = dest / 'evidence'
    evidence.mkdir(exist_ok=True)
    fixture = project / 'runs/incremental-proof'
    source = project / 'runs/source-route-proof'
    rows, panels = [], []
    stages = [('01-definition-only-sweep', 'Definition alone: three opens'),
              ('03-multilayer-routed', 'Six vias complete all four nets'),
              ('04-moved', 'TP4 move: unrelated copper preserved'),
              ('07-source-updated-reload', 'Authored pose survives rebuild')]
    summaries = {}
    for name, title in stages:
        stage = fixture / name
        summary = read(stage / 'independent/summary.json')
        board = next((stage / 'export').glob('*.kicad_pcb'))
        assert sha(board) == summary['source_board_sha256']
        assert summary['repeated_drc_agrees'] and summary['violations'] == []
        verify_saved_drc(stage, summary)
        target = evidence / name
        target.mkdir(exist_ok=True)
        for pattern in ('*.kicad_pcb', '*.kicad_pro', 'summary.json', 'drc-*.json'):
            for file in (stage / 'independent').glob(pattern):
                shutil.copy2(file, target / file.name)
        (target / 'fixture.svg').write_text(fixture_svg(summary))
        summaries[name] = summary
        rows.append({'stage': name, 'scope': 'eight-pad fixture', 'opens': summary['opens'],
                     'violations': 0, 'vias': summary['via_count'], 'layers': summary['copper_layers_used'],
                     'source_board_sha256': sha(board), 'evidence': str(target.relative_to(dest))})
        panels.append(f'<article><h3>{html.escape(title)}</h3>{fixture_svg(summary)}<p>{summary["opens"]} opens · 0 violations · {summary["via_count"]} vias</p></article>')
    before, moved = summaries['03-multilayer-routed'], summaries['04-moved']
    assert [r for r in before['poses'] if before['poses'][r] != moved['poses'][r]] == ['TP4']
    assert all(before['copper_by_net'][n] == moved['copper_by_net'][n] for n in ('HOLD', 'CROSS_B', 'CROSS_C'))
    for file in ('result.json', 'bridge-review.json'):
        shutil.copy2(source / file, evidence / ('source-route-' + file))
    shutil.copytree(source / 'source-snapshot', evidence / 'source', dirs_exist_ok=True)
    for name in ('01-built', '02-rebuilt'):
        target = evidence / ('source-' + name)
        target.mkdir(exist_ok=True)
        summary = read(source / name / 'independent/summary.json')
        board = next((source / name / 'export').glob('*.kicad_pcb'))
        assert sha(board) == summary['source_board_sha256']
        assert summary['opens'] == 0 and summary['violations'] == []
        verify_saved_drc(source / name, summary)
        for pattern in ('*.kicad_pcb', '*.kicad_pro', 'summary.json', 'drc-*.json'):
            for file in (source / name / 'independent').glob(pattern):
                shutil.copy2(file, target / file.name)
    for name, expected in read(source / 'result.json')['source_hashes'].items():
        assert sha(evidence / 'source' / name) == expected
    shutil.copy2(fixture / 'proof-result.json', evidence / 'incremental-proof-result.json')
    manifest = read(outputs / 'jitx-latest-replay-5x-manifest.json')
    history = []
    for frame in manifest['frames']:
        snapshot = frame['snapshot']
        for field, hashfield in [('board', 'board_sha256'), ('record', 'evaluation_sha256'), ('preview', 'preview_sha256')]:
            assert sha(Path(snapshot[field])) == snapshot[hashfield], (frame['label'], field)
        record = read(Path(snapshot['record']))
        status = 'failed; preceding board held' if frame['held'] else 'completed; reliable evaluation' if record['evaluation_reliable'] else 'completed; evaluation unreliable'
        history.append({'label': frame['label'], 'status': status, 'valid': record['valid'],
                        'metrics': None if frame['held'] or not record['evaluation_reliable'] else record['metrics'],
                        'board_sha256': snapshot['board_sha256']})
    video = outputs / 'jitx-latest-replay-5x.mp4'
    assert sha(video) in manifest['videos'].values()
    shutil.copy2(video, dest / 'whole-board-incomplete-replay.mp4')
    shutil.copy2(outputs / 'jitx-latest-replay-5x-manifest.json', evidence / 'whole-board-original-manifest.json')
    last = project / 'candidates/iteration-009-power-neighborhood-routed'
    evaluation = read(last / 'evaluation.json')
    assert not evaluation['valid'] and evaluation['metrics']['missing_connections'] == 310
    assert sha(last / 'pcbgolf.kicad_pcb') == evaluation['artifacts']['pcbgolf.kicad_pcb']
    for file in ('evaluation.json', 'drc.json', 'erc.json', 'pcbgolf.kicad_pcb', 'pcbgolf.kicad_pro'):
        shutil.copy2(last / file, evidence / ('whole-board-009-' + file))
    for num in ('008', '009'):
        shutil.copy2(project / f'runs/stage1/via-workflow-diagnostics/scope-{num}.json', evidence / f'scope-{num}.json')
    for report in ('jitx-source-authored-routing-verification.md', 'jitx-topology-capture-integration-report.md'):
        shutil.copy2(outputs / report, evidence / report)
    data = {'fixture_stages': rows, 'whole_board_history': history, 'whole_board_best': evaluation['metrics'],
            'whole_board_valid': False, 'new_native_runs': 0,
            'audit': 'Existing board/source/replay hashes and saved geometry invariants rechecked; no new routing or DRC execution.'}
    (evidence / 'audit.json').write_text(json.dumps(data, indent=2) + '\n')
    table = '\n'.join(f'| {h["label"]} | {h["status"]} | {h["metrics"]["missing_connections"] if h["metrics"] else "—"} | {h["metrics"]["physical_errors"] if h["metrics"] else "—"} |' for h in history)
    (dest / 'README.md').write_text('''# JITX offline evidence demo

Open index.html directly. No server, login, network or running JITX is needed.

Strongest original JITX demonstration: an eight-pad/four-net fixture with explicit six-via two-layer routing, zero opens/violations, then a component move preserving all three unrelated nets. A separate Python source candidate declares six concrete vias and ten per-layer Route requests; both build and unchanged-source rebuild pass repeated DRC. Numeric net IDs change, while route IDs/via records and normalized copper persist. This is not internal solver-state or arbitrary topology-edit persistence.

Suggested 60-second narration: show the three-open fixture; explain concrete via sites/net attachments and per-layer routes; show the connected result; show TP4 movement and preserved unrelated copper; explain source-authoritative pose persistence. Then show the historical full-board replay explicitly as incomplete engineering progress.

Top-layer copper is red, bottom-layer copper blue, vias gold. The dark vertical strip is the top-only routing keepout; bottom copper may cross it. Fixture SVGs render measured exported segments, vias and checked 1.2mm pads, not interpolated motion. Four fixed snapshots are displayed side by side; the whole-board video is a 6-second historical replay, not a live optimization.

Full-board009: 310 missing connections, 0 incorrect connections, 44 physical errors, 237 warnings, 7 parity findings; invalid, no final score. Requested layers0/1 do not prove successful multilayer completion:008 selected191nets/942terminals and009 selected7nets/296terminals, both with zero via definitions/instances and bottom-layer warnings. Never call this a routed/qualified product board.

The joint owner's report is included only as attributed existing evidence: its separate fixture improved53→51→49mm with6vias and0opens/violations; its generated-route single-layer capture demo also passed. Their raw workspaces were not accessed or repackaged here. Do not conflate these with the original full-board campaign or claim whole-board capture integration works. This package does not resume the blocked investigation.

Evaluation lessons: bind parent/rules/layers and complete external boundaries; check full obstacles for group moves; require export completion and post-refill DRC; score only qualified candidates; track attempted versus retained values; timeout is not native cancellation; author accepted poses before rebuild; compare per-net geometry with only ID normalization. Route sketches are hints, not an exact legacy-copper transfer mechanism. Source-authored Route/via realization is the demonstrated delivery path; capture repair is not a dependency of this demo.

Audit rechecked stored hashes, source hashes and geometry invariants, without rerouting or repeating already-passed DRC. Evidence includes prior twice-DRC reports and portable KiCad boards/projects. Files contain no runtime caches or credentials. Historical manifests/reports retain provenance paths; presentation links are relative and work offline.

## Original whole-board chronology

Failed attempts show the preceding board; their inherited metrics are deliberately omitted. Unreliable input evaluation is also excluded from the curve.

| Checkpoint | Status | Missing | Physical errors |
|---|---|---:|---:|
''' + table + '\n')
    (dest / 'index.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>JITX — explicit topology, measured routing</title><style>body{margin:0;background:#0a1220;color:#e7edf5;font:17px system-ui;line-height:1.55}main{max-width:1180px;margin:auto;padding:40px 24px}h1{font-size:40px;line-height:1.15}h2{margin-top:40px}.eyebrow{color:#73d6bd;text-transform:uppercase;letter-spacing:.12em;font-size:13px}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}article{border:1px solid #2c3c50;border-radius:12px;padding:18px;background:#111d2d}h3{font-size:17px;margin:0 0 12px}svg{width:100%;display:block}video{width:100%;max-height:660px;background:#000}a{color:#7ec7fa}.scope{border-left:4px solid #dfae65;padding:12px 18px;background:#202334}.muted{color:#aabbd0}@media(max-width:650px){.grid{grid-template-columns:1fr}h1{font-size:30px}}</style><main><p class="eyebrow">Copper Scar · verified JITX evidence</p><h1>Author the topology.<br>Realize and measure the copper.</h1><p>Eight pads. Four nets. Six explicit vias. Ten layer-specific routes.<br>Clean fixture DRC and preservation of unrelated copper through a component move.</p><p class="scope"><strong>Fixture proof, not full-product qualification.</strong> The original 245-component board remains incomplete. Every result below is a completed historical snapshot.</p><div class="grid">''' + ''.join(panels) + '''</div><p class="muted">Red: top copper · Blue: bottom copper · Gold: vias · Dark strip: top-layer keepout. Exact exported geometry; no interpolated motion.</p><h2>Python owns the candidate</h2><p>Declare component poses, via sites/spans/net attachments and per-layer Route endpoints before realization. The source-only build and rebuild both had zero opens and violations. Route/via IDs and copper were preserved, with numeric net IDs resolved by name.</p><p><a href="evidence/source/source_route_fixture.py">Candidate Python</a> · <a href="evidence/source/incremental_fixture/design.py">Exact base fixture</a> · <a href="evidence/source-route-result.json">Source proof result</a></p><h2>Full-board campaign — incomplete</h2><p>15 historical checkpoints, including three failed attempts held on their preceding board and one unreliable evaluation. Best009: <strong>310 missing connections,44 physical errors</strong>. No valid final score.</p><video controls preload="metadata" src="whole-board-incomplete-replay.mp4"></video><p class="muted">6-second accelerated replay. Outer copper only; airwires and inner copper are not displayed. See the evidence table before interpreting progress.</p><h2>Inspect the evidence offline</h2><p><a href="README.md">Narration, caveats and complete evidence table</a> · <a href="evidence/audit.json">Machine-readable audit</a> · <a href="evidence/jitx-source-authored-routing-verification.md">API and persistence report</a></p><p class="muted">No runtime, login or network required. No new native runs were launched for this package.</p></main></html>''')
    files = {str(p.relative_to(dest)): sha(p) for p in sorted(dest.rglob('*')) if p.is_file() and p.name != 'SHA256SUMS.json'}
    (dest / 'SHA256SUMS.json').write_text(json.dumps(files, indent=2) + '\n')
    print(json.dumps({'output': str(dest), 'files': len(files), 'history_entries': len(history)}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path, required=True)
    parser.add_argument('--outputs', type=Path, required=True)
    parser.add_argument('--dest', type=Path, required=True)
    args = parser.parse_args()
    package(args.project, args.outputs, args.dest)
