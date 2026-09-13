# Copper Scar — three-minute demo

Use the offline replay and architecture graphic. Spoken copy is approximately 390 words, leaving time for clicks and pauses. Freeze board images and counts from the same manifest before recording. The 55-open figure below is the historical report checkpoint; replace it only with a newly verified real-board checkpoint. Keep the JITX fixture visually labeled throughout.

| Time | Screen | Spoken copy |
|---|---|---|
| 0:00–0:25 | Real board overview, status visible | “This is Copper Scar: PCB design agents that remember what the board checker taught them. A plausible layout can still be impossible to connect. We built a loop that proposes placement, asks real routing tools to realize it, checks the saved CAD, and carries the failure forward. The product board is still incomplete. What you’ll see is the measured progress and the decisions that kept us honest.” |
| 0:25–0:50 | Architecture graphic | “The outer loop chooses a placement candidate. The inner loop gets a bounded routing budget. Native KiCad evaluates the resulting board, including connectivity and physical errors. Each attempt saves its exact parent, poses, board and diagnostics. Those diagnostics shape the next proposal. A router finishing is an event; a board passing its checks is a separate result.” |
| 0:50–1:20 | Real-board historical replay; matching board and curve | “Here is the real PCBGolf trajectory. Missing endpoint pairs fell from 208 to this retained checkpoint at 55. It has zero native physical errors and 18 warnings. It is not a finished board. Most of this reduction came from repairing copper at an existing placement, so we label the curve as routing history. We do not turn routing attempts into a count of placement optimizations.” |
| 1:20–1:50 | CAN0 result, L6 result, and saved feedback chain | “Here is a concrete feedback chain. A CAN0 group move closed one target connection, but collateral damage left 77 opens, so we rejected it. The saved findings and circuit review informed a narrower L6 proposal, which explicitly references that prior attempt. L6 realized at 58 opens and was also rejected against the 55-open parent. The feedback changed what we tried; it did not establish a placement win.” |
| 1:50–2:20 | JITX fixture tab, prominent FIXTURE label | “This separate eight-pad fixture tests a narrower integration claim. Concrete via sites and layer-specific Route proposals survive realization and independent evaluation. Two retained moves reduce measured centerline length from 53 to 51 to 49 millimeters, with six vias and zero opens or violations. Unrelated copper is preserved. This is evidence for the loop interface on a fixture, not proof that the original board is solved.” |
| 2:20–2:45 | Local evidence/provenance and W&B receipt | “Every plotted state points to a saved board and evaluation. Rejected attempts remain visible. W&B and Weave links are backed by recorded upload/readback evidence; this replay carries the local evidence so the presentation works offline. The original-board JITX bridge still has a resubmission blocker, and we show that boundary rather than borrowing the fixture’s clean result.” |
| 2:45–3:00 | Overview with incomplete status | “The result is a design loop with memory and an independent referee. The next milestone is a fully connected, qualified product board. Today we can show exactly what improved, what failed, and why the next proposal should be different.” |

Presenter notes:

- If a newer checkpoint exists, update its opens, physical errors, warnings, ID and matching screenshot together. Never replace just the number in this script.
- Keep the historical and fresh runs distinct; do not connect unrelated engine states into one best-so-far curve.
- Native missing-pair counts are not counts of distinct nets.
- Do not call the trace-length fixture metric an official PCBGolf score.
- If the question is “Did you solve the challenge?”, answer: “No. The real board is incomplete; the contribution is the evidenced improvement loop and its bounded integration proof.”
- If asked about Weave prize requirements, the detailed organizer criteria remain unverified; do not infer an online Monitor from stored traces.
