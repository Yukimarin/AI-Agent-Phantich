"""Kho dữ liệu theo kỳ: data/warehouse/<YYYY-Www>/.

Mọi module chỉ đọc từ đây. Chỉ Data Agent và Metric Engine được ghi.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pmo.config import WAREHOUSE_DIR


def current_period(now: datetime | None = None) -> str:
    now = now or datetime.now()
    year, week, _ = now.isocalendar()
    return f"{year}-W{week:02d}"


def utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class Snapshot:
    def __init__(self, period: str, base: Path = WAREHOUSE_DIR):
        self.period = period
        self.dir = base / period
        self.dir.mkdir(parents=True, exist_ok=True)

    def path(self, name: str) -> Path:
        return self.dir / name

    def exists(self, name: str) -> bool:
        return self.path(name).exists()

    def write_json(self, name: str, obj: Any) -> Path:
        p = self.path(name)
        p.parent.mkdir(parents=True, exist_ok=True)
        tmp = p.with_suffix(p.suffix + ".tmp")
        tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
        tmp.replace(p)  # ghi nguyên tử: không bao giờ để file dở dang
        return p

    def read_json(self, name: str, default: Any = None) -> Any:
        p = self.path(name)
        if not p.exists():
            return default
        return json.loads(p.read_text(encoding="utf-8"))

    # ---- manifest ----
    def manifest(self) -> dict:
        return self.read_json("manifest.json", {"period": self.period, "stages": {}})

    def update_manifest(self, stage: str, info: dict) -> None:
        m = self.manifest()
        m.setdefault("stages", {})[stage] = {"at": utcnow_iso(), **info}
        self.write_json("manifest.json", m)

    def previous(self) -> "Snapshot | None":
        """Kỳ gần nhất trước kỳ này (để so biến động)."""
        if not self.dir.parent.exists():
            return None
        older = sorted(p.name for p in self.dir.parent.iterdir() if p.is_dir() and p.name < self.period)
        return Snapshot(older[-1], self.dir.parent) if older else None
