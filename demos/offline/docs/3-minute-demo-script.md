# Copper Scar — three-minute demo

Use the offline replay and architecture graphic. Spoken copy is approximately 390 words, leaving time for clicks and pauses. Freeze board images and counts from the same manifest before recording. The 53-open retained checkpoint is bound to `stage1-20260913-044612-074e42`, final board SHA-256 `7cae9a8ec99e95450992d9fa620c890d5ac720f4e29c2b404afd14b3d725e0c4`. Keep the JITX fixture visually labeled throughout.

| Time | Screen | Spoken copy |
|---|---|---|
| 0:00–0:25 | Real board overview, status visible | “This is Copper Scar: PCB design agents that remember what the board checker taught them. A plausible layout can still be impossible to connect. We built a loop that proposes placement, asks real routing tools to realize it, checks the saved CAD, and carries the failure forward. The product board is still incomplete. What you’ll see is the measured progress and the decisions that kept us honest.” |
| 0:25–0:50 | Architecture graphic | “The outer loop chooses a placement candidate. The inner loop gets a bounded routing budget. Native KiCad evaluates the resulting board, including connectivity and physical errors. Each attempt saves its exact parent, poses, board and diagnostics. Those diagnostics shape the next proposal. A router finishing is an event; a board passing its checks is a separate result.” |
| 0:50–1:20 | Complete historical replay; correction and failed attempts preserved | “Here is the full real-board history. Routing and repair reduced missing pairs from 208 to 55. A diagnosed ground-access operation reached 54. Now a component move plus full routing reaches 53, with zero physical errors and 19 warnings. Failed attempts stay visible. One mistaken promotion has an explicit correction beside its preserved original audit. These are measured checkpoints, not a finished product board.” |
| 1:20–1:50 | 54-open parent, R37 move/proof card, 53-open final board | “R37’s CMD pad was isolated from the connector branch. We moved just that resistor and routed for 600 seconds. The final graph joins all three CMD pads, preserves its power connection and splits no previously connected pad group. Independent checks confirm the other 244 footprints stayed fixed. This demonstrates the combined placement-and-routing result. There was no fresh unchanged-parent control, so we do not isolate the placement’s causal effect. Warnings rose to 19.” |
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
