"""Built eval dataset + offline scorers (Weave Evaluation is mocked / skipped)."""

from __future__ import annotations

from pathlib import Path

import pytest

from copper_scar.eval.dataset import load_dataset
from copper_scar.eval.run import run_eval, run_example
from copper_scar.eval.scorers import (
    match_dataset_expected,
    row_passed,
    score_improves_vs_baseline,
    score_online_signals,
)
from copper_scar.harness.score import compute_score
from copper_scar.sim.board import BoardState


def test_dataset_has_required_fixtures() -> None:
    rows = load_dataset()
    assert len(rows) >= 5
    ids = {r["id"] for r in rows}
    for required in ("overlap", "clearance", "clean", "fat_outline", "via_heavy"):
        assert required in ids
    for row in rows:
        assert "board" in row and "expected" in row
        board = BoardState.from_dict(row["board"])
        assert board.width > 0 and board.parts
        exp = row["expected"]
        assert "drc_ok" in exp
        assert "score_upper_bound" in exp
        assert "scar_should_fire" in exp


def test_online_signal_helpers() -> None:
    improved = score_improves_vs_baseline({"baseline_score": 20000, "score": 15000})
    assert improved["score_improves_vs_baseline"] is True
    assert improved["delta"] == 5000
    signals = score_online_signals(
        {"baseline_score": 20000, "score": 15000, "scar_applied": True, "gates_ok": True, "drc_ok": True}
    )
    assert signals["gates_ok_when_scar_applied"] is True
    assert signals["drc_cleared_after_scar"] is True


def test_match_dataset_expected() -> None:
    scores = match_dataset_expected(
        {
            "score": 1000,
            "baseline_score": 2000,
            "drc_ok": True,
            "scar_should_fire_actual": True,
            "score_improved": True,
        },
        {"drc_ok": True, "score_upper_bound": 1500, "scar_should_fire": True, "score_should_improve": True},
    )
    assert row_passed(scores)


def test_eval_offline_passes(tmp_path: Path) -> None:
    result = run_eval(
        n_passes=3,
        enable_weave=False,
        work_dir=tmp_path,
        quiet=True,
    )
    assert result["weave_enabled"] is False
    assert result["n_total"] >= 5
    assert result["all_passed"], [
        (r["output"]["id"], r["scores"], r["output"]) for r in result["rows"] if not r["scores"]["passed"]
    ]


def test_clean_fixture_does_not_write_scar(tmp_path: Path) -> None:
    rows = {r["id"]: r for r in load_dataset()}
    out = run_example(rows["clean"], n_passes=2, work_dir=tmp_path, quiet=True)
    assert out["drc_ok"] is True
    assert out["scar_should_fire_actual"] is False


def test_cli_has_eval_command() -> None:
    from copper_scar.cli import build_parser

    parser = build_parser()
    args = parser.parse_args(["eval", "--no-weave", "--passes", "3"])
    assert args.command == "eval"
    assert args.no_weave is True


def test_overlap_fixture_writes_scar_and_keeps_official_formula(tmp_path: Path) -> None:
    rows = {r["id"]: r for r in load_dataset()}
    out = run_example(rows["overlap"], n_passes=2, work_dir=tmp_path, quiet=True)
    assert out["scar_should_fire_actual"] is True
    board = BoardState.from_dict(rows["overlap"]["board"])
    m = board.metrics()
    assert board.official_score() == compute_score(m["volume_mm3"], m["vias"], m["copper_layers"])
    assert out["baseline_score"] == board.official_score()
