# K26 Behavioral Shift and Intervention Implementation Plan

> **For Antigravity:** REQUIRED WORKFLOW: Use `.agent/workflows/execute-plan.md` to execute this plan in single-flow mode.

**Goal:** Xây dựng hệ thống phân tích chuyển dịch hành vi và can thiệp tân sinh viên K26 gồm File Excel đa sheet phân nhóm tác chiến và Báo cáo HTML trực quan dành cho Giám đốc Đào tạo.

**Architecture:** 
1. Kết nối dữ liệu gốc môn đầu tiên SSK101 (374 SV trên 9 lớp) với các môn học hiện tại (IT108, SKL01, ENG105, SSK102, SSK103) để phân loại 4 nhóm hành vi TH1 (Nguy cơ bỏ học), TH4 (Sốc môn mới), TH2 (Đang cải thiện), TH3 (Đã khắc phục).
2. Tính toán bảng tỷ lệ cải thiện và nhận diện môn gây nghẽn của từng lớp trong 9 lớp K26.
3. Xuất file Excel chuẩn tác chiến `K26_Theo_Doi_Chuyen_Dich_Hanh_Vi_Va_Giai_Phap.xlsx` với 14 sheet (Sheet tỷ lệ cải thiện từng lớp, 4 sheet nhóm tác chiến 5-15p, 9 sheet chi tiết từng lớp).
4. Sinh Dashboard HTML trực quan cao cấp `bao_cao_k26_chuyen_dich_hanh_vi.html` với thẻ chỉ số KPI, biểu đồ xếp hạng tiến độ từng lớp và ma trận hành động PIC/Deadline.

**Tech Stack:** Python 3.14, OpenPyXL, HTML5/CSS3/Vanilla JS, Chart.js.

---

### Task 1: Xây Dựng Engine Xử Lý Dữ Liệu & Phân Loại 4 Nhóm Chuyển Dịch K26

**Files:**
- Create: `scripts/process_k26_behavioral_shifts.py`
- Test: `tests/test_k26_behavioral_shifts.py`

**Step 1: Viết test kiểm tra logic phân loại và tính tỷ lệ cải thiện**
- Kiểm tra tính đúng đắn của logic TH1, TH2, TH3, TH4.
- Kiểm tra công thức Tỷ lệ Cải thiện của từng lớp: `(TH2 + TH3) / Sĩ số`.

**Step 2: Chạy test để xác nhận test chạy**
- Lệnh: `python3.14 -m unittest tests/test_k26_behavioral_shifts.py`

**Step 3: Viết mã nguồn module `process_k26_behavioral_shifts.py`**
- Đọc dữ liệu sinh viên từ `scratch/ks26_v2_clean.json` / LMS statistics.
- Đọc các môn mới từ `data/inputs/PTIT_Chiso.xlsx` (IT108, SKL01, ENG105, SSK102, SSK103).
- Ánh xạ từng sinh viên vào 4 nhóm hành vi TH1–TH4, tính toán độ chuyển dịch $\Delta$.
- Tính bảng chỉ số 9 lớp và lưu cache JSON tại `data/processed/k26_behavioral_analysis.json`.

**Step 4: Chạy test xác nhận pass và kiểm tra kết quả JSON**

**Step 5: Commit mã nguồn Task 1**

---

### Task 2: Xuất Bản File Excel Tác Chiến 14 Sheet

**Files:**
- Create: `scripts/export_k26_behavioral_excel.py`
- Output: `output/dashboards/management/K26_Theo_Doi_Chuyen_Dich_Hanh_Vi_Va_Giai_Phap.xlsx`

**Step 1: Xây dựng script tạo cấu trúc 14 Sheet bằng OpenPyXL**
- Sheet 1: `BANG_CHI_SO_CAI_THIEN_TUNG_LOP` (Xếp hạng 9 lớp, % cải thiện, phân rã TH1–TH4, môn gây nghẽn, mức độ ưu tiên).
- Sheet 2: `TH1_CAN_THIEP_NGAY` (Danh sách SV nguy cơ cao, cột lý do thực tế để điền tại lớp, PIC, Deadline).
- Sheet 3: `TH4_SOC_MON_MOI` (Danh sách SV sốc môn mới, GV bộ môn/Trợ giảng phụ trách).
- Sheet 4: `TH2_DANG_TIEN_BO` (Danh sách SV tiến bộ cần CVHT đôn đốc).
- Sheet 5: `TH3_DA_KHAC_PHUC` (Danh sách SV sạch vi phạm để biểu dương).
- Sheet 6–14: Chi tiết 9 lớp học sắp xếp theo thứ tự ưu tiên gặp mặt: TH1 &rarr; TH4 &rarr; TH2 &rarr; TH3.

**Step 2: Chạy script sinh file Excel**
- Lệnh: `python3.14 scripts/export_k26_behavioral_excel.py`

**Step 3: Kiểm tra định dạng, độ rộng cột, style màu sắc và dữ liệu các sheet**

**Step 4: Commit mã nguồn Task 2**

---

### Task 3: Xây Dựng Dashboard HTML Báo Cáo Giám Đốc Đào Tạo Kèm Biểu Đồ Trực Quan

**Files:**
- Create: `scripts/generate_k26_behavioral_dashboard.py`
- Output: `output/dashboards/management/bao_cao_k26_chuyen_dich_hanh_vi.html`
- Sync: `deploy_web/management/bao_cao_k26_chuyen_dich_hanh_vi.html`

**Step 1: Xây dựng script render HTML với thiết kế Premium SaaS Dashboard**
- 4 Thẻ chỉ số KPI lớn: Tỷ lệ Cải thiện Toàn khóa, Số SV Nguy cơ cao TH1, Số SV Sốc môn mới TH4, Số SV Thích nghi TH3.
- Biểu đồ Chart.js:
  1. Biểu đồ thanh ngang (Horizontal Bar Chart): Xếp hạng Tỷ lệ Cải thiện (%) của 9 lớp K26.
  2. Biểu đồ tròn (Doughnut Chart): Cơ cấu 4 nhóm hành vi TH1–TH4 toàn khóa.
- Bảng tương tác: Bảng Chỉ Số Cải Thiện 9 Lớp K26 (có thanh tiến độ màu).
- Bảng Kế hoạch Hành động Tác chiến: `Nhóm &rarr; Vấn đề &rarr; Giải pháp 5-15p tại lớp &rarr; PIC &rarr; Deadline`.
- Bộ nút chức năng: "Sao chép Tóm tắt Gửi Giám đốc", "Tải File Excel Tác Chiến", "Chế độ Chụp Ảnh Màn Hình (Screenshot Mode)".

**Step 2: Chạy script sinh HTML và đồng bộ sang `deploy_web/`**
- Lệnh: `python3.14 scripts/generate_k26_behavioral_dashboard.py`

**Step 3: Kiểm thử tự động bằng Visual QA để đảm bảo không lỗi console, hiển thị sắc nét**

**Step 4: Commit mã nguồn Task 3**

---

### Task 4: Tích Hợp Vào Báo Cáo Giao Ban Tuần & Cập Nhật Super Memory

**Files:**
- Modify: `scripts/generate_weekly_director_dashboard.py`
- Output: `output/dashboards/management/weekly_director_report.html`
- Sync: `deploy_web/weekly_director_report.html`
- Modify: `docs/super_memory.md`

**Step 1: Cập nhật Tab 3 của Weekly Director Report**
- Bổ sung nút liên kết nhanh và khối tóm tắt "Chẩn đoán Động thái Chuyển dịch Hành vi K26" vào Tab 3.

**Step 2: Chạy lại `generate_weekly_director_dashboard.py`**

**Step 3: Ghi lại bài học kinh nghiệm và quy chuẩn mới vào `docs/super_memory.md`**

**Step 4: Commit toàn bộ hoàn thành**
