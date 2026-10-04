"""Tính student_metrics.json từ raw trong kho bằng Metric Engine."""
from __future__ import annotations

from pmo.data_agent import raw_name
from pmo.metrics import lms_fe
from pmo.registry import is_valid_course_class_id
from pmo.warehouse import Snapshot


def build_student_metrics(snapshot: Snapshot) -> list[dict]:
    registry = snapshot.read_json("registry.json", [])
    rows = []
    for r in registry:
        if not r["tracked"] or not is_valid_course_class_id(r["courseClassId"]):
            continue
        raw = snapshot.read_json(raw_name(r["courseClassId"]))
        if raw is None:
            continue
        students = raw.get("students") or []
        m = lms_fe.calc_all_metrics(students)
        badge = lms_fe.assign_badge(m)
        rows.append({
            **{k: r[k] for k in ("className", "campus", "cohort", "major", "courseCode",
                                 "courseName", "courseClassId", "teacherName")},
            "totalStudents": m["totalStudents"],
            "status": "Chưa vào môn" if m["totalStudents"] == 0 else "Đang học",
            "cc": m["cc"], "bt": m["bt"], "el": m["el"],
            "badge": badge["badge"], "badgeEmoji": badge["emoji"],
        })
    snapshot.write_json("student_metrics.json", rows)
    snapshot.update_manifest("metrics", {"engine": "pmo.metrics.lms_fe (port lms_fe_formulas.js v1.0)",
                                         "rows": len(rows)})
    return rows
