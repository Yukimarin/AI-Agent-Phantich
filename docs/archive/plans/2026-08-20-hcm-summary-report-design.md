# Thiết kế Báo cáo Tổng hợp Nhân sự HCM (Khối CNTT)

Tài liệu này đặc tả thiết kế hệ thống báo cáo tổng hợp hiệu suất công việc dưới dạng HTML Dashboard SPA cho toàn bộ 9 nhân sự cơ sở Hồ Chí Minh (Khối CNTT).

## 1. Mục tiêu
- Xây dựng Dashboard HTML tự chứa dữ liệu (self-contained SPA) kế thừa giao diện chuyên nghiệp của Khối Ngoại ngữ.
- Tự động hóa quá trình tổng hợp từ các file JSON nguồn có sẵn (`daily_log_analysis.json` và `project_issues_worklane.json`).
- Cung cấp cái nhìn toàn diện về giờ làm việc, tiến độ dự án, tỷ lệ hoàn thành công việc, và kỷ luật tác nghiệp của nhân sự HCM.

## 2. Nhân sự Phạm vi (HCM-CNTT)
Bao gồm 9 nhân sự được chia làm 2 nhóm vai trò:
- **Giảng viên & Leader (GV_LEADER)**:
  1. Nguyễn Bá Minh Đạo (Leader)
  2. Lê Hà Thanh Sang (Giảng viên)
  3. Trần Quốc Tuấn (Giảng viên)
- **Trợ giảng (TG)**:
  4. Nguyễn Đức Minh (Trợ giảng thử việc)
  5. Đặng Minh Luân (Trợ giảng thử việc)
  6. Lưu Hoàng Xuân Nguyên (Trợ giảng)
  7. Phan Ngọc Tài (Trợ giảng thử việc)
  8. Nguyễn Ngọc Sơn (Trợ giảng thử việc)
  9. Phạm Viết Hùng (Trợ giảng)

## 3. Cấu trúc dữ liệu biến `D` (Schema)
Script Python sẽ tổng hợp dữ liệu thành một biến JSON `D` nằm trong thẻ `<script>` của HTML:
- `personnel`: Thông tin chi tiết của 9 nhân sự.
  - Phân nhóm `team`: `"GV_LEADER"` hoặc `"TG"`.
  - Phân loại `work_type`: `"Full-time"` hoặc `"Part-time/Thử việc"`.
  - Định mức `target_hours`: `8.0` cho full-time, `4.0` cho part-time/thử việc.
  - `weekly`: Thống kê theo từng tuần (W27 đến W34).
  - `monthly`: Tổng hợp toàn bộ giai đoạn 35 ngày.
- `weeks`: Định nghĩa nhãn và danh sách ngày của từng tuần (W27 - W34).
- `weekOrder`: Thứ tự tuần `["W27", "W28", ..., "W34"]`.
- `projects`: Các dự án Worklane có sự tham gia của ít nhất một nhân sự trong nhóm 9 người.
- `overdue`: Danh sách các task (issue) trễ hạn của 9 nhân sự.
- `workload`: Số lượng active task của từng người.
- `adhocTasks`: Danh sách các task phát sinh (ad-hoc) không nằm trong định mức chuẩn.
- `totalDays`: Tổng số ngày làm việc kỳ vọng trong giai đoạn (ví dụ: 35).
- `reportDate`: Ngày chạy báo cáo (ngày hôm nay).
- `period`: Khoảng thời gian báo cáo (`01/07/2026 - 21/08/2026`).
- `personDaily`: Chi tiết công việc hàng ngày của từng nhân sự từ `raw_reports`.

## 4. Thuật toán Phân loại & Quy tắc Xử lý
- **Lọc Địa lý / Nhân sự**: Script sẽ chuẩn hóa tên nhân sự không dấu để so khớp chính xác với keys trong `daily_log_analysis.json`.
- **Phân loại KPI Master vs Ad-hoc**:
  Sử dụng tập hợp các từ khóa CNTT và giáo dục để quét tiêu đề task:
  `KPI_KEYWORDS = ["giảng dạy", "thực hành", "lý thuyết", "khảo thí", "đề thi", "chấm thi", "coi thi", "vấn đáp", "chấm bài", "dự giờ", "chăm sóc sinh viên", "họp", "giáo án", "slide", "lesson", "mindmap", "video", "quiz", "bài tập", "chương trình", "microservice", "fastapi", "python", "java", "database", "sql", "hackathon", "project", "demo", "review", "training", "coaching", "mentee", "mentor", "sản xuất tài nguyên", "xây dựng học liệu", "lên kế hoạch", "định hướng"]`
  Nếu task chứa ít nhất một từ khóa thì tính vào giờ KPI Master. Ngược lại tính vào giờ Ad-hoc.
- **Lọc Dự án & Công việc**:
  - Quét 49 dự án Worklane. Lọc ra các dự án mà PIC hoặc có issue assignee thuộc danh sách 9 người HCM.
  - Lọc bỏ các issue ở trạng thái Hủy (`cancel`, `cancelled`, `hủy`).
  - Lọc bỏ các dự án ở trạng thái Hủy.
  - Xác định trễ hạn: task chưa hoàn thành và có `dueDate` nhỏ hơn hoặc bằng ngày hiện tại trong tuần báo cáo.

## 5. Thiết kế Giao diện HTML
- Kế thừa toàn bộ mã nguồn CSS, cấu trúc SPA của `Bao_Cao_Tong_Hop_NN.html`.
- Thay đổi bộ lọc nhóm hiển thị thành:
  - `🌐 Tất cả nhân sự HCM`
  - `👨‍🏫 Giảng viên & Leader` (lọc theo `team == "GV_LEADER"`)
  - `💻 Trợ giảng` (lọc theo `team == "TG"`)
- Thay đổi nhãn tiêu đề và các icon trang trí cho phù hợp với cơ sở Hồ Chí Minh và chuyên ngành CNTT.
- Đảm bảo tính năng in PDF/Xuất file hoạt động bình thường.
