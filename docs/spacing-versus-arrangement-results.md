# Controlled CMD branch comparison: space versus arrangement

All controls started from the same preserved 58-open incumbent `stage1-20260912-174325-566c96`, with original circuit, footprints, copper widths, six layers and manufacturing rules. The selected connected branch was R37 (CMD pull-up) and R42 (CMD series element). This is a small branch-space experiment, **not a global respacing of all 245 parts**.

| Control | Exact transformation | Native result | Decision |
|---|---|---|---|
| Added obstacle space | Translate R37 and R42 rigidly +100 mm in X, to (271.25,98.5) and (246.25,92.34), preserving their relative pose. Extend right board edge 240→284 mm. | 58 missing, 0 physical errors, 12 warnings after routing. | No connectivity gain; original incumbent retained after review. |
| Relative arrangement | R37 (171.25,98.5),0° → (153.2,95.34),90°; R42 and original outline unchanged. | 59 missing, 0 physical errors, 11 warnings after routing. | Regression; not promoted. |
| Local pad access | Rotate R37 0→90° at its original center; original outline and all other poses unchanged. | 60 missing, 4 physical findings, 12 warnings before routing. | Rejected at native placement gate; no unsafe route run. |

The space case added real space around the moved branch by placing it beyond the former board boundary. It did not merely add an empty outline border, scale footprint geometry, or enlarge trace widths. No transceiver, clock, decoupling or converter group was split by these two-resistor transformations. The rigid translation lengthens connections to the fixed rest of the circuit, a deliberate tradeoff in this test of surrounding room.

All routed controls had the same three-net scope (`+3V3`, `Net-(J2-CMD)`, `SD_CMD`) and 180-second inner allowance. Only copper incident to old pads of actually moved members was detached: six items in the space case, two in the arrangement and rotation cases. Exact comparisons found no changed copper outside the three declared nets and no nonmember placement changes. Remaining routing was retained. Original rules/support were independently checked; failed placement was never routed.

The first relative-placement option passed body screening but failed native copper checks (7 physical findings). A narrower search with retained-copper pad screening found no legal option. Expanding the proposal search from ±6 mm to ±12 mm around R42's CMD terminal produced the legal arrangement above. Both rejected preparations are preserved; neither is evidence that the neighborhood has no feasible arrangement.

## Connection-level findings

- **Space:** CMD's one open persisted, now between R42 pad 2 at (246.7,92.34) and R37 pad 2 at (271.7,98.5). The existing +3V3/U3-pad-32 open also persisted. SD_CMD stayed connected. No net's native missing-pair count improved or worsened.
- **Arrangement:** CMD's R37 branch remained open. A new +3V3 connection to R37 pad 1 at (153.2,95.79) appeared, in addition to the prior +3V3 open. SD_CMD stayed connected. This accounts for 58→59.
- **Pad rotation:** the native gate reported shorts between R37's relocated CMD pad and retained +3V3 tracks, plus solder-mask bridges. Power disconnections also increased. This is a measured local pad/copper conflict, not a conclusion drawn from proximity.

[Full per-net classifications, native endpoint UUIDs/positions and exact copper/pose deltas](/Users/philippe/dev/copper-scar-demo/.local/copperhead/reports/cmd-controlled-comparison/connections-and-effects.json). Native endpoint-pair identity can change with topology/reporting; a new track/via UUID alone is not counted as proof of a newly disconnected electrical island.

## What the experiment establishes

More surrounding space did **not** solve this CMD branch under the tested router. Its logs still show terminal validation refusals at a reported 0.300 mm edge distance. As established in the diagnostic analysis, the backend conflates raw overlap and forbidden terminal narrowing in the same message. This makes terminal construction/width refusal a stronger next diagnostic target than further blind outline expansion; it does not prove the exact rejected geometry without the typed branch data. The local rotation control separately demonstrates a genuine conflict with retained copper.

The existing scalar policy briefly promoted the expanded board on its airwire-distance tiebreak (1035.614 incumbent priority versus 1015.962 reported after), despite unchanged 58 opens and an extra warning. Review restored the original incumbent because this was not a verified connectivity improvement. The automatic decision remains in the historical attempt; the explicit correction is [recorded separately](/Users/philippe/dev/copper-scar-demo/.local/copperhead/loop/spacing-acceptance-review.json). This is another concrete reason not to drive placement solely from the scalar.

Evidence: [space](/Users/philippe/dev/copper-scar-demo/.local/copperhead/runs/stage1-20260912-175856-37d39b/attempt.json), [legal arrangement](/Users/philippe/dev/copper-scar-demo/.local/copperhead/runs/stage1-20260912-180311-fc397c/attempt.json), [pad-access rejection](/Users/philippe/dev/copper-scar-demo/.local/copperhead/runs/stage1-20260912-180410-42f8c9/attempt.json). Rejected relative preparations: `stage1-20260912-180024-78c334`, `stage1-20260912-180232-d91e53`.

The retained board is still **58 missing, zero physical errors, 11 warnings, not fully valid**. Native workers have completed these bounded controls. No broader placement sweep, manufacturing-rule relaxation or learned controller was added.
