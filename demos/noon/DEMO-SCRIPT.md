# PCB Loop — three-minute script

0:00 — “PCB Loop proposes a layout change, realizes all copper layers, checks the native board and either keeps or rejects the candidate. Above individual proposals, we compare authored rankings and revise experiment procedures using recorded failures.”

0:20 — Open medium-loop. “This 85-component, 67-net board keeps eight original-inspired switching blocks. Routing alone reduced 183 opens to one. Moving R88 and R89 together and rerouting both layers closed the final open. The subsequent complete-model handoff passed native DRC, schematic parity and ERC. This is a placement result on this input, not statistical evidence of general convergence.” Show input, routed control, actual placement preview, evaluated result, and model-only handoff.

1:00 — Open small-loop’s initial pilot. “Routing alone solves the initial 29 opens. The two placement-ranking policies produce the same choices and tie at zero after three decisions. Wire length improves, but it is a separate proxy. The dangling topology is rejected, and even a feasible but longer topology is rejected under its declared rule.”

1:35 — Open small-loop Stage 2. “Now we optimize the actual formula: assembled bounding-box volume plus 50 per via and 5,000 per copper layer. Every score requires zero opens, native DRC and schematic parity, ERC, complete populated models and the recorded assembly check. The first compacting epoch fails and preserves the valid incumbent. Later source-bound epochs adjust the margin and spacing; the graph shows only the retained valid score. Invalid candidate scores are not accepted.” Show the latest verified current score, a rejected candidate and an accepted compact placement.

2:25 — Open evidence details and the W&B/Weave links. “Every keep/reject has an action, source revision, real command timing, CAD hash and native receipt. Downloaded remote files were hash-checked. The replay and offline archive are bound to this exact snapshot.”

2:45 — “These are reduced original-inspired circuits and nominal assembly models, not a fabricated or powered product. large-loop is a separate additional size, shown only with its actual verified status. We do not claim a policy win from a tie, manufacture LLM traces, or treat an unfinished board as accepted.”
