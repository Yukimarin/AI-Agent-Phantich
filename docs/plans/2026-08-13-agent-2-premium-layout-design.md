# Tài liệu Thiết kế: Tái cấu trúc Giao diện Báo cáo Dự báo Học tập (Agent 2)

## 1. Mục tiêu
Cải thiện giao diện Dashboard của Agent 2 để giảm thiểu sự rắc rối, nâng cao tính trực quan và làm nổi bật các phần Hạn chế & Giải pháp khuyến nghị khắc phục. Đồng thời, lược bỏ hoàn toàn các từ ngữ mang tính kỹ thuật AI (như AI, AI Model, AI Prediction) để báo cáo mang tính chuyên nghiệp và hành vụ giáo dục hơn.

## 2. Giải pháp kỹ thuật

### 2.1 Bố cục 3 Tab SPA (Slate Dark Theme)
Sử dụng client-side JavaScript điều phối hiển thị 3 tab chính không reload trang:
1.  **Tab 1: Tổng quan & Khuyến nghị (Executive Cockpit):**
    *   3 KPI Cards: Sai số dự báo lịch sử (MAE), Tổng học viên nguy cơ cao (Báo động đỏ), Tổng học viên nguy cơ trung bình (Cảnh báo vàng).
    *   Action Plan Showcase: Chia bảng 2 cột đối xứng "Hạn chế (Điểm nghẽn học vụ)" và "Giải pháp khắc phục (Đề xuất hệ thống)".
2.  **Tab 2: Phân tích Lớp học:**
    *   Bảng thống kê lớp học tinh giản.
    *   Cột cảnh báo GV/TG hiển thị icon tam giác cam kèm tooltip mô tả lỗi khi hover (không làm giãn hàng của bảng).
    *   Cột hành động chứa nút `🔍 Chi tiết` để kích hoạt Slide-over Drawer.
3.  **Tab 3: Danh sách Học viên cần can thiệp (Care List):**
    *   Bảng lớn tổng hợp toàn bộ sinh viên Đỏ và Vàng.
    *   Nút lọc nhanh: Tất cả | Đỏ | Vàng | Khối CNTT | Khối QTKD.
    *   Nút `📥 Xuất danh sách can thiệp (CSV)` tải xuống dữ liệu lọc trực tiếp bằng JavaScript.

### 2.2 Slide-over Drawer (Bảng trượt chi tiết lớp)
*   Sử dụng CSS transitions `right 0.3s cubic-bezier(0.4, 0, 0.2, 1)` để hiển thị mượt mà.
*   Hiển thị chi tiết lỗi giảng viên và danh sách các thẻ học viên nguy cơ của riêng lớp đó khi trượt từ cạnh phải màn hình.

### 2.3 Loại bỏ ngôn từ AI
*   Đổi `"Dự báo (Luật cũ)"` thành `"Tỷ lệ đỗ dự kiến (Quy chuẩn cũ)"`.
*   Đổi `"Dự báo (Quy chế mới)"` thành `"Tỷ lệ đỗ dự kiến (Quy chế mới)"`.
*   Đổi `"AI Action Plan"` thành `"Giải pháp khắc phục (Đề xuất hệ thống)"`.
*   Đổi `"AI Model Error (MAE)"` thành `"Sai số đánh giá lịch sử (MAE)"`.

## 3. Các thành phần sửa đổi
*   Sửa đổi tệp generate report: [`generate_report.py`](file:///C:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/agents/core/agent_2_academic_pred/generate_report.py).
*   Chạy pipeline và xác nhận giao diện.
