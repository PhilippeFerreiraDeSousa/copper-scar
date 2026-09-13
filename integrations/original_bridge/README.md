# Original R37/R42 bridge qualification

This audit targets the exact retained Copperhead parent, not the earlier expanded SD proposal. It qualifies representation details and tests a minimal correction in disposable copies of **four real components / 160 physical pads**. It does not run placement or routing, claim a closed substitute board, or reset either accepted native state.

## Results

- R37/R42 and all twelve J2 copper and paste pads have exact native polygon unions. Full U3 courtyard, fabrication body outline and silkscreen also match when annotation glyphs are excluded. All 144 U3 copper pads have a measured approximately 0.472 µm rounded-corner polygonization discrepancy; this is not exact equivalence or an approved error tolerance.
- All twelve original unnamed circular NPTHs map to exactly one same-center/same-diameter drill plus an extra **mask-only** exported SMD object. Front/back mask unions are exact. No drill, copper, or mask object is deleted.
- Imported mask expansion uses mitred corners, unlike KiCad's rounded pad-margin geometry. Replacing `JOIN_STYLE.mitre` with `JOIN_STYLE.round` in two copied generated source helpers reduces the maximum R37/R42/J2 mask boundary discrepancy from 21.04 µm to 0.062 µm. Native before/after exports preserve all 160 pad/net assignments, poses, copper and paste. The remaining polygonization is explicitly nonexact.
- The four components touch 112 named nets; 70 have external members, totaling 383 external pad memberships. +3V3 has 46 external pads. The complete boundary manifest stays explicit. The probe omits 241 other footprints; it cannot substitute for full original-board obstacles or be used as an original-board routing score.
- All 44 errors in the accepted JITX checkpoint involve pads explicitly modified by the retained Copperhead footprint repairs. This is parent/provenance evidence, not a differential proof that the repairs alone caused the DRC difference.
- Whole-parent KiCad DRC **with zone refill** repeats Copperhead's 55 opens / 0 errors / 18 warnings and JITX's 310 opens / 44 errors / 237 warnings. The two geometry-only probes each have 48 local opens / 0 violations; those counts omit declared external geometry and are not comparable to full-board loss.
- A real placement trial is rejected before mutation: full parent states, layer profiles and obstacle scope differ, and representation tolerances remain unqualified. A generic multilayer planner and final dielectric/electrical feasibility are not prerequisites imposed on a consistent single-layer proxy; the actual parent/geometry/constraint gates still must pass.

## Source and preservation

`prepare_geometry_probe.py` copies the committed JITX import source and verifies/captures hashes for external STEP assets. It extracts the actual generated `PadMapping` definitions, including J2's four ground-shell pads and U3's **inlined** landpattern. Every local pad/net assignment comes from the retained parent's native inventory; all external endpoints are recorded separately. The source correction changes only the two mask-helper join styles. It neither renames the dynamic `self.solder` feature nor deletes the overlapping unexpanded mask feature.

`native_inventory.py` loads KiCad projects into private memory, localizes footprints only in that unsaved memory and captures native polygon geometry at a 1 nm conversion-error setting. It never calls `SaveBoard`. Annotation glyphs are recorded separately from physical obstacle intent by exclusion from polygon unions; this prevents a `${REFERENCE}` drawing from appearing to be a changed package body.

`normalize_probe_export.py` fixes a separate export-format problem in an **external copy**: legacy `add_net` names with parentheses are unquoted in JITX output. It quotes those names before parsing and removes the obsolete embedded netclass, retaining the exported `.kicad_pro` rule authority. Every other parsed field is asserted unchanged. Raw exports and normalization receipts remain immutable. No `designs/` file is edited.

`capture_geometry_probe.py` only invokes the supported export barrier and read-only native load for the explicitly marked disposable geometry identity. It has no route/reposition operation. `qualify.py` binds exact parent/project/inventory/boundary hashes and emits fail-closed gates; `check_project_copies.py` copies allowlisted support files and reruns whole-project DRC twice with in-memory zone refill, without saving the board. Skipping refill exposed stale cached-plane connectivity (230 opens) and is not the retained parent's accepted evaluation.

## Reproduce on this Mac

Dependencies: existing read-only JITX 4.4.0 / Python 3.14.6 interpreter, KiCad 10.0.6 bundled Python/CLI, and an audit environment with `sexpdata==1.0.2`, `shapely==2.1.2`. A separate audit venv was created under `.local/original-board-qualification/audit-venv`; no owner's environment was modified.

Run from this repository root, choosing a destination that does not exist:

```sh
python3 integrations/original_bridge/reproduce.py \
  --root /absolute/new/original-qualification \
  --parent /Users/philippe/dev/copper-scar-demo/.local/copperhead/candidates/stage1-20260912-182444-f54c2b \
  --jitx /Users/philippe/dev/copper-scar-jitx/candidates/iteration-009-power-neighborhood-routed \
  --source /Users/philippe/dev/copper-scar-jitx-worktree/integrations/jitx/project/pcbgolf_import \
  --assets /Users/philippe/dev/copper-scar-jitx/pcbgolf_import \
  --native-checkpoint /Users/philippe/dev/copper-scar-jitx/runs/stage1/iteration-009-power-neighborhood/routed/after.json \
  --native-python /Users/philippe/dev/copper-scar-jitx/.venv/bin/python \
  --kicad-python /Users/philippe/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 \
  --audit-python /Users/philippe/.codex/worktrees/ff86/copper-scar/.local/original-board-qualification/audit-venv/bin/python
```

The command creates two disposable geometry runtimes, regenerates source/net mappings, captures before/after native exports, verifies the masks/holes/body/complete boundaries, repeats independent DRC, emits the trial rejection and stops its runtimes. A nonzero command is recorded and stops the workflow; inspect the saved artifacts instead of overwriting the destination.

```sh
.local/original-board-qualification/audit-venv/bin/python -m unittest discover \
  -s integrations/original_bridge/tests -v
```

The compressed test fixture contains recorded native R37 geometry from the before/after qualification. Tests check measured mask improvement without falsely calling it exact, preserved copper/paste/pose, stale-parent/mapping/constraint/external-boundary rejection, omitted gate rejection and the permitted single-layer-proxy policy.

## Remaining common-parent transfer decision

The exact retained Copperhead parent contains 245 footprints, 4,480 segments, 668 vias and two GND planes on six layers. JITX's accepted checkpoint has different poses, 1,591 segments plus 1,166 arcs, no via instances/definitions, and two copper layers. The original PCBGolf reference itself has two layers; six layers belong to Copperhead's explicit variant. Its physical dielectric and electrical stack remain unqualified.

Do not blindly apply a pose request between these states. The next concrete technical step is a **bounded exact-copper transfer proof** using the verified source `Copper`, explicit `Via`, and `Pour` primitives, then a reviewed plan to reconstruct one shared full-board parent in a new identity. The newer typed `Route` API authors endpoint/layer intent; its computed traces do not establish exact legacy copper transfer. Whether the 4,480 segments / 668 vias / two planes can survive authoring and interactive movement remains unproven. A fresh routing baseline is a separate explicit choice, not an inevitable outcome or a preserved-incumbent comparison.

Future candidates should bind source-authored component poses, concrete via sites/spans/net attachments and feature-to-feature route intent before native per-layer realization, as clarified by Philippe. This audit does not introduce topology search, merge either branch, mutate accepted state, or publish geometry-only results as W&B routing progress.
