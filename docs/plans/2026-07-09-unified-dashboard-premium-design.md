# Tài liệu Thiết kế: Web Dashboard Tích hợp Premium (Glassmorphism, Dark/Light Mode, Chart.js)

Tài liệu này định nghĩa cấu trúc giao diện, cách bố trí biểu đồ và thiết kế kỹ thuật của trang Web Dashboard tích hợp 2 Tab, kết hợp kết quả của cả hai Agent.

---

## 🎨 1. Định hướng Thiết kế Giao diện Premium
*   **Hiệu ứng thị giác (Glassmorphism)**: Các thẻ nội dung (Card) và thanh Header sử dụng lớp phủ mờ kính (`backdrop-blur-md bg-white/75 border-white/45` ở Light Mode và `bg-slate-900/65 border-white/8` ở Dark Mode).
*   **Chế độ Sáng/Tối (Sleek Dark/Light Mode)**: 
    *   Sử dụng class `.dark` trên thẻ `<html>` thông qua Tailwind CSS config.
    *   Tự động lưu cấu hình giao diện ưa thích của người dùng vào `localStorage` hoặc tự động phát hiện tùy chọn của hệ điều hành.
    *   Cung cấp nút chuyển đổi (Switch Mode) tròn xinh xắn ở góc phải Header với biểu tượng Sun/Moon (FontAwesome).
*   **Chuyển Tab mượt mà**: Chuyển đổi ẩn/hiển thị bằng JavaScript cùng hiệu ứng transition mượt mà.
*   **Bo góc & Typography**: Sử dụng font chữ `Inter` từ Google Fonts, các góc được bo tròn mềm mại `rounded-3xl` (24px) tạo cảm giác hiện đại và tinh tế.

---

## 📈 2. Bố trí Biểu đồ & Cấu trúc Tab

### Tab 1: Đánh giá GV/TG & Lớp (Dữ liệu Excel - Agent 1)
*   **Bố cục**: Giữ nguyên vẹn 100% cấu trúc, bảng biểu và báo cáo chi tiết từ tệp gốc `output/kpi_report.html`.
*   **Tương thích Dark Mode**: Chuyển đổi toàn bộ màu sắc nền và chữ của Tab 1 sang màu tối đồng bộ khi bật chế độ Dark Mode bằng cách thay đổi giá trị của các biến CSS động (`--bg-card`, `--text-dark`, `--border`, v.v.).

### Tab 2: Dự báo Học lực & Care List (Dữ liệu DB - Agent 2)
*   **Thống kê MAE các khóa**: Đặt 3 thẻ MAE (K24, K25, QTKD) nổi bật ở trên cùng.
*   **Biểu đồ cột so sánh trực quan (Chart.js)**: 
    *   Bố trí 1 biểu đồ cột ghép (Grouped Bar Chart) hiển thị trực diện bên dưới các thẻ MAE.
    *   Trục X là tên của tất cả các lớp học lịch sử kiểm chứng của 3 khóa. Trục Y là tỉ lệ % đỗ.
    *   Mỗi lớp hiển thị 2 cột cạnh nhau: **Cột màu Indigo** thể hiện Tỷ lệ đỗ Dự báo, và **Cột màu Emerald** thể hiện Tỷ lệ đỗ Thực tế từ DB.
    *   Màu chữ chú thích (legend/axes) và đường lưới (grid lines) của biểu đồ sẽ tự động chuyển màu để hiển thị sắc nét trên cả nền sáng và nền tối.
*   **Dự báo hiện tại & Accordion Care List**:
    *   Bảng dự báo tỉ lệ đỗ môn hiện tại của các lớp (AI Application cho K24, Python Web cho K25, PRJ302 cho QTKD).
    *   Cột cuối cùng chứa nút bấm **"Care List (X)"** hiển thị số lượng sinh viên nguy cơ trượt của lớp đó.
    *   Khi click, dòng chứa bảng danh sách học sinh nguy cơ chi tiết (Mã SV, Họ tên, chuyên cần, bài tập, LMS, % đỗ và lý do chính) sẽ mở rộng trượt xuống ngay dưới lớp học đó, giữ cho giao diện gọn gàng và khoa học.

---

## 🛠️ 3. Thiết kế Kỹ thuật & Đồng bộ Hóa
*   **Đọc dữ liệu tự động**: Script Python `scratch/generate_unified_dashboard.py` sẽ đọc tệp JSON `scratch/predictions_cv_data.json` và tệp HTML `output/kpi_report.html` để render động toàn bộ trang.
*   **Tích hợp Pipeline**: Đưa script sinh dashboard vào cuối tệp `scratch/run_pipeline.py` (Bước 4) để tự động hóa hoàn toàn quy trình cập nhật mỗi khi chạy đường ống chính.


---
Trở về: [[docs/knowledge_map|Bản đồ Tri thức dự án]]
