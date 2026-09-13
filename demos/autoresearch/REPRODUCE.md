# Reproduction and evidence boundaries

## View and inspect offline

Extract the portable ZIP and open `index.html`. All board SVGs, raw CAD, JSON, replay video and native proof files are local. Optional W&B links require existing project access. No credentials are packaged. `package-manifest.json` hashes each included file; the separate ZIP receipt binds archive bytes.

The demo is static and requires no package installation. Play actual checkpoints reveals only recorded results known at each checkpoint. The final comparison and any next-campaign receipts are separate.

## Verify the viewer

The `reproduce/` directory contains the exact presentation source. Python 3.11+, Playwright, a supported Chromium executable and ffmpeg are required for browser QA/video regeneration. The snapshot contains already-exported SVGs; KiCad is needed only to regenerate CAD views. The author's QA used a macOS Chrome executable; change that explicit path in `verify.py`/`export_replay.py` for another host.

From the extracted package:

```sh
python3 reproduce/test_model.py
python3 reproduce/verify.py --output two-level-autoresearch
python3 reproduce/export_replay.py --output two-level-autoresearch
```

The event model's tests validate missing costs at N, rejection retention and screen-only decision semantics. Viewer verification checks exact file hashes, all six copper layers, offline loading and mobile overflow. Replay generation fully decodes its output with ffmpeg.

## Reproduce native experiment work

`source/` contains the frozen experiment Git source archive and its exact commit, plus a demo source archive when supplied. `experiment-input/` contains the original source board, original project support and routing options; the normalized common native checkpoint is additionally preserved in the pilot's hash-named board directory. Source manifest and attempt receipts bind the board, source implementation files, router JAR hash, commands, rules and routing options.

Native rerunning requires KiCad/pcbnew, the matching Freerouting JAR and Java environment described in the original source, plus its machine-specific tool paths. The frozen script is `scripts/copperhead_policy_experiment.py`, invoked with `--source` pointing at an isolated copy of `experiment-input`, `--route-seconds 600 --decisions 3`. It refuses to overwrite an existing experiment. Do not run it inside a live owner checkout. The source archive preserves the exact tested implementation, including its original path assumptions; this is reproducible source and evidence, not a bundled cross-platform router runtime.

The router exposes no verified random seed. Native UUID/item ordering can vary. Identical future routing geometry is not guaranteed; compare the recorded evidence and native acceptance gates instead of asserting bitwise rerun determinism.

## Remote publication

`publish.py`, `publish_evidence.py`, `publish_logs.py` and `publish_media.py` require an authorized W&B account. The demo run used W&B 0.30.0 and Weave 0.53.9. The remote project uses complete-mode traces; `trace_io.py` uses synchronous v2 start/end writes with bounded readback of actual persisted outputs. Evidence uploads download the listed files again and compare SHA256 bytes. Source credentials are deliberately omitted.
