"""Full authored-item comparison around the declared native topology primitive."""
from pathlib import Path
import sexpdata as sx
from .effects import canonical

def authored(tree):
    if not isinstance(tree,list):return tree
    return [authored(x) for x in tree if not (isinstance(x,list) and x and str(x[0]) in ('filled_polygon','fill_segments'))]

def check(before,after,removed,created):
    def read(path):
        root=authored(sx.loads(Path(path).read_text()));items={};other=[]
        for item in root:
            uid=next((str(n[1]) for n in item if isinstance(n,list) and n and str(n[0])=='uuid'),None) if isinstance(item,list) else None
            if uid:items[uid]=canonical(item)
            else:other.append(canonical(item))
        return items,other
    old,old_other=read(before);new,new_other=read(after)
    removed=set(removed);created=set(created)
    assert removed<=old.keys() and not removed&new.keys()
    assert created==new.keys()-old.keys()
    assert all(str(new[uid][0])=='via' for uid in created)
    assert {uid:row for uid,row in old.items() if uid not in removed}=={uid:row for uid,row in new.items() if uid not in created},'Undeclared authored item changed'
    assert old_other==new_other,'Board configuration changed'
    return dict(all_undeclared_authored_items_preserved=True,removed_uuids=sorted(removed),created_via_uuids=sorted(created),regenerated_zone_fills_excluded=True)
