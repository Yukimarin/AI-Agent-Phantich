# Báo cáo Tổng hợp Nhân sự HCM Implementation Plan

> **For Antigravity:** REQUIRED WORKFLOW: Use `.agent/workflows/execute-plan.md` to execute this plan in single-flow mode.

**Goal:** Xây dựng script Python tự động tổng hợp hiệu suất công việc của 9 nhân sự Hồ Chí Minh và xuất ra HTML Dashboard dạng SPA tương tự như file mẫu của khối Ngoại ngữ, đồng thời tích hợp vào pipeline của hệ thống.

**Architecture:** 
- Tạo script Python `generate_hcm_report.py` để đọc dữ liệu từ `daily_log_analysis.json` và `project_issues_worklane.json`.
- Lọc và tổng hợp các chỉ số theo tuần (W27 - W34) và tháng cho 9 nhân sự HCM.
- Lọc các dự án và task (issue) có liên quan đến nhóm nhân sự này.
- Đọc template HTML từ `Bao_Cao_Tong_Hop_NN.html`, thay thế biến `D` và các nhãn hiển thị tương ứng của HCM, rồi xuất ra `Bao_Cao_Tong_Hop_HCM.html`.
- Sửa `run_pipeline.py` để tích hợp việc tạo báo cáo HCM này vào đường ống tự động của hệ thống.

**Tech Stack:** Python 3, openpyxl, JSON, HTML/CSS/JS (Vanilla)

---

### Task 1: Tạo Script Python Tổng hợp Dữ liệu và Sinh Báo cáo HTML

**Files:**
- Create: `agents/advanced/management_audit/generate_hcm_report.py`
- Test: `tests/test_hcm_report.py` (Chúng ta sẽ viết một test script nhỏ để kiểm tra dữ liệu đầu ra)

**Step 1: Tạo script python `generate_hcm_report.py`**
Chúng ta sẽ viết code logic đầy đủ cho `generate_hcm_report.py` thực hiện:
- Đọc file JSON nguồn.
- Lọc 9 nhân sự: `"Nguyễn Bá Minh Đạo", "Lê Hà Thanh Sang", "Trần Quốc Tuấn", "Nguyễn Đức Minh", "Đặng Minh Luân", "Lưu Hoàng Xuân Nguyên", "Phan Ngọc Tài", "Nguyễn Ngọc Sơn", "Phạm Viết Hùng"`.
- Định nghĩa `WEEKS_CONFIG` và `KPI_KEYWORDS`.
- Xử lý dữ liệu weekly, monthly cho từng nhân sự (tương tự như logic trong `pipeline_nn.py` nhưng có điều chỉnh bộ lọc cho cơ sở HCM và các từ khóa CNTT).
- Lọc danh sách dự án và các task trễ hạn của nhân sự HCM.
- Đọc template HTML từ `C:\Users\DELL\Desktop\AI-Agent\AI_Report_NN\output\Bao_Cao_Tong_Hop_NN.html`.
- Thay thế biến `D` bằng dữ liệu đã xử lý.
- Sửa đổi các nhãn nhan đề trong file HTML:
  - `"BÁO CÁO TỔNG HỢP KHỐI NGOẠI NGỮ"` -> `"BÁO CÁO TỔNG HỢP NHÂN SỰ HCM (KHỐI CNTT)"`
  - `"Khối Ngoại Ngữ (DT-NN)"` -> `"Khối CNTT - Cơ sở Hồ Chí Minh (CNTT-HCM)"`
  - `"🇯🇵 Tiếng Nhật & 🇬🇧 Tiếng Anh"` -> `"💻 Giảng viên & Trợ giảng"`
  - `"5 Nhân sự (4 Full-time, 1 Thực tập sinh)"` -> `"9 Nhân sự (3 Giảng viên & Leader, 6 Trợ giảng)"`
  - Pill hiển thị:
    - `"🌐 Tất cả Khối NN"` -> `"🌐 Tất cả nhân sự HCM"`
    - `"🇯🇵 Bộ môn Tiếng Nhật"` -> `"👨‍🏫 Giảng viên & Leader"` (lọc `team == "GV_LEADER"`)
    - `"🇬🇧 Bộ môn Tiếng Anh"` -> `"💻 Trợ giảng"` (lọc `team == "TG"`)
    - Thay thế các màu sắc hoặc nhãn bộ môn tương ứng trong JS render của HTML.
- Ghi tệp HTML ra `output/dashboards/advanced/Bao_Cao_Tong_Hop_HCM.html`.

**Step 2: Tạo test script `tests/test_hcm_report.py`**
Chúng ta viết test script để chạy thử `generate_hcm_report.py` và kiểm duyệt xem file HTML có được tạo thành công và chứa biến `D` hợp lệ không.

**Step 3: Chạy test và xác minh**
Chạy lệnh: `uv run python agents/advanced/management_audit/generate_hcm_report.py`
Xác minh: File `output/dashboards/advanced/Bao_Cao_Tong_Hop_HCM.html` được tạo ra, dung lượng > 100KB, chứa đúng các nhãn nhan đề mới và dữ liệu của 9 nhân sự HCM.

---

### Task 2: Tích hợp vào Pipeline Chính `run_pipeline.py`

**Files:**
- Modify: `run_pipeline.py:185-188`

**Step 1: Sửa file `run_pipeline.py`**
Thêm bước 4.7 chạy script `generate_hcm_report.py`:
```python
    # Bước 4.7: Chạy báo cáo tổng hợp nhân sự HCM
    run_script(
        "HCM Summary Report: Báo cáo tổng hợp nhân sự HCM",
        "agents/advanced/management_audit/generate_hcm_report.py",
        with_deps=["openpyxl"]
    )
    validate_output("output/dashboards/advanced/Bao_Cao_Tong_Hop_HCM.html", "html")
```

**Step 2: Chạy kiểm thử đường ống**
Chạy: `uv run run_pipeline.py`
Xác minh: Pipeline chạy hoàn thành tất cả các bước (từ 0 đến 5) mà không có lỗi, và file `Bao_Cao_Tong_Hop_HCM.html` được tạo ra/cập nhật chính xác.
