# Latest outer-loop experiments

Open `index.html` directly in a browser. No server or network is required. Select an experiment, choose any copper layer, toggle zoom, or play the original → updated → fully routed stages. `latest-loop-replay.mp4` is the short recorded replay when packaged.

This is a separate focused view. It does not replace the historical 119-record package, which ends at the 06:17 seven-seed experiment. The focused view contains 11 completed component-pose, explicit-via and declared-topology experiments from 04:46 through the 07:35 topology replan, finished 07:45:39 Pacific on September 13, 2026. It includes all qualifying rejections in that window. The former pending replan is now a completed rejection.

Every displayed experiment has three exact saved boards: original retained input, actual pre-route edit snapshot, and final whole-board routed candidate. Native evaluations are hash-bound to those boards. Component poses, vias and track removals are independently derived from the saved CAD, rather than inferred from the proposal. Each layer SVG is natively exported from the packaged board and cropped to the board coordinate frame; rings and labels are presentation overlays. SHA256SUMS.json records packaged files. Reproduction source is included under `reproduction/`.

## Findings and limits

- R37 movement plus full routing is the only retained component-placement missing-pair gain in the selected window: 54/0/18 → 53/0/19. No matched unchanged-parent control establishes isolated placement causality.
- R12 movement was retained at 51/0/18 → 51/0/18 for a diagnostic distance change. It has no count gain.
- Seven explicit through-via seeds plus full routing reduced 51 → 45 missing pairs. This is topology, not a component-placement gain.
- Later R123 moves were rejected at 46 and 47 opens; the 07:01 via experiment remained at 45 and was rejected.
- The completed 07:35 topology replan finished at 46/0/22 and was rejected. CAN2 target groups remain separate and the original +5V group remains split. Via geometry and scoped width checks passed; those checks do not rescue the failed connectivity gates.
- All selected experiments configured 600 seconds and 100 passes, with all exported nets and six copper layers eligible. Actual command durations differ and are displayed. Existing copper is inherited; these are not fresh unrouted or otherwise matched trials. Backend coverage proves eligibility, not that every net was searched.
- Historical reports mostly use in-memory zone refill, so stored zone fill render differences are not inferred route gains. The 07:35 final evaluation explicitly checks saved CAD without refill. The corrected publication board from the canonical demo is not substituted into historical experiments.
- Selection is deliberately narrower than all history. Targeted incremental net-routing iterations are excluded. The 05:26 failed targeted fanout/full-route experiment is also excluded from this explicit pre-route change view; its new-via gain occurred during the subsequent full routing, rather than an explicit successful fanout edit. Parent inputs are independently bound per row, not implied to form a continuous displayed chain.
- Placement optimization has not converged. Electrical width suitability, assembly fit/function, manufacturing qualification and official scoring remain unproved.

## Verification

`QA.json` records board-hash joins, all layer controls, offline desktop/mobile browser checks and replay frames. No original candidate or canonical demo artifact is changed by the builder. It only exports SVGs from copies.

Source entry points: `build.py`, `index.html`, `verify.py`. The builder uses explicit private source/output paths for this audit. Verification uses the local Playwright runtime and installed headless Chrome. Replay is encoded from the captured frame sequence with FFmpeg at one screenshot per second, yielding 33 seconds for eleven three-stage experiments.
