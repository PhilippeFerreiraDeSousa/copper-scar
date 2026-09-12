"""copper-scar CLI: score baselines and run the stub agent loop."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from copper_scar.harness.schema import BaselineFile, ScoreOutput
from copper_scar.harness.score import score_from_metrics
from copper_scar.loop.run import run_loop_cli


def cmd_score(args: argparse.Namespace) -> int:
    path = Path(args.path)
    with path.open(encoding="utf-8") as f:
        raw = json.load(f)

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
        description="Copper Scar — PCBGolf score + stub agent loop",
    )
    sub = p.add_subparsers(dest="command", required=True)

    sp = sub.add_parser("score", help="Score a baseline or metrics JSON file")
    sp.add_argument("path", help="Path to baselines/*.json or metrics JSON")
    sp.set_defaults(func=cmd_score)

    lp = sub.add_parser("loop", help="Run stub agent loop and write a scar")
    lp.add_argument("--scar-id", default="scar_000", help="Scar id (default scar_000)")
    lp.add_argument("--out-dir", default="scars_out", help="Output directory for scar JSON")
    lp.add_argument("--label", default="stub loop run", help="Scar label")
    lp.set_defaults(func=run_loop_cli)

    return p


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    code = args.func(args)
    sys.exit(code if isinstance(code, int) else 0)


if __name__ == "__main__":
    main()
