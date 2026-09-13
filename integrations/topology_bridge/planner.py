"""Bounded topology proposals for externally supplied placement candidates.

This prototype supports two-terminal nets, front pads, through vias and a known
full-height top barrier. It rejects unsupported scope rather than closing it.
Native routing and exported DRC remain authoritative.
"""
import copy
import hashlib
import json
import math


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def propose(parent, moves, offsets=(1.5, 2.5), lower_layers=(1,)):
    if parent['scope'] != 'complete-two-terminal-barrier-fixture':
        raise ValueError('Unsupported scope; external net boundaries must be retained')
    if not moves or any(ref not in parent['components'] for ref in moves):
        raise ValueError('A mapped placement move is required')
    if any(len(net['ports']) != 2 for net in parent['nets'].values()):
        raise ValueError('Only complete two-terminal nets are supported')
    components = copy.deepcopy(parent['components'])
    for ref, xy in moves.items():
        if len(xy) != 2 or not all(math.isfinite(v) for v in xy):
            raise ValueError('Invalid move')
        components[ref]['xy'] = list(xy)
    affected = sorted(n for n, net in parent['nets'].items() if any(p.split('.')[0] in moves for p in net['ports']))
    result = []
    for offset in offsets:
        if offset < 1.2:
            raise ValueError('Escape site overlaps pad/clearance envelope')
        for layer in lower_layers:
            if layer not in parent['signal_layers'] or layer == 0:
                raise ValueError('Invalid escape layer')
            topology = copy.deepcopy(parent.get('topology', {}))
            for name, net in sorted(parent['nets'].items()):
                if name in topology and name not in affected:
                    continue
                a, b = net['ports']; ax, ay = components[a.split('.')[0]]['xy']; bx, by = components[b.split('.')[0]]['xy']
                key = name.lower()
                if ax * bx > 0:
                    topology[name] = {'vias': {}, 'routes': {key+'_direct': {'source': a, 'destination': b, 'layer': 0}}}
                    continue
                sites = [(ax + math.copysign(offset, bx-ax), ay), (bx + math.copysign(offset, ax-bx), by)]
                if any(abs(x) < parent['barrier_half_width'] + .55 or abs(x) > 15.2 or abs(y) > 13.2 for x, y in sites):
                    raise ValueError('Via site outside feasible barrier/board envelope')
                va, vb = key+'_escape_a', key+'_escape_b'
                topology[name] = {'vias': {va: {'xy': list(sites[0]), 'span': [0, -1], 'net': name, 'port': a}, vb: {'xy': list(sites[1]), 'span': [0, -1], 'net': name, 'port': b}},
                    'routes': {key+'_access_a': {'source': a, 'destination': va, 'layer': 0}, key+'_access_b': {'source': b, 'destination': vb, 'layer': 0}, key+'_cross': {'source': va, 'destination': vb, 'layer': layer}}}
            proposal = {'schema': 'topology-candidate-v1', 'parent_sha256': digest(parent), 'moves': moves,
                        'components': components, 'topology': topology, 'affected_nets': affected,
                        'constraints': parent['constraints'], 'effort': {'build_timeout_s': 360, 'route_sweeps': 0},
                        'choice': {'escape_offset_mm': offset, 'cross_layer': layer}, 'scope': parent['scope']}
            proposal['candidate_sha256'] = digest(proposal)
            result.append(proposal)
    return result


def render(base_source, candidate):
    # Ref/attribute mappings originate in the complete fixture manifest, never eval user text.
    import re
    for ref, c in candidate['components'].items():
        attr = c['attribute']
        if not re.fullmatch('[a-z_]+', attr):
            raise ValueError('Unsafe source mapping')
        base_source, count = re.subn(r'('+re.escape(attr)+r' = Terminal\(\)\.at\()[^)]*\)', lambda m: m[1]+repr(c['xy'][0])+', '+repr(c['xy'][1])+')', base_source)
        if count != 1:
            raise ValueError('Missing/ambiguous source component')
    lines = ['from jitx.circuit import Route', 'from jitx.net import PortAttachment', '', 'class SourceCandidate(ProofCircuit):', '    def __init__(self):']
    def endpoint(key):
        if '.' in key:
            ref, port = key.split('.')
            if port != 'p': raise ValueError('Unsupported pad')
            return 'self.'+candidate['components'][ref]['attribute']+'.p'
        if not re.fullmatch('[a-z_]+', key): raise ValueError('Unsafe key')
        return 'self.'+key
    for net, topology in sorted(candidate['topology'].items()):
        for key, via in sorted(topology['vias'].items()):
            if via['span'] != [0, -1] or via['net'] != net: raise ValueError('Invalid via contract')
            target = endpoint(key)
            lines += [f"        {target} = ProofSubstrate.ThroughVia().at({via['xy'][0]!r}, {via['xy'][1]!r})", f"        {target}_net = PortAttachment({endpoint(via['port'])}, {target})"]
        for key, route in sorted(topology['routes'].items()):
            lines += [f"        {endpoint(key)} = Route({endpoint(route['source'])}, {endpoint(route['destination'])}, {route['layer']!r})"]
    lines += ['', 'class BridgeProof(Design):', '    circuit = SourceCandidate()', '    board = ProofBoard()', '    substrate = ProofSubstrate()', '']
    return base_source+'\n'+'\n'.join(lines)


def fixture_parent():
    attrs = ['hold_left','hold_right','a_left','a_right','b_left','b_right','c_left','c_right']
    xy = [(-12,10),(-7,10),(-8,6),(8,6),(-8,0),(8,0),(-8,-3),(8,-3)]
    return {'scope': 'complete-two-terminal-barrier-fixture', 'components': {f'TP{i+1}': {'attribute': a, 'xy': list(p)} for i,(a,p) in enumerate(zip(attrs,xy))},
            'nets': {n: {'ports': [f'TP{i}.p', f'TP{i+1}.p']} for n,i in [('HOLD',1),('CROSS_A',3),('CROSS_B',5),('CROSS_C',7)]},
            'signal_layers': [0,1], 'barrier_half_width': 1,
            'constraints': {'width_mm': .2, 'clearance_mm': .25, 'via_diameter_mm': .6, 'via_drill_mm': .3}, 'topology': {}}

if __name__ == '__main__':
    import argparse
    from pathlib import Path
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('parent',type=Path);parser.add_argument('moves',type=Path);parser.add_argument('output',type=Path)
    args=parser.parse_args();args.output.mkdir(parents=True,exist_ok=False)
    for i,candidate in enumerate(propose(json.loads(args.parent.read_text()),json.loads(args.moves.read_text()))):
        (args.output/f'candidate-{i:02}.json').write_text(json.dumps(candidate,indent=2))
