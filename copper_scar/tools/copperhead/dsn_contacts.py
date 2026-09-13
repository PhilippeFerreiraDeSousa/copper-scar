"""Losslessly expose existing same-net wire contacts to the DSN importer."""
from collections import Counter,defaultdict
from copy import deepcopy
from decimal import Decimal
import sexpdata as sx
import re

VERSION='split-existing-junctions-v1'

def child(node,name):
    return next(x for x in node if isinstance(x,list) and x and str(x[0])==name)

def records(text):
    for match in re.finditer(r'(?m)^[ \t]*\((?:wire \(path |via )',text):
        start=match.start();depth=0;quoted=False;escaped=False;opened=False
        for end in range(start,len(text)):
            char=text[end]
            if quoted:
                if escaped:escaped=False
                elif char=='\\':escaped=True
                elif char=='"':quoted=False
            elif char=='"':quoted=True
            elif char=='(':depth+=1;opened=True
            elif char==')':depth-=1
            if opened and depth==0 and not quoted:
                end+=1
                if end<len(text) and text[end]=='\n':end+=1
                yield start,text[start:end]
                break
        else:raise ValueError('Unterminated DSN wire/via record')

def partition(text,nets):
    wires=[];points=defaultdict(set);counts=defaultdict(Counter);vias=defaultdict(set)
    for index,line in records(text):
        stripped=line.strip()
        if stripped.startswith('(wire (path '):
            wire=sx.loads(stripped);net=str(child(wire,'net')[1])
            if net not in nets:continue
            path=child(wire,'path');assert len(path)>=7 and (len(path)-3)%2==0
            layer=str(path[1]);pts=list(zip(path[3::2],path[4::2]));wires.append((index,line,wire,net,layer,pts));points[net,layer].update(pts);counts[net,layer].update(pts)
        elif stripped.startswith('(via ') and '(net ' in stripped:
            via=sx.loads(stripped);net=str(child(via,'net')[1])
            if net in nets:vias[net].add((via[2],via[3]))
    changes=[]
    for index,line,wire,net,layer,pts in wires:
        sequence=[];cuts=[];candidates=points[net,layer]|vias[net]
        for a,b in zip(pts,pts[1:]):
            sequence.append(a)
            if len(sequence)>1 and (a in vias[net] or counts[net,layer][a]>1):cuts.append(len(sequence)-1)
            ax,ay=(Decimal(str(v)) for v in a);bx,by=(Decimal(str(v)) for v in b);inside=[]
            for q in candidates:
                if q==a or q==b:continue
                x,y=(Decimal(str(v)) for v in q)
                if min(ax,bx)<=x<=max(ax,bx) and min(ay,by)<=y<=max(ay,by) and (x-ax)*(by-ay)==(y-ay)*(bx-ax):inside.append(q)
            inside.sort(key=lambda q:(Decimal(str(q[0]))-ax)**2+(Decimal(str(q[1]))-ay)**2)
            for q in inside:sequence.append(q);cuts.append(len(sequence)-1)
        sequence.append(pts[-1]);cuts=sorted(set(cuts))
        if not cuts:continue
        pieces=[];start=0;indent=line[:len(line)-len(line.lstrip())]
        for stop in cuts+[len(sequence)-1]:
            assert stop>start
            new=deepcopy(wire);child(new,'path')[3:]=[v for xy in sequence[start:stop+1] for v in xy];pieces.append(indent+sx.dumps(new)+'\n');start=stop
        changes.append(dict(index=index,net=net,layer=layer,old_line=line,new_lines=pieces,existing_junctions=[sequence[c] for c in cuts]))
    output=text
    for row in reversed(changes):output=output[:row['index']]+''.join(row['new_lines'])+output[row['index']+len(row['old_line']):]
    restored=output
    for row in changes:restored=restored[:row['index']]+row['old_line']+restored[row['index']+len(''.join(row['new_lines'])):]
    assert restored==text
    return output,dict(version=VERSION,nets=sorted(nets),changes=changes,exact_decimal_collinear_partitions=True,every_other_byte_unchanged=True,new_copper=False,rules_changed=False)
