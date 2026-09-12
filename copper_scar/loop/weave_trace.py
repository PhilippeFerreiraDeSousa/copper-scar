"""Optional live W&B Weave tracing for the demo loop.

Enabled only when *all* of the following hold:
- Weave was requested (default: auto)
- ``WANDB_API_KEY`` is set
- the optional ``weave`` extra is installed

Otherwise every span is a no-op. Tracing failures never raise into the demo.
"""

from __future__ import annotations

import os
import sys
import asyncio
import inspect
from collections.abc import Callable
from contextlib import contextmanager
from contextvars import ContextVar, Token
from dataclasses import dataclass, field
from typing import Any, Iterator, TypeVar

F = TypeVar("F", bound=Callable[..., Any])

DEFAULT_PROJECT = "copper-scar"
POLICY_VERSION = "copper-scar-sim-v1"

# Logged / traced span names (must stay aligned with demo stdout).
SPAN_PASS = "loop.pass.{i}"
SPAN_OBSERVE = "observe"
SPAN_OBSERVE_LOAD = "observe.load"
SPAN_ACT = "act"
SPAN_ACT_PLAN = "act.plan"
SPAN_ACT_APPLY_SCAR = "act.apply_scar"
SPAN_EVALUATE = "evaluate"
SPAN_EVAL_DRC = "evaluate.drc"
SPAN_EVAL_GATES = "evaluate.gates"
SPAN_EVAL_SCORE = "evaluate.score"
SPAN_IMPROVE = "improve"
SPAN_IMPROVE_WRITE = "improve.scar.write"
OP_AGENT = "copper_scar.agent"
OP_AGENT_PASS = "copper_scar.agent_pass"

ATTR_KEYS = (
    "score",
    "best_score",
    "drc_count",
    "gates_ok",
    "scar_id",
    "policy_version",
)

_current: ContextVar[WeaveTracer | None] = ContextVar("copper_scar_weave_tracer", default=None)


def import_weave() -> Any:
    """Import weave. Isolated so tests can simulate a missing extra."""
    import weave

    return weave


def resolve_project(cli_value: str | None = None) -> str:
    for candidate in (cli_value, os.environ.get("WEAVE_PROJECT"), os.environ.get("WANDB_PROJECT")):
        if candidate and candidate.strip():
            return candidate.strip()
    return DEFAULT_PROJECT


def _env_flag_disabled() -> bool:
    weave_off = os.environ.get("COPPER_SCAR_WEAVE", "").strip().lower()
    if weave_off in {"0", "false", "off", "no"}:
        return True
    disabled = os.environ.get("WEAVE_DISABLED", "").strip().lower()
    return disabled in {"1", "true", "yes", "on"}


def tracing_requested(enable: bool | None) -> bool:
    """Return True when the caller wants live Weave (still requires key + package)."""
    if enable is False:
        return False
    if _env_flag_disabled():
        return False
    if enable is True:
        return True
    return bool(os.environ.get("WANDB_API_KEY", "").strip())


def _warn(message: str) -> None:
    print(f"copper-scar weave: {message}", file=sys.stderr)


@dataclass
class SpanHandle:
    """In-process handle for a span (no-op or live Weave Call)."""

    name: str
    call: Any | None = None
    client: Any | None = None
    output: Any = None
    summary: dict[str, Any] = field(default_factory=dict)

    def set_output(self, output: Any) -> None:
        self.output = output

    def update_summary(self, values: dict[str, Any] | None = None, **kwargs: Any) -> None:
        payload = {**(values or {}), **kwargs}
        self.summary.update(payload)
        call = self.call
        if call is None:
            return
        existing = getattr(call, "summary", None)
        if existing is None:
            try:
                call.summary = dict(payload)
            except Exception:
                return
        else:
            try:
                existing.update(payload)
            except Exception:
                pass

    def merge_attributes(self, values: dict[str, Any]) -> None:
        """Best-effort attribute + summary update (Weave attrs are start-only)."""
        self.update_summary(values)
        call = self.call
        if call is None:
            return
        attrs = getattr(call, "attributes", None)
        if isinstance(attrs, dict):
            try:
                attrs.update(values)
            except Exception:
                pass


class WeaveTracer:
    """Best-effort Weave client wrapper. Disabled tracers are silent no-ops."""

    def __init__(
        self,
        *,
        enabled: bool = False,
        project: str = DEFAULT_PROJECT,
        client: Any | None = None,
        ui_url: str | None = None,
    ) -> None:
        self.enabled = enabled
        self.project = project
        self._client = client
        self._ui_url = ui_url
        self.best_score: float | None = None
        self.last_score: float | None = None
        self.last_drc_count: int | None = None
        self.last_gates_ok: bool | None = None
        self.last_scar_id: str = ""
        self._ops: dict[str, Any] = {}
        self._pending_signals: list[tuple[Any, dict[str, Any]]] = []
        self._weave: Any | None = None

    @classmethod
    def disabled(cls, project: str = DEFAULT_PROJECT) -> WeaveTracer:
        return cls(enabled=False, project=project)

    @classmethod
    def from_client(cls, client: Any, project: str = DEFAULT_PROJECT, ui_url: str | None = None) -> WeaveTracer:
        return cls(enabled=True, project=project, client=client, ui_url=ui_url)

    @classmethod
    def maybe_init(
        cls,
        *,
        project: str | None = None,
        enable: bool | None = None,
        announce: bool = False,
    ) -> WeaveTracer:
        proj = resolve_project(project)
        if not tracing_requested(enable):
            return cls.disabled(proj)

        if not os.environ.get("WANDB_API_KEY", "").strip():
            _warn("WANDB_API_KEY is not set; demo continues offline")
            return cls.disabled(proj)

        try:
            weave = import_weave()
        except ImportError:
            _warn('weave is not installed; demo continues offline. pip install -e ".[weave]"')
            return cls.disabled(proj)

        os.environ.setdefault("WEAVE_PRINT_CALL_LINK", "false")
        try:
            client = _connect(weave, proj)
        except Exception as exc:
            _warn(f"weave.init failed ({exc}); demo continues offline")
            return cls.disabled(proj)

        tracer = cls.from_client(client, project=proj, ui_url=_client_ui_url(client, proj))
        tracer._weave = weave
        if announce:
            tracer.announce()
        return tracer

    @property
    def ui_url(self) -> str | None:
        if self._ui_url:
            return self._ui_url
        if not self.enabled or self._client is None:
            return None
        return _client_ui_url(self._client, self.project)

    def announce(self) -> None:
        url = self.ui_url or f"https://wandb.ai/{self.project}/weave"
        print("Weave tracing enabled")
        print(f"  project: {self.project}")
        print(f"  UI: {url}")
        print("  traces: copper_scar.agent_pass / loop.pass.{i}")
        print("          → observe → observe.load → act → act.plan / act.apply_scar")
        print("          → evaluate → evaluate.drc / evaluate.gates / evaluate.score")
        print("          → improve → improve.scar.write")
        print("  eval:   copper-scar eval  (dataset + Weave Evaluation)")
        print("  signal: live scorers on each pass + attach in Weave → Monitors")
        print()

    def note_eval(
        self,
        *,
        score: float,
        drc_count: int,
        gates_ok: bool,
        scar_id: str | None = None,
    ) -> dict[str, Any]:
        self.last_score = float(score)
        self.last_drc_count = int(drc_count)
        self.last_gates_ok = bool(gates_ok)
        if scar_id:
            self.last_scar_id = scar_id
        if self.best_score is None or score < self.best_score:
            self.best_score = float(score)
        return self.loop_attributes()

    def loop_attributes(
        self,
        *,
        score: float | None = None,
        drc_count: int | None = None,
        gates_ok: bool | None = None,
        scar_id: str | None = None,
    ) -> dict[str, Any]:
        return {
            "score": self.last_score if score is None else float(score),
            "best_score": self.best_score,
            "drc_count": self.last_drc_count if drc_count is None else int(drc_count),
            "gates_ok": self.last_gates_ok if gates_ok is None else bool(gates_ok),
            "scar_id": self.last_scar_id if scar_id is None else scar_id,
            "policy_version": POLICY_VERSION,
        }

    def _disable(self, exc: BaseException) -> None:
        if self.enabled:
            _warn(f"tracing error ({exc}); remaining spans are no-ops")
        self.enabled = False
        self._client = None
        self._weave = None

    @contextmanager
    def span(
        self,
        name: str,
        *,
        inputs: dict[str, Any] | None = None,
        attributes: dict[str, Any] | None = None,
    ) -> Iterator[SpanHandle]:
        handle = SpanHandle(name=name)
        if not self.enabled or self._client is None:
            yield handle
            return

        attrs = {"policy_version": POLICY_VERSION, **(attributes or {})}
        try:
            call = self._client.create_call(
                op=name,
                inputs=inputs or {},
                attributes=attrs,
            )
        except Exception as exc:
            self._disable(exc)
            yield handle
            return

        handle.call = call
        handle.client = self._client
        handle.merge_attributes(attrs)
        try:
            yield handle
        except Exception as exc:
            try:
                self._client.finish_call(call, exception=exc)
            except Exception:
                pass
            raise
        else:
            if handle.summary:
                handle.update_summary(handle.summary)
            try:
                self._client.finish_call(call, output=handle.output)
            except Exception as exc:
                self._disable(exc)

    def as_op(self, name: str, fn: F, *, display_name: str | None = None) -> F:
        """Wrap ``fn`` with ``weave.op`` once; identity when tracing is off."""
        if not self.enabled or self._weave is None:
            return fn
        cached = self._ops.get(name)
        if cached is not None:
            return cached
        try:
            weave = self._weave
            kwargs: dict[str, Any] = {"name": name}
            if display_name:
                kwargs["call_display_name"] = display_name
            wrapped = weave.op(**kwargs)(fn)
        except Exception as exc:
            self._disable(exc)
            return fn
        self._ops[name] = wrapped
        return wrapped

    def queue_signals(self, handle: SpanHandle, output: dict[str, Any]) -> None:
        if handle.call is not None:
            self._pending_signals.append((handle.call, output))

    def apply_signals(self, handle: SpanHandle | None = None, output: dict[str, Any] | None = None) -> None:
        """Apply online Weave Signals/scorers to finished pass calls (best-effort)."""
        pending = list(self._pending_signals)
        self._pending_signals.clear()
        if handle is not None and handle.call is not None and output is not None:
            pending.append((handle.call, output))
        if not pending or not self.enabled or self._weave is None:
            return
        try:
            from copper_scar.eval.scorers import weave_signal_scorers

            scorers = weave_signal_scorers()
        except Exception as exc:
            _warn(f"signal scorers unavailable ({exc})")
            return
        for call, payload in pending:
            for scorer in scorers:
                try:
                    apply = getattr(call, "apply_scorer", None)
                    if apply is None:
                        continue
                    result = apply(scorer, additional_output=payload) if _takes_additional_output(apply) else apply(scorer)
                    _run_maybe_async(result)
                except TypeError:
                    try:
                        _run_maybe_async(apply(scorer))
                    except Exception as exc:
                        _warn(f"apply_scorer failed ({exc})")
                except Exception as exc:
                    _warn(f"apply_scorer failed ({exc})")

    def finish(self) -> None:
        self.apply_signals()
        if not self.enabled or self._client is None:
            return
        flush = getattr(self._client, "flush", None)
        if callable(flush):
            try:
                flush()
            except Exception as exc:
                _warn(f"weave.flush failed ({exc})")
                return
        try:
            weave = import_weave()
            finish = getattr(weave, "finish", None)
            if callable(finish):
                finish()
        except Exception:
            pass


def _connect(weave: Any, project: str) -> Any:
    settings = None
    settings_cls = getattr(weave, "Settings", None)
    if settings_cls is not None:
        try:
            settings = settings_cls(print_call_link=False)
        except TypeError:
            try:
                settings = settings_cls()
            except Exception:
                settings = None
        except Exception:
            settings = None
    if settings is not None:
        try:
            return weave.init(project, settings=settings)
        except TypeError:
            pass
    return weave.init(project)


def _client_ui_url(client: Any, project: str) -> str:
    entity = getattr(client, "entity", None)
    proj = getattr(client, "project", None) or project
    if entity:
        return f"https://wandb.ai/{entity}/{proj}/weave"
    return f"https://wandb.ai/{proj}/weave"


def get_tracer() -> WeaveTracer:
    return _current.get() or WeaveTracer.disabled()


def init_tracer(
    *,
    project: str | None = None,
    enable: bool | None = None,
    tracer: WeaveTracer | None = None,
    announce: bool = False,
) -> Token[WeaveTracer | None]:
    bound = tracer or WeaveTracer.maybe_init(project=project, enable=enable, announce=announce)
    return _current.set(bound)


def reset_tracer(token: Token[WeaveTracer | None]) -> None:
    _current.reset(token)


def _takes_additional_output(fn: Any) -> bool:
    try:
        return "additional_output" in inspect.signature(fn).parameters
    except (TypeError, ValueError):
        return False


def _run_maybe_async(value: Any) -> Any:
    if not inspect.isawaitable(value):
        return value
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(value)
    loop.create_task(value)
    return None
