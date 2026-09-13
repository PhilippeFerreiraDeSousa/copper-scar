# Native execution and evidence audit

Audit performed September 12, 2026 (Pacific). This closes specific execution-contract defects before adding any learning controller. The full board remains **not valid**. R42's completed placement candidate has 60 missing native connections, zero native physical errors and 11 warnings. Assembly, electrical/mechanical review and hardware qualification remain open; Stage Two has no accepted baseline or official score.

## Findings and repairs

- Preserved before/after CAD files match their recorded native evaluation hashes. Commands retain arguments, elapsed time, exit status and native reports (KiCad 10.0.6). Original circuit/pad identities, support files and rules are checked separately from router success.
- Seven historical attempts incorrectly received diagnostic-improvement credit when board bytes were identical and only the measured airwire distance changed. Historical records remain intact. Policy v4 classifies identical-byte variation explicitly and prevents promotion or exploratory continuation credit from it. Connection counts and physical defects take priority over this distance proxy.
- The first two v1 attempts predate controller-source archiving. Their input/output and reports exist, but complete historical source replay cannot be claimed. Subsequent archived sources match their recorded hashes.
- R17 and R15 intermediate placement boards were not originally retained. Running each archived placement producer on its preserved input recovered byte-exact boards matching all original intermediate CAD hashes. Policy v4 now preserves the placement project before inner routing; the real R42 run verifies this path.
- The router's selected nets are targets, not a guaranteed mutation boundary. One historical action changed copper on unselected CH1_SBU2 and Net-(LED14-AG) through cleanup. Native missing counts on those nets remained 1 and 0 respectively. New effects records report actual geometric copper changes and component movements, independent of item UUIDs, segment direction and numeric serialization.
- New records explicitly link the incumbent before and after each attempt and state whether promotion occurred. Failures retain evidence and never promote. Candidate copies exclude stale generated reports and previews.
- Policy v5 scopes tried-net and stagnation feedback to the actual placement/rotation, outline and layer configuration. The existing validated backend remains available after a move. Old placement failures therefore do not prematurely exhaust a new placement candidate's inner routing options. Derived geometry keys in historical feedback are identified as enrichment and the pre-enrichment feedback is preserved.

## Two levels within feasibility

An **outer candidate** changes placement: position, rotation or a coherent connected group. Its **inner effort** updates retained copper, makes bounded router repairs and performs native evaluation. Router timeout or failure records exhausted effort, not proof that placement is unroutable. Historical routing attempts are inner evidence; they are not counted as distinct placement proposals.

Next neighborhood selection should use concentrated missing endpoints and schematic relationships. Start with a meaningful connected group whose interface can be described, preserve unaffected poses and copper, and broaden the group only when measured local alternatives stagnate. Component count is a consequence of topology and access constraints, not a fixed one-part/all-board switch. Group-specific engineering requirements must be checked; current clearance screens do not qualify power paths, USB pairs, clocks or decoupling.

## Replay limits and evidence

Artifact replay can show exact saved boards and measurements; it is not a claim that rerunning a router produces identical output. KRT uses fresh processes with retained board copper, not retained internal solver state. The backend source, binary and dependencies are pinned and checked. Router-generated project settings are not adopted; only the resulting board is transferred and independently checked against original support/rules.

Evidence lives in `/Users/philippe/dev/copper-scar-demo/.local/copperhead/`:

- `audit-summary.txt` points to the latest finalized-attempt audit and reports exceptions.
- `audits/reconstructed-placement/` contains recovered intermediate boards and hash proofs.
- `audits/repeatability/summary.json` contains repeated native checks of identical input.
- `runs/stage1-20260912-172529-201931/attempt.json`, `placement-project/` and `effects.json` record R42's actual placement and inner routing result.
- `audits/feedback-before-geometry-enrichment.json` preserves feedback before geometry-scope enrichment.

Focused contract tests pass, including same-byte measurement variation, actual unselected copper effects, geometry scope changes and new-placement feedback isolation. These are software/evidence checks, not board qualification.
