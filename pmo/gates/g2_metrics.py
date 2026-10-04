"""GATE 2 — Chỉ số. Chạy sau Metric Engine.

(a) Bất biến toán học  (b) Bộ test hồi quy + đối chiếu JS  (c) Golden set do người dùng xác nhận.
"""
from __future__ import annotations

import json
import subprocess
import sys

from pmo.config import GOLDEN_DIR, ROOT
from pmo.gates.base import FAIL, PASS, WARN, Check
from pmo.warehouse import Snapshot

G = "G2 Chỉ số"
KEYS = ("cc", "bt", "el")


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


def _golden(rows: list[dict], period: str) -> Check:
    files = sorted(GOLDEN_DIR.glob("*.json")) if GOLDEN_DIR.exists() else []
    if not files:
        return Check(G, "Golden set (số liệu LMS FE đã xác nhận)", WARN,
                     "Chưa có golden set — chưa thể khẳng định khớp LMS Frontend. Xem tests/golden/README.md")
    index = {(r["className"], r["courseCode"]): r for r in rows}
    bad, compared = [], 0
    for f in files:
        g = json.loads(f.read_text(encoding="utf-8"))
        if g.get("period") and g["period"] != period:
            continue
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
                compared += 1
                got = r[k]["count"]
                if abs(got - exp) > tol.get(k, 0):
                    bad.append(f"{it['className']}/{it['courseCode']} {k.upper()}: hệ thống {got} SV ≠ LMS FE {exp} SV")
    if compared == 0 and not bad:
        return Check(G, "Golden set (số liệu LMS FE đã xác nhận)", WARN, f"Không có golden cho kỳ {period}")
    return Check(G, "Golden set (số liệu LMS FE đã xác nhận)", FAIL if bad else PASS,
                 f"{len(bad)} sai lệch / {compared} chỉ số" if bad else f"Khớp {compared} chỉ số", bad)


def run(snapshot: Snapshot, run_tests: bool = True) -> list[Check]:
    rows = snapshot.read_json("student_metrics.json", [])
    checks = [_invariants(rows)]
    if run_tests:
        checks.append(_test_suite())
    checks.append(_golden(rows, snapshot.period))
    return checks
