"""Offline + live Weave Signals/scorers for Copper Scar traces.

These functions are the source of truth. When Weave is installed they are also
exposed as ``weave.Scorer`` / ``@weave.op`` objects so:

- ``copper-scar eval`` can log a Weave Evaluation
- each ``loop.pass.{i}`` call can be scored online via ``Call.apply_scorer``
- judges can attach the same scorers in Weave → Monitors as a live Signal
"""

from __future__ import annotations

from typing import Any

SIGNAL_SCORE_IMPROVES = "score_improves_vs_baseline"
SIGNAL_GATES_WHEN_SCAR = "gates_ok_when_scar_applied"
SIGNAL_DRC_AFTER_SCAR = "drc_cleared_after_scar"

# Prompt for the optional UI Signal (Serverless Inference / W&B Inference credits).
SIGNAL_UI_PROMPT = """You are scoring a Copper Scar PCB agent pass.

Inputs include official PCBGolf metrics. Lower score is better.
{output}

Return JSON:
- score_improves: true if output.score < output.baseline_score
- gates_ok_when_scar_applied: true if no scar was applied, OR gates_ok is true
- drc_cleared_after_scar: true if no scar was applied, OR drc_ok is true
- reasoning: one sentence
"""


def score_improves_vs_baseline(output: dict[str, Any] | None) -> dict[str, Any]:
    payload = output or {}
    baseline = payload.get("baseline_score")
    score = payload.get("score")
    if baseline is None or score is None:
        return {SIGNAL_SCORE_IMPROVES: False, "delta": None, "applicable": False}
    baseline_f = float(baseline)
    score_f = float(score)
    return {
        SIGNAL_SCORE_IMPROVES: score_f < baseline_f,
        "delta": baseline_f - score_f,
        "applicable": True,
    }


def gates_ok_when_scar_applied(output: dict[str, Any] | None) -> dict[str, Any]:
    payload = output or {}
    applied = bool(payload.get("scar_applied") or payload.get("scars_applied"))
    if not applied:
        return {SIGNAL_GATES_WHEN_SCAR: True, "applicable": False}
    return {SIGNAL_GATES_WHEN_SCAR: bool(payload.get("gates_ok")), "applicable": True}


def drc_cleared_after_scar(output: dict[str, Any] | None) -> dict[str, Any]:
    payload = output or {}
    applied = bool(payload.get("scar_applied") or payload.get("scars_applied"))
    if not applied:
        return {SIGNAL_DRC_AFTER_SCAR: True, "applicable": False}
    return {SIGNAL_DRC_AFTER_SCAR: bool(payload.get("drc_ok")), "applicable": True}


def score_online_signals(output: dict[str, Any] | None) -> dict[str, Any]:
    """Deterministic live-signal bundle attached to every pass trace."""
    improves = score_improves_vs_baseline(output)
    gates = gates_ok_when_scar_applied(output)
    drc = drc_cleared_after_scar(output)
    return {
        SIGNAL_SCORE_IMPROVES: improves[SIGNAL_SCORE_IMPROVES],
        "score_delta": improves.get("delta"),
        SIGNAL_GATES_WHEN_SCAR: gates[SIGNAL_GATES_WHEN_SCAR],
        SIGNAL_DRC_AFTER_SCAR: drc[SIGNAL_DRC_AFTER_SCAR],
    }


def match_dataset_expected(output: dict[str, Any] | None, expected: dict[str, Any] | None) -> dict[str, Any]:
    payload = output or {}
    exp = expected or {}
    score = payload.get("score")
    upper = exp.get("score_upper_bound")
    scar_fired = bool(
        payload.get("scar_should_fire_actual")
        or payload.get("scar_written")
        or payload.get("scar_applied")
    )
    improved = bool(payload.get("score_improved"))
    if "score_improved" not in payload and score is not None and payload.get("baseline_score") is not None:
        improved = float(score) < float(payload["baseline_score"])
    return {
        "drc_ok_match": bool(payload.get("drc_ok")) == bool(exp.get("drc_ok")),
        "score_within_bound": (score is not None and upper is not None and float(score) <= float(upper)),
        "scar_fire_match": scar_fired == bool(exp.get("scar_should_fire")),
        "score_improve_match": (not exp.get("score_should_improve", False)) or improved,
    }


def row_passed(scores: dict[str, Any]) -> bool:
    return all(
        bool(scores.get(k))
        for k in ("drc_ok_match", "score_within_bound", "scar_fire_match", "score_improve_match")
    )


def weave_eval_scorers() -> list[Any]:
    """Scorers for ``weave.Evaluation`` (requires weave extra)."""
    from copper_scar.loop.weave_trace import import_weave

    weave = import_weave()

    @weave.op(name="copper_scar.eval.match_dataset_expected")
    def _match(output: dict, expected: dict) -> dict:
        return match_dataset_expected(output, expected)

    @weave.op(name=f"copper_scar.signal.{SIGNAL_SCORE_IMPROVES}")
    def _improves(output: dict) -> dict:
        return score_improves_vs_baseline(output)

    @weave.op(name=f"copper_scar.signal.{SIGNAL_GATES_WHEN_SCAR}")
    def _gates(output: dict) -> dict:
        return gates_ok_when_scar_applied(output)

    @weave.op(name=f"copper_scar.signal.{SIGNAL_DRC_AFTER_SCAR}")
    def _drc(output: dict) -> dict:
        return drc_cleared_after_scar(output)

    return [_match, _improves, _gates, _drc]


def weave_signal_scorers() -> list[Any]:
    """Class-based scorers for ``Call.apply_scorer`` / Weave Monitors."""
    from copper_scar.loop.weave_trace import import_weave

    weave = import_weave()
    scorer_cls = getattr(weave, "Scorer", None)
    if scorer_cls is None:
        from weave import Scorer as scorer_cls  # type: ignore

    class ScoreImprovesVsBaseline(scorer_cls):  # type: ignore[misc, valid-type]
        @weave.op
        def score(self, output: dict) -> dict:
            payload = output if isinstance(output, dict) else {}
            return score_improves_vs_baseline(payload)

    class GatesOkWhenScarApplied(scorer_cls):  # type: ignore[misc, valid-type]
        @weave.op
        def score(self, output: dict) -> dict:
            payload = output if isinstance(output, dict) else {}
            return gates_ok_when_scar_applied(payload)

    class DrcClearedAfterScar(scorer_cls):  # type: ignore[misc, valid-type]
        @weave.op
        def score(self, output: dict) -> dict:
            payload = output if isinstance(output, dict) else {}
            return drc_cleared_after_scar(payload)

    return [ScoreImprovesVsBaseline(), GatesOkWhenScarApplied(), DrcClearedAfterScar()]
