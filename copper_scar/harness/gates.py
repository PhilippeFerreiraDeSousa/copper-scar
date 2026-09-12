"""Hard gates for a valid Copper Scar / PCBGolf run.

A design must pass all gates before its score is considered shippable.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class GateResult:
    name: str
    passed: bool
    detail: str = ""


@dataclass
class GateReport:
    results: list[GateResult] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return all(r.passed for r in self.results)

    def failures(self) -> list[GateResult]:
        return [r for r in self.results if not r.passed]


# Hard gates (hackathon-ready checklist)
HARD_GATES = (
    "drc_clean",          # design-rule check passes
    "erc_clean",          # electrical-rule check passes
    "netlist_match",      # layout nets match schematic / golden netlist
    "fab_stackup_ok",     # copper layers / stackup within fab limits
    "min_trace_clearance", # trace/space >= process minimum
    "via_annular_ok",     # via annular rings meet fab rules
    "outline_closed",     # board outline is closed and valid
)


def evaluate_gates(flags: dict[str, Any] | None = None) -> GateReport:
    """Evaluate hard gates from a boolean flag map.

    Missing keys default to False (fail-closed).
    """
    flags = flags or {}
    report = GateReport()
    for name in HARD_GATES:
        passed = bool(flags.get(name, False))
        report.results.append(
            GateResult(
                name=name,
                passed=passed,
                detail="ok" if passed else "failed or missing",
            )
        )
    return report
