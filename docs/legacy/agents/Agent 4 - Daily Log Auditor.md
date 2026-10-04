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
  - Khối QTKD: [kpi_master_qtkd.md](file:///C:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/data/inputs/kpi_master_qtkd.md).
  - Khối CNTT: [kpi_master_cntt.md](file:///C:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/data/inputs/kpi_master_cntt.md).
- **Dữ liệu dự án**: Đọc từ [project_issues_worklane.json](file:///C:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/data/processed/project_issues_worklane.json) (chứa thông tin tiến độ dự án phòng Đào tạo).

### Dữ liệu Đầu ra (Outputs)
- **Tệp JSON phân tích**: [daily_log_analysis.json](file:///C:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/data/processed/daily_log_analysis.json) chứa phân tách `weekly_stats` và `monthly_stats`.
- **HTML Dashboard**: [agent_4_daily_logs.html](file:///C:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/output/dashboards/core/agent_4_daily_logs.html).

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
- **[2026-07-23] Tối ưu hóa UI/UX & Sửa đổi Dữ liệu Nhân sự:** Sửa lỗi hiển thị mất chữ của dự án, nâng độ tương phản nhãn trục của biểu đồ JPS. Bổ sung các thẻ Metric Cards và highlight đỏ nhạt cho các hàng task quá hạn/hoàn thành thấp trong Panel I và Panel V. Đồng thời loại bỏ Nguyễn Thanh Bình Phước khỏi báo cáo, chuyển Nguyễn Đức Minh sang Khối CNTT (CNTT-HCM).
- **[2026-07-23] Tích hợp Báo cáo Hiệu suất & Phân bổ Nhân sự Jira (JPS):** Xây dựng chỉ số hiệu suất tổng hợp Jira (JPS = 60% TCR + 40% TFR) cô lập hoàn toàn với điểm báo cáo ngày. Tích hợp biểu đồ xếp hạng hiệu suất nhân sự và bảng phân bổ nguồn lực động theo Khối phòng ban vào Dashboard HTML của Agent 4.
- **[2026-07-23] Tích hợp Fetch Dự án thời gian thực & Chi tiết Task:** Phát triển script `sync_worklane_projects.py` tự động đồng bộ 34 dự án Đào tạo và toàn bộ issues trực tiếp từ Worklane PM API. Bổ sung Panel "Chi Tiết Công Việc Dự Án" tương tác động trên Dashboard cho phép xem chi tiết, tìm kiếm và lọc trạng thái các task của dự án được click.
- **[2026-07-23] Tích hợp Project Hub theo Khối phòng ban:** Triển khai tính năng Project Hub động cho phép theo dõi dự án (lọc card dự án, cập nhật biểu đồ Doughnut trạng thái task) và hiển thị danh sách nhân sự trống việc (tasks = 0) theo 4 Khối: CNTT, QTKD, QLCLĐT, Ngoại ngữ & KNM.
- **[2026-07-23] Cập nhật Báo cáo & Khắc phục lỗi encoding:** Chuyển đổi các đường dẫn tuyệt đối cứng trong script sinh báo cáo sang tương đối để chạy đúng trên worktree. Lấy dữ liệu mới nhất đến ngày 22/07 và xử lý thành công lỗi KeyError Nguyễn Thanh Bình Phước trên môi trường Windows.
- **[2026-07-13] Tích hợp MCP Worklane & Rebuild Thống kê**: Tải trực tiếp dữ liệu báo cáo ngày qua API thay thế cho việc đọc thủ công từ log txt, đồng thời tích hợp token bảo mật mới.
- **[2026-07-13] Cải tiến quy chế phạt định mức**: Bỏ qua hoàn toàn các task tự do khỏi diện phạt trừ điểm. Chỉ phạt 5 điểm đối với các task khớp định mức nhưng khai báo lạm phát thời gian vượt quá 1.5 lần.
- **[2026-07-13] Chuyển đổi chu kỳ đánh giá**: Chuyển chu kỳ đánh giá bắt đầu từ ngày 13/07/2026 (Tuần III tháng 7). Dynamic hóa toàn bộ công thức day-counts (thay vì cố định 5 hay 9 ngày) và chuyển dịch bộ lọc ngày quá hạn/ngày đến hạn dự án sang tuần mới (13/07 - 17/07/2026).

---

## 5. Mã nguồn liên quan
- **Script phân tích & fetch Worklane logs**: [analyze_daily_logs.py](file:///C:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/agents/core/agent_4_daily_logs/analyze_daily_logs.py)
- **Script đồng bộ dự án & issues**: [sync_worklane_projects.py](file:///C:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/agents/core/agent_4_daily_logs/sync_worklane_projects.py)
- **Script sinh dashboard HTML**: [generate_report_v4.py](file:///C:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/agents/core/agent_4_daily_logs/generate_report_v4.py)



---

*   Xem chi tiết: [[output/reports/core/agent_4_daily_logs|Báo cáo Nhật ký Công việc & Đồng bộ Worklane]]
*   Dashboard trực quan: [agent_4_daily_logs.html](file:///C:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/output/dashboards/core/agent_4_daily_logs.html)
---
Trở về: [[Bản đồ Tri thức MOC|Bản đồ Tri thức dự án]]
