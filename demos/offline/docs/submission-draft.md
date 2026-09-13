# Copper Scar — submission draft

Status: draft, not submitted. Evidence reviewed September 13, 2026. Replace the final checkpoint only after matching native reports, board hashes and replay images are verified.

## Form-ready description

**Project:** Copper Scar

**Tagline:** PCB design agents that remember what the board checker taught them.

**Summary:** Copper Scar closes a physical design loop: propose component placement, realize copper under bounded router effort, evaluate the saved CAD in native KiCad, and write structured diagnostics back into the next proposal. An attempt retains its parent, exact poses, board snapshot, metrics and acceptance decision. Rejected attempts stay visible. The offline replay lets a reviewer inspect the evidence without running a CAD tool or connecting to the internet.

**What we demonstrated:** On the real PCBGolf design, the historical native trajectory reduced missing endpoint pairs from 208 to a retained 55. The reported 55-pair checkpoint has zero physical errors and 18 warnings, and remains incomplete. Much of that progress came from routing at an existing placement. Separate placement trials exercised the full proposal/apply/route/evaluate path, including a global expansion rejected at 477 opens and a translated SD-group exploratory result at 472. Those trials do not establish a causal placement win. On a separate eight-pad JITX integration fixture, explicit via and Route proposals retained centerline-length improvements of 53 → 51 → 49 mm with six vias and zero opens/violations. The fixture does not qualify the original product board.

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

W&B links are supported by local owner reports/receipts, not a fresh anonymous-access test. Confirm judge access before submission. The JITX v3 receipt records 15 remote history rows and trace links, with 310 missing pairs, 44 physical errors and seven parity issues; that run is neither the 55-open Copperhead checkpoint nor the clean topology fixture. Never exchange their screenshots or counts.

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
