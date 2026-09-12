# Tool forge

Registered tools live under `registry/` (one module or manifest per tool).

## Convention

- Name tools for what they do on the board (`place_refdes`, `route_net`, `check_drc`).
- Each tool should be callable from the agent loop and emit a Weave child span.
- Keep side effects on a working copy; scars capture before/after metrics.

## Registry

Populate `registry/` with real tool adapters during the hackathon.
`.gitkeep` holds the empty directory until the first tool lands.

## PCBGolf

Upstream challenge / tooling: https://github.com/commaai/PCBGolf  
(link only — do not assume a local clone in this repo).
