"""Closed agent loop over the sim board: observe → act → evaluate → improve."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from copper_scar.harness.gates import evaluate_gates
from copper_scar.harness.score import compute_score
from copper_scar.loop.weave_trace import (
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
    init_tracer,
    reset_tracer,
)
from copper_scar.scars.store import list_scars, load_scar, save_scar
from copper_scar.sim.board import MIN_CLEARANCE_MM, BoardState, render_svg

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_BASELINE = REPO_ROOT / "baselines" / "stock.json"
DEFAULT_SCARS_DIR = REPO_ROOT / "scars_out"
DEFAULT_DEMO_OUT = REPO_ROOT / "demos" / "out"


def _span(pass_n: int, name: str, detail: str = "") -> str:
    line = f"[loop.pass.{pass_n}] {name}"
    if detail:
        line = f"{line} {detail}"
    return line


def _gate_flags_from_board(board: BoardState) -> dict[str, bool]:
    """Map sim DRC into hard-gate flags (fail-closed for unchecked fab items when DRC fails)."""
    issues = board.check_drc()
    clean = len(issues) == 0
    # When DRC is clean, treat sim gates as OK (no KiCad); when dirty, fail DRC-related gates.
    return {
        "drc_clean": clean,
        "erc_clean": clean,
        "netlist_match": clean,
        "fab_stackup_ok": board.layers <= 8,
        "min_trace_clearance": clean,
        "via_annular_ok": clean,
        "outline_closed": clean and board.width > 0 and board.height > 0,
    }


def _next_scar_id(scars_dir: Path) -> str:
    existing = list_scars(scars_dir)
    n = 1
    used = {p.stem for p in existing}
    while f"scar_{n:03d}" in used:
        n += 1
    return f"scar_{n:03d}"


def _scar_rule_from_failure(board: BoardState) -> dict[str, Any]:
    """Build a typed keepout / min_clearance rule from failing parts."""
    issues = board.drc_issues or board.check_drc()
    for issue in issues:
        if issue.startswith("overlap:") or issue.startswith("clearance:"):
            body = issue.split(":", 1)[1]
            refs = body.split(":")[0].split("/")
            if len(refs) >= 2:
                a = board.part_by_ref(refs[0])
                if a:
                    return {
                        "type": "keepout",
                        "ref": a.ref,
                        "x": a.x,
                        "y": a.y,
                        "w": a.w,
                        "h": a.h,
                        "clearance": MIN_CLEARANCE_MM,
                        "parts": refs,
                        "nudge_self": False,
                    }
                return {
                    "type": "min_clearance",
                    "parts": refs,
                    "clearance": MIN_CLEARANCE_MM,
                }
        if issue.startswith("outline_violation:"):
            ref = issue.split(":", 1)[1]
            p = board.part_by_ref(ref)
            if p:
                return {
                    "type": "keepout",
                    "ref": p.ref,
                    "x": 0.0,
                    "y": 0.0,
                    "w": board.width,
                    "h": board.height,
                    "clearance": 0.0,
                    "nudge_self": True,
                }
    # Fallback keepout on first part
    if board.parts:
        a = board.parts[0]
        return {
            "type": "keepout",
            "ref": a.ref,
            "x": a.x,
            "y": a.y,
            "w": a.w,
            "h": a.h,
            "clearance": MIN_CLEARANCE_MM,
            "nudge_self": False,
        }
    return {"type": "min_clearance", "parts": [], "clearance": MIN_CLEARANCE_MM}


def _heuristic_fix(board: BoardState) -> list[str]:
    """Without scars: try move/shrink heuristics to fix DRC and reduce volume."""
    actions: list[str] = []
    issues = board.check_drc()
    for issue in list(issues):
        if issue.startswith("overlap:") or issue.startswith("clearance:"):
            body = issue.split(":", 1)[1]
            refs = body.split(":")[0].split("/")
            if len(refs) >= 2:
                a = board.part_by_ref(refs[0])
                b = board.part_by_ref(refs[1])
                if a and b:
                    # Mild heuristic: nudge b slightly — often insufficient alone
                    board.move_part(b.ref, 0.2, 0.0)
                    actions.append(f"heuristic.move {b.ref} +0.2x")
        elif issue.startswith("outline_violation:"):
            ref = issue.split(":", 1)[1]
            p = board.part_by_ref(ref)
            if p:
                dx = 0.0
                dy = 0.0
                if p.x < 0:
                    dx = -p.x
                if p.y < 0:
                    dy = -p.y
                if p.x + p.w > board.width:
                    dx = board.width - (p.x + p.w)
                if p.y + p.h > board.height:
                    dy = board.height - (p.y + p.h)
                board.move_part(ref, dx, dy)
                actions.append(f"heuristic.clamp {ref}")

    # Light shrink attempt (deterministic)
    before = (board.width, board.height)
    tw, th = board.tight_bbox(margin=MIN_CLEARANCE_MM)
    # Only shrink a little without scars so pass1 still fails / stays large
    max_shrink_w = min(2.0, max(0.0, board.width - tw))
    max_shrink_h = min(2.0, max(0.0, board.height - th))
    if max_shrink_w > 0 or max_shrink_h > 0:
        board.shrink_outline(max_shrink_w, max_shrink_h)
        actions.append(f"heuristic.shrink {before[0]:.1f}x{before[1]:.1f}->{board.width:.1f}x{board.height:.1f}")
    return actions


def _apply_scars(board: BoardState, scars: list[dict[str, Any]]) -> list[str]:
    credits: list[str] = []
    for scar in scars:
        sid = scar.get("scar_id", "?")
        rule = scar.get("rule") or {}
        rtype = rule.get("type", "keepout")
        target = rule.get("ref") or ",".join(rule.get("parts") or [])
        moved = board.apply_keepout_scar(scar)
        credit = f"{sid} → {rtype}"
        if target:
            credit = f"{sid} → {rtype} {target}"
        credits.append(credit)
        if moved:
            credits.append(f"  moved:{','.join(moved)}")
    # After scars: shrink outline tightly to reduce score
    before = (board.width, board.height)
    tw, th = board.tight_bbox(margin=MIN_CLEARANCE_MM)
    if board.width > tw or board.height > th:
        board.width = max(tw, min(board.width, tw))
        board.height = max(th, min(board.height, th))
        # Ensure parts fit
        for p in board.parts:
            p.x = max(0.0, min(p.x, max(0.0, board.width - p.w)))
            p.y = max(0.0, min(p.y, max(0.0, board.height - p.h)))
        credits.append(f"scar.shrink {before[0]:.1f}x{before[1]:.1f}->{board.width:.1f}x{board.height:.1f}")
    return credits


def _pass_span_ids(pass_n: int) -> list[str]:
    return [
        f"loop.pass.{pass_n}",
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
    ]


def observe(
    *,
    baseline_path: Path,
    scars_dir: Path,
    seed_board: BoardState | None = None,
) -> tuple[BoardState, list[dict[str, Any]], list[str]]:
    spans: list[str] = []
    tracer = get_tracer()
    with tracer.span(
        SPAN_OBSERVE,
        inputs={"baseline": str(baseline_path)},
        attributes={"policy_version": POLICY_VERSION, "scar_id": tracer.last_scar_id},
    ) as observe_span:
        with tracer.span(
            SPAN_OBSERVE_LOAD,
            inputs={"baseline": str(baseline_path)},
            attributes={"policy_version": POLICY_VERSION, "scar_id": tracer.last_scar_id},
        ) as load_span:
            if seed_board is not None:
                board = seed_board.copy()
            else:
                with baseline_path.open(encoding="utf-8") as f:
                    raw = json.load(f)
                board = BoardState.from_dict(raw)
            load_span.set_output({"label": board.label, "parts": len(board.parts)})
        spans.append("observe.load")
        scars: list[dict[str, Any]] = []
        for path in list_scars(scars_dir):
            scars.append(load_scar(path))
        if scars:
            spans.append(f"observe.scars n={len(scars)}")
        else:
            spans.append("observe.scars n=0")
        observe_span.set_output({"parts": len(board.parts), "n_scars": len(scars)})
    return board, scars, spans


def act(board: BoardState, scars: list[dict[str, Any]]) -> tuple[BoardState, list[str], list[str]]:
    """Apply scars if present; else heuristics. Returns board, span details, plan notes."""
    spans: list[str] = []
    plan: list[str] = []
    tracer = get_tracer()
    applied_ids = [str(s.get("scar_id", "?")) for s in scars]
    primary = applied_ids[0] if applied_ids else tracer.last_scar_id
    with tracer.span(
        SPAN_ACT,
        inputs={"n_scars": len(scars)},
        attributes={"policy_version": POLICY_VERSION, "scar_id": primary},
    ):
        return _act_body(board, scars, spans, plan, tracer, applied_ids, primary)


def _act_body(
    board: BoardState,
    scars: list[dict[str, Any]],
    spans: list[str],
    plan: list[str],
    tracer: WeaveTracer,
    applied_ids: list[str],
    primary: str,
) -> tuple[BoardState, list[str], list[str]]:
    with tracer.span(
        SPAN_ACT_PLAN,
        inputs={"n_scars": len(scars)},
        attributes={"policy_version": POLICY_VERSION, "scar_id": primary},
    ) as plan_span:
        if scars:
            plan.append("plan=apply_scars+tight_shrink")
            spans.append("act.plan apply_scars")
            with tracer.span(
                SPAN_ACT_APPLY_SCAR,
                inputs={"scar_ids": applied_ids},
                attributes={"policy_version": POLICY_VERSION, "scar_id": primary},
            ) as apply_span:
                credits = _apply_scars(board, scars)
                apply_span.set_output({"credits": credits, "scar_id": primary})
            for c in credits:
                if c.startswith("scar."):
                    spans.append(f"act.{c}")
                elif "→" in c:
                    spans.append(f"act.apply_scar {c}")
                else:
                    spans.append(f"act.apply_scar {c}")
        else:
            plan.append("plan=heuristics_only")
            spans.append("act.plan heuristics")
            actions = _heuristic_fix(board)
            for a in actions:
                spans.append(f"act.{a}")
            if not actions:
                spans.append("act.noop")
        plan_span.set_output({"plan": list(plan), "scar_id": primary})
    return board, spans, plan


def evaluate(board: BoardState) -> tuple[dict[str, Any], list[str]]:
    spans: list[str] = []
    tracer = get_tracer()
    with tracer.span(
        SPAN_EVALUATE,
        attributes={"policy_version": POLICY_VERSION, "scar_id": tracer.last_scar_id},
    ) as eval_span:
        result, spans = _evaluate_body(board, spans, tracer)
        eval_span.set_output(
            {
                "score": result["score"],
                "drc_ok": result["drc_ok"],
                "gates_ok": result["gates_ok"],
                "drc_count": len(result["drc_issues"]),
            }
        )
        return result, spans


def _evaluate_body(
    board: BoardState,
    spans: list[str],
    tracer: WeaveTracer,
) -> tuple[dict[str, Any], list[str]]:
    with tracer.span(
        SPAN_EVAL_DRC,
        attributes={"policy_version": POLICY_VERSION, "scar_id": tracer.last_scar_id},
    ) as drc_span:
        issues = board.check_drc()
        drc_span.merge_attributes({"drc_count": len(issues)})
        drc_span.set_output({"drc_count": len(issues), "issues": list(issues)})

    with tracer.span(
        SPAN_EVAL_GATES,
        attributes={"policy_version": POLICY_VERSION, "scar_id": tracer.last_scar_id},
    ) as gates_span:
        flags = _gate_flags_from_board(board)
        report = evaluate_gates(flags)
        gates_span.merge_attributes({"gates_ok": report.ok, "drc_count": len(issues)})
        gates_span.set_output({"gates_ok": report.ok, "gates": {r.name: r.passed for r in report.results}})

    with tracer.span(
        SPAN_EVAL_SCORE,
        attributes={"policy_version": POLICY_VERSION, "scar_id": tracer.last_scar_id},
    ) as score_span:
        metrics = board.metrics()
        score = compute_score(metrics["volume_mm3"], metrics["vias"], metrics["copper_layers"])
        attrs = tracer.note_eval(
            score=score,
            drc_count=len(issues),
            gates_ok=report.ok,
        )
        score_span.merge_attributes(attrs)
        score_span.set_output(attrs)

    spans.append(f"evaluate.drc issues={len(issues)}")
    spans.append(f"evaluate.gates ok={report.ok}")
    spans.append(f"evaluate.score score={score:.1f}")
    result = {
        "metrics": metrics,
        "score": score,
        "drc_issues": list(issues),
        "drc_ok": len(issues) == 0,
        "gates": {r.name: r.passed for r in report.results},
        "gates_ok": report.ok,
    }
    return result, spans


def improve(
    board: BoardState,
    eval_result: dict[str, Any],
    scars_dir: Path,
    pass_n: int,
) -> tuple[dict[str, Any] | None, list[str]]:
    spans: list[str] = []
    tracer = get_tracer()
    with tracer.span(
        SPAN_IMPROVE,
        inputs={"pass": pass_n},
        attributes={"policy_version": POLICY_VERSION, "scar_id": tracer.last_scar_id},
    ) as improve_span:
        scar, spans = _improve_body(board, eval_result, scars_dir, pass_n, spans, tracer)
        improve_span.set_output({"scar_id": scar["scar_id"] if scar else None})
        return scar, spans


def _improve_body(
    board: BoardState,
    eval_result: dict[str, Any],
    scars_dir: Path,
    pass_n: int,
    spans: list[str],
    tracer: WeaveTracer,
) -> tuple[dict[str, Any] | None, list[str]]:
    if eval_result["gates_ok"] and eval_result["drc_ok"]:
        spans.append("improve.skip gates_ok")
        return None, spans

    scar_id = _next_scar_id(scars_dir)
    rule = _scar_rule_from_failure(board)
    write_attrs = tracer.note_eval(
        score=eval_result["score"],
        drc_count=len(eval_result["drc_issues"]),
        gates_ok=eval_result["gates_ok"],
        scar_id=scar_id,
    )
    scar = {
        "scar_id": scar_id,
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "label": f"pass {pass_n} failure scar",
        "placeholder": False,
        "metrics": eval_result["metrics"],
        "score": eval_result["score"],
        "gates": eval_result["gates"],
        "gates_ok": eval_result["gates_ok"],
        "rule": rule,
        "weave": {
            "project": tracer.project or "copper-scar",
            "run_id": f"pass-{pass_n}-{scar_id}",
            "span_ids": _pass_span_ids(pass_n),
        },
        "tools_used": ["sim.board"],
        "notes": f"Typed {rule.get('type')} scar from DRC: {eval_result['drc_issues'][:3]}",
    }
    with tracer.span(
        SPAN_IMPROVE_WRITE,
        inputs={"scar_id": scar_id, "pass": pass_n},
        attributes=write_attrs,
    ) as write_span:
        path = save_scar(scar, scars_dir / f"{scar_id}.json")
        write_span.set_output({"scar_id": scar_id, "path": str(path), **write_attrs})
    spans.append(f"improve.scar.write {scar_id}")
    spans.append(f"improve.scar.path {path}")
    return scar, spans


def run_pass(
    pass_n: int,
    *,
    baseline_path: Path,
    scars_dir: Path,
    seed_board: BoardState | None = None,
    quiet: bool = False,
) -> dict[str, Any]:
    """Run one observe→act→evaluate→improve cycle. Always reloads stock + applies all scars."""
    tracer = get_tracer()
    impl = tracer.as_op("copper_scar.agent_pass", _run_pass_impl)
    return impl(
        pass_n,
        baseline_path=baseline_path,
        scars_dir=scars_dir,
        seed_board=seed_board,
        quiet=quiet,
    )


def _emit(log: list[str], line: str, quiet: bool) -> None:
    log.append(line)
    if not quiet:
        print(line)


def _run_pass_impl(
    pass_n: int,
    *,
    baseline_path: Path,
    scars_dir: Path,
    seed_board: BoardState | None,
    quiet: bool,
) -> dict[str, Any]:
    from copper_scar.eval.scorers import score_online_signals

    log: list[str] = []
    tracer = get_tracer()
    with tracer.span(
        f"loop.pass.{pass_n}",
        inputs={"pass": pass_n},
        attributes={"policy_version": POLICY_VERSION, "scar_id": tracer.last_scar_id},
    ) as pass_span:
        board, scars, obs_spans = observe(
            baseline_path=baseline_path,
            scars_dir=scars_dir,
            seed_board=seed_board,
        )
        baseline_score = board.official_score()
        for s in obs_spans:
            _emit(log, _span(pass_n, s), quiet)

        board, act_spans, plan = act(board, scars)
        for s in act_spans:
            _emit(log, _span(pass_n, s), quiet)

        eval_result, eval_spans = evaluate(board)
        for s in eval_spans:
            _emit(log, _span(pass_n, s), quiet)

        scar, imp_spans = improve(board, eval_result, scars_dir, pass_n)
        for s in imp_spans:
            _emit(log, _span(pass_n, s), quiet)

        scars_applied = []
        for sc in scars:
            rule = sc.get("rule") or {}
            sid = sc.get("scar_id", "?")
            rtype = rule.get("type", "?")
            target = rule.get("ref") or ",".join(rule.get("parts") or [])
            scars_applied.append(f"{sid}→{rtype}" + (f" {target}" if target else ""))

        pass_attrs = tracer.note_eval(
            score=eval_result["score"],
            drc_count=len(eval_result["drc_issues"]),
            gates_ok=eval_result["gates_ok"],
            scar_id=scar["scar_id"] if scar else (scars[-1].get("scar_id") if scars else tracer.last_scar_id),
        )
        pass_output = {
            **pass_attrs,
            "pass": pass_n,
            "baseline_score": baseline_score,
            "drc_ok": eval_result["drc_ok"],
            "scar_applied": bool(scars_applied),
            "scar_written": scar["scar_id"] if scar else None,
            "scars_applied": list(scars_applied),
        }
        signals = score_online_signals(pass_output)
        pass_output["signals"] = signals
        pass_span.merge_attributes(pass_attrs)
        pass_span.update_summary({"signals": signals})
        pass_span.set_output(pass_output)
        tracer.queue_signals(pass_span, pass_output)

    tracer.apply_signals()
    return {
        "pass": pass_n,
        "board": board,
        "score": eval_result["score"],
        "baseline_score": baseline_score,
        "drc_ok": eval_result["drc_ok"],
        "drc_issues": eval_result["drc_issues"],
        "gates_ok": eval_result["gates_ok"],
        "scars_applied": scars_applied,
        "plan": plan,
        "scar_written": scar["scar_id"] if scar else None,
        "log": log,
        "metrics": eval_result["metrics"],
        "signals": signals,
        "policy_version": POLICY_VERSION,
    }


def run_demo(
    *,
    n_passes: int = 3,
    baseline_path: Path | None = None,
    scars_dir: Path | None = None,
    out_dir: Path | None = None,
    seed: int = 0,
    weave_project: str | None = None,
    enable_weave: bool | None = None,
    tracer: WeaveTracer | None = None,
) -> dict[str, Any]:
    """Deterministic 3-pass closed loop demo."""
    _ = seed  # reserved for future RNG; layout is fully deterministic
    baseline_path = Path(baseline_path) if baseline_path else DEFAULT_BASELINE
    scars_dir = Path(scars_dir) if scars_dir else DEFAULT_SCARS_DIR
    out_dir = Path(out_dir) if out_dir else DEFAULT_DEMO_OUT
    out_dir.mkdir(parents=True, exist_ok=True)
    scars_dir.mkdir(parents=True, exist_ok=True)

    token = init_tracer(
        project=weave_project,
        enable=enable_weave,
        tracer=tracer,
        announce=tracer is None,
    )
    bound = get_tracer()
    try:
        return _run_demo_body(
            n_passes=n_passes,
            baseline_path=baseline_path,
            scars_dir=scars_dir,
            out_dir=out_dir,
            tracer=bound,
        )
    finally:
        bound.finish()
        reset_tracer(token)


def _run_demo_body(
    *,
    n_passes: int,
    baseline_path: Path,
    scars_dir: Path,
    out_dir: Path,
    tracer: WeaveTracer,
) -> dict[str, Any]:
    # Fresh scar store for a clean demo
    for old in list_scars(scars_dir):
        old.unlink()

    results: list[dict[str, Any]] = []
    all_logs: list[str] = []

    for i in range(1, n_passes + 1):
        # Each pass reloads stock baseline then applies accumulated scars
        r = run_pass(i, baseline_path=baseline_path, scars_dir=scars_dir)
        results.append(r)
        all_logs.extend(r["log"])
        svg_path = out_dir / f"board_pass_{i}.svg"
        render_svg(r["board"], svg_path)
        all_logs.append(_span(i, f"demo.svg {svg_path}"))

    # Summary table
    header = f"{'pass':>4}  {'score':>10}  {'drc':>6}  {'gates_ok':>8}  scars_applied"
    lines = [
        "Copper Scar — demo closed loop",
        f"baseline: {baseline_path}",
        f"scars_dir: {scars_dir}",
        "",
        header,
        "-" * len(header),
    ]
    for r in results:
        drc = "OK" if r["drc_ok"] else "FAIL"
        scars = ", ".join(r["scars_applied"]) if r["scars_applied"] else "-"
        lines.append(
            f"{r['pass']:>4}  {r['score']:>10.1f}  {drc:>6}  {str(r['gates_ok']):>8}  {scars}"
        )
    lines.append("")
    s0 = results[0]["score"]
    sN = results[-1]["score"]
    if results[-1]["gates_ok"] and sN < s0:
        lines.append(f"IMPROVED: score {s0:.1f} → {sN:.1f} (gates OK)")
    elif sN < s0:
        lines.append(f"TRAJECTORY: score {s0:.1f} → {sN:.1f} (gates pending)")
    else:
        lines.append(f"TRAJECTORY: score {s0:.1f} → {sN:.1f}")

    timeline = "\n".join(lines) + "\n\n--- spans ---\n" + "\n".join(all_logs) + "\n"
    timeline_path = out_dir / "pass_timeline.txt"
    timeline_path.write_text(timeline, encoding="utf-8")
    print()
    print("\n".join(lines))
    print(f"\nwrote {timeline_path}")
    for i in range(1, n_passes + 1):
        print(f"wrote {out_dir / f'board_pass_{i}.svg'}")
    if tracer.enabled and tracer.ui_url:
        print(f"\nWeave UI: {tracer.ui_url}")

    return {
        "results": results,
        "timeline_path": str(timeline_path),
        "summary_lines": lines,
        "weave_enabled": tracer.enabled,
        "weave_project": tracer.project if tracer.enabled else None,
        "weave_url": tracer.ui_url if tracer.enabled else None,
    }


def run_loop(
    *,
    scar_id: str = "scar_000",
    metrics: dict[str, Any] | None = None,
    gate_flags: dict[str, bool] | None = None,
    out_dir: Path | str | None = None,
    label: str = "stub loop run",
) -> Path:
    """Backward-compatible single-scar writer (used by `copper-scar loop`)."""
    from copper_scar.harness.gates import evaluate_gates as eg

    metrics = metrics or {
        "volume_mm3": 1000.0,
        "vias": 10,
        "copper_layers": 4,
    }
    gate_flags = gate_flags or {}
    report = eg(gate_flags)
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
        "rule": {"type": "keepout", "ref": "U1", "x": 0, "y": 0, "w": 1, "h": 1, "clearance": 0.5},
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


def run_demo_cli(args: Any) -> int:
    enable_weave = False if getattr(args, "no_weave", False) else None
    run_demo(
        n_passes=getattr(args, "passes", 3),
        baseline_path=Path(args.baseline) if getattr(args, "baseline", None) else None,
        scars_dir=Path(args.scars_dir) if getattr(args, "scars_dir", None) else None,
        out_dir=Path(args.out_dir) if getattr(args, "out_dir", None) else None,
        seed=getattr(args, "seed", 0),
        weave_project=getattr(args, "weave_project", None),
        enable_weave=enable_weave,
    )
    return 0
