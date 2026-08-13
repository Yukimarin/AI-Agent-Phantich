# Flexible Weekly Comparison Implementation Plan

> **For Antigravity:** REQUIRED WORKFLOW: Use `.agent/workflows/execute-plan.md` to execute this plan in single-flow mode.

**Goal:** Triển khai cơ chế so sánh chỉ số kỷ luật tuần thông minh (đối chiếu tuần học thực tế gần nhất khi sinh viên nghỉ và đối chiếu môn học liền kề khi bắt đầu môn mới).

**Architecture:** Xây dựng Class Timeline Map từ tất cả các sheet trong Excel, lùi tuần học đối chiếu dựa trên ngày dạy thực tế gần nhất, tự động kết nối môn học trước đó dựa trên dòng thời gian dạy học.

**Tech Stack:** Python, openpyxl, datetime.

---

### Task 1: Xây dựng bản đồ dòng thời gian học tập của lớp học (Class Timeline Map)

**Files:**
* Modify: [`generate_kpi_report.py`](file:///C:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/agents/core/agent_1_class_kpi/generate_kpi_report.py)

**Step 1: Write assertions to verify timeline builder**
Thêm code kiểm thử vào `generate_kpi_report.py` để verify hàm `build_class_timelines` trả về dữ liệu đúng định dạng:
```python
def test_build_class_timelines(wb):
    timelines = build_class_timelines(wb)
    assert isinstance(timelines, dict), "Timeline map must be a dictionary"
    print("test_build_class_timelines: PASS")
```

**Step 2: Run test to verify it fails**
Chạy script: `uv run python agents/core/agent_1_class_kpi/generate_kpi_report.py`
Expected: Fail do `build_class_timelines` chưa định nghĩa.

**Step 3: Implement minimal code for timeline mapping**
Xây dựng hàm `build_class_timelines(wb)` duyệt qua tất cả active sheets, lọc các cột không bị ẩn để lấy ra danh sách ngày học có dữ liệu của từng lớp. Trả về dictionary: `{class_name: {sheet_name: [sorted_dates]}}`.

**Step 4: Run test to verify it passes**
Chạy script: `uv run python agents/core/agent_1_class_kpi/generate_kpi_report.py`
Expected: PASS và in ra "test_build_class_timelines: PASS".

**Step 5: Commit**
```bash
git add agents/core/agent_1_class_kpi/generate_kpi_report.py
git commit -m "feat: add class timeline builder"
```

---

### Task 2: Triển khai Động cơ So sánh Tuần Linh hoạt (Flexible Selector)

**Files:**
* Modify: [`generate_kpi_report.py`](file:///C:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/agents/core/agent_1_class_kpi/generate_kpi_report.py)

**Step 1: Write assertions to verify flexible selector**
Viết hàm test để verify hàm `get_compare_date_range` trả về khoảng ngày đối chiếu chính xác cho hai kịch bản:
1. Có ngày học trong quá khứ của cùng môn học.
2. Không có ngày học quá khứ của môn hiện tại nhưng có môn học khác trước đó.
```python
def test_get_compare_date_range():
    # Thêm asserts verify khoảng ngày
    pass
```

**Step 2: Run test to verify it fails**
Chạy: `uv run python agents/core/agent_1_class_kpi/generate_kpi_report.py`
Expected: Fail do chưa định nghĩa logic lựa chọn tuần.

**Step 3: Implement comparison selector**
Định nghĩa hàm `get_compare_date_range(class_name, sheet_curr, monday_curr, timelines)`:
* Lọc ngày học trong `sheet_curr` trước `monday_curr`. Nếu có, lấy tuần chứa ngày lớn nhất.
* Nếu không, tìm sheet cũ khác có ngày dạy lớn nhất nhỏ hơn `monday_curr`. Lấy tuần cuối của sheet cũ đó.
* Trả về `(monday_prev, sunday_prev, sheet_prev, is_new_subject)`

**Step 4: Run test to verify it passes**
Chạy: `uv run python agents/core/agent_1_class_kpi/generate_kpi_report.py`
Expected: PASS

**Step 5: Commit**
```bash
git add agents/core/agent_1_class_kpi/generate_kpi_report.py
git commit -m "feat: implement flexible comparison engine"
```

---

### Task 3: Cập nhật tích hợp chỉ số tuần mới vào các hàm báo cáo và HTML Dashboard

**Files:**
* Modify: [`generate_kpi_report.py`](file:///C:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/agents/core/agent_1_class_kpi/generate_kpi_report.py)
* Modify: [`generate_report.py`](file:///C:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/agents/core/agent_1_class_kpi/generate_report.py)

**Step 1: Run integration build command**
Chạy: `uv run run_pipeline.py`
Expected: Các chỉ số chênh lệch tuần trong biểu đồ và bảng so sánh tuần của KS24 và QTKD phải hiển thị hợp lý thay vì mặc định so sánh lệch hoặc rỗng.

**Step 2: Implement integration formatting**
Cập nhật hàm `get_weekly_metrics` để lấy dải tuần động theo từng lớp và môn được chọn thay vì dải tuần cứng cho cả nhóm. Cập nhật file HTML sinh ra.

**Step 3: Verify output correctness**
Kiểm tra `output/reports/core/agent_1_student_discipline.md` và `output/dashboards/core/agent_1_student_discipline.html`.

**Step 4: Run full pipeline check**
Chạy: `uv run run_pipeline.py`
Expected: Đường ống chạy hoàn hảo không lỗi, dữ liệu đồng bộ.

**Step 5: Commit**
```bash
git add agents/core/agent_1_class_kpi/
git commit -m "feat: integrate flexible comparison to markdown and HTML reports"
```
