# Joint topology fixture replay

Build a portable offline evidence package from the existing read-only joint-integration artifacts:

```sh
python3 demos/offline/fixture/build.py \
  --source /Users/philippe/.codex/worktrees/ff86/copper-scar \
  --out /Users/philippe/Documents/Codex/2026-09-12/realtime-voice-chat/outputs/demo-final/topology-fixture
```

Open the generated `index.html` directly; no web server, network or dependencies are needed. The builder requires Python 3 and saved evidence, and runs no CAD tools. Runtime images, CAD, native reports and data stay in the output directory. Only this HTML, builder and README belong in source control.

The builder checks all image and CAD hashes against the original producer bundle, checks native summary source and normalized CAD hashes, checks both stored DRC reports, and independently sums straight native segment centerlines. The original producer script is bundled to document image construction. Zero native violations refers to the configured fixture rules; ignored checks remain visible in the reports. No fresh native validation is claimed.

The default is the latest retained candidate at 49 mm. `window.showFixture(index)` selects a frame for recording; `?play` starts the complete chronological replay.

| Index | Stage | Length | Decision |
|---|---|---:|---|
| 0 | 00-parent | 53 mm | Parent |
| 1 | 01-0-candidate | 51 mm | Retain |
| 2 | 01-1-candidate | 51 mm | Reject tie |
| 3 | 02-0-candidate | 49 mm | Retain |
| 4 | 02-1-candidate | 49 mm | Reject tie |

For three ten-second retained-progress frames, use indices **0, 1, 3**. Every frame has six vias, zero native opens and zero native violations. The rejected candidates pass native checks and tie the retained alternative. They are not failures to realize a board. This is the joint eight-pad topology fixture, never the real product board.
