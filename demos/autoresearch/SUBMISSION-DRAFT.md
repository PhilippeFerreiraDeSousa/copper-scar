# Submission copy — draft, not submitted

Project: Copper Scar

One-line description: An evidence-driven PCB optimizer research loop that tests placement and via proposals with whole-board routing, native connectivity gates and measured policy comparisons.

What it does: Copper Scar couples a lower proposal–route–evaluate–retain loop to a higher policy comparison. In the demonstrated pilot, two agent-authored rankings use the same four-candidate library, starting board and six-layer routing protocol. Every screening decision, routed attempt and retained incumbent is recorded. A policy is selected only after the predeclared three-decision budget, and any subsequent consumption is shown separately.

What makes the demo useful: It exposes a local placement edit that appears promising but splits an existing connected group, and refuses to retain it. The challenger reaches 44 missing pairs one decision earlier, while baseline catches up on its second decision. Both policies finish at 44 missing pairs after three decisions, so the predeclared tie rule keeps placement_first. The selected policy was subsequently consumed by a separate R89 placement campaign; its exact outcome is in the package receipt. Independent partition and trace-geometry evidence constrains the causal story.

Sponsor integration: Weights & Biases records actual metrics, native board media, router log snapshots and versioned evidence artifacts. Weave links experiment, policy and lower-decision spans with readable evidence summaries. Full downloadable JSON/CAD files are hashed and read back. No CoreWeave compute integration or per-lower-step LLM inference is claimed.

Limitations: Prior-informed single-board finite-library pilot. No no-update control isolates the contact normalizer. No verified backend random seed. Open connections remain; no engineering, manufacturing or hardware qualification is claimed. The public evidence summaries do not represent hidden model reasoning.

Repository: https://github.com/PhilippeFerreiraDeSousa/copper-scar

Demo source branch: codex/demo-final-owner

Private W&B project: https://wandb.ai/philippe-fdesousa/copper-scar

Local demo: two-level-autoresearch/index.html

Offline video: two-level-autoresearch/two-level-replay.mp4

Team name, additional members, contact details, public hosting/video link, eligibility declarations and final submission fields: not supplied; leave unanswered until provided by the team. Private W&B access has not been expanded. No submission has been sent.

The matched pilot uses KiCad native evaluation and Freerouting. JITX source-authored routing and transfer proofs are separate supplemental work and did not realize these pilot routes.
