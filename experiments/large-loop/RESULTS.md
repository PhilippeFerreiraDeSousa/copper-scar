# large-loop stage-one pilot

The new PCB Golf-inspired input has 156 populated components, 164 nets, 636 assigned pins and a 105 x 110 mm two-layer outline. All original CAN and protected-port/SBU blocks from sheets 4/5 are retained, plus the eight original SBU sense resistors. Seven populated controller/supply headers and the explicitly populated original CAN header define the external boundary. All 156 model references resolve. The added header model is a generic visualization model, not a qualified official assembly-volume envelope.

The input passes native schematic parity and ERC. Independent checks retain the source net partition, project rules, all numbered electrical pads and all unnumbered mechanical holes, including local position, orientation, size, drill and layers. The two-layer full-board router uses the same 240-second / 100-pass / one-thread ceiling, nominal 0.20 mm width, 0.60/0.30 mm vias and no optional undersized fanout stubs for every comparison. Natural early backend completion is recorded; equal ceilings do not imply equal consumed CPU time.

## Measured outcomes

| Trial | Native opens | Required footprint findings | Total native loss | Decision |
|---|---:|---:|---:|---|
| Unrouted input | 472 | 84 | 556 | Initial state |
| No-placement routing control 1 | 109 | 84 | 193 | Reference |
| No-placement routing control 2 | 109 | 84 | 193 | Reproduced reference |
| Six diagnostic-weighted resistor swaps | 345 | 84 | 429 | Reject |
| Q4/R92 targeted relocation | 95 | 84 | 179 | Retain |
| Q6/R118 targeted relocation | 120 | 84 | 204 | Reject |
| 90-degree port-bank rotation | 124 | 84 | 208 | Reject |
| CAN choke / power-bypass regrouping | 174 | 84 | 258 | Reject |
| Q3/Q5 gate orientation + Q8 spacing | 86 | 84 | 170 | Retain |
| Unchanged retained-placement repeat, shared executor | 87 | 84 | 171 | Keep original incumbent |

The measured placement trajectory is **109 -> 95 -> 86 opens**, separate from the initial routing-only improvement of 472 -> 109. Q4's two drain-net opens and two relay-control opens disappear after its retained relocation. The Q7 plan was pruned when the current native report showed its target net already connected. Failed translations and rotations prompted different grouping/access proposals; a shorter HPWL proxy was never accepted as a routing result.

The repeat used the identical retained placement and identical effective DSN apart from its output pathname. Its 87 opens show one-open variation at the fixed routing deadline; both 86 and 87 remain below the two 109-open controls. This is a bounded pilot result, not a general placement-policy superiority claim.

No candidate is fully valid. The source contains 16 internal hole-to-copper clearance errors in J5-J8 (0.2094 mm versus the preserved 0.25 mm rule), plus 68 required internal silkscreen findings. An isolated native DRC of the complete original source reproduces all 16 hole findings with the same object UUID pairs and measured clearance. See connector-findings.md. These 84 findings remain in every loss and acceptance result. No pad/drill, constraint, BOM or layer change was used to hide them. Stage2 has not started; there is no qualified official score.

Stage1 stops immediately at the first independently fully valid result, including when a caller selects an older invalid parent afterward. This guard was checked against the actual accepted medium fixture plus its native ERC report, and against misleading accepted/zero-open flags on the invalid large evaluation. Shared executor tests cover missing gates, source drift, first-valid handoff and qualified-score-only Stage2 retention.

## Reproduction and evidence

The immutable artifact root is `.local/large-loop/v1`. Each completed stage has preview/output KiCad boards, full project/library/model copies, PNG/SVG, native connectivity/DRC/ERC reports, acceptance/evaluation, command receipts and completed.json. `source-receipt.json` binds producers at stage start in newer records; earlier completed records also retain source file digests and proposal provenance. `provenance-addendum.json` distinguishes proposal and completion commits where needed.

`replay-final.json` (10 completed states) and preserved earlier replay indexes contain candidate and retained opens/loss separately. `live-status.json` is the canonical current-operation/incumbent discovery file; the dashboard reads direct child `*/completed.json` files. Failure records and pruned proposals remain available. The frozen small/medium film and all other worktrees were preserved.

The isolated JITX input is built as `large_loop.design.LargeLoopInput` under `.local/large-loop/jitx`, with its own designs directory and runtime. Its standalone board UI was visibly verified on port 61593. The proper KiCad application executable was launched with the full absolute v1 project path; the UI inspection tool remained bound to an older KiCad process, so separate large KiCad window visibility was not independently confirmed. JITX import/build is input-only; no full routed round-trip equivalence claim is made.

Shared executor/native geometry files were adopted from medium source 6d59511. Large retains its family-specific rule/geometry/error-floor adapter, and a canonical-record bridge keeps existing dashboard data compatible. The shared repeat uses no official score and cannot turn diagnostic retention into validity.

The shared repeat bound its source files without drift. Its first shared report incorrectly failed width/vias because the large adapter assumed legacy B.Cu enum 31; KiCad 10 uses enum 2 here. Commit e57e766 fixes the adapter by resolving IDs through the saved board layer names. A separate read-only native review verifies all 349 via endpoints are F.Cu to B.Cu, all vias are 0.60/0.30 mm, and track widths pass. The original report is preserved; `shared-results/retained-repeat-via-review/review.json` records the correction. The actual failed gates remain connectivity and physical findings, with validity false and official score null. The canonical bridge now takes acceptance and score from the shared completed result after every required gate, including source drift.

The shared Stage2 qualified-baseline guard from medium d7731b4 is adopted; all 12 shared executor tests pass. This pilot is finished with Stage1 incomplete and Stage2 unstarted. `live-status.json` reports `requires-input-qualification`; the retained project is `placement-06/pcbgolf.kicad_pro`. Further progress toward full validity needs both remaining routing work and a qualified resolution of the source footprint findings. No source geometry, manufacturing constraint or BOM repair has been established or applied.
