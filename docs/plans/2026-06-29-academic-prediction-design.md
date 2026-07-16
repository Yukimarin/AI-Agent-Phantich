# Tài liệu Thiết kế: Đánh giá & Dự báo Học tập Kết hợp (K24 & K25)

Tài liệu này đặc tả thiết kế mô hình dự báo tỷ lệ qua môn kết hợp giữa tầm nhìn tổng quan lớp học (Phương án A) và kế hoạch chăm sóc học viên chi tiết (Phương án C), tích hợp dữ liệu kỷ luật từ file Excel và kết quả học tập từ MySQL.

---

## 1. Mục tiêu thiết kế
*   **Dự báo tỷ lệ qua môn** ở cấp độ lớp học và khóa học (KS24, KS25) với sai số $< 10\%$.
*   **Xác định sớm** danh sách học viên có nguy cơ trượt (xác suất đỗ $< 50\%$) cùng nguyên nhân cụ thể để giáo vụ/trợ giảng có kế hoạch chăm sóc và hỗ trợ kịp thời.
*   **Tích hợp dữ liệu sạch**: Lấy dữ liệu vi phạm kỷ luật chốt từ file Excel `PTIT_Chiso.xlsx` (Phương án 1 - ngày học cuối cùng) để loại bỏ rác điểm danh trong DB khi sang phần Project.

---

## 2. Mô hình Thuật toán Dự báo Kết hợp (Hybrid Model)

Tỷ lệ qua môn của lớp học ($PR_{class}$) được tính bằng trung bình cộng xác suất đỗ của từng học viên ($p_i$) trong lớp đó:
$$PR_{class} = \frac{1}{N} \sum_{i=1}^{N} p_i$$

### 2.1 Tầng Học viên: Tính xác suất đỗ cá nhân ($p_i$)

Với mỗi học viên $i$ trong lớp, xác suất đỗ $p_i$ được xác định qua các bước sau:

#### Bước 1: Kiểm tra Điều kiện Chặn Cứng thi (Exam Eligibility Gate)
Học viên sẽ bị cấm thi (xác suất đỗ $p_i = 0\%$) nếu vi phạm bất kỳ điều kiện nào sau đây:
*   **Luật cũ (Áp dụng cho dữ liệu lịch sử để kiểm chứng sai số)**:
    - Điểm chuyên cần vắng $> 20\%$ (tức cột `attendance > 20.0` trong `final_results`).
    - Điểm Rpoint $< 80$ (nếu cột `rpoints` trong `final_results` không NULL).
*   **Luật mới (Áp dụng cho môn học mới từ KS25 Python Web, KS25 QTKD sau DTB202, KS24 HN sau AI, KS24 HCM sau Java Web Service)**:
    - Điểm Rpoint $< 80$ (tích lũy Rpoint trong bảng `final_results`).
    - Tỷ lệ chuyên cần $< 80\%$ (vắng $> 20\%$).
    - Tỷ lệ hoàn thành bài tập $< 80\%$ (nợ bài tập $> 20\%$).
    - Số bài vi phạm Elearning $> 3$ bài.

#### Bước 2: Kiểm tra Chốt chặn Project (Project Gate)
*   Nếu học viên chưa nộp hoặc trượt bảo vệ Project (`project = NULL` hoặc `project < 50.0` trên thang 100), học viên đó sẽ bị trượt môn trực tiếp $\rightarrow$ $p_i = 0\%$.
*   *Lưu ý*: Tại thời điểm dự báo (trước khi thi/bảo vệ), trạng thái nộp project/độ hoàn thiện project trên Git sẽ được dùng làm biến số thay thế.

#### Bước 3: Tính toán xác suất đỗ của học viên đủ điều kiện
Nếu học viên vượt qua các chốt chặn trên, xác suất đỗ $p_i$ được tính bằng kết hợp tuyến tính giữa học lực hiện tại và thái độ học tập tích lũy:
$$p_i = w_1 \times P_{prev\_student} + w_2 \times P_{exam\_student}$$
Trong đó:
*   $P_{prev\_student}$: Kết quả môn học trước của riêng sinh viên đó (100% nếu đỗ, 0% nếu trượt). Nếu môn trước không phải môn tiên quyết, ta lấy $(100\% - \text{Tỷ lệ vi phạm kỷ luật chốt môn trước của học viên})$.
*   $P_{exam\_student}$: Điểm thi Hackathon trung bình môn hiện tại của học viên đó (quy đổi về thang %: $\min(100.0, \text{Score} \times 1.25)$).
*   Trọng số tối ưu kiểm nghiệm: $w_1 = 0.42$, $w_2 = 0.58$.

---

## 3. Kiến trúc Dữ liệu & Quy trình Xử lý
1.  **Dữ liệu kỷ luật chốt môn**: Đọc từ sheet tương ứng trong file `docs/PTIT_Chiso.xlsx`. Tìm ngày có cột index lớn nhất có dữ liệu của lớp đó, lấy 3 chỉ số: Chuyên cần, Bài tập, Elearning.
2.  **Dữ liệu điểm số**: Đọc từ bảng `final_results` và `result_test` trong database MySQL.
3.  **Hợp nhất & Phân tích**: Chạy script python để map dữ liệu giữa Excel và DB theo tên lớp đã chuẩn hóa (sử dụng module `excel_loader.py` đã có).
4.  **Xuất báo cáo**:
    - File báo cáo tổng hợp: `reports/academic_predictions_v3.md` (chứa tỷ lệ qua môn dự báo của tất cả các lớp KS24, KS25 ở các môn).
    - File danh sách học viên cần chăm sóc: `reports/student_care_list.md` (danh sách học viên có nguy cơ trượt cao kèm lý do chi tiết).

---

## 4. Kế hoạch Kiểm chứng & Đánh giá Sai số
*   Chạy mô hình dự báo (theo quy tắc luật cũ) trên dữ liệu các môn đã hoàn thành trong DB:
    - **KS25**: Dự báo kết quả môn Database (ID 183) dựa trên môn JS (ID 124).
    - **KS24**: Dự báo kết quả môn Java Web Service (ID 194) dựa trên môn Java Web Application (ID 177).
*   So sánh tỷ lệ qua môn dự báo với kết quả thực tế trong DB để chứng minh sai số trung bình (MAE) đạt $< 10\%$.
