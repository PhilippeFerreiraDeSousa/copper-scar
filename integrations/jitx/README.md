# JITX checkpoint

This directory saves the completed JITX track independently of the common Copper Scar CLI/checker and the Copperhead checkout. It is a research checkpoint, not a valid routed-board release.

Current independently checked incumbent009: **310 missing connections,0 incorrect,44 physical errors,237 warnings,7 parity findings,ERC0** under policyv3. No valid board or Stage Two score exists. The thirteen added warnings involve LED9/C51 silkscreen and mask clipping; they remain assembly issues despite lower diagnostic cost. See `../../docs/jitx-via-workflow-and-warning-review.md`.

## Included source

- Python import/normalization, immutable circuit/rule checks, placement parameters, native capture/routing adapters, copper-preservation audits, measured process records, dashboard and replay service, and tests.
- `project/pcbgolf_import/`: full imported245-component circuit, component/landpattern/symbol definitions, source rule/stackup definitions, experimental wrappers and authored profile changes. Imported starting placements remain source inputs, not locks. `project/pcbgolf_probe/` preserves the separate two-resistor smoke example.
- `project/source-manifest.json`: source hashes and a manifest for28 excluded STEP assets. Eighteen model copies match the pinned original byte-for-byte; ten imported copies differ and require their exact preserved external assets (or a verified repeat of the pinned importer). Never silently substitute a different model and call3D qualification complete.
- `checkpoints/009/`: complete accepted placement source, proposal/parameters, warning review, compact checked summary and board/rule hashes. The optional via source is separately named and was only translated offline; it is not the accepted native design.

The imported Python derives from the PCBGolf reference at commit `7210bdb5049c5b7fdf4900a34928e2736767292a`, through JITX4.4.0 and the recorded hierarchy/no-connect normalization. Preserve upstream attribution and any upstream asset terms. This checkpoint does not relicense upstream design/model content. Geometry, manufacturing, assembly and SI qualification remain incomplete.

## Reproduce source validation without native mutation

Use the pinned project dependencies (`jitx==4.4.0`, `jitxlib-standard==4.4.0`, `jitxlib-jlcpcb==2.0.0`). Validation here used Python3.14.6. The tooling environment additionally needs `sexpdata` and `matplotlib`; rendering uses KiCadCLI10.0.6, `rsvg-convert`, `ffmpeg` and `ffprobe`. These dependency declarations are local to this integration; the shared project manifest is untouched.

From the repository root, prepare a **new** directory using the exact local asset source retained from this campaign:

```sh
python integrations/jitx/prepare_project.py /tmp/jitx-checkpoint-project \
  --asset-source /Users/philippe/dev/copper-scar-jitx \
  --accepted009 --via-proposal
```

The script verifies all286 Python source hashes and all28 external model hashes before writing. It refuses an existing destination or any path inside `designs/` or `.jitx/`. No native cache, generated copper, credentials, or runtime configuration is copied. Without the two optional flags it prepares the original saved source; `--accepted009` installs the saved accepted source inputs into the new copy; `--via-proposal` additionally selects the offline0.60/0.30mm through-via proposal.

Using a Python environment with JITX4.4.0 installed:

```sh
python integrations/jitx/dry_check_project.py /tmp/jitx-checkpoint-project --expect-via
python -m unittest discover -s integrations/jitx -p 'test_*.py'
```

The dry checker asserts the imported module resolves inside the prepared project (avoiding an installed editable-package shadow), uses `DryRunBuilder` without connecting to the runtime, checks the emitted via fields, and verifies no `designs/` directory was created. The28 STEP assets remain a separate local prerequisite and are intentionally not published in Git.

## Live workbench and retained-state limit

The existing adapters preserve their measured local workbench paths: project `/Users/philippe/dev/copper-scar-jitx`, reference `/Users/philippe/dev/PCBGolf`, and installed tool/runtime paths. Relocating the live workbench requires updating those explicit paths; this checkpoint does not pretend to be a portable one-command optimizer. Do not run the historical import/reevaluation scripts against populated output directories. No native capture runs just by running the dry checker or unit tests.

JITX exclusively owns native `designs/<identity>/` files. Outward snapshots are read-only evidence, never restore inputs. Live accepted002 has no via definitions. Source-level registration requires a full native design load, and the unchanged same-identity rebuild007 crashed another physical client with `Illegal tag bits`. Safe reload retaining the accepted layout is unqualified. Do not fresh-build away existing routes or apply the offline via proposal to live002 as an automatic checkpoint step.

Trial009 routed seven incident nets, **not the full board**. The full-board invocation audit is a separate follow-up; absence of vias prevents interpreting prior incomplete routing as placement infeasibility. No automatic fresh reset, merge, deployment or further optimization is part of this source checkpoint.

## Local records intentionally excluded

The live `.venv`, `.jitx` connection/authentication data, VSCode/user configuration, native `designs/`, caches, generated binaries, all candidates and routed KiCad boards, complete run/checker logs, manufacturer PDFs, screenshots, video files and STEP models remain in the external project/output directories. Git contains only source, compact provenance/summary records and reproducibility manifests. The accepted board hash is saved in `checkpoints/009/summary.json`; that hash is evidence identity, not a reconstruction of retained native copper.

Dashboard: `http://127.0.0.1:53919/`. “Replay to latest”: `http://127.0.0.1:53919/replay`. The action freezes completed published checkpoints, deduplicates corrected rechecks, renders/reuses a cutoff-keyed5× video, and restarts from the beginning. It includes failed/rejected attempts, excludes unreliable measurements from the curve, queues newer cutoffs during rendering, and labels the earliest available state. Replay requires the excluded local ledger/previews; a fresh source checkout cannot invent historical boards. Old fixed-cutoff videos remain historical.
