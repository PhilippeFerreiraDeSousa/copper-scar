"""copper-scar CLI: score baselines, stub loop, and demo closed loop."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from copper_scar.harness.schema import BaselineFile, ScoreOutput
from copper_scar.harness.score import score_from_metrics
from copper_scar.eval.run import run_eval_cli
from copper_scar.loop.run import run_demo_cli, run_loop_cli
from copper_scar.sim.board import BoardState


def cmd_score(args: argparse.Namespace) -> int:
    path = Path(args.path)
    with path.open(encoding="utf-8") as f:
        raw = json.load(f)

    # Prefer full BoardState serialization when present
    if "width" in raw and "height" in raw and "thickness_mm" in raw:
        board = BoardState.from_dict(raw)
        metrics_dict = board.metrics()
        score = score_from_metrics(metrics_dict)
        from copper_scar.harness.schema import Metrics

        metrics = Metrics.model_validate(metrics_dict)
        out = ScoreOutput(score=score, metrics=metrics)
        payload = out.model_dump()
        payload["label"] = board.label
        payload["placeholder"] = board.placeholder
        if board.notes:
            payload["notes"] = board.notes
        payload["board"] = {
            "width": board.width,
            "height": board.height,
            "thickness_mm": board.thickness_mm,
            "parts": len(board.parts),
        }
        print(json.dumps(payload, indent=2))
        return 0

    baseline = BaselineFile.model_validate(raw)
    score = score_from_metrics(baseline.metrics.model_dump())
    out = ScoreOutput(score=score, metrics=baseline.metrics)
    payload = out.model_dump()
    payload["label"] = baseline.label
    payload["placeholder"] = baseline.placeholder
    if baseline.placeholder:
        payload["warning"] = "PLACEHOLDER metrics — not fab-measured"
    if baseline.notes:
        payload["notes"] = baseline.notes
    print(json.dumps(payload, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="copper-scar",
        description="Copper Scar — PCBGolf score + sim agent loop",
    )
    sub = p.add_subparsers(dest="command", required=True)

    from copper_scar.real import run_real_cli
    rp = sub.add_parser("real-check", help="Check a real KiCad candidate and persist native failure evidence")
    rp.add_argument("--project", required=True, help="Candidate .kicad_pro")
    rp.add_argument("--reference", required=True, help="Original .kicad_pro with unchanged rules and schematics")
    rp.add_argument("--out-dir", default=".local/checks")
    rp.add_argument("--kicad", default="kicad-cli")
    rp.add_argument("--copperhead", default=None, help="Optional pinned Copperhead executable")
    rp.add_argument("--qualification", help="Candidate-bound engineering review JSON")
    rp.add_argument("--promote-to", help="New destination; only copied after all gates pass")
    rp.set_defaults(func=run_real_cli)

    sp = sub.add_parser("score", help="Score a baseline or metrics JSON file")
    sp.add_argument("path", help="Path to baselines/*.json or metrics JSON")
    sp.set_defaults(func=cmd_score)

    lp = sub.add_parser("loop", help="Run stub agent loop and write a scar")
    lp.add_argument("--scar-id", default="scar_000", help="Scar id (default scar_000)")
    lp.add_argument("--out-dir", default="scars_out", help="Output directory for scar JSON")
    lp.add_argument("--label", default="stub loop run", help="Scar label")
    lp.set_defaults(func=run_loop_cli)

    dp = sub.add_parser("demo", help="Run deterministic 3-pass sim closed loop")
    dp.add_argument("--passes", type=int, default=3, help="Number of passes (default 3)")
    dp.add_argument("--baseline", default=None, help="BoardState JSON (default baselines/stock.json)")
    dp.add_argument("--scars-dir", default=None, help="Scar store directory (default scars_out)")
    dp.add_argument("--out-dir", default=None, help="Demo artifacts dir (default demos/out)")
    dp.add_argument("--seed", type=int, default=0, help="Deterministic seed (reserved)")
    dp.add_argument(
        "--weave-project",
        default=None,
        help="W&B Weave project (default: WEAVE_PROJECT or copper-scar)",
    )
    dp.add_argument(
        "--no-weave",
        action="store_true",
        help="Disable Weave even if WANDB_API_KEY is set",
    )
    dp.set_defaults(func=run_demo_cli)

    ep = sub.add_parser("eval", help="Run the built BoardState dataset (Weave Evaluation when live)")
    ep.add_argument("--dataset", default=None, help="Fixture directory (default evals/dataset)")
    ep.add_argument("--passes", type=int, default=3, help="Loop passes per fixture (default 3)")
    ep.add_argument("--out-dir", default=None, help="Working dir for per-row boards/scars")
    ep.add_argument(
        "--weave-project",
        default=None,
        help="W&B Weave project (default: WEAVE_PROJECT or copper-scar)",
    )
    ep.add_argument(
        "--no-weave",
        action="store_true",
        help="Disable Weave even if WANDB_API_KEY is set",
    )
    ep.set_defaults(func=run_eval_cli)

    return p


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    code = args.func(args)
    sys.exit(code if isinstance(code, int) else 0)


if __name__ == "__main__":
    main()
