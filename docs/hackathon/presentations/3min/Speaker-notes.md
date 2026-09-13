# PCB Loop: three-minute presentation

Present slides 1-6. Slides 7-8 are hidden backup slides for questions.

## Slide 1

0:00–0:20
I built PCB Loop to explore whether an AI agent can improve a circuit board by changing its placement, measuring the result, and trying again. The hard part is shrinking the design while keeping every required connection and manufacturing rule intact.

## Slide 2

0:20–0:55
There are two stages: first get a valid board, then improve its score while preserving validity. A persistent Codex task reads the board, constraints, and previous failures. It writes or revises Python experiments. Freerouting chooses trace paths and vias across the allowed layers, and native KiCad checks decide whether the result passes. The saved diagnostics guide the next experiment. Some experiments evaluate a batch without another model decision between candidates. JITX import and display are separate from this demo routing path.

## Slide 3

0:55–1:25
On the 85-component Medium circuit, the recorded score fell from 65,288 to 35,365, a 45.8 percent reduction. The score combines assembled volume with via and layer penalties. This line shows the best valid result after each completed attempt, including flat sections when attempts fail or do not improve it. These are native CAD checks on a reduced demo circuit. I am not claiming the full original competition board is solved or that this hardware has been manufactured.

## Slide 4

1:25–1:55
One useful experiment regrouped components around their own external headers. The resulting route used 29 vias instead of 148. The assembled volume actually increased slightly, but the lower via penalty more than compensated, improving the score by about 9 percent. This is why the loop measures the full objective rather than just trying to make the outline smaller. The pictures are the recorded native board renders; Python proposed placement, and Freerouting generated the routes.

## Slide 5

1:55–2:30
W&B is how I inspect and compare the experiments. The charts show which attempts improved the retained score. In Weave, I can open a concrete attempt and see its action, source commit, commands, router log, and validation result. The artifact ties those measurements to the exact board. These records were uploaded after execution, so they are experiment evidence rather than live LLM spans. If time permits, click the grouping trace and expand action and result. The latest verified remote upload predates the latest local result.

## Slide 6

2:30–3:00
We now have valid reduced Small and Medium circuits, and a saved history of how each candidate was generated and evaluated. Large and the original 245-component board remain incomplete. The next step is qualifying that original board while preserving the same circuit and manufacturing constraints. The source, agent instructions, and candidate action history are public, so people can inspect what ran and build on the experiment. Thank you.

## Slide 7

Backup slide, excluded from the three-minute script. The excerpt is from the actual creation prompt. A task continues across experiments; there is no fresh agent spawn for every candidate. Some candidates come from a deterministic batch. Later Coordinator messages ask for a specific diagnostic-driven intervention. The prompt describes intended action space, while the recorded actions establish what actually ran.

## Slide 8

Backup slide. All four demo families used Freerouting for full-board trials. Earlier original/full work also used KiCadRoutingTools for targeted repairs. Separate JITX source-authored routing and transfer fixtures exist, but they do not establish the four-family demo as a JITX routing loop. Candidate directories preserve before-routing preview, evaluated board, actions, source hashes, and reports.