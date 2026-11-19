"""GATE 2 — Chỉ số. Chạy sau Metric Engine.

(a) Bất biến toán học  (b) Bộ test hồi quy + đối chiếu JS  (c) Golden set do người dùng xác nhận.
"""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timedelta, timezone

from pmo.config import GOLDEN_DIR, ROOT
from pmo.gates.base import FAIL, PASS, WARN, Check
from pmo.warehouse import Snapshot

G = "G2 Chỉ số"
KEYS = ("cc", "bt", "el")
VN_TZ = timezone(timedelta(hours=7))


def _vn_date(iso: str | None) -> str | None:
    if not iso:
        return None
    return datetime.fromisoformat(iso).astimezone(VN_TZ).date().isoformat()


def _invariants(rows: list[dict]) -> Check:
    bad = []
    for r in rows:
        tag = f"{r['className']}/{r['courseCode']}"
        for k in KEYS:
            m = r[k]
            if not 0 <= m["percent"] <= 100:
                bad.append(f"{tag} {k}.percent={m['percent']}")
            if m["count"] > max(m["total"], 0):
                bad.append(f"{tag} {k}.count {m['count']} > total {m['total']}")
            if m["total"] not in (0, r["totalStudents"]):
                bad.append(f"{tag} {k}.total {m['total']} ≠ sĩ số {r['totalStudents']}")
            if m["count"] != len(m["details"]):
                bad.append(f"{tag} {k}.count ≠ số SV trong danh sách")
    return Check(G, "Bất biến chỉ số", FAIL if bad else PASS,
                 f"{len(bad)} vi phạm" if bad else f"{len(rows)} lớp-môn hợp lệ", bad)


def _test_suite() -> Check:
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "--no-header", "-p", "no:cacheprovider",
         "tests/regression", "tests/test_lms_fe_parity.py"],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
    )
    last = (proc.stdout.strip().splitlines() or ["(không có output)"])[-1]
    if proc.returncode == 0:
        return Check(G, "Test hồi quy + đối chiếu JS", PASS, last)
    fails = [l for l in proc.stdout.splitlines() if l.startswith(("FAILED", "ERROR"))]
    return Check(G, "Test hồi quy + đối chiếu JS", FAIL, last, fails or [proc.stderr[-500:]])


def _golden(rows: list[dict], period: str, fetched_at: str | None = None) -> Check:
    """Golden là ảnh chụp LMS FE tại ngày `asOf` → chỉ so chặt với dữ liệu lấy cùng ngày (giờ VN).

    Khác ngày: số LMS thay đổi theo buổi học/bài tập mới nên chỉ WARN, kèm chênh lệch tham khảo.
    Golden thiếu `asOf`: so chặt như cũ.
    """
    files = sorted(GOLDEN_DIR.glob("*.json")) if GOLDEN_DIR.exists() else []
    if not files:
        return Check(G, "Golden set (số liệu LMS FE đã xác nhận)", WARN,
                     "Chưa có golden set — chưa thể khẳng định khớp LMS Frontend. Xem tests/golden/README.md")
    index = {(r["className"], r["courseCode"]): r for r in rows}
    data_date = _vn_date(fetched_at)
    bad, compared = [], 0
    stale, stale_compared, stale_dates = [], 0, set()
    for f in files:
        g = json.loads(f.read_text(encoding="utf-8"))
        if g.get("period") and g["period"] != period:
            continue
        as_of = g.get("asOf")
        is_stale = bool(as_of and data_date and as_of != data_date)
        if is_stale:
            stale_dates.add(as_of)
        for it in g.get("items", []):
            r = index.get((it["className"], it["courseCode"]))
            if r is None:
                bad.append(f"{f.name}: không thấy {it['className']}/{it['courseCode']} trong kỳ")
                continue
            tol = it.get("tolerance", {})
            for k in KEYS:
                exp = it.get(f"{k}_count")
                if exp is None:
                    continue
                got = r[k]["count"]
                if is_stale:
                    stale_compared += 1
                    if got != exp:
                        stale.append(f"{it['className']}/{it['courseCode']} {k.upper()}: "
                                     f"{as_of} LMS FE {exp} SV → {data_date} hệ thống {got} SV")
                    continue
                compared += 1
                if abs(got - exp) > tol.get(k, 0):
                    bad.append(f"{it['className']}/{it['courseCode']} {k.upper()}: hệ thống {got} SV ≠ LMS FE {exp} SV")
    if bad:
        return Check(G, "Golden set (số liệu LMS FE đã xác nhận)", FAIL,
                     f"{len(bad)} sai lệch / {compared} chỉ số", bad)
    if stale_compared and compared == 0:
        return Check(G, "Golden set (số liệu LMS FE đã xác nhận)", WARN,
                     f"Golden chụp ngày {', '.join(sorted(stale_dates))}, dữ liệu lấy ngày {data_date} → "
                     f"không đối chiếu chặt; {len(stale)}/{stale_compared} chỉ số đã biến động (tham khảo). "
                     f"Cần chụp golden mới cùng ngày để khẳng định khớp FE.", stale)
    if compared == 0 and not bad:
        return Check(G, "Golden set (số liệu LMS FE đã xác nhận)", WARN, f"Không có golden cho kỳ {period}")
    return Check(G, "Golden set (số liệu LMS FE đã xác nhận)", FAIL if bad else PASS,
                 f"{len(bad)} sai lệch / {compared} chỉ số" if bad else f"Khớp {compared} chỉ số", bad)


def run(snapshot: Snapshot, run_tests: bool = True) -> list[Check]:
    rows = snapshot.read_json("student_metrics.json", [])
    checks = [_invariants(rows)]
    if run_tests:
        checks.append(_test_suite())
    fetched_at = snapshot.manifest().get("stages", {}).get("fetch", {}).get("at")
    checks.append(_golden(rows, snapshot.period, fetched_at))
    return checks
