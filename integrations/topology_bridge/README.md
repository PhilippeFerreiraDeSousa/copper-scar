# Research-driven placement and topology bridge

This bounded prototype runs existing pinned KRT placement research, validates its
parent hash and poses, generates alternative concrete via sites and typed
layer-specific `Route` endpoints, rebuilds JITX source, exports, evaluates the
whole fixture twice in KiCad, and retains only measured improvements.

`PortAttachment` binds a via to a net through a port; it does not select a
horizontal routing layer. Via span defines vertical reach. `Route.layer` defines
the horizontal leg. The native router chooses trace geometry under the rules.
The optimization implementation does not use fixed `Copper`.

## Reproduce

From this repository, choose a NEW output directory:

```sh
/Users/philippe/dev/copper-scar-demo/.venv/bin/python integrations/topology_bridge/reproduce.py .local/topology-research-NEW --native-python /Users/philippe/dev/copper-scar-jitx/.venv/bin/python --checker-python /Users/philippe/dev/copper-scar-demo/.venv/bin/python --research
python3 integrations/topology_bridge/audit_identities.py .local/topology-research-NEW
```

The installed runtime/library and KRT paths are deliberately explicit in this
local integration. `research-provenance.json` binds the original owner script;
`research_proposals.py` verifies every pinned KRT source hash before use. It
parameterizes group, search translations, board filename and rules. It removes
historical SD/expanded-board claims. KRT sees a native-reserialized external
parser copy with readback checks; the proposal is bound to the original input.
KRT's pad-box/geometry ranking does not account for retained copper and cannot
approve a candidate. Native exports and full fixture checks make that decision.

`planner.py PARENT.json MOVES.json NEW_OUTPUT` is the standalone topology
proposal boundary. `research_adapter.py` checks KRT parent hash and exact poses
before converting export-coordinate translations to source coordinates. The
parent includes native board/project hashes and the research proposal digest.

Supported topology scope is a complete two-terminal-net fixture with top pads,
a known top barrier and two conducting layers. Two sites per affected crossing
net are derived from the proposed component coordinates and two escape offsets.
All unaffected source topology entries stay identical. Stable attribute keys
represent routes/vias. Arbitrary multi-terminal product nets, rotations,
bottom-side components and general multilayer obstacle planning are unsupported
and must not be mislabeled as qualified by this fixture.

Each alternative is preceded by an authoritative source rebuild of the retained
parent, followed by exact exported pose/copper/project equality checks. No
managed-state cache is reset, copied back or edited. Export equality does not
establish identical hidden solver caches. Effort is bounded to one source build,
no additional routing sweeps, a 360-second command limit and the existing native
controller's timeout/barrier rules. Elapsed build time is measured and reported.
The objective is lower actual exported centerline length, no additional vias,
zero opens/violations, unchanged unrelated copper and identical project rules.
Equal-scoring alternatives are rejected as ties. No learned/product score is
invented.

## Verified evidence

- `.local/topology-research-01`: actual KRT → topology → JITX → evaluation chain.
  Four alternatives, two successive retained moves: 53 → 51 → 49 mm; 6 vias;
  zero opens/violations in all stages. Each preserves seven unrelated native
  route records and four unrelated via records exactly (numeric net IDs resolved
  to names), plus identical exported copper on those nets.
- `.local/topology-proposals-02`: synthetic move-input test additionally rejects
  longer 55.133/55.153 mm alternatives against the 53 mm parent.
- `.local/topology-research-observability-01`: allowlisted board snapshots,
  candidate/research/result JSON, five-times replay, measured length chart,
  W&B/Weave publisher and readback receipt. This is synthetic fixture evidence,
  not PCB Golf progress. Replay intervals are completed-snapshot timestamps and
  include rebuild/evaluation overhead, not invented router durations.
- `.local/attachment-comparison-01/reconciled-results.json`: attachments alone
  produce six vias but ten opens after build; explicit top and bottom routing
  calls then produce zero opens/violations. Source Routes produce zero opens
  during build. The redundant routing policy on the already-routed arm timed
  out; a subsequent read-only export barrier and DRC verified zero opens and
  violations. Its uncertainty marker remains; no timing superiority claim.

## Separate transfer diagnostics — paused

`transfer.py` and `verify_transfer.py` test legacy geometry preservation only.
Ten source native straight segments were converted to net-bearing `Copper`
polygons with six retained via instances. An added fixed rectangular plane and
via demonstrate connectivity. Native DRC is zero/zero. Per-net/layer exported
polygon unions agree with declared shapes to < 6.3e-13 mm. Round-cap polygon
approximation is bounded by 0.00000753 mm. Output primitives are net-bearing
`gr_poly`, not mutable native route tracks. This does not establish `Pour`
refill/thermal equivalence or arbitrary arc transfer.

`.local/fullboard-transfer-01/diagnostic-scripts/` contains the INCOMPLETE diagnostic,
not a usable accepted-parent importer. The retained full parent was read and
its two planes refilled in unsaved private memory. A disposable source was
prepared for all 245 components, 4,480 segments, 668 vias and six conductor
layers. Its first build failed at generated `.at(x,y,angle)` Python
instantiation; no full-board design was successfully built/exported. Work was
then paused on explicit instruction to hold fixed-Copper expansion. Do not
interpret that Python mistake as an API impossibility. Original imported
footprint repairs, exact geometry mapping, plane behavior and the six-layer
proxy remain unqualified. No original-board candidate or gain is reported.

## Capture-first continuation

See [CAPTURE_REPORT.md](CAPTURE_REPORT.md) for the latest capture ownership
result, captured-via identity blocker, and the 245-component native proxy crash
at unchanged resubmission. All task-owned runtimes are stopped. No original-board
candidate passed the common-parent gate, and no product improvement is claimed.
