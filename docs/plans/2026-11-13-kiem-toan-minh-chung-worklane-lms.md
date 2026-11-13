# Kiểm Toán Minh Chứng Báo Cáo Công Việc (Worklane vs LMS Telemetry) Implementation Plan

> **For Antigravity:** REQUIRED WORKFLOW: Use `.agent/workflows/execute-plan.md` to execute this plan in single-flow mode.

**Goal:** Xây dựng module kiểm toán tính xác thực của báo cáo công việc hàng ngày (Worklane) đối soát với nhật ký hệ thống (LMS Telemetry), tự động tính giờ công hiệu dụng và xuất phiếu minh chứng vi phạm, loại trừ Trưởng ban QLĐT.

**Architecture:** Áp dụng mô hình Hybrid 2 giai đoạn: Giai đoạn 1 kiểm toán Heuristic bóc tách task chấm bài & chăm sóc SV và áp trần định mức cứng (Cap rule) trên dữ liệu Worklane; Giai đoạn 2 đối soát với telemetry logs LMS AI (thời gian delta T_start - T_end, độ dài nhận xét feedback, và bảng student_care_logs). Tích hợp Exemption Gate loại trừ Trưởng ban QLĐT.

**Tech Stack:** Python 3.12/3.14, Worklane MCP, Pytest, Openpyxl.

---

### Task 1: Thiết Lập Cấu Hình Định Mức & Danh Sách Ngoại Lệ Quản Lý

**Files:**
- Create/Modify: `config/audit_rules.json`
- Test: `tests/regression/test_audit_rules_config.py`

**Step 1: Write the failing test**

```python
import json
import os
import pytest

def test_audit_rules_config_structure():
    config_path = "config/audit_rules.json"
    assert os.path.exists(config_path), "Thiếu file config/audit_rules.json"
    with open(config_path, encoding="utf-8") as f:
        data = json.load(f)
    assert "exemptions" in data
    assert "bachnx@rikkeiacademy.com" in data["exemptions"]["emails"]
    assert "grading_caps" in data
    assert data["grading_caps"]["ai_bulk_approval_hours"] == 0.25
    assert data["grading_caps"]["manual_grading_max_hours"] == 2.0
    assert "student_care" in data
    assert data["student_care"]["minutes_per_student"] == 15
```

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/regression/test_audit_rules_config.py -v`  
Expected: FAIL with "Thiếu file config/audit_rules.json"

**Step 3: Write minimal implementation**

Tạo `config/audit_rules.json`:
```json
{
  "exemptions": {
    "roles": ["management", "acting_head", "director"],
    "emails": [
      "bachnx@rikkeiacademy.com",
      "director@rikkeieducation.com"
    ]
  },
  "grading_caps": {
    "ai_bulk_approval_hours": 0.25,
    "manual_grading_max_hours": 2.0,
    "min_comment_length_for_manual": 30,
    "ai_speed_threshold_seconds_per_submission": 30
  },
  "student_care": {
    "minutes_per_student": 15,
    "min_students_for_half_hour": 2,
    "min_students_for_one_hour": 4
  }
}
```

**Step 4: Run test to verify it passes**

Run: `uv run pytest tests/regression/test_audit_rules_config.py -v`  
Expected: PASS

**Step 5: Commit**

```bash
git add config/audit_rules.json tests/regression/test_audit_rules_config.py
git commit -m "feat(audit): establish audit rules configuration and leadership exemption gate"
```

---

### Task 2: Xây Dựng Engine Kiểm Toán Heuristic & Cắt Giảm Giờ Công (Giai Đoạn 1)

**Files:**
- Create: `pmo/modules/worklane_forensic_audit.py`
- Test: `tests/regression/test_worklane_forensic_audit.py`

**Step 1: Write the failing test**

```python
import pytest
from pmo.modules.worklane_forensic_audit import audit_daily_tasks

def test_exemption_for_acting_head():
    tasks = [{"title": "Chăm sóc sinh viên", "hours": 2.0, "percent": 100}]
    res = audit_daily_tasks("Nguyễn Xuân Bách", "bachnx@rikkeiacademy.com", tasks)
    assert res["is_exempt"] is True
    assert res["effective_hours"] == 2.0
    assert len(res["violations"]) == 0

def test_flag_ai_bulk_grading_inflation():
    tasks = [{"title": "Chấm bài tập về nhà lớp CNTT1", "hours": 2.0, "percent": 100}]
    res = audit_daily_tasks("Thầy A", "teacher_a@rikkei.edu.vn", tasks)
    assert res["is_exempt"] is False
    assert res["effective_hours"] == 0.25
    assert res["deducted_hours"] == 1.75
    assert res["violations"][0]["type"] == "TIME_INFLATION"

def test_flag_ghost_student_care():
    tasks = [{"title": "Chăm sóc sinh viên nghỉ học", "hours": 0.5, "percent": 100}]
    res = audit_daily_tasks("Cô B", "teacher_b@rikkei.edu.vn", tasks)
    assert res["is_exempt"] is False
    assert res["effective_hours"] == 0.0
    assert res["deducted_hours"] == 0.5
    assert res["violations"][0]["type"] == "GHOST_TASK"
```

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/regression/test_worklane_forensic_audit.py -v`  
Expected: FAIL with "ModuleNotFoundError"

**Step 3: Write minimal implementation**

Viết `pmo/modules/worklane_forensic_audit.py`:
- Nạp `config/audit_rules.json`.
- Kiểm tra email thuộc `exemptions.emails` $\rightarrow$ Trả về `is_exempt = True`.
- Với GV/TG: Bóc tách task theo từ khóa `chấm bài`/`btvn` và `chăm sóc`.
- Nếu chấm bài khai $> 0.5h$ mà không ghi rõ chấm tay $\rightarrow$ Cắt về trần `0.25h`, gắn cờ `TIME_INFLATION`.
- Nếu chăm sóc không kèm mã SV $\rightarrow$ Cắt về `0.0h`, gắn cờ `GHOST_TASK`.

**Step 4: Run test to verify it passes**

Run: `uv run pytest tests/regression/test_worklane_forensic_audit.py -v`  
Expected: PASS

**Step 5: Commit**

```bash
git add pmo/modules/worklane_forensic_audit.py tests/regression/test_worklane_forensic_audit.py
git commit -m "feat(audit): implement stage 1 heuristic audit and effective hours calculation"
```

---

### Task 3: Tích Hợp Module Xuất Phiếu Minh Chứng Vi Phạm (Evidence Dossier)

**Files:**
- Modify: `pmo/modules/worklane_forensic_audit.py`
- Test: `tests/regression/test_audit_evidence_dossier.py`

**Step 1: Write the failing test**

```python
import pytest
from pmo.modules.worklane_forensic_audit import generate_evidence_dossier

def test_generate_evidence_dossier():
    audit_results = [{
        "user": "Thầy Nguyễn Văn A",
        "email": "teacher_a@rikkei.edu.vn",
        "date": "2026-11-11",
        "violations": [{
            "type": "TIME_INFLATION",
            "task_title": "Chấm bài tập về nhà lớp CNTT1",
            "claimed_hours": 2.0,
            "effective_hours": 0.25,
            "deducted_hours": 1.75,
            "evidence": {
                "submissions_count": 28,
                "first_checked": "09:23:12",
                "last_checked": "09:30:05",
                "duration_minutes": 6.88,
                "avg_seconds_per_submission": 14.7,
                "manual_comments_count": 0
            }
        }]
    }]
    dossier_text = generate_evidence_dossier(audit_results)
    assert "Thầy Nguyễn Văn A" in dossier_text
    assert "09:23:12" in dossier_text
    assert "09:30:05" in dossier_text
    assert "-1.75h" in dossier_text
```

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/regression/test_audit_evidence_dossier.py -v`  
Expected: FAIL with "generate_evidence_dossier not defined"

**Step 3: Write minimal implementation**

Bổ sung hàm `generate_evidence_dossier` vào `pmo/modules/worklane_forensic_audit.py` để format bảng Markdown và xuất Excel cho Ban Đào tạo.

**Step 4: Run test to verify it passes**

Run: `uv run pytest tests/regression/test_audit_evidence_dossier.py -v`  
Expected: PASS

**Step 5: Commit**

```bash
git add pmo/modules/worklane_forensic_audit.py tests/regression/test_audit_evidence_dossier.py
git commit -m "feat(audit): implement evidence dossier generator with timestamp footprints"
```

---

### Task 4: Tích Hợp CLI & Kết Nối Vào PMO Data Hub

**Files:**
- Modify: `pmo/cli.py`
- Test: `tests/regression/test_audit_cli.py`

**Step 1: Write test for CLI command**

Run lệnh kiểm toán độc lập: `uv run python -m pmo audit-worklane --from 2026-11-09 --to 2026-11-13`  
Expected: In ra bảng tổng hợp giờ hiệu dụng và danh sách minh chứng vi phạm.

**Step 2: Implement CLI argument in `pmo/cli.py`**

**Step 3: Verify and Commit**

```bash
git add pmo/cli.py tests/regression/test_audit_cli.py
git commit -m "feat(cli): add audit-worklane command with forensic evidence reporting"
```
