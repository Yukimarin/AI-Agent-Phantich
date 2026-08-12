# Thiết kế Tái cấu trúc Báo cáo QLĐT sang Dashboard 3 Tab (Ngày/Tuần/Tháng)

Báo cáo QLĐT (`qldt_monthly_report.html`) ban đầu bị lọc cứng ở tháng 7/2026. Để hỗ trợ Leader QLCL theo dõi linh hoạt và trực quan, tài liệu này mô tả thiết kế nâng cấp báo cáo thành giao diện SPA 3 Tab tương tác động hoàn toàn theo Ngày, Tuần và Tháng.

---

## 1. Kiến trúc Dữ liệu & Đóng gói Backend (Python)

Tệp `generate_qldt_report.py` sẽ được nâng cấp để tổng hợp dữ liệu thành 3 cấu trúc JSON lớn từ nguồn `daily_log_analysis.json` và nhúng trực tiếp vào file HTML đầu ra.

### qldtDailyData (Báo cáo Ngày)
Chứa thông tin chi tiết nhật ký công việc của 4 nhân sự QLĐT theo từng ngày riêng lẻ:
```json
{
  "YYYY-MM-DD": {
    "summary": { "total_hours": 32.0, "total_tasks": 15, "completed_tasks": 12 },
    "staffs": {
      "Staff Name": {
        "role": "Giáo vụ",
        "total_hours": 8.0,
        "tasks": [
          { "title": "Task title", "hours": 4.0, "status_text": "Đã hoàn thành", "project": "Khảo thí" }
        ],
        "difficulties": "Nội dung khó khăn..."
      }
    }
  }
}
```

### qldtWeeklyData (Báo cáo Tuần)
Chứa năng suất tuần, tổng hợp khó khăn và xu hướng giờ làm việc:
```json
{
  "Tuần XX (DD/MM - DD/MM)": {
    "summary": { "avg_daily_hours": 8.0, "completion_rate": 90.0, "total_hours": 160.0 },
    "dept_trend_hours": [7.8, 8.2, 8.0, 7.9, 8.1],
    "staffs": {
      "Staff Name": {
        "total_hours": 40.0,
        "completed_tasks": 10,
        "total_tasks": 11,
        "uncompleted_tasks": ["Task title (Tiến độ: 50%)"]
      }
    }
  }
}
```

### qldtMonthlyData (Báo cáo Tháng)
Chứa bảng đề xuất HSNX, xếp loại hiệu suất, đánh giá định tính và tỷ lệ phân bổ giờ làm việc theo chuyên môn của bộ phận trong tháng:
```json
{
  "Tháng MM/YYYY": {
    "summary": { "total_tasks": 320, "completed_tasks": 280, "total_hours": 640.0, "avg_work_score": 95.0 },
    "dept_domain_hours": {
      "Khảo thí": 120.0,
      "Thời khóa biểu": 80.0,
      "Hành chính & Hỗ trợ SV": 200.0,
      "Xây dựng quy định & tài nguyên": 140.0,
      "Họp & Công việc chung": 100.0
    },
    "staffs": {
      "Staff Name": {
        "role": "Giáo vụ",
        "rank": "3",
        "reported_days": 21,
        "report_rate": 100.0,
        "total_tasks": 80,
        "completed_tasks": 80,
        "completion_rate": 100.0,
        "total_hours": 160.0,
        "work_score": 98.0,
        "proposed_ns": 1.15,
        "classification": "Xuất sắc",
        "evaluation": "Nhận xét chi tiết định tính...",
        "difficulties": [],
        "uncompleted_tasks": []
      }
    }
  }
}
```

---

## 2. Bố cục Giao diện UI (Tabbed Layout UX)

Giao diện SPA sử dụng hệ thống Tab tương tác mượt mà không reload trang.

### 2.1. Cấu trúc Tab Điều hướng
*   `📅 Báo cáo Ngày` (tab-daily)
*   `📊 Báo cáo Tuần` (tab-weekly)
*   `🏆 Báo cáo Tháng` (tab-monthly)

### 2.2. Chi tiết cấu trúc từng Tab
1.  **Tab Ngày**:
    *   Dropdown chọn ngày làm việc (chứa danh sách các ngày có log).
    *   Metrics Cards của ngày được chọn.
    *   Danh sách Staff Chips (hiển thị Avatar + Tên + Số giờ làm trong ngày). Click chọn staff sẽ render chi tiết công việc của người đó ở bảng bên cạnh.
    *   Bảng công việc chi tiết và Khối hiển thị khó khăn/vấn đề gặp phải của staff được chọn trong ngày.
2.  **Tab Tuần**:
    *   Dropdown chọn tuần.
    *   Trend Chart (Chart.js - Cột): Số giờ trung bình hàng ngày của bộ phận trong tuần.
    *   Bảng năng suất tuần của 4 giáo vụ.
    *   Danh sách tổng hợp khó khăn nổi bật của tuần.
3.  **Tab Tháng**:
    *   Dropdown chọn tháng.
    *   Bảng tổng hợp xếp hạng KPI & Đề xuất HSNX (NS).
    *   Doughnut Chart (Chart.js): Tỷ lệ % phân bổ thời gian theo 5 nhóm nghiệp vụ chuyên môn.
    *   Khối chi tiết đánh giá định tính (Điểm mạnh, Điểm yếu, Đề xuất cải thiện) của từng cá nhân.

---

## 3. Luồng điều khiển Client-Side (JS Dynamic Updates)

### 3.1. Quản lý trạng thái bộ lọc
```javascript
let activeTab = "tab-monthly";
let selectedDate = "";
let selectedWeek = "";
let selectedMonth = "";
let selectedStaff = "Trần Thị Mỹ Phước";
```

### 3.2. Cập nhật và vẽ lại biểu đồ động
*   Mỗi khi thay đổi bộ lọc thời gian hoặc click chuyển Tab, JavaScript sẽ cập nhật trạng thái tương ứng, thay đổi dữ liệu trong DOM và gọi hàm vẽ biểu đồ Chart.js.
*   **Quy tắc an toàn**: Luôn kiểm tra và gọi `.destroy()` biểu đồ cũ trước khi khởi tạo biểu đồ mới để tránh rò rỉ bộ nhớ hoặc lỗi chồng đè dữ liệu.
