# Full-board re-layout comparison: measured results

**The earlier spaced grid changed arrangement and outline. It did not test uniform position scaling. A separate exact-uniform arm is now running.**

All rows preserve the complete original 245-component/1,078-pad design and the full schematic net partition. These are invalid diagnostic boards with **51 unchanged original footprint errors**, not completed PCBs.

| Fresh full-board initialization | Outline | Initial missing | Missing after 600 s | Vias | New non-open native findings |
|---|---:|---:|---:|---:|---:|
| Package-aware spacious groups | 176×218 mm | 499 | 140 | 483 | 0 |
| Prior schematic-local ring floorplan | 140×105 mm | 499 | 111 | 443 | 0 |

The prior floorplan performed better in this matched-budget trial: 29 fewer missing connections and 40 fewer vias. The larger spaced layout did not reproduce the immediate success of the much smaller demonstration circuits. There is one run per initialization; pose/outline change together, router seed is not verified, and other host work may affect scheduling. Both received 600 seconds, 100-pass limits and one routing thread; actual wrapper elapsed times were 604.37 and 604.30 seconds. Both preserved native pad/net identity and restored every initially connected pad group.

Examples of remaining missing-connection counts (prior / spaced): GND **18 / 36**, +3V3 **5 / 13**, +5V **5 / 9**, +12V **3 / 7**. All four CAN-H nets have **4 / 5** each. Other nets trade off; complete locations and pad UUIDs are in the saved DRC reports. Missing counts describe KiCad report pairs, not a required number of new traces.

The spaced output initially tripped an exact-pose audit because the SES bridge round-tripped integer coordinates through floating-point millimeters: 17 anchors shifted by one nanometer. Commit `f4cfc27` fixes integer-coordinate preservation. The **same saved SES** was reimported into a separate project and checked again; no routing rerun or relaxed tolerance was used. The failed bridge output and audit remain preserved.

Verified spaced board: `74978e8565360327b9b3bd3aa7929390f320dfc322ee68a09d8ecbb0c5781b07`, receipt under `.local/copperhead/full-spacious/v1/spacious-baseline-r2/reimport-exact/`. Independent outcome audit passed 19 checks, including exact whole-footprint expressions and all 483 legal vias.

Prior-floorplan board: `a1eed6e10bfe3e89f22944733574e56db53ed82fea85d1f9445c1f4075f28341`, receipt under `.local/copperhead/full-spacious/v1/prior-floorplan-control/`.

## Diagnosed outer reordering, completed

A finite deterministic search scored 480 whole-group orderings using the 140-open spaced result as feedback. It selected a 156×238 mm layout preserving each group's internal offsets and component angles. Failed-net weighted center span decreased from 13,204.02 to 11,524.15 mm; total center span decreased only from 15,235.07 to 15,025.99 mm. This exposes the tradeoff: several previously routed MCU/hub/SD spans become longer. The objective is a proposal heuristic, not proof of routability or high-speed suitability.

Saved native preflight has the same 499 missing connections, exact non-open findings and complete original invariants. The full 600-second realization finished at 122 missing connections and 516 legal vias, with the same 51 errors. It was rejected because previously connected pad groups from its 140-open routed parent split. A lower count alone did not pass the restoration gate. The separate 111-open prior-floorplan checkpoint remains the best fresh baseline unless a candidate actually beats it. No Stage 2 begins while the required native validity gates fail.

The 51 errors are all intra-footprint: 31 J3 pad clearances, four U4 pad clearances, and four each at J5–J8. Translating components cannot remove them. Earlier experimental pad cleanup belongs to a different geometry epoch and still needs manufacturer/assembly review. The historical 44-open repaired board remains separate and unchanged; it is not joined to this study's curves.

Official assembled-volume score is unavailable: a board with these native defects is ineligible, and assembled height/model qualification is incomplete. No parts, model dimensions, BOM entries or rule limits were changed to invent a score.


## True uniform 1.2× test

The user clarified that the intended experiment is one scalar transform about a fixed center, preserving the prior arrangement. The new arm uses the prior ring-floorplan control's un-routed input, with every anchor transformed as `p_next = (170,102.5) + 1.2 * (p - (170,102.5))` in millimeters. Its outline scales from 140×105 to 168×126 mm. All 245 anchor residuals are zero nanometers; footprint geometry, angles, sides, pads, nets and rules remain unchanged. Native preflight remains 499 opens and the same 51 inherited physical errors.

The fixed-world-scale before/after/ghost-overlay image is `uniform-120/uniform-120-placement.png` under the study root. The completed 600-second uniform 1.2× route has **127 missing connections and 454 legal vias**, with the same 51 inherited errors and no new native findings. This is 16 more missing connections and 11 more vias than the unscaled control. Every input footprint/pose identity and initially connected pad group is preserved. Board SHA: `9e8ea51ba3306e0f00d983a7673ee287d3953649fbb29e4693b695ddc99b254f`. The earlier re-layout result remains a separate experiment and is not evidence about uniform scaling.

A second bounded test uses **1.5×** about the same center, producing a **210×157.5 mm** outline. Its verified input again has 499 opens and the same 51 physical errors. That route is currently running through the shared family-neutral lifecycle executor and the original-full native adapter. The twelve required gates remain explicit; any failed gate keeps validity false and the official score null. This Stage 1 routing comparison is not a Stage 2 score optimization.
