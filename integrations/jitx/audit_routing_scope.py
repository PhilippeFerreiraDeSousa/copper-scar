"""Read-only audit of recorded JITX route selections; never calls native APIs."""
from pathlib import Path
import argparse,collections,json,hashlib

def audit(directory):
 messages=json.loads((directory/'before.json').read_text())
 board=next(x['body'] for x in messages if x['type']=='board')
 nets=next(x['body']['nets'] for x in messages if x['type']=='nets' and x['body'].get('complete') is True)
 selection=json.loads((directory/'routing-selection.json').read_text());all_ids={p for n in nets for c in n['connected'] for p in c['pads']}
 chosen=[n for n in nets if n['name'] in selection['nets']];chosen_ids={p for n in chosen for c in n['connected'] for p in c['pads']}
 pads=[]
 def walk(module):
  for group in module.get('groups',[]):
   for instance in group.get('instances',[]):pads.extend(o for o in instance.get('objects',[]) if 'pad' in o)
   walk(group)
 walk(board['module'])
 notifications={};responses={}
 for layer in selection['layers']:
  replies=json.loads((directory/f'route-layer-{layer}.json').read_text())
  notifications[str(layer)]=[x['body'] for x in replies if x['type']=='notify']
  responses[str(layer)]=dict(collections.Counter(x['type'] for x in replies))
 return {'directory':str(directory),'source_capture_sha256':hashlib.sha256((directory/'before.json').read_bytes()).hexdigest(),'all_native_nets':len(nets),'selected_nets':len(chosen),'omitted_native_nets':sorted(n['name'] for n in nets if n not in chosen),'all_native_terminals':len(all_ids),'selected_terminals':len(chosen_ids),'physical_named_pad_objects':len(pads),'native_terminals_resolve_to_board':all_ids<={p['pad'] for p in pads},'unselected_physical_pads_with_pinref':sum(p['pad'] not in all_ids and 'pinref' in p for p in pads),'unselected_physical_pads_without_pinref':sum(p['pad'] not in all_ids and 'pinref' not in p for p in pads),'selected_pad_local_layer_shapes':dict(collections.Counter(str(sorted({layer for s in p['shapes'] for layer in s['layers']})) for p in pads if p['pad'] in chosen_ids)),'requested_layers':selection['layers'],'copper_layer_count':board['stackup']['numlayers'],'via_definitions':len(board.get('vias',[])),'notifications':notifications,'response_types':responses,'timings':json.loads((directory/'timings.json').read_text()),'conclusion':'All native nets selected for per-layer calls' if len(chosen)==len(nets) else 'Scoped net repair, not full-board routing','limitations':['No proof every intended connection had a legal layer/transition path.','Layer shapes are local; production selection must apply current anchor side.','Acknowledgement is not task completion; exported geometry and independent checks remain required.']}
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('directory',type=Path);p.add_argument('--output',type=Path);a=p.parse_args();r=audit(a.directory);text=json.dumps(r,indent=2)
 if a.output:a.output.write_text(text)
 print(text)
