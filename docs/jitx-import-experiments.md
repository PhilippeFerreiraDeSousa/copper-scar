# JITX full import and preservation audit

Updated 2026-09-12. **The complete PCBGolf design now imports, builds, renders, captures and exports in JITX 4.4.0.** Earlier board-only and hierarchy attempts failed; a compatibility conversion resolved the importer limitations without removing source circuits. Import success is not a valid routed board. Stage One implementation is continuing; see `jitx-plan-and-design.md`.

Reference `/Users/philippe/dev/PCBGolf` at `7210bdb5049c5b7fdf4900a34928e2736767292a` remains untouched. Experiments live in `/Users/philippe/dev/copper-scar-jitx/runs/import-ab-20260912`; transformed copies live under `candidates/import-ab-20260912`. Repository scripts remain isolated in `/Users/philippe/dev/copper-scar-jitx-worktree/integrations/jitx`.

## What resolved the import

1. Preserve all five original schematics beneath a deterministic wrapper root, updating only hierarchy/instance context. KiCad exports all sheets and reports zero ERC findings under the original severity/ignore settings.
2. Centralize legacy sheet and symbol instance metadata on the wrapper. Remove per-symbol modern instance metadata from copied children, which otherwise duplicates units in this importer. The native KiCad netlist remains unchanged by these metadata changes.
3. For the importer input only, remove net assignment fields from 111 explicitly NC physical pads. The importer deletes no-connect nodes before attempting board-net mapping, causing a missing-key failure otherwise. Physical pads and original schematic NC markers remain. Native output expresses 106 logical no-connect declarations, mapping to the same 111 physical pads. The independent checking adapter restores source schematic NC assignments afterward.
4. Add legacy `(net 0)`/`(net_name "")` fields to copied footprint keepout-zone inputs and omit empty netlist groups/variants. Keepout geometry is preserved. Fix generated route/pour flags on PJ-002AH keepouts; the generated default flags were ineffective. Via prohibition remains. Original pad prohibition is still an external-check requirement.
5. Build a fresh named full design `pcbgolf_import.current.PcbgolfFull`. Rebuilding an older loaded identity triggered a native `Illegal tag bits` crash in geometric cache reload. Fresh identities avoid that observed cache path; hot reload is not certified.

The board-only path still failed reference consistency. Rewriting body styles was a rejected diagnostic and is not part of the final solution. No source sheet was deleted to conceal a failure. The deprecated importer returns process zero even with `success:false`; scripts inspect its actual result.

## Preservation evidence

`runtime-preservation.json` records exact matches for 245 component references, 1,066 named physical pads, 191 active electrical net partitions and 111 explicitly NC physical pads. No missing/extra active endpoints or unknown native pin paths were found. Multi-pad ports were expanded by union, not overwritten. Mechanical unnamed pads are outside the named-pad inventory and require geometric qualification.

Source board and schematic differ on five J3 NC pairs: B11/B11T, B10/B10T, B8/B8T, B2/B2T, B3/B3T. Independent export of the untouched USB sheet proves these groupings predate the wrapper. The hierarchy netlist has 297 groups versus the board's 302; active partitions are equivalent. J2's CD/DAT3 name also requires the exact KiCad `{slash}` escape in the final board.

The native KiCad exporter renames four SW1 pad numbers: A/A'/B/B' become A0/A1/B0/B1. The independent adapter allows exactly that reversible component-specific mapping before topology comparison. It restores source values, fields, schematic paths and footprint identities only after the active partition and named pad inventory pass. Physical geometry remains subject to separate verification; inventory equality is not footprint certification.

Successful artifacts: `full-fresh-design-build.json`, `captured-live-view.json`, `capture-legacy-view.log`, `runtime-preservation.json`, `export-preservation.json`. Real native state is in `designs/pcbgolf_import.current.PcbgolfFull`. Its `kicad/` subdirectory contains the full generated project. The two-resistor `pcbgolf_probe` is preserved separately and is not the imported board.

## Validation outcome

Raw export: **58 physical findings, 499 missing connections, 597 parity findings**. The physical findings comprise 28 errors and 30 warnings. Parity comprises 199 value mismatches, 199 missing Name fields and 199 hierarchical net-name differences.

Source-rule identity normalization: **44 physical errors, 224 warnings, 499 missing connections, seven parity warnings, zero ERC findings**. There are28 clearance errors plus16 hole-clearance errors. The16 hole-clearance errors occur inside four source USB connector footprints and also exist in the original PCB. The 224 warnings are 199 library-footprint differences, nine undersized text heights and 16 silk overlaps. Seven source BOM attributes disagree with their symbols. These are retained findings, not waived constraints.

The first routing experiment reduced missing connections to 311 but reported46physical errors versus44at baseline. It was rejected by the non-regression retention gate. The second routed proposal preserves44physical errors and reduces opens to316, and is retained incomplete. These policyv2 comparisons remove legacy embedded netclasses that otherwise override original project rules; earlier counts are superseded. Native checks did not report those exported clearance failures. Native-only validation is therefore not sufficient; the loop uses source-rule KiCad checks for every evaluated candidate.

## Actual views and runtime limitations

VS Code JITX is the live project. Select the full design identity to view its actual native board; import, iteration one and iteration two are separate checkpoints. The original KiCad Manager, PCB Editor and full six-sheet schematic window are supplementary saved source checkpoints; external changes do not make them automatically live.

Legacy viewer capture (`phd.load`) and installed native export work. Modern Python capture routing was incompatible with the installed native listener and is not used. Router acknowledgement occurs before asynchronous physical work finishes. Export refuses while tasks are running; logs and bounded completion handling distinguish busy, timeout and real success.

Earlier failed imports and launch diagnostics are retained in `jitx-import-history-20260912.md`. Standalone translocated KiCad wrappers had missing-library crashes; launching through the installed full bundle worked. No protection bypass, quarantine removal, signing change or new CAD installation was required.
