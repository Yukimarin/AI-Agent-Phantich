"""Khung cổng kiểm định. Mỗi check trả về pass / warn / fail. Có fail ⇒ pipeline dừng."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field

PASS, WARN, FAIL = "pass", "warn", "fail"
ICON = {PASS: "✅", WARN: "⚠️", FAIL: "❌"}


@dataclass
class Check:
    gate: str
    name: str
    status: str
    message: str
    items: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


def passed(checks: list[Check]) -> bool:
    return all(c.status != FAIL for c in checks)


def render_markdown(checks: list[Check], max_items: int = 15) -> str:
    lines = ["| Gate | Kiểm tra | Kết quả | Chi tiết |", "|---|---|---|---|"]
    for c in checks:
        lines.append(f"| {c.gate} | {c.name} | {ICON[c.status]} {c.status.upper()} | {c.message} |")
    detail = [c for c in checks if c.status != PASS and c.items]
    for c in detail:
        lines += ["", f"**{ICON[c.status]} {c.gate} · {c.name}** ({len(c.items)} mục)", ""]
        for it in c.items[:max_items]:
            lines.append(f"- `{it}`")
        if len(c.items) > max_items:
            lines.append(f"- … và {len(c.items) - max_items} mục khác")
    return "\n".join(lines)
