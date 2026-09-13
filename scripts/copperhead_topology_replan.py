"""Apply a source-bound, declared-only ripup and explicit via hypothesis."""
import argparse,hashlib,json
from pathlib import Path
import pcbnew as p

def geometry(item,board):
    row=dict(uuid=item.m_Uuid.AsString(),net=item.GetNetname(),type='via' if isinstance(item,p.PCB_VIA) else 'track')
    if isinstance(item,p.PCB_VIA):
        row.update(position_nm=[item.GetPosition().x,item.GetPosition().y],diameter_nm=item.GetWidth(p.F_Cu),drill_nm=item.GetDrillValue(),span=[board.GetLayerName(item.TopLayer()),board.GetLayerName(item.BottomLayer())])
        row['diameters_by_layer_nm']={board.GetLayerName(layer):item.GetWidth(layer) for layer in board.GetEnabledLayers().Seq() if p.IsCopperLayer(layer) and item.IsOnLayer(layer)}
    else:
        row.update(start_nm=[item.GetStart().x,item.GetStart().y],end_nm=[item.GetEnd().x,item.GetEnd().y],width_nm=item.GetWidth(),layer=board.GetLayerName(item.GetLayer()))
        if item.GetClass()=='PCB_ARC':row['mid_nm']=[item.GetMid().x,item.GetMid().y]
    return row

def validate_track_declaration(item,row,board):
    assert item.GetClass()=='PCB_TRACK' and row['kind']=='TRACK'
    assert row['uuid']==item.m_Uuid.AsString() and row['net']==item.GetNetname()
    assert row['layers']==[board.GetLayerName(item.GetLayer())]
    for field,point in [('start_mm',item.GetStart()),('end_mm',item.GetEnd()),('position_mm',item.GetPosition())]:assert list(map(p.FromMM,row[field]))==[point.x,point.y]
    assert p.FromMM(row['width_mm'])==item.GetWidth()

ap=argparse.ArgumentParser();ap.add_argument('folder',type=Path);ap.add_argument('--proposal',type=Path,required=True);a=ap.parse_args()
folder=a.folder.resolve();path=folder/'pcbgolf.kicad_pcb';cfg=json.loads(a.proposal.read_text())
assert cfg['kind']=='local_topology_replan'
assert hashlib.sha256(path.read_bytes()).hexdigest()==cfg['parent_board_sha256'],'Stale topology parent'
options=json.loads((folder/'routing-options.json').read_text())
context=dict(schema_version='effective-via-rules-v1',constraint_scope=options['constraint_scope'],allowed_via_options=sorted(set(options['allowed_via_options'])))
assert cfg['realization_context_digest']==hashlib.sha256(json.dumps(context,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'Wrong or missing recipe'
removals=cfg['remove_items'];sites=cfg['via_sites']
assert 1<=len(removals)<=8 and 1<=len(sites)<=8
assert len({x['uuid'] for x in removals})==len(removals)
project=folder/'pcbgolf.kicad_pro';project_hash=hashlib.sha256(project.read_bytes()).hexdigest()
rules=json.loads(project.read_text())['board']['design_settings']['rules']
manager=p.SETTINGS_MANAGER();manager.LoadProject(str(project));board=p.LoadBoard(str(path));board.SetProject(manager.GetProject(str(project)))
tracks={t.m_Uuid.AsString():t for t in board.GetTracks()};original={uid:geometry(t,board) for uid,t in tracks.items()}
pads={q.m_Uuid.AsString():q for f in board.GetFootprints() for q in f.Pads()}
assert p.ZONE_FILLER(board).Fill(board.Zones());connectivity=board.GetConnectivity();connectivity.Build(board);connectivity.RecalculateRatsnest()
deleted=[]
for row in removals:
    item=tracks[row['uuid']];assert item.GetNetname()==row['net'] and row['net'] in cfg['nets']
    if 'geometry' in row:assert original[row['uuid']]==row['geometry'],'Declared removal geometry differs'
    else:validate_track_declaration(item,row['source_geometry'],board)
    deleted.append(original[row['uuid']])
assert {x['net'] for x in removals+sites}==set(cfg['nets'])
# Bind sites to native input pads or retained track anchors before any mutation.
for site in sites:
    assert (site['diameter_mm'],site['drill_mm']) in ((.45,.2),(.6,.3)) and site['span']==['F.Cu','B.Cu']
    assert rules['min_via_diameter']<=site['diameter_mm'] and rules['min_through_hole_diameter']<=site['drill_mm'] and rules['min_via_annular_width']<=(site['diameter_mm']-site['drill_mm'])/2
    if site.get('target_pad_uuid'):
        pad=pads[site['target_pad_uuid']];assert pad.GetNetname()==site['net']
        assert [round(p.ToMM(pad.GetPosition().x),6),round(p.ToMM(pad.GetPosition().y),6)]==site['target_pad_position_mm']
    if site.get('target_track_uuid'):
        anchor=tracks[site['target_track_uuid']];assert anchor.GetNetname()==site['net'] and site['target_track_uuid'] not in {x['uuid'] for x in removals}
        validate_track_declaration(anchor,site['target_track_geometry'],board)
        assert site['target_layer']==board.GetLayerName(anchor.GetLayer())
        actual_island={x.m_Uuid.AsString() for x in connectivity.GetConnectedItems(anchor) if isinstance(x,(p.PAD,p.PCB_TRACK))}|{anchor.m_Uuid.AsString()}
        assert actual_island==set(site['expected_original_island_item_uuids']),'Original anchor island differs'
        assert anchor.GetClass()=='PCB_TRACK','Only straight retained track anchors supported'
        x,y=map(p.FromMM,site['position_mm']);start=anchor.GetStart();end=anchor.GetEnd();dx=end.x-start.x;dy=end.y-start.y
        assert dx*dx+dy*dy>0
        t=((x-start.x)*dx+(y-start.y)*dy)/(dx*dx+dy*dy)
        assert 0<=t<=1 and ((x-start.x-t*dx)**2+(y-start.y-t*dy)**2)**.5<=anchor.GetWidth()/2,'Via does not intersect declared retained anchor'
    assert site.get('target_pad_uuid') or site.get('target_track_uuid'),'Explicit native target required'
for row in removals:board.Delete(tracks[row['uuid']])
created=[];nets=board.GetNetsByName()
for site in sites:
    via=p.PCB_VIA(board);via.SetViaType(p.VIATYPE_THROUGH);via.SetLayerPair(p.F_Cu,p.B_Cu);via.SetWidth(p.FromMM(site['diameter_mm']));via.SetDrill(p.FromMM(site['drill_mm']));via.SetPosition(p.VECTOR2I(p.FromMM(site['position_mm'][0]),p.FromMM(site['position_mm'][1])));via.SetNetCode(nets[site['net']].GetNetCode());via.SetIsFree(True);board.Add(via)
    created.append(geometry(via,board))
assert p.ZONE_FILLER(board).Fill(board.Zones());p.SaveBoard(str(path),board)
reloaded=p.LoadBoard(str(path));actual={x.m_Uuid.AsString():geometry(x,reloaded) for x in reloaded.GetTracks()}
expected={uid:row for uid,row in original.items() if uid not in {x['uuid'] for x in removals}}
expected.update({x['uuid']:x for x in created});assert actual==expected,'Undeclared copper change during save/reload'
for item in reloaded.GetTracks():
    if item.m_Uuid.AsString() in {x['uuid'] for x in created}:assert item.GetIsFree()
assert hashlib.sha256(project.read_bytes()).hexdigest()==project_hash
result=dict(parent_board_sha256=cfg['parent_board_sha256'],board_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),removed=deleted,created_vias=created,generated_tracks=0,undeclared_copper_preserved=True,save_reload_verified=True,original_project_preserved=True,qualification='Intentional disconnected trial; native preflight and full original pad-group restoration required.')
(folder/'topology-replan.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
