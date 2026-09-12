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
| `loop.pass.{i}` | One observe → act → evaluate → improve cycle |
| `observe.load` | Load stock baseline |
| `act.plan` / `act.apply_scar` | Intent + apply typed scar |
| `evaluate.drc` / `evaluate.gates` / `evaluate.score` | DRC, hard gates, official score |
| `improve.scar.write` | Persist scar |

Each live span carries attributes: `score`, `best_score`, `drc_count`, `gates_ok`, `scar_id`, `policy_version`.

### Live Weave — 90s Best Use of Weave script

Judges look for **all three**: (1) an agent that is actually instrumented, (2) a real eval on a dataset you built, (3) an online Signal on live traces.

The offline demo is unchanged without Weave. Live tracing is a no-op unless the extra is installed **and** `WANDB_API_KEY` is set.

```bash
pip install -e ".[weave]"
export WANDB_API_KEY=...          # https://wandb.ai/authorize
export WEAVE_PROJECT=philippe-fdesousa/copper-scar  # user entity (org blocks bare project names)

# W&B Inference credits (kickoff form): fill the form circulated at
# CoreWeave Hacks so Serverless Inference can power UI Signals/Monitors.
# Event page: https://wandb.ai/site/resources/events/coreweave-hacks-agent-loops-hackathon-with-weights-biases-and-agi-house/

copper-scar demo                  # 1. explicit weave.init + loop spans/ops
copper-scar eval                  # 2. built dataset → Weave Evaluation
```

`--weave-project` overrides `WEAVE_PROJECT`. `--no-weave` forces the offline path even if a key is present.

When tracing is on, commands print a Weave UI URL:

`https://wandb.ai/<entity>/copper-scar/weave`

**90s film beats**

| t | Show |
|---|------|
| 0–25 | `copper-scar demo` — Traces: `copper_scar.agent_pass` / `loop.pass.{i}` → `observe` → `act` → `evaluate` → `improve` |
| 25–55 | Expand pass 2: `act.apply_scar`, `evaluate.drc` / `gates` / `score`, attributes `score`, `best_score`, `drc_count`, `gates_ok`, `scar_id`, `policy_version` |
| 55–75 | `copper-scar eval` — Evaluations → `copper-scar-loop-eval` on dataset `copper-scar-boards` (`evals/dataset/`, 8 BoardState fixtures we built) |
| 75–90 | **Signal:** Traces → Scores column (live `apply_scorer`), then Monitors (below) |

**Attach / enable the online Signal in the Weave UI**

Code already applies three programmatic Signals to every `loop.pass.{i}` call:

- `score_improves_vs_baseline` — official score dropped vs the fixture/stock baseline
- `gates_ok_when_scar_applied` — after a scar is applied, hard gates pass
- `drc_cleared_after_scar` — after a scar is applied, DRC is clean

To attach the same criteria as a live Monitor / UI Signal (uses W&B Inference credits):

1. Run `copper-scar demo` once so ops appear
2. Weave sidebar → **Monitors** → **New Monitor** (or **Browse signals** → **Create custom signal**)
3. Operations: `copper_scar.agent_pass` and/or `loop.pass.1` (repeat for `.2` / `.3` if listed separately)
4. Sampling: 100%
5. Judge model: a **Serverless Inference** model (credits from the kickoff form)
6. Scoring prompt: see `SIGNAL_UI_PROMPT` in [`copper_scar/eval/scorers.py`](copper_scar/eval/scorers.py)
7. Create → re-run `copper-scar demo` → Traces shows the Signal tags / Scores column

Without the key or without the weave extra, `copper-scar demo` and `copper-scar eval` still run identically offline (no network, no crash).

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
.venv/bin/copper-scar eval
```

What you should see:

1. **Pass 1** — stock board with DRC issues; Weave-style spans; writes typed scar (`scar_001`)
2. **Pass 2** — loads/applies scar with credit `scar_001 → keepout U1`; plan changes
3. **Pass 3** — gates OK and official score **lower** than pass 1
4. **Eval** — 8 built fixtures in [`evals/dataset/`](evals/dataset/); table of expected vs loop output

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

- `copper-scar score` / `copper-scar loop` / `copper-scar demo` / `copper-scar eval`
- Exact official score
- Deterministic sim closed loop → scar JSON + SVG timeline
- Explicit Weave spans/ops around observe/act/evaluate/improve
- Built eval dataset + Weave Evaluation + online Signals
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
.venv/bin/copper-scar eval
```

Requires Python ≥ 3.11.

## License

Apache-2.0 — see [`LICENSE`](LICENSE).
