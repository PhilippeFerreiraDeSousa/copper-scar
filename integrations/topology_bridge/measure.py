"""Read actual KiCad centerline lengths; no invented objective values."""
import json
import sys
import pcbnew
b=pcbnew.LoadBoard(sys.argv[1])
print(json.dumps({'wire_length_mm':sum(t.GetLength()/1e6 for t in b.GetTracks() if not isinstance(t,pcbnew.PCB_VIA)),'via_count':sum(isinstance(t,pcbnew.PCB_VIA) for t in b.GetTracks())}))
