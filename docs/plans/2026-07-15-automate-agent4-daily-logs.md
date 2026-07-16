# Automate Daily Logs Fetching & Agent 4 Report Upgrade Implementation Plan

> **For Antigravity:** REQUIRED WORKFLOW: Use `.agent/workflows/execute-plan.md` to execute this plan in single-flow mode.

**Goal:** Tự động hóa lấy dữ liệu Worklane vào 7h sáng hàng ngày, hiển thị nhân sự chưa nộp báo cáo ngày hôm trước, thống kê động tuần/tháng (Tháng 7), vẽ biểu đồ hiệu suất Chart.js và xếp hạng nhân sự.

**Architecture:** 
- Tính toán ngày động (yesterday, weekly, monthly working days) bằng Python datetime.
- Quét báo cáo ngày hôm trước để lập danh sách nhân sự thiếu báo cáo.
- Sinh báo cáo HTML/Markdown của Agent 4 với bảng xếp hạng cao/thấp và biểu đồ thanh ngang Chart.js biểu diễn hiệu suất.
- Đăng ký Scheduled Task trong Windows bằng PowerShell và Cron trong hệ thống Agent.

**Tech Stack:** Python 3.14, HTML5, CSS3, Javascript, Chart.js, PowerShell

---

### Task 1: Thiết lập dynamic date calculation và phát hiện thiếu báo cáo ngày hôm trước

**Files:**
- Modify: [analyze_daily_logs_mcp.py](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/scratch/analyze_daily_logs_mcp.py)

**Step 1: Thay thế các ngày hardcoded bằng logic tính toán động**
- Nhập thư viện `datetime` và `timedelta`.
- Xác định `today = datetime.now().date()` (hoặc cấu hình giả lập thời gian nếu chạy test).
- Tính `yesterday = today - timedelta(days=1)`.
- Xác định danh sách ngày trong tuần hiện tại: `dates_weekly` (các ngày làm việc từ Thứ 2 đến `yesterday`).
- Xác định danh sách ngày trong tháng 7: `dates_all` (các ngày làm việc từ `2026-07-01` đến `yesterday`).
- Quét dữ liệu `yesterday_str` trong raw reports để tìm những nhân sự có báo cáo là `None` (chưa nộp).
- Lưu `yesterday`, `missing_yesterday`, `dates_weekly`, và `dates_monthly` vào `data/daily_log_analysis.json`.

**Step 2: Chạy kiểm thử thủ công**
- Chạy: `uv run --with openpyxl scratch/analyze_daily_logs_mcp.py`
- Kiểm tra file `data/daily_log_analysis.json` có các key: `yesterday`, `missing_yesterday`, `dates_weekly`, `dates_monthly` hoạt động đúng đắn.

---

### Task 2: Nâng cấp HTML Dashboard của Agent 4 với Bảng Xếp Hạng & Biểu Đồ Hiệu Suất

**Files:**
- Modify: [generate_agent4_report.py](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/scratch/generate_agent4_report.py)

**Step 1: Tải dữ liệu động từ daily_log_analysis.json**
- Đọc các trường `yesterday`, `missing_yesterday`, `dates_weekly`, `dates_monthly` từ file JSON.
- Xử lý phòng ngừa lỗi `IndexError` nếu danh sách ngày trống (ví dụ: hiển thị "Chưa có dữ liệu" thay vì crash).

**Step 2: Thêm Panel hiển thị nhân sự chưa nộp báo cáo ngày hôm trước**
- Thiết kế một Panel nổi bật có viền đỏ bên trái (`border-left: 5px solid var(--danger)`) hiển thị danh sách các card nhân sự chưa nộp báo cáo của ngày hôm trước. Nếu 100% đã nộp, hiển thị thông báo chúc mừng màu xanh.

**Step 3: Thêm Panel Bảng Xếp Hạng hiệu suất (Top 5 cao nhất / Top 5 thấp nhất)**
- Sắp xếp danh sách nhân sự theo điểm `work_score` tháng 7 giảm dần.
- Trích xuất Top 5 người có điểm cao nhất (green style) và Bottom 5 người có điểm thấp nhất (red style) để hiển thị trong hai cột cạnh nhau.

**Step 4: Thêm Panel Biểu Đồ đo hiệu suất bằng Chart.js**
- Tạo một Canvas mới `#monthlyPerformanceChart`.
- Đẩy mảng tên nhân sự và điểm `work_score` đã sắp xếp giảm dần vào JS.
- Khởi tạo biểu đồ thanh ngang (Horizontal Bar Chart) trong JS với màu sắc tự động tương ứng theo thang điểm (Xanh lá, Tím, Vàng, Đỏ).

**Step 5: Thực thi và kiểm tra**
- Chạy: `uv run python scratch/generate_agent4_report.py`
- Mở `output/4_daily_logs_report.html` để kiểm tra giao diện trực quan.

---

### Task 3: Đồng bộ điểm số và nhận xét vào Agent Lead KPI Report

**Files:**
- Modify: [generate_kpi_report.py](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/scratch/generate_kpi_report.py) (Verify sự hoạt động của pipeline)
- Modify: [generate_unified_dashboard.py](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/scratch/generate_unified_dashboard.py) (Verify sự hoạt động của pipeline)

**Step 1: Kiểm tra tính liên tục của dữ liệu**
- Đảm bảo script `generate_kpi_report.py` và `generate_unified_dashboard.py` vẫn nạp đúng dữ liệu `monthly_stats` mới từ file JSON động để tính toán điểm KPI cuối cùng cho GV/TG.

**Step 2: Chạy toàn bộ pipeline tích hợp**
- Thực thi: `uv run --with mysql-connector-python --with openpyxl --with numpy --with pandas --with markdown scratch/run_pipeline.py`
- Đảm bảo toàn bộ pipeline hoàn thành không có lỗi.

---

### Task 4: Tạo tập lệnh PowerShell tự động lập lịch trên Windows Task Scheduler

**Files:**
- Create: [schedule_task.ps1](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/scratch/schedule_task.ps1)

**Step 1: Viết tập lệnh đăng ký Task Scheduler**
- Thiết lập New-ScheduledTaskAction chạy lệnh `uv run` trỏ tới script `scratch/run_pipeline.py` với thư mục làm việc chính xác.
- Thiết lập trigger chạy hàng ngày lúc 7h sáng (`New-ScheduledTaskTrigger -Daily -At 7:00AM`).
- Đăng ký Scheduled Task có tên `PTIT_Daily_KPI_Fetch`.

**Step 2: Đăng ký Scheduled Job trong Agent**
- Gọi tool `default_api:schedule` của hệ thống để đặt lịch Cron Job hệ thống lúc 7h sáng hàng ngày (`0 7 * * *`).
