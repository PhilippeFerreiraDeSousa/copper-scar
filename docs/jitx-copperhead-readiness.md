# Copperhead–JITX integration readiness

**Joint recommendation: do not merge branches yet.** Both tracks agree to a small isolated fixed-proposal bridge after the successful incremental fixture, while continuing separate implementation. Code paths currently do not overlap, but that does not establish functional compatibility. No branch merge or real-board proposal application was performed.

Copperhead owns proposal generation and native placement checks. JITX owns incremental multilayer realization and failure diagnostics. Copperhead's `docs/copperhead-placement-exchange.md`, `scripts/copperhead_apply_pose.py`, and actual `sd-rigid-pose-v1.json` exchange were read directly. Copperhead independently read JITX's native fixture exports and DRC. Each side agrees that partial routing and a geometric proxy cannot prove placement feasibility.

## Actual readiness evidence

The Copperhead exchange identifies parent SHA `53abd9aef573fc55ae80345d22bb077db289198462fd4cf50a72bde3c3ab3744`, all 245 component UUIDs/poses, 1078 physical pad entries, constraint digests, six layers, and legal 0.60/0.30mm through vias. Its fixed proposal translates 13 SD-interface components by +15mm X with 232 references locked. It refers to Copperhead's expanded parent, not JITX's accepted parent.

A read-only comparison against accepted JITX 009 SHA `55f322cefea95659992382db38118566a0e93824790164809ba831b9d85e8fc0` found:

- All 245 component references and all 13 proposed SD references resolve to current JITX native group IDs. No named pad key is missing from the normalized export.
- Both exported models contain 297 named net groups and 196 groups with multiple named endpoints, with **exact matching endpoint memberships**. Removing the 111 explicitly no-connect pins from the original schematic yields the 191 active partitions. Five otherwise multinode NC groups are the J3 B2/B2T, B3/B3T, B8/B8T, B10/B10T and B11/B11T pairs.
- JITX's 942 active native terminal IDs equal the 1053 assigned source pads minus those 111 NC pins. The 1066 named physical pad objects additionally include 13 without native pin references. These are explicit representation distinctions, not permission to omit required pins.
- The original 1078 physical pads comprise 1066 named and 12 unnamed entries. JITX's normalized export has 1090 entries: the same 1066 named plus 24 unnamed. Twelve extra unnamed cutout/pad representations occur at J1, J3 and J5–J8. Their geometric/manufacturing equivalence is unqualified and related footprint errors remain.
- Parent component geometry differs, Copperhead uses six copper layers while accepted native JITX 002/009 uses two, and accepted native JITX has no via definitions. Matching references and net memberships alone does not make the supplied absolute pose request applicable.

JITX can accept a pose change without a full import/reset **on a correspondence-qualified existing identity**: `phd.reposition` uses current group IDs, global center/angle/side; `reposition_groups.py` already did this for full-board 008/009. No KiCad UUID is passed as a JITX group ID. Hierarchical source placement uses owner-local frames; global native/export transforms must be resolved explicitly, including Y reflection and component-local pad origins. The small fixture also proved native via anchoring, incremental copper preservation, and legal definition addition with accepted pose authored before rebuild. It does not remove the full-board cache-reload risk.

Copperhead reports its SD move passed native placement gates, then a 180s whole-board routing attempt yielded 472 opens/0 errors/7 warnings versus 477 for the expanded parent, rejected against its retained 55-open board. Eligible input scope is whole-board, but per-net attempt coverage is unexposed and effort expiry is not completion to feasibility. Boundary-copper removal and a different retained-copper parent confound a causal placement-quality conclusion. These Copperhead results were supplied by the owning task; the JITX track did not rerun its routing.

## Smallest next proof

1. Have Copperhead emit one immutable pose request for the existing synthetic fixture, with exact parent board hash, all eight ref/pad/net memberships, fixed references, source constraints, coordinate frame and intended TP4 target. Translate the request into current JITX native IDs only after validating the entire parent correspondence. This tests the exchange adapter, not a new placement search.
2. Apply through native reposition, retaining existing routes/vias. If transitions are missing, use verified legal definitions and actual via endpoints. Capture complete net scope, preliminary/unrealized routes, completion barrier, all changed copper and preserved routes. Run whole-fixture independent DRC and topology checks, and return input/output hashes and structured diagnostics to Copperhead.
3. Let Copperhead independently consume and verify the returned board and retain/reject decision. A passed synthetic bridge is an interface proof only. Before an original-board subset or whole-board trial, resolve the 12 unnamed-pad geometry discrepancies, source/native layer profile, footprint defects, global pose frame and reload strategy. Preserve both accepted parents. Any rebase of the +15mm proposal is a new explicit experiment, not the same evaluated proposal.

The minimal exchange remains a file-level request/result contract, not a shared framework. A routing score under a declared budget is evidence about that evaluator and parent state; actual feasibility requires complete realized coverage and all board gates. A real full-board fresh identity would discard retained routing and invalidate incremental-performance comparisons; diagnose or propose that tradeoff before using it.

Read-only audit: `/Users/philippe/dev/copper-scar-jitx/runs/incremental-proof/copperhead-readiness.json`. Copperhead exchange: `/Users/philippe/dev/copper-scar-demo/.local/copperhead/exchange/sd-rigid-pose-v1.json`. Its independent fixture audit: `/Users/philippe/dev/copper-scar-demo/.local/copperhead/reports/jitx-fixture-readiness.json`.
