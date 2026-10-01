# Thiết Kế: Dashboard Báo Cáo Tuần Giám Đốc Đào Tạo (Weekly Director Report)

> **Mục tiêu**: Xây dựng form báo cáo HTML chuyên biệt, định kỳ hàng tuần dành cho Giám đốc Đào tạo và Ban Điều Hành. Tích hợp toàn diện tình hình 3 khóa (KS24, KS25, KS26), kiểm toán Worklane 40h/tuần và chuyên đề phân tích sâu khóa KS26 môn SSK101 (điều kiện thi, danh sách 37 đơn bảo lãnh, phân nhóm 4 dải tỷ lệ vi phạm của 371 sinh viên).

---

## 1. Kiến Trúc & Vị Trí Lưu Trữ
- **File nguồn**: `output/dashboards/management/weekly_director_report.html`
- **File phát hành (Deploy)**: `deploy_web/weekly_director_report.html` (và link liên kết trong `deploy_web/index.html`)
- **Script tạo báo cáo**: `scripts/generate_weekly_director_dashboard.py`
- **Tích hợp đường ống**: Bổ sung vào `run_pipeline.py` (Bước 4: Management Dashboards) và `Cap_Nhat_Bao_Cao.bat`.

---

## 2. Cấu Trúc Nội Dung Dashboard (2 Phân Hệ Tab Tương Tác)

### Header & Quick Actions
- Tiêu đề: **BÁO CÁO GIAO BAN ĐÀO TẠO TUẦN (WEEKLY EXECUTIVE BRIEFING)**
- Mốc dữ liệu: Chốt ngày làm việc gần nhất (Ví dụ: Tuần 21/09 - 25/09/2026).
- Action Button:
  - **Sao chép Tóm tắt Giao ban (Copy Briefing)**: Click 1 chạm để sao chép toàn bộ text báo cáo rút gọn gửi Zalo/Slack cho BOD.
  - **In / Xuất PDF (Print Friendly)**.
  - **Nút chuyển đổi Dark/Light mode**.

---

### Tab 1: Tổng Quan Điều Hành Tuần (Executive Overview)
1. **Thẻ KPI Vĩ Mô (Hero Metrics)**:
   - Tổng số sinh viên chính quy: **767 SV** (KS24: 181, KS25: 345, KS26: 241).
   - Tỷ lệ vắng chuyên cần trung bình toàn viện: ~14.8%.
   - Tỷ lệ hoàn thành định mức giờ công Worklane (≥40h): **38.1%** (16/42 NS).
   - Số điểm nóng cảnh báo khẩn: **3 điểm nóng** (HN-K24-CNTT3 vắng 33.3%, HN-K25-QTKD1 vắng 56.5%, K26 HCM nợ Elearning 93.5%).

2. **Khung Tổng Hợp 3 Khóa Đào Tạo (Collapsible / Grid)**:
   - **Khóa KS24 (Microservices IT-214)**: Sĩ số 5 lớp, nề nếp ngày 25/09, lớp kiểu mẫu HN2 (vắng 10.26%), lớp cảnh báo HN3 (vắng 33.33%), tiến độ đồ án nước rút.
   - **Khóa KS25 (FastAPI IT105 & MAN107)**: Kết quả hoàn thành Hackathon 25/09, điểm nóng báo động đỏ lớp QTKD1 vắng 56.52% (26/46 SV vắng) và QTKD2 nợ EL 26.19%.
   - **Khóa KS26 (Học tập chủ động SSK101)**: Tiến độ tuần 1, tỷ lệ đủ ĐK thi 71.5% (sau bảo lãnh đạt 80.8%), điểm nghẽn BTVN HN3 (100% nợ) và Elearning khối HCM (93.5% nợ).

3. **Kiểm Toán Tuân Thủ Worklane Tuần (40h/tuần & KPI Master)**:
   - Biểu đồ phân bố giờ công 42 nhân sự (Chart.js).
   - Bảng 26 nhân sự chưa đạt 40h/tuần (nổi bật 7 NS bỏ trống 0.0h).
   - Bảng 34 nhân sự mắc lỗi khai báo ngoài KPI Master / Over-reporting (có trích dẫn task điển hình).

---

### Tab 2: Chuyên Đề Trọng Tâm Khóa KS26 (SSK101 In-depth Audit)
1. **Thống Kê Điều Kiện Dự Thi & Tỷ Lệ Bảo Lãnh (10 Lớp Học)**:
   - Bảng ma trận 10 lớp: Sĩ số | Đủ ĐK trực tiếp | Số SV được bảo lãnh | % Bảo lãnh | Tổng % Đủ ĐK sau bảo lãnh.
   - Chart so sánh tỷ lệ đủ điều kiện trước và sau khi bảo lãnh theo từng lớp.

2. **Phân Nhóm 371 Sinh Viên Theo 4 Dải Tỷ Lệ Vi Phạm (First Week Learning Issues)**:
   - Stacked Bar Chart hiển thị tỷ lệ theo 4 nhóm:
     - Nhóm 1: `[20% - 40%)`
     - Nhóm 2: `[40% - 60%)`
     - Nhóm 3: `[60% - 80%)`
     - Nhóm 4: `[80% - 100%]`
   - Bóc tách theo 3 tiêu chí: Chuyên cần (Vắng), Elearning (Chưa chuẩn bị), Bài tập về nhà (Nợ bài).
   - Đi kèm bảng diễn giải định tính các điểm nóng (HCM1 & HCM2 vi phạm Elearning 95.7% & 91.1%, HN3 nợ BTVN 100%).

3. **Bảng Danh Sách 37 Đơn Bảo Lãnh (Student Guarantee Directory)**:
   - Tính năng lọc theo Lớp (`Tất cả`, `HN1`, `HN2`, `HN3`, `HCM1`, `HCM2`, `QTKD3`, `HCM-QTKD1`).
   - Cột thông tin: Lớp | Họ và Tên | Chuyên cần (%) | Bài tập (%) | Elearning (%) | R-Point | Lý do bảo lãnh & Phương án khắc phục (Nộp bù BTVN, hoàn thành Elearning, kèm bổ sung) | Trạng thái (`Đã duyệt bảo lãnh` / `Cấm thi`).

---

## 3. Kiến Trúc Mã & Dữ Liệu
- Dữ liệu đầu vào:
  - `data/processed/daily_log_analysis.json` & `scratch/week_21_25_audit_result.json` (Worklane 40h).
  - `data/processed/classes_metrics_cache.json` (Số liệu nề nếp KS24, KS25, KS26).
  - `scratch/ks26_detailed_metrics.json` (Dữ liệu học tập 371 SV KS26).
  - Danh sách bảo lãnh từ `scripts/generate_academic_cohort_dashboards.py`.
- Tự động hóa:
  - Khi chạy `python run_pipeline.py`, file script `scripts/generate_weekly_director_dashboard.py` sẽ đọc dữ liệu từ các file cache JSON đã làm sạch và xuất ra file HTML hoàn chỉnh mà không cần fetch lại API tốn thời gian.
