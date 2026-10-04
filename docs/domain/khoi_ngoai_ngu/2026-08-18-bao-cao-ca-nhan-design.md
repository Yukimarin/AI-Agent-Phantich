# Thiết kế: Báo cáo Hồ sơ Cá nhân trong Dashboard Khối Ngoại Ngữ

**Ngày khởi tạo**: 2026-08-18  
**Dự án**: `AI_Report_NN`  
**Mục tiêu**: Bổ sung tab "Hồ sơ Cá nhân" trực quan vào Dashboard Khối Ngoại Ngữ, cho phép Leader đánh giá hiệu suất, tuân thủ và khối lượng công việc của từng nhân sự theo từng tháng (đặc biệt là Tháng 8) và xuất file PDF/in ấn độc lập.

---

## 1. Thiết kế Giao diện (UI Design)

Tab mới `#tab-profile` sẽ chứa các thành phần sau:

### A. Bộ lọc cá nhân (Filter Bar)
*   Dropdown chọn nhân sự: `<select id="profile-person-select">`. Tự động đồng bộ với Bộ môn hiển thị (JPN, ENG, hoặc ALL).
*   Dropdown chọn tháng: `<select id="profile-month-select">` với các lựa chọn:
    *   `all`: Toàn bộ giai đoạn
    *   `07`: Tháng 7/2026 (01/07 - 31/07)
    *   `08`: Tháng 8/2026 (01/08 - 21/08)

### B. Hệ thống Thống kê nhanh (KPI Dashboard Cards)
*   **Thẻ Tuân thủ (Compliance Rate)**: Tỷ lệ nộp báo cáo ngày (%) và số ngày quên nộp (chỉ tính đến ngày hiện tại).
*   **Thẻ Giờ làm TB**: Số giờ làm việc trung bình mỗi ngày trong khoảng thời gian đã chọn.
*   **Thẻ Tỷ lệ đạt chỉ tiêu**: Hiệu suất làm việc so với định mức quy định (FT 8h, TTS 4h).
*   **Thẻ Trạng thái Vận hành**: Nhãn màu động (`🟢 Đủ chỉ tiêu`, `🔴 Quá tải`, `🟡 Chưa đủ`).

### C. Bố cục Đánh giá Chi tiết (2 Cột)
*   **Cột bên trái**:
    *   Thông tin chung: Họ tên, Chức vụ, Bộ môn, Loại hình, Định mức tiêu chuẩn ngày.
    *   Chi tiết vi phạm kỷ luật: Danh sách ngày thiếu báo cáo (chỉ tính đến ngày hiện tại).
    *   Giải trình chi tiết của hệ thống về Trạng thái Vận hành để Leader hiểu rõ nguyên nhân.
*   **Cột bên phải**:
    *   Thống kê giờ làm: Tổng giờ KPI Master vs Tổng giờ phát sinh (Ad-hoc) bằng thanh tiến độ màu.
    *   Top công việc phát sinh tiêu tốn nhiều thời gian nhất của nhân sự đó.

### D. Bảng Chi tiết Công việc Dự án Cá nhân
*   **Thống kê tóm tắt dự án cá nhân (Project Task Summary)**: Đặt ngay phía trên bảng công việc cá nhân, bao gồm: Tổng số Task, Hoàn thành, Đang làm, Trễ hạn, Tỷ lệ hoàn thành để Leader có cái nhìn tổng quan nhanh chóng.
*   **Bảng công việc**: Hiển thị các task được giao cho nhân sự này (đã lọc theo tháng), hiển thị thông tin: Mã công việc, Tên công việc, Trạng thái (Đang làm, Hoàn thành, Quá hạn), và Hạn chót.

---

## 2. Logic xử lý & Tính toán Dữ liệu (Data Processing)

Dữ liệu ngày tháng sẽ được lọc động dựa trên Month được chọn (`all`, `07`, `08`) và ngày hiện tại (`today`):
*   **Lọc theo ngày hiện tại**: Mọi chỉ số tuân thủ, số ngày nộp báo cáo và danh sách ngày thiếu báo cáo (cả ở Python backend và JS client-side) sẽ chỉ tính toán các ngày $\le$ ngày hiện tại. Loại bỏ các ngày trong tương lai (ví dụ: ngày 19, 20, 21 của tháng 8) khỏi mẫu số và danh sách thiếu báo cáo để tránh cảnh báo sai lệch.
*   Khi lọc theo Tháng `08/2026`:
    *   Tập hợp ngày làm việc sẽ bao gồm các ngày từ `2026-08-01` đến ngày hiện tại.
*   Công thức tính Trạng thái Vận hành Cá nhân tương ứng theo tháng được lọc:
    *   Tỷ lệ nộp báo cáo = (Số ngày thực tế nộp báo cáo trong tháng đến hiện tại) / (Tổng số ngày làm việc trong tháng đến hiện tại).
    *   Giờ TB = (Tổng giờ làm trong tháng) / (Số ngày thực tế nộp báo cáo trong tháng).
    *   Đạt chỉ tiêu khi: Giờ TB $\ge$ định mức và Tỷ lệ nộp báo cáo $\ge 80\%$.
    *   Quá tải khi: Giờ TB $> 125\%$ định mức hoặc có $\ge 5$ active tasks hoặc có $\ge 2$ tasks quá hạn.

---

## 3. Thiết kế In ấn & Xuất bản (Print Layout)

Sử dụng CSS `@media print` để Leader có thể dễ dàng in báo cáo cá nhân của nhân viên đó:
```css
@media print {
    body { background: white; padding: 0; }
    /* Ẩn các thành phần không cần thiết */
    .actions-bar, .main-tabs, .team-filter-bar, .week-selector, .filter-bar, #tab-daily, #tab-project, #tab-kpi, .profile-filter-section {
        display: none !important;
    }
    /* Chỉ hiển thị tab hồ sơ cá nhân */
    #tab-profile {
        display: block !important;
    }
    .profile-card {
        border: 1px solid #ccc !important;
        box-shadow: none !important;
        page-break-inside: avoid;
    }
}
```
Khi leader chuyển sang tab "Hồ sơ Cá nhân", chọn nhân sự, sau đó bấm nút "Xuất PDF / In", trình duyệt sẽ mở hộp thoại in với trang hồ sơ cá nhân được căn chỉnh chuẩn khổ A4, loại bỏ toàn bộ các nút bấm và thanh menu điều hướng.
