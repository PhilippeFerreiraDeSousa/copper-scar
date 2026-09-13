# Copperhead placement and whole-board routing

`native-feasibility-v9` makes the default action an initial full-board route. Each subsequent explicit placement proposal produces one outer evaluation: move a scoped group or the full-board groups, preserve a native placement snapshot, reject native physical/invariant failures, export all nets, route with an explicit effort limit, import the session, and independently recheck the result. The retained incumbent is separate from exploratory candidates. Legacy individual-net repairs require `--legacy-inner`.

The global expansion proposal partitions every footprint into an explicit schematic-derived rigid group. It changes group translations and the outline, preserving footprint sizes, pad identities and within-group poses. Tracks/vias on nets internal to one group move with that group. Copper on nets spanning groups is removed because one rigid transform cannot preserve both endpoints. The original GND plane nets, copper layers and fill rules are retained; only their boundary polygons expand. This is a generous-space feasibility experiment, not mechanical or electrical qualification and not a controlled spacing-only causal experiment.

The first v8 initial/expanded pair requested600seconds,100passes,six layers,legal0.6/0.3mm through vias,fanout enabled,and optimization disabled. The expanded attempt exhausted its effort in fanout and produced no importable session. Policyv9 therefore disables the separate fanout stage and compares initial/expanded placement at180seconds each; all-net autorouting and legal vias remain enabled. These policies are separate W&B runs, and the default local graph/replay uses only the latest completed policy. Runtime can exceed the requested router limit during shutdown; records include both requested and measured time. All exported nets are eligible. Backend logs do not establish that each net was individually searched. `scripts/copperhead_route_evidence.py` extracts the 297-net/1053-pin/245-footprint input scope, layers, via and rule declarations, stage progress and termination from exact input/output files.

KiCad's DSN export contains a 50 µm SMD-to-SMD exception alongside 200 µm default clearance. Neither experiment changed this export behavior. The uploaded routing-coverage evidence retains the exact exported declarations. Native acceptance still uses the unchanged original project rules; a successful router exit is not proof of native legality. This limitation is visible in published evidence.

## Local views

- Dashboard: `http://127.0.0.1:53918/` — completed outer evaluations on the main graph; pending or rejected outer attempts remain in the table.
- Replay: `http://127.0.0.1:53918/replay/latest` — immutable snapshot of completed outer evaluations, 5× only.
- Legacy history is a separate dashboard toggle and `?view=legacy` replay, preserving the historical fine-grained evidence without calling those points placement steps.

## W&B and Weave

The authorized destination is `philippe-fdesousa/copper-scar`. `scripts/copperhead_observability.py` publishes historical immutable evaluation records, not purported live native spans. Runs are separated by track, policy, constraint scope and baseline hash. It logs actual loss/incumbent curves, corresponding hash-checked native board images, native gates, routing effort and coverage. Stage Two remains locked.

Use an isolated environment (`wandb==0.30.0`, `weave==0.53.9`, `pillow==12.3.0`) and invoke the script with `--credential-file /absolute/private/path`. The credential is read into process memory only; it is never a command-line value, report field or repository file. Project access is checked before uploading. A local publication lock, stable run/call IDs and remote read-before-write deduplicate repeated backfills. Publication verifies history rows, stored media files and completed Weave calls remotely and writes `.local/copperhead/observability/verified.json` only after those checks succeed.

SDK references: https://docs.wandb.ai/weave/guides/tracking/create-call and https://docs.wandb.ai/models/track/log/media.

After each native invocation, optional `.local/copperhead/observability/config.json` can start the publisher as a separate process. It contains only the observation Python executable path and private credential-file path. The native result is saved first; publication has its own log, worker PID and remote verification receipt. Local graph/replay operation does not require W&B availability. Failed outer attempts are preserved as separate run-summary/image and Weave failure records, never as completed routing curve points.
