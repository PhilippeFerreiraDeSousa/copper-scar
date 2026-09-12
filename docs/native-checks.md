# Native PCB validation setup

Worktree: `/Users/philippe/dev/copper-scar-demo`. The main checkout is unchanged.
This implements a real candidate checker, not an autorouter or a valid final PCB.

## Installed tools

- KiCad 10.0.6: `~/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli`.
  [Official universal macOS DMG](https://github.com/KiCad/kicad-source-mirror/releases/download/10.0.6/kicad-unified-universal-10.0.6.dmg), Homebrew-verified SHA256
  `ef4dcd4278c46d3efcd28c8db273d5957d68efda028f6bf79b4811fc5302dc68`.
  Homebrew's system demo-directory install needed sudo; the official application
  was instead copied into user Applications. No security protections were disabled.
- Copperhead 0.10.0, local npm package and lockfile; install with `npm ci --ignore-scripts`.
- Codex SDK 0.144.6, matching Copperhead's optional peer range, supplies a working
  local launcher. `node_modules/.bin/codex login status` confirmed a ChatGPT login.
  No provider is configured and no model calls were made. The global launcher is
  broken; use `scripts/copperhead.sh`, which chooses the pinned local launcher.
- Python 3.12 environment with native PCB extra (sexpdata and OpenCascade).
  OpenCascade's STEP bounding-box calculation was tested on a 10×20×7mm solid.

JITX 4.4.0 CLI and macOS runtime remain installed separately at
`/Users/philippe/dev/copper-scar-jitx`; they are not involved in this path.

## Reproduce

```bash
cd /Users/philippe/dev/copper-scar-demo
npm ci --ignore-scripts
python3.12 -m venv .venv
.venv/bin/python -m pip install -e '.[pcb]' pytest
bash scripts/prepare-pcbgolf.sh

.venv/bin/python -m copper_scar.cli real-check \
  --project .local/pcbgolf-candidate/pcbgolf.kicad_pro \
  --reference .local/pcbgolf-source/pcbgolf.kicad_pro \
  --kicad "$HOME/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli" \
  --out-dir .local/checks
```

The official baseline **must exit 1**, with score null and promotion false.
Each invocation retains a fresh candidate snapshot, input hashes, raw native
JSON, command arguments, exit codes and stdout/stderr in its printed directory.
`failure-record.json` binds all findings to that exact design. Source and working
candidate are never changed by the native checker.

`prepare-pcbgolf.sh` pins official source commit
`7210bdb5049c5b7fdf4900a34928e2736767292a` and makes a separate candidate clone.
It refuses a changed source checkout and never resets an existing candidate.
All original project, schematic, library and model files remain intact.

To use Copperhead's deterministic convenience check on this existing project,
configure `.local/pcbgolf-candidate/.copperhead/config.json` as follows (already
configured in this working copy):

```json
{"schematic":"pcbgolf.kicad_sch","board":"pcbgolf.kicad_pcb","docs":"docs","model":null}
```

```bash
bash scripts/copperhead.sh --repo .local/pcbgolf-candidate --json check
```

This also exits 1 on the baseline. It is a native KiCad check, without an LLM.
Do not use `create --brief` for this project. Further Copperhead orchestration is
deferred while an actual routing engine is evaluated.

## Actual baseline, September 12, 2026

KiCad 10.0.6 reported 180 DRC violations plus 499 unconnected items. Violations
include invalid outline, clearance, holes, shorts, solder mask and silkscreen.
Copperhead's independent native wrapper reported **679** DRC items and exited 1.

There are additionally 240 native schematic-parity items, but **whole-project
parity is unresolved**, because the CLI currently loads only the matching root
schematic. The `.kicad_pro` explicitly lists five top-level schematics. Running
each file independently produced 0, 150, 124, 198 and 266 ERC items respectively;
each report contained one root only. Standalone sheets also lose project-library
context and cross-sheet connections. Those counts are diagnostic artifacts, not
738 independently confirmed design defects. In particular, Copperhead's green
ERC summary describes only the first root. It does not qualify the project.

The new checker requires one ERC invocation to cover all expected root UUIDs,
so isolated per-file checks cannot accidentally satisfy project coverage. The
first full native run correctly rejected the baseline; no score or board was
promoted. Resolving KiCad's multi-root loading/coverage is an outstanding task.

## Acceptance contract

The native path checks original supporting-file hashes and original board
reference/pad/net mapping; validates report shape, source and exit status; requests
all severities, unconnected items, schematic parity and zone refill; and stores
structured failures. It never maps geometric cleanliness to electrical checks.

A qualified score requires a clean native DRC, resolved 3D model paths, successful
assembly STEP export and an OpenCascade envelope measurement. Five baseline
footprints (J4 and BH1–BH4) have no model; no assembled score is asserted.
The current complete-model gate is intentionally strict, including mounting
features; model/population review is required before refining it.

Automated checks do not prove manufacture, assembly or electrical function. The
optional `--qualification` input is an explicit engineering attestation: matching
`design_sha256`, a nonempty `reviewer`, and literal true values for
`manufacturing`, `assembly`, `electrical`, `connector_compatibility`. The report
records that attestation separately. None has been supplied for this design.
Only with all native and qualification gates satisfied can `--promote-to` copy
the snapshot into a **new** destination. It never overwrites an existing board.
The initial integration does not automatically choose the best score or route a
candidate. Approved native candidates can later be compared by the ordinary score
function, independent of whether Copperhead, JITX or another router produced them.

Still needed: complete routing, verified multi-root connectivity/ERC, assembly
models/envelope, selected fabrication constraints, critical-net engineering and
connector/assembly review. No JLCPCB process or provider has been selected.

Validation of this integration: 30 tests passed, one optional Weave import test
skipped. Tests exercise malformed/missing native evidence, process failure,
unconnected/parity failures, immutable source/rule checks, multi-root coverage,
blocked promotion and actual OpenCascade STEP measurement. They are distinct from
the native baseline smoke run, which correctly fails. Latest full evidence:
`.local/checks/candidate-4xpevryp/failure-record.json` (ignored generated output).
