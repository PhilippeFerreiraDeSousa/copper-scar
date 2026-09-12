# Copper Scar

**One-liner:** Agent loop that scars PCBGolf attempts — Weave spans, hard gates, official comma.ai score — for CoreWeave Hacks.

## Loop

1. Observe baseline / last scar  
2. Plan (Weave `plan`)  
3. Act via tool forge (`place` / `route`)  
4. Check hard gates (fail-closed)  
5. Score with the **official** formula  
6. Write a scar JSON  
7. Compare and keep best gates-ok run  

Contract: [`copper_scar/loop/contract.md`](copper_scar/loop/contract.md)

## Score formula (exact)

```
score = volume_mm3 + 50 * vias + 5000 * copper_layers
```

Source: [comma.ai leaderboard — PCBGolf](https://comma.ai/leaderboard#pcbgolf_challenge)  
PCBGolf repo (link only, do not clone into this tree): https://github.com/commaai/PCBGolf

## Hard gates

Fail-closed. Missing flag = fail. See `copper_scar.harness.gates.HARD_GATES`:

- `drc_clean`
- `erc_clean`
- `netlist_match`
- `fab_stackup_ok`
- `min_trace_clearance`
- `via_annular_ok`
- `outline_closed`

Do not ship a scar to the “best” board unless `gates_ok` is true.

## Weave spans

Minimum spans recorded on each scar:

| Span | Role |
|------|------|
| `plan` | Intent + tool selection |
| `place` | Placement |
| `route` | Routing / vias |
| `gates` | Hard-gate eval |
| `score` | Official score |
| `scar_write` | Persist scar |

Optional: `pip install -e ".[weave]"`

## Scar schema

JSON Schema: [`copper_scar/scars/schema.json`](copper_scar/scars/schema.json)  
Example: [`copper_scar/scars/examples/scar_012.json`](copper_scar/scars/examples/scar_012.json)  
Store helpers: `copper_scar.scars.store`

A scar holds `scar_id`, `metrics`, `score`, `gates`, optional `weave.span_ids`, and `tools_used`.

## Tool forge

Adapters live under [`copper_scar/tools/registry/`](copper_scar/tools/README.md).  
Empty at ship; fill during the hack. Loop calls only registered tools.

## 90s demo

See [`demos/pass_timeline.md`](demos/pass_timeline.md) — hook → score CLI → stub loop → scar → gates → forge → ship/cut.

## Ship / cut

**Ship (CoreWeave Hacks)**

- `copper-scar score` / `copper-scar loop`
- Exact official score
- Stub loop → scar JSON
- Weave span names on scars
- Hard gates module + schema

**Cut**

- Full PCBGolf / KiCad automation
- Measured (non-placeholder) stock baseline
- Mentra paths

## Dual timeline

| Track | When | Outcome |
|-------|------|---------|
| **CoreWeave Hacks** | This weekend | Harness + demo + Weave story |
| **Oct 12 $1k** | Oct 12 | Gates-ok scars with real measured deltas |

## Mentra — out of scope

Mentra / AR glasses integration is **out of scope** for Copper Scar. Do not block the CoreWeave or Oct 12 tracks on Mentra work.

## How to run

```bash
cd /workspace/copper-scar
pip install -e ".[dev]"
pytest -q
copper-scar score baselines/stock.json
copper-scar loop --scar-id scar_000 --out-dir scars_out
```

Requires Python ≥ 3.11. Baseline metrics in `baselines/stock.json` are **PLACEHOLDER** — labeled as such; replace before claiming leaderboard deltas.

## License

Apache-2.0 — see [`LICENSE`](LICENSE).
