# Changelog Archive - Lịch sử các phiên làm việc PMO

Tài liệu này lưu trữ chi tiết toàn bộ nhật ký các phiên làm việc từ tháng 08/2026 trở về trước nhằm giải phóng dung lượng ngữ cảnh cho Super Memory.

---
## 📋 Nhật ký Phiên Làm Việc — 27/08/2026 (08:05 → 08:35)
### Các việc đã hoàn thành
1. **Tái cấu trúc Master Portal SPA (`agent_5_master_portal.html`)**:
   - Xóa bỏ hoàn toàn **Tab 5: KPI Tổng Hợp (Agent 5)** và **Tab 6: Thống Kê & Đề Xuất KPI**.
   - Thiết lập thanh menu gọn gàng chỉ gồm 4 tab tương ứng với 4 Agent cốt lõi:
     - **Tab 1: Kỷ Luật SV (Agent 1)** (Mặc định hiển thị khi tải trang).
     - **Tab 2: Dự Báo & Care List (Agent 2)**.
     - **Tab 3: Tác Nghiệp GV/TG (Agent 3)**.
     - **Tab 4: Báo Cáo Ngày (Agent 4)**.
2. **Khắc phục triệt để lỗi mất dữ liệu & xung đột JS giữa các Agent**:
   - Khắc phục lỗi xung đột biến toàn cục `window.trendChart`: Trong Agent 1 có `<canvas id="trendChart">` (tự động tạo `window.trendChart = HTMLCanvasElement`). Agent 3 gọi `window.trendChart.destroy()` gây `TypeError: window.trendChart.destroy is not a function` và chặn đứng luồng render bảng/biểu đồ của Agent 3. Giải pháp: Đổi biến biểu đồ của Agent 3 sang `window.opsDisciplineTrendChart` và kiểm tra kiểu an toàn trước khi hủy.
   - Khắc phục xung đột tên hàm `switchTab` giữa Agent 2 và Agent 4 bằng cách chuyển thành `switchTab_a2` và `switchTab_a4`.
   - Bổ sung cơ chế auto-resize Chart.js (`window.dispatchEvent(new Event('resize'))`) khi chuyển tab, giúp các biểu đồ không bị co cụm hoặc méo kích thước khi hiển thị từ trạng thái `hidden`.
3. **Kiểm toán VisualQA thành công 100%**:
   - Sử dụng `browser_subagent` kiểm tra cả 4 Tab trên trình duyệt thực tế, chụp ảnh màn hình xác nhận toàn bộ biểu đồ đường, cột, gauge và bảng danh sách đều hiển thị dữ liệu đầy đủ, chính xác.

---
## 📋 Nhật ký Phiên Làm Việc — 26/08/2026 (20:30 → 20:55)
### Các việc đã hoàn thành
1. **Chuyển đổi Agent 1 (Chỉ số lớp) từ Báo cáo Tuần sang Báo cáo Ngày**:
   - Khôi phục hàm `get_class_latest_and_prev_metrics` trong `generate_kpi_report.py` về logic so sánh ngày học cuối cùng thực tế với ngày học liền trước.
   - Đối với KS25 CNTT (ngày lớn nhất trong Excel là 20/08), hệ thống tự động lùi linh hoạt so sánh ngày 20/08 với 19/08 để tránh lỗi rỗng dữ liệu.
   - Đồng bộ hóa logic chấm điểm kỷ luật học viên theo ngày học cuối cùng thực tế có dữ liệu.

---
## 📋 Nhật ký Phiên Làm Việc — 26/08/2026 (20:09 → 20:30)
### Các việc đã hoàn thành
1. **Sửa lỗi logic trùng lặp dữ liệu biểu đồ so sánh tuần của Agent 1 (Chỉ số lớp)**.
2. **Đồng bộ và cập nhật dữ liệu mới nhất từ Worklane PM**.

---
## 📋 Nhật ký Phiên Làm Việc — 26/08/2026 (16:43 → 16:48)
### Các việc đã hoàn thành
1. **Đồng bộ và cập nhật số liệu mới từ Excel nguồn `PTIT_Chiso.xlsx`**.

---
## 📋 Nhật ký Phiên Làm Việc — 25/08/2026 (10:20 → 10:47)
### Các việc đã hoàn thành
1. **Xây dựng công cụ phân tích cơ hội KPI (`analyze_kpi_opportunities.py`)**.

---
## 📋 Nhật ký Phiên Làm Việc — 20/08/2026 (14:15 → 14:55)
### Các việc đã hoàn thành
1. **Hiệu chỉnh Báo cáo Tổng hợp Nhân sự HCM**.
2. **Loại bỏ task 'Chờ duyệt' khỏi lỗi trễ hạn của nhân sự**.

---
## 📋 Nhật ký Phiên Làm Việc — 18/08/2026 (13:48 → 14:55)
### Các việc đã hoàn thành
1. **Tối ưu hóa import SQL dump khổng lồ (1.25 GB) qua MySQL binary stream**.
2. **Đồng bộ hóa SQLite Fallback tinh gọn (1.30 MB)**.
3. **Hiệu chuẩn tự động bộ tham số dự báo (Grid Search - Agent 2)**.
