"""File contract for the explicitly qualified eight-pad fixture; no generic planner."""
from pathlib import Path
import hashlib
import json
import math
import sexpdata as sx
from verify_incremental_fixture import children, one, without_ids, EXPECTED

FRAME = {'units': 'mm', 'coordinates': 'KiCad global, X right, Y down',
         'angle': 'degrees', 'native_transform': {'x_offset': 139.5, 'y_offset': 108.0, 'reflect_y': True}}
FIXED = ['TP1', 'TP2', 'TP3', 'TP5', 'TP6', 'TP7', 'TP8']

def require(condition, reason):
    if not condition:
        raise ValueError(reason)

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest()

def read(path):
    return json.loads(Path(path).read_text())

def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as stream:
        stream.write(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + '\n')

def pcb(stage):
    files = list((Path(stage) / 'export').glob('*.kicad_pcb'))
    require(len(files) == 1, 'one exported board required')
    return files[0]

def state_sha(path):
    # Export regenerates UUIDs and reorders top-level records. Keep every
    # non-ID field and record multiplicity; never sort polygon/path vertices.
    board=without_ids(sx.loads(Path(path).read_text()))
    return digest([str(board[0]), sorted(sx.dumps(v) for v in board[1:])])

def inventory(path):
    board = sx.loads(Path(path).read_text())
    refs = {}
    for f in children(board, 'footprint'):
        ref = next(str(t[2]) for t in children(f, 'fp_text') if str(t[1]) == 'reference')
        require(ref not in refs, 'duplicate reference')
        at = one(f, 'at')[1:]
        pads = []
        for p in children(f, 'pad'):
            geom = without_ids(p)
            geom = [v for v in geom if not (isinstance(v, list) and str(v[0]) == 'net')]
            pads.append({'name': str(p[1]), 'net': str(one(p, 'net')[2]), 'geometry': sx.dumps(geom)})
        refs[ref] = {'pose': [float(at[0]), float(at[1]), float(at[2]) if len(at)>2 else 0.0],
                     'side': str(one(f, 'layer')[1]), 'pads': sorted(pads, key=lambda p: p['name'])}
    static = [v for v in board if isinstance(v, list) and str(v[0]) in
              {'layers', 'setup', 'gr_line', 'gr_arc', 'gr_rect', 'gr_poly', 'zone'}]
    return {'refs': refs, 'static_geometry_sha256': digest(sx.dumps(without_ids(static)))}

def qualify(inv):
    require(set(inv['refs']) == set().union(*EXPECTED.values()), 'fixture references differ')
    for net, refs in EXPECTED.items():
        for ref in refs:
            r = inv['refs'][ref]
            require(r['side'] == 'F.Cu' and r['pose'][2] == 0, 'unsupported side or rotation')
            require(len(r['pads']) == 1 and r['pads'][0]['name'] == 'p' and r['pads'][0]['net'] == net,
                    'pad membership differs')

def validate_request(request, parent, source):
    require(request['schema'] == 'copperhead-jitx-fixture-pose-v1', 'unsupported schema')
    require(request['frame'] == FRAME, 'unsupported coordinate frame')
    require(request['fixed_refs'] == FIXED, 'fixed references differ')
    require(request['target'] == {'ref': 'TP4', 'pose': [149.5, 100.0, 0.0], 'side': 'F.Cu'}, 'unsupported fixture target')
    require(request['copper_policy'] == {'preserve_exactly': ['CROSS_B', 'CROSS_C', 'HOLD'], 'may_change': ['CROSS_A']}, 'copper policy differs')
    path = pcb(parent)
    require(sha(path) == request['parent']['board_sha256'], 'stale parent board')
    require(sha(path.with_suffix('.kicad_pro')) == request['parent']['project_sha256'], 'parent rules changed')
    require(sha(source) == request['parent']['source_sha256'], 'source constraints changed')
    require(state_sha(path) == request['parent']['state_sha256'], 'parent state differs')
    inv = inventory(path)
    qualify(inv)
    require(inv == request['inventory'], 'invalid reference/pad/geometry mapping')
    require(inv['refs']['TP4']['pose'] == [147.5, 102.0, 0.0], 'unsupported parent pose')
    require(request['net_memberships'] == {n: [r+'.p' for r in sorted(rs)] for n,rs in EXPECTED.items()}, 'net scope differs')
    return inv

def coverage(path):
    """Conservative endpoint graph from actual exported segments, pads and vias.

    Valid only for this endpoint-connected fixture: refuses arcs/zones. It may
    reject a connected general board with mid-segment junctions; never uses the
    native router's preliminary connected groups to infer realized topology.
    """
    b = sx.loads(Path(path).read_text()); inv = inventory(path); qualify(inv)
    require(not children(b, 'arc'), 'fixture graph does not support arcs')
    require(all(children(z, 'keepout') for z in children(b,'zone')), 'fixture graph does not support filled copper')
    nets = {int(n[1]): str(n[2]) for n in children(b,'net')}
    result = {}
    for net, refs in EXPECTED.items():
        points=[]; links=[]; terminals={}; layers=set(); segments=0; vias=0
        def point(x,y,l):
            for i,(a,c,d) in enumerate(points):
                if d==l and math.hypot(a-x,c-y) < 1e-5:return i
            points.append((x,y,l)); return len(points)-1
        for ref in sorted(refs):
            x,y,_=inv['refs'][ref]['pose'];terminals[ref+'.p']=point(x,y,'F.Cu')
        for s in children(b,'segment'):
            if nets[int(one(s,'net')[1])]!=net:continue
            layer=str(one(s,'layer')[1]); layers.add(layer); segments+=1
            links.append((point(*map(float,one(s,'start')[1:]),layer), point(*map(float,one(s,'end')[1:]),layer)))
        for v in children(b,'via'):
            if nets[int(one(v,'net')[1])]!=net:continue
            x,y=map(float,one(v,'at')[1:]); vias+=1
            require(list(map(str,one(v,'layers')[1:]))==['F.Cu','B.Cu'], 'unsupported via span')
            links.append((point(x,y,'F.Cu'),point(x,y,'B.Cu')))
        parent=list(range(len(points)))
        def root(i):
            while parent[i]!=i:i=parent[i]
            return i
        for a,c in links:parent[root(a)]=root(c)
        islands={root(i) for i in terminals.values()}
        all_islands={root(i) for i in range(len(points))}
        result[net]={'terminals':sorted(terminals),'terminal_islands':len(islands),
                     'all_copper_islands':len(all_islands), 'realized':len(islands)==1 and len(all_islands)==1,
                     'segments':segments,'vias':vias,'layers':sorted(layers)}
    return result
