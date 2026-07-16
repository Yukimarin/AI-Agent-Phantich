# Design Document: Redesign Prediction Report Interface

**Date:** 2026-06-30  
**Author:** Antigravity (AI Coding Assistant)  
**Status:** PROPOSED

---

## 1. Goal & Context
Hiện tại, báo cáo dự báo tỷ lệ qua môn (`three_recent_courses_report.html`) đang được trình bày dưới dạng bảng truyền thống trải dài và khá thô. Điều này gây khó khăn cho người dùng khi cần chụp ảnh màn hình (screenshot) để dán vào slide báo cáo tuần hoặc báo cáo giao ban (vì nội dung bị cuộn trang quá dài).

Mục tiêu của thiết kế này là **tái cấu trúc toàn bộ giao diện báo cáo** thành một giao diện **Dashboard tối giản, trực quan và hiện đại (Linear-style)**. Thiết kế mới sẽ gom các chỉ số tổng quan lên trên và nén dữ liệu chi tiết của các lớp học xuống dưới bằng biểu đồ thanh mini (Mini Progress Bars), giúp người dùng có thể chụp trọn vẹn toàn bộ báo cáo chỉ trong 1-2 khung hình.

---

## 2. Proposed Design (Executive Dashboard & Compact Tables)

### 2.1. Phần 1: Executive KPI Cards (Widget tổng quan ở đầu trang)
Hiển thị 3 thẻ chỉ số (Cards) lớn nằm ngang đại diện cho 3 khóa học, giúp ban quản trị nắm bắt ngay sai số tổng quan:
*   **Card 1 (Khóa KS24-CNTT)**: Hiển thị chỉ số MAE (ví dụ: `9.50%`) kèm nhãn trạng thái Đạt mục tiêu (màu xanh lá).
*   **Card 2 (Khóa KS25-CNTT)**: Hiển thị chỉ số MAE (ví dụ: `10.48%`) kèm nhãn trạng thái Cần lưu ý (màu vàng).
*   **Card 3 (Khóa KS25-QTKD)**: Hiển thị chỉ số MAE (ví dụ: `20.03%`) kèm nhãn trạng thái Lệch dữ liệu (màu đỏ).

### 2.2. Phần 2: Compact Tables with Mini Progress Bars (Bảng tối giản)
Rút gọn cấu trúc bảng, loại bỏ các cột điểm trung bình, chỉ giữ lại các cột cốt lõi:
1.  **Tên Lớp & GV**: Tên lớp in đậm kèm tên GV phụ trách hiển thị ngay dưới dạng chữ nhỏ màu xám (tiết kiệm 1 cột).
2.  **Môn Học**: Tên môn học hiển thị trực quan.
3.  **So sánh Dự báo vs Thực tế**: Thay thế các con số phần trăm khô khan bằng một **Thanh biểu đồ mini (Mini Progress Bar)**:
    *   Thanh dự báo biểu diễn bằng dải màu Tím nhạt (`#ddd6fe`) với thanh tiến trình Tím đậm (`#7c3aed`).
    *   Thanh thực tế biểu diễn bằng dải màu Xanh nhạt (`#d1fae5`) với thanh tiến trình Xanh đậm (`#10b981`).
    *   Hai thanh chạy song song lồng nhau trong 1 ô giúp so sánh trực tiếp tương quan độ dài của hai chỉ số chỉ bằng mắt thường.
4.  **Sai số (Error Badge)**: Hiển thị độ lệch dưới dạng Badge màu sắc bo góc:
    *   Xanh lá (`#22c55e`): Sai số $\le 10.0\%$.
    *   Đỏ (`#ef4444`): Sai số $> 10.0\%$.

---

## 3. Technical Implementation & Security (No Scripts)
Để đảm bảo file HTML không bị các bộ lọc bảo mật của Catbox.moe chặn (lỗi `Invalid uploader` / `412` do chứa thẻ `<script>` Tailwind CSS), toàn bộ giao diện mới sẽ được xây dựng bằng **HTML5 & CSS3 thuần nội tuyến (Pure CSS & Inline Styles)**:
*   **Typography**: Sử dụng font chữ **Inter** hiện đại từ Google Fonts.
*   **Layout**: Sử dụng **CSS Flexbox** và **Grid** để tự động co giãn tương thích (Responsive) trên cả màn hình Laptop và Mobile.
*   **Bảng mã**: Mọi dữ liệu text tiếng Việt được encode `UTF-8` chuẩn xác.

---

## 4. Proposed Changes

### 4.1. [MODIFY] [generate_three_recent_courses_report.py](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/scratch/generate_three_recent_courses_report.py)
*   Cập nhật logic ghi đè file Markdown nguồn sang [data/three_recent_courses_report.md](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/data/three_recent_courses_report.md).
*   Không in các cột trung gian trong Markdown để Markdown cũng sạch sẽ hơn.

### 4.2. [MODIFY] [export_online_reports.py](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/scratch/export_online_reports.py) (Hoặc script convert HTML tương ứng)
*   Sửa đổi hàm `md_to_html_fallback` để parse cấu trúc Markdown mới và render ra CSS Progress Bars, KPI Cards.
*   Sử dụng template CSS Linear cao cấp không chứa thẻ script Tailwind CSS.
