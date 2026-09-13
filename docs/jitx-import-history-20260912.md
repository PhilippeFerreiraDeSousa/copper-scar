# JITX import experiments — 2026-09-12

Both authorized import paths were exercised. Neither produced a usable JITX PCBGolf design. KiCad can load the complete five-sheet hierarchy and its unchanged physical board. No optimization or accepted candidate resulted.

## Inputs and reproducibility

Reference: `/Users/philippe/dev/PCBGolf`, pinned commit `7210bdb5049c5b7fdf4900a34928e2736767292a`. All reference file hashes verified unchanged after experiments. Repository implementation is isolated at `/Users/philippe/dev/copper-scar-jitx-worktree/integrations/jitx`; original/main and other experiment tracks were not edited. Scripts: `import_experiments.py` constructs initial inputs and records subprocess arguments/results; `audit_import_inputs.py` compares board/netlist connectivity and preserved syntax trees. Additional bounded compatibility invocations are recorded in the evidence directory.

Actual external project, already open in VS Code: `/Users/philippe/dev/copper-scar-jitx`.

Candidate root: `candidates/import-ab-20260912` beneath that project. Evidence root: `runs/import-ab-20260912`. JITX Python/native runtime 4.4.0, KiCad CLI 10.0.6. Import output scaffolds were created before calling the installed importer, as required by its project discovery.

## A — board-only copy

The `board-only` candidate omits all five schematic files while preserving the project, PCB, footprint libraries, 3D models and other support files. Tested directory, `.kicad_pro`, and `.kicad_pcb` inputs with `jitx project import kicad INPUT --output OUTPUT`.

All three returned JSON `success:false` with a consistency failure. Logs include footprint keepout-zone parse errors requiring `net` and `net_name`. These warnings do not establish the sole cause of the final failure. Installed native help exposes import output/field-mapping flags but no board-only mode. No usable generated Python was produced; the only Python files were our empty `converted/__init__.py` scaffolds. Evidence: `a-directory.json`, `a-project.json`, `a-board-file.json` and the corresponding output directories/logs.

Conclusion: board-only import is not demonstrated usable with this installed version and these preserved inputs. This does not prove all possible board-only inputs are unsupported.

## B — coherent full hierarchy

The `hierarchy` candidate contains a new root `pcbgolf.kicad_sch` instantiating all five originals. The former root becomes `power.kicad_sch`. Existing sheet-instance identities are retained under the deterministic wrapper root, symbol instance context and PCB schematic paths are updated, and project hierarchy metadata is updated. `hierarchy-mapping.json` records identities and paths.

Syntax-tree audit confirms all five child sheets are unchanged except instance context. Symbols, multiunits, embedded libraries, wires, power symbols, global labels, no-connect markers and other content remain identical. There are no local labels in these inputs. Board geometry, pad assignments and other PCB contents are identical except schematic path/file metadata. Project settings are identical except hierarchy metadata.

KiCad exports the wrapper plus all five children: 245 components and 1,053 pin memberships. The board has 302 net groups; the hierarchy exports 297. No missing/extra endpoints or split board groups were found. Five apparent merges concern original J3 no-connect pairs: B11/B11T, B10/B10T, B8/B8T, B2/B2T, B3/B3T. Independent export of the untouched original USB sheet produces exactly these same groups, proving they predate hierarchy conversion. Preserve this as an unresolved board-versus-schematic representation difference; do not silently claim exact partition equivalence or rewrite it. J2's CD/DAT3 also differs by KiCad name escaping (`{slash}` versus `/`). Evidence: `input-equivalence.json`, `j3-source-comparison.json`, `source-usb-netlist.xml`, `hierarchy-netlist.xml`.

ERC covers all six sheets and reports zero violations under original settings, including ignored checks. Native PCB DRC with schematic parity reports 180 DRC violations, 499 unconnected items, and seven footprint/symbol BOM-exclusion attribute mismatches. This is full-sheet coverage evidence, not electrical or manufacturing acceptance. Evidence: `hierarchy-erc.json`, `hierarchy-drc.json`, recorded command JSONs.

JITX initially rejected the XML netlist as non-S-expression syntax. A native KiCad S-expression netlist resolved that syntax failure, but import then rejected the directory as containing six root schematics. Retrying conventional spaced sheet-property names and placing all children in a subdirectory produced the same six-root rejection. Logs also contain unsupported netlist groups/variants and board keepout-zone expressions. No generated JITX circuit/board Python exists. Evidence: `b-import.json`, `b-import-sexpr.json`, `b-spaced-import.json`, `b-subdir-import.json` and their output logs.

Conclusion: the hierarchy is usable for KiCad whole-design inspection, with the above original discrepancies; the installed JITX importer still does not accept it. Its root-discovery behavior or supported format needs a further compatibility solution before JITX-native optimization can start. No source sheets were deleted to disguise that problem.

## What is actually visible

Native KiCad PCB Editor was launched with this exact argument:

`/Users/philippe/dev/copper-scar-jitx/candidates/import-ab-20260912/hierarchy/pcbgolf.kicad_pcb`

The `pcbgolf — PCB Editor` window was visually verified showing footprints and ratsnest; status bar shows 302 nets, zero vias and zero track segments. It is the experimental unrouted source, not a JITX-produced result. No board edits or saves were performed. The neighboring `.kicad_pro` and schematic wrapper remain available for project context. Do not assume an open KiCad window automatically reloads externally changed files: reopen the desired checkpoint when needed and preserve any user edits.

The initial standalone application launch crashed in DYLD because the translocated bundle could not locate `@rpath/libkicommon.10.0.6.dylib`. The working launch used `/Users/philippe/Applications/KiCad/KiCad.app/Contents/Applications/pcbnew.app/Contents/MacOS/pcbnew`. No quarantine removal, signing change or installation change was made. KiCad's first-run wizard initialized built-in library tables; automatic update checks were disabled. The crash evidence is `~/Library/Logs/DiagnosticReports/pcbnew-2026-09-12-155742.ips`.

VS Code's existing JITX Board and Schematic panels were inspected directly and both show **Waiting for design**. File writes/import attempts do not create realized board geometry. The installed build command explicitly translates and submits a named design to a runtime; the existing Run/Debug configuration runs `jitx build-all` with the extension's websocket port. A successful design build is required before a corresponding board can be displayed. There is no successful PCBGolf build/capture/render checkpoint to select. The existing `pcbgolf_probe` is only the original two-resistor sample.

Open `JITX-STATUS.md` in the external project for the current checkpoint and result. A static source-layer plot, generated by the working KiCad CLI, is available at `runs/import-ab-20260912/source-board-preview.svg`; it is explicitly a source snapshot, not live JITX geometry.

The full project was subsequently opened in **KiCad Manager** using the installed `KiCad.app/Contents/MacOS/kicad` executable and the exact neighboring `pcbgolf.kicad_pro`. The Manager screenshot visibly confirms the full hierarchy project path. Its root schematic was opened from the project tree. The **pcbgolf — Schematic Editor** screenshot confirms the PCBGolf root and five accessible children: Power, STM32H7, USB + SD, CAN-FD, Channels. No schematic save/conversion was performed. Both native board and schematic views are available; the full project is the entry point for inspecting both.

A separate app-selection attempt for `eeschema.app` also triggered a launch crash while the Manager-hosted schematic was successfully open. Its diagnostic (`eeschema-2026-09-12-160035.ips`) reports DYLD missing `@rpath/libwx_osx_cocoau_gl-3.2.0.dylib` in the translocated standalone bundle. The verified working schematic view is the one opened through the full KiCad Manager. No broken app relaunch or protection changes are needed. JITX VS Code remains the primary intended live view; KiCad is supplementary checkpoint inspection only.
