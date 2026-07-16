# Kế hoạch & Tổng hợp trao đổi phiên làm việc tiếp theo

Tài liệu này tổng hợp các nội dung đã chốt trong phiên làm việc hiện tại và định hướng triển khai các đầu việc cho phiên làm việc tiếp theo.

---

## 📅 1. Tóm tắt kết quả đã hoàn thành trong phiên này

1.  **Chuyển đổi nguồn dữ liệu vi phạm thực tế**:
    *   Loại bỏ hoàn toàn thuật toán dịch chuyển tịnh tiến (Shift Calibration) của file Excel.
    *   Truy vấn trực tiếp số liệu vi phạm thực tế cá nhân của từng sinh viên từ các bảng chi tiết của CSDL MySQL `qldt_el` (`attendance_detail` cho chuyên cần, `exercise` cho bài tập nợ, `elearning_late` cho Elearning lỗi, `rpoints` cho Rpoint).
2.  **Tích hợp Accordion ẩn/hiện thông minh vào Dashboard**:
    *   Sinh viên có nguy cơ trượt môn được phân loại lý do chi tiết (Vắng học, nợ bài tập, lỗi Elearning, Rpoint thấp, học lực yếu).
    *   Tích hợp danh sách dưới dạng các dòng Accordion ẩn/hiện ngay trong bảng **Mục 2** của báo cáo Dashboard, giúp slide báo cáo tổng quan giữ được sự gọn gàng, tinh tế.
3.  **Đóng gói và chia sẻ trực tuyến**:
    *   Xuất bản báo cáo HTML độc lập và tích hợp.
    *   Đóng gói toàn bộ báo cáo và upload thành công lên Gofile.io: [Tải file zip báo cáo tại đây](https://gofile.io/d/qUecnV).

---

## 🔍 2. Thông tin đối chiếu thực tế sắp tới (Người dùng thực hiện)

*   **Hành động**: Người dùng sẽ đi các lớp để lấy số liệu thực tế do Giảng viên/Trợ giảng (GV/TG) đánh giá trực tiếp.
*   **Lưu ý nghiệp vụ**: Dữ liệu từ GV/TG trên lớp có thể mang tính cảm tính nhiều hơn (ví dụ: đánh giá thái độ học tập trực quan, sự tích cực phát biểu, sự nỗ lực làm bài dù nộp muộn), khác biệt với số liệu hành vi ghi nhận cứng trên hệ thống MySQL (điểm danh, log nộp bài tập).

---

## 🚀 3. Kế hoạch triển khai cho phiên làm việc kế tiếp

Khi người dùng quay lại với số liệu đối chiếu thực tế, Agent sẽ thực hiện các đầu việc sau:

### Đầu việc 1: Phân tích chênh lệch (Gap Analysis)
*   So sánh danh sách cảnh báo từ Database MySQL với danh sách đánh giá thực tế của GV/TG.
*   Chỉ ra các trường hợp "Lọt lưới" (MySQL báo an toàn nhưng GV đánh giá nguy cơ) và "Cảnh báo nhầm" (MySQL báo nguy cơ nhưng GV đánh giá an toàn).
*   Phân tích nguyên nhân: Do hệ thống cập nhật chậm, do GV nhập thiếu điểm, hay do yếu tố cảm tính của GV.

### Đầu việc 2: Tinh chỉnh trọng số mô hình dự báo
*   Hiệu chỉnh công thức tính điểm năng lực dự báo `p_eligible`.
*   Điều chỉnh các ngưỡng cảnh báo vi phạm kỷ luật (ví dụ: nâng/hạ ngưỡng chuyên cần vắng 20%, nợ bài tập 20%, hoặc điểm Rpoint 80.0) sao cho tiệm cận nhất với đánh giá thực tế của GV/TG nhưng vẫn đảm bảo tính khách quan.

### Đầu việc 3: Bổ sung tính năng "Ghi chú ngoại lệ từ lớp học"
*   Tích hợp thêm cột hoặc công cụ nhập liệu để ghi nhận ý kiến phản hồi/đánh giá cảm tính của GV/TG vào Dashboard, giúp báo cáo tổng hợp có cả góc nhìn định lượng (Database) và định tính (Con người).
