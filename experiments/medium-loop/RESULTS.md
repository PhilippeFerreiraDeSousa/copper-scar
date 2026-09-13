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
