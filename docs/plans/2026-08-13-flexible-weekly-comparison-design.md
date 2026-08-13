# Tài liệu Thiết kế: Hệ thống Đối chiếu Tuần học gần nhất & Tự động kết nối Môn học liền kề

## 1. Mục tiêu
Giải quyết lỗi logic so sánh tuần cố định (7 ngày trước đó) trong phân tích chỉ số đào tạo giáo dục khi gặp trường hợp đặc biệt:
* Sinh viên nghỉ học giữa kỳ hoặc nghỉ hè kéo dài, dẫn đến tuần trước theo lịch không có ngày học thực tế (chỉ số vi phạm bằng 0% giả tạo).
* Lớp học bắt đầu học môn mới, dẫn đến tuần trước của môn học mới không có dữ liệu lịch sử.

## 2. Giải pháp kỹ thuật

### 2.1 Bản đồ Dòng thời gian Học tập (Class Timeline Map)
Xây dựng cấu trúc dữ liệu lưu trữ toàn bộ lịch sử ngày học thực tế của từng lớp học trên tất cả các môn học từ dữ liệu Excel.
```python
# class_timelines[class_name][sheet_name] = [list_of_sorted_dates]
```

### 2.2 Động cơ So sánh Linh hoạt (Flexible Comparison Engine)
Khi đánh giá lớp học `cls` trong tuần báo cáo hiện tại `[monday_curr, sunday_curr]`:

1. **Trường hợp Cùng Môn Học (Đã học môn này trước tuần hiện tại):**
   * Lùi thời gian để tìm ngày học gần nhất $D_{\text{last}}$ trước `monday_curr` của lớp `cls` trong môn học đó.
   * Xác định tuần chứa ngày $D_{\text{last}}$: `[monday_prev, sunday_prev]`.
   * Lấy dữ liệu của tuần học thực tế này làm mốc so sánh.

2. **Trường hợp Môn Học Mới (Chưa từng học môn này trước tuần hiện tại):**
   * Tự động quét tìm môn học gần nhất trước đó của lớp `cls` dựa trên ngày dạy lớn nhất nhỏ hơn ngày dạy đầu tiên của môn mới.
   * Xác định ngày dạy cuối cùng của môn cũ đó, lấy tuần học cuối cùng của môn cũ làm mốc so sánh.

3. **Trường hợp Lớp học mới thành lập:**
   * Không có lịch sử học tập ở bất kỳ môn nào.
   * Ghi nhận chênh lệch là `--`, hiển thị trạng thái `Môn mới`.

## 3. Các thành phần sửa đổi
* Sửa đổi logic tính toán tuần trong [`generate_kpi_report.py`](file:///C:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/agents/core/agent_1_class_kpi/generate_kpi_report.py).
* Cập nhật đồng bộ các chỉ số so sánh trong biểu đồ và báo cáo của Agent 1 và Agent 5.
