"""Dry packaging diagnostic; no native submission or managed-state edits."""
import json
from pathlib import Path
import sys
from google.protobuf.json_format import MessageToDict
from jitx.run.runtime import Runtime, _package_design
from jitx.inspect import visit
from jitx.via import Via
from jitx.proxy import typeof
from bridge_fixture.design import BridgeProof
out=Path(sys.argv[1]);out.mkdir(exist_ok=False)
root=Runtime()._construct(BridgeProof)
def dump(name):
    packaged,_=_package_design(root);data=MessageToDict(packaged,preserving_proto_field_name=True)
    (out/(name+'.json')).write_text(json.dumps(data,indent=2));return data
before=dump('before')
for _,v in visit(root,Via):
    v.diameters={0:.6,1:.6}
    v.type=typeof(v).type
changed=dump('after-overrides-and-enum')
print('payload keys',list(before))
print('definitions before',json.dumps(before.get('vias'))[:1800])
print('definitions after',json.dumps(changed.get('vias'))[:2200])
