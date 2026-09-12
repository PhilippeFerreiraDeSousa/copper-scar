"""Run the built BoardState dataset through the agent loop.

Offline: local table + deterministic scorers (no Weave).
With WANDB_API_KEY + weave extra: also logs a Weave Evaluation and applies
online Signals to each pass trace.
"""

from __future__ import annotations

import asyncio
import json
import tempfile
from pathlib import Path
from typing import Any

from copper_scar.eval.dataset import load_dataset, resolve_dataset_dir
from copper_scar.eval.scorers import match_dataset_expected, row_passed, score_online_signals
from copper_scar.loop.run import run_pass
from copper_scar.loop.weave_trace import (
    OP_AGENT,
    WeaveTracer,
    get_tracer,
    init_tracer,
    reset_tracer,
)
from copper_scar.sim.board import BoardState


def run_example(
    example: dict[str, Any],
    *,
    n_passes: int = 3,
    work_dir: Path | None = None,
    quiet: bool = True,
) -> dict[str, Any]:
    """Run the closed loop on one dataset fixture."""
    board = BoardState.from_dict(example["board"])
    baseline_score = board.official_score()
    baseline_drc_ok = len(board.check_drc()) == 0

    own_tmp: tempfile.TemporaryDirectory[str] | None = None
    if work_dir is None:
        own_tmp = tempfile.TemporaryDirectory(prefix="copper-scar-eval-")
        work_dir = Path(own_tmp.name)
    try:
        case_dir = work_dir / str(example["id"])
        case_dir.mkdir(parents=True, exist_ok=True)
        baseline_path = case_dir / "board.json"
        baseline_path.write_text(json.dumps(board.to_dict(), indent=2) + "\n", encoding="utf-8")
        scars_dir = case_dir / "scars"
        scars_dir.mkdir(exist_ok=True)
        for old in scars_dir.glob("scar_*.json"):
            old.unlink()

        results: list[dict[str, Any]] = []
        for i in range(1, n_passes + 1):
            results.append(
                run_pass(i, baseline_path=baseline_path, scars_dir=scars_dir, quiet=quiet)
            )
        last = results[-1]
        scar_fired = any(r.get("scar_written") for r in results)
        output = {
            "id": example["id"],
            "label": example.get("label", ""),
            "baseline_score": baseline_score,
            "baseline_drc_ok": baseline_drc_ok,
            "score": last["score"],
            "drc_ok": last["drc_ok"],
            "gates_ok": last["gates_ok"],
            "drc_count": len(last.get("drc_issues") or []),
            "scar_written": next((r["scar_written"] for r in results if r.get("scar_written")), None),
            "scar_applied": any(r.get("scars_applied") for r in results),
            "scar_should_fire_actual": bool(scar_fired),
            "score_improved": float(last["score"]) < float(baseline_score),
            "passes": [
                {
                    "pass": r["pass"],
                    "score": r["score"],
                    "drc_ok": r["drc_ok"],
                    "gates_ok": r["gates_ok"],
                    "scar_written": r.get("scar_written"),
                    "signals": r.get("signals") or {},
                }
                for r in results
            ],
            "policy_version": last.get("policy_version"),
        }
        output["signals"] = score_online_signals(output)
        return output
    finally:
        if own_tmp is not None:
            own_tmp.cleanup()


def _score_row(output: dict[str, Any], expected: dict[str, Any]) -> dict[str, Any]:
    scores = match_dataset_expected(output, expected)
    scores.update(output.get("signals") or score_online_signals(output))
    scores["passed"] = row_passed(scores)
    return scores


def run_eval(
    *,
    dataset_dir: Path | str | None = None,
    n_passes: int = 3,
    weave_project: str | None = None,
    enable_weave: bool | None = None,
    tracer: WeaveTracer | None = None,
    work_dir: Path | None = None,
    quiet: bool = True,
) -> dict[str, Any]:
    examples = load_dataset(dataset_dir)
    token = init_tracer(
        project=weave_project,
        enable=enable_weave,
        tracer=tracer,
        announce=tracer is None,
    )
    bound = get_tracer()
    tmp: tempfile.TemporaryDirectory[str] | None = None
    if work_dir is None:
        tmp = tempfile.TemporaryDirectory(prefix="copper-scar-eval-")
        work_dir = Path(tmp.name)
    try:
        rows, weave_summary = _run_eval_body(
            examples,
            n_passes=n_passes,
            work_dir=Path(work_dir),
            tracer=bound,
            quiet=quiet,
        )
        passed = sum(1 for r in rows if r["scores"]["passed"])
        lines = _format_table(rows, bound)
        print("\n".join(lines))
        if bound.enabled and bound.ui_url:
            print(f"\nWeave UI: {bound.ui_url}")
            print("Evaluations: open Evaluations → copper-scar-loop-eval")
            print("Signals: Traces → Scores, or Monitors → attach scorers (see README)")
        return {
            "rows": rows,
            "n_passed": passed,
            "n_total": len(rows),
            "all_passed": passed == len(rows),
            "summary_lines": lines,
            "weave_enabled": bound.enabled,
            "weave_project": bound.project if bound.enabled else None,
            "weave_url": bound.ui_url if bound.enabled else None,
            "weave_evaluation": weave_summary,
            "dataset_dir": str(resolve_dataset_dir(dataset_dir)),
        }
    finally:
        bound.finish()
        reset_tracer(token)
        if tmp is not None:
            tmp.cleanup()


def _run_eval_body(
    examples: list[dict[str, Any]],
    *,
    n_passes: int,
    work_dir: Path,
    tracer: WeaveTracer,
    quiet: bool,
) -> tuple[list[dict[str, Any]], dict[str, Any] | None]:
    weave_summary = None
    if tracer.enabled:
        try:
            weave_summary, rows = _run_weave_evaluation(examples, n_passes, work_dir, quiet)
            return rows, weave_summary
        except Exception as exc:
            print(f"copper-scar weave: Evaluation failed ({exc}); running offline scorers", flush=True)

    rows = []
    for example in examples:
        output = run_example(example, n_passes=n_passes, work_dir=work_dir, quiet=quiet)
        scores = _score_row(output, example["expected"])
        rows.append({"example": example, "output": output, "scores": scores})
    return rows, weave_summary


def _run_weave_evaluation(
    examples: list[dict[str, Any]],
    n_passes: int,
    work_dir: Path,
    quiet: bool,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    from copper_scar.eval.scorers import weave_eval_scorers
    from copper_scar.loop.weave_trace import import_weave

    weave = import_weave()
    local_outputs: dict[str, dict[str, Any]] = {}

    def predict(id: str, board: dict, expected: dict, label: str = "") -> dict[str, Any]:
        example = {"id": id, "board": board, "expected": expected, "label": label}
        output = run_example(example, n_passes=n_passes, work_dir=work_dir, quiet=quiet)
        local_outputs[id] = output
        return output

    predict_op = weave.op(name=OP_AGENT)(predict)
    dataset = weave.Dataset(name="copper-scar-boards", rows=examples)
    evaluation = weave.Evaluation(
        name="copper-scar-loop-eval",
        dataset=dataset,
        scorers=weave_eval_scorers(),
    )
    evaluate = evaluation.evaluate
    result = evaluate(predict_op)
    if asyncio.iscoroutine(result) or asyncio.isfuture(result):
        result = asyncio.run(result)

    rows = []
    for example in examples:
        output = local_outputs.get(example["id"]) or run_example(
            example, n_passes=n_passes, work_dir=work_dir, quiet=quiet
        )
        scores = _score_row(output, example["expected"])
        rows.append({"example": example, "output": output, "scores": scores})
    return {"result": result}, rows


def _format_table(rows: list[dict[str, Any]], tracer: WeaveTracer) -> list[str]:
    header = (
        f"{'id':<20} {'pass':>5} {'base':>10} {'score':>10} "
        f"{'drc':>5} {'scar':>5} {'ok':>5}"
    )
    lines = [
        "Copper Scar — dataset eval",
        f"dataset: {len(rows)} fixtures  weave: {'ON' if tracer.enabled else 'OFF'}",
        "",
        header,
        "-" * len(header),
    ]
    for row in rows:
        out = row["output"]
        scores = row["scores"]
        lines.append(
            f"{str(out['id'])[:20]:<20} "
            f"{'OK' if scores['passed'] else 'FAIL':>5} "
            f"{out['baseline_score']:>10.1f} "
            f"{out['score']:>10.1f} "
            f"{'Y' if out['drc_ok'] else 'n':>5} "
            f"{'Y' if out['scar_should_fire_actual'] else 'n':>5} "
            f"{'Y' if scores['passed'] else 'n':>5}"
        )
    n_ok = sum(1 for r in rows if r["scores"]["passed"])
    lines.append("")
    lines.append(f"{n_ok}/{len(rows)} fixtures passed dataset expectations")
    return lines


def run_eval_cli(args: Any) -> int:
    enable_weave = False if getattr(args, "no_weave", False) else None
    result = run_eval(
        dataset_dir=getattr(args, "dataset", None),
        n_passes=getattr(args, "passes", 3),
        weave_project=getattr(args, "weave_project", None),
        enable_weave=enable_weave,
        work_dir=Path(args.out_dir) if getattr(args, "out_dir", None) else None,
    )
    return 0 if result["all_passed"] else 1
