# small-loop: frozen Stage Two result

The complete nominal assembly score fell **33,500.64 → 15,900.96 (52.54%)**, with every retained board passing native connectivity, DRC, schematic parity, ERC, original-rule/pad-geometry checks, model coverage, and a conservative model-box overlap screen. The final accepted board is29×16mm, has two copper layers and ten vias. Its full assembled height is11.64mm, including connector tails below the board.

The official formula was checked against https://comma.ai/leaderboard and https://github.com/commaai/PCBGolf on2026-09-13:

`PCBA bounding-box volume(mm³) +50×via_count +5000×copper_layers`.

The final terms are **5400.96 +500 +10000 =15900.96**. This is the official formula applied to the deliberately reduced **small-loop** circuit. It is not a score eligible for the original full PCBGolf challenge or a claim of powered hardware qualification.

## Assembly and native provenance

Original J4 was DNP/excluded and lacked a model. Stage Two explicitly populates the original electrical2X04 footprint as a HarwinM20-9980446 header. The manufacturer lists10.16×5.08×11.64mm,8.64mm above PCB and3mm tail at https://www.harwin.com/products/M20-9980446. `stage2_prepare.py` produces a nominal body/pin model matching these extrema and original pad locations. It is a datasheet-dimensioned model, not the vendor's detailed STEP. All14other original populated component models are retained. OpenCascade measures the complete KiCad assembly STEP; substrate thickness is never substituted for assembly height.

Stage Two also makes the generated labels global, eliminating exact native schematic name conflicts caused by local `/NET` namespaces. This changes no electrical partitions. The populated header library entry matches the board. Original DRC/ERC/netclass settings and electrical pad geometries remain equal to the authoritative reference. Native board saves may rewrite project settings; producer output is preserved, and source project bytes are restored before every evaluation.

Final boardSHA256:
`c580b45e4ed18b8420e8d15b94a938c478ed845610367a82915e3793405cf9cc`

Frozen evidence lives in `.local/small-loop/stage2/final-accepted/` on the owning isolated checkout. `frozen.json` records the independent audit, source commit and score. `sha256-manifest.json` binds the complete package. The frozen board hash remained unchanged across the fresh independent KiCad checks and independent assembly export.

## Completed studies

| Study | Decisions | Result |
|---|---:|---|
| Tight margin, source625005f |5|All rejected: two full routes retained1/3opens, three outlines clipped silk before routing.|
|3mm margin, sourcead7f166 |5|All retained:25003.44→21534.72→19409.36→17737.70→16486.40. First changed outline only; remaining four each moved13components.|
|Closer packing, source73d2347 |4|15900.96 retained; three tighter placements rejected for physical violations.|
|2mm margin, source84a3f8a |2|Both fully routed candidates retained one open; rejected.|

Each candidate has input-derived component poses, pre-routing board, whole-board route invocation, actual elapsed time, saved routed board, native reports, assembly STEP, score terms, source SHA and keep/reject event. There are16completed proposals,10full routing trials and6preflight rejections. Invalid candidates have `official_formula_score: null`. Rejected geometry is never assigned an accepted score. The model dimensions and pad geometry are not scaled when placement spacing contracts. Geometry proposals are based on the known valid baseline; `parent_incumbent` identifies the score comparator, not a hidden geometry source.

The search is **completed/idle**. `live_status.py` derives a truthful live-status record from the completed receipts. It exposes actual start/end/elapsed, last completion, the latest rejected trial and the retained frozen board. Playback is historical completed-state playback; there is no claim of continuous router geometry streaming.

## Preserved earlier work

The earlier small-loop feasibility pilot is separate. The initial legal placement had29opens; routing alone reachedzero. Both three-decision placement policies stayed atzero and proposed identical swaps. Wire length fell493.61→436.57mm, a secondary quality change, not an official-score change or evidence placement was necessary for feasibility. Primary cost@3 tied0/0; the challenger was rejected.

A separate explicit topology proposal movedR90 and authored a net-attached via plus bottom-layer stub. Full routing left the stub dangling, so the board was rejected. A two-ended topology revision preserved two declared via sites/net identities and completed without native violations, but was longer and not retained. These failures and revisions remain saved. Router-created vias are not mislabeled as outer topology proposals.

The initial JITX design remains separately inspectable as `small_loop.design.SmallLoopInput`; it is not the Stage Two realization engine. Its export matches15components and11electrical partitions with one common coordinate translation, but native ERC/severities and exact mask/polygon equivalence are not claimed transferred. Native KiCad/Freerouting remains the acceptance path.

The accepted **medium-loop** handoff was copied into `.local/medium-loop/stage2/baseline` with unchanged boardSHA53771cdb168a054d54e6c4b556ebced2a8950e5259ac1db365b54ff1c8cb0336. Its85model,70×60×11.64mm assembly baseline scores65388.00 with130vias and two layers. No medium-loop Stage Two optimization was performed before the small-loop noon handoff. **large-loop** is an independent size family, not a stage label.

## Validation and publication

Fresh independent native audit:0opens,0DRC,0schematic parity,0ERC; all models resolved, no conservative body overlap; unchanged board hash; repeated score15900.96. Four negative acceptance tests passed: changed rules, schematic parity failure, missing populated model, and saved-board drift all prevent acceptance or scoring.

Source is committed and pushed on `codex/small-pcb-loop`. Generated CAD/runtime/media and credentials are excluded from Git. The demo owner owns W&B/Weave publication and final live/frozen UI packaging; this owner never published competing runs. The earlier small-loop deterministic evidence was remotely verified by the demo owner as run `small-noon-a633cb5e7ddb`; all traces are explicitly historical evidence backfill, with no invented LLM calls.
