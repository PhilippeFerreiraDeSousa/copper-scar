# medium-loop results

Stage one succeeded on an85component/67net/70x60mm/two-layer input derived from the eight original SBU switch blocks. This is not the full PCB Golf challenge. No stage-two score is claimed.

| Checkpoint | Placement action | Native opens | DRC / schematic parity / ERC | Vias | Wire mm | Full-route subprocess seconds |
|---|---|---:|---|---:|---:|---:|
| baseline-parity | none |1|0 /0 /0|128|3907.5003|31.90|
| relay-group-01 | R88/R89 translated together(-15,-6)mm |0|0 /0 /0|130|3896.6319|26.25|
| all-net-hpwl-1 | R112/R91 swapped |0|0 /0 /same schematic|143|3921.7669|30.60|
| all-net-hpwl-2 | thenR82/R90 swapped |0|0 /0 /same schematic|128|3701.5690|24.85|
| signal-net-hpwl-1 | same firstswap |0|0 /0 /same schematic|143|3921.7669|31.31|
| signal-net-hpwl-2 | same secondswap |0|0 /0 /same schematic|128|3701.5690|23.14|

Every routed run covers the entire board and both enabled copper layers, allowance240s/100passes/one thread. Optional fanout is disabled because it violates nominal trace width in this router; every net still gets full routing. No placement-only proxy is reported as routing success. Native rule, electrical pad geometry, pad/net partition, trace-width and via checks pass. Accepted-best was rechecked independently including fresh ERC0.

The first diagnosed relative group move improved1nativeopen to0. It is a small but real feasibility improvement. The separate predeclared cost@2 policy comparison tied:[1,0,0] for both. No algorithm superiority or independent generalization claim follows. Final retained geometry is from all-net-hpwl-2; signal policy produced equivalent metrics.

Accepted-best boardSHA256: bca7861dec65603a18cdcef65a9a6c23622e4a09c67e4e2a833c65815105e6bf. First-feasible handoff remains separately preserved. Both assembly packages include85/85models; eight populatedHarwinM20-9980446 interfaces use a datasheet nominal body/pin model, not detailed vendorSTEP. All routed via identities survive model-only packaging. Final source implementation includes the ERC report schema correction committed in04c0f9b; first handoff's recordedb265210 execution used that one-line correction before commit. Accepted-best was generated from clean024775e.

W&B/Weave records are real deterministic historical evidence, not live LLMcalls. Verified runs:

- https://wandb.ai/philippe-fdesousa/copper-scar/runs/medium-ad9071acd23f994
- https://wandb.ai/philippe-fdesousa/copper-scar/runs/medium-d8d03a4e2f0c240
- https://wandb.ai/philippe-fdesousa/copper-scar/runs/medium-ad74847d0b205c0

Local root `.local/medium-loop`; `replay/manifest.json` supplies before-routing/final front/back/both previews plus commands/actions/results; `accepted-best/handoff.json` is the later-stage ingestion contract. `jitx` is the separate successfully built input workspace, design `medium_loop.design.MediumLoopInput`. Native KiCad remains acceptance authority. No powered hardware qualification.

## Stage two completed

The Stage2seed is **accepted-best**, not the separate first-feasible branch. Its exactSHA bca7861dec65603a18cdcef65a9a6c23622e4a09c67e4e2a833c65815105e6bf is unchanged in Stage2baseline. Stage1lineage:183unrouted -> unchanged-placement route1open -> all-net R112/R91swap0 -> R82/R90swapretains0 -> model-onlyaccepted-best -> Stage2baseline. The diagnostic R88/R89firstzero and its53771chandoff remain preserved as a separate measuredbranch.

Official formula verified at https://comma.ai/leaderboard on2026-09-13: PCBA bounding-box volume(mm³)+50×vias+5000×copperlayers. This reduced circuit is still not an officialchallenge submission.

Baseline score65288.00=70×60×11.64+128×50+2×5000. Two valid improvements under unchanged connectivity/pads/rules/models:

| Study / candidate | Geometry action | Valid official score | Native opens / DRC / parity / ERC | Decision |
|---|---|---:|---|---|
| compact-v1/01 | sameplacement,1.5mmedge margin | null |1 /1 /0 /0|reject|
| compact-v1/02 |85%spacing,1.5mmmargin | null |1 /0 /0 /0|reject|
| edge-space-v1/01 |90%spacing,3mmmargin |59976.20|0 /0 /0 /0|keep|
| edge-space-v1/02 |85%spacing,3mmmargin |56499.28|0 /0 /0 /0|keep|
| compact-v1/03 |70%spacing,1.5mmmargin | null |6 /0 /0 /0|reject|
| compact-v1/04 |60%spacing,1.5mmmargin | null |177 /44 /0 /0|preflightreject; no routing attempted|

The edge-space study was motivated by near-header failures and ran independently alongside the remaining compact study, in separate folders/processes. Each legal proposal received240s/100passes/one-thread/both-layer full routing; no equal-policy or generalization claim is made. Global retained score is chronological minimum validscore, rather than each study's separate incumbent. Component and pad dimensions were never scaled, only positions about(55,50)mm. All8headerbodybounds were included. Conservative85modelbboxcollision checks reject overlaps before routing.

Final independent freeze: `.local/medium-loop/stage2/final-accepted/frozen.json`; exactboardSHA634dd5fbbdf74c354a3852b035089a652ef94c0ea8228fbb9b5e66656e9ff01f. Fresh DRC/parity/ERC/nativeconnectivity and independentSTEPexport/OpenCascade measurement reproduced score56499.28, with unchangedboardbytes. Dimensions63×54×11.64mm,volume39599.28mm³,138vias,2layers. Reduction8788.72(13.46%) from65288.00. All85models resolved and collision screen passed. No claim of optimality or poweredhardware qualification.

Stage2remote metrics/boardmedia/7finishedWeavecalls/finalartifactboarddigest read back successfully: https://wandb.ai/philippe-fdesousa/copper-scar/runs/medium-stage2-bca7861dec65 . Receipt `.local/medium-loop/stage2/observability/verified.json`. Retrievable completed before/final front/back/both layer snapshots and end-to-endlineage: `.local/medium-loop/stage2/replay-final/manifest.json`.

Continuation after the frozen noon checkpoint is additive. Functional net-group placement reduced vias from148to29 and score to45345.68; a controlled two-decision comparison then reached40074.08 with uniform spacing versus42538.32 with independent-axis spacing. The axis arm did not win. The40074.08 incumbent was independently rechecked and frozen in `stage2/checkpoint-40074`, without changing the noon checkpoint.

The shared native adapter reproduced40074.08 as a same-geometry control (not an improvement). Side-only outline trimming subsequently passed all12shared gates at38347.92, with25vias versus26, unchanged component poses, and assembly volume27097.92mm³. BoardSHA9bf56e7539ee3b129e7b0b52468aa135f74f10f2c87e21146c7844546675fef5. Vertical contraction initially failed four LED/Q clearance checks before routing; a local horizontal LED repair cleared preflight but left one Q7ground connection open. These rejected attempts have null scores.

A separate four-layer capability trial preserved1.6mm nominal stackup thickness and exported F.Cu/In1.Cu/In2.Cu/B.Cu with0.60/0.30mm through vias. Both the router and native connectivity reported68opens, so its score is null. Fresh native layer-name review confirmed all10vias span F.Cu→B.Cu and no medium gate was affected by the large adapter's separate numeric-layer-ID bug. One-layer native persistence probe reloaded as two layers; no one-layer scoring claim is made.
