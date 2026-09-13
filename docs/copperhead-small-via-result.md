# Additional through-via result

Completed trial `stage1-20260913-052618-76325d` reduced native missing connections from 53 to 52, with zero error-severity findings and 18 warnings under the unchanged project settings. The retained board SHA-256 is `0940a715d15b6505d9f854fc489b4ac81865f83426150b3560680ce655db25c4`.

The trial added a separate 0.45 mm copper / 0.20 mm drill through-via definition to routing eligibility. All eight targeted stock fanouts failed without creating geometry. The subsequent full 600-second routing evaluation created one actual new GND via at (137.238, 82.4427) mm. Independent KiCad connectivity checking showed R66.1 joining the 229-pad main ground group, including U15.3 and both ground planes. All 668 pre-existing vias retained their net, position, diameter on every copper layer, drill and span. Every other pad partition, footprint pose and original project file remained unchanged.

This proves native realization and a full-routing connectivity improvement. There was no fresh unchanged-parent routing control, so the gain is not isolated causal proof of via diameter, and it was not a successful targeted fanout. The board remains incomplete and has no official score or engineering/fabrication qualification.

The original proposal mislabeled the net of J8.A6 as CH2_SBU2; its actual native and engine binding was CH4_D_P. The original evidence remains immutable. A separate `terminal-scope-correction.json`, verified W&B summary and deterministic Weave correction call `e5c77ea5-11ee-565a-af13-7cd330fa8384` preserve the corrected interpretation. Future fanout actions resolve explicit terminal identities against native pad nets before routing.

The next explicit-site hypothesis places a free CAN0_H via at (122.75, 58.93) mm near J5.A2, without drawing a trace. `SetIsFree(True)` and save/reload net assertions preserve the intended standalone net assignment. Original-rule site legality does not prove the pad-to-via or via-to-trunk connection; the full router and native connectivity checker decide the result.

Unchanged project settings are this evaluation's acceptance contract, not a claim that official PCBGolf rules require identical project bytes. The project's 0.2 mm trace width is nominal, while 0.2 mm is the effective default net clearance. No trace-width or clearance changes were made in these trials.
