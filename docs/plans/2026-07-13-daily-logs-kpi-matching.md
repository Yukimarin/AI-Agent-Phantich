# Daily Logs KPI Matching Implementation Plan

> **For Antigravity:** REQUIRED WORKFLOW: Use `.agent/workflows/execute-plan.md` to execute this plan in single-flow mode.

**Goal:** Tích hợp logic đối chiếu định mức thời gian tiêu chuẩn từ KPI Master (QTKD & CNTT) để đánh giá tính hợp lý và tự động tính điểm Work Score động cho các giảng viên/trợ giảng trong dự án AI_PhantichchisoDT.

**Architecture:** 
- Đọc thông tin Role/Rank của nhân sự từ file Excel nguồn (sheet `STAFF` cho QTKD, sheet `BC hàng ngày` cho CNTT).
- Nạp bảng định mức thời gian tiêu chuẩn từ 2 file KPI Master.
- Sử dụng thuật toán so khớp heuristics dựa trên Regex để phân nhóm task, đối chiếu thời gian thực tế khai báo và tính toán điểm hợp lý thời gian ($S_{time}$).
- Cập nhật công thức tính điểm Work Score mới và tích hợp kết quả vào báo cáo KPI Markdown và Web Dashboard.

**Tech Stack:** Python 3.14, openpyxl, pandas, numpy

---

### Task 1: Thiết lập kiểm thử TDD cho logic so khớp Heuristics

**Files:**
- Create: `scratch/test_daily_logs_matching.py`

**Step 1: Viết test case kiểm thử ban đầu**

```python
import unittest
import sys
import os

# Giả lập hàm so khớp
def match_task_category(task_title):
    # Logic mock ban đầu để test fail
    return None

def calculate_time_score(actual_hours, standard_minutes):
    # Logic mock ban đầu để test fail
    return 100

class TestDailyLogsMatching(unittest.TestCase):
    def test_matching_theory(self):
        self.assertEqual(match_task_category("Giảng dạy lý thuyết lớp CNTT2"), "Giảng dạy lý thuyết - Buổi học")
        
    def test_matching_support(self):
        self.assertEqual(match_task_category("Support học viên fix bug code Python"), "Hỗ trợ học viên")

    def test_time_over_reporting(self):
        # Định mức 30 phút (0.5 giờ), khai báo 1.5 giờ -> vượt định mức (over-reporting)
        score = calculate_time_score(1.5, 30)
        self.assertEqual(score, 95) # Bị trừ 5 điểm

if __name__ == '__main__':
    unittest.main()
```

**Step 2: Chạy test để xác nhận kiểm thử thất bại**

Run: `uv run python scratch/test_daily_logs_matching.py`
Expected: FAIL (AssertionError do kết quả trả về là None và 100 thay vì mong muốn)

**Step 3: Viết minimal implementation cho các hàm kiểm thử**

```python
import re

def match_task_category(task_title):
    title_norm = task_title.strip().lower()
    if any(k in title_norm for k in ["giảng dạy", "lên lớp", "dạy lý thuyết"]):
        return "Giảng dạy lý thuyết - Buổi học"
    if any(k in title_norm for k in ["support", "hỗ trợ", "fix bug"]):
        return "Hỗ trợ học viên"
    return None

def calculate_time_score(actual_hours, standard_minutes):
    standard_hours = standard_minutes / 60.0
    score = 100
    if actual_hours > standard_hours * 1.5:
        score -= 5
    return score
```

**Step 4: Chạy lại test để xác nhận kiểm thử vượt qua**

Run: `uv run python scratch/test_daily_logs_matching.py`
Expected: PASS

**Step 5: Commit**

```bash
git add scratch/test_daily_logs_matching.py
git commit -m "test: add TDD test harness for daily logs matching"
```

---

### Task 2: Tích hợp logic nạp KPI Master và đối chiếu định mức vào analyze_daily_logs_mcp.py

**Files:**
- Modify: `scratch/analyze_daily_logs_mcp.py`

**Step 1: Viết test case kiểm thử việc nạp file Excel**

Thêm các test case vào `scratch/test_daily_logs_matching.py` để verify việc đọc thông tin nhân sự và nạp KPI Master từ các đường dẫn Excel thực tế của hệ thống.

**Step 2: Chạy test kiểm tra**

Run: `uv run python scratch/test_daily_logs_matching.py`
Expected: FAIL (do chưa implement logic nạp file thực tế)

**Step 3: Viết minimal implementation trong analyze_daily_logs_mcp.py**

- Thêm logic đọc sheet `STAFF` của file QTKD và sheet `BC hàng ngày` của file CNTT để build dict mapping `staff_info[normalize_name] = {'role': role, 'rank': rank}`.
- Thêm logic đọc sheet `KPI_MASTER` của file QTKD và sheet `Cấu trúc KPI công việc GV. TG` của file CNTT để build dict mapping `kpi_master[key] = standard_time`.
- Triển khai hàm `match_task_category` hoàn chỉnh dựa trên Regex và danh sách nhóm công việc có trong KPI Master.
- Tính toán điểm $S_{time}$ (Time Compliance Score) cho mỗi nhân sự, tích hợp cờ cảnh báo đối với task lạ (Standard Time = 30 phút, trừ 2 điểm).
- Cập nhật công thức tính điểm Work Score mới.
- Lưu chi tiết các task vượt định mức và cờ cảnh báo vào `data/daily_log_analysis.json`.

**Step 4: Chạy test kiểm tra**

Run: `uv run python scratch/test_daily_logs_matching.py` và chạy thử `uv run scratch/analyze_daily_logs_mcp.py`
Expected: PASS (Xuất thành công file `data/daily_log_analysis.json` chứa các chỉ số đối chiếu định mức thời gian).

**Step 5: Commit**

```bash
git add scratch/analyze_daily_logs_mcp.py
git commit -m "feat: integrate KPI Master matching and time compliance scoring"
```

---

### Task 3: Cập nhật Báo cáo HTML Agent 4 (generate_agent4_report.py)

**Files:**
- Modify: `scratch/generate_agent4_report.py`

**Step 1: Viết test case kiểm tra cấu trúc HTML**

Verify xem file output của Agent 4 có chứa cột "Điểm hợp lý thời gian" và hiển thị chi tiết các task vi phạm định mức hay không.

**Step 2: Triển khai code trong generate_agent4_report.py**

- Đọc thông tin đối chiếu thời gian từ `data/daily_log_analysis.json`.
- Render thêm cột **Điểm hợp lý thời gian (Time Score)** trong bảng tổng hợp.
- Highlight màu đỏ (hoặc nhãn Warning) đối với các task khai báo vượt định mức hoặc task lạ chưa được định danh trong bảng chi tiết nhật ký ngày.

**Step 3: Chạy script kiểm tra**

Run: `uv run python scratch/generate_agent4_report.py`
Expected: Báo cáo HTML được sinh thành công tại `output/4_daily_logs_report.html` và hiển thị trực quan các cảnh báo thời gian.

**Step 4: Commit**

```bash
git add scratch/generate_agent4_report.py
git commit -m "feat: enhance Agent 4 report HTML with time compliance alerts"
```

---

### Task 4: Cập nhật Agent Lead (generate_kpi_report.py)

**Files:**
- Modify: `scratch/generate_kpi_report.py`

**Step 1: Sửa đổi generate_kpi_report.py**

- Đọc điểm $S_{time}$ và danh sách vi phạm thời gian từ `data/daily_log_analysis.json`.
- Gắn thêm các nhận xét định tính chi tiết về lỗi khai báo thời gian (ví dụ: *"Khai báo vượt định mức ở task X thực tế Y giờ so với định mức Z giờ"*) vào phần **Điểm yếu / Lỗi vi phạm đã mắc** và **Đề xuất cải thiện** của GV/TG đó.

**Step 2: Chạy script kiểm tra**

Run: `uv run python scratch/generate_kpi_report.py`
Expected: File `data/report_kpi_gv_tg.md` được sinh ra chứa nhận xét định tính động về lỗi định mức thời gian.

**Step 3: Commit**

```bash
git add scratch/generate_kpi_report.py
git commit -m "feat: append dynamic time violation feedback to Master report"
```

---

### Task 5: Chạy đồng bộ Pipeline (run_pipeline.py)

**Files:**
- Modify: `scratch/run_pipeline.py` (Verify bước chạy)

**Step 1: Thực thi toàn bộ pipeline**

Run: `C:\Users\DELL\.local\bin\python3.14.exe scratch/run_pipeline.py`
Expected: PASS, tất cả 6 file HTML được cập nhật và lưu trữ đúng thứ tự trong thư mục `output/`.

**Step 2: Commit**

```bash
git add scratch/run_pipeline.py
git commit -m "feat: run final integrated pipeline with time compliance"
```
