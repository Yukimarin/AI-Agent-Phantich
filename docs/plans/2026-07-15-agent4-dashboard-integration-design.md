# Thiết Kế Tích Hợp Báo Cáo Agent 4 Vào Web Dashboard (Tab 3)

Tài liệu này đặc tả thiết kế kỹ thuật phục vụ việc dựng lại giao diện Tab 3 (Nhật ký công việc & Tiến độ dự án của Agent 4) bằng Tailwind CSS đồng bộ với Tab 2 và Tab 1 trong bộ ghép tổng hợp của Agent 5.

## 1. Mục tiêu thiết kế
- **Tính đồng nhất**: Sử dụng 100% Tailwind CSS và phong cách Glassmorphism để giao diện Tab 3 hài hòa tuyệt đối với phần còn lại của Unified Dashboard.
- **Tính tương thích**: Hỗ trợ đầy đủ Light Mode và Dark Mode tự động qua cơ chế class `dark:` của Tailwind CSS.
- **Tính trực quan**: Lựa chọn và tích hợp các biểu đồ tương tác phù hợp cho từng phần dữ liệu, giúp Ban quản lý dễ dàng nhận diện lỗi kỷ luật và tiến độ dự án.

## 2. Kiến trúc & Luồng dữ liệu
- **Nguồn dữ liệu**:
  - Dữ liệu Nhật ký & Điểm số: Đọc trực tiếp từ file JSON cấu trúc [daily_log_analysis.json](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/data/daily_log_analysis.json).
  - Dữ liệu Dự án & Issues: Đọc từ file JSON dự án [project_data.json](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/data/project_data.json).
- **Quy trình xử lý**:
  - Script [generate_unified_dashboard.py](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/scratch/generate_unified_dashboard.py) sẽ đọc trực tiếp 2 file JSON trên.
  - Render HTML tĩnh cho cấu trúc bảng và layout bằng Tailwind CSS.
  - Sinh mã JavaScript khởi tạo Chart.js tương ứng, nạp dữ liệu động từ JSON và đính kèm vào cuối trang.

## 3. Chi tiết Giao diện & Biểu đồ (UI/UX)
Giao diện Tab 3 được chia làm 3 phân khu chức năng:

### Phân khu A: Cảnh báo kỷ luật & Tổng quan
- **Cảnh báo hôm trước (Yesterday Alert)**: Thẻ panel màu đỏ `bg-red-500/10 border-red-500/20` hiển thị danh sách giảng viên chưa nộp báo cáo ngày hôm qua.
- **Thống kê tổng quan (Metrics Cards)**: 3 thẻ chỉ số bao gồm: Tổng nhân sự, Điểm Work Score trung bình tháng, Tổng giờ làm việc khai báo tháng.

### Phân khu B: Nhật ký báo cáo ngày (Gồm 2 Sub-tab Tuần & Tháng)
- **Thanh lọc dữ liệu**: Bộ lọc Khối/Nhóm (QTKD, KS24, KS25, HCM, Ngoại ngữ, QLĐT) và ô tìm kiếm tên giảng viên.
- **Bảng dữ liệu**:
  - Sub-tab Tuần: Bảng dữ liệu tuần.
  - Sub-tab Tháng: Bảng dữ liệu tháng.
- **Hệ thống biểu đồ trực quan**:
  - **Biểu đồ Tròn (Doughnut Chart)**: Đặt bên cạnh bảng tuần để phân tích trạng thái công việc (Hoàn thành, Chờ duyệt, Chưa làm/Đang làm, Đã hủy).
  - **Biểu đồ Cột ngang (Horizontal Bar Chart)**: Trực quan hóa điểm Work Score Tháng 7 của nhân sự. Hỗ trợ **lọc động** dữ liệu trên biểu đồ khi người dùng click chọn bộ lọc Khối/Nhóm.
  - **Biểu đồ Đường (Line Chart)**: Thể hiện xu hướng số ca thiếu báo cáo qua từng ngày trong tháng 7 để phát hiện các ngày hay quên nộp báo cáo.

### Phân khu C: Tiến độ dự án & Công việc (Projects & Issues)
- **Dự án cần lưu ý (Off-track)**: Thẻ hiển thị các dự án có Health không tốt.
- **Danh sách công việc quá hạn & sắp đến hạn**: Bảng dữ liệu chi tiết hiển thị mã công việc, tiêu đề, PIC phụ trách, trạng thái và hạn chót.

## 4. Kịch bản kiểm thử (Verification)
- **Tương thích giao diện**: Kiểm tra hiển thị giao diện Tab 3 ở cả hai chế độ Sáng (Light) và Tối (Dark).
- **Tương tác**: Kiểm tra việc chuyển đổi giữa 2 Sub-tab (Tuần/Tháng), thanh tìm kiếm tên, các nút lọc theo Khối/Nhóm (bảng dữ liệu và biểu đồ bar chart phải tự động cập nhật tương ứng).
- **Lập lịch tự động**: Đảm bảo pipeline sinh báo cáo tổng hợp chạy thành công mà không gây lỗi cú pháp Javascript.
