"""Choose a finite, failure-weighted whole-group reordering from a measured route."""
import argparse,hashlib,json,math,random
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('baseline',type=Path);ap.add_argument('output',type=Path);a=ap.parse_args()
init=json.loads((a.baseline/'input/initialization.json').read_text())
audit=json.loads((a.baseline/'before-audit.json').read_text())
result=json.loads((a.baseline/'reimport-exact/result.json').read_text())
groups={g['group']:g for g in init['groups']};order=list(groups)
owner={r:g for g,item in groups.items() for r in item['refs']}
poses={v['ref']:v['after'] for v in init['moves']}
netrefs={}
for ref,fp in audit['identity'].items():
 for pad in fp['pads']:
  net=pad[2]
  if net and not net.startswith('unconnected-'):netrefs.setdefault(net,set()).add(ref)
def layout(sequence,cols):
 x,y=25.,25.;rowh=0.;width=0.;height=0.;origins={}
 for i,g in enumerate(sequence):
  if i and i%cols==0:x=25.;y+=rowh+8;rowh=0.
  w,h=groups[g]['size_mm'];origins[g]=[x,y];width=max(width,x+w);height=max(height,y+h);x+=w+8;rowh=max(rowh,h)
 return origins,[15,15,math.ceil(width+10),math.ceil(height+10)]
def metrics(origins,box):
 points={r:[poses[r][i]+origins[g][i]-groups[g]['origin_mm'][i] for i in [0,1]] for r,g in owner.items()}
 spans={}
 for n,rs in netrefs.items():
  ps=[points[r] for r in rs if r in points]
  if len(ps)>1:spans[n]=sum(max(p[i] for p in ps)-min(p[i] for p in ps) for i in [0,1])
 weighted=sum(v*(1+math.log1p(result['missing_by_net'][n]) if n in result['missing_by_net'] else .05) for n,v in spans.items())
 return dict(failure_weighted_center_span_mm=weighted,total_center_span_mm=sum(spans.values()),outline_area_mm2=(box[2]-box[0])*(box[3]-box[1]),net_spans_mm=spans)
base_origins={g:v['origin_mm'] for g,v in groups.items()};before=metrics(base_origins,init['outline_mm']);rng=random.Random(713)
trials=[];best=None
# Finite search, not repeated routing. Every scored ordering and its objective survive.
for cols in [3,4]:
 current=order[:]
 for iteration in range(240):
  candidate=current[:]
  if iteration:
   i,j=rng.sample(range(len(candidate)),2);candidate[i],candidate[j]=candidate[j],candidate[i]
  origins,box=layout(candidate,cols);m=metrics(origins,box)
  eligible=m['outline_area_mm2']<=1.1*before['outline_area_mm2']
  row=dict(columns=cols,iteration=iteration,order=candidate,eligible=eligible,metrics={k:v for k,v in m.items() if k!='net_spans_mm'})
  trials.append(row)
  if eligible and (best is None or m['failure_weighted_center_span_mm']<best['metrics']['failure_weighted_center_span_mm']):
   best=dict(order=candidate,columns=cols,origins=origins,outline_mm=box,metrics=m);current=candidate
assert best and best['metrics']['failure_weighted_center_span_mm']<before['failure_weighted_center_span_mm']
proposal=dict(schema_version=1,primitive='functional_group_reorder',source_board=str(a.baseline/'input/pcbgolf.kicad_pcb'),source_board_sha256=hashlib.sha256((a.baseline/'input/pcbgolf.kicad_pcb').read_bytes()).hexdigest(),feedback_receipt=str(a.baseline/'reimport-exact/result.json'),feedback_sha256=hashlib.sha256((a.baseline/'reimport-exact/result.json').read_bytes()).hexdigest(),reason='140remaining native connections after full600s spaced route; reorder whole functional groups to reduce span of remaining-net neighborhoods, preserving spacious within-group cells',groups=[dict(group=g,refs=groups[g]['refs'],translation_nm=[round((best['origins'][g][i]-groups[g]['origin_mm'][i])*1e6) for i in [0,1]]) for g in order],outline_mm=best['outline_mm'],before=before,selected=best,scored_candidates=trials,expected_score_terms=dict(stage=1,official_score=None,outline_area_delta_mm2=best['metrics']['outline_area_mm2']-before['outline_area_mm2'],via_delta='unknown until full route',copper_layers_delta=0,assembled_height_delta=0),qualification='Deterministic seed713 controls proposal search only, not router. Component-center span is a selection proxy, not electrical proof. All original functional-group membership and within-group pad positions are preserved; no model or footprint scaling.')
a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(proposal,indent=2)+'\n')
print(json.dumps(dict(before=before['failure_weighted_center_span_mm'],after=best['metrics']['failure_weighted_center_span_mm'],outline=best['outline_mm'],columns=best['columns'],order=best['order'])))
