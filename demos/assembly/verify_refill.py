#!/usr/bin/env python3
"""Verify that a private KiCad refill/save preserves authored CAD subtrees."""
import argparse,collections,hashlib,json,re
from pathlib import Path

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def parse(path):
 stack=[];root=None
 for token in re.findall(r'"(?:\\.|[^"\\])*"|[()]|[^\s()]+',path.read_text()):
  if token=='(':
   node=[]
   if stack:stack[-1].append(node)
   stack.append(node)
  elif token==')':
   root=stack.pop()
  else:stack[-1].append(token)
 assert not stack
 return root

def authored(root):
 result=[]
 for item in root[1:]:
  if not isinstance(item,list):continue
  if item[0]=='zone':item=[x for x in item if not (isinstance(x,list) and x[0] in ['filled_polygon','fill_segments'])]
  result.append(json.dumps(item,separators=(',',':')))
 return collections.Counter(result)
p=argparse.ArgumentParser();p.add_argument('before',type=Path);p.add_argument('after',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
old=parse(a.before);new=parse(a.after);o=authored(old);n=authored(new)
missing=list((o-n).elements());added=list((n-o).elements());result=dict(source_board_sha256=sha(a.before),published_board_sha256=sha(a.after),all_authored_subtrees_preserved=not missing and not added,method='Exact tokenized root-child multiset; only generated zone filled_polygon/fill_segments entries excluded',missing_authored_subtrees=missing,added_authored_subtrees=added)
a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['missing_authored_subtrees','added_authored_subtrees']},indent=2));assert result['all_authored_subtrees_preserved']
