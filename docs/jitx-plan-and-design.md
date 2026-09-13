# Copper Scar: JITX feasibility and size optimization

> Current status: policy-v3 incumbent009 has310 opens,44 errors,237 warnings; no valid board. Native routing stopped. The surviving002 lacks via definitions; source reload is unqualified after007 crash. See [current via and warning review](jitx-via-workflow-and-warning-review.md). Earlier numeric status below describes its recorded experiment.

Updated 2026-09-12. **Authorized implementation in progress. Full import and first routing/export experiment completed. No valid fully routed board exists yet; Stage Two has not started.** HFSS is excluded. Work stays independent of Copperhead's runner and checker.

## Verified state and decision

Use original-rule **KiCad round-trip checks for every evaluated candidate**. JITX native checks supplement generation and provide feedback; they cannot currently replace KiCad DRC/ERC. This decision is based on actual divergent results, not a preference for a particular tool:

- Full five-sheet PCBGolf import builds and renders in JITX 4.4.0. The source reference is commit `7210bdb5049c5b7fdf4900a34928e2736767292a` and remains unchanged.
- Independent native runtime inventory matches 245 components, 1,066 named physical pads, all 191 active net partitions, and 111 explicitly unconnected physical pads. This is electrical inventory evidence, not proof that every geometric/mechanical property survived.
- Raw exported KiCad reports 58 violations, 499 unconnected items, and 597 schematic parity findings. Exit zero means the checker executed, not that the PCB passed.
- The 58 raw findings are 16 hole-clearance errors, five clearance errors, seven solder-mask bridge errors, five library-footprint mismatch warnings, nine text-height warnings, and 16 silkscreen overlap warnings. The parity findings comprise 199 wrong values, 199 missing `Name` fields, and 199 hierarchical net-name mismatches.
- A topology-guarded identity/rule adapter reduces parity to seven pre-existing source BOM attribute disagreements. It restores original net names, source fields and schematic paths, original project rules, 111 physical NC assignments from the authoritative schematic, and four explicitly mapped SW1 pad aliases. Five J3 physical NC pairs were already combined in the source USB schematic; the original PCB's singleton NC names disagree with that schematic. This is recorded source reconciliation, not deletion of no-connect intent.
- A first real native routing pass exported successfully. Independent checking reduced unconnected items from **499 to 311**, but reported **30 clearance errors** plus 16 intrinsic connector hole-clearance errors: 46 physical errors versus the correctly ruled baseline's 44. The retention gate rejected that regression. Native geometry checks still reported no issues. One exported gap was 0.1626 mm against a 0.2 mm minimum.
- Initial feasibility board size was an artificial 300 × 200 mm outline because the source has no outline. Proposal two tested a larger 300 × 300 mm outline for complete component containment, and a 0.25 mm native generation clearance to address the measured export deficit. KiCad's original 0.2 mm rule is unchanged. This margin is an experiment, not a validated universal fix. Under corrected source-rule checking, proposal two has 316 opens and44 physical errors and is retained as the best incomplete checkpoint. No components moved in proposals one/two.

The live external project is `/Users/philippe/dev/copper-scar-jitx`. The completed import is `pcbgolf_import.current.PcbgolfFull`; routed experiment one is `pcbgolf_import.stage_one_001.StageOne001`; proposal two is `pcbgolf_import.stage_one_002.StageOne002`. Each is a complete board, not the old two-resistor probe. VS Code's chosen design controls which checkpoint is shown. KiCad windows are supplementary saved checkpoints and do not automatically follow native edits.

## Placement is an active search variable

The imported `self.place` values are starting positions, not a global runtime lock. This was demonstrated on the complete board: source-parameterized `PlacementProbe` moved/rotated exactly R20 from global(22.159,65.4811,0°) to(10.1686,46.0476,180°), with244other poses unchanged. The same move then succeeded interactively on routed StageOne002 using the installed viewer's `phd.reposition` request with `groups[{id,side,pose}]`. A subsequent load retained the override and actual KiCad export succeeded. No floating/unlock call or wholesale placement deletion was needed.

`Circuit.at(floating=True)` concerns the reference frame and is not presented as an unverified soft-lock solution. Source constructors place descendants in nested parent frames; source edits must compose those frames correctly. Runtime reposition addresses the realized instance-group ID and global pose. In this design a group containing R20 alone permitted individual movement. Moving a multi-component group is different from individually freeing its members. A real unchanged-source full rebuild discarded the interactive R20 override and restored the source pose. The post-build capture confirms exactly that one reset. Therefore accepted search poses must be saved to source parameters before rebuilding; native cache alone is insufficient. Native cache reloads can also crash, so preserve native snapshots independently.

`placement_audit.py` records each moved/rotated reference and before/after coordinates/angle/side, unchanged count, board boundary and layers. `initial-placements.json` retains all imported starting values. `placement_parameters.py` inventories312 source placement requests and changes only named owner-local poses; empty overrides reproduce the source exactly. Campaign manifests support per-candidate `placement_overrides` and save accepted parameter sets separately. The full parameterized design dry-build passed, and12 focused tests cover missing evaluations, regressions, deterministic pose regeneration, unknown placement keys and non-finite values. `reposition_probe.py` implements the verified runtime edit and saves the pre-edit native state. The moved R20 board initially changes316opens to317 with44physical errors, and remained317 after targeted rerouting of its two affected nets. It was rejected against the316-open incumbent; movement capability is proven, placement benefit is not. Connector poses are preserved in this specific local test, not globally frozen without a mechanical reason.

Copperhead coordination is active and implementations remain independent. Its reported successful R17 placement+routing action124→123opens, and screened GND escapes to planes, inform candidate hypotheses. Its experimental footprint repairs remain unqualified and are not copied into this track.

## Boundaries and immutable requirements

All repository work belongs to `/Users/philippe/dev/copper-scar-jitx-worktree`, branch `codex/jitx-optimization`. Do not edit the primary checkout, Copperhead's worktree, or the reference PCBGolf directory. Native runtime, candidate projects, source snapshots and potentially large CAD artifacts stay in the external project. Repository scripts, tests and documents stay in this worktree. No new paid APIs, product publication, package changes, commits or merges are part of this implementation.

The immutable design requirements are the same interfaces and functionality: power supplies and 12 V input, STM32H725, USB hub/host, microSD, four controlled device ports, CAN transceivers, ignition functions, user input and LEDs. Components, values/part identities, active connectivity, explicit NC intent, connector electrical pinouts and mating compatibility must be preserved unless an engineering change is separately evidenced. Moving, rotating, placing on either permitted side, changing board shape, and adding compliant routing/vias are candidate actions. Component deletion, silently dropping pins/nets, changing power or signal relationships, disabling original rule severities, adding blanket DRC exclusions, and removing keepouts are forbidden shortcuts.

Electrical partition equality is a hard proposal gate. Manufacturing, assembly, functionality, connector envelopes and footprint geometry need independent evidence before a board is called valid. Those are still incomplete. A clean DRC or a low cost cannot supply that evidence. Source inconsistencies remain visible: seven BOM attribute mismatches, missing/uncertain assembly models, and 16 USB connector pad-to-NPTH clearances below the original 0.25 mm minimum. The latter persist in the original source and cannot be solved by simply moving complete footprints.

## Stage One: first valid placed and routed board

The implemented loop is:

1. Propose a concrete action with a reason, named unique Python design, bounded runtime and expected metric effect. Save a source snapshot before execution.
2. Build with the installed JITX 4.4.0 runtime. Inspect actual build status and artifacts; capture failure instead of manufacturing a metric.
3. Capture the realized board and optional native non-forced routing. Preserve the pre-route native checkpoint. Requests are the installed viewer's `phd.load` and `phd.route` protocol. Route acknowledgements do not imply all asynchronous physical work completed.
4. Wait for exportable quiescence. The exporter explicitly refuses while physical tasks run. Retry only that documented-in-runtime busy result within a bounded deadline. Timeout or other errors produce an unevaluated failure record; no zero metrics or promotion.
5. Export the actual realized copper to a fresh immutable iteration directory. Capture timings and native findings. Native route count is diagnostic, not proof of a corresponding fully connected KiCad board.
6. Apply `roundtrip.py`: verify pad inventory and full active partition equality before changing identity metadata; restore source rules, source schematic identity and reversible aliases. Preserve copper routing, drills, component placement and physical geometry. Restore original global setup/mask controls as original rules. Log all identity transformations. This does not certify exact footprint geometry.
7. Run all-sheet KiCad ERC and PCB DRC with schematic parity using fresh output files. Check process completion, JSON structure and candidate hashes before/after checking. Parse findings and severities, not only process status.
8. Evaluate hard gates and lexicographic feasibility cost. Record every candidate, rejected regression, metrics, raw findings, next actions, elapsed time and artifact hashes in durable JSONL. Keep separate best-feasibility and best-valid pointers. Rejected candidates remain available for diagnosis.
9. Propose the next change from remaining defects. Do not loop blindly on a failed command or same candidate. Prefer a change that addresses a measured defect class. End Stage One only when explicit validity conditions all pass.

### Cost and retention

For a reliably evaluated, inventory-preserving candidate, the cost is the integer tuple:

`(incorrect_connections, missing_connections, physical_errors, physical_warnings, erc_errors, erc_warnings, parity_issues)`.

Compare lexicographically, not by arbitrary conversion weights. Incorrect connections include physical shorts/crossing nets and unresolved net parity conflicts. Missing connections are KiCad's disconnected-item count, not JITX's different remaining-unroutes statistic. Physical errors/warnings follow original project severities. ERC remains its own category, and any ERC error regression blocks retention independently of tuple order. Parity is retained separately for traceability, even when a net conflict already contributes to the first tier; this is not a weighted sum.

Additional non-regression guards forbid trading fewer missing connections for more incorrect connections, physical errors or ERC errors. Thus experiment one was rejected despite routing progress. Every improvement is still an incomplete feasibility checkpoint until all validity gates pass. Counts are raw units within their category, avoiding unjustified normalization between a short, an open connection and a warning. Future rule-specific prioritization must be explicit, versioned and tested; don't retrospectively rewrite earlier result policies.

Missing report, timeout, malformed metrics, nonzero checker execution, changed files during checks, or missing topology proof gives **unknown cost (`null`) and no retention**. Missing engineering evidence gives **invalid** even when measurable electrical inventory is intact and all counts happen to be zero. Engineering unknowns must remain explicit fields, never silently represented as zero defects.

The current conservative validity criterion requires zero errors, unconnected items, warnings and parity findings, plus evidence-backed footprint, manufacturing, assembly, electrical-functionality and connector-compatibility checks. If reviewed warnings are ever allowed, add a narrow evidence-linked disposition model with original severity retained; no such dispositions are currently fabricated. `best-feasibility.json` can refer to an invalid board. Only `best-valid.json` signifies a valid board.

### Executable implementation

- `integrations/jitx/campaign.py`: explicit proposal → source snapshot → build → native route/capture/export → normalization → evaluate/retain. Separate design identity per proposal avoids observed stale native cache failures.
- `native_iteration.py`: installed viewer protocol, pre-route snapshot, bounded busy-export handling and timings. This is version-pinned integration code, not a claimed stable public API.
- `roundtrip.py`: full active partition gate, four SW1 pad aliases, source schematic NC restoration, source identity and project rules; aborts on unexpected electrical changes.
- `feasibility.py`: reliable execution, fresh report parsing, severity counts, hard gates, lexicographic retention, rejection feedback, artifact hashes and durable JSONL.
- `rule_coverage.py`: inventory of original minima, DRC/ERC severities, netclasses, pin map, keepouts and challenge obligations.
- `differential_checks.py`: real KiCad negative controls for track width, crossing net copper and conflicting electrical pin types.
- `test_feasibility.py`: missing metrics, failed checks, topology failure, physical regression, incomplete improvement and Stage Two admission tests.

Runtime locations are intentionally explicit in this workstation integration. JITX uses its Python 3.14 virtual environment. S-expression normalization uses the already-installed parser environment read-only; this does not invoke Copperhead. Weave is reused only through its existing optional tracing helper. No API key or installed Weave package was present in the current execution environment, so durable local JSONL is the authoritative trace. No model/API calls are made by the campaign.

Example (from this repository worktree):

```sh
python3 integrations/jitx/campaign.py /Users/philippe/dev/copper-scar-jitx/runs/stage1/proposals-002.json
python3 -m unittest discover -s integrations/jitx -p test_feasibility.py -v
```

A manifest proposal requires a fresh ID and fresh fully qualified design name. Existing native state is never silently overwritten by a campaign rerun. The framework does not invent an optimizer or guarantee convergence: the coding assistant authors the next bounded action from the recorded feedback. The independent JITX loop is not wrapped in Copperhead's agent loop.

## Corrected effective-rule baseline

An additional audit found legacy embedded `net_class` blocks in exported `.kicad_pcb` files overriding original `.kicad_pro` defaults. Policyv1 comparisons are explicitly superseded in `policy-v1-invalidation.json`; their artifacts remain intact. `roundtrip.py` removes exporter-only embedded classes, and policyv2 requires that evidence before retention. Corrected comparable results are baseline44errors/499opens, route00146errors/311opens(rejected), route00244errors/316opens(retained incomplete). All have224physical warnings,7pre-existing BOM parity warnings andERC0. This corrects the earlier mistaken characterization of all30clearance findings as newly introduced defects.

The JLCPCB profile investigation and reusable derived four-layer proposal are documented in [jitx-jlcpcb-profile.md](jitx-jlcpcb-profile.md). Package2.0.0 was verified against official documentation and current primary JLCPCB data; it is not blindly applied to the two-layer experiments.

## Checking coverage: native, round trip, hybrid

The exhaustive current inventory is [jitx-rule-coverage.md](jitx-rule-coverage.md), with machine-readable source values and original rule objects in `runs/stage1/rule-coverage.json`. Its 152 entries distinguish translatable but unproven mappings, missing native semantics, partial keepouts, external-only checks and absent source files.

Critical gaps:

- Original default netclass clearance is 0.2 mm; importer initially used only the global minimum 0.0762 mm. Corrected native generation to at least 0.2 mm, without claiming behavioral equivalence. The original 0.2 mm rule is present in every normalized KiCad project.
- Original minimum through-hole drill is 0.2 mm; importer used the microvia minimum 0.1 mm globally. Current two-layer generation uses 0.2 mm. A future microvia design needs proper per-via-class mapping rather than globally relaxing this.
- Original text minimum is 0.8 mm; importer used 0.762 mm. Native minimum was corrected, but existing imported text is still undersized and remains reported.
- Original netclass width, differential-pair rules, source severity policy, ERC pin-type conflict matrix and complete electrical typing are not shown equivalent in JITX. Imported component ports are generic `Port()` objects; no faithful KiCad ERC electrical pin-type translation was found.
- Imported PJ-002AH keepout routes/pours initially had no enabled flags. Native pour/route flags were repaired, and via prohibition retained. Native KeepOut does not expose the original pad prohibition; independent geometric/source keepout validation is still required.
- No source `.dru` exists. That is absence of that file, not proof the board needs no custom engineering constraints.
- Challenge requirements—manufacturable by JLCPCB, assemblable, working and usable, mating-compatible—are not established by native or KiCad DRC alone.

| Option | Demonstrated coverage | Decision |
|---|---|---|
| A: native only | Useful route/build checks and connectivity diagnostics; missed physical source errors and exported clearance violations; ERC and full rule equivalence absent | Reject for acceptance and best-checkpoint evaluation |
| B: export + original KiCad each evaluated iteration | Original supported DRC/ERC/severity semantics and schematic parity; normalization plus topology guards needed; independent engineering still required | Current default |
| C: native inner operations, authoritative round-trip at candidate boundaries | Can reject obviously broken native builds early, then evaluate every retained candidate with B | Current practical hybrid, with no skipped authoritative acceptance checks |

Measured negative controls (one local run, not a statistical speed benchmark): control DRC 1.44 s; thin-track DRC 1.19 s adds one `track_width`; crossing-net DRC 1.22 s adds one `tracks_crossing`; modified schematic electrical pin types produce 632 `pin_to_pin` ERC errors in 1.52 s. Original all-sheet ERC is zero under its existing ignore settings. The first attempted short fixture lacked anchored pads and KiCad reassigned the tracks' net; it was rejected as an invalid test and replaced by explicitly anchored opposite-net pads. That failed fixture remains archived.

Native capture takes roughly 0.2–0.8 s but is not the same task as authoritative checking. Identity normalization took about 1.1 s; normalized DRC+ERC evaluation about 2.6–2.9 s; a successful first routed export including the last remaining wait took 6.0 s after routing had already run for minutes. These cannot support a claim that native checks are equivalent or faster for equal coverage. Native route acknowledgements returned in seconds while actual work continued for several minutes.

Migration criteria: construct source-rule positive and negative boundary cases for each rule proposed for migration; compare pass/fail, locations and original severity against KiCad; test original NC/multipad semantics, real short/open injections, hole and mask constraints, forbidden pad/via/route placement, edge clearance, differential pairs, ERC pin conflicts and assembly invariants. Validate actual exported geometry with a declared numerical tolerance. Require zero unexplained false negatives across representative designs and record median/p95 time for equal-coverage workloads. Keep every untranslated/unsupported check external. Re-run certification after JITX/KiCad/exporter upgrades. The current real-world clearance counterexample must be resolved before any physical-clearance equivalence claim.

## Stage Two: optimize only accepted boards

The official PCBGolf objective is **assembled PCBA bounding-box volume in mm³ + 50 × via count + 5,000 × copper-layer count**. Bare board area or board volume is not the official volume. Count physical vias and copper layers in the final verified export and derive the assembled envelope from a complete, correctly transformed assembly model. Missing component models, incorrect units, omitted connectors or absent mating/mechanical evidence yield no valid score.

Stage Two begins from a saved valid Stage One checkpoint. Propose a smaller outline, component rearrangement, permitted side change, routing/via reduction or justified layer change; regenerate/export and run the same complete validity gates. Reject any loss of validity regardless of numerical score. Retain only a strictly smaller official score among valid candidates; preserve the previous valid board otherwise. Record volume, via and layer contributions separately to make tradeoffs reviewable. Current implementation has the objective/admission function, but no Stage Two campaign has run because no valid assembly exists.

## Next executable work and stopping conditions

1. Finish proposal two, independently evaluate the resulting copper, and compare against the preserved baseline with the same rules. Keep its source, native messages, timings and KiCad artifacts even if rejected.
2. Verify placement/complete geometry lies inside the signal/board boundary; use the actual component outlines rather than center points. A route warning about off-board pads is a failed placement condition, not harmless UI text.
3. Partition remaining opens into same-layer paths, needed layer transitions and congestion; introduce explicit compliant vias/route structure where native one-layer routing cannot connect SMD endpoints across obstacles. Avoid repeated blind full-board route requests.
4. Resolve the intrinsic USB connector pad-to-NPTH rule conflict against manufacturer landpattern and assembly requirements. A clearance exception cannot be invented. Any corrected pad geometry needs manufacturer-backed solder/mechanical compatibility and source-footprint comparison.
5. Resolve the seven source BOM disagreements and missing assembly models with explicit design-intent evidence. Restore proper silk/text and validate exact exported mask/paste/pad/keepout geometry. Library mismatch warnings are not automatically waived merely because an exporter changes representation.
6. Continue measurable feasibility proposals. A runtime timeout, unsupported operation or missing engineering evidence is reported precisely with saved reproduction and next dependency. Never mark Stage One complete merely because import/build/routing returned successfully or a run budget ended.

The earlier research-only proposal is retained separately as history. It is superseded by this verified implementation state and does not revoke the user's authorization to continue.
