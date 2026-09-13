# Incremental multilayer realization proof

The isolated `incremental_fixture.design.IncrementalProof` demonstrated actual native multilayer routing and route preservation after a component move. This is an eight-pad synthetic fixture, not qualification of the full PCBGolf board or a complete generic via/layer planner.

The fixture source is `integrations/jitx/incremental_fixture/design.py`. Its four two-terminal nets use eight top-only 1.2mm pads. A top-layer route/via/pour keepout spans the board edge to edge. `HOLD` stays on one side; `CROSS_A/B/C` require layer transitions. The 32×28mm two-layer board starts with a 0.60/0.30mm through-via definition and **no instances or authored routes**. Native generation uses 0.20mm width, 0.25mm copper spacing, 0.28mm copper-hole spacing, 0.50mm edge spacing, and 0.15mm minimum annular ring.

| Checkpoint | Actual vias | Exported opens | Physical violations | Result |
|---|---:|---:|---:|---|
| Definition-only single-layer sweep |0|3|0|Only HOLD realized. Three preliminary native routes were not copper.|
| Explicit via escapes + bottom trunks |6|0|0|All four source net memberships match; 10 realized segments across two layers.|
| Move TP4 / a_right from (8,6) to (10,8) |6|0|0|All 10 native route IDs survive. Eight route records stay identical; only two CROSS_A segments change.|
| Rebuild unchanged source |6|0|0|Interactive TP4 pose resets to its source pose. Connectivity stays clean, but placement is not preserved.|
| Author accepted moved pose and add 0.80/0.40mm via definition; rebuild |6|0|0|Both definitions loaded; all existing net copper, six instances, and moved poses preserved exactly.|

The initial sweep returned native net connected groups even for the three **preliminary** routes through the obstruction. Independent KiCad reported three opens. Thus neither native group merging nor a `routed` message alone establishes realized connectivity. The controller removed only those three identified preliminary routes before adding the required transitions; HOLD was never unrouted.

`phd.via-add` used each current pad as origin, the actual component instance as anchor, and explicit sites 2mm toward the barrier. It created a through-via instance, net attachment, and top escape. `phd.route` on layer 1 selected the six newly returned via IDs. No forced placement, rule relaxation, generated-file edits, or external router were used. The native reposition operation moved the anchored via and re-realized its existing route automatically. The exported copper for HOLD, CROSS_B and CROSS_C remained exactly identical after normalizing object IDs and net-number renumbering.

The successful source update matters: via definitions can be added to an existing *small healthy* design while preserving its routing, if current placement is authored into the source. This does not establish that the old full-board identity can reload safely: the earlier full-board 006 reload crashed its native cache loader, while this fixture did not. No operation targeted accepted full-board 002/009.

## Evidence and reproduction boundary

Local evidence root: `/Users/philippe/dev/copper-scar-jitx/runs/incremental-proof`. Every mutation phase includes the exact plan, before/final replies, successful export barrier, outward native snapshots, and exported KiCad project. The main phases are `01-definition-only-sweep`, `02-via-escapes`, `03-multilayer-routed`, `04-moved`, `05-reloaded`, `06-moved-before-source-update`, and `07-source-updated-reload`. `proof-result.json` summarizes the independent gates.

`fixture_control.py` is deliberately fixed to this identity and permits only the bounded native operations used by the proof. It records per-request outputs and exports after the supported completion barrier, then loads final state. A request timeout is not native cancellation; do not issue a new mutation after an unresolved timeout. Run only one fixture controller at a time. Initial build took 0.93s, unchanged reload 1.04s, and source-update reload 0.82s. The native route and move operations each completed in well under a second on this small fixture; these are not realistic-board benchmarks.

`verify_incremental_fixture.py <evidence-root>` uses the existing parser environment and KiCad CLI. It checks all eight references and four exact endpoint partitions, top-only pads, legal through-via dimensions/layers, source generation-rule floors, and identical nonaffected copper. It makes external copies, removes legacy embedded netclasses, and normalizes duplicate IDs without changing geometry; no duplicate IDs occurred in this fixture. Two independent DRC runs agree for every verified stage. It does not assert electrical SI, assembly, thermal, or product feasibility for a synthetic test.

The initial source and source-update patch are committed with the fixture. Exact action plans and the final compact result are committed under `integrations/jitx/incremental_fixture/evidence/`. Native `designs/` state, installed proprietary implementation sources, and generated CAD remain external. To reproduce, prepare a new isolated project/identity rather than overwrite an existing fixture or accepted native design. Adapt the fixed identity in the controller explicitly for that new project; use the emitted current IDs when generating action plans.

## Limits and next integration experiment

The controller uses a known topology and explicit via sites; it does not choose a topology or layer assignment for arbitrary boards. Three well-separated cross-barrier nets do not test congested escapes or guarantee convergence. The proof establishes the incremental realization mechanism and a source-reload boundary, not sufficient routing coverage on the original board.

Copperhead independently inspected the 03/04 exports and confirmed the eight footprints, six vias, ten segments, clean DRC, TP4-only move, and exact unrelated-copper preservation. Both tracks recommend a fixed-proposal isolated bridge next and continued separate implementation, with no branch merge yet. See `jitx-copperhead-readiness.md` for the actual original-board correspondence and remaining barriers.
