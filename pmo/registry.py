"""Registry phân công: Lớp ↔ Môn ↔ GV ↔ courseClassId — nguồn sự thật duy nhất.

Nguồn: config/registry_seed.json (khởi tạo từ scratch/ks26_course_material_audit.json).
Mở rộng KS24/KS25 sau bằng cách bổ sung lớp vào seed, không sửa code.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from pmo.config import CONFIG_DIR, ROOT, TRACKED_COURSES

SEED_FILE = CONFIG_DIR / "registry_seed.json"
LEGACY_SEED = ROOT / "scratch" / "ks26_course_material_audit.json"


def _parse_class_name(name: str) -> dict:
    campus = name.split("-")[0] if "-" in name else ""
    cohort = (re.search(r"K(?:S)?(\d{2})", name) or [None, ""])[1]
    major = "QTKD" if "QTKD" in name else ("CNTT" if "CNTT" in name else "")
    return {"campus": campus, "cohort": f"K{cohort}" if cohort else "", "major": major}


def is_valid_course_class_id(cid: str | None) -> bool:
    return bool(cid) and len(cid) >= 10


def load_seed(path: Path | None = None) -> dict:
    path = path or (SEED_FILE if SEED_FILE.exists() else LEGACY_SEED)
    if not path.exists():
        raise FileNotFoundError(f"Không tìm thấy registry seed: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def build_registry(seed: dict, tracked: list[str] | None = None) -> list[dict]:
    tracked = tracked if tracked is not None else TRACKED_COURSES
    rows = []
    for cls in seed.get("classes", []):
        meta = _parse_class_name(cls.get("className", ""))
        for c in cls.get("assignedCourses", []):
            rows.append({
                "className": cls.get("className"),
                "classId": cls.get("classId"),
                **meta,
                "courseCode": c.get("courseCode"),
                "courseName": c.get("courseName"),
                "courseClassId": c.get("courseClassId"),
                "teacherName": c.get("teacherName") or "Chưa phân",
                "tracked": c.get("courseCode") in tracked,
            })
    return rows
