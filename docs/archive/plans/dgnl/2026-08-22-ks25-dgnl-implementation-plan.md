# Kế hoạch triển khai Báo cáo ĐGNL KS25 CNTT

> **For Antigravity:** REQUIRED WORKFLOW: Use `.agent/workflows/execute-plan.md` to execute this plan in single-flow mode.

**Goal:** Triển khai xử lý dữ liệu và tạo báo cáo ĐGNL cho khóa KS25 CNTT dưới dạng Dashboard tương tác `outputs/KS25_DGNL_Report.html` và báo cáo chuyên sâu `docs/reports/ks25_dgnl_evaluation_report.md`, tách biệt hoàn toàn dữ liệu & mã nguồn với KS24.

**Architecture:** 
- Tệp sinh dashboard: `src/generate_dashboard_ks25.py`
- Tệp xuất giao diện: `outputs/KS25_DGNL_Report.html`
- Tệp báo cáo chuyên sâu: `docs/reports/ks25_dgnl_evaluation_report.md`

---

### Task 1: Xây dựng bộ Parser bóc tách dữ liệu thi KS25
- Viết logic python trong `src/generate_dashboard_ks25.py` để:
  1. Đọc dữ liệu điểm thi từ `Danh sách thi ĐGNL.xlsx` (lọc học viên KS25/K25 thuộc `Danh sách ĐGNL CNTT`).
  2. Đọc 4 tệp chấm ca thi chi tiết trong `inputs/` để map tên và parse cột `Chi tiết tiêu chí` (Cột 13) bằng Regex.
  3. Ánh xạ 11 tiêu chí thành **5 chiều năng lực cốt lộ**:
     - Python Core & Thuật toán
     - Pydantic Validation
     - SQLAlchemy ORM
     - FastAPI Endpoints
     - Logic nghiệp vụ & Xử lý lỗi
  4. Tính toán điểm trung bình toàn khóa cho từng chiều năng lực và tỷ lệ trượt của 11 tiêu chí.
  5. Phân loại Readiness Level (0 - 3) và định hướng học tập bổ trợ cho từng sinh viên.

---

### Task 2: Thiết kế giao diện Dashboard độc lập cho KS25
- Tạo tệp `outputs/KS25_DGNL_Report.html` với cấu trúc:
  - **Tab 1: Tổng quan (KPIs & Biểu đồ)**:
    - KPIs: Tổng số học viên, Điểm trung bình MCQ (61.38) & Thực hành (26.12), Tỷ lệ trượt thực hành (81.9% - Cảnh báo đỏ).
    - Radar Chart: 5 chiều năng lực cốt lõi của khóa KS25 (Căn chỉnh font/padding nhãn chuẩn).
  - **Tab 2: Danh sách học viên**:
    - Bảng thông tin học viên tinh giản cột, click vào dòng sẽ bung chi tiết 5 điểm năng lực, nhận xét của GV và định hướng bổ trợ.
    - Thanh tìm kiếm và bộ lọc nhanh theo lớp, cơ sở, readiness level.
  - **Tab 3: Đánh giá & Kiến nghị**:
    - Chỉ số độ phù hợp tổng thể (90%) kèm progress bar.
    - Biểu đồ **Bản đồ Điểm nghẽn** hiển thị tỷ lệ trượt chi tiết trên 11 tiêu chí.
    - Đề xuất cải tiến chương trình đào tạo Kỳ III AI-focused (Toán AI, DSA, Applied ML, RAG & LLMs).

---

### Task 3: Tạo báo cáo chuyên sâu & Nghiệm thu
- Tạo tệp báo cáo chuyên sâu `docs/reports/ks25_dgnl_evaluation_report.md`.
- Chạy biên dịch và kiểm tra tính hoạt động của Dashboard trên trình duyệt.
- Kiểm tra tính cô lập hoàn toàn giữa mã nguồn KS24 và KS25.
- Cập nhật tệp theo dõi tiến trình `task.md`.
