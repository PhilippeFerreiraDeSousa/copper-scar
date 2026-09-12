# Agent loop contract — Copper Scar

One **scar** = one closed agent attempt against PCBGolf metrics.

## Loop (happy path)

1. **Observe** — load baseline / last scar metrics + gate report.
2. **Plan** — emit Weave span `plan`; choose tool-forge actions.
3. **Act** — place / route / edit stackup via registered tools.
4. **Check** — hard gates (fail-closed). Do not ship if any gate fails.
5. **Score** — official formula only:
   `score = volume_mm3 + 50 * vias + 5000 * copper_layers`
6. **Scar** — write `scar_NNN.json` (schema: `copper_scar/scars/schema.json`).
7. **Compare** — vs stock baseline and prior scars; keep best gates-ok score.

## Weave spans (minimum)

| Span        | Purpose                          |
|-------------|----------------------------------|
| `plan`      | Intent + tool selection          |
| `place`     | Component / footprint placement  |
| `route`     | Net routing / via decisions      |
| `gates`     | Hard-gate evaluation             |
| `score`     | Official score computation       |
| `scar_write`| Persist scar document            |

Optional weave install: `pip install -e ".[weave]"`.

## Hard gates

See `copper_scar.harness.gates.HARD_GATES`. Missing flag ⇒ fail.

## Non-goals this contract

- Mentra / AR glasses paths are **out of scope**.
- No cloning of remote PCBGolf in CI; link only: https://github.com/commaai/PCBGolf
