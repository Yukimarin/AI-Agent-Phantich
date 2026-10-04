"""Bài học đã trả giá — mỗi bài học là một test. Thêm test mới mỗi khi người dùng sửa một lỗi.

Nguồn: docs/archive/super_memory_20261004.md mục 7 và mục 11.
"""
from __future__ import annotations

from pmo.metrics import lms_fe


def _hw(done: int, total: int = 4) -> dict:
    return {"studentCode": "x", "fullName": "x", "homework": {"done": done, "total": total}}


def test_lesson1_bt_khong_chia_tong_bai_ca_mon():
    """Tuần đầu giao 1 bài, môn có 4 bài: SV nộp 1 bài thì KHÔNG vi phạm (không phải 75%)."""
    students = [_hw(1)] * 9 + [_hw(0)]
    bt = lms_fe.calc_homework_violation(students)
    assert bt["count"] == 1
    assert bt["percent"] == 10.0


def test_lesson1_bt_chua_giao_bai_thi_0_phan_tram():
    students = [_hw(0)] * 8 + [_hw(1)] * 2  # 80% done=0
    assert lms_fe.calc_homework_violation(students)["percent"] == 0


def test_cc_nguong_nghiem_ngat_lon_hon_10():
    students = [{"absence": {"rate": 10}}, {"absence": {"rate": 10.5}}]
    cc = lms_fe.calc_attendance_violation(students)
    assert cc["count"] == 1


def test_el_dem_sv_chua_hoan_thanh_100():
    students = [{"elearning": {"rate": 100}}, {"elearning": {"rate": 99.9}}, {}]
    el = lms_fe.calc_elearning_violation(students)
    assert el["count"] == 1  # thiếu field elearning => coi như 100%


def test_lop_khong_co_sv_la_chuan_bi_hoc():
    m = lms_fe.calc_all_metrics([])
    assert lms_fe.assign_badge(m)["badge"] == "Chuẩn bị học"
