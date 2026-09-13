# Actual two-level experiment observability

This read-only adapter mirrors the owner's append-only policy experiment. It never launches routing, changes owner CAD, or infers policy acceptance. Historical unmatched experiments remain a separate artifact.

- `build.py --source DIR --output DIR` verifies source-event prefix integrity, receipt and exact-board hashes, and renders a local `index.html` + `data.js` view.
- `watch.py` with the same arguments runs the builder, idempotent event publisher, and labeled router-log snapshots in one foreground process. It stops after the recorded policy decision. Use the protected owner observability Python environment for W&B/Weave.
- `publish.py --output DIR` publishes actual events, policy and lower-decision Weave spans, native cost/gate metrics, board media, and source artifacts. It verifies remote event hashes and media existence before writing `remote/verified.json`. Credentials are loaded from the protected config into process memory only. Fixtures are rejected.
- `publish_logs.py --run-id ID --attempt ID --output DIR` uploads existing router stdout and command-heartbeat snapshots. Original log timestamps are preserved; publication time and heartbeat-derived status are explicitly separate.
- `export_replay.py --output DIR` requires Playwright, Chrome and ffmpeg. It renders chronological recorded checkpoints, truncating curves at each recorded time, and fully decodes the resulting MP4. Incomplete comparisons are labeled.
- `python3 demos/autoresearch/test_model.py` verifies no invented cost at N, rejection retention, screening decisions versus route counts, and partial/conflicting event handling.

N counts decisions, including precheck rejection. Routed dispatches, completed routed results, router elapsed time and total decision time are separate fields. An incomplete arm has no cost at N. Index 0 is the common saved native baseline and has no router run. A lower open count does not override validity or original connected-pad-group gates.

Open `index.html` directly without a server, or serve its output parent locally. Query parameters `?policy=placement_first&decision=1` select an exact recorded checkpoint. Follow mode refreshes only the local data script; W&B links are optional outbound navigation.

The live output is mutable. Freeze `data.json`, `data.js`, events, manifests and hash-bound board directories together before making a portable archive. Do not include W&B runtime/cache directories or any credentials. `remote/verified.json` is a receipt, not a promise that every newest local event is uploaded.
