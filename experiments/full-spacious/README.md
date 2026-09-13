# Full original-board spacious initialization

This experiment preserves all 245 original components and 1,078 physical pad UUIDs. It reuses the independently checked whole-project schematic wrapper, with only five J3 stacked-pad unconnected-name aliases reconciled to the actual schematic partition. Original electrical pad geometry, footprint angles, project design rules and netclasses remain unchanged. Component positions and a new generous outline are explicit design variables.

The actual small-loop initializer is a hand-written 8×9 mm grid; medium-loop uses a 6×5 mm grid with connector banks. Neither is a learned placement optimizer. The large-loop generator also uses coarse rows but was not established success evidence when this study began.

Here each functional group from the earlier full-board proposal receives package-aware shelf cells: minimum 6×5 mm, enlarged to the footprint drawing/pad envelope plus a 3 mm gap. Original component angles stay fixed. Groups receive 8 mm spacing and are packed in three columns; four mounting holes move to the corners. The resulting first board is 176×218 mm. The un-routed original-position control has a 90×87 mm envelope including the same 10 mm margin. The two outlines differ deliberately as part of the initialization; this is not a placement-only causal experiment.

Both use six copper layers, the same capacity as the prior full-board campaign. The source file originally enables two layers; this increase is an explicit feasibility choice, not an unchanged-source claim. There are no authored traces, vias or zones in either initial board. Both receive the same full-board/all-net/all-layer Freerouting 2.4.1 budget: 600 seconds, 100 passes, one routing thread, sequential strategy, no optional fanout or optimizer, and verified 0.60/0.30 mm and 0.45/0.20 mm F–B through-via options. No routing seed is verified. Other independent tasks may consume host CPU, so equal wall-time limits are not equal search work.

The original footprint geometry contains 51 invariant physical errors: 31 J3 pad clearances, 4 U4 pad clearances and 16 J5–J8 pad/hole clearances. The exact error UUID pairs and measured violations match between the two initializations. They are **not waived**. Initial missing count is 499 in both; seven schematic footprint-attribute warnings are also preserved. The raw native DRC violations have 124 warnings for spacious and 131 for original, with those seven parity warnings additional. No candidate can be called valid while these defects remain.

`campaign.py` preserves each initial and routed project, source hashes, original-board hash, commands, timings, saved-fill DRC, fresh saved-file DRC, ERC, schematic partition checks, full native pad groups, via geometry and checkpoint SVGs. New reported findings or splits of initially connected groups reject diagnostic retention. Even a retained diagnostic improvement has `valid_board=false`.

Run from `/Users/philippe/dev/copper-scar-demo`:

```sh
.venv/bin/python experiments/full-spacious/campaign.py \
  --root .local/copperhead/full-spacious/v1 \
  --name original-control --mode original --seconds 600
```

Names must be new: prior attempts are never overwritten. Use `--mode spacious --gap 3` for the first spaced initialization. Every invocation regenerates a complete source-bound placement and performs a full-board routing/evaluation; this is not accumulation of one-net repair calls. A next outer candidate must be selected from measured full-board failures and compared with the retained candidates.

The first successful preparation (`spacious-baseline-r2`) launched while these three source files were being committed. Its recorded source hashes exactly match pushed commit `b0416ea90388c070b3cfa7df7b10da4d8a1c09e1`, but the original launch record names the preceding commit. A separate committed-source binding explains this; it does not rewrite the launch record or claim a preregistered experiment. Earlier preparation failures remain saved and never reached routing.

Independent preflight audit: `/Users/philippe/Documents/Codex/2026-09-12/realtime-voice-chat/outputs/higher-loop-provenance-audit/spacious-preflight-audit.json`.

This study does not replace the separate historical 44-open checkpoint. That checkpoint contains explicitly recorded experimental land-pattern repairs and accumulated routing, so it is not a matched control for these fresh original-footprint baselines. Connector usability, high-speed routing, supply-loop behavior, assembly and manufacturing review remain necessary beyond native connectivity.
