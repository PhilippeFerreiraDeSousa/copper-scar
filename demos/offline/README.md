# Copper Scar — offline evidence replay

Run `python3 serve.py` from this folder, then open http://127.0.0.1:8765. Or open `index.html` directly: no server, network, account, build or dependency is required for the dashboard. All board images, data and evidence links are local.

Use **Play from start**, the timeline slider, arrow keys, or the attempt table to replay completed native snapshots. The teal curve is best observed so far, the copper dots are attempted outcomes. Failed realizations appear as events without invented outcome points. Open counts mean native missing endpoint pairs. Zero physical errors does not mean electrically complete. Warning counts remain visible. No official score or qualified product board is claimed.

The full real-board history includes routing within retained placements and changed-placement experiments; the UI labels these separately. Comparisons across different routing effort, copper history or placement are observational and are not causal placement improvements. The JITX fixture is a separate bounded proof and must not be presented as whole-board qualification.

`evidence/` preserves native board files, native evaluations and attempt/parent/proposal receipts. `data.json` links each displayed count to that evaluation and matching board SHA-256. `SHA256SUMS.json` inventories package content. Source paths in receipts are provenance only; replay requires no owner workspace. CAD boards are evidence snapshots; complete fabrication/support packages are not claimed.

Rebuild from the source checkout (Python standard library):

```sh
python3 demos/offline/build.py --source /path/to/copperhead --output /path/to/demo-final
```

The builder reads completed attempts, verifies native evaluation board hashes, and excludes mismatches. It does not run CAD or modify source evidence. Videos are edited snapshot presentations: playback speed is presentation speed, not measured solver throughput. See their manifest for exact timing and hashes.

## Presentation files

- `copper-scar-demo-normal.mp4`: 180-second scripted edit, 1920×1080 H.264, silent for live narration.
- `copper-scar-demo-5x.mp4`: 5× presentation speed, approximately 36 seconds.
- `docs/3-minute-demo-script.md`: narration aligned to the normal video chapters.
- `topology-fixture/index.html`: verified joint 53 → 51 → 49 mm fixture and rejected ties.
- `jitx/index.html`: separate source-routing and whole-board JITX evidence.
- `docs/submission-draft.md`: primary-source requirements and unknown form fields.

The full historical trajectory is compressed into the video’s 0:50–1:20 chapter; the dashboard preserves every attempt for inspection. The later placement chapter revisits historical rejected trials. Video timing is an editorial choice, not claimed routing performance.

## Refresh and freeze

The optional `--feedback-chain /path/to/copperhead-feedback-chain` argument on `build.py` verifies and packages the concrete native feedback → changed proposal → rejected result chain. Automatic exclusion of a failed pose is a separate mechanism from circuit reasoning; neither implies a retained placement win.

After rebuilding, regenerate the normal and accelerated videos with `render_video.py PACKAGE`, run `verify_browser.py PACKAGE`, then `freeze.py PACKAGE` to verify source joins, record the current source commit and atomically replace the portable ZIP. Browser/video tools need Playwright, Chrome/Chromium and FFmpeg; presentation playback does not. The freeze rejects stale browser coverage or a video missing current attempt IDs. Existing ZIP stays intact until the replacement passes integrity checks.

## Parent-specific diagnostic view

`diagnostics/index.html` adds the saved native island analysis of the exact 55-open parent, covering nine nets and 32 missing pairs. It separates existing copper connectivity from unknown blocking cause and untested route/via legality. The root card explicitly indicates whether its parent hash matches the selected board. This additive view does not change the frozen video history or extend its duration.

Package new saved diagnostic evidence with `package_diagnostics.py --source REPORT_FOLDER --output PACKAGE`, or pass `--diagnostic-source REPORT_FOLDER` when rebuilding. No native CAD execution or board changes occur.

## Completed terminal-topology checkpoint

`topology-gain/` preserves the retained 54-open checkpoint, its exact final board/evaluation join, separate intermediate and final native graph proofs, and verified W&B/Weave readback. The U15 ground-island repair is a topology/routing gain with fixed component poses; the real board remains incomplete. `package_topology_gain.py` rebuilds this bounded case from its run directory, independent review directory and optional readback receipt.

Use `build.py --through-attempt ATTEMPT_ID` to freeze the historical replay at a completed checkpoint while the owner continues optimizing. This avoids silently adding a newer state during a video refresh.
