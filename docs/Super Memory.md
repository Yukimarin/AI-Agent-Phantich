# Super Memory - PTIT Training & KPI Analytics

This file acts as the persistent memory for the AI agent working on the training and KPI evaluation project. Read this file at the start of every session, và update it with new insights, styling preferences, or logic updates at the end of each session.

## 1. User & Style Preferences
- **Language**: Tiếng Việt chuẩn, chuyên nghiệp, rõ ràng.
- **UI Aesthetics**: Báo cáo HTML phải đạt tiêu chuẩn premium:
  - Glassmorphism, độ tương phản tốt, thiết kế hiện đại, bảng biểu phân cấp rõ ràng.
  - Tích hợp Tailwind CSS và Chart.js trực quan.
- **Reporting Format**:
  - Báo cáo KPI tổng hợp GV/TG xuất ra định dạng Markdown tại `data/report_kpi_gv_tg.md`.
  - Các dashboard thống kê chi tiết xuất ra định dạng HTML động tại thư mục `output/` (nổi bật là `5_master_evaluation_dashboard.html`).
- **Hệ thống Agent**:
  - Sử dụng 1 Master Lead (MasterEvaluator) và 4 Sub Agent (ViolationAnalyst, AcademicPredictor, TaskAggregator, Daily Log Auditor).
  - Có các skill hỗ trợ: `data-cleaner-and-aligner`, `automated-visual-testing`, `premium-dashboard-charts`.

## 2. Core Project Logic & Constraints
- **Quy trình duyệt UI**: Bắt buộc chốt giao diện HTML đơn lẻ của từng Agent (ví dụ: `output/4_daily_logs_report.html`) và được User xác nhận trước khi tích hợp vào Dashboard tổng của Agent 5.
- **Subagent Delegation**:
  - *Agent 1 (Class KPI)*: Phân tích `data/vi_pham.xlsx`, chấm điểm kỷ luật theo quy định.
  - *Agent 2 (Academic)*: Phân tích MySQL `qldt_el` để tính GPA/tỷ lệ đỗ/trượt.
  - *Agent 3 (Ops)*: Phân tích vi phạm tác nghiệp 6 lỗi của GV/TG.
  - *Agent 4 (Logs)*: Phân tích `data/daily_logs.txt`.
  - *Agent 5 (Master)*: Tổng hợp theo trọng số (Kỷ luật 40%, Học tập 30%, Báo cáo 30%).
- **Luật CCDC & Lịch sử Học tập**:
  - *KS25*: Điểm kỷ luật môn trước từ bảng `auto_rpoints` (trường `total_score`).
  - *KS24*: Điểm kỷ luật môn trước từ bảng `final_results` (cột `rpoints`).
  - *Cấm thi*: Chỉ áp dụng cảnh báo cấm thi khi thời lượng môn học > 3 buổi. Đối với khóa cũ (KS24), đã bỏ cấm thi cứng, chỉ lưu cảnh báo.

## 3. Key Learnings & Kỹ thuật cốt lõi (Rút gọn)
- **Cơ sở dữ liệu & Pipeline**: MySQL 9.7 ngầm định chạy trên cổng **3307**. Chạy ngoài đường ống dùng `uv run` cần kèm `--with openpyxl pandas markdown numpy mysql-connector-python`. Hạn chế Numpy C-extensions nếu bị chặn.
- **Xử lý Dữ liệu Excel**: Đảo ngược tỷ lệ nợ bài tập thành tỷ lệ hoàn thành (`100 - excel_disc['bt']`). Chỉ số lớp học của TG phải đồng bộ từ dòng GV chính.
- **Lịch sử Triển khai Agent (Đã chốt)**:
  - *Agent 1 (Kỷ luật)*: Phân tích Excel, tính điểm, vẽ biểu đồ Chart.js tự động.
  - *Agent 2 (Học thuật)*: UI Dark-theme Vanilla CSS. Fallback tự động MySQL -> SQLite. Tối ưu MAE qua Grid Search: KS24 (1.10), KS25 (0.85), QTKD (0.80) giúp MAE < 12%. 
  - *Agent 4 (Logs)*: Phân tích báo cáo ngày.
- **Master Portal (SPA) & JS Errors**:
  - Tích hợp 5 tab không dùng iframe (file `5_master_evaluation_dashboard.html`).
  - **SyntaxError & Chart.js**: Rất chú ý khi build HTML/JS động bằng f-string. Lỗi thừa/thiếu cặp ngoặc nhọn `}}` ở cuối `<script>` khiến JS báo lỗi cú pháp im lặng trên trình duyệt, dẫn đến biểu đồ không thể khởi tạo/trống rỗng mà Python không quăng lỗi. Tránh bóc tách DOM phức tạp, nên trích xuất dữ liệu thẳng vào JSON template. 
  - Khắc phục lỗi Unicode trên Windows console bằng `sys.stdout.reconfigure(encoding='utf-8')`.

## 4. Danh Sách Nhân Sự & Phân Bổ Phòng Ban (44 Nhân sự chính thức)

### 4.1 Khối CNTT (24 Nhân sự)
*   **Trần Minh Cường** - Leader - rank 5
*   **Hồ Xuân Hùng** - Leader - rank 5
*   **Trịnh Quốc Hai** - Leader - rank 4
*   **Nguyễn Bá Minh Đạo** - Leader - rank 5
*   **Nguyễn Công Hưởng** - rank 3
*   **Phạm Tuấn Bình** - rank 4
*   **Mai Xuân Chinh** - rank 2
*   **Đinh Thành Nam** - rank 2
*   **Bùi Thanh Hải** - rank 5
*   **Nguyễn Quảng An** - rank 4
*   **Lương Quốc Tuấn** - rank 3
*   **Lâm Tùng Dương** - rank 3
*   **Ngọ Văn Quý** - rank 4
*   **Nguyễn Xuân Bách** - rank 4 (vừa là GV vừa thêm nhiệm vụ bên QLCL)
*   **Lại Trung Lâm** - rank 2
*   **Phạm Ngọc Kiên** - rank 2
*   **Đặng Minh Luân** - rank 3
*   **Lê Hà Thanh Sang** - rank 4
*   **Lưu Hoàng Xuân Nguyên** - rank 2
*   **Nguyễn Đức Minh** - rank 3
*   **Nguyễn Ngọc Sơn** - rank 3
*   **Phạm Viết Hùng** - rank 3
*   **Phan Ngọc Tài** - rank 3
*   **Trần Quốc Tuấn** - rank 3

### 4.2 Khối Ngoại ngữ và KNM (6 Nhân sự)
*   **Giáp Thị Minh Hằng** - Leader tiếng Nhật - rank 5
*   **Lò Thị Ngọc Anh** - Leader tiếng Anh - rank 5
*   **Ngô Quang Huấn** - Leader KNM - rank 5
*   **Bùi Thị Xuân Mai** - rank 3
*   **Hoàng Phương Thảo** - rank 3
*   **Lê Thị Đỏ** - rank 3

### 4.3 Khối QTKD (10 Nhân sự)
*   **Lê Thành Ngọc** - Leader - rank 5
*   **Hoàng Thị Kim Oanh** - Leader - rank 5
*   **Hoàng Thị Hậu** - rank 5
*   **Đặng Quỳnh Trang** - rank 3
*   **Lê Nhựt Mi** - rank 3
*   **Lê Thị Bảo Yến** - rank 3
*   **Nguyễn Ngọc Vân Khanh** - rank 4
*   **Nguyễn Thị Hồng Minh** - rank 3
*   **Nguyễn Thị Như Quỳnh** - rank 1 (Trợ giảng)
*   **Triệu Thị Thanh Tâm** - rank 1 (Trợ giảng)

### 4.4 Khối QLCLĐT (4 Nhân sự)
*   **Nguyễn Thị Tươi** - Leader - rank 5
*   **Nguyễn Huyền Trang** - rank 3
*   **Trần Thị Mỹ Phước** - rank 3
*   **Nguyễn Xuân Bách** - rank 4

*(Lưu ý: Nhân sự Nguyễn Thanh Bình Phước không thuộc khối Đào tạo, chỉ hỗ trợ, cần loại khỏi báo cáo KPI).*

## 5. Active Task
- (Hiện tại không có task nào đang làm dở)

