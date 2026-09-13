# PCB Loop: ten-minute presentation

Slides 1-12 are the main talk. Slides 13-14 are hidden Q&A backups. The 75-second W&B slot includes about 40 seconds of live navigation.

## Slide 1

0:00-0:30 | Opening
I built PCB Loop to explore whether an AI agent can improve a circuit board through measured experiments. The agent changes placement, a router rebuilds the connections, and native CAD checks decide whether the result works. This is the best recorded Medium candidate. I will show the actual pipeline, the evidence behind the improvement, and what remains unfinished.

## Slide 2

0:30-1:15 | Objective
The task is more subtle than making a board smaller. Moving components closer together can reduce assembled volume, but it can also make routing difficult or require more vias. The objective adds the assembled bounding-box volume to a penalty of fifty per via and five thousand per copper layer. That creates a measurable tradeoff between compactness and routing cost. A smaller candidate only counts if it still passes the circuit and physical checks. For this demonstration, Medium is an eighty-five-component reduced circuit derived from the original board, with complete nominal assembly models. Its score uses the competition formula, but it is not an accepted original-board submission.

## Slide 3

1:15-2:15 | Corrected architecture
The loop has two stages. Stage one seeks a valid, fully connected board. Stage two starts with a valid board and searches for a lower score. A persistent Codex task chooses an experiment and writes or changes Python code. Python applies the proposal to native board geometry. Freerouting then routes across the enabled layers, including choosing via transitions. KiCad imports that result and independently checks the saved board. The experiment records the measurements and failure details so the task can decide what to try next. In all four demonstrated board families, this full-board routing path used Freerouting. JITX import and display were a separate branch of the work. Separate JITX routing research also exists, but it did not route these evolving demo candidates.
Presenter cue: follow the diagram from left to right, then point to the feedback loop.

## Slide 4

2:15-3:10 | Update input and output
Here is the precise answer to what the update step receives and returns. The agent reads the board and schematic, the applicable constraints, the current best result, and reports from previous attempts. Those reports can identify missing connections, affected components, clearance problems, or an unfavorable score tradeoff. The output is an experiment: Python proposal code, concrete parameters, and a reason for trying them. That code may generate one candidate or a batch. Evaluation then returns the routed board, native diagnostics, score terms, and the keep or reject decision. The agent can use those results in its next decision. A model decision and a candidate evaluation are different events, so a deterministic batch can contain several candidates without another model call between them.

## Slide 5

3:10-4:00 | The actual prompt
The judges asked what prompt runs at each update. In these runs, the Medium work continued in a persistent Codex task. It received an initial task instruction, a later transition into stage two, and subsequent Coordinator feedback. The sentence on this slide is an exact excerpt from that initial instruction. It describes an outer experiment loop and an inner routing and evaluation loop. The stage-two message changed the objective to the official formula while requiring validity and preservation of the best result. The public archive contains those historical messages. There was no single fixed prompt submitted to a newly spawned agent for every candidate. To understand what actually happened, we inspect both the task instructions and the recorded candidate actions.

## Slide 6

4:00-4:50 | Candidate construction
The candidate starts from a selected native KiCad board. Python reads the source geometry and applies an explicit action. The experiments include contracting spacing, grouping connected blocks near their headers, changing the outline, and a ground-escape topology proposal. The experiment also carries the project settings, libraries, and models needed for evaluation. KiCad exports a DSN routing problem. Freerouting returns an SES route, and KiCad imports it into the candidate. That means the action record describes the proposed change, while the router adds the resulting trace and via geometry. Freerouting supports routing across multiple enabled layers. For the Medium results shown here, the design and score remained on two copper layers.

## Slide 7

4:50-5:35 | Acceptance
The router finishing is only one step. The saved result has to pass native connectivity and rule checks, schematic and net parity, and preservation of the intended electrical geometry and constraints. Assembly checks require resolved models and screen for overlap. In stage two, a valid candidate replaces the retained board only when its score is strictly lower. A tie keeps the incumbent. Invalid attempts still have value because their reports explain why a proposal failed, so they remain in the experiment history. These checks support the recorded CAD result. They do not establish that the board has been manufactured or tested with power.

## Slide 8

5:35-6:25 | Overall result
Across the completed Stage Two record, the best valid Medium score went from sixty-five thousand two hundred eighty-eight to thirty-five thousand three hundred sixty-five. That is a forty-five-point-eight percent reduction. The chart plots the best valid score after each completed attempt. Flat portions matter: they include attempts that failed or did not improve the retained result. The ledger contains twenty-five completed stage-two events, excluding baselines, frozen copies, separate stage-one policy trials, and interrupted attempts without completed records. This is a combined chronology across studies. It is useful for seeing progress, but it does not mean every candidate was created by modifying the immediately preceding candidate.
Presenter cue: pause on the downward curve, then point out one flat section.

## Slide 9

6:25-7:20 | Concrete intervention
This pair of boards shows one useful experiment. On the left is a valid candidate before functional grouping. On the right, connected blocks sit near their own external headers. After routing, the via count falls from one hundred forty-eight to twenty-nine. The score improves from forty-nine thousand nine hundred ten to forty-five thousand three hundred forty-five, about nine percent. The assembled volume actually increases slightly in this comparison. The reduction in via penalty more than compensates for that increase. That is why we measure the complete objective instead of assuming the smallest outline is always the best board. Python proposed the arrangement, and Freerouting produced the traces. These are the actual saved board renders from those attempts.

## Slide 10

7:20-8:05 | Provenance and storage
Each completed attempt has its own study and candidate folder. The preview captures the geometry before routing, and the evaluated board captures the result after import. The event record stores the action, parameters, timestamps, source commit, commands, reports, and decision. Two fields are especially useful: proposal source identifies the geometry being transformed, while parent incumbent identifies the comparison board. Independent scale trials may repeatedly transform the same source. Python scripts evolve in the working tree and are versioned through commits; the runner does not automatically archive a separate copy of every Python file inside each candidate. The public ledger exposes the action history. Its native board paths refer to local artifacts.

## Slide 11

8:05-9:20 | W&B walkthrough
W&B lets me connect a chart point to the experiment that produced it. I will open the functional-grouping record and show the action, then the native result and score. These are records uploaded from completed experiments. Command logs contain the actual routing time. The last verified remote upload reaches a score of forty thousand seventy-four; the newest local best is lower and is shown separately in this deck.

LIVE DEMO: allow about 40 seconds inside this 75-second slot.
1. Click Inspect the 29-via result. Use the browser already signed into W&B.
2. Expand the action and show the grouping proposal and source information.
3. Expand result and show validity, the 29-via count, and score 45,345.68. If the schema nests it, use the output/global-incumbent score.
4. Point to command or router-log evidence. A zero-duration backfilled Weave span is not the router runtime.
5. Return to the deck. If login or loading slows the demo, stay on the slide and describe these fields instead. Do not spend the closing time troubleshooting.

## Slide 12

9:20-10:00 | Close
The project has valid reduced Small and Medium circuits. Medium shows a forty-five-point-eight percent score reduction with a saved experiment history. Large and the original two-hundred-forty-five-component board remain incomplete. The next step is to qualify that original board while preserving the full circuit and its manufacturing constraints. What we have built is a practical way to connect agent-written experiments with an external router, native checks, and inspectable evidence. The public repository links the implementation branches, historical prompts, and candidate action ledger. Thank you.
Presenter cue: stop at 10:00. The remaining two slides are hidden backups for questions.

## Slide 13

BACKUP | Score decomposition
The baseline terms sum to 65,288.00: 48,888 volume, 6,400 for 128 vias, and 10,000 for two layers. The best recorded terms sum to 35,365.44: 23,815.44 volume, 1,550 for 31 vias, and the same 10,000 layer penalty. The total decrease is 29,922.56. The grouping comparison in the main talk uses a different pair of intermediate candidates and has 148 versus 29 vias.

## Slide 14

BACKUP | Tool roles
All four demo families used Freerouting for full-board routing trials. Earlier original/full-board work also used KiCadRoutingTools for targeted repairs. JITX initial-board import and display, and separate source-authored routing research, are distinct from that demonstrated loop. Candidate designs are stored as KiCad artifacts, not as a fresh JITX project for each iteration. W&B and Weave expose recorded experiment evidence, not a claim that every model decision was traced.