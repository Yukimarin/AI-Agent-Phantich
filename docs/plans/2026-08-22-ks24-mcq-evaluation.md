# Đánh giá Chất lượng Đề thi ĐGNL Hợp nhất (KS24) Implementation Plan (V2)

> **For Antigravity:** REQUIRED WORKFLOW: Use `.agent/workflows/execute-plan.md` to execute this plan in single-flow mode.

**Goal:** Gộp Phân tích Trắc nghiệm và Nhận định Tự luận thành một phần duy nhất có tên **"Phân tích & Đánh giá chất lượng đề thi ĐGNL (KS24)"** trên Tab 3. Thiết lập chỉ số **Độ phù hợp tổng thể để triển khai ĐGNL đạt 90%** (do cả MCQ và Tự luận đều có độ phù hợp học thuật 90% so với ôn tập hè, loại bỏ sự nhầm lẫn với bài làm học sinh) và xóa bỏ bảng đối soát cũ.

**Architecture:** Tính toán và render nội dung thống kê MCQ, nhận định Tự luận, và điểm số phù hợp tổng thể (90%) trực tiếp trong `generate_dashboard.py` dưới dạng một Card lớn hợp nhất. Cập nhật các báo cáo markdown liên quan.

**Tech Stack:** Python, HTML, CSS, JS, Chart.js.

---

### Task 1: Cập nhật `src/generate_dashboard.py` để gộp Tab 3 và bổ sung chỉ số 90% phù hợp

**Files:**
- Modify: [generate_dashboard.py](file:///c:/Users/DELL/Desktop/AI-Agent/AI-ĐGNL/src/generate_dashboard.py)

**Step 1: Update HTML content in Tab 3**
Thay thế toàn bộ nội dung của `#tab-curriculum` để:
1. Gộp thống kê trắc nghiệm (MCQ).
2. Thêm nhận định học thuật về đề thi Tự luận (Thực hành) so với ôn tập hè: Chỉ ra rằng các bài toán trong đề thi (thiếu `@Transactional`, tin tưởng tham số client, thiếu kiểm tra quyền sở hữu) thực chất là các lỗi logic nghiệp vụ Spring Boot cơ bản đều nằm trong phạm vi ôn tập hè, đề thi không đòi hỏi các công nghệ nâng cao ngoài phạm vi.
3. Thiết lập Khối đánh giá "Độ phù hợp tổng thể để triển khai ĐGNL đạt **90%**" với thanh tiến độ (Progress bar) trực quan và phần lý giải/khuyến nghị sư phạm.
4. Xóa bỏ hoàn toàn bảng đối soát lệch pha cũ.

**Step 2: Run build script**
Run: `C:\Users\DELL\.local\bin\python3.14.exe src/generate_dashboard.py`
Expected: Output generated successfully.

---

### Task 2: Cập nhật báo cáo chuyên sâu `roadmap_evaluation.md`

**Files:**
- Modify: [roadmap_evaluation.md](file:///c:/Users/DELL/Desktop/AI-Agent/AI-ĐGNL/docs/reports/roadmap_evaluation.md)

**Step 1: Update Section II and III**
Gộp phần đối soát lệch pha và đánh giá trắc nghiệm thành mục: "Đánh giá chất lượng đề thi ĐGNL & Độ phù hợp triển khai (KS24)" với chỉ số 90% và lập luận tương ứng.

---

### Task 3: Cập nhật tài liệu đề xuất trong plans

**Files:**
- Modify: [2026-08-20-KS24-curriculum-proposals.md](file:///c:/Users/DELL/Desktop/AI-Agent/AI-ĐGNL/docs/plans/2026-08-20-KS24-curriculum-proposals.md)
- Modify: [2026-08-21-KS24-curriculum-proposal-design.md](file:///c:/Users/DELL/Desktop/AI-Agent/AI-ĐGNL/docs/plans/2026-08-21-KS24-curriculum-proposal-design.md)

**Step 1: Synchronize modifications**
Cập nhật gộp phần đánh giá đề thi và chỉ số 90% vào hai tài liệu này.

---

### Task 4: Kiểm duyệt visual bằng subagent

**Step 1: Launch browser subagent**
Verify: Dùng browser subagent chụp màn hình Tab 3 để kiểm tra độ hiển thị của khối Đánh giá chất lượng đề thi ĐGNL hợp nhất.
