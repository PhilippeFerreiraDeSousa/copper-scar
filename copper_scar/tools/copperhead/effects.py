"""Artifact-level action effects; no solver state or causal benefit is inferred."""
from collections import Counter,defaultdict
from pathlib import Path
import fnmatch,json,re
import sexpdata as sx

def nodes(v,key):return [n for n in v if isinstance(n,list) and n and str(n[0])==key]
def first(v,key,default=None):
    n=nodes(v,key)
    return n[0][1:] if n else default

def canonical(value):
    if isinstance(value,dict):return {k:canonical(v) for k,v in value.items()}
    if isinstance(value,list):return [canonical(v) for v in value]
    if isinstance(value,(int,float)) and not isinstance(value,bool):return float(value)
    return value

def inventory(path):
    tree=sx.loads(Path(path).read_text());names={str(n[1]):str(n[2]) for n in nodes(tree,'net') if len(n)>2}
    copper=defaultdict(Counter);poses={}
    for item in tree:
        if not isinstance(item,list) or not item:continue
        kind=str(item[0])
        if kind=='footprint':
            ref=next(str(n[2]) for n in nodes(item,'property') if n[1]=='Reference')
            at=first(item,'at',[0,0]);poses[ref]=[float(at[0]),float(at[1]),float(at[2]) if len(at)>2 else 0]
        if kind not in ('segment','arc','via'):continue
        net=first(item,'net',[''])[0];net=names.get(str(net),str(net))
        fields=[n for n in item[1:] if not isinstance(n,list) or str(n[0]) not in ('uuid','tstamp','net')]
        if kind=='segment':
            ends=sorted([first(item,'start'),first(item,'end')]);fields=[n for n in fields if not isinstance(n,list) or str(n[0]) not in ('start','end')]+[['endpoints',ends]]
        fields=sorted(fields,key=str);copper[net][json.dumps(canonical([kind,fields]),default=str,sort_keys=True)]+=1
    return copper,poses

def compare(before,after,selected=()):
    old,op=inventory(before);new,np=inventory(after);changes=[]
    for net in sorted(old.keys()|new.keys()):
        removed=sum((old[net]-new[net]).values());added=sum((new[net]-old[net]).values())
        if removed or added:changes.append(dict(net=net,removed=removed,added=added,selected=any(fnmatch.fnmatchcase(net,p) for p in selected)))
    moves=[dict(ref=ref,from_mm=op[ref][:2],to_mm=np[ref][:2],from_degrees=op[ref][2],to_degrees=np[ref][2]) for ref in sorted(op.keys()&np.keys()) if op[ref]!=np[ref]]
    return dict(schema_version=1,selected_net_patterns=list(selected),copper_changes=changes,changed_unselected_nets=[n['net'] for n in changes if not n['selected']] if selected else [],moves=moves,removed_refs=sorted(op.keys()-np.keys()),added_refs=sorted(np.keys()-op.keys()),interpretation='Geometric copper multiset comparison ignores item UUIDs and segment direction; selected nets are routing targets, actual cleanup effects may be wider')

def missing_by_net(evaluation):
    c=Counter()
    for v in evaluation.get('violations',[]):
        if v['type']=='unconnected_items':c.update({n for i in v.get('items',[]) for n in re.findall(r'\[([^\]]+)\]',i.get('description',''))})
    return dict(c)

def geometry_scope(path):
    """Scope routing feedback to placement, board outline and enabled layers."""
    import hashlib
    tree=sx.loads(Path(path).read_text());poses={};outline=[]
    for item in tree:
        if not isinstance(item,list) or not item:continue
        if str(item[0])=='footprint':
            ref=next(str(n[2]) for n in nodes(item,'property') if n[1]=='Reference')
            at=first(item,'at',[0,0]);poses[ref]=[float(at[0]),float(at[1]),float(at[2]) if len(at)>2 else 0]
        elif str(item[0]).startswith('gr_') and first(item,'layer')==['Edge.Cuts']:
            outline.append([n for n in item if not isinstance(n,list) or str(n[0]) not in ('uuid','tstamp')])
    data=canonical(dict(poses=poses,layers=nodes(tree,'layers'),outline=sorted(outline,key=str)))
    return hashlib.sha256(json.dumps(data,default=str,sort_keys=True).encode()).hexdigest()
