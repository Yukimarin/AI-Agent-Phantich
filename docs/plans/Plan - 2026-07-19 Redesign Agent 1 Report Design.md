# Tài liệu Thiết kế: Tái cấu trúc Báo cáo Tuần & Giao diện Agent 1 (Violation Analyst)

Tài liệu này định nghĩa thiết kế chi tiết cho việc nâng cấp giao diện, sửa lỗi dữ liệu và tích hợp biểu đồ trực quan cho Báo cáo Tuần của Agent 1 (Violation Analyst).

---

## 1. Mục tiêu & Yêu cầu thay đổi

1.  **Sửa lỗi dữ liệu tuần trước bằng 0**:
    *   **Nguyên nhân**: Trong cấu hình nhóm tuần của `generate_weekly_report.py`, `sheet_prev` bị trỏ sang sheet môn học cũ (`KS25_Python` / `KS25_QTKD_DTB202`) vốn không có ngày học trong tuần đối chiếu (06/07 - 12/07).
    *   **Giải pháp**: Trỏ `sheet_prev` về chính sheet môn học hiện tại (`KS25_Python_Web` / `KS25_QTKD_PRJ302`) vì các sheet này thực tế đã học từ tuần trước và chứa đầy đủ dữ liệu ngày học đối chiếu.
2.  **Đổi mới bảng vi phạm tuần (Phương án A)**:
    *   Chỉ hiển thị các cột chỉ số của tuần này: `Chuyên cần`, `Bài tập`, `Elearning`.
    *   Hiển thị chỉ số dạng `Tuần này (Tăng/Giảm so với tuần trước)`.
    *   **Quy tắc tô màu vi phạm**:
        *   Nếu vi phạm tăng (Xấu): Tô màu đỏ `rgb(239, 68, 68)` / `#ef4444`. Ví dụ: `15.00% (+2.50%)`.
        *   Nếu vi phạm giảm (Tốt): Tô màu xanh `rgb(16, 185, 129)` / `#10b981`. Ví dụ: `10.00% (-1.50%)`.
        *   Nếu không đổi hoặc không có dữ liệu tuần trước: Tô màu xám `rgb(100, 116, 139)`.
3.  **Lọc bỏ Giảng viên chỉ dạy 1 lớp**:
    *   Ẩn bảng `📋 Danh sách Giảng viên/Trợ giảng mới (Đang theo dõi / Chưa xếp hạng)` khỏi file báo cáo Markdown và HTML của Agent 1 để tối ưu không gian hiển thị.
    *   Vẫn giữ nguyên việc tính toán và lưu trữ các nhân sự này trong cấu trúc dữ liệu nội bộ để Agent 5 đọc và tính KPI bình thường.
4.  **Nâng cấp Giao diện & Trực quan hóa Biểu đồ**:
    *   **Obsidian Markdown**: Sử dụng biểu đồ **Mermaid** vẽ xu hướng vi phạm (Chuyên cần, Bài tập, Elearning) qua 3-4 môn học gần nhất của từng khối.
    *   **HTML Dashboard**:
        *   Nâng cấp Typography sang font `Inter` / `Outfit`.
        *   Các phần đánh giá chung và giải pháp được bọc trong các Card HSL màu dịu (tím/xanh) kèm icon chuyên nghiệp.
        *   Tích hợp **Chart.js** vẽ biểu đồ cột kép so sánh vi phạm Tuần này vs Tuần trước của 3 khối lớn.
        *   Tích hợp biểu đồ đường (Line Chart) thể hiện xu hướng vi phạm qua 4 môn gần đây nhất, hỗ trợ nút lọc chuyển đổi nhanh giữa các khối.
        *   Đảm bảo encoding UTF-8 không lỗi font tiếng Việt trên môi trường Windows.

---

## 2. Kiến trúc & Thiết kế Chi tiết

### 2.1 Cấu trúc dữ liệu và logic tính toán (`generate_weekly_report.py`)

*   **Sửa cấu hình tuần**:
    ```python
    weekly_groups = {
        'KS25_CNTT_HN': {
            'classes': ['HN-K25-CNTT1', 'HN-K25-CNTT2', 'HN-K25-CNTT3', 'HN-K25-CNTT4', 'HN-K25-CNTT5', 'HN-K25-CNTT6'],
            'sheet_curr': 'KS25_Python_Web',
            'sheet_prev': 'KS25_Python_Web',  # Sửa từ KS25_Python
            'label': 'Khóa KS25 CNTT Hà Nội (Python Web)'
        },
        'KS25_CNTT_HCM': {
            'classes': ['HCM-K25-CNTT5', 'HCM-K25-CNTT6', 'HCM-K25-CNTT7', 'HCM-K25-CNTT8'],
            'sheet_curr': 'KS25_Python_Web',
            'sheet_prev': 'KS25_Python_Web',  # Sửa từ KS25_Python
            'label': 'Khóa KS25 CNTT TP. HCM (Python Web)'
        },
        'KS25_QTKD_HN': {
            'classes': ['HN-K25-QTKD1', 'HN-K25-QTKD2', 'HN-K25-QTKD3'],
            'sheet_curr': 'KS25_QTKD_PRJ302',
            'sheet_prev': 'KS25_QTKD_PRJ302',  # Sửa từ KS25_QTKD_DTB202
            'label': 'Khóa KS25 QTKD Hà Nội (PRJ302)'
        }
    }
    ```

*   **Logic tính toán Delta**:
    Với mỗi lớp và chỉ số (CC, BT, EL):
    $$\Delta = \text{Chỉ số tuần này} - \text{Chỉ số tuần trước}$$
    Trong Markdown:
    *   Nếu \(\Delta > 0\): `Tuần này% <span style="color:#ef4444">(▲ +Delta%)</span>`
    *   Nếu \(\Delta < 0\): `Tuần này% <span style="color:#10b981">(▼ -Delta%)</span>`
    *   Nếu \(\Delta == 0\): `Tuần này% <span style="color:#64748b">(--)</span>`

*   **Ẩn danh sách watchlist**:
    Trong script `generate_weekly_report.py`, ta vẫn thu thập `watchlist_staff` nhưng khi ghi ra `data/kpi_report.md`, ta sẽ loại bỏ khối văn bản ghi danh sách này ra.

### 2.2 Thiết kế Giao diện Markdown (Obsidian Vault)

Tệp `data/kpi_report.md` sẽ chứa biểu đồ Mermaid thể hiện xu hướng vi phạm qua các môn gần nhất:
```mermaid
line
    title Xu hướng vi phạm qua các môn - Khối KS25 CNTT HN
    x-axis Javascript --> Database --> Python --> Python Web
    y-axis Tỷ lệ vi phạm (%)
    "Chuyên cần" : [10.2, 8.5, 5.4, 7.2]
    "Bài tập" : [15.3, 12.1, 8.2, 9.5]
    "Elearning" : [20.1, 18.2, 12.4, 11.2]
```

### 2.3 Thiết kế Giao diện HTML Dashboard (`output/1_kpi_report.html`)

*   **Bố cục (Layout)**:
    1.  **Header**: Thông tin báo cáo, tuần báo cáo động, logo A1.
    2.  **Summary Cards**: Các thẻ thống kê chỉ số trung bình và cảnh báo nhanh của tuần.
    3.  **Interactive Charts**: Khu vực biểu đồ Chart.js:
        *   Bên trái: Grouped Bar Chart so sánh Chuyên cần, Bài tập, Elearning của tuần này vs tuần trước.
        *   Bên phải: Line Chart xu hướng vi phạm qua các môn lịch sử, có tabs chọn khối.
    4.  **Detailed Tables**: Các bảng vi phạm của 3 khối lớp, sử dụng định dạng so sánh tuần trực quan.
    5.  **General Assessment**: Khối đánh giá chất lượng có thiết kế dạng Callout Card bắt mắt.

---

## 3. Kế hoạch xác minh (Verification Plan)

### 3.1 Kiểm thử dữ liệu
*   Chạy script và kiểm tra xem chỉ số tuần trước có khác 0 và phản ánh đúng thực tế trong Excel hay không.
*   Kiểm tra tính chính xác của phép tính tăng/giảm vi phạm.

### 3.2 Kiểm thử trực quan (Visual QA)
*   Sử dụng `browser_subagent` để mở và kiểm tra giao diện của `output/1_kpi_report.html` và `unified_dashboard.html` để đảm bảo:
    *   Font chữ hiển thị chuẩn, không lỗi tiếng Việt.
    *   Màu sắc đỏ (tăng vi phạm) và xanh (giảm vi phạm) hiển thị đúng logic.
    *   Biểu đồ Chart.js và Mermaid render chính xác, không crash.
    *   Bảng watchlist giáo viên 1 lớp đã được ẩn thành công.
