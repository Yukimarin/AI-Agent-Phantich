# Thiết Kế Chi Tiết: Khoang Lái Điều Hành Giám Đốc Đào Tạo (Agent 5 Executive Cockpit)

## 1. Mục Tiêu Thiết Kế
Xây dựng giao diện điều hành tối cao (Executive Cockpit) cho Giám đốc Đào tạo (Agent 5 Master Hub) đạt các tiêu chí:
1. **Zero-Text, High-Impact Visuals**: Tập trung vào biểu đồ, thẻ chỉ số nhịp đập, ma trận tương quan và các nhận định ngắn gọn (one-liner takeaways).
2. **Quy tắc 3 giây**: Nắm bắt ngay bức tranh toàn diện về chất lượng đào tạo, điểm nghẽn và tình hình nhân sự tại 2 cơ sở (Hà Nội, TP.HCM) và 2 khối (CNTT, QTKD).
3. **Bố cục 3 Tầng Chiến Lược**:
   - **Tầng 1**: 4 Thẻ Nhịp Đập Hệ Thống (Dự báo đỗ, Kỷ luật lớp, Tác nghiệp GV/TG, Tiến độ Worklane).
   - **Tầng 2**: 2 Biểu Đồ Ma Trận Chiến Lược (Ma trận Lớp học Bubble Chart & Ma trận Phân bổ Nhân sự 4 Góc Phần Tư Quadrant).
   - **Tầng 3**: Bảng Lệnh Hành Động Khẩn Cấp (Top 5 Điểm Nóng Cần Xử Lý Ngay Trong Ngày).
4. **Slide-over Drawer Drill-down**: Click vào bất kỳ lớp hoặc nhân sự nào để mở ngăn kéo trượt chi tiết mà không làm vỡ bố cục tổng thể.

## 2. Kiến Trúc Dữ Liệu Tổng Hợp
- **Agent 1 Data** (`agent1_output.json` & `classes_metrics_cache.json`): Chỉ số kỷ luật, tỷ lệ vắng, nợ bài tập, chậm EL của từng lớp và giảng viên phụ trách.
- **Agent 2 Data** (`agent2_output.json`): Tỷ lệ dự báo đỗ, sinh viên Care List, học viên bị cấm thi và Nghịch lý kỷ luật (⚡ Discipline Paradox).
- **Agent 3 Data** (`agent3_output.json`): Điểm tác nghiệp GV/TG, danh sách lỗi vi phạm theo khung chế tài T6/2026.
- **Agent 4 Data** (`daily_log_analysis.json` & `project_issues_worklane.json`): Tỷ lệ nộp log ngày, cảnh báo `UNVERIFIED`, task quá hạn theo Khối & Cơ sở.
- **Staff Metadata** (`staff_roles_ranks.md`): Phân loại nhân sự theo Khối (CNTT, QTKD), Cơ sở (HN, HCM) và Rank (R1-R5).

## 3. Kiến Trúc Giao Diện UI/UX
- File đầu ra: `output/dashboards/core/agent_5_master_portal.html`.
- Theme: Dark Mode Glassmorphism cao cấp (Slate 900 / Indigo / Emerald / Amber / Rose).
- Thư viện trực quan: Chart.js 4.x + FontAwesome 6.4 + Google Fonts (Plus Jakarta Sans).
- Bộ lọc C-Level đa chiều:
  - Lọc Cơ sở: [Tất cả Cơ sở | 🏢 Hà Nội | 🏢 TP. Hồ Chí Minh]
  - Lọc Khối chuyên môn: [Tất cả Khối | 💻 Khối CNTT | 📈 Khối QTKD]
- Tích hợp 4 tab chuyên sâu (Agent 1, 2, 3, 4) ở thanh điều hướng phụ để Giám đốc có thể xem sâu khi cần.

## 4. Kế Hoạch Triển Khai
1. **Module Tổng Hợp Dữ Liệu Cockpit**: Viết logic trích xuất và liên kết dữ liệu chéo giữa 4 Agent trong `agents/master/agent_5_master_portal/generate_unified_dashboard.py`.
2. **Dựng Giao Diện Cockpit 3 Tầng**:
   - Header & C-Level Filters.
   - Tầng 1: 4 Vital Stat Cards.
   - Tầng 2: Bubble Matrix (Lớp học) & Scatter Quadrant (Nhân sự).
   - Tầng 3: Action Priority Table.
   - Slide-over Drawer cho Class & Personnel Drill-down.
3. **Cập Nhật Báo Cáo Markdown**: Cập nhật `data/report_kpi_gv_tg.md` với bảng xếp hạng thi đua và Action Plan trực quan.
4. **Kiểm Thử & Xác Thực**: Kiểm tra kích thước file, tốc độ tải (< 0.5s), không lỗi JS console và khả năng tương tác mượt mà.
