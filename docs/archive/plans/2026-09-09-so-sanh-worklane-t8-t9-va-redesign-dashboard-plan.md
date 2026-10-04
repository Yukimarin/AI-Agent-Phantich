# Kế Hoạch Triển Khai: Tích Hợp Biểu Đồ So Sánh T8 vs T9 & Redesign Thẻ Chống Tràn Dòng

> **For Antigravity:** REQUIRED WORKFLOW: Use `.agent/workflows/execute-plan.md` to execute this plan in single-flow mode.

**Goal:** Xây dựng cụm biểu đồ Chart.js so sánh đa chiều Tháng 8 vs Tháng 9 (theo Tỷ lệ vênh % và Giờ dôi dư TB/ngày), đồng thời tái cấu trúc giao diện Dashboard chống tràn dòng cho tên thầy cô dài và cập nhật toàn bộ báo cáo liên quan.

**Architecture:** Tạo engine tính toán Delta so sánh T8 vs T9 (`scratch/compute_exact_comparison.py`), tích hợp biểu đồ Chart.js vào `agents/audit/generate_audit_dashboard.py`, áp dụng CSS Flexbox 2 tầng chống tràn dòng cho thẻ Leader và tags, sinh lại `output/dashboards/audit/worklane_staff_audit.html` và cập nhật báo cáo Markdown `docs/reports/2026-09-09-kiem-toan-worklane-01-08-thang-9-theo-kpi-master-moi.md`.

**Tech Stack:** Python 3, Chart.js 4.4, Tailwind CSS, Vanilla JS, OpenPyXL, HTML5.

---

### Task 1: Tính Toán Số Liệu So Sánh T8 vs T9 Chuẩn Hóa Theo 6 Khối & 41 Nhân Sự
- **Mục tiêu:** Tạo script tổng hợp số liệu T8 (20 ngày) và T9 (4 ngày): tỷ lệ vênh %, giờ dôi dư TB/ngày/nhân sự, tỷ lệ nộp log.
- **Tệp:** `scratch/compute_exact_comparison.py`
- **Đầu ra:** `data/processed/worklane_comparison_t8_t9.json`

### Task 2: Tích Hợp Cụm Biểu Đồ So Sánh Chart.js & Tái Cấu Trúc Thẻ Leader Chống Tràn Dòng
- **Mục tiêu:** 
  1. Thêm cụm 2 biểu đồ Chart.js (Tỷ lệ vênh % và Giờ dôi dư TB/ngày/NS) với SaaS gradient fill, custom tooltip glassmorphism.
  2. Tái cấu trúc Header thẻ Leader thành layout 2 tầng: Tầng 1 là Họ tên trọn vẹn, Tầng 2 là Badge Rank & Badge Trạng thái, thiết lập `h-full flex flex-col justify-between`.
  3. Cải tiến tags diện Rà soát Rank & Cắt giờ ảo với `max-w-full truncate`.
- **Tệp:** `agents/audit/generate_audit_dashboard.py` ➔ Sinh `output/dashboards/audit/worklane_staff_audit.html`

### Task 3: Cập Nhật Báo Cáo Chuyên Đề Phân Tích So Sánh T8 vs T9
- **Mục tiêu:** Bổ sung chương phân tích đối chiếu T8 vs T9, bảng so sánh Delta tăng/giảm và biểu đồ ASCII/Mermaid trực quan.
- **Tệp:** `docs/reports/2026-09-09-kiem-toan-worklane-01-08-thang-9-theo-kpi-master-moi.md`

### Task 4: Kiểm Thử Visual Tự Động Bằng Browser Subagent & Hoàn Tất
- **Mục tiêu:** Chạy `browser_subagent` kiểm tra biểu đồ Chart.js vẽ đầy đủ, không tràn dòng tên thầy cô, console không có lỗi.
