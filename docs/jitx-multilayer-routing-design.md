# Completing the JITX multilayer routing evaluator

Research/design checkpoint,2026-09-12. The source checkpoint was pushed and remotely verified **before this investigation**: `d70fde77cf4936473c0b5e7c78b01639fb21c719`, branch `codex/jitx-optimization`. This investigation used installed4.4.0 Python/viewer sources, saved native API responses and primary upstream documentation. It did not mutate accepted native state or launch a routing planner.

**Conclusion:** the current harness correctly issues the installed single-layer route operation, but it is **not a complete multilayer routing evaluator**. Registering a via definition alone will not fix that. Actual via instances, net attachments, layer transitions and a complete terminal selection must be prepared; then all required per-layer legs must be attempted and the realized full board checked. Prior incomplete runs do not establish placement infeasibility.

## What the native workflow actually provides

[JITX's topological autorouter documentation](https://docs.jitx.com/en/latest/essentials/physical_design/autorouter.html) describes one-layer legs between selected pads, vias or controls. Search and geometric realization are separate; heuristic termination can fail on feasible geometry, and a displayed RBE can remain after realization failure. The docs recommend a two-terminal diagnostic when broad selection gives ambiguous feedback. These are documented semantics, not a verified guarantee of complete search.

The installed VSCode4.4 source map resolves these concrete operations. The websocket route is `design/<qualified_design_name>` and message namespace is `phd`:

| Operation | Exact relevant body | Role and limit |
|---|---|---|
| `load` | `{}` | Current board, definitions, placements, routed records, net groups and progress. Read all complete/update messages; do not mix stale generations. |
| `reposition` | `{groups:[{id,pose:{center:{x,y},angle,flipx:false},side}]}` | Component/group outer placement. Uses existing IDs; native geometry may be recreated. |
| `route` | `{layer,pads:[terminalIDs],force:false,configure:null}` | Connect legal selected endpoints on one layer. Field `pads` can contain pad/via/control endpoints in the viewer; it is not a full-board multilayer planner. |
| `via-drop` | `{drops:[{origin,layer,instance}],def:definitionName,axis?,"start-step"?,"fixed-direction"?,configure?}` | Auto-via from selected routable origins. Cardinal/diagonal direction and initial step may be specified. |
| `via-add` | `{origin,layer,instance,"global-point":{x,y},"force-place":false,"def-name":name}` | Explicit local via from drag. Creation/attachment must be verified in resulting state. |
| `via-create` | `{create:[{"def-name":name,origin,layer,pose,turns:null}],configure:null}` | Explicit placed via and optional connecting route; viewer reads `via-info` for created IDs. |
| `route-rbe` | `{layer,start,end,turns,configure?}` | Guide a leg around obstacles. It is still native topological routing, not arbitrary copper-file editing. |
| `unroute` / `via-delete` | `{layer,routes:[IDs]}` / `{vias:[IDs]}` | Targeted repair of known owned objects. Not a blanket reset; code-placed vias are not UI-deletable. |

Source references: `services/autoroute.ts`, `services/vias.ts`, `services/control.ts`, `utils/regions.ts`, `services/route-configuration.ts` within the installed `main.efcfdae6.js.map`. The compact extracted evidence is local under `runs/stage1/via-workflow-diagnostics/`; proprietary installed sources are not republished in Git.

The [Auto-Via documentation](https://docs.jitx.com/en/4.0/user-interface/board-view/auto-via.html) confirms adjacent placement of the active via type, cardinal or diagonal, and a local route if space permits. The installed implementation filters origins using `routableLayers`, applies anchor-side/layer normalization, and sends one `via-drop` request. It does not select a global topology, decide how many layer transitions a net needs, cover all remaining islands, or iterate repairs to completion. No claim about its undocumented search radius or completeness is warranted.

Source-level `Via` specifies `start_layer`, `stop_layer`, diameter and hole. `Net += via` or `PortAttachment(port,via)` associates an actual instance; `Route(source,destination,layer)` specifies a leg. Installed `jitxlib.via_structures` supplies structures such as ground cages, not an arbitrary-board autorouter. The official [BGA escape example](https://docs.jitx.com/en/latest/_modules/jitxexamples/demos/si_bga_optimization/bga_escape.html) explicitly constructs via instances, attachments, controls and layer-specific routes. Its HDI assumptions and latest-doc revision are not proof of compatibility with this manufacturing profile or installed package.

## What the completed runs covered

The read-only `integrations/jitx/audit_routing_scope.py` regenerates these facts from saved before/selection/response records:

| Saved run | Native nets selected | Native terminal IDs | Requested layers | Via definitions | Observed route acknowledgements / export wait |
|---|---:|---:|---|---:|---|
|008 broad floorplan |191/191|942/942|0,1|0|1.61s +7.15s /333.61s|
|009 connected power neighborhood|7/191|296/942|0,1|0|2.96s +35.22s /15.09s|

Both exported boards contain no vias.008 selected all current native net terminals, so it is a whole-board **single-layer sweep**, not complete multilayer routing.009 is a scoped repair. All942 native terminal IDs resolve to physical pad objects. Of1066 named physical pad objects,111 omitted objects have pin references but are not in active native net groups;13 have no native pin reference. These counts align with the separately recorded no-connect/unmapped-pad import distinctions; neither942 nor1066 alone proves complete source topology. The independent245-ref/1066-pad/191-partition original-source invariant check remains necessary.

For the active native942 pad IDs,903 expose local copper on layer0 only and39 on layers0/1. With no vias, a bottom-layer call cannot magically reach the903 top-only pads. The current helper submits the same pad list on each layer, matching the broad viewer operation, but never builds a per-layer coverage manifest or adds transitions. New selection must include current legal via/control IDs and apply anchor-side normalization; it must account for every required source-net island, not blindly route every no-connect pad.

Both runs recorded `Some requested pads were off the board and could not be routed.` on both layer calls; bottom calls also recorded `Unable to find any valid routes for the selection.` These notifications were saved but not promoted into a structured failure classification. Wrong-layer selections can be irrelevant on the bottom, but this does **not** explain the top-layer warning conclusively. Whether particular endpoints are outside geometry, rejected during realization, or unavailable for another reason remains unresolved. Audit current transformed pad envelopes, board/signal bounds and native endpoint eligibility, then use one representative two-terminal diagnostic per failure class. Do not equate a successful request envelope with coverage.

Native progress reported237 remaining unroutes after009 versus310 independent KiCad missing-connection findings. Different representations/check rules mean these counts must be kept separate; native zero would still require exported full-board validation.

## Completion, effort and cancellation

Current helper calls `asyncio.wait_for(consume(),55)` for each load/route conversation. It then invokes installed `do_export('kicad',name)`, waiting/retrying when the runtime reports physical design tasks in progress, with a600s export wait ceiling. Its owning subprocess has a900s wrapper timeout. This is one sweep through requested layers, not600seconds of deliberate topology search, and it has no native maximum-pass setting.

The installed route configuration exposes neckdown, widths/spaces, pour, squiggle room and endpoint targeting. No supported search-time or iteration-limit field was found there. Native heuristic termination is documented but its numeric limits are not exposed by the inspected code. Do not invent a `max_iterations` setting or represent elapsed wall time as comparable exhaustive search effort.

Acknowledgement is insufficient:008's export remained busy for333.61s after the short acknowledgements. The later successful export and independent board checks establish the final saved geometry at that checkpoint. A preliminary `after` load can precede realization completion and must not be the final board.

Killing the wrapper process group does **not** demonstrate native cancellation: the persistent physical client is a separate process. Python conversation `close()` explicitly closes without sending a command unless supplied one. No native task-cancel operation has been qualified here. On timeout, report `native_state_unknown/potentially_busy`, keep the per-design mutation lease, and perform supported read/status/export completion checks. Do not start another mutation merely because the controller subprocess disappeared. A complete evaluator needs a tested completion barrier and recovery protocol; process liveness and controller heartbeats are not native progress.

## Recommended division of work

Keep component placement as the outer candidate. Start with a generous, legal full-board arrangement; compactness and via-count optimization are StageTwo concerns. Preserve electrical/connector/thermal placement requirements and original manufacturing rules. The inner evaluator owns routing topology, layer assignment, via siting and leg routing for that fixed component placement. Via XY choices depend on pad escape and congestion, so they are not passive metadata.

1. **Preflight and capture.** Acquire one per-design writer lease. Record source/rules/stackup/placement hashes, native generation and immutable outward checkpoint. Build an identity map from source terminals to current pad/via/control endpoints and per-layer copper islands. Reject missing identities, intrinsic footprint violations that invalidate a test, illegal spans and unresolved busy state explicitly.
2. **Whole-board coverage plan.** For every intended active net, connect its current islands with a topology (a tree is an initial heuristic, not a guarantee). Treat required differential-pair/topology/return-path constraints separately from generic signal nets. Reuse verified native copper, through-hole terminals and existing vias where legal. Record each required leg, layer, endpoints and any transition still missing.
3. **Instantiate transitions.** For islands with no usable path on the assigned layer, choose legal via sites near escapes or a blockage. Use native auto-via first where its local policy fits; otherwise explicit via creation. Verify emitted IDs, net attachment, span, pose and actual pad-to-via copper. Deduplicate by net/site/span and bound created instances; repeated calls must not accumulate anonymous vias.
4. **Attempt all remaining legs.** After transitions, reload current endpoints and route every remaining net on relevant layers, including via endpoints. Use `force:false` and no rule-relaxing overrides. Compare returned notifications and realized geometry against the coverage plan. Some local repair may occur inside the evaluator, but it must return a whole-board evaluation, never silently narrow the reported scope to incident nets.
5. **Bounded inner repair.** Classify missing transitions, no legal endpoints, unavailable escape space, topology-search failure, realization failure and timeout separately. Change via site/layer assignment or targeted owned routes first. A bounded alternative topology/order may resolve a dead end; identical retries are not progress. Stagnation uses connected-island changes and geometry/plan hashes, not only native counters.
6. **Evaluate and feed back.** Wait for quiescent export; run original-rule DRC/ERC, topology/identity invariants, realized copper and through-via checks, plus assembly/electrical gates. Return all unresolved nets and classified causes to the placement proposer. Only persistent spatial failures justify a controlled spacing expansion or relative arrangement change. Via/component updates can be coupled at that boundary; avoid an unbounded joint optimizer inside a single measurement.

There is no convergence guarantee. Retained topological routes can constrain subsequent choices; frozen poses plus a poor topology can fail even with ample board area. Native re-realization may alter unrelated copper geometrically, so compare electrical islands and preserved-route intent as well as exact primitives. Fair comparisons require the same topology policy, rule profile, layer set, seeds/order and bounded attempts. More vias are acceptable for StageOne if legal; do not trade away current/return-path or clearance requirements.

## Manufacturing spans and reusable options

For the presently considered ordinary JLC stackups, the [published capabilities](https://jlcpcb.com/capabilities/Capabilities) support through holes and distinguish their via dimensional guidance from the PTH annular-ring table. The proposed0.60/0.30mm through-via gives0.15mm ring, exceeding the original0.0762mm requirement. A through-via spans top to bottom even if a route only uses top and inner1; unused barrel/pads still affect intermediate layers. Do not create all start/end pairs: that could imply unsupported blind/buried fabrication. Layer-use assignment and physical drill span are different fields.

- **Preferred native integration:** reuse installed auto-via, explicit via/route APIs and source `Via`/`Route`/`PortAttachment`; add a small deterministic topology/coverage controller. This preserves JITX native geometry but still requires qualified reload, completion and targeted repair behavior. Existing via-structure/BGA patterns are useful examples, not a generic planner to call.
- **Open-source reference or alternate evaluator:** [Freerouting's architecture](https://github.com/freerouting/freerouting/blob/master/docs/architecture.md) includes fanout, unfinished-net passes, multilayer maze/drill search and repair. Its [CLI](https://github.com/freerouting/freerouting/blob/master/docs/command_line_arguments.md) accepts DSN/SES, layer controls and rule input. A local pinned invocation can provide a comparison without a paid API. This is an alternate backend unless a supported round-trip into JITX is verified; do not copy its output into native design files. DSN geometry/rules, custom pads, nets, vias and layer restrictions require independent round-trip validation. Review its [GPLv3 license](https://github.com/freerouting/freerouting/blob/master/LICENSE) before embedding code; a subprocess comparison has different integration boundaries from copying its implementation.

## Minimum proof before another campaign

A bounded proof is proposed, not executed by this research report:

- Use a separately named fixture, never overwrite accepted002. Include two top-side net endpoints whose front path is blocked but whose back path is clear; one legal through-via definition exists initially, but no instances. Include an independent already-routed net to audit preservation. Add two more nets with conflicting escape choices so a fake one-net success cannot pass as whole-board coverage.
- First verify source reload on that disposable fixture and that definition-only per-layer sweeps leave the cross-layer net open. Then create/attach real vias, route top escape legs and back trunks, and verify every net connected in exported copper with0 incorrect/physical/annular errors. Record exact selected IDs and native task completion. Check attempted local repair does not drop the independent net.
- Bound the proof to one initial topology plus at most two classified site/layer alternatives and a20minute controller budget. These are proposed controller limits, not claimed native solver controls. A timed-out native job must remain quarantined until actual completion/recovery is verified.
- After that passes, one deliberately spacious full-PCBGolf trial can evaluate all191 active partitions with legal transitions. If only a new identity can load the via-enabled source safely, report the tradeoff before running it: **fresh routing state, preserved accepted009 elsewhere, no retained-copper speed/comparison claim**. No via-count or area minimization in this proof. Compare whole-board results, and retain the intrinsic44-footprint-error caveat until geometry is independently repaired.

Accepted009 remains untouched and incomplete. The production blockers are a usable legal transition graph, qualified native state/completion handling, and unresolved footprint/assembly/electrical validation—not user permission. This report deliberately precedes any large planner implementation.
