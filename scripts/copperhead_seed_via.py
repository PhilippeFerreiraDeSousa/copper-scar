"""Realize one explicit, net-assigned through-via site; generate no trace path."""
import argparse,hashlib,json
from pathlib import Path
import pcbnew as p

ap=argparse.ArgumentParser();ap.add_argument('folder',type=Path);ap.add_argument('--proposal',type=Path,required=True);a=ap.parse_args()
folder=a.folder.resolve();path=folder/'pcbgolf.kicad_pcb';cfg=json.loads(a.proposal.read_text())
assert hashlib.sha256(path.read_bytes()).hexdigest()==cfg['parent_board_sha256'],'Stale via-site parent'
seeds=cfg['via_sites'];assert len(seeds)==1,'One bounded via-site hypothesis per trial'
project=folder/'pcbgolf.kicad_pro';rules=json.loads(project.read_text())['board']['design_settings']['rules']
manager=p.SETTINGS_MANAGER();manager.LoadProject(str(project));board=p.LoadBoard(str(path));board.SetProject(manager.GetProject(str(project)))
nets=board.GetNetsByName();original={item.m_Uuid.AsString() for item in board.GetTracks()};created=[]
for site in seeds:
 assert site['net']==cfg['net'] and site['diameter_mm']==.45 and site['drill_mm']==.2 and site['span']==['F.Cu','B.Cu']
 assert rules['min_via_diameter']<=.45 and rules['min_through_hole_diameter']<=.2 and rules['min_via_annular_width']<=.125
 matches=[pad for footprint in board.GetFootprints() for pad in footprint.Pads() if pad.m_Uuid.AsString()==site['target_pad_uuid']]
 assert len(matches)==1 and matches[0].GetNetname()==site['net'],'Target pad identity/net mismatch'
 pad=matches[0];assert [round(p.ToMM(pad.GetPosition().x),6),round(p.ToMM(pad.GetPosition().y),6)]==site['target_pad_position_mm'],'Target pad moved since site proposal'
 via=p.PCB_VIA(board);via.SetViaType(p.VIATYPE_THROUGH);via.SetLayerPair(p.F_Cu,p.B_Cu);via.SetWidth(p.FromMM(.45));via.SetDrill(p.FromMM(.2));via.SetPosition(p.VECTOR2I(p.FromMM(site['position_mm'][0]),p.FromMM(site['position_mm'][1])));via.SetNetCode(nets[site['net']].GetNetCode());via.SetIsFree(True);board.Add(via)
 created.append(dict(**site,uuid=via.m_Uuid.AsString()))
assert original<={item.m_Uuid.AsString() for item in board.GetTracks()} and len(board.GetTracks())==len(original)+1
assert p.ZONE_FILLER(board).Fill(board.Zones());p.SaveBoard(str(path),board)
reloaded=p.LoadBoard(str(path));by_uuid={item.m_Uuid.AsString():item for item in reloaded.GetTracks()}
for item in created:
 via=by_uuid[item['uuid']];assert isinstance(via,p.PCB_VIA) and via.GetNetname()==item['net'] and via.GetIsFree(),'Seed net assignment did not survive native save/reload'
result=dict(parent_board_sha256=cfg['parent_board_sha256'],created_vias=created,generated_tracks=0,free_via_preserves_explicit_net=True,save_reload_net_verified=True,qualification='Explicit site only; independent native preflight and full autorouting required. No connection or route feasibility inferred from site legality.')
(folder/'via-seed.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
