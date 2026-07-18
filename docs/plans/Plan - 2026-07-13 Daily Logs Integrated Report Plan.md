# Daily Logs Integrated Report Implementation Plan

> **For Antigravity:** REQUIRED WORKFLOW: Use `.agent/workflows/execute-plan.md` to execute this plan in single-flow mode.

**Goal:** Tích hợp bộ lọc thời gian Tuần/Tháng, khu vực Critical Alerts quản lý dự án, biểu đồ Chart.js Doughnut vào Dashboard HTML Agent 4, đồng thời cập nhật logic đối chiếu định mức (bỏ qua phạt task lạ) và đồng bộ hóa với báo cáo KPI tổng hợp.

**Architecture:** 
- Đọc dữ liệu báo cáo ngày của 9 ngày trong tháng 7 từ MCP server.
- Tách biệt tính toán điểm số và thống kê cho hai giai đoạn: Tuần (06/07 - 10/07) và Tháng (01/07 - 13/07).
- Cập nhật công thức tính điểm: Bỏ qua task lạ, chỉ trừ điểm khi task khớp và vượt định mức.
- Thiết kế giao diện HTML Dashboard tương tác có sub-tabs chọn Tuần/Tháng sử dụng JS và tích hợp Chart.js Doughnut cho Tab 2 dự án.
- Đồng bộ điểm hiệu suất tháng và nhận xét định tính vào báo cáo KPI Lead Markdown.

**Tech Stack:** Python 3.14, HTML5, CSS3, Javascript, Chart.js, openpyxl, pandas, numpy

---

### Task 1: Thiết lập kiểm thử TDD cho logic tính điểm Tuần/Tháng và Bỏ qua task lạ

**Files:**
- Create: `scratch/test_daily_logs_integrated.py`

**Step 1: Viết test case kiểm thử ban đầu**

```python
import unittest
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Giả lập hàm tính điểm hợp lý thời gian mới
def calculate_time_score_v2(task_list, kpi_master):
    # Logic mock ban đầu để test fail
    return 100

class TestDailyLogsIntegrated(unittest.TestCase):
    def test_wildcard_task_ignored(self):
        # Task 'Task lạ' không có trong master, task 'Giảng dạy' có trong master và hợp lệ
        task_list = [
            {"title": "Task lạ", "hours": 4.0},
            {"title": "Giảng dạy lý thuyết", "hours": 3.0} # Định mức 180 phút (3.0h)
        ]
        kpi_master = {"giảng dạy lý thuyết": 180}
        
        # Điểm thời gian phải đạt 100 (không bị trừ điểm do task lạ)
        score = calculate_time_score_v2(task_list, kpi_master)
        self.assertEqual(score, 100)

    def test_time_violation_only(self):
        # Task 'Giảng dạy' có trong master và khai báo 5.0h (định mức 3.0h) -> vượt định mức (> 1.5 lần)
        task_list = [
            {"title": "Giảng dạy lý thuyết", "hours": 5.0}
        ]
        kpi_master = {"giảng dạy lý thuyết": 180}
        
        # Bị trừ 5 điểm do vượt định mức
        score = calculate_time_score_v2(task_list, kpi_master)
        self.assertEqual(score, 95)

if __name__ == '__main__':
    unittest.main()
```

**Step 2: Chạy test để xác nhận kiểm thử thất bại**

Run: `uv run python scratch/test_daily_logs_integrated.py`
Expected: FAIL (do chưa implement logic tính điểm mới)

**Step 3: Viết minimal implementation cho các hàm kiểm thử**

```python
def calculate_time_score_v2(task_list, kpi_master):
    score = 100.0
    for t in task_list:
        title = t["title"].lower()
        hours = t["hours"]
        
        # Tra cứu kpi_master
        std_time = None
        for key, val in kpi_master.items():
            if key in title:
                std_time = val
                break
                
        if std_time is None:
            # Task lạ: Bỏ qua hoàn toàn, không phạt
            continue
            
        std_hours = std_time / 60.0
        if hours > std_hours * 1.5:
            score -= 5.0
            
    return max(0.0, score)
```

**Step 4: Chạy lại test để xác nhận kiểm thử vượt qua**

Run: `uv run python scratch/test_daily_logs_integrated.py`
Expected: PASS

**Step 5: Commit**

```bash
git add scratch/test_daily_logs_integrated.py
git commit -m "test: add TDD test harness for weekly/monthly matching and scoring"
```

---

### Task 2: Cập nhật analyze_daily_logs_mcp.py để tích hợp tải 9 ngày và phân tách thống kê Tuần/Tháng

**Files:**
- Modify: `scratch/analyze_daily_logs_mcp.py`

**Step 1: Viết test case nạp dữ liệu Tuần/Tháng**

Thêm các test case vào `scratch/test_daily_logs_integrated.py` để verify việc phân tách thống kê tuần (5 ngày) và thống kê tháng (9 ngày) từ một danh sách báo cáo ngày giả lập.

**Step 2: Viết implementation trong analyze_daily_logs_mcp.py**

- Cập nhật danh sách ngày tải: `dates = ["2026-07-01", "2026-07-02", "2026-07-03", "2026-07-06", "2026-07-07", "2026-07-08", "2026-07-09", "2026-07-10", "2026-07-13"]`.
- Khai báo danh sách ngày tuần: `dates_weekly = ["2026-07-06", "2026-07-07", "2026-07-08", "2026-07-09", "2026-07-10"]`.
- Cập nhật hàm `match_kpi_standard_time` để trả về `is_wildcard = True` nếu là task lạ và bỏ qua việc phạt.
- Tách biệt tính toán và tạo ra 2 object stats cho từng nhân sự: `weekly_stats` và `monthly_stats`.
- Xuất file cấu trúc mới tại `data/daily_log_analysis.json`:
  ```json
  {
    "weekly_stats": { "norm_name": { ... } },
    "monthly_stats": { "norm_name": { ... } }
  }
  ```

**Step 3: Chạy test kiểm tra**

Run: `uv run python scratch/test_daily_logs_integrated.py` và chạy thử `uv run --with openpyxl scratch/analyze_daily_logs_mcp.py`
Expected: PASS (Xuất thành công file JSON phân tách tuần/tháng và không còn trừ điểm task lạ).

**Step 4: Commit**

```bash
git add scratch/analyze_daily_logs_mcp.py
git commit -m "feat: split weekly and monthly logs matching and scoring"
```

---

### Task 3: Cập nhật Báo cáo HTML Agent 4 (generate_agent4_report.py)

**Files:**
- Modify: `scratch/generate_agent4_report.py`

**Step 1: Nạp thêm thư viện Chart.js và cấu hình sub-tabs**

- Chèn CDN của Chart.js: `<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>` ở phần `<head>`.
- Thiết kế nút chuyển đổi chế độ xem Tuần/Tháng cho Tab 1.
- Render 2 bảng hiệu suất riêng biệt: `#logs-table-weekly` và `#logs-table-monthly`.
- Render 2 bảng chi tiết lỗi thời gian riêng biệt: `#violations-table-weekly` và `#violations-table-monthly`.
- Render chi tiết nhật ký 5 ngày (chế độ Tuần) và nhật ký tích lũy (chế độ Tháng).

**Step 2: Tích hợp Critical Alerts & Doughnut Chart vào Tab 2**

- Thống kê các dự án `health == 'OFF_TRACK'` và các task overdue có `dueDate <= "2026-07-13"` và `state != 'Hoàn thành'`.
- Render khu vực cảnh báo đỏ (Critical Alerts) ở đầu Tab 2.
- Khởi tạo biểu đồ Doughnut Chart.js hiển thị tỷ lệ trạng thái công việc (Hoàn thành, Chờ duyệt, Chưa làm, Hủy) từ dữ liệu `project_data`.

**Step 3: Viết Javascript tương tác**

- Cập nhật hàm `switchTab` để ẩn/hiển thị linh hoạt giữa chế độ Tuần và Tháng.
- Cập nhật bộ lọc tìm kiếm và bộ lọc khối để hỗ trợ lọc động cho cả bảng tuần và tháng.

**Step 4: Chạy script kiểm tra**

Run: `uv run python scratch/generate_agent4_report.py`
Expected: Dashboard HTML Agent 4 được sinh thành công tại `output/4_daily_logs_report.html` hiển thị đầy đủ sub-tabs Tuần/Tháng, biểu đồ Doughnut động và cảnh báo Critical Alerts.

**Step 5: Commit**

```bash
git add scratch/generate_agent4_report.py
git commit -m "feat: complete integrated weekly/monthly dashboard HTML with Chart.js"
```

---

### Task 4: Cập nhật Agent Lead (generate_kpi_report.py)

**Files:**
- Modify: `scratch/generate_kpi_report.py`

**Step 1: Triển khai code trong generate_kpi_report.py**

- Đọc dữ liệu từ `data/daily_log_analysis.json`, lấy điểm Work Score và danh sách vi phạm từ khóa `monthly_stats` (Chế độ xem Tháng 7 từ 01/07 đến 13/07).
- Tính điểm KPI tổng hợp học kỳ dựa trên điểm Work Score tháng này.
- Append các nhận xét định tính về lỗi vượt định mức thời gian của tháng vào phần Điểm yếu/Đề xuất cải tiến của từng GV/TG.

**Step 2: Chạy script kiểm tra**

Run: `uv run --with pandas --with openpyxl --with numpy --with markdown scratch/generate_kpi_report.py`
Expected: File `data/report_kpi_gv_tg.md` được sinh ra chính xác sử dụng điểm số báo cáo tháng 7.

**Step 3: Commit**

```bash
git add scratch/generate_kpi_report.py
git commit -m "feat: sync monthly Work Score and comments into KPI Master report"
```

---

### Task 5: Chạy đồng bộ Pipeline (run_pipeline.py)

**Files:**
- Modify: `scratch/run_pipeline.py` (Verify bước chạy)

**Step 1: Thực thi toàn bộ pipeline**

Run: `uv run --with mysql-connector-python --with openpyxl --with numpy --with pandas --with markdown scratch/run_pipeline.py`
Expected: PASS, tất cả 6 file HTML được cập nhật và lưu trữ đúng thứ tự trong thư mục `output/`.

**Step 2: Commit**

```bash
git add scratch/run_pipeline.py
git commit -m "feat: run integrated weekly/monthly dashboard pipeline"
```


---
Trở về: [[Bản đồ Tri thức MOC|Bản đồ Tri thức dự án]]
