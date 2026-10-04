# Weekly Director Report Implementation Plan

> **For Antigravity:** REQUIRED WORKFLOW: Use `.agent/workflows/execute-plan.md` to execute this plan in single-flow mode.

**Goal:** Xây dựng script và giao diện HTML Báo cáo Giao ban Đào tạo Tuần chuyên biệt (`weekly_director_report.html`) dành cho Giám đốc Đào tạo, tích hợp toàn diện tình hình 3 khóa (KS24, KS25, KS26), kiểm toán Worklane 40h/tuần và chuyên đề KS26 (37 đơn bảo lãnh & phân nhóm vi phạm 371 sinh viên).

**Architecture:** Script Python `scripts/generate_weekly_director_dashboard.py` tổng hợp trực tiếp từ các file cache JSON đã chuẩn hóa (`classes_metrics_cache.json`, `week_21_25_audit_result.json`, `ks26_detailed_metrics.json`) để biên dịch ra file HTML độc lập, giàu tính tương tác với 2 Tab (Overview & KS26 Deep-dive), nút sao chép tóm tắt và biểu đồ Chart.js, sau đó tự động đồng bộ sang `deploy_web/`.

**Tech Stack:** Python 3.14, Tailwind CSS, Chart.js, FontAwesome 6, Vanilla JS.

---

### Task 1: Xây dựng script sinh Dashboard Tuần Giám Đốc Đào Tạo
**Files:**
- Create: `scripts/generate_weekly_director_dashboard.py`
- Test Output: `output/dashboards/management/weekly_director_report.html`

**Step 1:** Viết script python nạp dữ liệu từ các cache JSON:
- Tình hình nề nếp KS24, KS25, KS26 chốt 25/09.
- Thống kê 26 NS chưa đạt 40h/tuần và 34 NS khai sai barem KPI Master.
- Thống kê 10 lớp KS26: tỷ lệ đủ ĐK thi, 37 đơn bảo lãnh.
- Phân nhóm 371 SV theo 4 dải vi phạm [20-40%), [40-60%), [60-80%), [80-100%].
- Danh sách chi tiết 37 sinh viên được bảo lãnh có bộ lọc lớp.

**Step 2:** Tích hợp giao diện HTML hiện đại chuẩn SaaS Executive:
- Nút Sao chép Tóm tắt giao ban (Copy Briefing to Clipboard).
- 2 Tab chuyển đổi mượt mà không reload trang.
- Stacked Bar Charts phân bố sinh viên và biểu đồ tròn tỷ lệ dự thi.

---

### Task 2: Tích hợp vào Pipeline và Đồng Bộ Web
**Files:**
- Modify: `run_pipeline.py` (bổ sung bước sinh `weekly_director_report.html` và đồng bộ sang `deploy_web/`)

---

### Task 3: Kiểm thử & Xác Thực Báo Cáo
**Step 1:** Chạy `python scripts/generate_weekly_director_dashboard.py`
**Step 2:** Kiểm tra tính toàn vẹn của file HTML sinh ra và tính tương tác của các nút bấm.
