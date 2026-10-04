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


# --- Bài học 04/10/2026: đối chiếu LMS FE lớp HN-KS26-CNTT1/2 (golden 2026-W40) ---

def _sv(abs_rate: float, l_abs: float, hw_done: int = 1, hw_miss: float = 0) -> dict:
    return {"studentCode": "x", "fullName": "x",
            "absence": {"rate": abs_rate, "absentSessions": 0, "attendedSessions": 2, "plannedSessions": 4},
            "homework": {"done": hw_done, "total": 4},
            "learning": {"source": "LIVE", "absenceRate": l_abs, "homeworkMissingRate": hw_miss}}


def test_cc_dung_learning_absenceRate_co_trong_so_muon_va_co_phep():
    """CNTT2/SKL01: FE 25% (10/40), hệ thống cũ 10% (4/40).

    absence.rate chỉ đếm buổi vắng (không tách KP/CP, bỏ qua đi muộn). FE dùng
    learning.absenceRate = (KP×1 + CP×0.5 + Muộn×0.5) / buổi kế hoạch, vi phạm khi ≥ 10%.
    Môn 4 buổi: đi muộn 1 lần = 12.5% → vi phạm.
    """
    students = ([_sv(0, 0)] * 30 + [_sv(0, 12.5)] * 6   # đi muộn 1 buổi
                + [_sv(25, 12.5)] * 2                    # vắng có phép 1 buổi
                + [_sv(25, 25)] * 2)                     # vắng không phép 1 buổi
    cc = lms_fe.calc_attendance_violation(students)
    assert cc["count"] == 10
    assert cc["percent"] == 25.0


def test_cc_learning_nguong_tu_10_phan_tram():
    cc = lms_fe.calc_attendance_violation([_sv(0, 10), _sv(0, 9.99)])
    assert cc["count"] == 1


def test_bt_dung_learning_homeworkMissingRate_khong_suy_luan_so_bai_den_han():
    """CNTT1/JPN105: hệ thống cũ 44.19% (19/43), FE 0%.

    Hàm suy luận cũ lấy phân vị 75% của done (=3) làm số bài đến hạn, trong khi bài
    buổi 3 chưa đến hạn → 19 SV done=2 bị tính oan. API đã có learning.homeworkMissingRate
    (tỉ lệ bài thiếu so với bài đã đến hạn) → chỉ SV thiếu thật mới vi phạm.
    """
    students = [_sv(0, 0, hw_done=3)] * 24 + [_sv(0, 0, hw_done=2)] * 16 + [_sv(0, 0, hw_done=0, hw_miss=0)] * 3
    bt = lms_fe.calc_homework_violation(students)
    assert bt["count"] == 0

