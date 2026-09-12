# 90s demo pass timeline — Copper Scar

Target: ~90 seconds live, narrated.

| t (s) | Beat | What to show |
|------:|------|--------------|
| 0–10  | Hook | One-liner: agent loop that scars PCBGolf attempts with Weave + official score |
| 10–25 | Demo | `.venv/bin/copper-scar demo` — 3-pass sim loop |
| 25–40 | Pass 1 | Stock DRC fail → typed scar write; spans like `[loop.pass.1] improve.scar.write` |
| 40–55 | Pass 2 | `scar_001 → keepout U1` credit; plan = apply_scars; SVG changes |
| 55–70 | Pass 3 | Gates OK + score lower than pass 1; open `demos/out/pass_timeline.txt` |
| 70–80 | Score + Weave | Formula: `volume_mm3 + 50*vias + 5000*copper_layers`. If `WANDB_API_KEY` is set, open the printed Weave UI (`copper-scar` project → Traces → `loop.pass.{i}`) |
| 80–90 | Ship/cut | Dual timeline; Mentra out of scope |

## Commands

```bash
.venv/bin/pip install -e ".[dev]"
.venv/bin/copper-scar demo
.venv/bin/copper-scar eval
.venv/bin/pytest -q
```

With `WANDB_API_KEY`: after demo+eval, open the printed Weave URL — Traces (instrumented loop), Evaluations (`copper-scar-loop-eval`), Scores / Monitors (online Signal). Inference credits: kickoff form.

## Ship / cut

**Ship for CoreWeave Hacks**

- Runnable `copper-scar demo`
- Official score exact match
- Sim loop writing typed scars + SVGs
- Weave-style span names
- Hard gates module

**Cut / defer**

- Full KiCad / PCBGolf clone integration
- Mentra / glasses UX
