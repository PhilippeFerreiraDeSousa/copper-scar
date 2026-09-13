"""Independent exported-fixture gates; copies and metadata normalization only."""
from pathlib import Path
import argparse
import collections
import hashlib
import json
import shutil
import subprocess
import uuid
import sexpdata as sx

KC = '/Users/philippe/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli'
EXPECTED = {'HOLD': {'TP1', 'TP2'}, 'CROSS_A': {'TP3', 'TP4'},
            'CROSS_B': {'TP5', 'TP6'}, 'CROSS_C': {'TP7', 'TP8'}}


def children(tree, name):
    return [v for v in tree if isinstance(v, list) and v and str(v[0]) == name]


def one(tree, name):
    return children(tree, name)[0]


def without_ids(tree):
    if not isinstance(tree, list):
        return tree
    return [without_ids(v) for v in tree if not (isinstance(v, list) and v and str(v[0]) in {'uuid', 'tstamp'})]


def check(stage):
    output = stage / 'independent'
    output.mkdir(exist_ok=True)
    source = next((stage / 'export').glob('*.kicad_pcb'))
    board = sx.loads(source.read_text())
    original_geometry = without_ids(board)
    # Legacy embedded netclasses can override modern project rules. Normalize an
    # external evaluation copy, and verify all physical geometry stays identical.
    board[:] = [v for v in board if not (isinstance(v, list) and v and str(v[0]) == 'net_class')]
    original_geometry[:] = [v for v in original_geometry if not (isinstance(v, list) and v and str(v[0]) == 'net_class')]
    seen = set()
    duplicate_count = 0

    def unique(tree, path=''):
        nonlocal duplicate_count
        if not isinstance(tree, list):
            return
        if tree and str(tree[0]) in {'uuid', 'tstamp'}:
            value = str(tree[1])
            if value in seen:
                duplicate_count += 1
                tree[1] = sx.Symbol(str(uuid.uuid5(uuid.NAMESPACE_URL, 'incremental-fixture/' + path + '/' + value)))
            seen.add(str(tree[1]))
        for i, value in enumerate(tree):
            unique(value, path + '/' + str(i))
    unique(board)
    assert original_geometry == without_ids(board)
    for path in (stage / 'export').iterdir():
        if path.is_file() and path.suffix != '.kicad_pcb':
            shutil.copy2(path, output / path.name)
        elif path.is_dir():
            shutil.copytree(path, output / path.name, dirs_exist_ok=True)
    pcb = output / source.name
    pcb.write_text(sx.dumps(board))
    project = json.loads(pcb.with_suffix('.kicad_pro').read_text())
    rules = project['board']['design_settings']['rules']
    for key, floor in {'min_clearance': .25, 'min_track_width': .2, 'min_via_annular_width': .15,
                       'min_hole_clearance': .28, 'min_copper_edge_clearance': .5}.items():
        assert rules[key] >= floor
    nets = {int(v[1]): str(v[2]) for v in children(board, 'net')}
    members = collections.defaultdict(set)
    poses = {}
    for footprint in children(board, 'footprint'):
        ref = next(str(t[2]) for t in children(footprint, 'fp_text') if str(t[1]) == 'reference')
        assert ref not in poses
        poses[ref] = one(footprint, 'at')[1:]
        pads = children(footprint, 'pad')
        assert len(pads) == 1 and str(pads[0][1]) == 'p'
        assert list(map(str, one(pads[0], 'layers')[1:])) == ['F.Cu']
        members[nets[int(one(pads[0], 'net')[1])]].add(ref)
    assert dict(members) == EXPECTED
    vias = children(board, 'via')
    for via in vias:
        assert abs(float(one(via, 'size')[1]) - .6) < 1e-9
        assert abs(float(one(via, 'drill')[1]) - .3) < 1e-9
        assert list(map(str, one(via, 'layers')[1:])) == ['F.Cu', 'B.Cu']
    copper = collections.defaultdict(list)
    for kind in ('segment', 'arc', 'via'):
        for item in children(board, kind):
            net = nets[int(one(item, 'net')[1])]
            canonical = without_ids(item)
            one(canonical, 'net')[1] = net
            copper[net].append(sx.dumps(canonical))
    signatures = {n: sorted(items) for n, items in copper.items()}
    counts = []
    for i in range(2):
        report = output / f'drc-{i}.json'
        result = subprocess.run([KC, 'pcb', 'drc', '--format', 'json', '--output', str(report), str(pcb)],
                                capture_output=True, text=True, timeout=60, check=True)
        drc = json.loads(report.read_text())
        counts.append({'opens': len(drc['unconnected_items']),
                       'violations': sorted(collections.Counter((v['type'], v['severity']) for v in drc['violations']).items())})
    assert counts[0] == counts[1], 'Repeated independent DRC disagreed'
    result = {'stage': stage.name, 'source_board_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
              'normalized_board_sha256': hashlib.sha256(pcb.read_bytes()).hexdigest(),
              'project_sha256': hashlib.sha256(pcb.with_suffix('.kicad_pro').read_bytes()).hexdigest(),
              'geometry_unchanged': True, 'duplicate_ids_reassigned': duplicate_count,
              'all_four_net_memberships_correct': True, 'component_count': len(poses), 'via_count': len(vias),
              'copper_layers_used': sorted({str(one(s, 'layer')[1]) for s in children(board, 'segment')}),
              'through_via_geometry_legal': True, 'repeated_drc_agrees': True, **counts[0],
              'poses': poses, 'copper_by_net': signatures}
    (output / 'summary.json').write_text(json.dumps(result, indent=2))
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path)
    args = parser.parse_args()
    names = ['01-definition-only-sweep', '03-multilayer-routed', '04-moved', '05-reloaded']
    stages = [check(args.root / name) for name in names]
    assert stages[0]['opens'] == 3 and stages[0]['via_count'] == 0
    for s in stages:
        assert s['violations'] == []
    for s in stages[1:]:
        assert s['opens'] == 0 and s['via_count'] == 6
        assert s['copper_layers_used'] == ['B.Cu', 'F.Cu']
    before, moved, reloaded = stages[1:]
    assert [r for r in before['poses'] if before['poses'][r] != moved['poses'][r]] == ['TP4']
    for net in ('HOLD', 'CROSS_B', 'CROSS_C'):
        assert before['copper_by_net'][net] == moved['copper_by_net'][net]
    assert before['copper_by_net']['CROSS_A'] != moved['copper_by_net']['CROSS_A']
    report = {'fixture_incremental_proof_passed': True, 'whole_product_board_qualified': False,
              'stages': [{k: v for k, v in s.items() if k not in ('poses', 'copper_by_net')} for s in stages],
              'placement_change': 'TP4 only; native a_right (8,6) to (10,8)',
              'unrelated_copper_preserved_exactly': ['HOLD', 'CROSS_B', 'CROSS_C'],
              'unchanged_source_reload_preserved_moved_poses_and_all_copper':
                  moved['poses'] == reloaded['poses'] and moved['copper_by_net'] == reloaded['copper_by_net'],
              'reload_changed_pose_refs': [r for r in moved['poses'] if moved['poses'][r] != reloaded['poses'][r]],
              'reload_changed_copper_nets': [n for n in moved['copper_by_net'] if moved['copper_by_net'][n] != reloaded['copper_by_net'][n]],
              'reload_limit': 'Source placement is authoritative: unchanged source reload resets the interactive TP4 pose. Preserve accepted poses in authored source before any rebuild.'}
    updated_stage = args.root / '07-source-updated-reload'
    if updated_stage.exists():
        source_before = check(args.root / '06-moved-before-source-update')
        source_after = check(updated_stage)
        assert source_before['poses'] == source_after['poses']
        assert source_before['copper_by_net'] == source_after['copper_by_net']
        assert source_after['opens'] == 0 and source_after['violations'] == [] and source_after['via_count'] == 6
        native = json.loads((updated_stage / 'final.json').read_text())
        native_board = next(m['body'] for m in native if m['type'] == 'board')
        assert {v['name'] for v in native_board['vias']} == {'Proof through via 0.60-0.30', 'Proof through via 0.80-0.40'}
        report['source_update_reload'] = {'legal_definition_added': True, 'accepted_pose_authored_in_source': True,
            'moved_poses_preserved': True, 'all_copper_preserved': True, 'existing_via_instances_preserved': 6,
            'drc_opens': 0, 'drc_violations': [],
            'project_rules_unchanged': source_before['project_sha256'] == source_after['project_sha256'],
            'source_board_sha256': source_after['source_board_sha256']}
    (args.root / 'proof-result.json').write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))
