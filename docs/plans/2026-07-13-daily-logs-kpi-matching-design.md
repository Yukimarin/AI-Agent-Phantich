# Tài liệu Thiết kế: Tích hợp Đối chiếu Định mức Thời gian (KPI Master) vào Agent 4

Tài liệu này đặc tả kiến trúc, thuật toán và công thức tính toán điểm hiệu suất báo cáo ngày (Work Score) dựa trên việc đối chiếu định mức thời gian tiêu chuẩn từ các file KPI Master của QTKD và CNTT.

## 1. Dữ liệu nguồn và ánh xạ Role/Rank

Hệ thống tự động tra cứu Vai trò và Cấp bậc (Rank) của nhân sự phòng Đào tạo (39 người) để làm cơ sở đối chiếu định mức:
- **Khối QTKD**: Đọc sheet `STAFF` trong file `C:\Users\DELL\Downloads\_Task Management_ QL Khối QTKD.xlsx` để lấy `Role` và `Rank` của giảng viên/trợ giảng.
- **Khối CNTT & Khối khác**: Đọc sheet `BC hàng ngày` trong file `C:\Users\DELL\Downloads\Quản lý hiệu suất đào tạo.xlsx` để tra cứu Vị trí và Rank.
- **Dự phòng (Fallback)**: Nếu nhân sự mới chưa có thông tin tra cứu, hệ thống tự động gán **Giảng viên - Rank 3** (hoặc Trợ giảng - Rank 3 nếu là trợ giảng) và cảnh báo.

## 2. Dữ liệu định mức tiêu chuẩn (KPI Master)

- **Cấu trúc QTKD**: Đọc sheet `KPI_MASTER` từ file QTKD. Ánh xạ khóa tìm kiếm: `Vị trí` + `Rank` + `Loại công việc` $\rightarrow$ `Standard Time (Minutes)`.
- **Cấu trúc CNTT & Khối khác**: Đọc sheet `Cấu trúc KPI công việc GV. TG` từ file CNTT. Ánh xạ khóa tìm kiếm: `Vị trí` + `Rank` + `Loại công việc` $\rightarrow$ `Thời gian tiêu chuẩn (phút)`.

## 3. Thuật toán so khớp gần đúng (Heuristic Matching)

Áp dụng các mẫu Regex và từ khóa chuẩn hóa để tự động phân nhóm các task tự do khai báo trên Worklane:
- **Giảng dạy lý thuyết**: `giảng dạy`, `dạy lý thuyết`, `lên lớp`, `buổi học` $\rightarrow$ quy đổi thành *"Giảng dạy lý thuyết - Buổi học"* (hoặc *"Triển khai buổi thực hành - Buổi"* nếu là trợ giảng).
- **Chuẩn bị bài học**: `chuẩn bị`, `soạn slide`, `soạn bài`, `soạn giáo án` $\rightarrow$ quy đổi thành *"Chuẩn bị giảng dạy - Buổi học"*.
- **Mindmap**: `mindmap`, `bản đồ tư duy` $\rightarrow$ quy đổi thành *"Làm mindmap bài học - Session"*.
- **Hỗ trợ học viên**: `hỗ trợ`, `support`, `fix bug`, `sửa lỗi`, `hướng dẫn` $\rightarrow$ quy đổi thành *"Báo cáo hỗ trợ SV.HV"* hoặc *"Triển khai hoạt động nhóm - Lớp"*.
- **Khảo thí**: `chấm bài`, `chấm thi`, `chấm vấn đáp`, `trông thi`, `khảo thí` $\rightarrow$ quy đổi thành nhóm *"Khảo thí"* tương ứng.
- **Khác**: Nếu không khớp bất kỳ nhóm nào $\rightarrow$ Thời gian tiêu chuẩn = **30 phút** và gắn cờ cảnh báo `[Đầu việc lạ - Cần rà soát định mức]`.

## 4. Công thức tính điểm Work Score mới

Điểm hiệu suất báo cáo ngày (Work Score) của Agent 4 được cấu thành từ 3 trọng số:

$$\text{Work Score} = (\text{Tỷ lệ nộp báo cáo} \times 40\%) + (\text{Tỷ lệ hoàn thành task} \times 40\%) + (\text{S}_{time} \times 20\%)$$

Trong đó:
- **Tỷ lệ nộp báo cáo**: Số ngày nộp thực tế / 5 ngày làm việc của tuần.
- **Tỷ lệ hoàn thành task**: Số task có trạng thái Done / Tổng số task khai báo.
- **$S_{time}$ (Điểm hợp lý thời gian)**: Bắt đầu từ 100 điểm:
  - Trừ **5 điểm** cho mỗi task khai báo thực tế vượt định mức tiêu chuẩn quá 50% ($H_{actual} > H_{standard} \times 1.5$).
  - Trừ **2 điểm** cho mỗi task lạ chưa được cấu hình định mức (cờ cảnh báo).
  - $S_{time} = \max(0, 100 - \text{Điểm trừ})$.

## 5. Tích hợp báo cáo
- Các task khai báo vượt định mức hoặc task lạ sẽ được liệt kê chi tiết trong file phân tích `data/daily_log_analysis.json`.
- Agent Lead sẽ tự động chèn nhận xét định tính (ví dụ: *"Khai báo vượt định mức ở task X thực tế Y giờ so với định mức Z giờ"*) vào phần đánh giá chi tiết của GV/TG trên báo cáo Markdown `report_kpi_gv_tg.md`.


---
Trở về: [[docs/knowledge_map|Bản đồ Tri thức dự án]]
