# Design Document: Daily Logs Cross-Verification with Worklane PM & KPI Master

## 1. Overview
Nhằm khắc phục tình trạng nhân sự báo cáo khống tiến độ dự án trên Báo cáo ngày (Daily Logs) mà không có bước xác minh, thiết kế này áp dụng cơ chế xác thực chéo (Cross-check) giữa ba hệ thống: 
1. Daily Logs (Lời khai của nhân sự).
2. Worklane PM (Trạng thái công việc dự án thực tế).
3. KPI Master (Định mức thời gian cho các công việc tác nghiệp/vận hành).

## 2. Core Logic (Matching & Verification)

### 2.1. Phân loại Task
Thuật toán phân tích (`analyze_daily_logs.py`) sẽ phân loại từng task trong báo cáo ngày thành 2 nhóm:
- **Dự án (Project Tasks):** Các task thuộc về phát triển/sản xuất tài nguyên, R&D, v.v. (Có trên Worklane).
- **Tác nghiệp (Ops Tasks):** Các task cố định như Giảng dạy, chấm thi, hỗ trợ sinh viên, v.v. (Có trong KPI Master).

### 2.2. Quy tắc Xác thực Dự án (Worklane Cross-check)
- Khi nhân sự báo cáo một Project Task là "Hoàn thành" (100% / Done) trong Daily Logs.
- Hệ thống sẽ tìm kiếm Task này trong tập dữ liệu `project_issues_worklane.json`.
- Nếu Issue tương ứng trên Worklane đang ở trạng thái khác `DONE` hoặc `COMPLETED`, task đó sẽ bị gắn cờ `UNVERIFIED` (Chưa xác thực).
- **Hình phạt:** Task `UNVERIFIED` sẽ không được cộng vào số lượng task hoàn thành (Completed Tasks). Điều này làm giảm trực tiếp Tỷ lệ Hoàn thành (Completion Rate) của nhân sự, kéo theo Work Score giảm.

### 2.3. Quy tắc Xác thực Tác nghiệp (KPI Master Cross-check)
- Khi nhân sự khai báo thời gian thực hiện một Ops Task.
- Hệ thống đối chiếu với Standard Time (Định mức) trong KPI Master.
- Nếu `Reported_Time > 1.5 * Standard_Time`, task bị gắn cờ `TIME_STOLEN`.
- **Hình phạt:** Trừ trực tiếp 5 điểm vào Time Score cho mỗi lần vi phạm (đã có trong logic hiện tại, sẽ được giữ nguyên và làm rõ trên UI).

## 3. UI/UX Dashboard Updates

### 3.1. Cảnh báo hiển thị (Visual Alerts)
- Tại Tab Dự án (Project Tab), thêm một Panel mới: **"Blacklist: Khai khống tiến độ"**.
- Danh sách này sẽ liệt kê những nhân sự có task bị gắn cờ `UNVERIFIED` (tức là báo cáo xong nhưng hệ thống chưa xong).

### 3.2. Bổ sung thông tin cá nhân
- Trong danh sách Nhân sự Cảnh báo (Low Performance), bổ sung thông tin "Có n task khai khống" bằng thẻ Badge màu đỏ để người quản lý dễ dàng nhận diện.

## 4. Edge Cases & Error Handling
- **Task không khớp tên (Name Mismatch):** Nếu tên task ghi trong báo cáo ngày bị sai khác quá lớn so với Worklane (fuzzy match thất bại), hệ thống có thể cảnh báo "Không tìm thấy task trên Worklane".
- **Dữ liệu Worklane rỗng:** Nếu Worklane API lỗi hoặc `project_issues_worklane.json` không khả dụng, hệ thống sẽ bỏ qua bước check Worklane để tránh làm hỏng luồng chạy, nhưng ghi log cảnh báo.
