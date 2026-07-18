# Tài liệu Thiết kế: Tinh chỉnh Mô hình Dự báo & Danh sách Sinh viên Yếu

**Ngày:** 02/07/2026  
**Tác giả:** Antigravity (AI Coding Assistant)  
**Trạng thái:** ĐÃ DUYỆT (APPROVED)

---

## 1. Mục tiêu thiết kế
*   **Loại bỏ 100% cảnh báo cấm thi ảo:** Đảm bảo không cấm thi học viên ở môn hiện tại chỉ vì kết quả môn học trước của họ bị trượt hoặc cấm thi, nếu môn hiện tại họ tuân thủ tốt kỷ luật.
*   **Tối ưu hóa độ chính xác dự báo (Nâng cao chất lượng dự báo):** Thay đổi cách tính năng lực học tập môn trước từ nhị phân thô sơ (0% hoặc 100%) sang **Điểm thi thực tế trung bình môn trước** của sinh viên đó.
*   **Phân loại rõ diện cảnh báo:** Tách biệt danh sách học viên yếu thành 2 nhóm rõ rệt: Nhóm nguy cơ cấm thi do kỷ luật môn hiện tại và Nhóm nguy cơ trượt do năng lực học lực yếu.

---

## 2. Đặc tả Thuật toán và Logic mới (Mô hình Cải tiến)

### 2.1. Chốt chặn cấm thi môn hiện tại (Exam Eligibility Gate)
Học viên bị cấm thi môn hiện tại (xác suất đỗ \(p_i = 0.0\%\)) **chỉ khi** vi phạm các chốt chặn kỷ luật của **chính môn học hiện tại** (và chỉ xét khi môn hiện tại có số buổi học thực tế > 3 để tránh cảnh báo ảo ở đầu môn):
1.  **Vắng học nhiều:** Tỷ lệ vắng chuyên cần môn hiện tại > 20% (Chuyên cần hiện tại < 80%).
2.  **Nợ bài tập:** Tỷ lệ bài tập nợ môn hiện tại > 20% (Bài tập hoàn thành < 80%) và số lượng bài tập giao thực tế >= 2.
3.  **Lỗi Elearning:** Số bài vi phạm Elearning môn hiện tại > 3 bài.
4.  **Rpoint thấp:** Điểm Rpoint tích lũy môn hiện tại < 80.
5.  **Trượt Project (Chỉ áp dụng cho QTKD):** Điểm Project môn hiện tại < 50.0 (thang 100) khi môn học đã kết thúc hoặc có điểm project.

*Lưu ý:* Tuyệt đối không cấm thi môn hiện tại dựa vào kết quả học tập hoặc chuyên cần môn học trước đó.

### 2.2. Tính toán năng lực học tập môn trước (\(P_{prev\_student}\))
Năng lực học tập môn trước được tính toán mịn hơn dựa trên điểm thi thực tế trung bình môn trước (bao gồm điểm project, trắc nghiệm, tự luận, hackathon):
*   **Nếu đỗ môn trước** (hoặc điểm trung bình thi môn trước >= 50%):
    $$\(P_{prev\_student} = \text{Điểm thi trung bình thực tế môn trước}\)$$
*   **Nếu trượt nhẹ môn trước** (Điểm từ 40% đến < 50%):
    $$\(P_{prev\_student} = \text{Điểm thi trung bình thực tế môn trước}\)$$
    *(vẫn giữ giá trị thực tế như 45%, phản ánh năng lực thực của sinh viên có cải thiện so với mất gốc hoàn toàn).*
*   **Nếu trượt nặng môn trước** (Điểm thi trung bình thực tế môn trước < 40% hoặc bị cấm thi môn trước do vắng > 30%):
    $$\(P_{prev\_student} = 0.0\)$$
*   **Nếu không có dữ liệu điểm thi môn trước:** Fallback về `100.0 - % vắng chốt môn trước`.

---

## 3. Quy chuẩn Báo cáo Danh sách Sinh viên Yếu (student_risk_report.md)

Báo cáo chi tiết sinh viên yếu sẽ chia danh sách của mỗi lớp thành 2 nhóm:

### Nhóm 1: Cảnh báo Kỷ luật (Nguy cơ cấm thi môn hiện tại)
*   **Điều kiện:** Vi phạm ít nhất 1 trong các chốt chặn kỷ luật môn hiện tại (khi số buổi học > 3).
*   **Điểm dự báo:** Gán cứng `0.0%`.
*   **Lý do hiển thị:** Nêu chi tiết lỗi vi phạm thực tế (ví dụ: `"Vắng học nhiều (22.5%)"`, `"Nộp bài tập thấp (72.4% xong)"`, `"Vi phạm Elearning (4 bài)"`).

### Nhóm 2: Cảnh báo Học lực (Nguy cơ trượt môn hiện tại)
*   **Điều kiện:** Không vi phạm kỷ luật môn hiện tại, đi học đầy đủ, nhưng xác suất đỗ dự báo < 50% (do điểm thi Hackathon môn hiện tại thấp hoặc bị hổng kiến thức từ môn trước).
*   **Điểm dự báo:** Giữ nguyên giá trị tính toán thực tế (Ví dụ: `35.4%`, `48.2%`).
*   **Lý do hiển thị:** `"Xác suất đỗ thấp (X.X%)"` kèm ghi chú học thuật: `"[Học lực] Yếu kiến thức nền tảng (Trượt môn trước)"`.

---

## 4. Các file mã nguồn cần sửa đổi
1.  [scratch/analyze_student_risk_real.py](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/scratch/analyze_student_risk_real.py): Cập nhật logic lọc sinh viên yếu, tính điểm năng lực môn trước mịn hơn, loại bỏ chốt chặn cấm thi môn trước, phân loại sinh viên thành 2 nhóm trong Markdown đầu ra.
2.  [scratch/run_academic_predictions_v3.py](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/scratch/run_academic_predictions_v3.py): Đồng bộ hóa logic tính điểm năng lực học tập môn trước mịn hơn cho mô hình dự báo lớp học.
3.  [scratch/generate_three_recent_courses_report.py](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/scratch/generate_three_recent_courses_report.py): Đồng bộ hóa logic dự báo lớp học để đảm bảo tỷ lệ dự báo qua môn ở Mục 2 của Dashboard nhất quán với mô hình cá nhân mới.


---
Trở về: [[Bản đồ Tri thức MOC|Bản đồ Tri thức dự án]]
