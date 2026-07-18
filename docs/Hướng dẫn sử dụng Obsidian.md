# Hướng dẫn Sử dụng Hệ thống Báo cáo Học vụ trên Obsidian

Chào mừng bạn đến với hệ thống quản lý tri thức và báo cáo học vụ được tích hợp với **Obsidian**. Việc chuyển đổi thư mục dự án thành một **Obsidian Vault** giúp liên kết động dữ liệu đào tạo và tăng hiệu suất ra quyết định.

---

## 1. Cách thiết lập Obsidian Vault cho dự án

Để bắt đầu xem các báo cáo trực quan và liên kết chéo:
1. Tải và cài đặt [Obsidian](https://obsidian.md/) trên máy tính của bạn.
2. Mở ứng dụng Obsidian, chọn **Open folder as vault** (Mở thư mục dưới dạng Vault).
3. Trỏ tới thư mục dự án: `C:\Users\DELL\Desktop\AI-Agent\AI_PhantichchisoDT`.
4. Nhấn Open. Obsidian sẽ tải toàn bộ cấu trúc báo cáo Markdown hiện có.

---

## 2. Các tính năng cốt lõi được tối ưu hóa cho Obsidian

### 2.1. Liên kết chéo đa chiều (Wiki-links)
*   Trong báo cáo KPI giảng viên tại [report_kpi_gv_tg.md](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/data/report_kpi_gv_tg.md), các lớp học phụ trách đã được tự động định dạng thành liên kết.
*   **Cách dùng**: Nhấp chuột trái vào liên kết lớp học (ví dụ: `[[student_risk_report#HN-K25-CNTT8|HN-K25-CNTT8]]`) để nhảy thẳng đến vùng dữ liệu Care List của lớp đó trong báo cáo sinh viên nguy cơ trượt môn. Nhấn `Alt + Mũi tên trái` để quay lại báo cáo trước đó.

### 2.2. Biểu đồ liên kết Graph View
*   Nhấp vào biểu đồ đồ thị (nút biểu tượng Graph trên thanh công cụ bên trái hoặc nhấn tổ hợp phím `Ctrl + G`).
*   **Lợi ích**: Bạn sẽ nhìn thấy trực quan mối liên kết giữa Giáo viên (GV/TG), Lớp học, Môn học và các học viên thuộc diện Care List. Các tệp báo cáo có nhiều liên kết sẽ xuất hiện dưới dạng các nút lớn (hub), giúp phát hiện nhanh các vùng dữ liệu nóng.

### 2.3. Tương tác "Human-in-the-loop" (Ghi chú bổ sung)
*   Hệ thống sinh báo cáo tự động hàng tuần nhưng **không ghi đè các ghi chú cá nhân** nếu bạn lưu chúng đúng cách.
*   **Cách làm**: Bạn có thể tạo một thư mục mới ví dụ `notes/` trong Obsidian và tạo các tệp ghi chú như `Nhật ký hỗ trợ học viên Nguyễn Văn A.md`. Bạn chỉ cần chèn liên kết `[[student_risk_report#Nguyễn Văn A]]` để tạo mối liên kết ngược (Backlink). Obsidian sẽ tự động ghi nhận liên kết này và hiển thị ở phần Backlinks của báo cáo chính.

---

## 3. Khuyến nghị cài đặt thêm Plugin cho Obsidian

Để tối ưu hóa hiển thị, hãy cài đặt các plugin cộng đồng (Community Plugins) sau:
1.  **Dataview**: Giúp viết các truy vấn động. Ví dụ, để liệt kê tất cả các lớp có tỷ lệ vi phạm chuyên cần > 15% ngay trên trang chủ:
    ```dataview
    TABLE curr_cc_avg as "Vi phạm chuyên cần %"
    FROM "data"
    WHERE curr_cc_avg > 15
    ```
2.  **Admonition / Obsidian Callouts**: Hỗ trợ hiển thị đẹp mắt các cảnh báo dạng `> [!IMPORTANT]` hay `> [!WARNING]` mà hệ thống AI sử dụng để phân loại rủi ro học viên.
