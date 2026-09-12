"""Official PCBGolf score (comma.ai leaderboard).

score = volume_mm3 + 50 * vias + 5000 * copper_layers
Source: https://comma.ai/leaderboard#pcbgolf_challenge
"""

from __future__ import annotations


def compute_score(volume_mm3: float, vias: int, copper_layers: int) -> float:
    """Compute the official PCBGolf score.

    Lower is better on the leaderboard; this is the raw objective value.
    """
    return float(volume_mm3) + 50.0 * int(vias) + 5000.0 * int(copper_layers)


def score_from_metrics(metrics: dict) -> float:
    """Score a metrics dict with keys volume_mm3, vias, copper_layers."""
    return compute_score(
        volume_mm3=metrics["volume_mm3"],
        vias=metrics["vias"],
        copper_layers=metrics["copper_layers"],
    )
