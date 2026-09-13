#!/usr/bin/env python3
"""Copy and verify frozen fixture evidence; never run native CAD or access network."""
import argparse, hashlib, json, shutil, re, math
from pathlib import Path

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads(p.read_text())

def build(source, out):
    obs=source/'.local/topology-research-observability-01'; media=obs/'media'
    native=source/'.local/topology-research-01'; bundle=read(obs/'bundle.json')
    result=read(media/'results.json'); assert len(result['rows'])==5
    assert sha(media/'results.json')==bundle['result_sha256']
    out.mkdir(parents=True,exist_ok=True); evidence=out/'evidence'; evidence.mkdir(exist_ok=True)
    rows=[]
    for i,(r,b) in enumerate(zip(result['rows'],bundle['rows'])):
        assert r['stage']==b['stage'] and b['step']==i
        assert b['image']==f'board-{i:02}.png'
        pcb=media/f'board-{i:02}.kicad_pcb'; pro=pcb.with_suffix('.kicad_pro'); png=media/b['image']
        for p in (pcb,pro,png):
            assert sha(p)==bundle['media_sha256'][p.name],p
            shutil.copy2(p,evidence/p.name)
        summary=read(native/r['stage']/'independent/summary.json')
        assert sha(pcb)==b['board_sha256']==summary['source_board_sha256']
        assert sha(pro)==summary['project_sha256']
        assert summary['geometry_unchanged'] and summary['repeated_drc_agrees']
        assert summary['opens']==0 and summary['violations']==[] and summary['via_count']==6
        assert summary['component_count']==8 and summary['all_four_net_memberships_correct']
        # Independent saved evaluation uses normalized board; bind that board too.
        norm=next((native/r['stage']/'independent').glob('*.kicad_pcb'))
        assert sha(norm)==summary['normalized_board_sha256']
        sd=evidence/r['stage']; sd.mkdir(exist_ok=True)
        shutil.copy2(norm,sd/norm.name); shutil.copy2(pro,sd/pro.name)
        shutil.copy2(native/r['stage']/'independent/summary.json',sd/'summary.json')
        for n in (0,1):
            p=native/r['stage']/f'independent/drc-{n}.json'; drc=read(p)
            assert drc['unconnected_items']==[] and drc['violations']==[] and drc['schematic_parity']==[]
            shutil.copy2(p,sd/p.name)
        # Independently sum stored straight centerline records, without native CAD.
        length=0
        for records in summary['copper_by_net'].values():
            for rec in records:
                if rec.startswith('(segment '):
                    m=re.search(r'\(start ([\d.-]+) ([\d.-]+)\) \(end ([\d.-]+) ([\d.-]+)\)',rec)
                    assert m,rec
                    x,y,a,z=map(float,m.groups()); length+=math.hypot(a-x,z-y)
        assert abs(length-r['wire_length_mm'])<1e-8,(length,r)
        rows.append({**r,'via_count':summary['via_count'],'board_sha256':sha(pcb),'image_sha256':sha(png),'image':f'evidence/{png.name}','board':f'evidence/{pcb.name}','summary':f'evidence/{r["stage"]}/summary.json','drc0':f'evidence/{r["stage"]}/drc-0.json','drc1':f'evidence/{r["stage"]}/drc-1.json','independently_summed_length_mm':length})
    for p in media.glob('*.json'):
        assert sha(p)==bundle['media_sha256'][p.name],p
        shutil.copy2(p,evidence/p.name)
    for name in ['bundle.json','upload-receipt.json']:shutil.copy2(obs/name,evidence/name)
    shutil.copy2(source/'integrations/topology_bridge/media.py',evidence/'original-media-producer.py')
    payload={'scope':'Eight-pad four-net joint topology fixture only','whole_product_board_qualified':False,'rows':rows,'verification':'All five original image/CAD hashes match producer bundle. CAD hashes match independent summaries and normalized evaluated CAD. Both stored DRC reports have zero opens/violations. Centerline lengths independently summed from native segment records. No native rerun.','source_root':str(source),'fixture_root':str(native),'media_root':str(media)}
    (out/'data.js').write_text('window.FIXTURE='+json.dumps(payload)+';\n')
    shutil.copy2(Path(__file__).with_name('index.html'),out/'index.html')
    (out/'verification.json').write_text(json.dumps(payload,indent=2)+'\n')
    hashes={str(p.relative_to(out)):sha(p) for p in sorted(out.rglob('*')) if p.is_file() and p.name!='SHA256SUMS.json'}
    (out/'SHA256SUMS.json').write_text(json.dumps(hashes,indent=2)+'\n')
    print(json.dumps({'output':str(out),'snapshots':len(rows),'lengths':[r['wire_length_mm'] for r in rows],'decisions':[r['decision'] for r in rows],'all_hash_checks_passed':True}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();build(a.source.resolve(),a.out.resolve())
