# Tài liệu Thiết kế: Dashboard Báo cáo Công việc Agent 4 (Tuần/Tháng & Dự án)

Tài liệu này đặc tả thiết kế và kiến trúc cho việc nâng cấp Dashboard Agent 4, tích hợp bộ lọc thời gian Tuần/Tháng, tích hợp cảnh báo quản lý dự án trực quan và điều chỉnh logic đối chiếu định mức thời gian (bỏ qua task lạ).

## 1. Dữ liệu thời gian
- **Xem theo Tuần**: Giai đoạn Tuần 28 gồm 5 ngày: `2026-07-06` đến `2026-07-10`.
- **Xem theo Tháng**: Giai đoạn Tháng 7 gồm 9 ngày làm việc từ đầu tháng đến nay: `01/07, 02/07, 03/07, 06/07, 07/07, 08/07, 09/07, 10/07, 13/07`.

## 2. Logic đối chiếu định mức (Bỏ qua task lạ)
- Hệ thống so khớp task thực tế trên Worklane với KPI Master.
- **Task lạ (không khớp)**: Bỏ qua hoàn toàn, không trừ điểm, không ghi nhận cảnh báo.
- **Task khớp**: Đối chiếu $H_{actual}$ với $H_{standard}$. Nếu $H_{actual} > H_{standard} \times 1.5$ $\rightarrow$ Trừ 5 điểm vào $S_{time}$ và ghi nhận lỗi *"Khai báo vượt định mức"*.
- Điểm hợp lý thời gian $S_{time} = \max(0, 100 - \text{Điểm trừ do vượt định mức})$.
- Công thức tính điểm Work Score:
  $$\text{Work Score} = (\text{Tỷ lệ nộp báo cáo} \times 40\%) + (\text{Tỷ lệ hoàn thành task} \times 40\%) + (\text{S}_{time} \times 20\%)$$

## 3. Cấu trúc Giao diện HTML Báo cáo (`output/4_daily_logs_report.html`)
- **Tab 1: Báo cáo ngày (Nhân sự)**:
  - Thêm nút bấm sub-tabs: **[Xem theo Tuần]** và **[Xem theo Tháng]**.
  - **Chế độ Tuần**: Hiển thị danh sách chưa nộp báo cáo tuần, bảng hiệu suất tuần, chi tiết nhật ký 5 ngày và bảng các task vượt định mức tuần.
  - **Chế độ Tháng**: Hiển thị danh sách chưa nộp báo cáo tháng, bảng hiệu suất lũy kế 9 ngày tháng 7 và bảng các task vượt định mức trong tháng.
- **Tab 2: Tiến độ Dự án & Issues**:
  - **Critical Alerts (Cảnh báo khẩn cấp)** ở đầu tab: Hiển thị các dự án bị cảnh báo "Off-track" và các task đã quá hạn chót (Overdue tasks) nhưng chưa hoàn thành, kèm tên PIC phụ trách.
  - **Biểu đồ Trạng thái Task (Chart.js Doughnut)**: Biểu đồ tròn biểu diễn tỷ lệ các trạng thái task (Done, Chờ duyệt, Chưa làm, Hủy) trên hệ thống.
  - **Bảng phân bổ công việc**: Task đến hạn trong tuần và thống kê phân bổ theo nhân sự (PIC).

## 4. Tích hợp Báo cáo KPI Lead
- Điểm Work Score của chế độ xem Tháng 7 sẽ được sử dụng làm điểm Báo cáo ngày chính thức để tính KPI tổng hợp học kỳ cho các thầy cô trong file `report_kpi_gv_tg.md`.
- Các nhận xét định tính trong `report_kpi_gv_tg.md` sẽ chỉ ghi nhận các vi phạm khai báo vượt định mức thực sự (không còn chứa cảnh báo task lạ).


---
Trở về: [[Bản đồ Tri thức MOC|Bản đồ Tri thức dự án]]
