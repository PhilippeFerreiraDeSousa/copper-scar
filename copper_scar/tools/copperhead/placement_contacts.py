"""Reject implicit reassignment of existing vias during a placement edit."""
from pathlib import Path
import sexpdata as sx

def via_nets(path):
 root=sx.loads(Path(path).read_text());names={str(x[1]):str(x[2]) for x in root if isinstance(x,list) and x and str(x[0])=='net' and len(x)>2};out={}
 for item in root:
  if not isinstance(item,list) or not item or str(item[0])!='via':continue
  fields={str(x[0]):x[1:] for x in item[1:] if isinstance(x,list) and x};uid=str(fields['uuid'][0]);raw=str(fields.get('net',['0'])[0]);out[uid]=names.get(raw,raw)
 return out

def check(before,after):
 old,new=via_nets(before),via_nets(after);changes=[dict(uuid=u,before_net=net,after_net=new[u]) for u,net in old.items() if u in new and new[u]!=net]
 return dict(existing_via_net_attachments_preserved=not changes,changes=changes,removed_via_uuids=sorted(old.keys()-new.keys()),qualification='Checks net identity of surviving source vias; declared removals and geometric movement have separate guards')
