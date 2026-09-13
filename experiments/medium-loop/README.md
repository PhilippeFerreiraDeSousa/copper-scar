# Medium PCB Loop stage one

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
