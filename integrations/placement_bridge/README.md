# Fixed placement / routing bridge proof

This is a file-based **synthetic fixture exchange proof**, not a general placer/router, a PCB Golf optimization result, or permission to merge either upstream track. Copperhead-side `copperhead.py` emits a fixed request and independently consumes the result. `jitx_adapter.py` resolves current native IDs only after parent qualification, then uses the supported native reposition mechanism. Existing anchored vias and incident routes update incrementally.

The eight top-only pads form four complete two-terminal nets on a 32 × 28 mm two-layer board. A top-layer barrier requires six actual 0.60/0.30 mm through vias. The fixed TP4 move is native (8,6) → (10,8), equivalent to KiCad (147.5,102) → (149.5,100). Seven other components and copper on HOLD/CROSS_B/CROSS_C stay fixed. Baseline construction explicitly creates the missing transitions; the qualified incremental parent already contains all six, so the move adds none.

## Modules and contract

- `contract.py`: immutable request identity, complete ref/pad/net/geometry inventory, coordinate frame, fixed refs, source/project hashes, and conservative actual-copper endpoint graph.
- `copperhead.py`: fixed emitter and independent consumer. The consumer makes new external evaluation copies and reruns whole-fixture KiCad DRC twice. It does not accept a producer's claimed score as evidence.
- `fixture_control.py`, `jitx_adapter.py`: one controller lock per runtime, fresh parent export, current native correspondence, bounded native reposition, supported export completion barrier, outward snapshots. An unresolved mutation leaves `.bridge-uncertain.json` and prevents another controller from proceeding. A timeout is never interpreted as cancellation.
- `result.py`: binds request/parent/output hashes, per-net realized coverage, diagnostics, actual pose/copper delta, native route/via preservation and completion evidence to the file-level result.
- `reproduce.py`: creates a new source-only runtime directory and executes baseline → emit → negative requests → qualified move → evaluate → consume. It refuses an existing destination and stops only its own runtime on successful completion. Failed runs remain for diagnosis; never restore their native snapshots into `designs/`.
- `media.py`, `publish.py`: actual exported board snapshots, diagnostic curve and 5× wall-time replay; optional allowlisted publication into the existing W&B/Weave project, in a distinct `synthetic_fixture_bridge` run. No additional server.

The exact saved parent board SHA is required. Fresh JITX exports regenerate `uuid`/`tstamp` metadata and may reorder top-level records. For the live-parent comparison only, `state_sha` removes those two field types recursively and sorts top-level serialized records. All other fields, record multiplicity, numeric geometry and internal polygon/path vertex order remain exact. This is a fixture-qualified serialization comparison, not a general original-board identity conversion. No net-number normalization or geometric rounding is used in this gate.

The graph uses actual segment endpoints, pad centers and through-via transitions, with a 0.00001 mm endpoint tolerance. It refuses arcs and filled copper zones and is intentionally conservative: arbitrary mid-segment junctions or complicated pads can fail it. Full KiCad DRC is independently required, including opens/shorts. The fixture's unchanged configured checks ignore six categories: missing courtyard, track endpoint centered on via, tuning-profile track geometry, symbol footprint filters, PTH inside courtyard and NPTH inside courtyard. This is not an all-checks or assembly/electrical qualification claim.

## Reproduction on this Mac

Installed dependencies used: JITX 4.4.0 and jitxlib-standard 4.4.0 under Python 3.14.6; KiCad CLI 10.0.6 at the path in `verify_incremental_fixture.py`; `sexpdata` in the checker environment. Existing interpreter environments are invoked read-only. Each runtime/source/design state is new and isolated. No original `.jitx/`, `designs/`, authentication file or generated cache is copied.

From this repository root:

```sh
python3 integrations/placement_bridge/reproduce.py /absolute/new/bridge-proof \
  --native-python /Users/philippe/dev/copper-scar-jitx/.venv/bin/python \
  --checker-python /Users/philippe/dev/copper-scar-demo/.venv/bin/python
```

The runtime launcher uses the installed JITX login. Source import is explicitly rooted with `PYTHONPATH` in the new project; the CLI `--project` flag alone did not put it on Python's import path. Keep interpreter symlinks intact: resolving a venv Python symlink to its underlying interpreter loses the venv environment.

```sh
/Users/philippe/dev/copper-scar-demo/.venv/bin/python -m unittest discover \
  -s integrations/placement_bridge/tests -p test_contract.py -v
/Users/philippe/dev/copper-scar-jitx/.venv/bin/python -m unittest discover \
  -s integrations/placement_bridge/tests -p test_native.py -v
```

The checked-in test fixtures are synthetic generated exports/native messages from the first successful bridge, not runtime restore inputs. They exercise stale and wrong mappings, missing fixed refs, incorrect transforms/targets, missing actual vias, a removed bottom segment, serialization noise versus physical changes, immutable requests, native correspondence and unresolved timeout blocking. The shared repository suite is separate: `python -m pytest -q`.

Optional media and already-authorized proof upload (key **file path** only; never put key content in arguments):

```sh
/Users/philippe/dev/copper-scar-demo/.venv/bin/python integrations/placement_bridge/media.py \
  /absolute/completed/bridge-proof /absolute/new/bridge-observability
/Users/philippe/dev/copper-scar-jitx/runs/observability-venv/bin/python \
  integrations/placement_bridge/publish.py /absolute/bridge-observability \
  --key-file /absolute/private/key-file
```

The replay uses completed-snapshot wall timestamps at 5× speed plus a declared one-second final hold. It includes controller/evaluation overhead and must not be described as a native solver benchmark. The uploader reuses the existing track's SDK/REST patterns, verifies all downloaded allowlisted artifact bytes, final image, history and Weave output. Only synthetic board/project files, images/video and request/result/decision JSON are uploaded. Runtime logs, native caches, credentials and unrelated boards are excluded.

## Verified local delivery

Primary final reproduction: `/Users/philippe/.codex/worktrees/ff86/copper-scar/.local/placement-bridge-reproduction-03`.
Runtime: that directory's `runtime/`, identity `bridge_fixture.design.BridgeProof`; stopped after confirmed completion.
Result: `sealed/result.json`; independent decision: `consumer/decision.json`; exact CLI logs: `commands/`.
Initial independent owner-audited proof remains under `.local/placement-bridge/`. An overly strict metadata/order comparison failure is preserved under `.local/placement-bridge-reproduction-02`; it rejected before mutation. The first setup-only failed reproduction is also preserved. All native state remains owned by its originating runtime.

Observability: `/Users/philippe/.codex/worktrees/ff86/copper-scar/.local/placement-bridge-observability`, with verified `upload-receipt.json` and `media/replay-5x.mp4`.

Upstream source provenance and unmodified source hashes are in `provenance.json`. The fixture source and independent checker derive from JITX track commit `d1e545cfc30a324e075dc2c6e76e004e512d16da`; controller changes add relocation, locking and the preflight hook. No proprietary installed JITX implementation is vendored. Copperhead contract context is commit `b1473ba00fec9c78045e632fdc7a7ff52d1c250c`. Both remote branch tips were checked live; neither branch was merged.
