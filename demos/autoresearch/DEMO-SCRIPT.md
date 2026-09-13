# Copper Scar — three-minute demonstration

**0:00–0:25 — The problem and two loops**
“PCB routing is full of tempting local improvements that can damage existing connectivity. Copper Scar records a proposal, runs the whole-board router, and lets native evidence decide whether to keep it. Above that loop, we test the optimizer itself: two authored ranking hypotheses, one frozen protocol, three decisions per arm.”

Open the actual pilot view. Keep the graph on the left and exact board snapshots on the right. This is the current matched experiment; the historical research ledger is supplemental.

**0:25–1:10 — An attempted improvement that must be rejected**
Select `placement_first`, decision 1. Show Original → Updated before routing → After full routing. R123 moves from (155,98) to (153,98.5). A roughly ten-minute whole-board route ends at 45 missing pairs and zero physical errors. The original CH2_SBU2_RELAY group splits: R123.2 loses its connection to U3.78, Q7.3 and R108.2. The proposal is rejected, and the retained-best curve stays flat at 45.

“Zero physical errors and a completed router process are insufficient. We preserve original connected pad groups as well.”

**1:10–1:45 — What the challenger actually demonstrated**
Select `island_first`, decision 1; compare layers including In4.Cu. The challenger retains 44 missing pairs, zero physical errors and 20 warnings, preserving all original pad groups. The two added vias are dangling. Both first attempts made the same CAN2 bridge using existing vias; the challenger’s advantage was avoiding the R123 collateral split. Baseline decision 2 then catches up to 44.

“This result supports a narrow ranking observation. It does not prove the new vias enabled routing, nor establish a generally superior optimizer.”

**1:45–2:20 — The higher-level decision**
Use Play actual checkpoints to reveal measured results in chronological order. The completed comparison has 49 events and exactly three decisions per arm. Both retain 44 missing pairs, zero physical errors and 20 warnings. The predeclared tie rule keeps placement_first. Time and distance are secondary diagnostics.

Show the selected-policy receipt and the separately labeled next-campaign receipt. The selected placement_first version 1 was consumed at 09:23:52 Pacific and dispatched the R89 (-1,0) trial for full routing at 09:24:43. Read its final outcome from the included receipt; do not treat consumption alone as proof of a completed route. This follow-on campaign is outside the frozen comparison.

**2:20–2:50 — W&B / Weave and reproducibility**
Open a linked Evidence summary and complete original files trace. Show its proposal, alternatives, native outcome, decision and causal limitation. These are public evidence summaries, not fabricated model thought traces: deterministic ranking executes each lower decision. Downloadable artifact files contain complete JSON and exact CAD, with SHA256 readback receipts; the Weave array preview is not the full record.

**2:50–3:00 — Close**
“The deliverable is a measurable, inspectable optimizer research loop. This board still has open connections and is not engineering-qualified. The offline package preserves the actual experiment, including rejected proposals and limitations.”

Fallback: play `two-level-autoresearch/two-level-replay.mp4`. The frozen package opens offline, without W&B credentials or a local CAD installation.

The matched pilot uses KiCad native evaluation and Freerouting. JITX source-authored routing and transfer proofs are separate supplemental work and did not realize these pilot routes.

Verified R89 outcome: the separate trial finished at 09:35:07 Pacific after 674.45 seconds overall. Native evaluation found 45 missing pairs, zero physical errors and 21 warnings, with an original connected pad group split. It was rejected; the selected board remains at 44 missing pairs. This proves selected-policy consumption and executed evaluation, not an improvement from that follow-on trial.
