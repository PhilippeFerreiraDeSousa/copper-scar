# Hackathon work index — 2026-09-13

This index identifies the public implementation branches and preserved research checkpoints. The repository root also contains the earlier simulation/observability scaffold; it should not be confused with the later native board experiments below.

## Actual routing architecture

The **small, medium, large, and original/full demo families used Freerouting for full-board autorouting**, with KiCad exporting DSN, importing SES, and independently checking results. Some earlier original/full-board repairs also used KiCadRoutingTools. The small/medium/large JITX projects imported and displayed their initial boards; they did not generate or route the evolving demo candidates.

Separate JITX research does contain source-authored route/via and transfer experiments on bounded fixtures. Its results do not establish a JITX optimization loop for all four demo families or a valid original competition board.

## Implementation branches

| Workstream | Source | Scope |
|---|---|---|
| Small native loop | [codex/small-pcb-loop](https://github.com/PhilippeFerreiraDeSousa/copper-scar/tree/codex/small-pcb-loop/experiments/small-loop) | KiCad + Freerouting; JITX input import is separate. |
| Medium native loop | [codex/medium-pcb-loop](https://github.com/PhilippeFerreiraDeSousa/copper-scar/tree/codex/medium-pcb-loop/experiments/medium-loop) | KiCad + Freerouting; includes latest committed ground escape and bottom-trim work. |
| Large native loop | [codex/large-pcb-loop](https://github.com/PhilippeFerreiraDeSousa/copper-scar/tree/codex/large-pcb-loop/experiments/large-loop) | KiCad + Freerouting; remains invalid in the recorded pilot. |
| Original/full board | [codex/demo-takeover](https://github.com/PhilippeFerreiraDeSousa/copper-scar/tree/codex/demo-takeover/experiments/full-spacious) | Freerouting full-board trials; earlier targeted repairs also used KiCadRoutingTools. |
| Live viewer | [codex/pcb-loop-live-unified](https://github.com/PhilippeFerreiraDeSousa/copper-scar/tree/codex/pcb-loop-live-unified/demos/live) | Replay and live-status presentation. |
| Offline demo | [codex/offline-demo](https://github.com/PhilippeFerreiraDeSousa/copper-scar/tree/codex/offline-demo/demos/autoresearch) | Recorded experiment replay and publication tooling. |
| JITX research | [codex/jitx-optimization](https://github.com/PhilippeFerreiraDeSousa/copper-scar/tree/codex/jitx-optimization/integrations/jitx) | Separate JITX investigation; not the four-family demo router. |
| Placement bridge | [codex/placement-routing-bridge](https://github.com/PhilippeFerreiraDeSousa/copper-scar/tree/codex/placement-routing-bridge/integrations/placement_bridge) | Bounded JITX/KiCad fixture and geometry-contract research. |

## Local work preserved as public checkpoints

These branches add captured working-tree edits to their original source history. They preserve unfinished work without rewriting or merging the implementation branches. Each includes `PUBLICATION_CHECKPOINT.md` with scope and file inventory. A published checkpoint is not a claim that interrupted implementation or hardware qualification is complete.

| Workstream | Snapshot branch | Commit |
|---|---|---|
| live-viewer | [codex/public-checkpoint-live-viewer-20260913](https://github.com/PhilippeFerreiraDeSousa/copper-scar/tree/codex/public-checkpoint-live-viewer-20260913) | [`75b0fa73`](https://github.com/PhilippeFerreiraDeSousa/copper-scar/commit/75b0fa73ef3f4d33168f603564f2d0fdfd1f47b2) |
| offline-demo | [codex/public-checkpoint-offline-demo-20260913](https://github.com/PhilippeFerreiraDeSousa/copper-scar/tree/codex/public-checkpoint-offline-demo-20260913) | [`11e8524b`](https://github.com/PhilippeFerreiraDeSousa/copper-scar/commit/11e8524b5bc9a1f9ad4710170a82e5a64258b7bb) |
| large-repair | [codex/public-checkpoint-large-repair-20260913](https://github.com/PhilippeFerreiraDeSousa/copper-scar/tree/codex/public-checkpoint-large-repair-20260913) | [`fe886382`](https://github.com/PhilippeFerreiraDeSousa/copper-scar/commit/fe88638252176b5367799c1ef86ce2ddf3ca7985) |
| jitx-topology | [codex/public-checkpoint-jitx-topology-20260913](https://github.com/PhilippeFerreiraDeSousa/copper-scar/tree/codex/public-checkpoint-jitx-topology-20260913) | [`75c0a278`](https://github.com/PhilippeFerreiraDeSousa/copper-scar/commit/75c0a278aa3bab08d20a97e32fb0ad5c1d5d4d7f) |
| full-demo | [codex/public-checkpoint-full-demo-20260913](https://github.com/PhilippeFerreiraDeSousa/copper-scar/tree/codex/public-checkpoint-full-demo-20260913) | [`613ba0fb`](https://github.com/PhilippeFerreiraDeSousa/copper-scar/commit/613ba0fbd5b3bf4e7011b456ecfcf61d266456b3) |
| jitx-review | [codex/public-checkpoint-jitx-review-20260913](https://github.com/PhilippeFerreiraDeSousa/copper-scar/tree/codex/public-checkpoint-jitx-review-20260913) | [`22ca70b8`](https://github.com/PhilippeFerreiraDeSousa/copper-scar/commit/22ca70b810924abe53a90b99e02ac68f66b0190a) |

## Prompts and candidate provenance

- [Medium Stage 1 task prompt](prompts/stage-1-medium-initial.md)
- [Same task's Stage 2 transition prompt](prompts/stage-2-medium-transition.md)
- [Selected subsequent update instructions](prompts/medium-update-followups.md)
- [Medium candidate action ledger](medium-candidate-ledger.json)

The prompts went to a persistent Codex task, with later Coordinator messages; a new agent was not created for each candidate. The task wrote or revised Python experiments, which could generate a single candidate or a deterministic batch. These are task-level instructions, not a fixed per-candidate API prompt. Prompt exports replace machine-specific paths and task identifiers with placeholders and omit links into private local chat logs; that redaction is documented in each file.

The ledger includes the Stage 1 diagnostic group move and 25 completed Stage 2 events from study event files, sorted by completion timestamp. Baselines, frozen duplicates, separate Stage 1 policy trials, and interrupted attempts without completed event records are outside that count. Studies can overlap, so chronological order is not a single ancestry chain. `proposal_source` is the geometry source, while `parent_incumbent` is the comparison board. In particular, independent scale trials often transform the same baseline rather than applying cumulative scaling. Action parameters describe proposal changes; Freerouting creates additional routing geometry afterward. The ledger's relative artifact references identify local experiment files, not public download URLs. Native candidate boards and bulky runtimes are not included in this index.

The latest recorded Medium incumbent is **35,365.44**, with 31 vias, at `stage2/edge-x-tight-01/candidate-01`. This is a reduced PCB Golf-inspired circuit, not an accepted original challenge submission. This publication pass checked record/hash consistency; it did not rerun CAD or establish powered-hardware qualification.

## W&B and Weave evidence

- [Initial Medium Stage 2 run](https://wandb.ai/philippe-fdesousa/copper-scar/runs/medium-stage2-bca7861dec65)
- [Medium continuation run](https://wandb.ai/philippe-fdesousa/copper-scar/runs/medium-stage2-continuation-20260913)
- [Functional grouping evaluation record](https://wandb.ai/philippe-fdesousa/copper-scar/weave/calls/4ea50c71-2ab3-549f-8917-d32b321e2fa7)

These W&B resources require project access. Medium evaluation traces were backfilled from completed native experiment records; their span durations are not actual routing time, and they are not per-candidate LLM inference traces. Recorded command durations and router logs contain execution timing. The last confirmed continuation upload reaches **40,074.08**; newer local results are not represented by that publication receipt.

## Publication validation

- 12 shared-executor tests passed.
- 16 placement/topology contract tests passed.
- 9 original geometry-contract tests passed using the existing JITX environment's Shapely dependency.
- Captured Python and JSON files parsed; inline JavaScript syntax checks passed.
- Newly published source and checkpoint files were checked for common credential patterns; local credential files and runtime directories were excluded.

No new native routing run or full browser/CAD regression test was performed for this source-preservation pass. Local installation paths in research code may need configuration on another machine. JITX, KiCad, and Freerouting runtimes are not redistributed here.
