# SD group placement: completed comparison

**Result: no improvement; incumbent preserved.** The six-resistor SD placement candidate finished with 59 missing native connections, zero physical errors and 14 warnings. The incumbent remains at 58 missing connections, zero physical errors and 11 warnings. Neither board is fully valid.

| Checkpoint | Missing pairs | Physical errors | Warnings |
|---|---:|---:|---:|
| Incumbent / outer input | 58 | 0 | 11 |
| After group placement, before inner routing | 74 | 0 | 11 |
| After routing the 12 affected signal nets | 59 | 0 | 14 |
| After additional targeted DAT1 repair | 59 | 0 | 14 |

The outer group contained R38–R43, the schematic SD data/command/clock series bundle. Two packing orders searched position and rotation around the declared U3/J2 interface pads. Five members moved or rotated; R42 stayed in place. The interface-distance proxy fell from 472.6 to 308.7 mm. This proxy improvement did not translate into better whole-board connectivity.

The placement removed 263 copper items on its 12 declared signal nets. Exact geometric comparison found no copper changes outside those nets and no nonmember movement. Original support files, parts/pad assignments, outline and layer stack remained unchanged. Native reference invariants passed before, after placement and after routing.

The placement search took 25.3 seconds. The first inner routing command completed in 20.1 seconds under a 900-second allowance; the second targeted command also completed without timing out. It returned identical design bytes. Raising the wall-time allowance alone is therefore not supported by this experiment as the next remedy.

Before the move, the SD CMD branch had one open and DAT1 had none. After routing, CMD still had one and DAT1 had one. All other declared SD nets had zero missing pairs. The warnings increased through three additional dangling vias. The saved candidate was not promoted, and the exploratory result is retained separately.

The comparison establishes that this particular group placement and bounded inner routing did not improve the board. It does not establish that the SD neighborhood is unroutable. Including the pull-up branch or changing the local routing search is a possible future experiment, not an action taken here. No broader experiment list or learning controller was implemented.

Evidence:

- [Outer placement and first inner routing](/Users/philippe/dev/copper-scar-demo/.local/copperhead/runs/stage1-20260912-174807-940294/attempt.json)
- [Immutable intermediate placement board](/Users/philippe/dev/copper-scar-demo/.local/copperhead/runs/stage1-20260912-174807-940294/placement-project/pcbgolf.kicad_pcb)
- [Actual copper and placement effects](/Users/philippe/dev/copper-scar-demo/.local/copperhead/runs/stage1-20260912-174807-940294/effects.json)
- [Targeted inner DAT1 repair, linked to the outer candidate](/Users/philippe/dev/copper-scar-demo/.local/copperhead/runs/stage1-20260912-175029-458217/attempt.json)
- [Preserved incumbent](/Users/philippe/dev/copper-scar-demo/.local/copperhead/candidates/stage1-20260912-174325-566c96/pcbgolf.kicad_pcb)

Both attempts' saved input/output CAD hashes and archived source hashes were verified; the intermediate placement project matches every recorded CAD hash. Sixteen focused contract tests passed. These checks establish execution/evidence integrity, not assembly, electrical or hardware qualification.

At completion of this comparison, the native routing workers had finished. The read-only dashboard remains available. The foreground task is yielding the result for review.
