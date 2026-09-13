# Placement, topology and capture integration — terminal evidence

The explicit-via/Route proposal loop works on the bounded eight-pad fixture.
Capture-based reuse works on a small single-layer fixture with the ownership
adaptation below. The 245-component original-board proxy is technically blocked
at unchanged captured-parent resubmission. No original-board candidate or gain
is reported. All integration-owned runtimes are stopped; original owner layouts
and checkpoints were preserved. This directory remains uncommitted review work.

## Proposal, realization and evaluation

`planner.py`, `research_adapter.py`, `research_proposals.py`, and `reproduce.py`
connect pinned KRT placement proposals to concrete via sites and layer-specific
Route endpoints, native realization, exported centerline measurement and twice
KiCad evaluation. Parent hashes and exact component poses bind proposals.
Via span sets vertical reach; Route.layer sets horizontal routing; a
PortAttachment supplies net association. Native routing determines traces.

`.local/topology-research-01` completed four alternatives and two retained moves:
53 → 51 → 49 mm, six vias, zero opens and violations. Every trial preserved seven
unrelated route records and four unrelated via records exactly after resolving
numeric net IDs. `.local/topology-proposals-02` additionally rejected worsening
55.133/55.153 mm alternatives. Each alternative first rebuilds and verifies the
same retained parent. These are fixture results, not PCB Golf qualification.

W&B evidence and readback receipt: `.local/topology-research-observability-01`;
https://wandb.ai/philippe-fdesousa/copper-scar/runs/topology-search-82b7d2050019
The replay uses completed-snapshot intervals, including evaluation overhead.

## Capture ownership and via blocker

`capture_loop.py` uses public capture first and updates in-memory objects. It
does not reconstruct Trace/Copper geometry or require source-file rewriting.
Generated Routes can disappear from ownership on repeated capture: the linker
replaces its links and only adds newly created routes. The bounded flat-circuit
adaptation saves object references, captures, then reattaches only objects that
actually disappeared. Attaching duplicates before capture fails duplicate-child
validation. `.local/capture-owned-routes-02/evidence` verifies native routing,
captured resubmission and a TP4 move with zero opens/violations; roundtrip copper
and unrelated nets remain equal. `evidence/capture-owned-routes.json` summarizes
this. This adaptation is not a general hierarchy ownership solution.

Captured vias encounter a separate packaging issue. Capture writes resolved
`diameters` to memoized via instances. Via.type then resolves through Proxy.type;
a diagnostic restoration of the declared enum bypasses that Python error but
native submission fails `No ref for local: [Int object]`. The dry payload probe
shows definition IDs 52,53,57,58,62,63 colliding with all six geometry IDs after
capture-equivalent diameter overrides plus that enum assignment; the baseline
has no collisions. See `.local/capture-source-vias-resume-01/dry-payload` and
`evidence/via-identity-collision.json`. Public dememoization failed on initial
submit with `No ref for local: 0`. These are concrete blockers, not a supported
via-capture repair. No private ID forcing or installed-package patch was used.

## Original-board trial and common-parent gate

`.local/capture-fullboard-proxy-02` contains a new native proxy with all 245
original components and physical net boundaries, verified against its manifest
(with documented SW1 pad aliases). Recorded original poses seed the new parent.
Only four local top-layer Route intents are present, on three nets, with no
vias or imported legacy copper. Full obstacles/boundaries do not make this
full-board routing. The explicit 0.0762 mm manufacturing clearance floor is part
of this new parent; it is not a preserved legacy routed board.

The initial parent export passed its component/net boundary gate. Two whole
board DRC runs agree: 499 opens, 51 errors (16 hole clearance, 35 solder mask
bridge), 44 warnings. Native capture completed with four owned Routes. Unchanged
`Runtime.submit(rd.root)` then caused physical-client exit 255 and repeated
relaunches; the controller timed out after 180 seconds. The first fatal error is
`FATAL ERROR: Illegal tag bits`, runtime.log line 846. The stack passes
`core/no-method-error`, `core/hash`, `hamt/key-hash`, `Feature/layer-data`, and
`inject-cache-effect/geometric-match` at cache.stanza:438. This locates the
observed failure in native cache geometry matching; it does not prove its root
cause or establish that the preceding shared-pin warnings caused it.

No roundtrip export exists, so parent-to-roundtrip geometry, poses, rules and
twice-DRC equality remain unverified. KRT and the candidate move never started;
there was no rejected candidate to restore. The script now explicitly gates on
all three comparisons and compares a restored parent after rejection; those
additional branches were added after this failed run and were not exercised by
it. A local comparator check accepted the parent against itself and rejected an
external copy with altered clearance. No equivalent native retry was launched.

Exact evidence:

- `.local/capture-fullboard-proxy-02/evidence/result.json`
- `.local/capture-fullboard-proxy-02/evidence/native-crash-excerpt.txt`
- `.local/capture-fullboard-proxy-02/runtime/.jitx/logs/runtime.log`
- `.local/capture-fullboard-proxy-02/run.stderr`
- `.local/capture-fullboard-proxy-02/evidence/00-parent/whole-board-check/summary.json`
- `.local/capture-fullboard-proxy-02/runtime/.capture-uncertain.json`
- `evidence/original-capture-blocker.json` (portable summary with log hash)

The CLI stopped only the disposable proxy02 runtime PID2496 with SIGTERM after
the timeout. A process check found no remaining integration capture controllers
or runtimes. Managed design files and the uncertainty marker remain intact.
A future native retry needs a changed, supported hypothesis; clearing managed
caches or rebuilding a different parent would not qualify this roundtrip.

## Validation and scope

Recorded focused tests: four new planner/adapter tests plus twelve existing
contract tests passed; thirteen native/original bridge tests passed in the
JITX environment with pytest supplied separately. The final comparator change
also passed the two explicit acceptance/rejection checks described above.

Historical fixed-Copper transfer evidence is retained separately and is not the
optimization implementation. Official examples/shipped lifecycle research found
no reusable public HFSS outer loop or capture/resubmit example: see the Main
output `jitx-existing-optimization-loop-research.md`. The thin custom loop is
therefore still required, with the native capture blockers unresolved.
