# Copperhead checkpoint and local reproduction

This checkpoint contains the native adapter, original-reference conversion/checking scripts, placement/inner-routing producers, native evidence metrics, audits, dashboard, cutoff-keyed 5x replay, focused tests and experiment reports. It does not claim a valid board or deterministic reproduction of every historical router output. The initial two attempts predate source archiving; that gap is documented in the execution audit.

## Environment and inputs

Use Python 3.12 with an isolated environment, the repository's existing package, and `copper_scar/tools/copperhead/reproduction/requirements.txt`. Tests use pytest (the checked environment had 9.1.1). The native scripts import KiCad's `pcbnew` through KiCad's own Python 3.9, not the project environment. The measured installation was KiCad 10.0.6 on macOS arm64. No global runtime installation or update is performed by these scripts.

The scripts currently record this machine's explicit KiCad, project, ffmpeg/rsvg and output paths. Inspect/update those constants for a different installation; this is a local experiment adapter, not a portable installer. The HTML dashboard is run directly from the checkout. `matplotlib`, `/opt/homebrew/bin/ffmpeg` and `rsvg-convert` are needed for replay rendering. The original/fixed replay URLs remain available locally; new on-demand replays are 5x only.

The immutable-by-convention reference is public `commaai/PCBGolf` commit `7210bdb5049c5b7fdf4900a34928e2736767292a`. The existing `scripts/prepare-pcbgolf.sh` retrieves/checks that revision. Do not edit that source checkout. `copperhead_prepare_baseline.py` copies it into a fresh native hierarchy, `copperhead_reconcile_reference.py` consumes a native exported netlist, and `copperhead_check_reference.py` validates original circuit/pad equivalence. Placement, planes and experimental land-pattern repair scripts document their separate transformations. Manufacturer/assembly qualification of those repairs is still open.

To regenerate the small schematic-position input for the legacy placement heuristic:

```sh
.venv/bin/python scripts/copperhead_schematic_positions.py .local/pcbgolf-source .local/copperhead/runs/schematic-positions.json
```

KRT uses `https://github.com/drandyhaas/KiCadRoutingTools.git` at `1c428c0b2285a4dfe8901ca7035109ded6cfbb4d`, with official native release v0.22.0. Its native binary and source-file hashes are in the committed `reproduction/krt-provenance.json`; the isolated Python dependencies are in `krt-requirements.lock`. Populate `.local/copperhead/tools/KiCadRoutingTools`, install the official matching native binary, create `.local/copperhead/tools/krt-venv`, and copy the provenance/lock metadata into `.local/copperhead/tools/` before using `copperhead_krt.py`. The wrapper checks every pinned file before executing. No third-party source or native binary is redistributed by this checkpoint.

Freerouting used official macOS version 2.4.1. The wrapper currently points at its mounted application under `/private/tmp/copper-router/freerouting-mount/`; set the executable path to your authorized local installation. Its recorded commands retain copper, use one thread and explicit routing/time limits. KRT success or Freerouting exit status never replaces native whole-board checks.

## Running and verifying

From an existing qualified-for-experiment local candidate with its support files, use `python -m copper_scar.tools.copperhead.stage1 --help` for bounded native attempts and `--proposal` for one explicit placement experiment. Candidate paths must be under this checkout's `.local/copperhead/candidates/`. The runner preserves input, generated board, commands, native reports, source hashes and incumbent decisions. Rejected candidates remain separate. The historical 58-open incumbent is an experimental starting point, not an accepted design.

```sh
.venv/bin/python -m pytest -q
.venv/bin/python -m copper_scar.tools.copperhead.dashboard --port 53918
```

The stable replay action is `/replay/latest`; it snapshots completed attempt records and renders independently of native routing. Reports under `docs/` distinguish historical routing microsteps from actual placement experiments and disclose incomplete qualification. Some report links point to excluded local evidence and will only resolve on the originating machine.

## Intentionally excluded and retained locally

- `.local/copperhead/candidates/` and `runs/`: CAD/model copies, native reports, command output and archived per-attempt sources. These are bulky generated evidence, not included in Git. Best retained candidate: `stage1-20260912-174325-566c96`, 58 opens/0 physical errors/11 warnings, design hash `09f9378a6e03d557f7cc96ff73610cff802799eec98f5a28cc9dceb7ecab1984`.
- `.local/copperhead/tools/`, `.venv*`, `node_modules/`, compiler caches and mounted applications: local dependency/runtime files. Only dependency/provenance metadata is committed.
- `.local/copperhead/replays/`, audits, proposals, loop state and review-output MP4s: preserved local snapshots and acceptance-review evidence. The reports identify exact paths and limitations; replay media is generated on demand, not published to GitHub.
- Pre-existing `demos/pass_timeline.md`, `demos/record-demo.sh`, and `demos/weave-evidence.md`: unrelated dirty work, deliberately excluded from this commit.

No credentials, native binaries, generated CAD/model sets or video files are staged. This is a branch checkpoint only; no merge into main is requested.
