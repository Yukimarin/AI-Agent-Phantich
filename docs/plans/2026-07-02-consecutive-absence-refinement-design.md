# Tài liệu Thiết kế: Dự báo Cải tiến với Kỷ luật Đa môn, Phạt Nghỉ/Nợ Liên tiếp và Xử lý Học viên Bảo lưu

**Ngày:** 02/07/2026  
**Tác giả:** Antigravity (AI Coding Assistant)  
**Trạng thái:** ĐÃ DUYỆT (APPROVED)

---

## 1. Mục tiêu thiết kế
*   **Đồng bộ hóa 100% chỉ số dự báo lớp học:** Chuyển đổi dự báo lớp học từ mô hình Class-level thô sơ sang trung bình cộng xác suất đỗ của từng học viên trong lớp (\(PR_{class} = \frac{1}{N} \sum p_i\)).
*   **Xử lý nghỉ/nợ liên tiếp ở môn hiện tại:** Phát hiện và phạt điểm dự báo đối với học viên nghỉ học liên tiếp >= 2 buổi hoặc nợ bài tập liên tiếp >= 2 bài ở môn hiện tại.
*   **Kỷ luật đa môn gần nhất:** Tính điểm kỷ luật môn trước (\(discipline\_prev\)) dựa trên trung bình cộng Rpoint của tối đa 2 môn học gần nhất.
*   **Ước lượng điểm thi tối ưu (khi chưa thi):** Ước lượng điểm thi dựa trên tỷ lệ vàng 65% năng lực môn trước + 35% kỷ luật chuyên cần hiện tại.
*   **Xử lý học viên bảo lưu / nghỉ dài hạn:** Tự động phát hiện học viên không học 2 môn gần nhất của lớp để gán điểm học lực/kỷ luật môn trước mặc định ở mức an toàn (\(50.0\) / \(70.0\)) và phạt 15% xác suất đỗ do rủi ro thích nghi lại.

---

## 2. Đặc tả Thuật toán & Mô hình Dự báo Học viên Chi tiết

### 2.1. Điểm Kỷ luật Môn học trước (\(discipline\_prev\))
*   Hệ thống tìm sequence các môn học của lớp trong DB: `seq = class_course_seq[cid]`.
*   Tìm index môn hiện tại: `idx = seq.index(co_id)`.
*   Lấy Rpoint của sinh viên ở tối đa 2 môn trước đó: `prev_co_1 = seq[idx-1]`, `prev_co_2 = seq[idx-2]`.
*   Công thức:
    $$discipline\_prev = \frac{Rpoint_{prev\_1} + Rpoint_{prev\_2}}{2}$$
    *(Nếu chỉ có 1 môn trước, lấy 1 môn; nếu không có môn nào, mặc định 100.0).*

### 2.2. Nhận dạng và Xử lý Học viên Bảo lưu / Nghỉ dài hạn
*   **Điều kiện nhận diện:** Sinh viên không có bất kỳ điểm số/kết quả học tập nào ở cả 2 môn học gần nhất trước đó của lớp (`prev_co_id` và `prev_co_id_2` đều không có trong `final_results` của sinh viên đó).
*   **Thiết lập giá trị đầu vào diện bảo lưu:**
    *   Điểm năng lực môn trước: \(P_{prev\_student} = 50.0\) (mức đỗ tối thiểu).
    *   Điểm kỷ luật môn trước: \(discipline\_prev = 70.0\) (để đưa vào diện theo dõi sát).
    *   Hệ số phạt thích nghi lại: \(penalty\_resumption = 0.85\) (giảm 15% xác suất đỗ).
    *   Lý do hiển thị thêm: `"[Cảnh báo] Học viên mới / quay lại sau bảo lưu"`.

### 2.3. Ước lượng điểm thi Hackathon môn hiện tại (khi chưa thi)
Nếu sinh viên chưa có điểm Hackathon trong DB ở môn hiện tại, điểm thi ước lượng (\(P_{hack\_est}\)) được tính bằng:
$$P_{hack\_est} = 0.65 \times P_{prev\_student} + 0.35 \times discipline\_curr$$
Trong đó:
*   \(P_{prev\_student}\) là điểm thi thực tế môn trước của học viên (nếu thuộc diện bảo lưu thì bằng 50.0).
*   \(discipline\_curr = \max(0.0, 100.0 - \text{att\_val})\) là điểm chuyên cần tích lũy môn hiện tại.
Quy đổi điểm thi về thang %:
$$P_{hack} = \min(100.0, P_{hack\_est} \times 1.25)$$

### 2.4. Phạt Nghỉ học và Nợ bài tập liên tiếp môn hiện tại
Duyệt lịch sử điểm danh và bài tập sắp xếp theo thời gian tăng dần của môn hiện tại:
*   **Phạt Nghỉ học liên tiếp (>=2 buổi gần nhất):**
    *   Hệ số phạt: \(penalty\_abs = 0.5\) (giảm 50% xác suất đỗ).
    *   Lý do vi phạm thêm: `"[Cảnh báo] Nghỉ liên tiếp (X buổi)"`.
*   **Phạt Nợ bài tập liên tiếp (>=2 bài gần nhất):**
    *   Hệ số phạt: \(penalty\_hw = 0.6\) (giảm 40% xác suất đỗ).
    *   Lý do vi phạm thêm: `"[Cảnh báo] Nợ bài tập liên tiếp (Y bài)"`.
*   *Nếu vi phạm cả hai:* Áp dụng đồng thời cả hai hệ số phạt: \(p\_eligible = p\_eligible \times 0.5 \times 0.6\).

### 2.5. Xác suất đỗ hiệu chỉnh cuối cùng (\(p\_eligible\))
*   Học viên bị cấm thi (xác suất đỗ = 0.0%) nếu vi phạm các chốt chặn kỷ luật môn hiện tại (chuyên cần vắng > 20%, nợ bài tập > 20%, vi phạm Elearning > 3 bài, Rpoint < 80, hoặc trượt Project).
*   Học viên đủ điều kiện thi:
    $$p\_eligible = (P_{learning} / \text{CDC}) \times 0.6 + discipline\_val \times 0.4$$
    Sau đó áp dụng các hệ số phạt liên tiếp và bảo lưu:
    $$p\_eligible = p\_eligible \times penalty\_abs \times penalty\_hw \times penalty\_resumption$$
    $$p\_eligible = \min(100.0, \max(0.0, p\_eligible))$$

---

## 3. Các file mã nguồn cần sửa đổi
1.  [scratch/analyze_student_risk_real.py](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/scratch/analyze_student_risk_real.py): Sửa logic tính kỷ luật đa môn, phát hiện bảo lưu, phạt nghỉ/nợ liên tiếp, ước lượng điểm thi và phân bảng Markdown báo cáo sinh viên yếu.
2.  [scratch/run_academic_predictions_v3.py](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/scratch/run_academic_predictions_v3.py): Đồng bộ hóa mô hình tính toán cá nhân cho mô hình dự báo lớp học. Đồng thời sửa đổi để tính tỷ lệ qua môn dự báo của lớp bằng trung bình cộng xác suất đỗ của từng học viên trong lớp.
3.  [scratch/generate_three_recent_courses_report.py](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/scratch/generate_three_recent_courses_report.py): Đồng bộ hóa logic dự báo lớp học tại Mục 1 và Mục 2 của Dashboard sử dụng trung bình cộng xác suất cá nhân thay vì Class-level Model cũ, nhằm đảm bảo số liệu lớp học thay đổi tương ứng và chính xác.
