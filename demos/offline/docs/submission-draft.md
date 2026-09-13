# Copper Scar — submission draft

Status: draft, not submitted. Evidence reviewed September 13, 2026. Replace the final checkpoint only after matching native reports, board hashes and replay images are verified.

## Form-ready description

**Project:** Copper Scar

**Tagline:** PCB design agents that remember what the board checker taught them.

**Summary:** Copper Scar closes a physical design loop: propose component placement, realize copper under bounded router effort, evaluate the saved CAD in native KiCad, and write structured diagnostics back into the next proposal. An attempt retains its parent, exact poses, board snapshot, metrics and acceptance decision. Rejected attempts stay visible. The offline replay lets a reviewer inspect the evidence without running a CAD tool or connecting to the internet.

**What we demonstrated:** On the real PCBGolf design, the native trajectory reduced missing endpoint pairs from 208 to 55 through historical routing/repair, then to a retained 54 through a diagnostic-driven terminal-topology operation followed by a full 600-second route. The final 54-open board has zero physical errors, 18 warnings and passing invariants; it remains incomplete. An independent check of its exact final hash confirms U15.3+PAD joined both original ground planes, GND islands 11 → 10, and no old connected pad group split. All component poses stayed fixed; this is not component-placement improvement. The preceding 55-open checkpoint remains in the history. The historical 55-pair checkpoint also had zero physical errors and 18 warnings. Much of that progress came from routing at an existing placement. Separate placement trials exercised the full proposal/apply/route/evaluate path, including a global expansion rejected at 477 opens and a translated SD-group exploratory result at 472. Those trials do not establish a causal placement win. On a separate eight-pad JITX integration fixture, explicit via and Route proposals retained centerline-length improvements of 53 → 51 → 49 mm with six vias and zero opens/violations. The fixture does not qualify the original product board.

**Latest component-placement result:** R37 moved (−23, −3) mm and +90°, with 244 other footprints fixed. After full 600-second routing, the retained result is 53 opens, zero physical errors and 19 warnings. Independent native graph and pose checks bind the exact final board: CMD islands 2 → 1; R37.1 stays in the same +3V3 island; no old connected pad group splits. This is a realized placement-plus-routing result. No fresh unchanged 54-parent control exists, so placement alone has not been isolated as the causal factor. Warnings rose 18 → 19, including a duplicate-via manufacturing warning. The board remains unqualified. The preceding nine-ground batch is effectively rejected by an explicit retention correction; its original historical promotion audit remains intact.

**Latest manufacturing repair:** Completed `stage1-20260913-045815-bd7054` retains 53 opens / 0 physical errors / 18 warnings. Removing a named near-coincident CAN2_L via clears the hole-to-hole finding; the completed native board preserves every connected pad group and the original project bytes. Final SHA-256 `c9228fa396fffa385ab0efadfa2f7f9aad2c0d19da21ee3fea1de8f69f901624`. The selection-basis confirmation was added after the original run, which also accepted it; it does not claim the newer policy ran inside that attempt. The full fabrication profile remains unverified and 53 opens remain. Proof, proposal, immutable attempt and verified publication receipt are in `evidence/stage1-20260913-045815-bd7054/`.

**Concrete feedback evidence:** A CAN0 group move was rejected at 77 opens / 0 physical errors / 60 warnings. Its persisted feedback record is referenced by a subsequent L6 proposal, informed by native findings and circuit review. L6 realized at 58 / 0 / 20 and was also rejected against the 55-open parent. A same-parent proposal-generator check excludes the failed CAN0 pose and selects a smaller retry; that exported challenger was not yet realized in the evidence snapshot. This proves a feedback mechanism, not a retained placement gain or learned-model prediction. See `feedback-chain/chain.md` and its hash-verified local sources.

**Why the loop matters:** A lower proxy score or a router exit code cannot establish a usable PCB. Native evaluation can reject a plausible proposal, and that rejection becomes persistent, attributable feedback. Copper Scar distinguishes a routing attempt from a placement candidate, keeps failed realization separate from a completed board, and preserves the best diagnostic checkpoint while exploring alternatives.

**Built with:** Python orchestration, KiCad native evaluation, KiCadRoutingTools placement/diagnostic routines, Freerouting realization, a separate JITX integration track, and W&B/Weave observability where upload/readback evidence exists. Source-authored topology and full-board capture are distinct capability levels.

**Current limits:** No valid finished product board, no qualified official PCBGolf score, no fabrication or assembled-product proof. Original-board JITX resubmission remains unresolved in the reviewed checkpoint. No claim of CoreWeave compute deployment, deployed online Weave Monitor, or production readiness is made.

## Links and fields

| Field | Value |
|---|---|
| Source | https://github.com/PhilippeFerreiraDeSousa/copper-scar |
| Final source commit | UNKNOWN — packaging owner to insert published checkpoint |
| Team name | Copper Scar (project name; confirm team field) |
| Team members, contact, affiliation | UNKNOWN — user to fill |
| Public demo/video URL | UNKNOWN — offline deliverables are packaged locally |
| Hackathon submission portal | UNKNOWN — not established from reviewed primary pages |
| Registration/eligibility | UNKNOWN — not verified |
| Prior work / event-period work | UNKNOWN — disclose accurately using commit history and organizer rules |
| W&B Copperhead v9 | https://wandb.ai/philippe-fdesousa/copper-scar/runs/ch-faf401a5149d0ba1 |
| W&B topology fixture | https://wandb.ai/philippe-fdesousa/copper-scar/runs/topology-search-82b7d2050019 |
| Weave calls | https://wandb.ai/philippe-fdesousa/copper-scar/weave/calls |

W&B links are supported by local owner reports/receipts, not a fresh anonymous-access test. The latest repair receipt is in evidence/stage1-20260913-045815-bd7054/observability-verified.json. The R37 53-board receipt is in placement-gain/observability-verified.json, with the earlier 54-board W&B/Weave readback receipt bundled in topology-gain/observability-verified.json and verifies matching metrics, media and finished calls. Repeated publications are not additional attempts. Confirm judge access before submission. The JITX v3 receipt records 15 remote history rows and trace links, with 310 missing pairs, 44 physical errors and seven parity issues; that run is neither the 55-open Copperhead checkpoint nor the clean topology fixture. Never exchange their screenshots or counts.

## Verified event context and claim boundaries

The organizer identifies **CoreWeave Hacks: Agent Loops Hackathon with Weights & Biases and AGI House**, September 12–13, 2026, San Francisco, focused on autonomous improvement loops and observation/evaluation with Weave. The event advertises a $20k+ prize pool. [Organizer event page](https://wandb.ai/site/resources/events/coreweave-hacks-agent-loops-hackathon-with-weights-biases-and-agi-house/)

The organizer's announcement names Best Loop Design, Best Use of Weave and Most Production-Ready among prize categories. Detailed judging requirements, track eligibility, mandatory platform use, submission format, and exact deadline were not established from the reviewed primary pages. The repository's assertion that Weave judging requires an instrumented agent, dataset evaluation and online Signal is an implementation checklist, not independently verified organizer rules. [Weights & Biases announcement](https://ir.linkedin.com/company/wandb)

The working delivery cutoff is 10:00 a.m. Pacific and user-provided submission target is before 11:00 a.m. September 13. These are task instructions, not a publicly verified organizer deadline. No prize eligibility is claimed by this draft.

PCBGolf is a separate challenge. Its score is assembled PCBA bounding-box volume in mm³ + 50 × vias + 5,000 × copper layers; lowest wins. It advertises $1,000 for the lowest score by October 12, 2026. Do not substitute bare board thickness for assembly height. [Official leaderboard](https://comma.ai/leaderboard#pcbgolf_challenge)

PCBGolf requires JLCPCB manufacturability, feasible assembly, a functional usable product and compatible mating connectors. Submission is a ZIP of the finalized KiCad project plus final-assembly STEP, subject to review. This demo is not that finalized entry. [Official challenge rules](https://github.com/commaai/PCBGolf#rules)

## Local evidence used

All reports below are in the coordinator's `outputs` folder and should accompany the final evidence package:

- `copperhead-convergence-report.md`: historical 208-pair baseline, attempt attribution and stagnation diagnosis.
- `copperhead-placement-results.md`: reported 55 / 0 / 18 retained checkpoint; failed and exploratory outer candidates; Copperhead W&B readback statement.
- `jitx-topology-capture-integration-report.md`: bounded 53 → 51 → 49 mm fixture proof and original-board limitation.
- `jitx-resumption-checkpoint.md`: original-board unchanged-parent resubmission failures.
- `jitx-wandb-upload-receipt.json`: JITX v3 remote readback receipt; separate run with separate metrics.

These are frozen report-derived claims. The packaging owner must insert any freshly verified checkpoint and matching identifiers before final recording; retaining these historical claims is safe if no stronger result is verified.
