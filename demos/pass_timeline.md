# 90s demo pass timeline — Copper Scar

Target: ~90 seconds live, narrated.

| t (s) | Beat | What to show |
|------:|------|--------------|
| 0–10  | Hook | One-liner: agent loop that scars PCBGolf attempts with Weave + official score |
| 10–20 | Score | `copper-scar score baselines/stock.json` → formula on screen |
| 20–35 | Loop | `copper-scar loop --scar-id scar_demo` → scar file appears |
| 35–50 | Scar schema | Open `scar_*.json`: metrics, gates, weave.span_ids |
| 50–65 | Gates | Hard gates fail-closed; ship only when `gates_ok` |
| 65–80 | Tool forge | Point at `tools/registry/` + contract.md spans |
| 80–90 | Ship/cut | Dual timeline: CoreWeave hack ship vs Oct 12 $1k track; Mentra out of scope |

## Ship / cut

**Ship for CoreWeave Hacks**

- Runnable `copper-scar` CLI
- Official score exact match
- Stub loop writing scars
- Weave span names wired in scar docs
- Hard gates module

**Cut / defer**

- Full KiCad / PCBGolf clone integration
- Mentra / glasses UX
- Non-placeholder measured baselines

## Dual timeline

| Track | Date / venue | Goal |
|-------|----------------|------|
| CoreWeave Hacks | This weekend | Working harness, demo, Weave story |
| $1k track | Oct 12 | Measured deltas vs stock, gates-ok scars on real boards |
