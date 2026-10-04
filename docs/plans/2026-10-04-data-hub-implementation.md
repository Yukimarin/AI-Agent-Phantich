# Data Hub + Verification Gates — Implementation Plan (Đợt 1: P1 + P2 + khung P3/P5)

> **For Antigravity:** REQUIRED WORKFLOW: Use `.agent/workflows/execute-plan.md` to execute this plan in single-flow mode.

**Goal:** Dựng package `pmo/` gồm Data Agent (lấy dữ liệu 1 lần/kỳ vào kho), Metric Engine Python (port 1:1 từ `lib/lms_fe_formulas.js`), Gate 1 + Gate 2, Module M1 và lệnh `pmo run / verify`.

**Architecture:** Thiết kế tại `docs/plans/2026-10-04-data-hub-verification-design.md`. Script tính, AI nhận định. Mọi module chỉ đọc `data/warehouse/<kỳ>/`. Gate lỗi → dừng, ghi `run_report.md`.

**Tech Stack:** Python 3 (stdlib `urllib`, `json`), pytest, Node (chỉ dùng trong test đối chiếu với bản JS cũ).

---

### Task 1: Khung dự án
- Create: `pyproject.toml` (`[tool.uv] package = false`, dev-dep pytest), `pmo/__init__.py`, `pmo/config.py`
- Token LMS đọc từ biến môi trường / `.env` (`LMS_TOKEN`), **không** hardcode. `.env` vào `.gitignore`.

### Task 2: Metric Engine (TDD)
- Test: `tests/test_lms_fe_parity.py` — chạy cùng fixture qua Node (`lib/lms_fe_formulas.js`) và Python, so sánh kết quả.
- Test: `tests/regression/test_lessons.py` — Bài học #1 (BT chia tổng cả môn), ngưỡng CC `> 10` nghiêm ngặt, ≥80% done=0 ⇒ 0%.
- Create: `pmo/metrics/lms_fe.py`.
- Run: `uv run pytest -q` → PASS.

### Task 3: Kho dữ liệu theo kỳ
- Create: `pmo/warehouse.py` (period ISO-week `YYYY-Www`, đọc/ghi JSON, manifest).
- Test: `tests/test_warehouse.py`.

### Task 4: Registry + Data Agent
- Create: `pmo/registry.py` (nguồn ban đầu: `scratch/ks26_course_material_audit.json`), `pmo/connectors/lms.py`, `pmo/data_agent.py`.
- Raw response lưu `raw/lms/<courseClassId>.json`; cache theo kỳ, `--refresh` để lấy lại.

### Task 5: Gate framework + G1 + G2
- Create: `pmo/gates/base.py`, `pmo/gates/g1_data.py`, `pmo/gates/g2_metrics.py`.
- G1: registry rỗng, courseClassId không hợp lệ, sĩ số 0 trên môn đang theo dõi, thiếu raw, dữ liệu quá hạn.
- G2: bất biến (0–100, count ≤ total), golden set (`tests/golden/*.json`, cảnh báo nếu chưa có).
- Test: `tests/test_gates.py`.

### Task 6: Module M1 Chỉ số lớp
- Create: `pmo/modules/m1_class_health.py` → `result.json` + `summary.json` (≤5KB) + đề xuất theo luật.
- Test: `tests/test_m1.py`.

### Task 7: Orchestrator CLI
- Create: `pmo/cli.py`, `pmo/__main__.py`. Lệnh: `uv run python -m pmo run [--refresh] [--offline]`, `verify`.
- Ghi `output/<kỳ>/run_report.md`.

### Task 8: Skill câu lệnh tự nhiên + tài liệu
- Create: `.agents/skills/run-analytics/SKILL.md`.
- Modify: `.agents/AGENTS.md` (thêm mô hình mới, đánh dấu mô hình cũ đang chuyển đổi), `docs/super_memory.md`.

### Đợt sau (chưa làm trong đợt này)
- P0 golden set do người dùng xác nhận · Connector Worklane + M3 · M2 dự báo · Renderer + G3/G4 · Cắt chuyển.
