# PCB Loop — submission draft, not submitted

Tagline: An agent-driven PCB optimization loop that proposes layout changes, autoroutes the board, and learns from verified results.

PCB Loop demonstrates source-bound PCB research across a board-size family: small-loop, medium-loop and the separately developing large-loop. Stage 1 feasibility and Stage 2 score optimization are distinct from board size.

The medium-loop result closes the final remaining connection after moving a pair of components and rerouting both copper layers. Its complete-model handoff passes native connectivity, DRC, schematic parity and ERC. The small-loop Stage 2 experiment optimizes assembled bounding-box volume plus 50 per via and 5,000 per copper layer, rejecting invalid compact layouts and keeping only valid improvements. Exact final values are in the frozen viewer's native receipts.

An earlier small-loop comparison shows two authored placement policies tying after the declared decision budget; routing alone had already reached zero. Wire length is reported separately and is not presented as the official score. Weights & Biases and Weave contain real recorded metrics, readable source-bound actions, saved native board media and downloadable evidence. Traces are explicitly historical execution evidence, not fabricated model calls or hidden reasoning.

The CAD pipeline uses KiCad native validation and full-board Freerouting. JITX input/build evidence is separate unless a specific receipt demonstrates its role. No CoreWeave compute integration is claimed.

Limitations: reduced original-inspired circuits, deterministic candidate libraries and limited samples; no generalized or statistical policy superiority, official challenge eligibility, fabrication, powered hardware qualification or detailed vendor assembly-model claim. Populated header/BOM and nominal model contracts are explicit in native records.

Repository: https://github.com/PhilippeFerreiraDeSousa/copper-scar

W&B project: https://wandb.ai/philippe-fdesousa/copper-scar (private access)

The offline ZIP and video are local deliverables. No public hosting, project visibility change or submission has been performed. Team/contact/eligibility fields remain for the user to supply.
