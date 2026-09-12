"""CI defaults: never open a live Weave session unless explicitly requested."""

from __future__ import annotations

import os

import pytest


@pytest.fixture(autouse=True)
def _no_live_weave(monkeypatch: pytest.MonkeyPatch) -> None:
    if os.environ.get("COPPER_SCAR_TEST_LIVE_WEAVE") == "1":
        return
    monkeypatch.delenv("WANDB_API_KEY", raising=False)
    monkeypatch.delenv("WEAVE_API_KEY", raising=False)
