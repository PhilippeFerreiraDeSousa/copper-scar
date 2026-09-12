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

| Span | Purpose |
|------|---------|
| `loop.pass.{i}` | One closed-loop pass |
| `observe.load` | Load baseline |
| `act.plan` / `act.apply_scar` | Intent + scar application |
| `evaluate.drc` / `evaluate.gates` / `evaluate.score` | DRC, gates, official score |
| `improve.scar.write` | Persist scar document |

Attributes on live spans: `score`, `best_score`, `drc_count`, `gates_ok`, `scar_id`, `policy_version`.

Optional live tracing: `pip install -e ".[weave]"` and set `WANDB_API_KEY`. Default project is `copper-scar` (`WEAVE_PROJECT` / `--weave-project`). Without the key or package, the loop is identical and offline.

Built eval dataset: `evals/dataset/` via `copper-scar eval` (Weave Evaluation when live). Online Signals: `copper_scar.eval.scorers` applied to each pass trace; attach the same criteria under Weave → Monitors.

## Hard gates

See `copper_scar.harness.gates.HARD_GATES`. Missing flag ⇒ fail.

## Non-goals this contract

- Mentra / AR glasses paths are **out of scope**.
- No cloning of remote PCBGolf in CI; link only: https://github.com/commaai/PCBGolf
