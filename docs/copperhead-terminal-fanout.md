# Native terminal topology experiments

The September 13 control retained 55 missing native connection pairs, zero physical errors and 18 warnings. A CAN0 group move finished at 77 missing pairs, L6 at 58 and L7 at 57; all were rejected. Circuit island analysis found isolated connector pads and ground islands despite connected bus trunks and ground planes. That evidence motivated a supported terminal fanout operation before full-board routing.

`scripts/native/CopperheadFanout.java` invokes the installed Freerouting 2.4.1 `RoutingBoard.fanout` API. It does not implement path search. The Python wrapper checks the exact proposed parent board, records the source and JAR hashes, and uses existing DSN via rules. The current wrapper reads the project's hole and copper-edge constraints into the routing job before DSN loading, then initializes board-specific settings. Per-terminal execution is bounded to 30 seconds; rip-up and automatic neckdown are disabled. Setting `strictDrc` alone does not provide the CLI router's rollback behavior for this direct API, so independent native checking is mandatory.

The stage-one action is labeled `outer_topology`, not a component move. Its sequence is export, scoped fanout, import, immutable intermediate project snapshot, native invariant/physical check, fresh export, full-board 600-second routing, import and final native check. Component and pad poses/net identity are preserved through the bridge. SES import may normalize existing copper; it is not an append-only operation. Every attempt retains its implementation source, proposal and intermediate board separately from the incumbent.

## Representative probe

Attempt `stage1-20260913-041948-8b21b9` failed because the board-specific settings constructor left a nullable pull-tight setting unset. No board was accepted. The corrected attempt `stage1-20260913-042140-425473` uses stock `DefaultSettings` initialization:

| Terminal | Net | Engine result |
|---|---|---|
| J5.A2 | CAN0_H | Failed to find a fanout |
| J8.A6 | CH4_D_P | Failed to find a fanout |
| U15.3 | GND | Routed |

The intermediate native result is 54 missing pairs, zero physical errors, 18 warnings and passing invariants. The immutable `fanout-project/` snapshot has aggregate design hash `56043e47761f9e98121555b6d836b776241dd4d70bcd3a6b39eb8840ad03aa77`. Full routing was still running when this checkpoint was written; the final attempt record is authoritative. The initial probe used stock loading defaults; explicit original hole/edge settings were added afterward and are not retroactively claimed for this probe. Native project rules and acceptance checks were unchanged throughout.

Independent review verified footprint poses, pad UUID/net/position/layers and original project bytes. The SES intermediate has 97 removed and 61 added exact copper geometry records across 38 nets, including normalization; those counts are not a claim that fanout intentionally rerouted 38 nets.

## Input clearance diagnosis

A read-only load of the control DSN reproduces all 297 Freerouting internal clearance reports before routing: 565 directional reports reduce to 297 item-pair/layer records, 75 sharing a net and 222 on different nets. Native rules remain authoritative; same-net membership does not automatically invalidate a report.

For J3.B11/B12, native and DSN geometry are 600 micrometer circles separated by an exact 206.225775 micrometer copper gap; native effective-shape measurement gives 206.225. Both native pad clearance values are 200. Freerouting retains the original Circle shape but uses an `IntOctagon` tile in its clearance/search geometry. Enlarging and intersecting those tiles produces a reported 177.835083 micrometer gap. This is a concrete internal representation discrepancy, not a reason to lower the 200 micrometer requirement. Other reports have not all been reconciled.

Evidence lives in `.local/copperhead/reports/freerouting-input-audit/`, including the read-only Java inspector, native shape measurements, original directional records, detailed tile shapes and official versioned source excerpts. None of the audit changed engine geometry, source rules or DSN primitives.

Validation at this checkpoint: 49 tests passed, one skipped; Java wrapper compilation passed; the representative intermediate passed independent native checks. The board remains incomplete and has no official score or completed-board qualification.
