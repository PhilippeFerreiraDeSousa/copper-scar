# JITX recording and incremental routing

The local dashboard is http://127.0.0.1:53919/. It was opened in a new foreground Safari tab and visually verified. VS Code's existing JITX view remains the interactive board. The dashboard shows history on the left, actual selected board captures on the right, and separates the best incomplete candidate from the latest attempted candidate. No valid board or Stage Two score exists.

## Recording contract

The implementation adapts Copperhead's read-only local HTTP view, measured subprocess phases, five-second heartbeat, immutable preview and incumbent/attempt distinction. It does not share mutable files or reuse Copperhead's inner checker. The inspected sources were `copper_scar/tools/copperhead/dashboard.py`, `dashboard.html`, `stage1.py`, `metrics.py` and `docs/native-feasibility-loop.md`, plus owner feedback. Specific pitfalls avoided include copied stale previews, treating controller activity as worker liveness, and overwriting a mid-placement board before its routing comparison.

JITX records remain under `/Users/philippe/dev/copper-scar-jitx/runs/stage1/`. Every evaluated candidate has original-rule KiCad DRC and all-sheet ERC, independent pin/part/value/MPN/project invariants, input/output hashes, policy version, measured evaluation times, and failure/retention reasons. New subprocess records add actual PID, status, five-second heartbeat, exact argv, invoked Python-source hashes and elapsed time. Attempt records snapshot generator source and helper hashes. Historical missing hashes and pose audits remain explicitly unknown; today's rendering-tool hashes are not represented as historical evaluator provenance.

Preview publication verifies the board bytes match the evaluation hash, copies those exact bytes to a content-addressed checkpoint, exports a real KiCad SVG and records its hash. The published checkpoint is not overwritten. Rendering failure does not replace the displayed board. Superseded policy-v1/v2 checks remain in the table but are excluded from the corrected-v3 trajectory. Duplicate object UUID normalization and repeated DRC agreement are required for current reliable measurements. Warnings, parity and unknown engineering gates remain visible. The outer-copper SVG does not display inner-layer copper or airwires; the fit control crops empty board area, not the board artifact itself. It is a discrete real checkpoint, not a routing animation.

The source project and metric revisions are explicit. Raw JITX costs cannot be compared directly against Copperhead costs with different footprints, layers, priorities or evaluation coverage. A changed layer count is an experimental change, not an isolated placement improvement.

## Runtime ownership

The user explicitly requires JITX to own `designs/<design>/`, including `design-info/physical-layout.design`, associated state and routing geometry. The agent does not manually edit, delete, replace or restore these files. Whole-directory copies go outward to immutable evidence locations only. Source placement parameters are agent-owned inputs; generated copper is runtime-owned output.

Earlier fresh candidates 001/002/003/006 used new Python design identities. `campaign.py` previously required a new design directory, which made these fresh starts rather than incumbent-routing continuations. This was initially motivated by native reload crashes, but cannot serve as the normal incremental loop. The driver now defaults to an existing identity, snapshots it outward, optionally rebuilds, then captures/routes/exports it. A fresh identity requires an explicit reset reason. No old design directories were deleted by these drivers.

Concrete installed 4.4 viewer operations:

- `phd.load` captures board, interactive placements, routed records and nets.
- `phd.reposition` receives a list of existing group IDs and target poses. JITX updates affected copper. No file patch or unlock call is used.
- `phd.route` receives `layer`, selected `pads`, `force:false` and `configure:null`. Targeted R20 routing used only its two named nets; a whole-floorplan move affects all groups and therefore routes all affected nets.
- Installed `services/autoroute.ts` also exposes `phd.unroute` with explicit layer/route IDs. It has not been used for blanket rip-up here.
- `do_export('kicad', design)` is the installed legacy exporter. Route acknowledgement is not completion: export waits while physical tasks are in progress. The command record includes that wait.

## Measured lifecycle evidence

Corrected original-rule two-layer incumbent002 had 316 missing connections, 44 physical errors, 224 warnings, seven parity warnings and ERC zero.

| Transition | Actual geometric outcome |
|---|---|
| Existing002 to live R20 move004 | 1,863 of 1,896 copper primitives preserved; 33 removed, 22 added across three nets; only R20 moved |
| Move004 to targeted route005 | All 1,885 primitives preserved; none removed or added; 317 missing connections remained |
| Fresh four-layer006 | Pre-route capture contained no routed records; full native phase 308.45 seconds; 313 missing, same44 errors/224 warnings/seven parity/ERC zero; incumbent before009 |
| Same-identity unchanged rebuild007 | Build timed out after 90.24 seconds; native physical client crashed loading existing board state with `FATAL ERROR: Illegal tag bits` and exit255; subsequent `phd.load` could not be delivered |

The 1,333 primitives matching the prior output after fresh006 are not proof of saved-state reuse: the pre-route capture demonstrates a fresh start. Copper primitive identity ignores UUID and numeric net IDs, but does not merge segment fragmentation and is not a connectivity proof.

Test007 preserved a complete outward native-input checkpoint before invoking the normal unchanged build command. No generated state was patched or reset. The 313-open checked board remains available; the006 live physical client is unavailable. A supported same-identity source-rebuild path is therefore **not qualified**, and no speed benefit is claimed. The surviving002 live client is used for continued placement/routing work without a rebuild.

## Broad circuit-group experiment008

A recorded floorplan proposal considers all five circuit groups: Channels, Power, STM32H7, USB/SD and CAN FD. Their imported bounding boxes are interleaved. The proposal separates them into five slots, choosing among120 assignments and deterministic right-angle rotation sweeps using actual cross-group net connectivity. Weighted component-center half-perimeter wire length is a proposal heuristic, not a routed-length or electrical-quality metric. Connector access, assembly and SI remain open gates.

One live reposition call moved/rotated245 components. R20 specifically returns from the earlier rejected override to its original within-group pose; this is the one measured rigid-pose outlier. Other within-group relative positions are preserved. Actual input and post-placement boards were separately exported, normalized, checked and frozen before rerouting.

Input:317 opens,44 physical errors. After group placement:386 opens,44 errors. Both passed immutable circuit/project checks with ERC zero. The placement was not retained. World-coordinate geometry has zero identical primitives because the whole floorplan moved; that alone would falsely suggest a full reset. A second audit transforms prior copper by measured block motion and finds219 of307 eligible internal-net primitives preserved. It excludes cross-group nets and nets touching the R20 outlier. Pre-reroute native capture already contains420 routed records, demonstrating live state retention. The completed incremental route measured307 opens and48 physical errors under policy v3 and was rejected. Trial009 then moved six connected power/indicator parts and retained310 opens/44 errors/237 warnings. Repeated DRC agrees; no valid board exists.

If the broad proposal regresses, the saved incumbent remains retained; further proposals or API-based pose changes use runtime operations. Outward snapshots are not copied over live `designs/` files. A cache-corruption workaround requiring native-state changes needs a separate precise explanation, not a silent reset.

## Current009 and on-demand replay

Best incomplete candidate is `candidates/iteration-009-power-neighborhood-routed`, policy `jitx-feasibility-v3`: **310 missing, 0 incorrect, 44 physical errors, 237 physical warnings, 7 parity findings, ERC 0**. Independent invariants (245 components, 1066 named pads, 191 active partitions; original schematics and rules unchanged) passed; repeated DRC agrees. No valid board or Stage Two score exists.

Native routing is stopped. The surviving two-layer physical client is `pcbgolf_import.stage_one_002.StageOne002`; its live placement is trial009 on the broad008 floorplan. Six power/indicator parts moved;239 other poses stayed fixed in009. Accepted parameters and complete proposed Python are preserved in `runs/stage1/best-placement-parameters.json` and `iteration-009-power-neighborhood/Pcbgolf-proposed.py`. They have not replaced live generator source. The runtime owns all files under `designs/`; none were manually changed or restored.

The13 warnings added relative to006 are3 LED9/C51 silkscreen overlaps and10 silk/mask clipping findings. These require assembly-marking/courtyard review, although electrical-clearance errors did not increase. Policy v3 prefers fewer missing connections before warning count while forbidding regression in incorrect connections, physical errors or ERC errors. Retention means a better incomplete diagnostic checkpoint, not acceptance.

Current native002 has no via definitions (fresh read-only load confirmed). Supported viewer via operations consume a named definition; the installed source builder sends a full design load. Offline source using saved009 placement plus a0.60/0.30mm through-via translates successfully; its emitted definition was checked. Installing it in the accepted live design is not qualified: unchanged same-identity build007 crashed006 with `Illegal tag bits`. No new design identity or manual cache replacement was used to bypass this.

Dashboard: http://127.0.0.1:53919/ . On-demand replay: http://127.0.0.1:53919/replay . The action freezes completed records and previews, renders/reuses a5× video (30seconds of history in6seconds) keyed by the exact cutoff, and restarts playback. Cutoff and generation status are explicit. Original fixed replay ending008 remains historical; the on-demand replay includes009. No pre-recording placement snapshots are invented.

Policy v1 is superseded because embedded export netclasses overrode source rules. Policy v2 is superseded because duplicated JITX object UUIDs made DRC object attribution ambiguous. Policy v3 normalizes IDs without geometry changes, rechecks immutable invariants and rejects inconsistent repeated DRC measurements. Historical reports remain saved.

See `docs/jitx-via-workflow-and-warning-review.md` for the concrete routing blocker, source-safe alternatives and diagnostic next placement steps. No routine permission is needed; no further full routing effort is claimed until the via workflow is usable.

Replay verification: latest5× artifact is `outputs/jitx-latest-replay-5x.mp4`,15 logical checkpoints through009-routed,6.000seconds at1920×1080 H.264. Background browser verified cache reuse and restart from ended6s to playing0.3389s; foreground UI was not changed. Current cutoff key is09a8ae80a2352d959229. Dashboard deduplicates corrected rechecks by logical action; raw history remains visible. A newer request during rendering queues the latest frozen cutoff. Verification evidence: `runs/stage1/replays/latest-verification.json`.16 tests passed; original immutable board invariants reverified.
