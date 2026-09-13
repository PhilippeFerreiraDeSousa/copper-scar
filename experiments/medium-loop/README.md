# medium-loop: stage one

85 components, 67 nets, 70 x 60 mm, two copper layers. This is an explicitly derived PCB Golf-inspired input, not an official full-challenge submission. Frozen source: commaai/PCBGolf 7210bdb5049c5b7fdf4900a34928e2736767292a.

All eight original SBU switching blocks are retained: Q2-Q9 common-source dual NMOS, original gate pull-downs R78-R81/R98-R105/R122-R125, indicator/load resistors R82-R97/R106-R121, LED10-LED17, and the eight original sense resistors. Each dual switch sinks the original externally biased SBU load through its original load resistors. Original differing resistor values are retained. The MCU, CAN, USB, and internal power conversion are excluded deliberately.

J101-J108 are populated copies of original J4 electrical land pattern, in SBU1 channels1-4 then SBU2 channels1-4 order. Pin1/8 ground, pin2/7 externally regulated5V, pin3 IGN control, pin4 RELAY control, pin5 externally biased SBU load, pin6 sense output to external sensing circuitry. Drivers must supply original LED currents. This is a different connector function/pinout from original CAN J4. C5/C46/C50 bypass the external5V rail; LED6/R74 indicate that rail. No powered, thermal or EMI qualification is claimed.

The source J4 was DNP/excluded; our eight interfaces are explicitly populated. A generic KiCad 2x4 2.54mm vertical header STEP model is included in relative models/ with a90degree rotation matching the original horizontal pin ordering. It is a visualization model, not yet a manufacturer-qualified official-score envelope. Original signal land patterns remain byte-normalized equivalent. Local library header metadata is updated consistently. The original undersized LED6 silk marking is enlarged under the unchanged rules. These are deliberate input changes.

Original ERC, net settings, board design settings, severities and exclusions are preserved exactly. There are no source custom .kicad_dru files. Global minimum width0.1016mm, nominal Default routing width0.20mm, effective clearance0.20mm and Default vias0.60/0.30mm. All routes additionally require nominal width0.20mm. Native saves can overwrite project settings, so authoritative project bytes are restored after every native subprocess. Native schematic parity is mandatory: explicit global labels avoid root local-label slash prefixes.

Acceptance requires native0opens, zero required physical violations, zero schematic-parity issues, exact intended pad/net membership, exact retained source electrical pad geometry, source rule parity, two layers and compliant widths/vias. Router exit state or its score is not acceptance. Source missing-courtyard warnings retain original severity; no new ignored rules are introduced.

## Reproduction

Use sexpdata Python environment and KiCad10.0.6 bundled Python3.9. `build_input.py SOURCE OUT` then `native_input.py SOURCE OUT`; save/restore project around native save and move filtered PCB outside input before import. Input manifest records all refs, intended nets, source hashes and deterministic placements. `campaign.realize()` makes a new immutable stage, exports both-layer full-board DSN, routes with Freerouting2.4.1 (240s,100passes,one thread,no optional fanout,no optimization), imports, audits, renders, and stores command receipts. Do not overwrite existing stage directories.

JITX4.4: own project `.local/medium-loop/jitx`, Python package `medium_loop`, viewer design `medium_loop.design.MediumLoopInput`. Import a directory containing exactly one PCB using `jitx project import kicad INPUT --output PROJECT`. Native constraints remain authoritative; design.py explicitly restores effective clearance/width and via dimensions omitted by import. No solver state or full-board round-trip equivalence is claimed.

Each outer placement/topology action starts fresh whole-board routing. Parent routed checkpoints are immutable; their via identities are never reused as if preserved in a fresh realization. Preview has zero inherited vias; final newly produced vias have recorded UUID/net/layer/geometry. A direct topology operation must instead preserve declared via UUIDs through native saves and audit them.

## Completed native evidence (2026-09-13)

Unchanged baseline placement:183 initial missing connections ->1 native open,0DRCviolations,0schematicparity and0ERCviolations after full routing. Moving R88/R89 together(-15,-6)mm then doing a fresh full-board route reached0opens/0violations/0parity;130vias,3896.6319mm wire. Router subprocess26.25s under240s/100passes/one-thread budget. The remaining baseline net was CH4_SBU1_RELAY between Q5.3 and R88.2. This is a measured placement improvement, not a general solver guarantee.

The separate preregistered cost@2 comparison starts from the same one-open baseline. Both all-net-hpwl and signal-net-hpwl reached0 at their first decision and stayed0. Tie rule retains all-net-hpwl; there is no policy win. The board was previously observed, so this is a descriptive pilot, not independent generalization evidence.

`prepare_handoff.py BASE SOURCE` makes an accepted copy with every original retained component model and an explicit Harwin M20-9980446 nominal body/pin model for all8headers. Header model generator provenance is sibling source commit ad7f166b11fba43eb0c9de16fa626d21686a8fe7. It replaces the generic preview model and preserves every copper/via UUID, net, layer span and dimension. Source page: https://www.harwin.com/products/M20-9980446. Nominal model is not vendor detailedSTEP; no stage-two score is claimed here. The script checks native DRC/parity/ERC again and writes handoff.json.

Current local complete artifact: `.local/medium-loop/accepted-handoff/handoff.json`; source trace `relay-group-01/completed.json`; policy records `policy-pilot/records.json`; current status `status.json`; append-only placement events `events.jsonl`. Human size-family label is always **medium-loop**; stage-one validity is separate from stage-two score.
