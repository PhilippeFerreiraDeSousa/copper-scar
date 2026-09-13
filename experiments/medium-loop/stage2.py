"""Validity-gated optimization of the official PCBA volume/via/layer objective."""
from pathlib import Path
import argparse,copy,hashlib,json,math,shutil,subprocess,sys,time,os,threading
import sexpdata as sx
from audit import audit,inventory,nodes,first
from campaign import command as base_command,KIPY,KICAD,ROOT,now,write
from assembly import step_volume,board_inventory

def command(argv,folder,label):
    """Publish operation heartbeats while the bounded native command executes."""
    status_path=folder.parent/'live-status.json'
    if not status_path.exists():return base_command(argv,folder,label)
    status=json.loads(status_path.read_text());started=now();tick=time.monotonic();stop=threading.Event()
    def heartbeat():
        while not stop.is_set():
            record={**status,'status':'running','current_operation':label,'operation_started_at':started,'operation_elapsed_seconds':round(time.monotonic()-tick,2),'heartbeat_at':now(),'worker_pid':os.getpid(),'candidate_folder':str(folder)}
            write(status_path,record);write(folder.parent.parent/'status.json',{**record,'active_study':str(folder.parent)})
            stop.wait(2)
    thread=threading.Thread(target=heartbeat,daemon=True);thread.start()
    try:return base_command(argv,folder,label)
    except Exception as error:
        stop.set();thread.join();write(status_path,{**status,'status':'operation_failed','current_operation':label,'heartbeat_at':now(),'error':str(error),'worker_pid':os.getpid()});raise
    finally:stop.set();thread.join()

def assembly_clearance(f):
    # Conservative box-intersection screen of every populated model, independent
    # of missing KiCad courtyard settings. A box overlap rejects, never proves collision.
    boxes={}
    d=sx.loads((f/'pcbgolf.kicad_pcb').read_text())
    for fp in nodes(d,'footprint'):
        ref=next(v[2] for v in nodes(fp,'property') if v[1]=='Reference');at=first(fp,'at');fx,fy=at[1:3]
        assert len(at)<4 or at[3]==0,'Rotation extension requires independent transform qualification'
        model=first(fp,'model');off=first(first(model,'offset'),'xyz')[1:];scale=first(first(model,'scale'),'xyz')[1:];rot=first(first(model,'rotate'),'xyz')[1:]
        assert scale==[1,1,1] and rot[:2]==[0,0]
        v=step_volume(Path(model[1].replace('${KIPRJMOD}',str(f))))['bounds_mm'];angle=math.radians(rot[2]);corners=[]
        for x,y in [(v[0],v[1]),(v[0],v[4]),(v[3],v[1]),(v[3],v[4])]:
            xx=x*math.cos(angle)-y*math.sin(angle)+off[0];yy=x*math.sin(angle)+y*math.cos(angle)+off[1];corners.append((fx+xx,-fy+yy))
        boxes[ref]=[min(x for x,y in corners),min(y for x,y in corners),v[2]+off[2],max(x for x,y in corners),max(y for x,y in corners),v[5]+off[2]]
    overlaps=[]
    import itertools
    for a,b in itertools.combinations(boxes,2):
        u,v=boxes[a],boxes[b];depth=[min(u[i+3],v[i+3])-max(u[i],v[i]) for i in range(3)]
        if all(q>1e-5 for q in depth):overlaps.append({'components':[a,b],'bbox_overlap_mm':depth})
    return {'ok':not overlaps,'model_boxes_mm':boxes,'conservative_overlap_findings':overlaps}

def score(f):
 inv=board_inventory(f/'pcbgolf.kicad_pcb');assert not inv['missing_models'];e=step_volume(f/'assembly.step');a=json.loads((f/'acceptance.json').read_text());d=json.loads((f/'drc.json').read_text());erc=json.loads((f/'erc.json').read_text());ercviolations=[v for s in erc['sheets'] for v in s['violations']]
 assembly_check=assembly_clearance(f)
 valid=assembly_check['ok'] and a['accepted'] and not d['violations'] and not d['unconnected_items'] and not d['schematic_parity'] and not ercviolations
 terms={'pcba_bbox_volume_mm3':e['volume_mm3'],'via_count':inv['vias'],'via_penalty':50*inv['vias'],'copper_layers':inv['copper_layers'],'layer_penalty':5000*inv['copper_layers']}
 result={'valid':valid,'official_formula_score':sum(terms[k] for k in ['pcba_bbox_volume_mm3','via_penalty','layer_penalty']) if valid else None,'terms':terms,'assembly':e,'assembly_clearance':assembly_check,'board_sha256':hashlib.sha256((f/'pcbgolf.kicad_pcb').read_bytes()).hexdigest(),'model_coverage':{'populated_components':inv['footprints'],'resolved_models':inv['footprints'],'missing':[]},'native':{'opens':len(d['unconnected_items']),'violations':len(d['violations']),'parity_findings':len(d['schematic_parity']),'erc_findings':len(ercviolations)},'qualification':'Official formula applied to PCB Golf-inspired reduced circuit and complete nominal assembly model. Not an official competition submission; no powered hardware qualification.'};write(f/'score.json',result);return result

def proposal(template,factor,margin=1):
 d=sx.loads(template.read_text());poses={};bounds=[];fx,fy=factor if isinstance(factor,(list,tuple)) else (factor,factor)
 for f in nodes(d,'footprint'):
  r=next(v[2] for v in nodes(f,'property') if v[1]=='Reference');at=first(f,'at');old=at[1:];x=round(55+(old[0]-55)*fx,4);y=round(50+(old[1]-50)*fy,4);at[1:]=[x,y,*old[2:]];poses[r]={'before':old,'after':at[1:]}
  # Fixed component bodies and pads are not scaled, only their placement spacing.
  for p in nodes(f,'pad'):
   px,py=first(p,'at')[1:3];w,h=first(p,'size')[1:3];bounds.append((x+px-w/2,y+py-h/2,x+px+w/2,y+py+h/2))
  if r.startswith('J1'):bounds.append((x-5.08,y-2.54,x+5.08,y+2.54))
 xmin=math.floor((min(v[0] for v in bounds)-margin)*2)/2;xmax=math.ceil((max(v[2] for v in bounds)+margin)*2)/2;ymin=math.floor((min(v[1] for v in bounds)-margin)*2)/2;ymax=math.ceil((max(v[3] for v in bounds)+margin)*2)/2
 d[:]=[v for v in d if not(isinstance(v,list) and v and str(v[0]) in ['segment','via','arc','zone','gr_line'])]
 import uuid
 for x,y,xx,yy in [(xmin,ymin,xmax,ymin),(xmax,ymin,xmax,ymax),(xmax,ymax,xmin,ymax),(xmin,ymax,xmin,ymin)]:d.append(sx.loads(f'(gr_line (start {x} {y}) (end {xx} {yy}) (stroke (width 0.05) (type default)) (layer "Edge.Cuts") (uuid "{uuid.uuid4()}"))'))
 return sx.dumps(d),{'kind':'independent_axis_spacing_and_outline' if fx!=fy else 'placement_spacing_and_outline','spacing_factor':factor,'x_factor':fx,'y_factor':fy,'edge_margin_mm':margin,'component_poses':poses,'outline_mm':[xmin,ymin,xmax,ymax],'netlist_or_pad_geometry_changed':False,'copper_topology':'Explicit full ripup and all-net two-layer realization; no retained via UUID is reassigned','rationale':'Reduce the official PCBA bounding-box volume by contracting component spacing and trimming unused edge margin. Keep physical component/pad dimensions fixed and reject all native/assembly failures.'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('base',type=Path);ap.add_argument('--source',type=Path,required=True);ap.add_argument('--study',default='');ap.add_argument('--margin',type=float,default=1);ap.add_argument('--factors',default='1,.8,.65,.5,.4');ap.add_argument('--incumbent',type=Path);ap.add_argument('--geometry',type=Path);ap.add_argument('--primitive',default='');ap.add_argument('--rationale',default='');a=ap.parse_args();base=a.base.resolve();root=base/'stage2';source=a.source.resolve();baseline=root/'baseline';root=root/a.study if a.study else root;root.mkdir(exist_ok=True);manifest=base/'input/circuit.json';commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip();incdir=a.incumbent.resolve() if a.incumbent else baseline;inc=json.loads((incdir/'score.json').read_text());assert inc['valid'];geometry=a.geometry.resolve() if a.geometry else baseline/'pcbgolf.kicad_pcb'
 protocol={'formula':'PCBA bbox volume mm^3 +50*via_count +5000*copper_layers','source':'https://comma.ai/leaderboard','source_sha':commit,'initial_board_sha256':inc['board_sha256'],'baseline_score':inc['official_formula_score'],'objective':'Strict lower official-formula score, after full native/assembly acceptance','factors':[list(map(float,x.split(':'))) if ':' in x else float(x) for x in a.factors.split(',')],'geometry_source':str(geometry),'geometry_sha256':hashlib.sha256(geometry.read_bytes()).hexdigest(),'initial_incumbent':str(incdir),'route_seconds':240,'route_passes':100,'full_board':True,'layers':2,'tie_policy':'retain incumbent','assembly_contract':'assembly-contract.json','wire_length_is_objective':False,'edge_margin_mm':a.margin};write(root/'protocol.json',protocol);events=[]
 for idx,factor in enumerate(protocol['factors'],1):
  f=root/f'candidate-{idx:02}';f.mkdir();start=now();write(root/'live-status.json',{'size_family':'medium-loop','stage':2,'running':idx,'worker_pid':os.getpid(),'started_at':start,'last_completed':idx-1,'incumbent_score':inc['official_formula_score']});board,action=proposal(geometry,factor,a.margin);(f/'pcbgolf.kicad_pcb').write_text(board)
  for name in ['pcbgolf.kicad_pro','pcbgolf.kicad_sch','pcbgolf.kicad_sym','fp-lib-table','sym-lib-table']:shutil.copy2(baseline/name,f/name)
  for name in ['pcbgolf.pretty','pcbgolf.3dshapes','models']:shutil.copytree(baseline/name,f/name)
  action['kind']=a.primitive or action['kind'];action['rationale']=a.rationale or action['rationale'];parent_poses=inventory(incdir/'pcbgolf.kicad_pcb')[0];action['geometry_transform_poses']=action['component_poses'];action['component_poses']={r:{'before':parent_poses[r]['pose'],'after':v['after']} for r,v in action['geometry_transform_poses'].items()};dims=action['outline_mm'];expected_volume=(dims[2]-dims[0])*(dims[3]-dims[1])*inc['assembly']['dimensions_mm'][2];action['expected_score_terms']={'qualification':'Forecast only, fixedheight andexistingviacount; nativeassemblyandactualrouting decide score','volume_mm3':expected_volume,'volume_delta_mm3':expected_volume-inc['terms']['pcba_bbox_volume_mm3'],'via_count_assumption':inc['terms']['via_count'],'via_penalty_assumption':inc['terms']['via_penalty'],'layer_penalty':inc['terms']['layer_penalty'],'score_if_vias_unchanged':expected_volume+inc['terms']['via_penalty']+inc['terms']['layer_penalty']};metadata=geometry.parent/'proposal.json';action['source_primitive']={'metadata_file':str(metadata),'metadata_sha256':hashlib.sha256(metadata.read_bytes()).hexdigest(),'kind':json.loads(metadata.read_text()).get('kind')} if metadata.exists() else {'kind':'uniform_spacing','reason':'Exploratoryvolumecontraction'};write(f/'proposal.json',action);project=(f/'pcbgolf.kicad_pro').read_bytes();cmds=[]
  def native(kind):
   cmds.append(command([KIPY,ROOT/'experiments/medium-loop/native_stage.py',kind,f],f,kind));current=(f/'pcbgolf.kicad_pro').read_bytes()
   if current!=project:(f/(kind+'-producer-project.json')).write_bytes(current)
   (f/'pcbgolf.kicad_pro').write_bytes(project)
  native('export');shutil.copy2(f/'pcbgolf.kicad_pcb',f/'preview.kicad_pcb');cmds.append(command([KICAD,'pcb','drc','--schematic-parity','--format','json','-o',f/'preflight.json',f/'pcbgolf.kicad_pcb'],f,'preflight'));pre=json.loads((f/'preflight.json').read_text())
  # Even rejected physical candidates retain an explicit preflight record. Do not
  # send illegal geometry to a router or treat early rejection as router failure.
  pre_assembly=assembly_clearance(f);write(f/'preflight-assembly.json',pre_assembly)
  legal=not pre['violations'] and not pre['schematic_parity'] and pre_assembly['ok']
  if legal:
   cmds.append(command([sys.executable,ROOT/'scripts/copperhead_route.py',f,'--seconds','240','--passes','100','--whole-board','--skip-fanout'],f,'full-route'));native('import')
  native('audit');cmds.append(command([KICAD,'pcb','drc','--schematic-parity','--format','json','-o',f/'drc.json',f/'pcbgolf.kicad_pcb'],f,'drc'));cmds.append(command([KICAD,'sch','erc','--format','json','-o',f/'erc.json',f/'pcbgolf.kicad_sch'],f,'erc'));accept=audit(f,manifest,source);cmds.append(command([KICAD,'pcb','export','step','-f','-o',f/'assembly.step',f/'pcbgolf.kicad_pcb'],f,'step-export'));result=score(f);cmds.append(command([KICAD,'pcb','export','svg','--layers','F.Cu,B.Cu,F.SilkS,Edge.Cuts','--mode-single','--page-size-mode','2','--exclude-drawing-sheet','-o',f/'board.svg',f/'pcbgolf.kicad_pcb'],f,'render'));cmds.append(command(['/opt/homebrew/bin/rsvg-convert','-w','1400','-o',f/'board.png',f/'board.svg'],f,'raster'));retain=result['valid'] and result['official_formula_score']<inc['official_formula_score'];event={'index':idx,'started_at':start,'finished_at':now(),'source_sha':commit,'folder':str(f),'parent_incumbent':str(incdir),'proposal_source':str(geometry),'action':action,'routing_attempted':legal,'commands':cmds,'result':result,'retained':retain}
  if retain:inc=result;incdir=f
  event['incumbent_score']=inc['official_formula_score'];event['incumbent_folder']=str(incdir);write(f/'event.json',event);events.append(event);write(root/'events.json',events);write(root/'current.json',{'folder':str(incdir),'score':inc,'last_completed':idx,'source_sha':commit});write(root/'live-status.json',{'size_family':'medium-loop','stage':2,'running':None,'status':'assessing-next-proposal','heartbeat_at':now(),'worker_pid':os.getpid(),'last_completed':idx,'incumbent_score':inc['official_formula_score']});print(idx,factor,result['valid'],result['official_formula_score'],'retained',retain,'native',result['native'],flush=True)
 write(root.parent/'status.json',{'size_family':'medium-loop','stage':2,'running':False,'status':'assessing-next-proposal','heartbeat_at':now(),'active_study':str(root),'last_completed':len(events),'incumbent_score':inc['official_formula_score'],'latest_completed_folder':str(incdir)})
 print(json.dumps({'selected':str(incdir),'score':inc}),flush=True)
if __name__=='__main__':main()
