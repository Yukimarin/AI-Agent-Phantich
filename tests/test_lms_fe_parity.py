"""Đối chiếu 1:1 Metric Engine Python với lib/lms_fe_formulas.js (bản JS đã được người dùng duyệt).

Nếu test này fail nghĩa là bản Python đang tính KHÁC bản chuẩn — không được xuất báo cáo.
"""
from __future__ import annotations

import json
import random
import shutil
import subprocess

import pytest

from pmo.config import ROOT
from pmo.metrics import lms_fe

NODE = shutil.which("node")
pytestmark = pytest.mark.skipif(NODE is None, reason="Cần Node.js để đối chiếu với bản JS")

JS_RUNNER = """
const f = require(process.argv[1]);
let buf = '';
process.stdin.on('data', d => buf += d);
process.stdin.on('end', () => {
  const cases = JSON.parse(buf);
  const out = cases.map(c => {
    const m = f.calcAllMetrics(c.students, c.dueHw);
    return { metrics: m, badge: f.assignBadge(m) };
  });
  process.stdout.write(JSON.stringify(out));
});
"""


def _random_student(rng: random.Random, i: int) -> dict:
    s: dict = {"studentCode": f"SV{i:03d}", "fullName": f"Sinh vien {i}"}
    if rng.random() > 0.05:
        planned = rng.randint(0, 12)
        absent = rng.randint(0, planned) if planned else 0
        s["absence"] = {
            "absentSessions": absent,
            "attendedSessions": planned - absent,
            "plannedSessions": planned,
            "rate": round(absent / planned * 100, 4) if planned else 0,
        }
    if rng.random() > 0.05:
        total = rng.randint(0, 6)
        s["homework"] = {"done": rng.randint(0, total) if total else 0, "total": total}
    if rng.random() > 0.05:
        s["elearning"] = {"rate": rng.choice([100, 100, 100, rng.uniform(0, 100)])}
    return s


def _cases() -> list[dict]:
    rng = random.Random(20261004)
    cases = [
        {"students": [], "dueHw": None},
        # ≥80% done=0 => chưa giao bài
        {"students": [{"homework": {"done": 0, "total": 4}}] * 9 + [{"homework": {"done": 1, "total": 4}}], "dueHw": None},
        # Ngưỡng CC đúng 10% không tính vi phạm
        {"students": [{"absence": {"rate": 10}}, {"absence": {"rate": 10.01}}], "dueHw": None},
    ]
    for n in range(300):
        size = rng.randint(1, 50)
        due = rng.choice([None, None, 0, 1, 2, 3])
        cases.append({"students": [_random_student(rng, i) for i in range(size)], "dueHw": due})
    return cases


def test_python_matches_js_reference():
    cases = _cases()
    proc = subprocess.run(
        [NODE, "-e", JS_RUNNER, str(ROOT / "lib" / "lms_fe_formulas.js")],
        input=json.dumps(cases), capture_output=True, text=True, encoding="utf-8", check=True,
    )
    js_out = json.loads(proc.stdout)

    for idx, (case, js) in enumerate(zip(cases, js_out)):
        py_metrics = lms_fe.calc_all_metrics(case["students"], case["dueHw"])
        py_badge = lms_fe.assign_badge(py_metrics)
        # So sánh qua JSON; JS bỏ field undefined nên bỏ các key None ở phía Python
        normalized = json.loads(json.dumps(py_metrics), object_hook=lambda d: {k: v for k, v in d.items() if v is not None})
        assert normalized == js["metrics"], f"Lệch metrics ở case {idx}"
        assert py_badge == js["badge"], f"Lệch badge ở case {idx}"
