"""Simulated PCB board state (no KiCad) for closed-loop demos."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

MIN_CLEARANCE_MM = 0.5


@dataclass
class Part:
    ref: str
    x: float
    y: float
    w: float
    h: float

    def bbox(self) -> tuple[float, float, float, float]:
        """Return (x0, y0, x1, y1)."""
        return (self.x, self.y, self.x + self.w, self.y + self.h)

    def center(self) -> tuple[float, float]:
        return (self.x + self.w / 2.0, self.y + self.h / 2.0)


@dataclass
class BoardState:
    width: float
    height: float
    thickness_mm: float
    parts: list[Part]
    vias: int
    layers: int
    drc_issues: list[str] = field(default_factory=list)
    label: str = "sim board"
    placeholder: bool = False
    notes: str | None = None

    def volume_mm3(self) -> float:
        return float(self.width) * float(self.height) * float(self.thickness_mm)

    def metrics(self) -> dict[str, float | int]:
        return {
            "volume_mm3": self.volume_mm3(),
            "vias": int(self.vias),
            "copper_layers": int(self.layers),
        }

    def official_score(self) -> float:
        from copper_scar.harness.score import compute_score

        m = self.metrics()
        return compute_score(m["volume_mm3"], m["vias"], m["copper_layers"])

    def part_by_ref(self, ref: str) -> Part | None:
        for p in self.parts:
            if p.ref == ref:
                return p
        return None

    def check_drc(self, min_clearance: float = MIN_CLEARANCE_MM) -> list[str]:
        """AABB clearance + outline containment. Updates and returns drc_issues."""
        issues: list[str] = []
        for p in self.parts:
            if p.x < 0 or p.y < 0 or p.x + p.w > self.width + 1e-9 or p.y + p.h > self.height + 1e-9:
                issues.append(f"outline_violation:{p.ref}")
            if p.w <= 0 or p.h <= 0:
                issues.append(f"invalid_size:{p.ref}")

        for i, a in enumerate(self.parts):
            ax0, ay0, ax1, ay1 = a.bbox()
            for b in self.parts[i + 1 :]:
                bx0, by0, bx1, by1 = b.bbox()
                gap_x = max(0.0, max(bx0 - ax1, ax0 - bx1))
                gap_y = max(0.0, max(by0 - ay1, ay0 - by1))
                if ax0 < bx1 and ax1 > bx0 and ay0 < by1 and ay1 > by0:
                    issues.append(f"overlap:{a.ref}/{b.ref}")
                else:
                    if gap_x == 0.0 and gap_y == 0.0:
                        dist = 0.0
                    elif gap_x == 0.0:
                        dist = gap_y
                    elif gap_y == 0.0:
                        dist = gap_x
                    else:
                        dist = (gap_x * gap_x + gap_y * gap_y) ** 0.5
                    if dist < min_clearance - 1e-9:
                        issues.append(f"clearance:{a.ref}/{b.ref}:{dist:.3f}<{min_clearance}")

        self.drc_issues = issues
        return issues

    def shrink_outline(self, dw: float, dh: float) -> None:
        """Shrink board outline."""
        self.width = max(0.1, self.width - dw)
        self.height = max(0.1, self.height - dh)

    def move_part(self, ref: str, dx: float, dy: float) -> bool:
        p = self.part_by_ref(ref)
        if p is None:
            return False
        p.x += dx
        p.y += dy
        return True

    def apply_keepout_scar(self, scar: dict[str, Any]) -> list[str]:
        """Nudge parts out of a keepout / enforce min_clearance from scar rule.

        Returns list of refs that were moved.
        """
        rule = scar.get("rule") or {}
        rtype = rule.get("type", "keepout")
        moved: list[str] = []
        clearance = float(rule.get("clearance", MIN_CLEARANCE_MM))

        if rtype == "keepout":
            kx = float(rule.get("x", 0))
            ky = float(rule.get("y", 0))
            kw = float(rule.get("w", 0))
            kh = float(rule.get("h", 0))
            anchor = rule.get("ref")  # protected part — do not move unless nudge_self
            nudge_self = bool(rule.get("nudge_self", False))
            kx0, ky0, kx1, ky1 = kx, ky, kx + kw, ky + kh
            kx0e, ky0e = kx0 - clearance, ky0 - clearance
            kx1e, ky1e = kx1 + clearance, ky1 + clearance

            for p in self.parts:
                if anchor and p.ref == anchor and not nudge_self:
                    continue
                px0, py0, px1, py1 = p.bbox()
                intersects = px0 < kx1e and px1 > kx0e and py0 < ky1e and py1 > ky0e
                if not intersects:
                    continue
                cx = (kx0 + kx1) / 2.0
                cy = (ky0 + ky1) / 2.0
                pcx, pcy = p.center()
                if abs(pcx - cx) >= abs(pcy - cy):
                    if pcx >= cx:
                        p.x = kx1e
                    else:
                        p.x = kx0e - p.w
                else:
                    if pcy >= cy:
                        p.y = ky1e
                    else:
                        p.y = ky0e - p.h
                moved.append(p.ref)

        elif rtype == "min_clearance":
            refs = rule.get("parts") or []
            if len(refs) >= 2:
                a = self.part_by_ref(refs[0])
                b = self.part_by_ref(refs[1])
                if a and b:
                    ax0, ay0, ax1, ay1 = a.bbox()
                    b.x = ax1 + clearance
                    moved.append(b.ref)

        # Expand outline if needed so nudged parts fit, then clamp
        if self.parts:
            need_w = max(p.x + p.w for p in self.parts) + MIN_CLEARANCE_MM
            need_h = max(p.y + p.h for p in self.parts) + MIN_CLEARANCE_MM
            self.width = max(self.width, need_w)
            self.height = max(self.height, need_h)
        for p in self.parts:
            p.x = max(0.0, min(p.x, max(0.0, self.width - p.w)))
            p.y = max(0.0, min(p.y, max(0.0, self.height - p.h)))

        return moved

    def copy(self) -> BoardState:
        return deepcopy(self)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> BoardState:
        parts_raw = data.get("parts") or []
        parts = [
            Part(
                ref=p["ref"],
                x=float(p["x"]),
                y=float(p["y"]),
                w=float(p["w"]),
                h=float(p["h"]),
            )
            for p in parts_raw
        ]
        layers = data.get("layers", data.get("copper_layers", 4))
        return cls(
            width=float(data["width"]),
            height=float(data["height"]),
            thickness_mm=float(data["thickness_mm"]),
            parts=parts,
            vias=int(data.get("vias", 0)),
            layers=int(layers),
            drc_issues=list(data.get("drc_issues") or []),
            label=str(data.get("label", "sim board")),
            placeholder=bool(data.get("placeholder", False)),
            notes=data.get("notes"),
        )

    def tight_bbox(self, margin: float = MIN_CLEARANCE_MM) -> tuple[float, float]:
        """Minimal outline that fits all parts with margin."""
        if not self.parts:
            return (margin * 2, margin * 2)
        max_x = max(p.x + p.w for p in self.parts) + margin
        max_y = max(p.y + p.h for p in self.parts) + margin
        return (max_x, max_y)


def render_svg(board: BoardState, path: str | Path, *, scale: float = 8.0) -> None:
    """Write a simple SVG: board rect + labeled part rects (red fill if in DRC)."""
    board.check_drc()
    bad_refs: set[str] = set()
    for issue in board.drc_issues:
        if ":" not in issue:
            continue
        rest = issue.split(":", 1)[1]
        for part in rest.split("/"):
            ref = part.split(":")[0]
            if ref and any(c.isalpha() for c in ref):
                bad_refs.add(ref)

    w_px = board.width * scale
    h_px = board.height * scale
    pad = 20
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_px + 2 * pad}" height="{h_px + 2 * pad}" '
        f'viewBox="{-pad} {-pad} {w_px + 2 * pad} {h_px + 2 * pad}">',
        f'  <rect x="0" y="0" width="{w_px}" height="{h_px}" fill="#1a1a2e" stroke="#eaeaea" stroke-width="2"/>',
    ]
    for p in board.parts:
        fill = "#e94560" if p.ref in bad_refs else "#0f3460"
        stroke = "#ff6b6b" if p.ref in bad_refs else "#4ea8de"
        lines.append(
            f'  <rect x="{p.x * scale}" y="{p.y * scale}" width="{p.w * scale}" height="{p.h * scale}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="1.5" opacity="0.9"/>'
        )
        lines.append(
            f'  <text x="{(p.x + p.w / 2) * scale}" y="{(p.y + p.h / 2) * scale}" '
            f'fill="#ffffff" font-size="{max(8, 3 * scale)}" text-anchor="middle" '
            f'dominant-baseline="middle">{p.ref}</text>'
        )
    status = "DRC_FAIL" if board.drc_issues else "DRC_OK"
    lines.append(
        f'  <text x="0" y="{-6}" fill="#cccccc" font-size="12">'
        f"{board.width:.1f}x{board.height:.1f}mm score={board.official_score():.0f} {status}</text>"
    )
    lines.append("</svg>")
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
