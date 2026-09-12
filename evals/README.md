# Copper Scar eval dataset

Built BoardState fixtures for the CoreWeave Hacks **Best Use of Weave** eval.

Each JSON file is one row: a sim board plus expected outcomes after `copper-scar eval` runs the observe→act→evaluate→improve loop.

| id | Intent |
|----|--------|
| `overlap` | Colliding parts (stock-like) |
| `clearance` | Legal overlap-free but below 0.5 mm |
| `clean` | Already gates-ok; must not scar |
| `fat_outline` | Clean parts, wasteful outline |
| `via_heavy` | Clean layout, via-dominated score |
| `outline_violation` | Part past the board edge |
| `multilayer` | 8-layer overlap |
| `stacked` | Three overlapping ICs |

Expected keys: `drc_ok`, `score_upper_bound`, `scar_should_fire`, optional `score_should_improve`.

```bash
pip install -e ".[weave]"   # optional
export WANDB_API_KEY=...    # optional; without it the eval is offline
copper-scar eval
```
