"""Add terminal labels to the existing unsaved native partition inspection."""
import argparse,json
from pathlib import Path
import pcbnew as p
from copperhead_pad_partitions import inspect

ap=argparse.ArgumentParser();ap.add_argument('--before',type=Path,required=True);ap.add_argument('--after',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
before=inspect(a.before);after=inspect(a.after)
for path,result in ((a.before,before),(a.after,after)):
 board=p.LoadBoard(str(path.resolve()))
 result['pad_labels']={pad.m_Uuid.AsString():dict(terminal=footprint.GetReference()+'.'+pad.GetNumber(),net=pad.GetNetname()) for footprint in board.GetFootprints() for pad in footprint.Pads()}
groups=[set(x) for x in after['groups']];splits=[x for x in before['groups'] if not any(set(x)<=g for g in groups)]
result=dict(before=before,after=after,pad_partitions_equal=before['groups']==after['groups'],no_connected_pad_group_split=not splits,split_groups=splits,CAD_saved=False)
a.output.write_text(json.dumps(result,indent=2))
