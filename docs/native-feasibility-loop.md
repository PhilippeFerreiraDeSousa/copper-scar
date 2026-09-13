# Native feasibility loop: cost, state and evidence

Implementation revision: 12 September 2026. The Copperhead/native track has two stages. **Stage 1 is the real PCB repair loop**, not a hidden manual prerequisite: obtain a feasible full board. **Stage 2 optimizes accepted boards** using assembled volume + 50 × vias + 5000 × copper layers. Stage 2 is currently disabled; there is no accepted baseline.

## Implemented flow

`copper_scar/tools/copperhead/stage1.py` wraps the accumulated native scripts. It copies a selected candidate into a preserved run input and a distinct working candidate, freezes support-file/constraint hashes, runs a fresh complete netlist/ERC/DRC and reference comparison, records the action decision, executes bounded commands, reevaluates independently, persists scoped feedback and selects the next state. Every attempted candidate survives, including tool failure, timeout and regression. A single runner lock prevents concurrent state writers.

The controller supports continued routing from retained copper, screened GND escape batches of at most 20 through vias, pinned local KRT net repairs, and recorded passive position/rotation searches followed by scoped rerouting. Scoped feedback selects GND escapes after repeated routing, and stops repeating them after a measured regression. It selects this action only when reference invariants hold and the input lacks native shorts/clearance regressions. A targeted repair proposal is required for those defects. Recorded placement proposals currently search a two-pad resistor across positions and four rotations, preserve all global rails, remove only its two local nets and independently check the intermediate placement before rerouting. Broader group/plane/footprint action selection is not yet automatic. The LLM can supply the next justified repair through recorded code/proposals; it no longer needs to hide routing iterations in an undocumented command sequence.

Each loop attempt archives its tool source and SHA-256 provenance and has `attempt.json`, immutable-by-workflow input, commands with exact arguments/timings/status, before/after evaluations, raw native reports, candidate hashes and action rationale. The current controller is deterministic; it does not imply a model call occurred. Local `feedback.json` separates measured facts from the routing hypothesis. Scope combines frozen support-file/constraint identity with specific input/output design hashes and violated object IDs. Old geometric feedback remains historical evidence, not an instruction that automatically applies at new positions.

## Operational feasibility cost

Metric version **`native-defects-v1`** is implemented in `metrics.py`. Lower lexicographic tuples rank better:

1. Reference/constraint invariant failure: 0 or 1. Failed invariants disqualify incumbent selection.
2. Distinct native short item pairs.
3. Other error findings outside connectivity/clearance categories, including invalid outline when present.
4. Distinct clearance-related findings, including hole clearance, edge clearance, courtyard overlap and mask bridges.
5. Maximum **measured** clearance shortfall, in millimetres.
6. Distinct missing-connection endpoint pairs.
7. Sum of measured straight-line endpoint distances, in millimetres, rounded to 0.001 mm for comparison.
8. Remaining warning findings.

The ordering prioritizes preserving the circuit and avoiding shorts before repairing ordinary missing connections. It prevents a new short from being compensated by many cosmetic fixes. It is an operational starting policy, not a physical law or promised convergence theorem. Changing this order requires a new metric version and reevaluation of incumbents; do not splice incomparable trajectories together.

All components are logged individually. Findings are deduplicated by native type and sorted involved object UUIDs. Raw unconnected report counts remain alongside deduplicated counts. The metric reports maximum and total measured clearance shortfall plus measurement coverage; descriptions it cannot parse are left **unmeasured**, not assigned an invented violation depth. The maximum measured shortfall alone cannot compare missing severity information fairly; consult coverage when evaluating ties or proposing repairs.

Connectivity cost is a **native airwire endpoint-pair proxy**. It is more explicit than counting arbitrary log lines, but is not the exact number of disconnected electrical islands. Native reports may select different representative endpoints after routing. Summed Euclidean distance is neither realizable route length nor total copper demand and can change when representatives change. Net/pin connectivity equivalence is checked independently. An exact per-net connected-component metric is a future refinement, not a claim of this implementation.

Do not normalize these categories into a fabricated dimensionless weighted sum. Counts have count units, distances have millimetres, and lexicographic comparison makes priorities visible. Never call this tuple the PCBGolf score. A zero tuple does not establish acceptance when check coverage, models, manufacturing or engineering review are unknown.

## Actual examples

Existing native reports produce these diagnostic examples; their different topology/footprint revisions must remain visible when comparing history:

| Candidate | Native shorts | Clearance findings | Missing pairs | Endpoint-distance sum | Warnings |
|---|---:|---:|---:|---:|---:|
| baseline-003, first four-layer route | 5 | 56 | 235 | 4957.636 mm | 125 |
| baseline-009, block placement and two inner planes | 0 | 51 | 473 | 5184.281 mm | 111 |
| baseline-012, repaired land patterns before route | 0 | 0 | 499 | 4183.033 mm | 1 |
| baseline-013, six-layer routed trial | 0 | 0 | 208 | 2654.483 mm | 1 |

Baseline-009 has worse connectivity than baseline-003 but no native shorts. This is a measured tradeoff, not “everything improved.” Baseline-013 improves missing pairs relative to baseline-012 while retaining its zero native shorts/clearance findings. It remains invalid: 208 missing connections, one library warning and unresolved engineering/assembly evidence.

These historical numbers do not prove that memory helped. A controlled memory test must hold input, engine, rule revision and budget constant, compare feedback-enabled/disabled decisions, retain all results, and account for router variability. The current feedback mechanism supports stagnation detection; no causal memory-benefit claim has been established.

Seven completed durable attempts following baseline-013 reduced native missing pairs as follows: 208 → 177 → 171 → 152 → 133 → 133 → 132 → 128. The fifth action regressed endpoint distance from 2069.485 to 2094.011 mm with unchanged pair count; the fourth incumbent remained retained. Every completed attempt passed reference invariants with zero physical errors. Warnings increased from one to two on the second attempt and remain explicit. These are actual native measurements, not simulation. Subsequent attempts are listed live in the dashboard.

## Incumbent, exploration and stops

`loop/state.json` distinguishes the best feasibility incumbent, the latest exploratory candidate and the accepted baseline. Each incumbent is tied to its constraint scope and metric version. The initial candidate is eligible as incumbent before an action; a regressing first output cannot silently replace it. Outputs with broken invariants cannot become incumbent.

An exploratory continuation may temporarily accept a worse diagnostic tuple when invariants and absence of shorts are preserved; the old incumbent stays available. This allows a measured tradeoff/recovery rather than assuming every action must improve. The current implementation allows a bounded exploratory continuation and falls back to the incumbent. More complex placement/backend exploration needs a specific recorded proposal, not unbounded retries.

The runner stops on explicit iteration/wall-time budgets, execution/report failure, invariant failure, defects requiring an unsupported targeted repair, or two scoped routing attempts without diagnostic improvement. A runner budget stop does not declare the user's board goal complete. The controller can inspect preserved evidence and resume with a justified action. A genuine external blocker must identify the missing decision/evidence precisely.

Every action is evaluated before and after. Failures retain command logs and partial artifacts; they do not promote. Router exit zero and `COMPLETED` may still mean timeout or incomplete routing. Native recheck determines resulting diagnostic state. Tool timeout details remain in the underlying execution record.

## Acceptance and stage transition

Current support files, design rules and netclasses are frozen within a campaign. The independent reference checker verifies all five original sheets, complete native ERC coverage, physical pad identities and full pin-connectivity partitions. The runner fails on unexpected support changes and malformed/incomplete reports. Removing parts, changing connectivity, weakening rules or skipping checks cannot lower a candidate into acceptance.

Native CAD acceptance requires complete reliable checks, no unresolved required violations and no missing connections. Further acceptance requires manufacturer-compatible land patterns/process, reviewed power/pair/return-path/clock layout, complete assembly geometry, connector access and engineering evidence tied to the exact design. Physical hardware proof is tracked separately and cannot be inferred from those CAD results.

The runner currently records engineering review, assembly completeness and hardware proof as unknown. It never manufactures reviewer attestations. Consequently `validity_gate=false`, `stage2_enabled=false` and `official_score=null` are explicit until an appropriate evidence-backed acceptance mechanism is implemented and satisfied. Stage 2's intended rule is simple: an accepted candidate can replace the accepted incumbent only if validity remains satisfied and its verified assembled-volume/via/layer objective decreases. No Stage 2 optimizer is implemented yet.

## Observability and viewing

Existing `WeaveTracer` provides structured before/action/after spans when the already authorized API key and optional dependency are available. There is no new service, enrollment or paid model dependency. Local structured evaluations and `loop/eval-rows.jsonl` persist regardless of live tracing. Live Weave delivery has not been verified in this environment; offline records are the evidence source.

`copperhead_publish.py` renders the actual checked board, hashes it and atomically replaces `CURRENT.md` and `current-status.json` with exact candidate/report links. Each completed native board is a separate path; the generator does not overwrite published boards or the user's unsaved edits. `copperhead_viewer.py` starts at most one owned editor and requires guarded UI file switching thereafter. The available CUA bundle selector currently identifies the existing JITX process, not the owned Copperhead process, and its Window menu exposes only that JITX window. Safe graphical switching remains unverified; no JITX window was replaced.

The read-only local dashboard at http://127.0.0.1:53918/ is visible and graphically verified. It refreshes every three seconds and shows actual attempt history, regressions, incumbent versus exploratory state, native SVG checkpoints, versioned cost components and links to raw records. Active subprocesses record five-second heartbeats and per-phase elapsed time. PID liveness distinguishes running, stopped and stale workers. Measured durations include sample counts and ranges, not invented ETAs. Automatic refresh to the seventh checkpoint (128 missing pairs) was verified without reloading the page. This dashboard does not imply native PCB Editor switching works.

## Run and replay

From `/Users/philippe/dev/copper-scar-demo`:

```sh
.venv/bin/python -m copper_scar.tools.copperhead.stage1 \
  --source .local/copperhead/candidates/baseline-013 \
  --iterations 2 --route-seconds 120 --budget 600
```

Use the recorded input snapshot and command JSON for exact tool/action replay into another fresh candidate directory. Tool versions and effective router settings are recorded with outputs. Byte-identical routing is not promised: no deterministic router seed has been verified. Replay means a reproducible input/action/check contract, not guaranteed identical copper.

The focused metric tests check deduplication, distance units, clearance measurement, invariant priority and the inability to trade a short for connectivity improvement. Actual native loop runs provide the integration evidence. Mock/unit checks cannot stand in for a completed board.

## Placement actions and alternate backend

The R17 action moved (142.5,121.75) to (160.95,87.5) mm with unchanged 0-degree rotation after searching four rotations. Native missing pairs changed 124 → 127 after placement/rip-up → 123 after routing, with zero physical errors and two warnings throughout. This demonstrates combined move-and-route progress, not an isolated causal effect of placement. A previous producer crash was preserved and independently inspected; it never promoted. The next R15 move rotated 0 → 90 degrees and regressed 123 → 124 missing pairs with three warnings, so the prior incumbent stayed retained. Positions and rotations are search variables; holding other parts still for a local experiment does not freeze them globally.

KRT source commit `1c428c0b2285a4dfe8901ca7035109ded6cfbb4d` and native release 0.22.0 are local to this track. The official arm64 binary checksum is recorded. The producer disables size escalation, net/pad swaps and normal DRC-setting writeback. It nevertheless adjusts a temporary output-project hole floor internally; that project is never adopted. Only produced board bytes enter the candidate, followed by independent checks against the frozen original project. Native producer acceptance is not the feasibility authority. Feedback now selects the largest untreated missing-net scope after the successful pilot, so one proposal completion does not require a user prompt to dispatch each subsequent routing action.

## Replay artifact

`scripts/copperhead_replay.py` snapshots finalized records, verifies board hashes against native evaluations, renders actual outer-copper SVG views, and encodes a discrete 1080p H.264 MP4. It never reruns routing or interpolates PCB geometry. The delivered replay cutoff is 2026-09-12 23:58:20 UTC: fourteen finalized attempts plus the starting checkpoint, 43 seconds at 30fps. It preserves regressions and a failed producer with a trustworthy subsequent native inspection. Beginning/middle/end decoded frames were checked; visible browser playback was verified as advancing. The MP4 and hash/source manifest are in the requested review outputs directory. Later live attempts are intentionally outside this fixed replay.
