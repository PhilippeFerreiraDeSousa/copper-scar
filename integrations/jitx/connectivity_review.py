"""Read native KiCad connectivity on an unsaved private board with refilled zones.

Run using KiCad's bundled Python. Source board/project must be disposable copies.
Never saves CAD, routes, changes poses, or modifies rules.
"""
import argparse
import collections
import hashlib
import json
from pathlib import Path
import re

import pcbnew as k
import wx


NETS = ['CAN0_H', 'CAN1_H', 'CAN2_H', 'CAN3_H', 'CAN1_L', 'CAN2_L',
        'GND', 'CH2_D_P', 'CH4_D_P']


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def uid(item):
    return item.m_Uuid.AsString()


def kind(item):
    return {k.PCB_PAD_T: 'PAD', k.PCB_TRACE_T: 'TRACK', k.PCB_VIA_T: 'VIA',
            k.PCB_ARC_T: 'ARC', k.PCB_ZONE_T: 'ZONE'}.get(item.Type(), type(item).__name__)


def describe(item, board):
    result = {'uuid': uid(item), 'type': kind(item), 'net': item.GetNetname(),
              'position_mm': [item.GetPosition().x / 1e6, item.GetPosition().y / 1e6],
              'copper_layers': [board.GetLayerName(n) for n in item.GetLayerSet().Seq()
                                if k.IsCopperLayer(n) and board.GetEnabledLayers().Contains(n)]}
    if isinstance(item, k.PAD):
        result.update(ref=item.GetParentFootprint().GetReference(), pad=item.GetNumber(),
                      size_mm=[item.GetSize().x / 1e6, item.GetSize().y / 1e6],
                      drill_mm=[item.GetDrillSize().x / 1e6, item.GetDrillSize().y / 1e6])
    if kind(item) in ('TRACK', 'ARC'):
        result['start_mm'] = [item.GetStart().x / 1e6, item.GetStart().y / 1e6]
        result['end_mm'] = [item.GetEnd().x / 1e6, item.GetEnd().y / 1e6]
    return result


def run(board_path, drc_path, output):
    app = wx.App(False)
    project_path = board_path.with_suffix('.kicad_pro')
    initial_hashes = {str(p): digest(p) for p in (board_path, project_path)}
    manager = k.GetSettingsManager()
    assert manager.LoadProject(str(project_path))
    board = k.LoadBoard(str(board_path))
    board.SetProject(manager.GetProject(str(project_path)))
    saved_fill = [z.IsFilled() for z in board.Zones()]
    assert k.ZONE_FILLER(board).Fill(board.Zones())
    conn = board.GetConnectivity()
    assert conn.Build(board)
    conn.RecalculateRatsnest()
    drc = json.loads(drc_path.read_text())
    assert conn.GetUnconnectedCount(False) == len(drc['unconnected_items']) == 55
    all_items = [p for f in board.GetFootprints() for p in f.Pads()] + list(board.GetTracks())
    item_by_id = {uid(i): i for i in all_items}
    reports = {}
    for net in NETS:
        members = [i for i in all_items if i.GetNetname() == net]
        seen, islands, membership = set(), [], {}
        for seed in members:
            if uid(seed) in seen:
                continue
            connected = conn.GetConnectedItems(seed)
            # Never merge clusters merely because they return the same ZONE parent:
            # separate polygons within one zone can belong to different clusters.
            copper = {uid(i): i for i in connected if not isinstance(i, k.ZONE)}
            copper.setdefault(uid(seed), seed)
            assert not seen.intersection(copper), 'Overlapping native cluster membership'
            seen.update(copper)
            index = len(islands)
            for identity in copper:
                membership[identity] = index
            pads = [describe(i, board) for i in copper.values() if isinstance(i, k.PAD)]
            counts = collections.Counter(kind(i) for i in copper.values())
            zones = {uid(i): board.GetLayerName(i.GetLayer()) for i in connected if isinstance(i, k.ZONE)}
            islands.append({'index': index, 'item_counts': dict(counts), 'pads': pads,
                            'copper_item_ids': sorted(copper), 'zone_parents': zones,
                            'layers': sorted({n for i in copper.values() for n in describe(i, board)['copper_layers']}),
                            'isolated_single_pad': len(copper) == 1 and len(pads) == 1})
        targets = []
        for island in islands:
            if len(island['copper_item_ids']) <= 5:
                island['small_island_features'] = [describe(item_by_id[i], board)
                                                   for i in island['copper_item_ids']]
            if not island['isolated_single_pad']:
                continue
            pad = item_by_id[island['pads'][0]['uuid']]
            candidates = []
            for other in members:
                if membership[uid(other)] == island['index'] or not other.IsOnLayer(k.F_Cu):
                    continue
                distance = other.GetEffectiveShape(k.F_Cu).Distance(pad.GetPosition()) / 1e6
                candidates.append({'island': membership[uid(other)], 'feature': describe(other, board),
                                   'target_island_has_plane_contact': bool(islands[membership[uid(other)]]['zone_parents']),
                                   'pad_center_to_existing_copper_distance_mm': distance})
            targets.append({'pad': describe(pad, board), 'island': island['index'],
                            'nearest_existing_F_Cu_features': sorted(candidates, key=lambda c: c['pad_center_to_existing_copper_distance_mm'])[:3],
                            'nearest_plane_connected_F_Cu_feature': next(iter(sorted(
                                [c for c in candidates if c['target_island_has_plane_contact']],
                                key=lambda c: c['pad_center_to_existing_copper_distance_mm'])), None),
                            'route_clearance_legality': 'unknown; geometric proximity only, not a collision-tested route'})
        native_pairs = []
        for issue in drc['unconnected_items']:
            if re.search(r'\[([^]]+)\]', issue['items'][0]['description'])[1] != net:
                continue
            ids = [i['uuid'] for i in issue['items']]
            clusters = [membership.get(i) for i in ids]
            assert None not in clusters and clusters[0] != clusters[1]
            native_pairs.append({'items': issue['items'], 'islands': clusters})
        reports[net] = {'islands': islands, 'reported_pairs': native_pairs,
                        'attachment_feature_candidates': targets,
                        'pair_count': len(native_pairs), 'island_count': len(islands),
                        'attempt_status': 'selected by all-net control; per-island attempt/refusal unknown',
                        'new_attachment_legality': 'not established; layers are existing copper access, not a routed solution'}
    # Local foreign-pad geometry at currently isolated connector terminals. This
    # records native shapes and distances, not a proposed route or a DRC judgment.
    local = []
    for net in NETS:
        if net == 'GND':
            continue
        for island in reports[net]['islands']:
            if not island['isolated_single_pad']:
                continue
            pad_info = island['pads'][0]
            if not pad_info['ref'].startswith('J'):
                continue
            pad = item_by_id[pad_info['uuid']]
            shape = pad.GetEffectiveShape(k.F_Cu)
            nearby = []
            for other in pad.GetParentFootprint().Pads():
                if other.GetNetname() == net or not other.IsOnLayer(k.F_Cu):
                    continue
                delta = other.GetPosition() - pad.GetPosition()
                if abs(delta.x) > 2000000 or abs(delta.y) > 2000000:
                    continue
                other_shape = other.GetEffectiveShape(k.F_Cu)
                if not shape.Collide(other_shape, 1000000):
                    continue
                lo, hi = 0, 1000000
                while hi - lo > 1:
                    mid = (hi + lo) // 2
                    if shape.Collide(other_shape, mid):
                        hi = mid
                    else:
                        lo = mid
                nearby.append({'item': describe(other, board), 'edge_distance_mm_approx': hi / 1e6})
            local.append({'terminal': pad_info, 'nearby_foreign_connector_pads': sorted(nearby, key=lambda x: x['edge_distance_mm_approx'])})
    assert all(digest(Path(p)) == expected for p, expected in initial_hashes.items())
    result = {'kicad_version': k.GetBuildVersion(), 'source_hashes': initial_hashes,
              'drc_sha256': digest(drc_path), 'native_open_count_after_memory_refill': 55,
              'zones_filled_on_load': saved_fill, 'zones_filled_in_memory': True,
              'saved_CAD': False, 'routing_performed': False,
              'method': 'GetConnectedItems default flags, native connectivity clusters with zones; enumerate non-zone item seeds, never merge on zone UUID alone',
              'nets': reports, 'connector_terminal_neighbors': local}
    output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({n: {'islands': v['island_count'], 'pairs': v['pair_count'],
                         'isolated_pads': [p['ref']+'.'+p['pad'] for i in v['islands'] if i['isolated_single_pad'] for p in i['pads']]}
                      for n, v in reports.items()}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('board', type=Path)
    parser.add_argument('drc', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    run(args.board, args.drc, args.output)
