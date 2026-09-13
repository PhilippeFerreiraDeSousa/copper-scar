# Placement loop results and integration readiness

September 12, 2026, Pacific. The retained Copperhead incumbent remains **55 native missing endpoint pairs, zero physical errors, 18 warnings**. No valid board or Stage Two score exists. The earlier retained 58-open board had 11 warnings; the warning increase to 18 is explicit and remains unqualified.

## Completed placement / routing experiments

| Policy / attempt | Placement | Native before route | Native after route | Decision |
|---|---|---:|---:|---|
| v8 `182444-f54c2b` | Initial incumbent placement, fanout enabled, 600 s requested | 58 / 0 / 11 | 55 / 0 / 18 | Retained diagnostic incumbent |
| v8 `183642-ca8dab` | All 245 components translated in 17 rigid groups; 182 × 338 mm outline | 499 / 0 / 7 | No importable session; native failure recheck 499 / 0 / 7 | Failed realization, rejected |
| v9 `184802-649d0d` | Initial retained placement, fanout stage disabled, 180 s requested | 55 / 0 / 18 | 55 / 0 / 18 | Not retained |
| v9 `185217-d06b3b` | Same global expanded placement, fanout stage disabled, 180 s requested | 499 / 0 / 7 | 477 / 0 / 7 | Completed budget-limited result, rejected against incumbent |
| v9 `185942-295ff2` | Entire 13-part SD group translated +15 mm X; other 232 references fixed; same outline | 499 / 0 / 7 | 472 / 0 / 7 | Improvement over exploratory parent; not retained against 55-open incumbent |

Numbers are missing native endpoint pairs / physical errors / warnings. All listed native checks passed circuit/identity/support-file invariants. Attempt IDs have prefix `stage1-20260912-`.

Global expansion preserved footprint/pad sizes and rotations. Independent native comparison checked all 1,078 physical pads, 245 component identities, and rigid within-group offsets to 1 nm, plus unchanged GND plane layers/clearance. It translated 1,745 internal-net copper items and removed 3,403 items on nets crossing groups. The plane polygons expanded, with the six-layer stack retained. The first 600-second attempt spent its effort in fanout and failed to deliver SES before the 620-second wrapper limit. v9 both started whole-board autorouting immediately and exported sessions at the requested 180-second effort limit plus shutdown time.

Every route input exported 297 nets, 1,053 assigned pins, 245 footprints and six copper layers, with 0.6/0.3 mm through vias and no via minimization. This proves the eligible scope, not that each net was searched: Freerouting does not expose sufficient per-net coverage here. The result is censored by effort. KiCad's DSN has a 50 µm SMD-to-SMD exception alongside the 200 µm rule; native acceptance uses the unchanged original project rules. No rule relaxation was made to obtain a passing native result.

**The expanded result does not prove that generous space is worse or that these placements are infeasible.** Expansion removes substantial prior copper and lengthens interfaces; time-limited rebuilding confounds geometry with copper history and effort. Likewise, 477 → 472 after the SD pose is one exploratory measurement, with affected boundary copper removed and no replicated matched-parent control. The per-net audit attributes the five fewer opens to +12V (−1), +5V (−1), CAN2_L (−1), and GND (−2); no SD net count improved. The reduction cannot be attributed to the SD pose. It proves the proposal/apply/route/evaluate path operates, not a robust optimization win.

## How the research changed the implementation

Read the completed `pcb-placement-research.md` and inspected the actual pinned KRT entrypoints: `place_optimize.py`, `placement/quench.py`, `placement/groups.py`, `placement/diagnosis.py`, and `place_route_loop.py` at `1c428c0b2285a4dfe8901ca7035109ded6cfbb4d`. The stock loop ranks failed nets then iterations; the optimizer gates routed input and its writer does not handle arbitrary retained copper. Those are not sufficient native acceptance or mutation boundaries, so the stock loop/writer was not adopted.

The new pose proposer actually reused `derive_groups`, `make_state`, `diagnose`, `group_move_valid`, `apply_group_move` and `total_cost` against the 245-footprint native parent in an isolated KRT environment. It examined 24 deterministic translations of the explicit SD group in 0.94 s, kept three finalists, and selected +15 mm X. The proxy decreased from 85,991.57 to 83,861.37, chiefly from 2,698 to 2,627 projected crossings; HPWL changed only 1.52 mm. Power/plane nets were excluded only from this proposal proxy and remained included in whole-board native evaluation. No native CAD was written by KRT, and proposal undo restored its in-memory starting poses.

KRT reported 69 footprints without courtyards and used pad bounding boxes. Its pad legality layer was off in the ranking probe, and it does not model retained copper. Therefore native application rejects a stale parent hash/pose, fixes all unrelated components, moves the group rigidly, audits internal/boundary copper, refills unchanged planes, and runs the native legality/invariant gate before routing. This is selective geometry reuse with measured limitations, not a claim that KRT's screen establishes legality.

Implementation: `scripts/copperhead_pose_proposals.py`, `scripts/copperhead_apply_pose.py`, and the existing native outer loop. The exact proposal and a 245-component/1,078-pad exchange manifest are preserved in `.local/copperhead/proposals/sd-rigid-pose.json` and `.local/copperhead/exchange/sd-rigid-pose-v1.json`.

## Joint integration recommendation

**Continue separate implementations; prepare one isolated bridge experiment. Do not merge branches yet.** Copperhead and JITX owners agree. Copperhead should supply identity-checked pose proposals and independent native evaluation; JITX should supply incremental multilayer realization and typed diagnostics. Both engines' partial results are coupled to the quality/capabilities of the other stage, so neither side is established by isolated progress alone.

I independently loaded JITX fixture `03-multilayer-routed` and `04-moved`: both exports contain eight footprints, six physical through vias, ten copper segments, two layers, and stored KiCad reports with zero violations/opens. TP4 moves (+2, −2) mm in KiCad coordinates. Copper geometry on HOLD, CROSS_B and CROSS_C is identical; only CROSS_A changes. This supports the small incremental capability. It does not validate 245-component loading, six-layer routing, original rules or the real board's geometry. Source/API inspection confirms `phd.reposition`/`via-add`/per-layer routing are used; definitions alone were insufficient before actual via instances were added.

Current blockers to functional integration:

1. Parent geometry is different. The +15 mm SD proposal is based on Copperhead's exact expanded native parent, not JITX's current original-board state. Absolute poses cannot be copied blindly. A verified hierarchical local/global transform and explicit rebase or equivalent imported parent is required.
2. The read-only correspondence audit now resolves all 245 references and the 13 proposed SD references to JITX IDs. Both exported boards have 297 named net groups and 196 multi-node partitions with exactly matching endpoint membership; explicitly excluding 111 source NC pads gives the 191 active JITX partitions. Five J3 NC pad-pair groups explain the partition difference. This closes the named-terminal mapping question. Geometry still differs: JITX exports 12 extra unnamed mechanical/cutout-derived pad representations, and footprint shape equivalence is not yet established.
3. JITX's original loaded board lacks via definitions, and adding/reloading them while preserving its live state is not yet qualified. The successful fixture had definitions from creation. The generalized via/layer topology planner is not a completed whole-board autorouter merely because the fixture works.
4. JITX's unchanged fixture reload reset the interactive pose to its source value while retaining connectivity. Its subsequent source-update fixture persisted the accepted pose and added another legal via definition: the recorded result preserves the pose, all copper and six existing via instances, with zero opens/violations. This establishes the required source-persistence sequence on the small fixture; the earlier full-board cache failure and full-board rebuild behavior remain separate unqualified risks.
5. Copperhead's router provides eligible net scope but not exhaustive per-net attempt coverage. Its short, partial results cannot conclusively rank placement feasibility. Returned diagnostics must distinguish unattempted, effort-exhausted, terminal refusal and actual geometry violations.

The smallest next proof is a fixed proposal in the already qualified isolated fixture, using explicit component/pad/net and transform mappings, preserving the accepted state and unrelated copper, instantiating legal vias, exporting a completed native board, and returning independently checked whole-board connectivity/DRC plus action-specific diagnostics to the proposer. An equivalence-qualified original-board subset follows; applying the real SD proposal waits for exact parent/constraints correspondence. No new shared service or framework is needed; see `copperhead-placement-exchange.md`.

Code compatibility is a separate question: a read-only changed-path comparison at common base `27846f947b19588c271856001379e30da503ee1e`, Copperhead `baf6e77a`, JITX `08515e58`, including each worktree's then-uncommitted files, found no overlapping changed paths. Copperhead owns its adapter/scripts/docs; JITX owns its integrations and evaluator. This is not a tested merge or a runtime-equivalence guarantee. No branch merge or other track's CAD mutation was performed.

## Observable evidence

- W&B v8: https://wandb.ai/philippe-fdesousa/copper-scar/runs/ch-af8a774730aff846
- W&B v9: https://wandb.ai/philippe-fdesousa/copper-scar/runs/ch-faf401a5149d0ba1
- Local outer replay: http://127.0.0.1:53918/replay/latest (5× only; latest policy, completed evaluations).
- Legacy history remains separate. Failed realization is represented separately, not a fabricated curve point. Publication reads back metrics, matching native image records and finished Weave calls and deduplicates repeat uploads. A short server propagation delay was observed and bounded readback retries were added; the earlier failed verification was not reported as success.
