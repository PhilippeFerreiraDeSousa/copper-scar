"""Layer-aware original-interface audit; produces a fail-closed trial gate."""
from pathlib import Path
import argparse
import collections
import hashlib
import json
import math
import re
from shapely.geometry import Polygon
from shapely.ops import unary_union

REFS=('R37','R42','J2','U3')
HOLES=('J1','J3','J5','J6','J7','J8')
GATES={'complete_named_interface_mapping','same_full_parent_state','same_layer_profile','full_obstacle_context_on_probe','representation_differences_qualified'}

def read(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def require(v,s):
    if not v:raise ValueError(s)
def union(polygons):return unary_union([Polygon(p) for p in polygons if len(p)>=3])
def layer(f,label):
    # Drills remove all nominal copper from these zero-annulus NPTH pads.
    parts=[g for p in f['pads'] if not(label.endswith('.Cu') and p['name']=='' and p['drill']==p['size'])
           for g in p.get('polygons',{}).get(label,[])]+f['graphics'].get(label,[])
    return union(parts)
def difference(a,b,hausdorff=True):
    return {'symmetric_difference_mm2':a.symmetric_difference(b).area,
            'hausdorff_mm':(0.0 if a.is_empty and b.is_empty else a.hausdorff_distance(b) if not a.is_empty and not b.is_empty else None) if hausdorff else None,
            'exact_native_polygon_union':a.equals(b)}

def verify_request(request,observed):
    require(request['parent_board_sha256']==observed['parent_board_sha256'],'stale parent')
    require(request['parent_project_sha256']==observed['parent_project_sha256'],'constraints mismatch')
    require(request['inventory_sha256']==observed['inventory_sha256'],'mapping mismatch')
    require(request['boundaries_sha256']==observed['boundaries_sha256'],'external boundary mismatch')
    return True

def trial_gate(request,observed,gates):
    verify_request(request,observed)
    require(set(gates)==GATES and all(type(v) is bool for v in gates.values()),'incomplete or invalid qualification gates')
    failed=[name for name,passed in gates.items() if not passed]
    return {'may_mutate':not failed,'decision':'qualified' if not failed else 'reject_before_mutation','failed_gates':failed,
            'routing_mode':'single-layer proxy permitted only after geometry/parent/constraints qualification',
            'generic_multilayer_planner_is_a_gate':False}

def audit(root,parent,jitx,native_checkpoint,output):
    output.mkdir(parents=True,exist_ok=False)
    inventories=root/'physical-inventories'
    original=read(inventories/'copperhead-native.json');accepted=read(inventories/'jitx-native.json')
    before=read(inventories/'before-native-normalized.json');after=read(inventories/'corrected-native-normalized.json')
    require(original['board_sha256']==sha(parent/'pcbgolf.kicad_pcb'),'parent changed during audit')
    require(accepted['board_sha256']==sha(jitx/'pcbgolf.kicad_pcb'),'JITX checkpoint changed during audit')
    prep=read(root/'probe-corrected/preparation.json');metrics={}
    for ref in REFS:
        a,b,c,d=[v['footprints'][ref] for v in (original,accepted,before,after)]
        expected={p['name']:p['net'] for p in a['pads']}
        require(all({p['name']:p['net'] for p in f['pads']}==expected for f in (b,c,d)),'pad/net mismatch '+ref)
        metrics[ref]={'pads':len(a['pads']),'local_pad_centers_exact':all(next(q for q in b['pads'] if q['name']==p['name'])['at']==p['at'] for p in a['pads']),
                     'layers':{l:difference(layer(a,l),layer(b,l),ref!='U3') for l in ('F.Cu','F.Mask','B.Mask','F.Paste')},
                     'correction_preserves_copper':layer(c,'F.Cu').equals(layer(d,'F.Cu')),
                     'correction_preserves_paste':layer(c,'F.Paste').equals(layer(d,'F.Paste')),
                     'correction_preserves_pose':c['pose']==d['pose']}
        metrics[ref]['body_and_obstacle_layers']={l:difference(layer(a,l),layer(b,l)) for l in ('F.CrtYd','F.Fab','F.SilkS')}
        if ref!='U3':metrics[ref]['corrected_mask']=difference(layer(a,'F.Mask'),layer(d,'F.Mask'))
        else:
            p=next(p for p in a['pads'] if p['name']=='114');q=next(p for p in b['pads'] if p['name']=='114')
            metrics[ref]['pad114_corner_difference']=difference(union(p['polygons']['F.Cu']),union(q['polygons']['F.Cu']))
    holes=[]
    for ref in HOLES:
        a=original['footprints'][ref];b=accepted['footprints'][ref]
        orig=[p for p in a['pads'] if p['name']==''];target=[p for p in b['pads'] if p['name']=='']
        require(len(orig)==2 and len(target)==4,'unexpected hole representation')
        for p in orig:
            require(p['drill']==p['size'] and p['drill'][0]==p['drill'][1], 'noncircular/annular source hole')
            matches=[q for q in target if q['at'][:2]==p['at'][:2] and q['size']==p['size']]
            drills=[q for q in matches if q['drill']==p['drill']]
            masks=[q for q in matches if q['drill']==[0,0]]
            require(len(drills)==len(masks)==1,'drill/mask mapping not one-to-one')
            require(all(not l.endswith('.Cu') for q in matches for l in q['layers']),'unexpected copper on unnumbered export pad')
            row={'ref':ref,'local_center':p['at'][:2],'diameter':p['drill'][0],'one_physical_drill':True,'extra_is_mask_only':True,'mask_unions':{}}
            for label in ('F.Mask','B.Mask'):
                row['mask_unions'][label]=difference(union(p['polygons'][label]),union([g for q in matches for g in q['polygons'][label]]),False)
            holes.append(row)
    # Every external endpoint on every touched net remains explicit, not just CMD.
    boundary=prep['boundaries'];require(boundary['Net-(J2-CMD)']['included']==['J2.3','R37.2','R42.2'],'CMD partition differs')
    require(boundary['SD_CMD']['included']==['R42.1','U3.114'],'SD_CMD partition differs')
    parent_project=read(parent/'pcbgolf.kicad_pro');jitx_project=read(jitx/'pcbgolf.kicad_pro')
    repairs=read(parent/'footprint-repairs.json')['changes'];changed={(x['ref'],str(x['pad'])) for x in repairs if 'pad'in x}
    errors=[v for v in read(jitx/'drc.json')['violations'] if v['severity']=='error'];matched=[]
    for v in errors:
        pads=[]
        for item in v['items']:
            match=re.search(r'pad (\S+) .*?of (\w+)',item['description'],re.I)
            if match:pads.append(tuple(reversed(match.groups())))
        matched.append({'type':v['type'],'pads':pads,'touches_parent_repaired_pad':bool(set(pads)&changed)})
    messages=read(native_checkpoint);native_board=next(m['body'] for m in messages if m['type']=='board')
    groups={g['id']:dict(g) for g in native_board['module']['groups']}
    for m in messages:
        if m['type']=='placements':
            for g in m['body']['groups']:groups[g['id']].update(g)
    transforms={}
    for g in groups.values():
        for i in g.get('instances',[]):
            ref=i['designator']
            if ref in REFS:
                x,y,_=accepted['footprints'][ref]['pose'];n=g['pose']['center']
                transforms[ref]={'group_id':g['id'],'native_center':n,'accepted_export_pose':accepted['footprints'][ref]['pose'],
                                 'offset_x':x-n['x'],'offset_y':y+n['y'],'retained_parent_pose':original['footprints'][ref]['pose']}
    offsets=[(round(t['offset_x'],6),round(t['offset_y'],6)) for t in transforms.values()]
    require(len(set(offsets))==1,'no common native/export transform')
    features={r:{'pads':original['footprints'][r]['pads'],'pose':original['footprints'][r]['pose']} for r in REFS}
    observed={'parent_board_sha256':sha(parent/'pcbgolf.kicad_pcb'),'parent_project_sha256':sha(parent/'pcbgolf.kicad_pro'),
              'inventory_sha256':digest(features),'boundaries_sha256':digest(boundary)}
    gates={'complete_named_interface_mapping':True,'same_full_parent_state':original['board_sha256']==accepted['board_sha256'],
           'same_layer_profile':original['copper_layers']==accepted['copper_layers'],
           'full_obstacle_context_on_probe':len(after['footprints'])==len(original['footprints']),
           'representation_differences_qualified':all(m['layers']['F.Cu']['exact_native_polygon_union'] and
              m.get('corrected_mask',m['layers']['F.Mask'])['exact_native_polygon_union'] for m in metrics.values())}
    result={'scope':'original-board interface geometry qualification; no placement/routing trial',
            'request':observed,'parent_path':str(parent),'jitx_checkpoint_path':str(jitx),'jitx_board_sha256':accepted['board_sha256'],
            'interface':metrics,'unnamed_holes':holes,'complete_boundary_manifest':boundary,
            'boundary_summary':{'touched_nets':len(boundary),'externally_open_nets':sum(bool(v['external']) for v in boundary.values()),
                                'external_pad_memberships':sum(len(v['external']) for v in boundary.values()),'included_physical_pads':160,'omitted_footprints':len(prep['omitted_board_obstacles'])},
            'coordinate_correspondence':transforms,'layer_profiles':{'copperhead':original['copper_layers'],'jitx':accepted['copper_layers']},
            'via_definitions_on_accepted_native':native_board['vias'],
            'rules':{'retained_parent_rules':parent_project['board']['design_settings']['rules'],
                     'retained_parent_netclasses':parent_project['net_settings']['classes'],
                     'jitx_export_rules':jitx_project['board']['design_settings']['rules'],
                     'project_bytes_equal':sha(parent/'pcbgolf.kicad_pro')==sha(jitx/'pcbgolf.kicad_pro'),
                     'six_layer_assumptions':read(parent/'six-layer-assumptions.json')},
            'accepted_jitx_errors':{'count':len(errors),'involving_retained_parent_repaired_pad':sum(v['touches_parent_repaired_pad'] for v in matched),'details':matched},
            'source_correction':prep['changes'],'gates':gates,'trial_gate':trial_gate(observed,observed,gates),
            'candidate_architecture':'Future candidate must bind authored component poses, concrete via sites/spans/net attachments and feature-to-feature route intent; native per-layer routing realizes it. Not implemented by this geometry audit.',
            'native_routing_started':False}
    (output/'qualification.json').write_text(json.dumps(result,indent=2,allow_nan=False));(output/'request.json').write_text(json.dumps(observed,indent=2))
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ('root','parent','jitx','native-checkpoint','output'):p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();r=audit(a.root,a.parent,a.jitx,a.native_checkpoint,a.output);print(r['trial_gate'])
