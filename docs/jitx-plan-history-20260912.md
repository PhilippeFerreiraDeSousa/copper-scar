# Copper Scar: JITX plan and design

Document date: 2026-09-12. Status: proposed implementation plan for review; documentation only in this phase. Earlier bounded research is complete. No new implementation or optimization campaign is authorized by this document.

Research date: 2026-09-12. Installed JITX/Python packages: 4.4.0. Official PCBGolf source: `7210bdb5049c5b7fdf4900a34928e2736767292a`. Public JITX skills inspected at `bd4cb45905e27b8e472cd01276fdcc744ee39f5b`.

## Recommendation

**Proposed direction for review: preserve JITX as a full design-and-optimization candidate, prove its compatibility gates, and keep the native KiCad/Copperhead path available until those gates pass.** JITX has useful real design/routing infrastructure and a Python feedback surface. However, its actual importer rejects PCBGolf's five independent root schematics. The earlier runtime submission required authentication; Philippe subsequently reported successful VS Code sign-in, which has not yet been followed by an authenticated build test. Neither routing this board nor a lossless KiCad/STEP export has been demonstrated.

The most reusable architecture is an existing coding assistant editing JITX Python, using JITX's own runtime, native checks and export facilities. Export selected checkpoints for independent KiCad comparison and final validation. Benchmark whether translated checks permit a faster inner loop before asserting a speedup. Do not build another CAD kernel, and do not nest Copperhead's full agent loop around another autonomous JITX agent. Retain separate generation approaches behind the existing candidate-directory boundary.

HFSS is excluded. A useful loop can use connectivity, native DRC, assembly envelope, via count, layer count, and engineering constraints as feedback. A clean DRC alone cannot establish electrical functionality or connector usability.

## What actually ships

| Stage | JITX 4.4 evidence | What Copper Scar still supplies |
|---|---|---|
| Proposal and editing | Customer's coding assistant edits Python; JITX does not bundle a model. Public skill bundle contains workflow instructions, component/layout guidance, review templates and small lint/extraction helpers. | Objective, candidate budget, permitted edits, experiment selection and challenge-specific acceptance. |
| Design construction | `Design`, `Circuit`, `Component`, `Port`/`Net`, `Board`, `Substrate`, `Placement`, `Via`, `Route`, tags and `design_constraint`. Structural Python objects translate into runtime input. | Faithful conversion of the original circuit and original mechanical/electrical constraints. |
| Placement and routing | Code placement and per-layer `Route(source, destination, layer, ...)`; sketches/control points; deterministic native geometry/constraint/routing engines. | Placement search, layer/via strategy and proof of complete board routing. No public all-board placement optimizer or `route_all()` Python call was found in the installed package. |
| Build | `jitx design build`; `Runtime.submit()` and synchronous/asynchronous wrappers. | Enforce process timeout and parse structured outcome, not merely exit code. |
| Read solver output | `Runtime.capture()` gets layout output and attaches solved geometry to the Python design; `RuntimeDesign.query()`, `.nets()`, `.layers()`. `Route.traces` becomes available after capture. | Translate relevant findings into the next proposal; retain immutable inputs/outputs. |
| Export | Registered `Export` plugins and hooks: `preflight`, `submitted`, `export`. Installed commands include `legacy-kicad` and `legacy-step`. | Verify export completion/path, full artifact content and provenance. Independent assembly STEP measurement remains the final comparison evidence; its exact exporter must be qualified. |
| Persistent learning | Design rules are Python source. Runtime capture mutates the in-memory object model; it is not evidence of an LLM editing source or a durable learned-rule database. | Agent writes justified source constraints; retain evidence-linked scars/decisions, regression checks and challenger/incumbent comparison. |

JITX's architecture docs explicitly describe the approved external assistant and ordinary deterministic engines. The homepage describes a feedback loop, including use of the customer's own checker; that does not establish a packaged optimizer with candidate selection and persistent learning. [Architecture](https://docs.jitx.com/en/latest/jumpstart-kits/shared/JITX_Architecture_and_Systems_Requirements_v2_0.html), [homepage](https://www.jitx.com/).

The shipped `jitx-skills` tree is substantial workflow guidance, not a Python agent runner. Its complete-board flow delegates component/circuit tasks, reviews the assembled system, then builds/verifies/iterates. Executable helpers inspected were pattern checks, datasheet extraction/tests and plugin-manifest validation. No general proposal→score→select→write-back controller was found there. These files were inspected as research material, not installed as active skills. [Repository](https://github.com/JITx-Inc/jitx-skills).

**Reuse qualification:** although the architecture page calls the skills bundle open, the inspected repository's `LICENSE` says all rights reserved and requires a separate written agreement for copying/modification/distribution. Do not vendor it into Copper Scar on an assumption of a permissive license. The `jitx` wheel is also marked proprietary. Invocation of installed software and redistribution of its implementation are different integration choices. [Inspected license](https://github.com/JITx-Inc/jitx-skills/blob/bd4cb45905e27b8e472cd01276fdcc744ee39f5b/LICENSE).

## Original execution evidence

All earlier generated research artifacts are in `/private/tmp/copper-scar-jitx-research`. This canonical plan resides in the separate JITX experiment project; the identical review copy resides in the Main task outputs directory. The original PCBGolf and Copper Scar main checkouts remained clean. This task made no model calls, created no account, ran no paid jobs and made no product commits, pushes or merges. Philippe later reported completing sign-in himself. The temporary runtime was stopped after the probe.

1. **Python translation succeeds.** The installed two-resistor scaffold was copied into scratch. `design build ... --dry --no-dependency-check` returned `status: ok` and a 64KB translated payload. This proves executable Python construction/translation only. It is not a PCBGolf board and proves no fabrication, routing or score. See [dry output](/private/tmp/copper-scar-jitx-research/dry-build.stdout.json) and [payload](/private/tmp/copper-scar-jitx-research/dry-payload.txt).
2. **Hidden importer is callable.** `jitx project import kicad --help` works, although `jitx project --help` omits import. Installed source registers it with `hidden=True` and labels it deprecated, pending removal. It forwards to the native `import-kicad` launcher. The destination must exist and contain a Python package; an empty destination is insufficient.
3. **Importing the real `.kicad_pro` fails.** With a prepared package destination, the log warns that a netlist or PCB is missing and nets will not be imported, then fails its reference-designator consistency pass. The source PCB is present on disk, so the warning is importer behavior, not proof the challenge omitted it. [Result](/private/tmp/copper-scar-jitx-research/import-probe-package.json), [native log](/private/tmp/copper-scar-jitx-research/imported/imported_board/imports/Pcbgolf/log.txt).
4. **Importing the real directory gives the decisive limitation.** It explicitly reports five root schematic files, says it expects a single design and refuses the import. Do not follow its suggestion to delete all but one root: all five circuits must survive. This establishes unsupported direct multi-root ingestion in this probe; it does not prove every possible faithful conversion is impossible. [Result](/private/tmp/copper-scar-jitx-research/import-directory-probe.json).
5. **Import errors return process exit 0.** Every failed import above returned a JSON envelope with `success: false`. The adapter must reject such results and missing/partial artifacts, even if the process exited cleanly.
6. **Historical pre-login test: local runtime starts, but submission was unauthenticated.** `auth show` reported no license file and `Authorized: no`. After local runtime startup and an explicit Python `Runtime(uri=...)` connection, submission returned `ErrorMessage: You are not authenticated`. No design capture or export completed. [Python probe](/private/tmp/copper-scar-jitx-research/runtime_probe.py), [result](/private/tmp/copper-scar-jitx-research/runtime-api-probe.json).
7. **Additional integration rough edges:** default runtime discovery did not produce a usable manifest in this scratch run; the printed websocket URL's trailing slash was rejected, while the normalized path reached the authentication gate. The CLI's explicit URI build still sought a project announcement. These are observed local failures, not a claim all 4.4 installations fail. Also, `--dry` alone still ran the dependency check despite help claiming it skips it; add `--no-dependency-check`. The `--dump` payload is text-format data, not JSON, regardless of its filename.

There is no successful import→compile/route→KiCad+STEP→native-check run to report. Authentication alone will not remove the demonstrated five-root importer limitation.

## Routing and export proof boundaries

The documented topological router operates one layer at a time. Routes connect pads/vias/control points and respect applicable geometry rules; layer transitions require additional structure. Moving components causes route re-realization. A topological route may exist while concrete copper realization fails, leaving a rubber-band representation. Therefore neither a build success nor an apparent route in the UI establishes complete routed copper. [Autorouter documentation](https://docs.jitx.com/en/latest/essentials/physical_design/autorouter.html).

The actual 4.4 export syntax differs from older PyPI README examples:

```sh
jitx design export legacy-kicad package.module.DesignClass
jitx design export legacy-step package.module.DesignClass
```

The installed export implementation **instantiates/submits the design again, captures output, then calls the exporter**. It is not simply exporting a previously selected immutable checkpoint. Before trusting optimization results, verify that interactive placement/routes survive this sequence and that both exports correspond to the same exact state. Legacy exporters expose no output-path option in their current help. Automated destination discovery and completion handling remain unproven. [Installed export source](/Users/philippe/dev/copper-scar-jitx/.venv/lib/python3.14/site-packages/jitx/_cli/design/export.py:58).

Useful Python reuse is `Runtime.submit/capture`, `RuntimeDesign.query`, and the `Export` lifecycle, rather than copying private websocket messages or reverse-flow internals. A future small exporter hook could capture diagnostic counts, but it must not replace native KiCad acceptance. [Installed runtime API](/Users/philippe/dev/copper-scar-jitx/.venv/lib/python3.14/site-packages/jitx/run/runtime.py:140).

## Round-trip fidelity gate

| Invariant | Current proof | Required before acceptance |
|---|---|---|
| Components, pins, nets | No successful JITX import. Original board mapping is available; five-root schematic equivalence is unresolved in the shared checker. | Complete reference/value/part and pin-to-net equality, cross-root global labels, unconnected pins and multi-unit components accounted for. Never treat one-root ERC as whole-project coverage. |
| Footprint geometry | Import/export capability advertised; no tested fidelity. | Pad numbers/types/shapes/layers, drills/plating, offsets, courtyard and mask/paste compared. Allow only explicitly intended placement/rotation/side changes. |
| Rules | No demonstrated translation of `.kicad_pro` netclasses, minima, severities or exclusions to/from Python. | Preserve original support files; add reviewed fab/electrical constraints in both native acceptance and JITX generation. Compare effective rules, not just names. |
| Models and assembly | STEP exporter exists; not executed. Shared checker notes missing baseline models. | Preserve model references, transforms and units; resolve populated assembly parts and connector mating envelopes; independently export/measure assembly. |
| Schematics/project identity | Direct five-root import rejected. | A verified single-root conversion or separate composition with exact global connectivity and provenance, followed by native all-sheet validation. No source-sheet deletion. |

For an initial bridge, put only the exported PCB into a fresh copy of the original project/support files. This keeps the original rules, libraries and models authoritative. It is a **proposal**, not a bypass: exported footprints must still retain original model references and schematic identity, and native parity/geometry checks must pass. If JITX replaces footprint UUIDs, paths, net names or model transforms, this transplant may fail legitimately. Any normalization must have a narrow, reviewed equivalence rule and reversible mapping.

The shared checker currently rejects changed support-file hashes. Do not weaken it for JITX. A five-sheet conversion needed inside JITX can remain an internal representation; the final candidate must still be checked against the original. The absence of a complete explicit rule set in PCBGolf also means preserving files alone is insufficient engineering qualification. [Official challenge](https://github.com/commaai/PCBGolf).

## Copperhead overlap and coexistence

| Flow | Copperhead 0.10.0 | JITX route |
|---|---|---|
| Agent | Ships provider interface, turn loop, budgets, retries and transcripts. | Existing Codex/Claude/Cursor-style coding assistant runs the workflow. |
| Edit | Dispatches its own file/design tools against KiCad. | Assistant edits Python design/placement/constraints. |
| Generate | KiCad utilities; no autorouter tool found in the inspected catalog. | Native JITX construction and routing engines. |
| Check | ERC/DRC, document drift, obligations and finish gates. | JITX build/capture plus exported candidate's shared native check. |
| Remember | `record_constraint`, affected-item obligations, decisions and dual-written docs. | Python rules plus Copper Scar evidence-linked decisions/scars. |
| Accept | Copperhead's own run/commit gate. | Shared Copper Scar validator/promotion policy controls challenge acceptance. |

The installed Copperhead source concretely contains `agent/loop.ts`, `tools.ts`, provider adapters and constraint persistence. Its Codex provider uses the saved-login SDK as a reasoning backend and keeps Copperhead as tool dispatcher. This is materially more agent orchestration than JITX's public Python package supplies. It is also coupled to Copperhead's tool catalog: JITX cannot be dropped into that catalog without an explicit tool integration. [Loop source](/Users/philippe/dev/copper-scar-demo/node_modules/copperhead/src/agent/loop.ts), [tool source](/Users/philippe/dev/copper-scar-demo/node_modules/copperhead/src/agent/tools.ts).

Simplest same-main layout: separate JITX-specific scripts/design modules and Copperhead-specific scripts; each works on its own candidate directory, runtime and run folder. Both invoke:

```sh
copper-scar real-check \
  --project <candidate>/pcbgolf.kicad_pro \
  --reference <original>/pcbgolf.kicad_pro \
  --out-dir <approach-specific-runs> \
  --kicad <verified-kicad-cli>
```

Keep the common checker, score and record schema under one owner. Integrate independent branch changes into main only after review. No generic adapter framework is required. Each approach may have its own internal agent loop, while the outer experiment comparison consumes the same hashed candidate and validation record.

Retain Weave for proposal→edit→generate→check traces, comparison and artifacts. Retain scars only as measured, scoped constraints tied to a failure record and a successful recheck; do not carry the simulator's hand-coded keepout rectangles forward as learned PCB knowledge. Persistent rule updates are adaptation, not model-weight training. For an improving-loop demonstration, replay the same initial state with and without the retained rule and show fewer repeated failures or a better valid incumbent.

## Access, gates and realistic effort

The current plan page offers unlimited design complexity and KiCad integration in Free and Open, but specifically limits designs to CERN OHL-Permissive v2 and excludes proprietary/copyleft designs. Exact activated router/export entitlements have not been verified. The PCBGolf checkout has no top-level LICENSE file; do not assume its publicly available challenge files automatically satisfy JITX's design-license condition. This is a condition to resolve, not permission to relicense upstream files. [Plans](https://www.jitx.com/plans).

Existing setup is reusable: CLI `/Users/philippe/dev/copper-scar-jitx/.venv/bin/jitx`, runtime `/Users/philippe/.jitx/4.4.0`, Python 3.14 environment. No duplicate installation is needed. Official metadata requires Python 3.12+ and lists macOS/Linux/Windows. Package installation, authentication, successful design execution, and engineering qualification are separate gates. Existing coding-assistant access can remain the model interface; no new metered provider is architecturally necessary.

Proposed sequence and estimates below are engineering estimates, not measured delivery promises:

1. **Access and 2-component round trip: half a day after access is ready.** Philippe reports login is complete; verify current authorization without printing tokens, and confirm applicable design licensing. Submit/capture a tiny real design, realize copper, export KiCad/STEP, and run native checks. Gate: exact pins/geometry survive and automated checkpoint export is repeatable. Stop if export requires unresolved manual state or privileges.
2. **PCBGolf fidelity: 1–3 engineering days if a documented faithful conversion exists; unbounded if importer support requires vendor work.** Resolve five-root representation without losing global connectivity, then perform a no-optimization round trip. Gate: component/pad/net/model/rule invariants and complete native schematic coverage. Stop before optimization if any circuit is lost.
3. **Routing checkpoint: 1–2 days to prove the API strategy, not to finish this board.** Prove layer/via placement and route completion on a representative preserved circuit, then attempt the complete original board. Gate: complete connectivity, concrete copper, acceptable DRC and reproducible exports. Do not assume the per-layer router solves whole-board placement or via planning.
4. **Bounded learning loop: roughly 1–2 days once those gates pass.** One proposal per candidate, native failure feedback, evidence-backed rule edit, rerun and incumbent comparison. Engineering qualification and compacting all 245 footprints can take substantially longer.

Today the correct status is **research completed; implementation qualification pending compatibility work and a post-sign-in runtime check**. There is enough shipped infrastructure to justify a probe, but insufficient evidence to promise a weekend-ready valid PCBGolf board or to retire the parallel KiCad/Copperhead approach.


## Current workspace and responsibility map

Task metadata still names `/Users/philippe/dev/copper-scar`, but all future repository commands and edits must use the explicit cwd `/Users/philippe/dev/copper-scar-jitx-worktree`, branch `codex/jitx-optimization`. This registered worktree was created from main commit `27846f947b19588c271856001379e30da503ee1e`. The existing sibling `/Users/philippe/dev/copper-scar-jitx` remains an external experiment project and environment; it is not itself a git worktree or a security sandbox. Neither directory is integrated into main merely by existing.

| Purpose | Exact path / owner | Present status |
|---|---|---|
| Shared main checkout / task metadata cwd only | `/Users/philippe/dev/copper-scar` | Existing simulator and scoring/Weave scaffolding; this documentation task does not edit it. |
| Dedicated JITX repository worktree | `/Users/philippe/dev/copper-scar-jitx-worktree`, branch `codex/jitx-optimization` | Registered worktree; explicit cwd for every future repository mutation. |
| JITX Python project | `/Users/philippe/dev/copper-scar-jitx` | Official generated two-resistor scaffold, venv and editor settings; not PCBGolf conversion. |
| JITX project CLI | `/Users/philippe/dev/copper-scar-jitx/.venv/bin/jitx` | 4.4.0, Python 3.14.6. |
| Extension global CLI | `/Users/philippe/.jitx/.venv/bin/jitx` | Separate 4.4.0 environment; used by VS Code bootstrap. |
| Native runtime | `/Users/philippe/.jitx/4.4.0`; symlink `/Users/philippe/.jitx/current` | Official installation, verified matching 4.4.0. |
| Extension | `/Users/philippe/.vscode/extensions/jitx.jitx-vscode-4.4.0` | Official Marketplace package; do not patch bundled extension as an integration strategy. |
| Research scratch and execution evidence | `/private/tmp/copper-scar-jitx-research` | Report, import probes/logs, dry build, runtime API probe and inspected public skills checkout. Temporary storage; archive evidence before cleanup. |
| Immutable reference checkout | `/Users/philippe/dev/PCBGolf` | Verified pinned SHA above. Preserve all five roots, board, libraries, rules and models. |
| Core/native owner | Task `01a0978d-25db-7930-b0da-d69de0304648`, `/Users/philippe/dev/copper-scar-demo` | Native checker integration at commit `9b72b82`, branch `codex/demo-takeover`; no integration into main assumed. |
| Native evidence | `/Users/philippe/dev/copper-scar-demo/.local/checks/candidate-4xpevryp/failure-record.json` | Failed official baseline, not an accepted candidate. |
| Native source/candidate copies | `/Users/philippe/dev/copper-scar-demo/.local/pcbgolf-source` and `.local/pcbgolf-candidate` | Core-owned copies; JITX must create its own candidate directories. |
| KiCad | `/Users/philippe/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli` | 10.0.6; use this executable explicitly. |
| Autorouter evidence | `/Users/philippe/.codex/worktrees/408e/copper-scar/investigation` | Separate task `01a0979f-ec8a-70a3-abec-489822c151f0`; research artifacts, not a qualified PCB. |
| Canonical plan | `/Users/philippe/dev/copper-scar-jitx/docs/jitx-plan-and-design.md` | This document. |
| Review copy | `/Users/philippe/Documents/Codex/2026-09-12/realtime-voice-chat/outputs/jitx-plan-and-design.md` | Byte-identical copy for review alongside the Copperhead plan. |

Isolation is established now: use the registered `codex/jitx-optimization` worktree. Its initial base is main `27846f9`; it does not contain the separate core worktree commit `9b72b82`. Any adoption of core changes requires owner coordination, not an implicit merge or cherry-pick. JITX-owned files should stay under an approach-specific directory such as `integrations/jitx/` plus its own documentation/tests. This is a proposed ownership layout, not a directory tree created by this task. Core retains `copper_scar/real.py`, CLI entry points, shared scoring/scars, record schema, dependency manifests and native tests. Request reviewed core changes when required rather than editing those files concurrently. Copperhead's own implementation remains with its owner. The JITX project must not be copied wholesale into main with `.venv`, generated logs or runtime state.

## Runtime repair and latest access status

The initial installation failure named `~/.jitx/.venv/.../anyio/_core/_sockets.py`. Inspection found two VS Code window logs creating and populating the same global venv, one failing on AnyIO and another on `websockets-15.0.1.dist-info/WHEEL`. This supports a concurrent-bootstrap explanation; the logs did not supply enough timing evidence to prove the exact race. No installer was active when inspected. About 45 GiB was free, so current disk exhaustion was not established.

By inspection time, all installed package files were present: 2,889 SHA-256 RECORD entries matched, imports of AnyIO/websockets/httpx/JITX passed, and `pip check` was clean. The extension's own bootstrap command, `python -m pip install --upgrade 'jitx>=4.4.0,<4.5'`, then succeeded with dependencies already satisfied. `jitx --format json runtime update --version 4.4.0` returned `action: noop`, `installed_version: 4.4.0`. The affected VS Code window was reloaded and reached sign-in. No environment replacement, pip upgrade, Python downgrade or configuration/credential edits were needed.

Logs are in `/Users/philippe/Library/Application Support/Code/logs/20260911T151334/window6/exthost/output_logging_20260912T143236/4-jitx-log.log` and `window2/exthost/output_logging_20260911T151336/3-jitx-log.log` under the same log root. Avoid publishing full logs without checking for credentials or signed URLs.

Philippe subsequently said he signed in. This task opened the exact existing JITX project in a new VS Code window and verified its Explorer files. The last UI inspection showed Restricted Mode for that folder. Trust/activation may have changed since then; neither successful post-login compilation nor present license entitlements are asserted. At the next implementation session, verify the selected project, folder trust and authorization, then run the bounded smoke check. Do not ask for credentials in task text or accept terms on the user's behalf. Do not change the shared Copper Scar `pyproject.toml` just because the extension expects a JITX project.

## Intended optimization loop and state model

The deliverable has two independent success conditions: a real eligible PCB assembly, and evidence that retained feedback improves subsequent design attempts. The existing deterministic rectangle simulation satisfies neither condition. The physical objective is:

`assembly bounding-box volume in mm³ + 50 × via count + 5000 × copper-layer count`.

Compute volume from the complete assembly's measured envelope, not board area × an assumed thickness, and not the sum of solid volumes. Tall connectors and parts on both sides affect the score. Fewer layers do not justify violating power integrity, routing, assembly or fabrication constraints.

Proposed iteration:

1. Load a fixed reference plus current incumbent JITX source, approved constraints and scoped evidence. Record an exact source/package/runtime snapshot.
2. The selected coding assistant proposes one bounded edit with an expected effect: placement grouping, outline geometry, legal layer/via structure, route sketch, or a justified rule. Preserve immutable circuit and connector requirements.
3. Apply the edit to a private challenger project. Run Python construction/translation first, then runtime submission and capture. A source hash changes only when the actual editable design changes.
4. Confirm concrete realized copper and collect JITX diagnostics. Export one checkpoint into a private export directory. Establish experimentally whether export resubmission preserves state. Use the same checkpoint for KiCad and STEP; do not pair artifacts from different revisions.
5. At a selected checkpoint, materialize a complete standalone candidate project with original supporting files and reviewed identity mappings. Use copies, not symlinks; make it portable enough that the validator cannot silently resolve files from the author's home directory.
6. At comparison/release checkpoints, invoke independent native KiCad validation outside the candidate directory, using the core checker if its contract is the agreed comparison standard. Preserve raw logs, JSON, snapshot, fingerprints and assembly output even when the candidate fails. Do not require this export/check on every internal JITX iteration: use JITX-native checks inside the loop when their coverage is understood.
7. Feed failures back to the assistant. A diagnostic may motivate a rule proposal, but does not automatically prove the proposed rule correct. Record rationale, affected objects, reference evidence and a regression expectation. Re-test before retaining the rule.
8. Compare only accepted candidates for the valid incumbent. Keep invalid experiments for diagnosis, never as the winning board. Write an immutable incumbent pointer with exact candidate/record hashes after gates pass; export/promotion remains core-owned.

Use one design-owning writer/runtime session per challenger. Multi-process parallel evaluation is a later optimization; it is not necessary for the first proof and must not contend for one JITX design name or one global environment. Separate source state, transient runtime geometry and exported artifact state explicitly. Runtime `capture()` does not itself prove source write-back survives restart. A checkpoint recovery test must stop/restart the runtime and reproduce the same intended geometry.

A minimal runner can be a short approach-specific orchestration script invoking existing JITX and core facilities. Prefer the normal coding assistant as controller for the first bounded experiment. Introduce a standalone unattended runner only if demonstration/reproducibility requirements need it. If a shipped supported JITX optimization controller is discovered later, evaluate its callable contract and replace this glue; do not insist on maintaining custom orchestration for its own sake.

## Common validation record: consume it without changing semantics

The current core implementation starts with `schema_version: 1`, `kind: native-kicad-candidate`, `created_at`, `run_dir`, `checks`, `failures`, nullable `metrics`/`score`, and `gates_ok: false`, `promoted: false`. Successfully inventoried inputs add `design_sha256` and `reference_sha256`. Early failures may lack fields; consumers must handle that rather than fabricate a fingerprint. `assembly`, `promoted_to` and detailed check payloads appear as the run progresses.

Important current behavior from `real.py`: clean native DRC plus complete model inventory permit STEP export and metric calculation, **before** the final engineering-review and overall-failure checks. Consequently a numeric score can coexist with `gates_ok: false`. The candidate selector must require a compatible schema, expected fingerprints, complete checks and `gates_ok is True`; a score alone is never acceptance. `promoted` only means the optional core promotion operation actually copied the artifact; it is not the same as a successful evaluation.

The engineering-review input binds `reviewer` and four literal true attestations (`manufacturing`, `assembly`, `electrical`, `connector_compatibility`) to `design_sha256`. An agent must not generate these attestations as a substitute for review. If a project adopts a separate provisional ranking of invalid candidates for search guidance, label it diagnostic, keep it out of the official incumbent and preserve all failure counts. That ranking is proposed work, not the existing core score contract.

## Five-root import remediation options

Resolve the importer and validator coverage problem before claiming circuit equivalence. Evaluate these options in order of lowest semantic change:

- **Supported vendor import path:** look for an existing documented method/version that imports the original multi-root project. Verify it on the pinned source. A newer version, hidden command or vendor claim is insufficient without output parity. No new vendor contact or installation is part of this documentation request.
- **Reviewed internal single-root representation:** create a separate wrapper/hierarchy or flattening of the five roots for ingestion. Preserve every symbol instance, pin, global/local label scope, power-net connection, no-connect marker, annotation and multi-unit relationship. A wrapper can alter local-label scope; flattening can create accidental shorts. Compare the resulting full electrical graph against the original multi-root design and verify it natively. Keep a reversible instance mapping and original files untouched.
- **Compose separately imported circuit blocks:** possible only if importer output exposes faithful reusable Python components/circuits and the cross-sheet graph can be independently reconstructed and verified. Importing five roots separately and concatenating nets by string is not an acceptable shortcut. Block-level parsing success does not establish whole-project identity.
- **Native-board-preserving route:** continue KiCad generation with an external router if conversion cannot be qualified. This fallback retains the real-board objective and common checker; it does not return to the simulator.

Do not delete roots, remove components or relax original rule hashes to get past an import error. Do not regenerate all parts from LLM recollection as a substitute for an auditable conversion. Any circuit redesign permitted by the challenge still requires an explicit, separately reviewed functional equivalence case; initial compatibility work should preserve components and pin assignments.

## JLCPCB and electrical/mechanical constraint policy

JLCPCB manufacturability is fixed by the challenge; the exact process profile is not fixed by the current project. Select and record layer stackup, board thickness, copper weight, minimum feature/clearance and drill limits, tolerances, material and assembly process. Use a dated official capability source and an engineering-reviewed profile, not a generic `jlcpcb=True` setting.

JITX documentation exposes JLCPCB library examples for particular 4- and 6-layer stackups. They are not proof that the installed standard library contains the required separate package, nor a reason to increase this two-layer baseline by default. A 4-layer example also incurs another 10,000 score units versus two layers. Check the chosen profile's availability and effective constraints when implementation begins. Do not blindly substitute `SampleDesign` fabrication rules; the sample library explicitly describes itself as experimental.

Represent generation constraints in JITX and enforce the authoritative profile in the native gate. Build a reviewed mapping for each translated rule. Preserve stronger original constraints; explicitly document any stricter selected manufacturing requirements. Rules missing from the source require engineering input, especially power/current paths, regulator placement/return loops, USB differential routing/return paths, clocks, decoupling and connector positioning. Clearance-clean geometry does not establish signal or power integrity. HFSS remains excluded; conventional engineering checks and supported native constraints must carry the relevant assurance.

The original support-file hash policy must evolve only through core review if adding a fabrication profile or completing models changes those files. One sensible approach is to retain immutable original hashes and separately fingerprint the approved augmentation, rather than silently treating a modified file as original. That is a design proposal, not implemented behavior. Connector mating geometry, access for cables and assembly tooling, populated/unpopulated parts, component heights, and mounting-feature treatment need explicit acceptance criteria. Original missing models (J4 and BH1–BH4 in core evidence) must be resolved or dispositioned through a reviewed population policy, not hidden with placeholder zero-height models.

## Milestones and verification matrix

| Milestone | Deliverable | Verification / exit criterion | Stop condition |
|---|---|---|---|
| M0: review this direction | Agreed ownership, objective, allowed edits, profile and effort cap | User reviews JITX and Copperhead documents together | Unknown scope or conflicting ownership; no implementation yet |
| M1: post-login runtime checkpoint | Small real design's source, captured copper, KiCad and assembly STEP | Build/capture succeeds; export state reproducible across restart; native artifact parser works | Auth/entitlement failure, undocumented manual export dependence or state mismatch |
| M2: full circuit fidelity | PCBGolf internal JITX representation and original-to-generated mapping | All five roots covered; full electrical graph, footprint/pad/model/rule invariants independently checked | Missing circuit, ambiguous label scope, unsupported importer transformation |
| M3: physical baseline | Complete original board routed with reviewed outline/placement | All connections routed as copper; native DRC/ERC/parity; JLC and assembly review; complete STEP | Incomplete routing, critical electrical uncertainty, native checker crash/coverage gaps |
| M4: bounded improvement proof | Challenger series, feedback rules, accepted incumbent, replay | Improvement over a valid baseline; fresh-start replay demonstrates retained feedback changes outcomes | Invalid board offered as winner, repeated failure without useful diagnosis, budget exhausted |
| M5: integration review | Approach-specific code/docs/tests in isolated branch | Core contract unchanged or explicitly reviewed; existing tests and focused integration checks pass | Cross-provider file interference, manifest drift, unreviewed source/license redistribution |

Tests should target real failure modes: importer exit-zero/JSON-false; missing partial exports; changed support files; lost or shorted cross-sheet nets; changed pad drill/shape or connector model transform; unresolved models; a score with false gates; reused stale checkpoint; invalid native JSON/process crash; runtime restart state loss; rejected source change and incumbent recovery. Add positive acceptance fixtures only when an independently valid real board exists. Tests that merely mirror wrapper implementation do not add proof.

The setup task reported 30 tests passing with one optional Weave import test skipped. This document did not rerun them. Its native baseline had 180 DRC violations and 499 unconnected items. First-root ERC success and 240 apparent parity items are incomplete-coverage evidence, not a definitive whole-board electrical result. Resolve complete multi-root loading centrally before either provider can pass acceptance. Native tool crashes are failed checks, never empty-success reports.

## Artifacts, scars and failure recovery

Proposed per-attempt manifest fields, stored beside rather than injected into core records: attempt ID, approach/version, parent incumbent hash, JITX source hash, original reference hash, profile hash, assistant/provider identity, prompt/proposal, editable-file diff, runtime/package versions, commands and durations, stdout/stderr paths, export paths/hashes, native record path/hash, decision and reason. Use stable object identifiers with reference/pad/net mappings so findings survive coordinate changes.

A scar record should include the original failed candidate hash, concrete native finding, hypothesized cause, affected scope, proposed durable constraint, review status, counterexample/regression check and evidence from the rerun. Distinguish a keepout caused by a connector's physical clearance from a temporary collision due to one placement. Avoid accumulating blanket keepouts that merely encode accidental failures and shrink the feasible design space. Retire or amend contradicted rules with history rather than silently overwriting evidence.

Keep code-defined design intent in versioned source; keep transient solver output in immutable artifact directories; keep credentials out of both. On failure, preserve challenger artifacts and return to the last accepted incumbent without modifying the reference. No candidate should resolve dependencies or update packages mid-comparison. Pin packages/runtime for the campaign and make any upgrade a separately recorded change with a rerun of fidelity gates.

## Fallback evidence and decisions for review

The separate router investigation has a working real KiCad→DSN→Freerouting→SES→KiCad path. Its saved summary reports 2,073 segments and 400 vias on the challenge, with 367 incomplete connections and 70 router-reported clearance violations. It preserved pin/net identity; four footprints showed coordinate differences with maximum pad delta 46 nm. Native DRC in that task aborted at application registration, so this is **not** a validated alternative board. Its recommendation is nevertheless a practical fallback experiment because it avoids JITX's five-root import conversion. [Router proposal](/Users/philippe/.codex/worktrees/408e/copper-scar/investigation/autorouter-proposal.md), [saved summary](/Users/philippe/.codex/worktrees/408e/copper-scar/investigation/evidence/summary.json).

Decisions to review, not new permission questions in this document:

1. **JITX role:** recommended full design/constraint/routing path with a compatibility milestone, rather than limiting it to a router or forcing it inside Copperhead's agent controller.
2. **Campaign prerequisite:** recommended no valid-board optimization claim until full-project electrical validation and complete assembly scoring are operational for both approaches.
3. **Import investment:** choose an explicit time cap for faithful multi-root conversion; stop and retain the native KiCad fallback if it cannot be verified within that cap.
4. **Design freedom:** initially preserve all components/pins/interfaces. Approve any functional redesign separately with a reviewable equivalence case.
5. **Manufacturing and assembly profile:** select the actual JLC process, stackup and population/mechanical assumptions before hardcoding routing defaults.
6. **Assistant/controller:** use an already approved coding-assistant subscription where practical, with no automatic fallback to metered APIs. A browser-chat subscription alone is not evidence of a callable automation API. JITX requires file editing plus CLI invocation, so its architecture does not force a new inference vendor.
7. **Reuse/license scope:** resolve the free-tier design-license condition and skills redistribution restrictions. No former-employer entitlement is assumed. Prefer invoking supported installed APIs over copying vendor implementation.
8. **Integration ownership:** retain the shared validator/scorer under the core owner and independent approach code under each provider owner. Merge reviewed results later; main is the integration destination, not a shared experimental working directory.

The practical recommendation remains a staged decision: qualify JITX's faithful board/checkpoint path first, then use its shipped design and runtime primitives as deeply as they support the task. If those primitives suffice, the missing glue is small. If they do not, an opaque rewrite or a simulated demo would not satisfy the project.


## Isolation update and inner-loop benchmark (2026-09-12)

JITX and Copperhead now have different registered Git worktrees. This is workspace isolation, not security containment: Git objects and refs are still shared. Main was clean when inspected and remains untouched by the isolation changes. Existing JITX experiment files, venv, runtime and docs were preserved in place; no files were moved, deleted or reinstalled. No commits, merges, resets or pushes were performed.

The repository copy of this plan is `/Users/philippe/dev/copper-scar-jitx-worktree/docs/jitx-plan-and-design.md`. The existing external canonical and review copy remain synchronized. The short write-boundary record is `/Users/philippe/dev/copper-scar-jitx-worktree/docs/jitx-ownership.md`.

JITX owns its internal proposal/edit/generate/check/feedback/write-back loop. Translating suitable KiCad constraints into JITX may reduce the cost of repeated exports and checks, but equivalent coverage and speed have not been demonstrated. The design explicitly permits JITX-native checks on internal iterations, with independent KiCad checks at selected checkpoints and final comparison. It does not make Copperhead the controller or require the shared checker on every iteration.

Before relying on translated checks, benchmark the following in a bounded experiment:

1. Fix the board revision, tool/package/runtime versions and reviewed manufacturing profile. Establish a coverage matrix linking each native rule/check to its JITX equivalent or an explicit unsupported category. Include net continuity, shorts, clearance, width, drills/annular rings, mask/courtyard, board edge, differential constraints, schematic parity and assembly/model checks. Do not presume JITX exposes every category as a callable headless API.
2. Evaluate both valid fixtures and deliberately invalid copies with independently known defects. Compare detected violations, false negatives/positives, severities, scopes and object identities. A clean JITX result is insufficient if the native checker detects a disqualifying defect. Five-root connectivity and assembled STEP coverage remain separate until equivalent checks are actually demonstrated.
3. Measure cold and warm construction, solve, native JITX checking, export, native KiCad checking and total iteration time separately. Use repeated bounded runs on the same machine, report median and tail latency plus sample count, and include failed/time-out runs. Compare at matched coverage; fewer checks is not an equivalent speedup.
4. Classify each check as equivalent, intentionally checkpoint-only, unsupported, or unresolved. Use the proven subset for fast internal feedback. Always run checkpoint-only checks before promoting a valid incumbent; do not inherit a stale result after a relevant change.
5. Keep native KiCad checkpoint cadence explicit: after import/conversion, at designated candidate comparisons, after changes to unproven rule categories, and before final acceptance. If disagreement appears, preserve both reports, stop promotion and investigate the mapping. Do not silence native findings to preserve the speed claim.

Until this experiment passes, any JITX inner-loop success is provisional. Benchmark execution and board optimization are proposed next work, not part of this isolation/documentation task.
