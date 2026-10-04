"""Metric Engine — công thức chuẩn LMS Frontend (port 1:1 từ lib/lms_fe_formulas.js v1.0).

QUYỀN HẠN: Đây là NƠI DUY NHẤT trong pipeline mới được tính CC / BT / EL.
Module, renderer, AI đều KHÔNG được tự tính lại.

Tính đúng đắn được khóa bởi:
  - tests/test_lms_fe_parity.py   (đối chiếu với bản JS chuẩn)
  - tests/regression/test_lessons.py (các bài học đã trả giá)
"""
from __future__ import annotations

import math
from collections import Counter
from decimal import ROUND_HALF_UP, Decimal
from typing import Any, Iterable

Student = dict[str, Any]


def _round2(x: float) -> float:
    """Tương đương parseFloat(x.toFixed(2)) của JS (làm tròn trên giá trị nhị phân chính xác)."""
    return float(Decimal(x).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def _num(value: Any, default: float) -> float:
    """Tương đương toán tử `??` của JS: chỉ thay khi None/thiếu."""
    return default if value is None else value


def _empty() -> dict:
    return {"count": 0, "total": 0, "percent": 0, "details": []}


def _pct(count: int, total: int) -> float:
    return _round2(count / total * 100)


def _has_learning(students: list[Student], key: str) -> bool:
    """API mới (từ 10/2026) trả `learning.<key>` — đúng nguồn LMS FE dùng."""
    return bool(students) and all(isinstance((s.get("learning") or {}).get(key), (int, float)) for s in students)


def calc_attendance_violation(students: list[Student]) -> dict:
    """SV vi phạm CC.

    Ưu tiên (khớp FE, golden 2026-W40): `learning.absenceRate` ≥ 10, trong đó
    absenceRate = (KP×1 + CP×0.5 + Muộn×0.5) / buổi kế hoạch × 100.
    Fallback (API cũ không có `learning`): `absence.rate` > 10 — không tách KP/CP/Muộn.
    """
    if not students:
        return _empty()
    use_learning = _has_learning(students, "absenceRate")
    details = []
    for s in students:
        abs_ = s.get("absence") or {}
        if use_learning:
            rate = s["learning"]["absenceRate"]
            violated = rate >= 10
        else:
            rate = _num(abs_.get("rate"), 0)
            violated = rate > 10
        if violated:
            details.append({
                "code": s.get("studentCode"),
                "name": s.get("fullName"),
                "absRate": _round2(rate),
                "absentSessions": _num(abs_.get("absentSessions"), 0),
                "attendedSessions": _num(abs_.get("attendedSessions"), 0),
                "plannedSessions": _num(abs_.get("plannedSessions"), 0),
            })
    total = len(students)
    out = {"count": len(details), "total": total, "percent": _pct(len(details), total), "details": details}
    if use_learning:  # nhánh fallback giữ nguyên định dạng bản JS (test parity)
        out["source"] = "learning.absenceRate>=10"
    return out


def infer_due_homework(students: list[Student]) -> int | None:
    """Suy luận số bài đã đến hạn. Trả về None nếu ≥80% SV done=0 (chưa giao bài)."""
    done_values = sorted(_num((s.get("homework") or {}).get("done"), 0) for s in students)
    total = len(done_values)
    if sum(1 for v in done_values if v == 0) >= total * 0.8:
        return None
    due = done_values[math.floor(total * 0.75)] or 0
    if due == 0:
        freq = Counter(v for v in done_values if v > 0)
        # JS: sắp xếp theo tần suất giảm dần, hòa thì giá trị nhỏ hơn đứng trước
        due = sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))[0][0] if freq else 0
    return int(due)


def calc_homework_violation(students: list[Student], current_due_hw: int | None = None) -> dict:
    """SV vi phạm BT. TUYỆT ĐỐI không dùng homework.rate của API (chia cho tổng bài cả môn).

    Ưu tiên (khớp FE, golden W40): `learning.homeworkMissingRate` ≥ 10 — nhãn FE "thiếu BTVN từ 10%".
    Môn dài (22 buổi) thiếu 1 bài = 4.55% → chưa vi phạm; môn 4 buổi thiếu 1 bài = 25% → vi phạm.
    Fallback: done < số bài đến hạn suy luận — suy luận này từng tính oan cả lớp
    (CNTT1/JPN105 44% vs FE 0%) nên chỉ dùng khi API thiếu trường `learning`.
    """
    if not students:
        return _empty()
    total = len(students)
    if current_due_hw is None and _has_learning(students, "homeworkMissingRate"):
        details = []
        for s in students:
            miss = s["learning"]["homeworkMissingRate"]
            if miss >= 10:
                hw = s.get("homework") or {}
                details.append({
                    "code": s.get("studentCode"),
                    "name": s.get("fullName"),
                    "done": _num(hw.get("done"), 0),
                    "hwTotal": _num(hw.get("total"), 0),
                    "missingRate": _round2(miss),
                })
        return {"count": len(details), "total": total, "percent": _pct(len(details), total),
                "details": details, "source": "learning.homeworkMissingRate>=10"}
    due = current_due_hw
    if due is None:
        due = infer_due_homework(students)
        if due is None:
            return {"count": 0, "total": total, "percent": 0, "details": [],
                    "inferredDueHw": 0, "note": "Chưa có bài đến hạn (80%+ SV done=0)"}
    if due <= 0:
        return {"count": 0, "total": total, "percent": 0, "details": [], "inferredDueHw": 0}

    details = []
    for s in students:
        hw = s.get("homework") or {}
        done = _num(hw.get("done"), 0)
        if done < due:
            details.append({
                "code": s.get("studentCode"),
                "name": s.get("fullName"),
                "done": done,
                "dueHw": due,
                "hwTotal": _num(hw.get("total"), 0),
                "shortfall": due - done,
            })
    return {"count": len(details), "total": total, "percent": _pct(len(details), total), "details": details}


def calc_elearning_violation(students: list[Student]) -> dict:
    """SV vi phạm EL khi elearning.rate < 100 (thiếu field coi như 100)."""
    if not students:
        return _empty()
    details = []
    for s in students:
        rate = _num((s.get("elearning") or {}).get("rate"), 100)
        if rate < 100:
            details.append({
                "code": s.get("studentCode"),
                "name": s.get("fullName"),
                "elRate": _round2(rate),
                "violationPercent": _round2(100 - rate),
            })
    total = len(students)
    return {"count": len(details), "total": total, "percent": _pct(len(details), total), "details": details}


def calc_all_metrics(students: list[Student] | None, current_due_hw: int | None = None) -> dict:
    students = students or []
    return {
        "cc": calc_attendance_violation(students),
        "bt": calc_homework_violation(students, current_due_hw),
        "el": calc_elearning_violation(students),
        "totalStudents": len(students),
    }


def assign_badge(metrics: dict) -> dict:
    cc, bt, el = metrics["cc"]["percent"], metrics["bt"]["percent"], metrics["el"]["percent"]
    if metrics["totalStudents"] == 0:
        return {"badge": "Chuẩn bị học", "emoji": "⏳", "className": "badge-info"}
    if cc >= 20 or bt >= 20 or el >= 40:
        return {"badge": "Báo động", "emoji": "🚨", "className": "badge-danger"}
    if cc >= 10 or bt >= 10 or el >= 20:
        return {"badge": "Đôn đốc", "emoji": "🟡", "className": "badge-warning"}
    if el >= 10:
        return {"badge": "Nhắc EL", "emoji": "🟡", "className": "badge-warning"}
    return {"badge": "Chuẩn mực", "emoji": "🟢", "className": "badge-success"}


def iter_violations(metrics: dict) -> Iterable[tuple[str, dict]]:
    for key in ("cc", "bt", "el"):
        yield key, metrics[key]
