# Báo cáo Ghi nhận Phân tích Sai lệch & Hiệu chuẩn Mô hình Dự báo Học vụ

Báo cáo này tài liệu hóa các ghi nhận thực tế, phân tích nguyên nhân sai lệch và kết quả hiệu chuẩn mô hình dự báo học vụ đối với các khóa K24 và K25 dựa trên nguồn dữ liệu mới:
1.  **Excel**: `docs/PTIT_Chiso.xlsx` (đã làm sạch).
2.  **MySQL Database**: `qldt_el` (cổng 3307, đã làm sạch trùng lặp).

---

## 1. Các điểm sai trong phân tích trước đó (Root Causes)

Qua đối chiếu chéo dữ liệu thô trong cơ sở dữ liệu và cấu trúc tệp Excel, chúng tôi đã xác định được 4 điểm sai lệch nghiêm trọng của mô hình cũ:

### 1.1. Lỗi nhận diện sai cột Rpoints chốt trên khóa KS25
*   **Hiện tượng**: Tỷ lệ đỗ dự báo của các lớp KS25 (đặc biệt là nhóm lớp HCM 5, 6, 7, 8) bị kéo tụt xuống mức cực thấp (chỉ khoảng 30% đỗ), tạo ra sai lệch so với thực tế tới **-53%**.
*   **Nguyên nhân**: Khóa KS25 là khóa mới nên trong tệp Excel, các sheet của khóa này (Javascript, Database, Python) **không hề có cột điểm Rpoints chốt** ở cuối sheet. Thuật toán quét ngược tự động đã nhận diện nhầm cột Elearning của một ngày học ngẫu nhiên ở giữa sheet làm cột Rpoints chốt (vì trung bình cột đó tình cờ nằm trong khoảng `[30, 115]`).
*   **Hậu quả**: Điểm Rpoint chốt của cả lớp bị gán sai thành **17.95**, **24.39**, **28.57** (thực tế đây là tỉ lệ vi phạm Elearning). Do điểm Rpoints quá thấp này, mô hình đã ép xác suất đỗ của tất cả học viên về 0% theo luật cấm thi (Rpoint < 80).

### 1.2. Áp đặt quy chế cấm thi Luật cũ quá nghiêm ngặt so với thực tế
*   **Hiện tượng**: Dự báo Luật cũ bị sai số MAE rất cao (~30% - 33%).
*   **Nguyên nhân**: Mô hình cũ tự ý áp dụng quy tắc chặn cứng (ép xác suất đỗ về 0%) khi học viên vi phạm chuyên cần (vắng > 20%) hoặc bài tập (< 80%). Tuy nhiên, dữ liệu thực tế lịch sử trong DB lại chứng minh điều ngược lại:
    *   **58.9%** học viên vắng chuyên cần > 20% thực tế **vẫn đỗ** bình thường.
    *   **38.5%** học viên nợ bài tập > 20% thực tế **vẫn đỗ** bình thường.
    *   **40.1%** học viên có Rpoint < 80 thực tế **vẫn đỗ** bình thường.
*   **Hậu quả**: Việc chặn cứng 0% đối với dự báo lịch sử khiến mô hình trở nên bi quan một cách phi thực tế, trong khi thực tế giảng viên vẫn tạo điều kiện cho thi và học viên vẫn đỗ bình thường.

### 1.3. Lạm dụng công thức kỹ thuật đối với môn Kỹ năng mềm & Thực tập
*   **Hiện tượng**: Các môn như Kỹ năng mềm (SKL) và Thực tập (TTRK) có tỷ lệ dự báo đỗ rất thấp (~35%) trong khi thực tế đỗ gần như tuyệt đối (~90% - 100%).
*   **Nguyên nhân**: Các môn này không có điểm thi Hackathon nặng hay môn học tiên quyết kỹ thuật. Việc ép công thức toán học lập trình vào các môn này tạo ra sai số giả khổng lồ.

### 1.4. Xung đột môi trường MySQL 9.7
*   **Hiện tượng**: MySQL Server 9.7 của hệ thống từ chối khởi động dữ liệu cũ của bản 8.0.46 do không hỗ trợ nâng cấp trực tiếp.
*   **Giải pháp**: Khởi tạo thư mục dữ liệu sạch mới `data/mysql_data_97` bằng `--initialize-insecure` trên cổng **3307** để import sạch SQL dump 1.08 GB mới, tránh xung đột phân quyền và phiên bản.

---

## 2. Kết quả tối ưu hóa siêu tham số (Grid Search)

Bằng cách chạy Grid Search quét toàn bộ các tham số trên tập dữ liệu 225 môn-lớp học thực tế sau khi đã tháo bỏ các chốt chặn cứng Luật cũ và cô lập môn Kỹ năng mềm, chúng tôi đã xác định bộ tham số tối ưu nhất cho từng khóa học:

### 2.1. Khóa K24 (Tập trung kết quả môn trước)
*   **Trọng số**: $w_1$ (Prerequisite) = **0.40** | $w_2$ (Hackathon) = **0.60**
*   **Prereq Pass Base**: **0.98** (Học viên đỗ môn trước có 98% cơ hội đỗ môn sau).
*   **Prereq Fail Base**: **0.10** (Học viên trượt môn trước chỉ có 10% cơ hội đỗ môn sau nếu học bình thường).
*   **Hackathon Multiplier**: **1.25**
*   **Base Scale**: **1.00**
*   **MAE tối thiểu đạt được**: **10.53%** *(giảm mạnh từ 33.32%)*.

### 2.2. Khóa K25 (Tập trung kết quả hiện tại do thiếu lịch sử học tập trước)
*   **Trọng số**: $w_1$ (Prerequisite) = **0.00** | $w_2$ (Hackathon) = **1.00**
*   **Prereq Pass Base**: **0.85**
*   **Prereq Fail Base**: **0.10**
*   **Hackathon Multiplier**: **1.30**
*   **Base Scale (Scale cuối)**: **0.95**
*   **MAE tối thiểu đạt được**: **10.77%** *(giảm mạnh từ 25.09%)*.

---

## 3. Các cải tiến đã triển khai trong Thuật toán

1.  **Sửa logic nhận diện Rpoint chốt**: Chỉ quét tìm cột Rpoint chốt ở phía sau cột ngày học cuối cùng, loại bỏ hoàn toàn việc nhận diện nhầm các cột daily.
2.  **Sửa chốt chặn Luật cũ**: Đặt `p_eligible_old = p_eligible` (không ép về 0% khi vi phạm kỷ luật) để phản ánh đúng thực tế vận hành lịch sử.
3.  **Heuristics cho môn Kỹ năng mềm/Thực tập**: Tự động phát hiện và gán tỷ lệ đỗ dự báo cố định là **93.0%**.
4.  **Tích hợp siêu tham số tối ưu**: Áp dụng các bộ trọng số $w_1, w_2$ và scaling factors riêng biệt cho K24 và K25.
