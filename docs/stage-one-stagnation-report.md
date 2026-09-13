# Why native Stage One is slowing down, and what to change next

Evidence snapshot: **September 12, 2026, 17:41:54 Pacific**. The best verified native candidate at that cutoff is **59 missing connection pairs, zero native physical errors, 11 warnings**. Its circuit/reference invariants pass. It is **not a valid finished board**: connectivity, warning disposition, models/assembly and electrical/mechanical qualification remain open. The independent inner-routing worker continued during report preparation.

Post-cutoff update: during final report checks, the worker reached **58 missing pairs, zero physical errors and 11 warnings** in `stage1-20260912-174325-566c96`. Its saved CAD files were checked against the recorded evaluation hashes. The tables below deliberately retain the frozen 59-pair cutoff for reproducibility; the worker was still running. Latest verified design SHA-256: `09f9378a6e03d557f7cc96ff73610cff802799eec98f5a28cc9dceb7ecab1984`.

The principal measured limitation is an imbalance in search: most effort has repaired copper on essentially the same placement, while only three successful single-resistor placement actions have been evaluated through routing. Remaining opens concentrate in CAN interfaces and shared power/ground. More repetitions of the same net-routing action are unlikely to address all of those constraints. The next system change should make a meaningful connected placement neighborhood the outer candidate, and attach bounded routing/repair effort to it as the inner loop. This does not require a new learning framework.

## Verified evidence and progress

The cutoff includes **85 finalized attempts**, not 85 placement candidates:

| Action | Finalized | Completed reductions in missing pairs | Median elapsed | Total elapsed |
|---|---:|---:|---:|---:|
| Full retained-copper routing | 8 | 6 | 205.1 s | 25.4 min |
| GND escape generation | 3 | 2 | 17.0 s | 0.9 min |
| Targeted KRT routing | 70 | 32 | 19.2 s | 27.5 min |
| Single-resistor placement plus routing | 4, including one producer failure | 2 | 45.8 s | 3.4 min |

These are attempt durations and pair reductions, not independent causal benefits or a sum of retained improvements. Regressions and exploratory branches are included. Some equal-pair results improved only the distance proxy. Seventeen targeted KRT attempts returned identical design hashes.

The trajectory nevertheless represents substantial real progress: the checked baseline had 208 missing pairs; retained candidates reached 125, then 105 after the +3V3 backend trial, then 61. R42 placement and routing reached 60; subsequent inner routing reached 59. Two full routing continuations at 61 made no pair-count progress. R17 improved 124→123 after its corrected producer; R15 regressed 123→124; R42 improved 61→60. There is no evidence that every relocation helps.

The immutable cutoff data, including every contributing attempt, is in [evidence.json](/Users/philippe/dev/copper-scar-demo/.local/copperhead/reports/stagnation-20260913-004154/evidence.json). The best board is [pcbgolf.kicad_pcb](/Users/philippe/dev/copper-scar-demo/.local/copperhead/candidates/stage1-20260912-173505-e742f2/pcbgolf.kicad_pcb), with [its complete attempt](/Users/philippe/dev/copper-scar-demo/.local/copperhead/reports/stagnation-20260913-004154/best-attempt.json). Recorded design SHA-256: `0f0520c5964c13efc9ef37ce0b4fa5f8e94fea23de2b145014e1b061bb056989`.

## Where the remaining 59 opens concentrate

These are native endpoint-pair counts, not distinct nets or proof of the exact obstructing object. Categories are mutually exclusive in the evidence script; reference frequencies can overlap within a pair.

| Cluster | Missing pairs | What the actual reports show |
|---|---:|---|
| CAN bus and controls | 28 | CAN0_H through CAN3_H each have four opens; additional CAN lows, MCU controls and transceiver/choke connections remain open. |
| Shared power/ground | 14 | GND accounts for 12; +3V3 and +5V account for one each. |
| USB data and hub clock | 6 | CH2_D_P has two; CH3_D_N, CH4_D_P, STM_D_N and U4 XTAL2 each have one. |
| Channel SBU signals | 4 | CH2_SBU1 has two, with CH1_SBU2 and CH4_SBU2 also open. |
| Other local/control/power signals | 6 | Includes VLXSMPS, PDR_ON, current-monitor, enable, LED and channel VBUS connections. |
| SD interface | 1 | The remaining CMD branch reaches pull-up R37. |

U3 and J6 each occur in 11 missing-pair descriptions; J5 occurs in eight, J8 in seven and J7 in five. Thus the largest remaining connectivity issue is the distributed connector/CAN interface, not the SD bus alone. Native descriptions and exact net counts are retained in the cutoff artifacts above.

## Measured causes, and limits of the evidence

**Placement generation put a real circuit bundle near the wrong block.** The original generator assigns support parts to the closest IC on the same schematic sheet. R38–R43 are the six SD data/command/clock series resistors, but most were placed around U4, the USB hub, rather than the U3/J2 interface. This is a concrete topology error in the grouping heuristic, not proof that the whole board needs global movement. See [the original generator](/Users/philippe/dev/copper-scar-demo/scripts/copperhead_place.py) and [schematic positions](/Users/philippe/dev/copper-scar-demo/.local/copperhead/runs/schematic-positions.json).

A prepared six-member outer placement preview moved or rotated five members and retained R42. Two deterministic packing orders were compared; positions and rotations were variables. The summed interface-distance proxy fell **472.6→308.7 mm**. All 263 removed copper items belong to the 12 declared SD signal nets; exact comparison verified unchanged copper elsewhere and unchanged nonmember poses. Fresh native evaluation found **75 missing pairs, zero physical errors, 11 warnings, preserved invariants** before routing. This is encouraging placement evidence, but the increased opens are expected after ripping affected routes and the candidate has **not yet earned promotion**. It also leaves pull-ups in their old locations; that is a justified potential expansion, not a claim that the six-series-part group is the final correct SD layout. [Preview, search, effects and evaluation](/Users/philippe/dev/copper-scar-demo/.local/copperhead/audits/sd-bundle-placement-preview/evaluation.json).

**The inner action space is narrow.** The KRT wrapper targets selected nets with fixed 0.2 mm tracks and 0.6/0.3 mm vias, escalation off, no stub-layer swap and maximum rip-up zero. Freerouting runs with fanout and optimizer disabled, one routing thread and bounded passes/time. Those are generator settings, not evidence that the original design rules make routing impossible. They intentionally constrain search, but may leave inaccessible pad escapes or poor retained routes in place. [KRT invocation code](/Users/philippe/dev/copper-scar-demo/scripts/copperhead_krt.py), [Freerouting invocation code](/Users/philippe/dev/copper-scar-demo/scripts/copperhead_route.py).

Preserved-route lock-in is a plausible cause, not yet a controlled experimental finding. A GND trial's producer attempted rescue, reported collateral open nets and reverted the result through its own improvement gate. Thus even the nominal no-rip-up setting is not a strict global mutation guarantee; rescue/cleanup behavior can be wider. The independent whole-board DRC and actual copper delta must remain authoritative. [GND producer evidence](/Users/philippe/dev/copper-scar-demo/.local/copperhead/runs/stage1-20260912-173152-ab618c/krt_reconnect.stdout).

**Longer wall time alone is not established as the solution.** All 70 finalized targeted routing commands completed without producer failure at the cutoff; many returned no useful change. Across 73 KRT runs including placement-associated routing, the producer-reported main-loop duration had a median of 0.24 s and maximum of 0.65 s. This excludes other phases such as refill, rescue and checking, and is not full router CPU time. It nevertheless argues for measuring which search phase exhausted its limit before blindly raising every 180-second command allowance. [Extracted producer summaries](/Users/philippe/dev/copper-scar-demo/.local/copperhead/reports/stagnation-20260913-004154/krt-summary.json).

**Acceptance and feedback encouraged too much routing at one placement.** The old action policy tracks tried nets and stagnation, but mostly selects another net rather than a new placement. A lexicographic distance tiebreak can also credit minor copper/distance changes without reducing opens. Requiring every intermediate placement to beat the routed incumbent would be equally wrong: a placement legitimately starts with more opens after boundary rip-up. Keep its inner budget separate, then compare the completed candidate globally. Preserve a bounded exploratory branch when needed, without promoting it or weakening native defect requirements.

**Some apparent progress was measurement noise.** The completed execution audit found seven historical identical-byte attempts incorrectly labeled improvement because native airwire distance varied. Policy v4 prevents that promotion; v5 scopes old routing feedback to placement/rotation, outline and layers. This repairs attribution and stale feedback, not routability. The audit also records the two earliest source-archive gaps and restored intermediate placement evidence. It need not be rerun to justify these findings. [Completed execution audit](/Users/philippe/dev/copper-scar-demo/docs/native-execution-audit.md).

## Prioritized experiments

Budgets below are proposed local experiment limits, not measured completion guarantees. They retain original circuit, pad identities and manufacturing rules. Actual timeout or failed routing means “not solved under this effort,” not “infeasible.”

| Priority and experiment | Expected benefit and cost | Success criterion | Interpretation if unsuccessful |
|---|---|---|---|
| 1. Finish the prepared SD outer candidate with inner routing | Low implementation cost; one group placement already screened. Allow roughly 10–20 minutes for bounded 12-net rerouting and checks. Tests the correct outer/inner contract and may relieve a real shared detour. | Exact group poses/snapshot and inner effort recorded; no physical/reference regression. Promotion only after global result beats incumbent. Also report whether old opens moved elsewhere. | More than 59 opens or new defects means do not promote. A lower distance alone is insufficient; inspect pull-up branches/escape conflicts and compare the alternative packing order before expanding. |
| 2. Build one CAN neighborhood from actual open endpoints | Highest direct connectivity opportunity: 28 opens. Start with one transceiver/choke and its connected termination/support neighborhood, preserving connector poses initially. Budget 2–3 placement alternatives with equal 5-minute inner effort each. | Reduce the chosen channel's missing pairs and total board opens; unchanged unrelated poses and measured copper effects. Treat H/L as a paired engineering interface, not unrelated wires. | If the same boundary opens persist, expand to the specific adjacent connector corridor or neighboring support parts. Do not move all 245 parts or all connectors as an automatic fallback. |
| 3. Controlled local rip-up/fanout comparison at one frozen placement | Tests retained-route lock-in directly. One baseline and one bounded variant on copied identical inputs, about 5 minutes each. Allow only a declared obstructing neighborhood, with whole-board effect checking. | Better global connectivity at unchanged rules, without collateral physical defects or loss outside the explicitly measured region. Archive exact settings and effort. | No improvement rules out only that local edit/budget. Diagnose pad access, plane connection and route ordering before increasing neighborhood size. |
| 4. Target remaining ground/power pad escapes | Fourteen shared-rail opens give high leverage. Inspect the 12 GND endpoints and plane refill; try a small spatial neighborhood per trial, not global rail deletion. About 2–5 minutes each. | Native closure of targeted pairs, no new clearance/hole violations, and trace/via geometry suitable for the eventual current review. | A conservative generator rejecting all placements does not prove no legal escape exists. Check actual geometry; the current GND helper also needs its layer-aware via-width call fixed before reuse. |
| 5. Target USB/hub-clock geometry as an engineering neighborhood | Six opens plus signal-quality risk. Keep source/load relationships, paired paths, return paths and local clock network explicit; cost includes drawing/constraint review before movement. | Connectivity and independent physical checks pass, with documented pair/clock geometry requirements. | Zero opens without those constraints is not qualification. Broaden placement only with a reason tied to the observed interface. |
| 6. Increase router budget only where limits are active | Run the same frozen input/settings at baseline and larger limits after evidence of exhaustion. Cost approximately proportional to the selected bound, capped per comparison. | Additional useful routes attributable to added search effort, with no rule drift. | No improvement suggests action/placement restrictions rather than insufficient wall time; do not repeat indefinitely. |

Implement the reporting contract in the existing runner: `outer candidate → immutable placement snapshot → inner action list → native after-check → incumbent decision`. Include group membership, original and target poses, affected nets, actual global copper changes, elapsed effort, failure/timeout classification and explicit parent IDs. A small fixed experiment schedule is sufficient initially. A learned selector should wait until these comparable trials provide evidence about which neighborhoods and inner operations help.

## What “fully valid” still requires

Closing 59 pairs is necessary but insufficient. The cutoff warning set contains seven dangling tracks, two dangling vias, one hole-to-hole warning and one library-footprint mismatch. These need explicit disposition; zero error severity alone does not make the hole geometry or footprint correct. Five model assignments are missing: BH1–BH4 and J4. The assembled bounding-box objective cannot be substituted with substrate volume or an incomplete model set.

The original full-board ERC passes its configured checks; some checks were disabled in the source configuration. Experimental footprint repairs still require manufacturer/assembly confirmation. J1's exact part/current budget, per-channel and combined loading, power trace/via capacity, converter loops, decoupling, USB return paths, clocks, connector access and mechanical integration remain unresolved. Hardware proof is unknown. These requirements should be resolved alongside placement/routing so the project does not arrive at a fully connected but unqualified board.

The immediate decision is to evaluate coherent local placement alternatives with controlled inner routing, retain the best verified board, and use matched experiments to distinguish poor placement from restricted routing. No result so far proves that the current outline/layer arrangement is infeasible, and none supports entering Stage Two yet.
