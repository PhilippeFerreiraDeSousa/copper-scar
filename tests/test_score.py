"""Official score formula regression + sim/scar/demo tests."""

from __future__ import annotations

import json
from pathlib import Path


from copper_scar.harness.score import compute_score, score_from_metrics
from copper_scar.loop.run import run_demo, run_pass
from copper_scar.sim.board import BoardState, Part


def test_compute_score_fixture():
    # volume_mm3 + 50*vias + 5000*copper_layers
    # 1000 + 50*10 + 5000*4 = 1000 + 500 + 20000 = 21500
    assert compute_score(1000, 10, 4) == 21500


def test_score_from_metrics():
    assert score_from_metrics({"volume_mm3": 1000, "vias": 10, "copper_layers": 4}) == 21500


def test_volume_and_score_from_board():
    board = BoardState(
        width=10,
        height=10,
        thickness_mm=1.0,
        parts=[],
        vias=10,
        layers=4,
    )
    assert board.volume_mm3() == 100.0
    # 100 + 500 + 20000 = 20600
    assert board.official_score() == 20600.0


def test_drc_detects_overlap():
    board = BoardState(
        width=40,
        height=40,
        thickness_mm=1.6,
        parts=[
            Part("U1", 5, 5, 10, 10),
            Part("U2", 10, 8, 10, 10),
        ],
        vias=0,
        layers=2,
    )
    issues = board.check_drc()
    assert any(i.startswith("overlap:") for i in issues)


def test_drc_clearance():
    board = BoardState(
        width=40,
        height=40,
        thickness_mm=1.6,
        parts=[
            Part("U1", 0, 0, 5, 5),
            Part("U2", 5.2, 0, 5, 5),  # gap 0.2 < 0.5
        ],
        vias=0,
        layers=2,
    )
    issues = board.check_drc(min_clearance=0.5)
    assert any(i.startswith("clearance:") for i in issues)


def test_scar_applied_changes_plan_or_positions(tmp_path: Path):
    baseline = {
        "width": 50.0,
        "height": 40.0,
        "thickness_mm": 1.6,
        "vias": 10,
        "layers": 4,
        "parts": [
            {"ref": "U1", "x": 5.0, "y": 5.0, "w": 10.0, "h": 8.0},
            {"ref": "U2", "x": 12.0, "y": 7.0, "w": 10.0, "h": 8.0},
        ],
        "drc_issues": [],
        "label": "test",
    }
    bpath = tmp_path / "stock.json"
    bpath.write_text(json.dumps(baseline), encoding="utf-8")
    scars_dir = tmp_path / "scars"
    scars_dir.mkdir()

    r1 = run_pass(1, baseline_path=bpath, scars_dir=scars_dir)
    assert r1["plan"] == ["plan=heuristics_only"]
    assert r1["scar_written"] is not None
    pos1 = {p.ref: (p.x, p.y) for p in r1["board"].parts}

    r2 = run_pass(2, baseline_path=bpath, scars_dir=scars_dir)
    assert r2["plan"] == ["plan=apply_scars+tight_shrink"]
    assert r2["scars_applied"]
    pos2 = {p.ref: (p.x, p.y) for p in r2["board"].parts}
    assert pos1 != pos2 or r1["board"].width != r2["board"].width


def test_demo_improves_or_clears_drc(tmp_path: Path):
    baseline = Path(__file__).resolve().parents[1] / "baselines" / "stock.json"
    out = tmp_path / "out"
    scars = tmp_path / "scars"
    demo = run_demo(
        n_passes=3,
        baseline_path=baseline,
        scars_dir=scars,
        out_dir=out,
        seed=0,
    )
    results = demo["results"]
    assert len(results) == 3
    assert (out / "pass_timeline.txt").is_file()
    assert (out / "board_pass_1.svg").is_file()
    assert (out / "board_pass_2.svg").is_file()
    assert (out / "board_pass_3.svg").is_file()

    # Pass 1 starts dirty; later pass clears DRC or improves score
    assert results[0]["drc_ok"] is False or results[0]["gates_ok"] is False
    later = results[1:]
    improved = any(r["drc_ok"] for r in later) or any(
        r["score"] < results[0]["score"] for r in later
    )
    assert improved
    # When gates eventually OK, score must be lower than pass 1
    ok_passes = [r for r in results if r["gates_ok"]]
    if ok_passes:
        assert ok_passes[-1]["score"] < results[0]["score"]


def test_stock_baseline_loads():
    root = Path(__file__).resolve().parents[1]
    raw = json.loads((root / "baselines" / "stock.json").read_text(encoding="utf-8"))
    board = BoardState.from_dict(raw)
    assert board.width == 50.0
    issues = board.check_drc()
    assert issues  # stock starts dirty
