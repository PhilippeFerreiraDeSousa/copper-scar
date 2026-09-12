"""Stub agent loop: writes a scar JSON (no real EDA yet)."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from copper_scar.harness.gates import evaluate_gates
from copper_scar.harness.score import compute_score
from copper_scar.scars.store import save_scar


def run_loop(
    *,
    scar_id: str = "scar_000",
    metrics: dict[str, Any] | None = None,
    gate_flags: dict[str, bool] | None = None,
    out_dir: Path | str | None = None,
    label: str = "stub loop run",
) -> Path:
    """Execute a stub loop and persist a scar document.

    Metrics default to PLACEHOLDER values matching the unit-test fixture
    (1000 mm³, 10 vias, 4 layers → score 21500).
    """
    metrics = metrics or {
        "volume_mm3": 1000.0,
        "vias": 10,
        "copper_layers": 4,
    }
    gate_flags = gate_flags or {}
    report = evaluate_gates(gate_flags)
    score = compute_score(metrics["volume_mm3"], metrics["vias"], metrics["copper_layers"])

    scar: dict[str, Any] = {
        "scar_id": scar_id,
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "label": label,
        "placeholder": True,
        "metrics": metrics,
        "score": score,
        "gates": {r.name: r.passed for r in report.results},
        "gates_ok": report.ok,
        "weave": {
            "project": "copper-scar",
            "run_id": f"stub-{scar_id}",
            "span_ids": ["plan", "place", "route", "gates", "score", "scar_write"],
        },
        "tools_used": [],
        "notes": "Stub loop — PLACEHOLDER metrics; replace with real EDA outputs.",
    }

    out = Path(out_dir) if out_dir else Path.cwd() / "scars_out"
    path = out / f"{scar_id}.json"
    return save_scar(scar, path)


def run_loop_cli(args: Any) -> int:
    path = run_loop(
        scar_id=args.scar_id,
        out_dir=args.out_dir,
        label=args.label,
    )
    print(json.dumps({"wrote": str(path), "scar_id": args.scar_id}, indent=2))
    return 0
