"""Pydantic models for metrics, baselines, and CLI payloads."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, field_validator


class Metrics(BaseModel):
    """PCBGolf-facing metrics used by the official score formula."""

    volume_mm3: float = Field(..., ge=0, description="Board volume in mm³")
    vias: int = Field(..., ge=0, description="Via count")
    copper_layers: int = Field(..., ge=1, description="Copper layer count")

    @field_validator("copper_layers")
    @classmethod
    def layers_reasonable(cls, v: int) -> int:
        if v > 32:
            raise ValueError("copper_layers > 32 is outside typical fab range")
        return v


class BaselineFile(BaseModel):
    """baselines/*.json shape (may be PLACEHOLDER)."""

    label: str
    placeholder: bool = False
    notes: str | None = None
    metrics: Metrics
    gates: dict[str, bool] = Field(default_factory=dict)
    extra: dict[str, Any] = Field(default_factory=dict)


class ScoreOutput(BaseModel):
    score: float
    metrics: Metrics
    formula: str = "volume_mm3 + 50 * vias + 5000 * copper_layers"
    source: str = "https://comma.ai/leaderboard#pcbgolf_challenge"
