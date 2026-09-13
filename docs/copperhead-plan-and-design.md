# Copper Scar: Copperhead/native track and comparison architecture

Status: implementation update, 12 September 2026. The user subsequently authorized local Stage 1 implementation and real native iterations. Account enrollment, paid calls, fabrication, pushing and merging remain outside scope. Historical setup sections below describe their original checkpoint; Section 9 and the linked loop design describe the subsequent implementation. Its primary goal is a real, electrically and mechanically valid PCBGolf board, followed by measurable improvement of that board.

## 1. Outcome and acceptance boundary

Copper Scar should propose real PCB changes, execute real design tools, independently evaluate the resulting KiCad project, remember measured failures, and retain better accepted designs. The first milestone is feasibility: a complete board that satisfies the original interfaces, electrical requirements, manufacturing process, assembly and connector constraints. Optimization follows feasibility.

The [official PCBGolf project](https://github.com/commaai/PCBGolf) requires the same functionality and usable, mechanically and electrically compatible mating connectors, a manufacturable and assemblable PCB, and KiCad plus assembled STEP deliverables. Its objective is:

`assembled bounding-box volume in mm³ + 50 × vias + 5000 × copper layers`

Board area multiplied by substrate thickness is not assembled volume. An unrouted smaller board is not an improvement over an accepted board. No existing artifact in this investigation has passed the full acceptance boundary. Physical operation and manufacturing qualification remain distinct from CAD checks; neither an agent nor an ERC/DRC pass can establish them alone.

The intended result is the full board. A partial routed artifact may demonstrate progress or provide failure evidence, but must remain labeled partial. A hackathon time limit does not redefine it as a valid PCB.

## 2. Verified starting point

The reference is PCBGolf commit `7210bdb5049c5b7fdf4900a34928e2736767292a`. The original checkout at `/Users/philippe/dev/PCBGolf` was preserved. The working native setup uses separate source and candidate copies under `/Users/philippe/dev/copper-scar-demo/.local/`.

The input has 245 footprints, 1,078 physical pads, 1,053 pad-net assignments, 302 distinct net strings and two copper layers. It has no tracks, vias, zones or top-level board-outline graphics. It is an unrouted starting design, not an already valid board awaiting compression. Netless mechanical pads matter even though they are absent from the assignment count.

Five independent top-level schematics are declared in the project: Power, STM32H7, USB+SD, CAN-FD and Channels. Their actual root UUIDs differ from the project entries. Loading a single schematic through the tested CLI does not establish whole-project connectivity. This is the first correctness problem to solve, before allowing an optimizer to use ERC as an oracle.

The design includes 12 V/5 V/3.3 V supplies, switched and monitored channel power, four CAN interfaces, a USB hub and USB connections, STM32H725, microSD, crystals, LEDs and a button. Routing needs electrical constraints for these functions, not just generic fabrication minima. OBD-C connector pin assignments must be preserved; their USB-C-shaped shells do not establish standard USB-C wiring.

There are model entries on 240 footprints referencing 26 existing STEP paths. J4 and BH1–BH4 lack model assignments. Population, mounting geometry, transforms and access envelopes require review. The absence of a model cannot silently mean the part is unpopulated.

### Native evidence obtained

KiCad 10.0.6 executed successfully in the setup task. The unchanged starting board produced 180 DRC violations, 499 unconnected items and 240 schematic-parity entries. The latter are affected by incomplete schematic context and are not 240 independently established circuit defects. Separate sheet ERC counts were 0, 150, 124, 198 and 266; those cannot be summed into a trustworthy whole-project defect count. The root's zero is equally insufficient evidence of a clean project.

The latest native record is [failure-record.json](/Users/philippe/dev/copper-scar-demo/.local/checks/candidate-4xpevryp/failure-record.json). It reports failed gates, no score and no promotion. Copperhead independently reported root ERC zero and DRC total 679, also failing. It did not request the native parity check.

The routing investigation independently demonstrated KiCad→DSN→Freerouting→SES→KiCad on the actual board. Freerouting 2.4.1 ran for approximately 71 seconds and imported 2,073 segments and 400 vias. It still reported 367 incomplete connections and 70 clearance violations. All 1,053 logical pin assignments and 302 net names survived the export; four footprint coordinates changed by 18–46 nm during the round trip. Its artificial test outline was not an approved mechanical design. Native DRC on that routed probe was not completed because that task's application invocation aborted; this does not invalidate the separate successful native baseline execution.

See the [routing investigation](/Users/philippe/.codex/worktrees/408e/copper-scar/investigation/autorouter-proposal.md) and its [evidence summary](/Users/philippe/.codex/worktrees/408e/copper-scar/investigation/evidence/summary.json). The probe is evidence that a real routing bridge works, not that the board is acceptable.

### Existing simulator evidence

The original simulator uses deterministic rectangle geometry and a hardcoded policy. It has no LLM or KiCad routing. Its measured second pass improved the simulated score, while the third repeated that result. Because the policy also changes its shrink behavior when stored scars exist, this does not isolate a causal benefit from memory. The authored offline evaluation and simulated demo remain useful software fixtures, but cannot support claims of PCB validity, autonomous routing or real assembly improvement.

## 3. Implemented core and its limits

Native setup commit `9b72b82` on local branch `codex/demo-takeover` adds [real.py](/Users/philippe/dev/copper-scar-demo/copper_scar/real.py), a `real-check` CLI entry, pinned tooling, setup scripts and focused tests. The local suite passed 30 tests with one optional Weave import skip. Contract tests include mocks; they do not constitute board qualification. A real OpenCascade box measurement separately verified the installed measurement library.

The command accepts a candidate project, reference project, output directory and KiCad executable, with optional Copperhead check, qualification file and explicit promotion destination:

```text
copper-scar real-check --project <candidate>/pcbgolf.kicad_pro \
  --reference <reference>/pcbgolf.kicad_pro --out-dir <runs> \
  --kicad <kicad-cli> [--copperhead <executable>] \
  [--qualification <JSON>] [--promote-to <new-directory>]
```

Current behavior:

- Copies the candidate into a unique run directory, rejects unsafe nesting and source symlinks, records CAD/support-file hashes, and checks those hashes again after validation. The snapshot is hash-verified; it is not enforced immutable by filesystem permissions.
- Requires unchanged reference support files and matching board component/pad/net assignments. Only the main board is exempt from exact support-file equality. This is board-to-reference parity, not proven schematic equivalence.
- Runs KiCad version checks, sheet ERC and board DRC with schematic parity and zone refill. Requires usable JSON, matching report metadata and allowed process statuses; violations, warnings, missing reports and inconclusive coverage fail closed.
- Requires an ERC report covering all expected actual schematic root UUIDs. Five unrelated single-root reports cannot collectively satisfy this gate. The current input fails it.
- Optionally runs Copperhead checks as supplementary evidence. Copperhead cannot override a failed native check.
- Requires model paths for every footprint. On eligible native geometry, exports STEP and uses OpenCascade to measure its bounding box. File existence and successful export do not yet prove every expected model instance and transform is present in the assembly.
- Requires separate qualification attestations tied to the exact CAD fingerprint, a reviewer and literal acceptance flags for manufacturing, assembly, electrical and connector compatibility. These flags are attestations, not physical test evidence; none has been supplied for the input.
- Records failures, checks, hashes, inventory, nullable metrics/score and promotion status. Explicit promotion only copies an accepted snapshot into a new destination. It does not compare against a best candidate or overwrite an existing design.

A provisional metric may be computed before every other gate passes; only `gates_ok` establishes current checker acceptance. The eventual user-facing accepted score must be clearly distinguished from any provisional metric.

At the initial setup checkpoint there was no real candidate-generation loop or router adapter. The subsequent Stage 1 runner now provides native routing attempts, best-feasibility selection and scoped failure evidence; controlled scar-benefit experiments and Stage 2 optimization remain unimplemented. `failure-record.json` is persisted evidence; its name does not mean its contents already encode an actionable repair policy.

Exact support-file equality intentionally prevents silent rule and schematic changes, but also blocks legitimate reviewed model additions, constraint changes and alternative tool exports. A versioned reference and explicit equivalence policy must address that limitation. A provider-specific bypass is unacceptable.

## 4. Recommended architecture

Copperhead/native and JITX run **separate internal loops and checkers in different Git worktrees**. They share the intended board requirements and comparison criteria, not a mandatory implementation of the inner loop. The model provider and routing engine remain independent choices. This supersedes the earlier proposal to require every producer to pass through one shared checker on every iteration.

```text
approved reference and electrical/mechanical/process constraints
             |                                  |
Copperhead/native worktree                JITX worktree
local edits/routing/checks                native design/routing/checks
local candidates and memory              local candidates and memory
             |                                  |
       selected checkpoint / final exported KiCad artifacts
                              |
         independent KiCad checks and assembly-score comparison
```

### Track-owned responsibilities and checkpoint contract

Copperhead owns its existing native checker, execution budgets, candidate snapshots, failure records and local selection logic within its worktree. JITX owns its internal representation, constraint translation, checks and iteration policy within its separately registered worktree. JITX may translate approved constraints into native checks to avoid exporting on every iteration. Faster execution and equivalent coverage are hypotheses to benchmark, not established benefits. Neither track may silently weaken the approved requirements or turn an unknown gate into a pass.

At selected checkpoints and for the final comparison, each track supplies a complete KiCad project, reference/constraint hashes, provenance, gate coverage and assembly artifacts. Independent KiCad checks can reveal divergence between the tracks' internal judgments. The checkpoint schedule is a later implementation decision; KiCad export is not mandated for every JITX iteration. Final accepted-score claims still require the full evidence boundary in this document.

Within the Copperhead track, a proposed request contains a run ID, input path and hashes, constraint revision, unique output directory, permitted edit scope, tool/provider identity, budget and prior failures. A response contains candidate path, changed objects, versions, effective settings, logs, elapsed time and termination reason. Tool-reported completion is not acceptance. Copperhead's own checker evaluates a separate snapshot.

Checkpoint projects preserve all five schematics, coherent project context, libraries, model dependencies and rules. DSN/SES and tool-native files remain provenance. A future common checker or schema change must have an explicitly agreed owner and reviewed handoff before either track edits it; there is no concurrently writable shared implementation or generated-output directory.

### Proposed state and failure interfaces

Persist one structured record per attempt. Extend the current record through a versioned schema rather than replacing it with provider-specific summaries. Record input and output hashes, source commit, approved constraint revision, engine/provider versions, invocation/effective configuration, raw report paths, gate states, provisional geometry, accepted score if any and review evidence references.

Use gate states `pass`, `fail` and `unknown`; unknown never promotes. Suggested native failures include missing connectivity endpoints, clearance/short/outline violations, lost pin identity, changed locked geometry, rule loss, incomplete schematic coverage, missing assembly instances and tool timeout. Each failure should retain its native code, object IDs, nets, coordinates where available, source report and design hash.

A proposed repair such as moving a switcher block is a hypothesis separate from the measured violation. Scope each remembered fact to the relevant objects and constraint revision. Invalidate stale geometry-dependent memories after affected objects move. Never learn “ignore this error” merely because repeated runs fail it.

## 5. Copperhead flow

Copperhead 0.10.0 is installed and pinned locally. Its agent tools can edit files and call external commands. Its `layout-draft` guidance permits remaining ratsnest: it is not a global autorouter and cannot alone deliver a routed board. Its native `check`/`verify` commands are useful conveniences, but their current one-schematic configuration, missing-input skip behavior and weaker report handling cannot be the acceptance authority.

The proposed Copperhead adapter receives the core request, launches an explicitly selected provider in its candidate workspace, asks for a bounded change, invokes a routing backend where appropriate and returns the artifact contract. The Copperhead track’s native checker then checks a separate snapshot. Start with small allowed edits and one attempt, not an unrestricted optimizer.

The local Codex SDK is pinned at 0.144.6 and reports an existing ChatGPT login. No end-to-end provider call was executed. The global Codex binary is broken; [the launcher](/Users/philippe/dev/copper-scar-demo/scripts/copperhead.sh) points to local tooling. Claude authentication was absent, and the executable named `agent` resolved to Grok rather than verified Cursor. Provider configuration must resolve the actual intended executable. Generic compatible API support is possible in the source, but no xAI/API route or subscription entitlement has been established here.

No default model, paid API dependency or new subscription is required by the architecture. Existing coding-agent execution can call native tools directly while the optional Copperhead adapter is brought up. Provider convenience must not become a blocker for board correctness.

## 6. Routing engine decision

Use native KiCad as the authoritative design representation. Freerouting is the first bulk-routing candidate because the actual round trip has been exercised. Native KiCad interactive routing remains necessary for critical supplies, crystals, USB pairs and final cleanup. The installed CLI does not expose the exercised DSN/SES bridge; it uses KiCad's bundled `pcbnew` Python API.

Before trusting that bridge, characterize preservation of fixed copper, stronger netclasses, keepouts, plated slots, filled zones, thermal connections and real pair polarity. DSN carries a subset of native rules. Keeping `.kicad_pro` unchanged does not make an external router enforce every rule. Resolve coordinate quantization explicitly through restoration and validation or narrowly approved tolerances; do not weaken all geometry checks.

| Engine | Proposed role | Admission condition |
|---|---|---|
| Freerouting 2.4.1 | First local ordinary-net router | Preserved critical copper and supported constraints; independent native checks after every import |
| KiCad native router | Critical routes and cleanup | Reviewed electrical geometry and preserved project context |
| KiCadRoutingTools | One bounded challenger if the first route fails | Disable net/pad swaps; audit clearance caps and native round-trip fidelity |
| JITX | Alternative producer, discussed below | Resolve complete import, entitlement and export equivalence first |
| tscircuit autorouter | Later experiment | Demonstrated whole-project return path and enforcement of required constraints |

Do not use router-reported volume or normalized scores for PCBGolf scoring. Freerouting's measured counters were not interchangeable with KiCad geometry or unconnected counts. Its fanout and optimizer settings also differed from initial short-flag assumptions; record effective settings and enforce an outer timeout.

A four-layer reference is a reasonable proposal for ground reference and routing feasibility, subject to an approved fabrication stackup. It has not been adopted. Two added layers cost 10,000 score units, equivalent to 200 vias before volume differences. Layer selection is an electrical/process decision before it becomes an optimization variable.

## 7. Interchangeable JITX flow, without HFSS

JITX 4.4.0 is installed in the separate investigation workspace. It exposes design/build/export and routing-related runtime capabilities. Existing probes reject the actual directory because it contains five top-level schematic roots; the importer returns `success:false` even with process exit zero. Runtime authentication and design-license eligibility were unresolved in those probes. Deleting four sheets or treating public repository visibility as licensing permission does not solve these gates.

The JITX producer should consume the same approved reference and constraints, generate or import the complete design, perform its own placement/routing work, and export a full KiCad candidate plus assembly/provenance artifacts. It must prove pin-connectivity equivalence, all required parts and mechanical features, rule preservation or approved translation, and model transforms. JITX may validate intermediate candidates using its own native checks. At selected checkpoints and final export, independent KiCad validation and common score definitions support comparison; the tracks need not share checker code or export on each iteration.

This may require a reviewed translation layer or equivalent unified schematic representation. Such a representation needs independent proof of sheet-local versus global labels, power nets, no-connects and reference identities. Until that proof exists, JITX is a conditional path rather than the baseline dependency.

HFSS is not part of this architecture or an acceptance prerequisite. The team can establish needed stackup, return-path and interface constraints using appropriate design guidance and engineering review. Additional simulation, if later justified by an unresolved electrical question, is a separate decision. The dedicated JITX plan owns its detailed runtime integration; this document does not modify it.

## 8. Qualification policy

The present checker is deliberately stricter than a production waiver workflow. Proposed refinements must preserve traceability:

1. Establish complete schematic electrical truth and compare pin-connectivity partitions, not only net strings or the existing board's assignments.
2. Preserve all components, physical pads, connector pinouts, locked mechanical features, approved model transforms and critical routes. Changes require an explicit reviewed scope.
3. Run whole-project ERC and filled-board DRC with the selected fabrication deck and electrical rules. Do not aggregate incomplete reports into a pass. Reviewed waivers need native code/object scope, reason, reviewer and constraint revision; agents cannot self-waive failures.
4. Review power currents, switcher hot loops/feedback, thermal paths, USB geometry/return paths, SD and clock constraints, CAN topology and decoupling. Generic trace-width minima do not prove these requirements.
5. Validate assembly population, every expected model instance, physical collisions, connector access and bounding-box units. STEP exporter success alone is insufficient.
6. Separate CAD acceptance and engineering review from fabricated-board testing. Record physical power-up, interfaces, thermal/load and mating checks when hardware exists. Do not describe attestation flags as those tests.

JLCPCB manufacturing constraints must correspond to the chosen layer count, copper, stackup and process. Third-party rule collections such as [kicad-druid](https://github.com/Cimos/kicad-druid) can be reviewed inputs, not official certification. The current project's minima are not a complete manufacturing or electrical rule set. Do not silently apply a four-layer deck to a two-layer candidate.

## 9. Two-stage durable loop

Stage 1 is the hackathon's **feasibility repair loop**: it systematically evaluates and repairs the full real board toward valid placement and routing. Stage 2 then shrinks/optimizes accepted boards under the official assembled-volume/via/layer objective. Stage 1 is implemented now in `copper_scar/tools/copperhead/stage1.py`; Stage 2 is gated and not yet implemented. This supersedes the earlier sequencing that treated finding a valid starting board as a manual prerequisite to building the loop.

The runner freezes input/support constraints, performs fresh full native evaluation, selects a justified bounded action, executes and reevaluates, retains artifacts/commands/hashes and scoped feedback, and records an incumbent separately from exploration. Initial automatic action support is continued routing; unsupported targeted repairs require a recorded controller proposal. Each step persists structured cost and evidence, including regressions and timeout/failure. Budgets stop an invocation, not the overall board objective.

Feasibility cost `native-defects-v1` uses lexicographic diagnostic categories: invariant failure, native shorts, other errors, clearance findings, measured maximum clearance shortfall in millimetres, deduplicated missing endpoint pairs, their measured distance sum in millimetres, and warnings. Counts, units, measurement coverage and limitations are explicit; no arbitrary weighted sum or official-score claim is used. Unknown acceptance evidence cannot be converted into a pass by reducing this cost.

See [the implemented loop design](/Users/philippe/dev/copper-scar-demo/docs/native-feasibility-loop.md) for the operational ordering, actual candidate comparisons, feedback scope, exploration/stagnation policy, command contract, Weave integration and exact invocation. Baseline-013 began with 208 native missing connections. Seven durable repair attempts reached 128 with zero physical errors and two warnings; the live dashboard exposes subsequent results. This is partial, not valid. Engineering, manufacturing and assembly proof remain outstanding, and Stage 2 stays disabled. Existing native contracts and original rule values are preserved within the campaign; no acceptance attestations are fabricated.

## 10. Ownership and eventual main integration

Copperhead retains the registered worktree `/Users/philippe/dev/copper-scar-demo`, branch `codex/demo-takeover`, HEAD `9b72b82f91b37d17314dcd281ccd90d31d6bf432`. Its existing local native implementation and all earlier demo edits are preserved. The primary checkout `/Users/philippe/dev/copper-scar` is on `main`; this track must not edit it. JITX's task owns creation/verification of its different registered worktree. Its path is not asserted here until that task reports it; Copperhead must not edit any JITX workspace, environment or document.

Copperhead-owned repository paths are its local `copper_scar/real.py`, native CLI/checker sections, `tests/test_real.py`, `scripts/copperhead.sh`, `scripts/prepare-pcbgolf.sh`, native documentation and any future `copper_scar/tools/copperhead/` adapter. Shared score/schema/CLI/dependency changes need explicit coordination before editing; current scope includes the separately authorized native feasibility implementation. No global or other-worktree dependency changes are allowed.

All Copperhead-generated state stays under its own `.local/`: existing `pcbgolf-candidate/` and `checks/` are retained; future attempts use unique `.local/copperhead/candidates/<run-id>/` and `.local/copperhead/runs/<run-id>/` directories. `.local/pcbgolf-source/` remains a reference, not an output. The track uses its own `.venv/` and `node_modules/`; these directory roots were verified to be local, not symlinks to another worktree. Existing shared KiCad binaries may be invoked but must not be updated. No global package installation or shared runtime update is permitted.

Git worktrees isolate working-tree changes; they are not security sandboxes. They share the repository's Git administration and run under the same user. Distinct output roots, dependency environments, write ownership and preservation hashes prevent ordinary workflow overlap by convention and detect mistakes; they do not enforce filesystem access restrictions. Do not claim stronger isolation. Actual process/filesystem enforcement would be a separate implementation decision.

The initial documentation-only authorization covered this plan, [the ownership record](/Users/philippe/dev/copper-scar-demo/docs/copperhead-worktree-ownership.md), and the explicitly requested plan copy at `/Users/philippe/Documents/Codex/2026-09-12/realtime-voice-chat/outputs/copperhead-plan-and-design.md`. That review copy has one writer: Copperhead. No common mutable candidate or run directory is used. The subsequent implementation authorization permits track-owned scripts, modules and candidate/run outputs; it does not permit reset, clean, delete, merge, push or blanket-staging.

Future main integration requires separately reviewed track changes, explicit ownership of any common interfaces/checker files and one integration owner. Validate the eventual integration tree rather than citing another worktree's tests. Neither track should directly modify main or cherry-pick changes into the other's active workspace. The ownership record captures the initial preservation checkpoint and subsequent implementation authorization.

## 11. Milestones and decisive checks

| Milestone | Deliverable and exit evidence | Stop condition |
|---|---|---|
| M0: complete electrical reference | Whole-project ERC/netlist coverage and independently compared connectivity partitions; versioned constraints | Unresolved five-root scope or lost pin identity |
| M1: conservative design basis | Approved stackup, outline/access envelopes, population/model policy and critical electrical constraints | No supported process or unresolved essential interface requirements |
| M2: trustworthy native bridge | Fixtures prove required fixed-copper, rule, geometry and connectivity preservation | Unsupported rule silently relaxed or geometry lost |
| M3: first real route | Bounded candidate with raw provenance and independent native results | Time budget exhausted, missing reports or required violations remain |
| M4: accepted CAD baseline | Complete routing, required checks, engineering review, complete assembly measurement and submission structure | Missing qualification/model evidence; retain partial status |
| M5: actual improvement | At least one independently accepted candidate beats baseline under unchanged objective/constraints | Only invalid candidates improve score or budget expires |
| M6: comparable separate tracks | Selected/final exports satisfy the comparison contract; benchmark internal-check coverage and iteration time separately | Import/export failure or uncovered constraint; retain native path |
| M7: physical qualification | Fabricated assembly and recorded functional, load/thermal and connector tests | Hardware does not satisfy original functions; revise design |

Benchmark JITX internal checks against independent KiCad checkpoints using the same frozen candidate set, including known violations and clean fixtures; report disagreement by constraint and measure total iteration time including export overhead. Do not assume equivalence from aggregate pass counts. Tests should target failure modes: incomplete five-root reports, malformed JSON despite zero exit, changed support rules, lost netless pads, changed pin partition, missing model instances, locked-copper damage, timeout handling and promotion races. Keep existing unit fixtures, but label native integration runs and physical evidence separately. A meaningful first validation is a real candidate passing the actual checker; additional mock coverage cannot substitute for it.

## 12. Open decisions, risks and fallback

Decide the electrical reference representation first. Then choose the supported manufacturing stackup, permissible mechanical movement, population/model policy and reviewed waiver process. Select a provider only when bringing up its adapter. Decide JITX eligibility and complete import/export equivalence before making it part of the delivery path. No decision here is implied approval to enroll or spend.

The principal risks are incomplete schematic truth, insufficient electrical constraints, routing a dense full design within limited time, external-router rule loss, incomplete assembly geometry and confusing local attestations with hardware proof. Their mitigations are independent checks, frozen references, narrow edit scopes, bounded experiments and explicit evidence states.

If Copperhead integration fails, run the same native tools directly. If Freerouting cannot finish, retain critical routes and use native manual cleanup or one bounded challenger. If JITX remains blocked, continue the native path without HFSS. If no valid board is achieved, deliver the real partial artifact and measured remaining failures without a validity or accepted-score claim; the full-board goal remains unfinished.

## Evidence and implementation references

- [Native checker documentation](/Users/philippe/dev/copper-scar-demo/docs/native-checks.md) and [baseline audit](/Users/philippe/dev/copper-scar-demo/docs/real-board-baseline.md).
- [Native checker](/Users/philippe/dev/copper-scar-demo/copper_scar/real.py), [focused tests](/Users/philippe/dev/copper-scar-demo/tests/test_real.py), [source preparation](/Users/philippe/dev/copper-scar-demo/scripts/prepare-pcbgolf.sh).
- [Routing proposal and executed evidence](/Users/philippe/.codex/worktrees/408e/copper-scar/investigation/autorouter-proposal.md).
- [Official PCBGolf source/rules](https://github.com/commaai/PCBGolf), [KiCad 10 PCB documentation](https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html), [Freerouting 2.4.1 CLI](https://github.com/freerouting/freerouting/blob/v2.4.1/docs/command_line_arguments.md), [Copperhead](https://copperhead.sh/), [JITX routing documentation](https://docs.jitx.com/en/latest/essentials/physical_design/autorouter.html).

External capability statements above are grounded in the saved investigations, not a new live vendor audit performed for this document. Version-specific behavior should be checked when implementation resumes.
