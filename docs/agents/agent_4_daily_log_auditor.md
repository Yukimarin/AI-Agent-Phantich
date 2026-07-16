# Sub Agent 4: Báo cáo ngày (Daily Log Auditor) - Tài liệu tổng hợp hoạt động

Báo cáo này tổng hợp vai trò, cấu trúc dữ liệu, thuật toán tính điểm và các thay đổi phát triển đối với **Sub Agent 4 (Daily Log Auditor)** trong dự án đánh giá hiệu suất đào tạo.

---

## 1. Vai trò & Mục tiêu
Daily Log Auditor đóng vai trò là kiểm toán viên nhật ký công việc phòng Đào tạo. Nhiệm vụ chính là:
- Fetch và phân tách dữ liệu báo cáo ngày của 39 nhân sự phòng Đào tạo trực tiếp từ Worklane PM thông qua MCP server.
- Đối chiếu công việc khai báo với bảng định mức thời gian KPI Master của khối QTKD và khối CNTT.
- Chấm điểm hiệu suất báo cáo ngày (Work Score) cho từng nhân sự phục vụ tính điểm KPI tổng hợp (trọng số 30%).
- Xuất bản Dashboard HTML Agent 4 tích hợp phân tích theo tuần/tháng, Critical Alerts (Dự án Off-track, Task Overdue), và biểu đồ trạng thái.

---

## 2. Dữ liệu Đầu vào & Đầu ra

### Dữ liệu Đầu vào (Inputs)
- **Dữ liệu Worklane**: Gọi MCP tool `list_daily_reports` với tham số `department="DT"` và ngày làm việc của chu kỳ.
- **Token xác thực Worklane**: `wl_jtpd1dOgxnUm5n2d7V6dxBT_AZHNrnCK`.
- **Thông tin nhân sự & định mức KPI Master**:
  - Khối QTKD: [\_Task Management\_ QL Khối QTKD.xlsx](file:///C:/Users/DELL/Downloads/_Task%20Management_%20QL%20Kh%E1%BB%91i%20QTKD.xlsx) (sheet `STAFF` và `KPI_MASTER`).
  - Khối CNTT: [Quản lý hiệu suất đào tạo.xlsx](file:///C:/Users/DELL/Downloads/Qu%E1%BA%A3n%20l%C3%BD%20hi%E1%BB%87u%20su%E1%BA%A5t%20%C4%91%C3%A0o%20t%E1%BA%A1o.xlsx) (sheet `BC hàng ngày` và `Cấu trúc KPI công việc GV. TG`).
- **Dữ liệu dự án**: Đọc từ `scratch/project_issues.json` (chứa thông tin tiến độ dự án phòng Đào tạo).

### Dữ liệu Đầu ra (Outputs)
- **Tệp JSON phân tích**: [daily_log_analysis.json](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/data/daily_log_analysis.json) chứa phân tách `weekly_stats` và `monthly_stats`.
- **HTML Dashboard**: [4_daily_logs_report.html](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/output/4_daily_logs_report.html).

---

## 3. Quy tắc & Thuật toán tính Work Score
Điểm Work Score phản ánh tính tuân thủ và năng suất báo cáo, được tính theo công thức:

$$\text{Work Score} = \text{Report Rate} \times 40.0 + \text{Completion Rate} \times 40.0 + \text{Time Score} \times 0.20$$

Trong đó:
- **Report Rate (Tỷ lệ báo cáo - 40%)**:
  $$\text{Report Rate} = \frac{\text{Số ngày nộp báo cáo thực tế}}{\text{Tổng số ngày làm việc trong chu kỳ}}$$
- **Completion Rate (Tỷ lệ hoàn thành task - 40%)**:
  $$\text{Completion Rate} = \frac{\text{Số task có trạng thái hoàn thành (hoặc 100%)}}{\text{Tổng số task khai báo}}$$
- **Time Score (Điểm thời gian - 20%)**:
  - Điểm thời gian xuất phát từ 100 điểm.
  - **Quy tắc đối chiếu định mức**:
    - Đối với các task lạ/tự do (không khớp từ khóa KPI Master): Bỏ qua không phạt trừ điểm (gán mặc định định mức 30 phút).
    - Đối với các task khớp KPI Master: Nếu giờ khai báo thực tế vượt quá 1.5 lần giờ định mức tiêu chuẩn ($Hours_{declared} > Hours_{std} \times 1.5$), trừ 5.0 điểm/lần.
    - Điểm thời gian tối thiểu là 0.0 điểm.
- *Trường hợp đặc biệt:* Nếu nhân sự không nộp báo cáo ngày nào trong cả chu kỳ ($\text{Report Rate} = 0.0$), gán cứng $\text{Work Score} = 0.0$.

---

## 4. Lịch sử Thay đổi & Quyết định quan trọng
- **[2026-07-13] Tích hợp MCP Worklane & Rebuild Thống kê**: Tải trực tiếp dữ liệu báo cáo ngày qua API thay thế cho việc đọc thủ công từ log txt, đồng thời tích hợp token bảo mật mới.
- **[2026-07-13] Cải tiến quy chế phạt định mức**: Bỏ qua hoàn toàn các task tự do khỏi diện phạt trừ điểm. Chỉ phạt 5 điểm đối với các task khớp định mức nhưng khai báo lạm phát thời gian vượt quá 1.5 lần.
- **[2026-07-13] Chuyển đổi chu kỳ đánh giá**: Chuyển chu kỳ đánh giá bắt đầu từ ngày 13/07/2026 (Tuần III tháng 7). Dynamic hóa toàn bộ công thức day-counts (thay vì cố định 5 hay 9 ngày) và chuyển dịch bộ lọc ngày quá hạn/ngày đến hạn dự án sang tuần mới (13/07 - 17/07/2026).

---

## 5. Mã nguồn liên quan
- **Script phân tích & fetch Worklane**: [analyze_daily_logs_mcp.py](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/scratch/analyze_daily_logs_mcp.py)
- **Script sinh dashboard HTML**: [generate_agent4_report.py](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/scratch/generate_agent4_report.py)
