# From unresolved routes to justified placement actions

This extends the convergence report using the completed SD group experiment and the pinned local KRT/KiCad interfaces. It is an analysis and minimal implementation design; no router change, new experiment, rule relaxation or instrumentation framework was introduced. The incumbent remains 58 missing pairs, zero physical errors and 11 warnings.

## The SD example shows why a scalar is insufficient

The group reduced its interface-distance proxy 472.6→308.7 mm but finished with 59 opens versus the incumbent's 58. Its remaining SD opens are specific branches:

- **CMD:** native DRC links a B.Cu track at (146.7, 94.4) to R37 pad 2 at (171.7, 98.5). The router's multipoint report independently identifies R37 at that coordinate, though its pad number is `?`. R37 is the pull-up outside the moved six-series-resistor group. Thus the failed branch is attributable to a known endpoint; this does not establish why the corridor failed.
- **DAT1:** native DRC links a track at (118.6, 131.9) to a via at (114.63, 128.35). The router identifies the disconnected R39 terminal at the latter coordinate. Native item UUIDs distinguish the track and via; coordinates alone should not be used as permanent identity.

The targeted DAT1 retry **found a path in 41 iterations**, then rejected terminal copper on F.Cu. Its fine-parameter rescue found paths in 160 iterations and rejected their terminals too. It did not time out, and the final board bytes were unchanged. Therefore the useful classification is **attempted, path found, terminal validation refused, no output change**—not skipped, not proven search-budget exhaustion, and not proof that no route exists. [Actual retry log](/Users/philippe/dev/copper-scar-demo/.local/copperhead/runs/stage1-20260912-175029-458217/krt_reconnect.stdout).

The printed terminal message says foreign track/via overlap, but the source has an important ambiguity. `_neck_terminal_grazes` puts both actual raw-distance overlap **and refusal to narrow with escalation off** into the same `hard` list. The caller prints the overlap message for either. The observed 0.300 mm distance must therefore not be presented as independently established physical overlap. The exact segment, nearest foreign item, required width and rejection branch are not retained in this attempt's structured output. [Shared rejection list](/Users/philippe/dev/copper-scar-demo/.local/copperhead/tools/KiCadRoutingTools/py_router/single_ended_routing.py:719), [generic message and returned failure](/Users/philippe/dev/copper-scar-demo/.local/copperhead/tools/KiCadRoutingTools/py_router/single_ended_routing.py:2107).

The later `boxed_in_static` hint is also not a causal proof. Its helper produces that verdict from a low iteration count in the no-rippable-blocker path. Here a path had already been found and rejected, and the returned failure contains empty blocked frontiers. Treat that hint as a router heuristic with its provenance, not as an instruction to move a nearby component. [Hint implementation](/Users/philippe/dev/copper-scar-demo/.local/copperhead/tools/KiCadRoutingTools/py_router/routing_diagnostics.py:760).

## Available now, versus what needs implementation

| Evidence | Available now | Limits / small missing piece |
|---|---|---|
| Disconnected native items | KiCad DRC JSON supplies UUIDs, positions, item descriptions and layers; original board supplies pad references/numbers/nets. | A missing pair is not a complete electrical island. Join by UUID and preserve the report's raw pair; do not invent a unique island count from airwire count. |
| Pads and copper belonging to an island | Installed pcbnew bindings expose `BOARD.BuildConnectivity`, `GetConnectivity`, `GetConnectedPads`, `GetConnectedTracks`, `GetNetItems` and ratsnest access. | A small read-only extractor must still assemble and validate component membership, with filled zones included. API existence is verified; a complete island extractor has not been implemented/tested here. |
| Attempted versus unresolved | Current command argv, net scope, exit/timeout state, detailed log phases, full `JSON_SUMMARY`, and final native DRC exist. | Success exit code is not successful routing. Preserve phase/subrun scope; absence from one summary is not proof of skipping. |
| Search limits | Configured limits, elapsed command time and some per-phase iteration counts exist. | Record an explicit solver termination code where absent. Low iterations cannot distinguish frontier exhaustion from a later validation refusal. |
| Blocker candidates | KRT full summaries can expose `blockers`, pre-existing net names, and frontier track/via/unique/near-source/near-target cell counts. | These are phase-local candidates, not proof that moving/ripping one will solve the net. Existing serialization caps lists and may retain the last nonempty attribution; preserve phase and truncation. DAT1 has no named blocker in its saved final summary. |
| Escape / via / terminal refusal | Some current logs name endpoint coordinates, layer, blocked neighbor counts, dog-bone failure and terminal rejection. | Do not turn these into a generic corridor diagnosis. Emit a typed rejection at the exact existing branch, including attempted geometry and relevant constraints. |
| Actual global consequences | Preserved boards, intermediate placement snapshot, native checks and geometric copper deltas already exist. | Use these to validate every candidate regardless of the router's scoped success count. |

For example, CMD's reconciliation summary names STM_D_P, +3V3, CH2_D_N, CAN3_EN, U4-XTAL1 and U4-VDD18PLL as pre-existing blocker candidates. That gives a bounded set to inspect, not authorization to rip those sensitive nets or evidence that a particular nearby part is the cause. [Outer producer log](/Users/philippe/dev/copper-scar-demo/.local/copperhead/runs/stage1-20260912-174807-940294/krt_reconnect.stdout). KRT's [blocker records](/Users/philippe/dev/copper-scar-demo/.local/copperhead/tools/KiCadRoutingTools/py_router/blocking_analysis.py:104) retain useful frontier attribution but do not constitute a geometric impossibility proof.

## Minimal diagnostic record and classification

Reuse the existing attempt directory. Add one compact `route-diagnostics.json` beside the native reports, populated first from already-preserved full summaries and logs. Do not add a service, global tracer, new database or controller. Keep references to the raw lines/JSON and input/placement hash.

For each unresolved net/branch, record:

1. **Identity and scope:** outer candidate, inner action/subrun, board hash, net, native item UUIDs, resolved reference/pad/layer/position, and island membership only when measured.
2. **Disposition:** `not_requested`, `skipped_explicitly` with reason, `attempted_no_path`, `search_limit_reached`, `path_found_validation_rejected`, `producer_timeout/error`, `changed_but_still_open`, or `unknown`. A net can have different dispositions across phases; retain them rather than flattening to one story.
3. **Observed evidence:** elapsed/iterations, configured grid/width/clearance/via/layer restrictions; rejected terminal segment or via coordinates if available; blocker candidates and attribution type; explicit missing fields.
4. **Interpretation and action:** a hypothesis separately labeled from observation, the smallest relevant neighborhood, fixed related nets/constraints, one proposed change, and its matched comparison/success criterion.

Two small producer additions would materially improve this record: split terminal refusal into `physical_overlap` versus `narrowing_disallowed`, and preserve the responsible segment, distance, requested/allowed width, clearance/floor and nearest foreign item identity at that existing validation branch. Preserve explicit search termination status instead of inferring it from iteration count. Changes to pinned KRT would require a separately recorded patch/provenance revision and focused fixture checks; they are proposed here, not silently applied.

## How the evidence should choose an action

| Observed failure | Justified next action | Evidence needed to accept the inference |
|---|---|---|
| Not requested / explicitly skipped | Correct the inner net or layer scope. Do not move placement to fix missing work. | Confirm the formerly skipped branch is attempted; whole-board DRC remains authoritative. |
| Path found, terminal refused | Inspect/reproduce the rejected terminal with original rules. Compare a different legal approach or a small move/rotation of the identified terminal's component. | Typed refusal and geometry tie the proposed edit to that terminal. Improvement must survive native checks; do not accept the router's generic suggestion to lower clearance/width. |
| Named frontier copper blockers | Compare identical placement with one declared local routing-neighborhood change. | Actual copper delta and global outcome show whether the candidate blocker mattered. If no benefit, retain it as an unconfirmed attribution. |
| Explicit search limit reached | Compare the same input/settings with a larger bound. | Additional search reaches useful connectivity; otherwise no inference that the placement is impossible. |
| Escape or via rejected with a measured constraint | Change the offending local approach/pose while preserving decoupling, paired signals and power relationships. | Candidate via/escape geometry plus the violated layer/clearance/hole constraint, not proximity alone. |
| Cause unavailable | Run a matched, bounded experiment changing one factor: terminal pose, route approach/order, or a declared local copper neighborhood. | Same starting board and equal inner effort; compare global opens/defects and exact effects. Failure only rejects that experiment. |

For DAT1, the immediate information gap is the **terminal-rejection branch and geometry**, not another shortest-distance score. For CMD, the known failed R37 pull-up branch means the next potential neighborhood should consider that branch and its actual approach, rather than re-moving all six already-routed series elements. Neither proposed experiment has been executed as part of this analysis.

The outer loop should consume this compact evidence to choose the next coherent neighborhood; scalar cost remains useful for acceptance and prioritization. Neighborhood membership follows the failed terminal/island and verified electrical relationships, expanding only after measured local alternatives fail. Connected, zero-error geometry still requires assembly, signal/power and mechanical qualification before Stage Two.
