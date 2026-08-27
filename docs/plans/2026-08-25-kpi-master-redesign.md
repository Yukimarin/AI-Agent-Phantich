# KPI Master Redesign Implementation Plan

> **For Antigravity:** REQUIRED WORKFLOW: Use `.agent/workflows/execute-plan.md` to execute this plan in single-flow mode.

**Goal:** Thống kê toàn bộ công việc thực tế của GV/TG từ 01/07/2026 đến nay, gom nhóm thông minh để đề xuất bổ sung/hiệu chỉnh KPI Master theo Rank và tích hợp giao diện báo cáo vào Master Portal, đồng thời xuất file Excel đề xuất.

**Architecture:** 
1. Xây dựng script Python phân tích `analyze_kpi_opportunities.py` thực hiện gom nhóm bằng NLP/Heuristics từ khóa và khoảng cách chuỗi, đối chiếu định mức cũ và tính giờ trung bình thực tế theo Rank.
2. Tích hợp script phân tích vào pipeline `run_pipeline.py`.
3. Cập nhật `generate_unified_dashboard.py` để render Tab "Thống kê & Đề xuất KPI" tương tác, hỗ trợ bộ lọc và slide-over drawer xem log thô.

**Tech Stack:** Python, openpyxl, Vanilla JS, HTML (Tailwind CSS, Chart.js)

---

### Task 1: Tạo Script Phân tích & Gom nhóm thông minh (`analyze_kpi_opportunities.py`)

**Files:**
- Create: `agents/master/agent_5_master_portal/analyze_kpi_opportunities.py`

**Step 1: Viết script phân tích logic**
Triển khai logic:
- Đọc `data/processed/daily_log_analysis.json` (lấy `"raw_reports"`).
- Nạp KPI Master cũ của CNTT và QTKD từ hai file Excel:
  - CNTT: `C:\Users\DELL\Downloads\Quản lý hiệu suất đào tạo.xlsx` sheet `"Cấu trúc KPI công việc GV. TG"`
  - QTKD: `C:\Users\DELL\Downloads\_Task Management_ QL Khối QTKD.xlsx` sheet `"KPI_MASTER"`
- Xây dựng thuật toán gom nhóm từ khóa `group_tasks_by_keyword(task_title)` sử dụng chuẩn hóa tiếng Việt không dấu và regex/từ điển đồng nghĩa (Nghỉ phép, Làm học liệu video, Họp, Chấm bài, Soạn slide, Trông thi, Hỗ trợ...).
- Tính toán 3 tập dữ liệu:
  1. **Task thực tế**: Toàn bộ task thô kèm cảnh báo (Đúng định mức, Vượt định mức, Chưa có định mức).
  2. **Task tự do**: Các task chưa định mức đã gom nhóm, tính giờ trung bình của từng giảng viên.
  3. **Đề xuất KPI**: Nhóm việc đã gộp, phân theo Rank, tính giờ trung bình đề xuất.
- Xuất file JSON: `data/processed/kpi_opportunities.json`.
- Xuất file Excel đề xuất: `output/reports/proposed_kpi_master.xlsx` chia theo các sheet khối.

**Step 2: Chạy kiểm thử script độc lập**
Run: `uv run agents/master/agent_5_master_portal/analyze_kpi_opportunities.py`
Expected: Tạo thành công `data/processed/kpi_opportunities.json` và `output/reports/proposed_kpi_master.xlsx`.

**Step 3: Commit**
```bash
git add agents/master/agent_5_master_portal/analyze_kpi_opportunities.py
git commit -m "feat: add analyze_kpi_opportunities.py for smart grouping and KPI suggestions"
```

---

### Task 2: Tích hợp vào Pipeline chính (`run_pipeline.py`)

**Files:**
- Modify: `run_pipeline.py`

**Step 1: Thêm bước chạy phân tích KPI cơ hội vào pipeline**
Chèn vào trước bước chạy Agent 5:
```python
    # Bước 4.8: Phân tích cơ hội & đề xuất KPI Master
    run_script(
        "KPI Master Redesign Analysis: Phân tích và đề xuất KPI Master",
        "agents/master/agent_5_master_portal/analyze_kpi_opportunities.py",
        with_deps=["openpyxl", "pandas"]
    )
    validate_output("data/processed/kpi_opportunities.json", "json")
    # Đăng ký đề xuất Excel vào danh sách whitelist của dọn dẹp
```

**Step 2: Chạy pipeline để kiểm thử tích hợp**
Run: `uv run run_pipeline.py`
Expected: Pipeline chạy thành công qua bước 4.8 mà không có lỗi.

**Step 3: Commit**
```bash
git add run_pipeline.py
git commit -m "chore: integrate analyze_kpi_opportunities.py into run_pipeline.py"
```

---

### Task 3: Cập nhật giao diện Master Portal (`generate_unified_dashboard.py`)

**Files:**
- Modify: `agents/master/agent_5_master_portal/generate_unified_dashboard.py`

**Step 1: Nâng cấp script sinh dashboard**
- Đọc file `data/processed/kpi_opportunities.json`.
- Tích hợp một Tab HTML/JS mới: **"Thống kê & Đề xuất KPI"**.
- Code JavaScript client-side để quản lý dữ liệu cho 3 bảng:
  - Bảng 1: Thống kê & Cảnh báo Task thực tế.
  - Bảng 2: Thống kê & Gom nhóm việc tự do.
  - Bảng 3: Đề xuất cập nhật KPI Master mới theo Rank.
- Thêm bộ lọc tương tác: Khối, Vai trò và thanh tìm kiếm.
- Tạo Slide-over Drawer động trượt từ phải sang để hiển thị danh sách log thô khi click vào các dòng công việc.
- Thêm nút tải file Excel đề xuất liên kết tới `/output/reports/proposed_kpi_master.xlsx` (trực tiếp tải file).

**Step 2: Chạy pipeline để xuất bản dashboard**
Run: `uv run run_pipeline.py`
Expected: Sinh thành công portal tại `output/dashboards/core/agent_5_master_portal.html` chứa Tab mới hoạt động bình thường.

**Step 3: Commit**
```bash
git add agents/master/agent_5_master_portal/generate_unified_dashboard.py
git commit -m "feat: add KPI Redesign Tab with interactive tables and drawer to Master Portal"
```

---

### Task 4: Kiểm duyệt trực quan giao diện

**Files:**
- Test: Kiểm duyệt thủ công và chạy visual testing.

**Step 1: Xác thực hiển thị HTML**
Mở file `output/dashboards/core/agent_5_master_portal.html` trên trình duyệt và kiểm tra:
- Khả năng chuyển đổi qua Tab "Thống kê & Đề xuất KPI".
- Kiểm tra dữ liệu hiển thị có đúng 3 bảng như thiết kế.
- Kiểm tra tính năng lọc Khối, Vai trò, và chức năng tìm kiếm.
- Kiểm tra drawer trượt ra hiển thị các log thô chính xác khi click vào dòng công việc.
- Kiểm tra link tải file Excel đề xuất.

**Step 2: Commit**
```bash
git commit --allow-empty -m "docs: complete KPI Master Redesign feature verification"
```
