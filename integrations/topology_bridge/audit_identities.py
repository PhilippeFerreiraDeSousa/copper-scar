"""Verify unchanged native route/via records by net, resolving numeric net IDs."""
import json
from pathlib import Path
import sys

def inventory(stage):
    messages=json.loads((stage/'final.json').read_text())
    named=next(m['body']['nets'] for m in messages if m['type']=='nets' and m['body'].get('complete'))
    names={n['id']:n['name'] for n in named};via_records=next(m['body']['vias'] for m in messages if m['type']=='via-info')
    routes={};vias={}
    for m in messages:
        if m['type']=='routed':
            r=dict(m['body']);net=names[r['net']];r['net']=net;routes.setdefault(net,{})[r['route']]=r
    for n in named:
        vias[n['name']]={v:via_records[v] for part in n['connected'] for v in part.get('vias',[])}
    return routes,vias
root=Path(sys.argv[1]);result=json.loads((root/'results.json').read_text());rows=[]
for row in result['rows'][1:]:
    stage=root/row['stage'];parent=root/(row['stage']+'-parent');p=json.loads((root/(row['stage']+'-proposal.json')).read_text())
    br,bv=inventory(parent);ar,av=inventory(stage);unchanged=sorted(set(br)-set(p['affected_nets']))
    assert all(br[n]==ar[n] and bv[n]==av[n] for n in unchanged)
    rows.append({'stage':row['stage'],'unchanged_native_records_by_net':unchanged,'unchanged_route_ids_and_bodies':sum(len(br[n]) for n in unchanged),'unchanged_via_ids_and_records':sum(len(bv[n]) for n in unchanged)})
(root/'identity-audit.json').write_text(json.dumps(rows,indent=2));print(json.dumps(rows,indent=2))
