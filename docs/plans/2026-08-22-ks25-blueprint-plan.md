# Quy trình Hướng dẫn ĐGNL KS25 Implementation Plan

> **For Antigravity:** REQUIRED WORKFLOW: Use `.agent/workflows/execute-plan.md` to execute this plan in single-flow mode.

**Goal:** Chốt lại toàn bộ báo cáo KS24 (khóa cứng kết quả) và xây dựng tài liệu quy trình chuẩn hóa (Blueprint) để áp dụng phân tích dữ liệu và lập báo cáo ĐGNL cho khóa KS25 CNTT.

**Architecture:** Tạo tài liệu hướng dẫn quy trình xử lý dữ liệu và tạo báo cáo ĐGNL chuẩn hóa tại `docs/reports/ks25_dgnl_process_guideline.md`. Đảm bảo các tệp tin kết quả KS24 hiện có được giữ nguyên trạng.

**Tech Stack:** Markdown.

---

### Task 1: Khóa cứng báo cáo KS24 và tạo tài liệu quy trình cho KS25

**Files:**
- Create: [ks25_dgnl_process_guideline.md](file:///c:/Users/DELL/Desktop/AI-Agent/AI-ĐGNL/docs/reports/ks25_dgnl_process_guideline.md)

**Step 1: Write process guideline document**
Tài liệu sẽ chi tiết hóa:
1. **Quy trình xử lý dữ liệu thô (Data Processing)**:
   - Các công thức tính điểm final ĐGNL (phân biệt HN vs HCM).
   - Cách mapping tên học viên giữa các file để trích xuất điểm tiêu chí thực hành.
   - Các tiêu chí phân loại mức độ sẵn sàng (Level 0 - 3) và định hướng nghề nghiệp.
2. **Quy trình Đánh giá chất lượng trắc nghiệm (MCQ Evaluation)**:
   - Công thức tính điểm trung bình, độ lệch chuẩn và phân phối dải điểm thang 100.
   - Đánh giá tính phân hóa (Std Dev).
3. **Quy trình Đối soát học thuật & Độ phù hợp (%)**:
   - Phương pháp so sánh nội dung học thuật đề thi vs nội dung ôn tập (không dùng kết quả SV).
   - Công thức tính chỉ số độ phù hợp tổng thể (Weighted Suitability Index).
4. **Quy chuẩn Thiết kế Giao diện (UI/UX Guidelines)**:
   - Quy định thiết kế Radar Chart (Chart.js), bố cục grid, thẻ KPI, thanh tiến độ (Progress bar).

**Step 2: Commit**
Expected: Guideline file created successfully in the project docs.
