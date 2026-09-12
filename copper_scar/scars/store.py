"""Scar store: load/save scar JSON documents under a directory."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from copper_scar.harness.score import compute_score


def default_scars_dir() -> Path:
    return Path(__file__).resolve().parent / "examples"


def load_scar(path: Path | str) -> dict[str, Any]:
    p = Path(path)
    with p.open(encoding="utf-8") as f:
        return json.load(f)


def save_scar(scar: dict[str, Any], path: Path | str) -> Path:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    # Ensure score matches metrics when present
    m = scar.get("metrics")
    if m and all(k in m for k in ("volume_mm3", "vias", "copper_layers")):
        scar = {**scar, "score": compute_score(m["volume_mm3"], m["vias"], m["copper_layers"])}
    with p.open("w", encoding="utf-8") as f:
        json.dump(scar, f, indent=2, sort_keys=False)
        f.write("\n")
    return p


def list_scars(directory: Path | str | None = None) -> list[Path]:
    d = Path(directory) if directory else default_scars_dir()
    if not d.is_dir():
        return []
    return sorted(d.glob("scar_*.json"))
