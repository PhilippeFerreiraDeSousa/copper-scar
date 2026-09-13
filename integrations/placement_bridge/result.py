"""Seal the producer result after independent evaluation of actual native output."""
import argparse
from pathlib import Path
from contract import read, write, sha, pcb, require
from copperhead import evaluate

def seal(request, parent, candidate, source, output):
    candidate=Path(candidate);parent=Path(parent);output=Path(output)
    result=evaluate(request,parent,candidate,source,output/'evaluation')
    before=read(parent/'final.json');after=read(candidate/'final.json')
    def routes(messages):return {m['body']['route']:m['body'] for m in messages if m['type']=='routed'}
    a,b=routes(before),routes(after)
    require(set(a)==set(b),'native route identity lost')
    def vias(messages):return next(m['body']['vias'] for m in messages if m['type']=='via-info')
    require(set(vias(before))==set(vias(after)), 'native via identity lost')
    result.update(schema='copperhead-jitx-fixture-result-v1',comparison_kind='synthetic_fixture_bridge',
        termination=read(candidate/'completion.json'),
        native_delta={'route_ids_preserved':len(a),'route_records_identical':sum(a[k]==b[k] for k in a),
                      'via_ids_preserved':len(vias(before)),'vias_added_during_move':0},
        diagnostics={'scope':'all eight terminals / all four complete fixture nets',
                     'realization':'existing anchored via and incident routes updated by native reposition',
                     'native_messages': sorted({m['type'] for m in after}),
                     'generic_layer_or_via_planner':False},
        artifact_sha256={str(p.relative_to(candidate)):sha(p) for p in candidate.rglob('*') if p.is_file() and
            (p.parent==candidate or 'export' in p.relative_to(candidate).parts)})
    write(output/'result.json',result)
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('request','parent','candidate','source','output'):p.add_argument('--'+name,type=Path,required=True)
    a=p.parse_args();r=seal(a.request,a.parent,a.candidate,a.source,a.output);print(r['decision'])
