"""Test pipeline mới không cần mạng: fetcher giả + kho tạm."""
from __future__ import annotations

from pmo import data_agent
from pmo.gates import g1_data, g2_metrics
from pmo.gates.base import FAIL, passed
from pmo.metrics.build import build_student_metrics
from pmo.modules import m1_class_health
from pmo.warehouse import Snapshot, current_period

ID_A = "a" * 24
ID_B = "b" * 24
ID_C = "c" * 24


def _seed(extra_id: str | None = None) -> dict:
    return {"classes": [
        {"className": "HN-KS26-CNTT1", "classId": "1", "assignedCourses": [
            {"courseCode": "IT108-K26", "courseName": "Nhập môn", "courseClassId": ID_A, "teacherName": "GV A"},
            {"courseCode": "Orientation", "courseName": "Định hướng", "courseClassId": "x", "teacherName": "GV X"},
        ]},
        {"className": "HN-KS26-CNTT2", "classId": "2", "assignedCourses": [
            {"courseCode": "IT108-K26", "courseName": "Nhập môn", "courseClassId": extra_id or ID_B, "teacherName": "GV B"},
        ]},
    ]}


def _students(n: int, absent_rate: float = 0) -> dict:
    return {"students": [
        {"studentCode": f"S{i}", "fullName": f"S{i}", "absence": {"rate": absent_rate if i == 0 else 0},
         "homework": {"done": 1, "total": 4}, "elearning": {"rate": 100}}
        for i in range(n)
    ]}


def _fake(sizes: dict[str, int]):
    def fetch(cid: str) -> dict:
        return _students(sizes[cid], absent_rate=50)
    return fetch


def test_cache_khong_goi_lai_nguon(tmp_path):
    snap = Snapshot(current_period(), base=tmp_path)
    calls = []

    def fetch(cid):
        calls.append(cid)
        return _students(10)

    data_agent.fetch(snap, fetcher=fetch, seed=_seed())
    data_agent.fetch(snap, fetcher=fetch, seed=_seed())
    assert len(calls) == 2  # 2 courseClassId hợp lệ, lần 2 dùng cache
    data_agent.fetch(snap, fetcher=fetch, seed=_seed(), refresh=True)
    assert len(calls) == 4


def test_g1_chan_ma_lop_cu_si_so_0(tmp_path):
    snap = Snapshot(current_period(), base=tmp_path)
    data_agent.fetch(snap, fetcher=_fake({ID_A: 10, ID_B: 0}), seed=_seed())
    checks = g1_data.run(snap)
    stale = [c for c in checks if c.name.startswith("Sĩ số 0")][0]
    assert stale.status == FAIL
    assert not passed(checks)


def test_g1_chan_loi_lay_du_lieu(tmp_path):
    snap = Snapshot(current_period(), base=tmp_path)

    def broken(cid):
        raise ConnectionError("timeout")

    data_agent.fetch(snap, fetcher=broken, seed=_seed())
    assert not passed(g1_data.run(snap))


def test_bai_hoc_3_registry_tu_cap_nhat_ma_lop_tu_lms(tmp_path):
    """04/10/2026: seed giữ mã cũ của HN-K26-QTKD2/SSK102 → sĩ số 0. Data Agent phải lấy mã hiện hành."""
    snap = Snapshot(current_period(), base=tmp_path)
    live = {"1": [{"courseCode": "IT108-K26", "courseName": "Nhập môn", "courseClassId": ID_A, "teacherName": "GV A"}],
            "2": [{"courseCode": "IT108-K26", "courseName": "Nhập môn", "courseClassId": ID_C, "teacherName": "GV B"}]}
    info = data_agent.fetch(snap, fetcher=_fake({ID_A: 10, ID_C: 12}), seed=_seed(), lister=lambda cid: live[cid])
    assert info["registryChanges"] == [f"HN-KS26-CNTT2/IT108-K26: {ID_B} → {ID_C}"]
    assert passed(g1_data.run(snap))
    # offline dùng lại registry đã cache, không quay về mã cũ
    data_agent.fetch(snap, fetcher=_fake({}), seed=_seed(), lister=lambda cid: 1 / 0, offline=True)
    ids = {r["courseClassId"] for r in snap.read_json("registry.json")}
    assert ID_C in ids and ID_B not in ids


def test_pipeline_dat_va_m1_de_xuat(tmp_path, monkeypatch):
    monkeypatch.setattr(g2_metrics, "GOLDEN_DIR", tmp_path / "golden")  # dữ liệu giả: không áp golden thật
    snap = Snapshot(current_period(), base=tmp_path)
    data_agent.fetch(snap, fetcher=_fake({ID_A: 5, ID_B: 20}), seed=_seed())
    assert passed(g1_data.run(snap))
    rows = build_student_metrics(snap)
    assert len(rows) == 2  # Orientation không theo dõi
    checks = g2_metrics.run(snap, run_tests=False)
    assert passed(checks)

    out = m1_class_health.run(snap)
    top = out["result"]["classes"][0]
    assert top["className"] == "HN-KS26-CNTT1"  # 1/5 SV vắng = 20% CC → báo động
    assert top["badge"] == "Báo động"
    assert top["recommendations"][0]["issue"] == "cc"
    assert top["recommendations"][0]["students"] == ["S0"]
    import json
    assert len(json.dumps(out["summary"], ensure_ascii=False).encode()) <= 5 * 1024
