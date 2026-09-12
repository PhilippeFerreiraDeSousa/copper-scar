"""Load the built Copper Scar BoardState eval dataset."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from copper_scar.sim.board import BoardState

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATASET_DIR = REPO_ROOT / "evals" / "dataset"

REQUIRED_EXPECTED = ("drc_ok", "score_upper_bound", "scar_should_fire")


def resolve_dataset_dir(path: Path | str | None = None) -> Path:
    if path:
        return Path(path)
    if DEFAULT_DATASET_DIR.is_dir():
        return DEFAULT_DATASET_DIR
    return Path.cwd() / "evals" / "dataset"


def load_dataset(path: Path | str | None = None) -> list[dict[str, Any]]:
    """Load fixture JSON files. Each row is Evaluation-ready (id, board, expected, label)."""
    directory = resolve_dataset_dir(path)
    if not directory.is_dir():
        raise FileNotFoundError(f"eval dataset not found: {directory}")
    rows: list[dict[str, Any]] = []
    for file in sorted(directory.glob("*.json")):
        with file.open(encoding="utf-8") as f:
            raw = json.load(f)
        row = normalize_example(raw, source=file)
        rows.append(row)
    if len(rows) < 5:
        raise ValueError(f"eval dataset {directory} must contain at least 5 fixtures")
    return rows


def normalize_example(raw: dict[str, Any], *, source: Path | None = None) -> dict[str, Any]:
    expected = raw.get("expected") or {}
    missing = [k for k in REQUIRED_EXPECTED if k not in expected]
    if missing:
        raise ValueError(f"{source or raw.get('id')}: expected missing {missing}")
    board_raw = raw.get("board") or raw
    board = BoardState.from_dict(board_raw)
    example_id = str(raw.get("id") or (source.stem if source else board.label))
    return {
        "id": example_id,
        "label": str(raw.get("label") or board.label),
        "notes": raw.get("notes") or board.notes,
        "board": board.to_dict(),
        "expected": {
            "drc_ok": bool(expected["drc_ok"]),
            "score_upper_bound": float(expected["score_upper_bound"]),
            "scar_should_fire": bool(expected["scar_should_fire"]),
            "score_should_improve": bool(expected.get("score_should_improve", False)),
        },
    }
