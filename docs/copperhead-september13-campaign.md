# September 13 placement campaign

The retained parent was freshly verified at 55 missing native connection pairs, zero physical errors, 18 warnings, and passing schematic/pad/reference invariants. Its board SHA-256 is `684e7d7c2b23bd54c3d87cf51295e9575c7bb23ef4c6ab3d98d9e30f53037b2f`. It is not a valid or qualified finished board and has no official score.

A 600-second all-net routing control and subsequent changed-placement candidates start from the same immutable parent. The routing budget, layer profile, rules and router flags match. The control is inner routing work, not a placement improvement. Each placement proposal records its control attempt. Warm-start copper removal is also recorded, so equal effort alone does not establish placement causality.

The pinned KRT generator now searches a specified connected group using bounded translations. Previously evaluated translations on the exact same parent are excluded using recorded action parameters. Native failed endpoint involvement prioritizes groups; prior failed group moves lower their priority, and measured changes on incident nets can raise it. The geometric ranking is a proposal heuristic only. Endpoint-pair counts and distances are diagnostic quantities, not electrical qualification or official score.

For local moves, boundary-net copper is detached at the old moved pads, while internal-net copper translates with the group. A bounded cleanup then removes only tracks/vias explicitly identified in native physical-error findings. Every removed UUID, net, geometry and triggering finding is preserved under `placement-collisions/`. This can affect other nets crossing the new location, which are recorded separately in `reroute_nets`. No pad, footprint, net, zone or design rule is deleted to clear a failure. The final independent native placement gate must pass before all-net routing starts; the final routed result is independently checked again. No failed execution promotes a candidate.

The initial standalone CAN0 preflight moved 11 connected components by (+1, -1) mm. It translated 55 internal route items, detached 35 old-pad boundary items, and retained 5,058 other items before collision cleanup. Native collisions required removal of 67 further track/via items. The resulting pre-route board had 107 missing pairs, zero physical errors and 77 warnings; invariants passed. That is an unevaluated routing hypothesis, not an improvement. An independent copper comparison verified that only declared incident/rip-up nets changed and only the 11 declared footprints moved. Original source and retained board remain unchanged.

Run the supervisor from the owned checkout:

```sh
.venv/bin/python scripts/copperhead_campaign.py \
  --source .local/copperhead/candidates/stage1-20260912-182444-f54c2b \
  --until 2026-09-13T09:25:00-07:00 --route-seconds 600
```

The supervisor serializes native evaluations, writes five-second heartbeat and decision records to `.local/copperhead/campaign/state.json`, and stops before another complete evaluation would cross the packaging deadline. Each decision links the exact proposal, parent, prior outcomes, matched control and realized attempt. A native execution failure requests supervisor attention rather than silently scheduling overlapping work. The incumbent is retained separately from every rejected trial. Replay generation follows completed evaluations; W&B publication remains a separate worker with its own verification receipt.

Validation so far: 46 existing tests pass, one skips; the real CAN0 preflight passed fresh native/reference checks after explicitly recorded collision cleanup. Full routing outcomes and actual placement benefit must be read from completed attempt records, not inferred from this preflight.

A circuit-aware review distinguishes 19 shared CAN connector-bus failures from four local choke/transceiver failures. A second standalone preflight changes L6 by (+1, -1) mm and +90 degrees relative to its fixed CAN1 group members. It detaches four old-pad incident items and removes four colliding route items, all on the four incident nets. Fresh native results are 59 missing pairs, zero physical errors, 21 warnings and passing invariants. Geometry comparison verifies all other 244 poses and unrelated net copper unchanged. That is a queued relative-placement hypothesis, not yet a routed gain.
