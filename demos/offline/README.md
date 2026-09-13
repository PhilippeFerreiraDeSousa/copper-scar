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
