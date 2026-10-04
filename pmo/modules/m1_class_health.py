"""MODULE M1 — Chỉ số lớp: đánh giá + đề xuất cải thiện.

Chỉ đọc kho (student_metrics.json). Không gọi API, không tự tính CC/BT/EL.
Đầu ra: result.json (đầy đủ cho renderer) + summary.json (≤5KB cho AI đọc).
"""
from __future__ import annotations

from collections import defaultdict
from statistics import mean

from pmo.warehouse import Snapshot

NAME = "m1_chi_so_lop"
LABEL = {"cc": "Chuyên cần", "bt": "Bài tập về nhà", "el": "Elearning"}
# Ngưỡng đồng bộ với assign_badge (lms_fe_formulas.js)
ALARM = {"cc": 20, "bt": 20, "el": 40}
WARN = {"cc": 10, "bt": 10, "el": 20}


def _recommend(row: dict) -> list[dict]:
    recs = []
    cc, bt, el = row["cc"], row["bt"], row["el"]
    if cc["percent"] >= WARN["cc"]:
        recs.append({
            "issue": "cc", "level": "alarm" if cc["percent"] >= ALARM["cc"] else "warn",
            "action": f"GV/TG liên hệ trực tiếp {cc['count']} SV vắng > 10% trong 48h; "
                      "SV vắng ≥ 20% báo CVHT và phụ huynh; điểm danh đầu và cuối buổi.",
            "owner": row["teacherName"],
            "students": [d["code"] for d in cc["details"]][:50],
        })
    if bt["percent"] >= WARN["bt"]:
        recs.append({
            "issue": "bt", "level": "alarm" if bt["percent"] >= ALARM["bt"] else "warn",
            "action": f"Nhắc {bt['count']} SV chưa nộp đủ bài đã đến hạn; TG mở buổi hỗ trợ chữa bài; "
                      "đăng hạn nộp lên nhóm lớp trước 24h.",
            "owner": row["teacherName"],
            "students": [d["code"] for d in bt["details"]][:50],
        })
    if el["percent"] >= WARN["el"] or (el["percent"] >= 10 and not recs):
        recs.append({
            "issue": "el", "level": "alarm" if el["percent"] >= ALARM["el"] else "warn",
            "action": f"{el['count']} SV chưa hoàn thành 100% Elearning trước buổi học: "
                      "kiểm tra đầu giờ, gắn hoàn thành EL với điều kiện vào lớp.",
            "owner": row["teacherName"],
            "students": [d["code"] for d in el["details"]][:50],
        })
    return recs


def _severity(row: dict) -> float:
    # Chuẩn hóa theo ngưỡng báo động để 3 chỉ số so sánh được với nhau
    return round(sum(row[k]["percent"] / ALARM[k] for k in ALARM), 3)


def run(snapshot: Snapshot) -> dict:
    rows = snapshot.read_json("student_metrics.json", [])
    active = [r for r in rows if r["totalStudents"] > 0]

    classes = []
    for r in rows:
        classes.append({
            "className": r["className"], "courseCode": r["courseCode"], "courseName": r["courseName"],
            "teacherName": r["teacherName"], "campus": r["campus"], "cohort": r["cohort"], "major": r["major"],
            "totalStudents": r["totalStudents"], "status": r["status"],
            "badge": r["badge"], "badgeEmoji": r["badgeEmoji"],
            "cc": {"percent": r["cc"]["percent"], "count": r["cc"]["count"]},
            "bt": {"percent": r["bt"]["percent"], "count": r["bt"]["count"]},
            "el": {"percent": r["el"]["percent"], "count": r["el"]["count"]},
            "severity": _severity(r) if r["totalStudents"] else 0,
            "recommendations": _recommend(r) if r["totalStudents"] else [],
        })
    classes.sort(key=lambda c: -c["severity"])

    by_subject: dict[str, list] = defaultdict(list)
    by_teacher: dict[str, list] = defaultdict(list)
    for c in classes:
        if c["totalStudents"]:
            by_subject[c["courseCode"]].append(c)
            by_teacher[c["teacherName"]].append(c)

    def agg(items: list) -> dict:
        return {
            "classes": len(items),
            "avgCC": round(mean(i["cc"]["percent"] for i in items), 2),
            "avgBT": round(mean(i["bt"]["percent"] for i in items), 2),
            "avgEL": round(mean(i["el"]["percent"] for i in items), 2),
            "alarm": sum(1 for i in items if i["badge"] == "Báo động"),
        }

    subjects = {k: {**agg(v), "hotspot": v[0]["className"]} for k, v in by_subject.items()}
    teachers = {k: agg(v) for k, v in by_teacher.items()}
    badge_count: dict[str, int] = defaultdict(int)
    for c in classes:
        badge_count[c["badge"]] += 1

    result = {"period": snapshot.period, "classes": classes, "subjects": subjects, "teachers": teachers}
    summary = {
        "period": snapshot.period,
        "module": NAME,
        "totals": {"classCourses": len(rows), "active": len(active), "badges": dict(badge_count)},
        "top_hotspots": [
            {k: c[k] for k in ("className", "courseCode", "teacherName", "badge")}
            | {"cc%": c["cc"]["percent"], "bt%": c["bt"]["percent"], "el%": c["el"]["percent"]}
            for c in classes[:5] if c["severity"] > 0
        ],
        "subjects": {k: {kk: v[kk] for kk in ("classes", "avgCC", "avgBT", "avgEL", "alarm", "hotspot")}
                     for k, v in subjects.items()},
        "actions_needed": sum(len(c["recommendations"]) for c in classes),
    }
    return {"result": result, "summary": summary}
