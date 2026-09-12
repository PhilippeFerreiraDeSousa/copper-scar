"""Optional Weave tracer: no-op offline, named spans when a client is injected."""

from __future__ import annotations

from pathlib import Path

import pytest

from copper_scar.loop.run import run_demo, run_pass
from copper_scar.loop.weave_trace import (
    ATTR_KEYS,
    POLICY_VERSION,
    SPAN_ACT,
    SPAN_ACT_APPLY_SCAR,
    SPAN_ACT_PLAN,
    SPAN_EVALUATE,
    SPAN_EVAL_DRC,
    SPAN_EVAL_GATES,
    SPAN_EVAL_SCORE,
    SPAN_IMPROVE,
    SPAN_IMPROVE_WRITE,
    SPAN_OBSERVE,
    SPAN_OBSERVE_LOAD,
    WeaveTracer,
    get_tracer,
    import_weave,
    init_tracer,
    reset_tracer,
    resolve_project,
    tracing_requested,
)


class FakeCall:
    def __init__(self, op: str, inputs: dict, attributes: dict | None) -> None:
        self.op = op
        self.inputs = inputs
        self.attributes = dict(attributes or {})
        self.summary: dict = {}
        self.output = None
        self.exception = None
        self.scorers: list = []

    def apply_scorer(self, scorer, additional_output=None):
        self.scorers.append(scorer)
        return {"ok": True}


class FakeClient:
    def __init__(self) -> None:
        self.entity = "demo"
        self.project = "copper-scar"
        self.created: list[FakeCall] = []
        self.finished: list[FakeCall] = []

    def create_call(self, op, inputs, parent=None, attributes=None, display_name=None, use_stack=True):
        call = FakeCall(str(op), inputs, attributes)
        self.created.append(call)
        return call

    def finish_call(self, call, output=None, exception=None):
        call.output = output
        call.exception = exception
        self.finished.append(call)

    def flush(self) -> None:
        return None


def test_disabled_without_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("WANDB_API_KEY", raising=False)
    assert tracing_requested(None) is False
    tracer = WeaveTracer.maybe_init(project="copper-scar")
    assert tracer.enabled is False
    with tracer.span("loop.pass.1") as handle:
        handle.set_output({"ok": True})
        assert handle.call is None


def test_missing_weave_extra_does_not_crash(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("WANDB_API_KEY", "test-key")

    def _boom() -> None:
        raise ImportError("no weave")

    monkeypatch.setattr("copper_scar.loop.weave_trace.import_weave", _boom)
    tracer = WeaveTracer.maybe_init(project="copper-scar", enable=True)
    assert tracer.enabled is False


def test_resolve_project_default() -> None:
    assert resolve_project(None) == "copper-scar"


def test_import_weave_is_optional() -> None:
    try:
        import_weave()
    except ImportError:
        pytest.skip("weave extra not installed")


def test_demo_offline_has_no_weave_banner(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    baseline = Path(__file__).resolve().parents[1] / "baselines" / "stock.json"
    demo = run_demo(
        n_passes=3,
        baseline_path=baseline,
        scars_dir=tmp_path / "scars",
        out_dir=tmp_path / "out",
        enable_weave=False,
    )
    assert demo["weave_enabled"] is False
    out = capsys.readouterr().out
    assert "Weave tracing enabled" not in out
    assert "[loop.pass.1] observe.load" in out
    assert "[loop.pass.1] evaluate.score" in out


def test_injected_client_records_required_span_names(tmp_path: Path) -> None:
    baseline = Path(__file__).resolve().parents[1] / "baselines" / "stock.json"
    client = FakeClient()
    tracer = WeaveTracer.from_client(client, project="copper-scar")
    token = init_tracer(tracer=tracer)
    try:
        r1 = run_pass(1, baseline_path=baseline, scars_dir=tmp_path / "scars", quiet=True)
        r2 = run_pass(2, baseline_path=baseline, scars_dir=tmp_path / "scars", quiet=True)
    finally:
        tracer.finish()
        reset_tracer(token)

    names = [c.op for c in client.created]
    assert "loop.pass.1" in names
    assert "loop.pass.2" in names
    for required in (
        SPAN_OBSERVE,
        SPAN_OBSERVE_LOAD,
        SPAN_ACT,
        SPAN_ACT_PLAN,
        SPAN_ACT_APPLY_SCAR,
        SPAN_EVALUATE,
        SPAN_EVAL_DRC,
        SPAN_EVAL_GATES,
        SPAN_EVAL_SCORE,
        SPAN_IMPROVE,
        SPAN_IMPROVE_WRITE,
    ):
        assert required in names, f"missing span {required} in {names}"

    pass1 = next(c for c in client.finished if c.op == "loop.pass.1")
    assert pass1.output is not None
    for key in ATTR_KEYS:
        assert key in pass1.output, f"missing attribute {key}"
    assert pass1.output["policy_version"] == POLICY_VERSION
    assert r1["score"] == pass1.output["score"]
    assert r2["plan"] == ["plan=apply_scars+tight_shrink"]
    assert get_tracer().enabled is False
