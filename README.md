# Copper Scar

**One-liner:** Agent loop that scars PCBGolf attempts — Weave spans, hard gates, official comma.ai score — for CoreWeave Hacks.

## Loop

1. Observe baseline / last scar  
2. Plan (Weave `plan`)  
3. Act via tool forge (`place` / `route`) or **sim board** scars  
4. Check hard gates (fail-closed)  
5. Score with the **official** formula  
6. Write a scar JSON  
7. Compare and keep best gates-ok run  

Contract: [`copper_scar/loop/contract.md`](copper_scar/loop/contract.md)

## Score formula (exact)

```
score = volume_mm3 + 50 * vias + 5000 * copper_layers
volume = bbox_width * bbox_height * thickness_mm
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

Minimum spans recorded on each scar / demo pass:

| Span | Role |
|------|------|
| `plan` / `act.plan` | Intent + tool selection |
| `place` | Placement |
| `route` | Routing / vias |
| `gates` / `evaluate.gates` | Hard-gate eval |
| `score` / `evaluate.score` | Official score |
| `scar_write` / `improve.scar.write` | Persist scar |

Optional: `pip install -e ".[weave]"`

## Scar schema

JSON Schema: [`copper_scar/scars/schema.json`](copper_scar/scars/schema.json)  
Example: [`copper_scar/scars/examples/scar_012.json`](copper_scar/scars/examples/scar_012.json)  
Store helpers: `copper_scar.scars.store`

A scar holds `scar_id`, `metrics`, `score`, `gates`, optional typed `rule` (`keepout` / `min_clearance`), `weave.span_ids`, and `tools_used`.

## Sim board (no KiCad)

`copper_scar.sim.board` provides a deterministic AABB board:

- Parts + outline DRC (min 0.5 mm clearance)
- Actions: `shrink_outline`, `move_part`, `apply_keepout_scar`
- Official score from `volume_mm3 = w * h * thickness`

Stock baseline: [`baselines/stock.json`](baselines/stock.json) (overlapping parts + oversized outline).

## Tool forge

Adapters live under [`copper_scar/tools/registry/`](copper_scar/tools/README.md).  
Empty at ship; fill during the hack. Loop calls only registered tools.

## 90s demo

```bash
cd /workspace/copper-scar
python3 -m venv .venv
.venv/bin/pip install -e ".[dev]"
.venv/bin/copper-scar demo
```

What you should see:

1. **Pass 1** — stock board with DRC issues; Weave-style spans; writes typed scar (`scar_001`)
2. **Pass 2** — loads/applies scar with credit `scar_001 → keepout U1`; plan changes
3. **Pass 3** — gates OK and official score **lower** than pass 1

Artifacts:

- `demos/out/pass_timeline.txt` — summary table + spans
- `demos/out/board_pass_{1,2,3}.svg` — board snapshots

Also:

```bash
.venv/bin/pytest -q
.venv/bin/copper-scar score baselines/stock.json
```

See [`demos/pass_timeline.md`](demos/pass_timeline.md) for the narrated beat sheet.

## Ship / cut

**Ship (CoreWeave Hacks)**

- `copper-scar score` / `copper-scar loop` / `copper-scar demo`
- Exact official score
- Deterministic sim closed loop → scar JSON + SVG timeline
- Weave-style span names on scars
- Hard gates module + schema

**Cut**

- Full PCBGolf / KiCad automation
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
.venv/bin/pip install -e ".[dev]"
.venv/bin/pytest -q
.venv/bin/copper-scar score baselines/stock.json
.venv/bin/copper-scar loop --scar-id scar_000 --out-dir scars_out
.venv/bin/copper-scar demo
```

Requires Python ≥ 3.11.

## License

Apache-2.0 — see [`LICENSE`](LICENSE).
