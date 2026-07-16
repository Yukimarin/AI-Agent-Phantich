# Hiệu chuẩn Mô hình Dự báo Học thuật & Cảnh báo Nguy cơ Đa tầng Implementation Plan

> **For Antigravity:** REQUIRED WORKFLOW: Use `.agent/workflows/execute-plan.md` to execute this plan in single-flow mode.

**Goal:** Triển khai thuật toán dự báo và kiểm chứng chéo cho hai khóa K24 (môn Java Web Service kiểm chứng, AI Application dự báo hiện tại) và K25 (môn Python kiểm chứng, Python Web dự báo hiện tại) tích hợp hệ số phạt môi trường và Care List nguy cơ đa tầng, sau đó xuất bản thành báo cáo HTML Dashboard.

**Architecture:** Viết một script chuyên biệt `scratch/run_cross_validation_predictions.py` kết nối tới cổng MySQL 3307 để xử lý dữ liệu học tập và Excel, áp dụng hệ số phạt môi trường tuyến tính và siêu tham số Grid Search tối ưu để tính xác suất đỗ, xuất báo cáo Markdown kiểm chứng và danh sách Care List 3 cấp độ nguy cơ (Cao/Trung bình/Thấp) cho môn hiện tại. Sau đó, viết script `scratch/export_prediction_dashboard_html.py` để xuất bản giao diện HTML Dashboard.

**Tech Stack:** Python, `mysql-connector-python`, `openpyxl`, `markdown`, HTML/CSS.

---

### Task 1: Phát triển Chương trình Dự báo & Kiểm chứng chéo (`scratch/run_cross_validation_predictions.py`)

**Files:**
- Create: `scratch/run_cross_validation_predictions.py`

**Step 1: Viết mã nguồn triển khai dự báo & kiểm chứng chéo**
Tạo file `scratch/run_cross_validation_predictions.py` với logic:
- Kết nối MySQL cổng 3307.
- Đọc dữ liệu Excel chốt từ `docs/PTIT_Chiso.xlsx`.
- Tính toán tỷ lệ vi phạm trung bình của lớp $V_{class}$ để áp dụng hệ số phạt môi trường tuyến tính:
  $$Multiplier_{env} = \max(0.90, 1.0 - 0.5 \times (V_{class} - 10\%)) \quad (\text{nếu } V_{class} > 10\%)$$
- Áp dụng trọng số và tham số tối ưu Grid Search:
  - K24: w1=0.40, w2=0.60 | Prereq Pass = 0.98, Fail = 0.10 | Hack_mult = 1.25.
  - K25: w1=0.00, w2=1.00 | Prereq Pass = 0.85, Fail = 0.10 | Hack_mult = 1.30 | base_scale = 0.95.
- Thực hiện kiểm chứng chéo (so sánh dự báo vs thực tế DB và tính MAE):
  - K24: Môn Java Web Service (ID 211)
  - K25: Môn Python (ID 124 / 103B)
- Thực hiện dự báo môn hiện tại (chặn cứng cấm thi quy chế mới đối với Luật mới):
  - K24: Môn AI Application (ID 212)
  - K25: Môn Python Web (ID 215)
- Phân loại học viên nguy cơ môn hiện tại thành 3 mức độ (Đỏ/Vàng/Xanh):
  - Đỏ (Cao): Cấm thi (Vắng > 20%, Nợ bài tập > 20%, Elearning > 3 bài) hoặc xác suất < 30%.
  - Vàng (Trung bình): Cận cấm thi (Vắng 10-20%, Nợ bài tập 15-20%, Elearning 2-3 bài), nghỉ/nợ liên tiếp >= 2 buổi, hoặc xác suất 30-50%.
  - Xanh (Thấp): Xác suất 50-60%.
- Xuất dữ liệu báo cáo ra:
  - `reports/khoi_k24_k25_predictions.md`
  - `reports/student_care_list_multi_level.md`
  - `scratch/predictions_cv_data.json` (phục vụ dashboard)

**Step 2: Chạy kiểm tra để đảm bảo code hoạt động không có lỗi cú pháp**
Run: `python -m py_compile scratch/run_cross_validation_predictions.py`
Expected: PASS (không có lỗi cú pháp)

---

### Task 2: Chạy Chương trình để tạo Báo cáo Markdown

**Files:**
- Modify: `reports/khoi_k24_k25_predictions.md` [NEW]
- Modify: `reports/student_care_list_multi_level.md` [NEW]

**Step 1: Thực thi chương trình dự báo**
Run: `uv run --with mysql-connector-python --with openpyxl python scratch/run_cross_validation_predictions.py`
Expected: Output hiển thị quá trình chạy thành công, tính toán MAE kiểm chứng và ghi nhận báo cáo.

**Step 2: Xác minh tệp báo cáo sinh ra**
- Đọc `reports/khoi_k24_k25_predictions.md` để xác minh sai số MAE của môn kiểm chứng (Java Web Service và Python) đã giảm dưới 15%.
- Đọc `reports/student_care_list_multi_level.md` để đảm bảo sinh viên nguy cơ được chia nhóm Đỏ, Vàng, Xanh rõ ràng.

---

### Task 3: Phát triển Dashboard HTML xuất bản kết quả

**Files:**
- Create: `scratch/export_prediction_dashboard_html.py`

**Step 1: Viết mã nguồn xuất bản HTML**
Tạo file `scratch/export_prediction_dashboard_html.py` với logic:
- Đọc dữ liệu từ `scratch/predictions_cv_data.json` và hai file Markdown báo cáo.
- Tạo giao diện HTML tĩnh premium dùng CSS Glassmorphism, phông chữ Inter, bảng biểu trực quan và hiệu ứng Hover.
- Đầu ra:
  - `output/class_predictions_dashboard.html`
  - `output/student_risk_dashboard.html`

**Step 2: Chạy kiểm tra cú pháp**
Run: `python -m py_compile scratch/export_prediction_dashboard_html.py`
Expected: PASS

---

### Task 4: Chạy Xuất bản Dashboard HTML & Xác minh

**Files:**
- Modify: `output/class_predictions_dashboard.html` [NEW]
- Modify: `output/student_risk_dashboard.html` [NEW]

**Step 1: Thực thi script xuất bản**
Run: `uv run --with markdown python scratch/export_prediction_dashboard_html.py`
Expected: Tạo thành công hai tệp HTML trong thư mục `output/`.

**Step 2: Xác minh trực quan qua Browser**
- Dùng Browser subagent mở hai tệp HTML này để kiểm tra cấu trúc giao diện, màu sắc cảnh báo (Đỏ/Vàng/Xanh) hiển thị đúng thiết kế premium.
