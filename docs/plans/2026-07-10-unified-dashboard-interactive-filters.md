# Cấu trúc Multi-Agent mới & Nâng cấp Dashboard Premium (Kịch bản B)

**Goal:** Tái cấu trúc mô hình đánh giá thành 1 Agent Lead (MasterEvaluator) và 4 Sub Agent chuyên biệt. Đồng thời nâng cấp Web Dashboard Premium hỗ trợ tìm kiếm lớp/GV học thời gian thực, lọc động và tải dữ liệu Care List & KPI GV/TG dạng CSV chuẩn tiếng Việt.

**Architecture:**
1. **Quy trình Multi-Agent**:
   - **Agent Lead (MasterEvaluator)**: Tổng hợp KPI theo tỷ trọng mới: Điểm Kỷ luật (40% - gộp Kỷ luật SV từ Sub Agent 1 & Kỷ luật tác nghiệp GV/TG từ Sub Agent 3), Điểm Học tập (30% - Sub Agent 2), Điểm Báo cáo ngày (30% - Sub Agent 4).
   - **Sub Agent 1 (ViolationAnalyst)**: Phân tích vi phạm của SV từ Excel.
   - **Sub Agent 2 (AcademicPredictor)**: Phân tích GPA và tỷ lệ trượt của lớp từ database.
   - **Sub Agent 3 (TaskAggregator)**: Phân tích lỗi kỷ luật tác nghiệp của GV/TG và tiến độ lớp.
   - **Sub Agent 4 (Báo cáo ngày)**: Phân tích chất lượng báo cáo ngày trong `daily_logs.txt`.
2. **Dashboard**: Nhúng dữ liệu JSON, sử dụng JS thuần để lọc động các hàng bảng `class-row` và accordion `care-list`. Tạo tệp CSV tải xuống qua Blob mã hóa UTF-8 BOM (`\uFEFF`).

**Tech Stack:** Python 3.14 (openpyxl, json, re), HTML5, CSS3, Tailwind CSS, FontAwesome, JavaScript, Chart.js.

---

## Proposed Changes

### System Rules & Documentation

#### [MODIFY] [AGENTS.md](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/.agents/AGENTS.md)
- Cập nhật mục **2. Vai trò của các Subagent** để định nghĩa lại cơ cấu:
  - **Agent Lead (MasterEvaluator)**
  - **Sub Agent 1 (ViolationAnalyst)**
  - **Sub Agent 2 (AcademicPredictor)**
  - **Sub Agent 3 (TaskAggregator - Phân tích Công việc & Kỷ luật)**: Phân tích lỗi kỷ luật tác nghiệp của GV/TG (quên điểm danh, phản hồi trễ, v.v.) và tiến độ lớp.
  - **Sub Agent 4 (Báo cáo ngày)**: Phân tích chi tiết chất lượng báo cáo ngày từ `daily_logs.txt`.
- Cập nhật mục **3. Quy chuẩn Báo cáo cuối cùng** để phản ánh công thức tính điểm KPI tổng hợp mới.

### KPI Engine & Report Generator

#### [MODIFY] [generate_kpi_report.py](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/scratch/generate_kpi_report.py)
- Cập nhật logic tính điểm để phản ánh đúng cấu trúc 4 Sub Agent:
  - Tách biệt điểm kỷ luật học viên (Sub Agent 1) và điểm kỷ luật tác nghiệp của GV/TG (Sub Agent 3).
  - Tách biệt điểm chất lượng báo cáo ngày (Sub Agent 4) khỏi điểm kỷ luật tác nghiệp.
  - Tính điểm KPI tổng: `KPI = (Điểm Kỷ luật SV + Điểm Kỷ luật tác nghiệp GV/TG) / 2 * 0.40 + Điểm Học tập * 0.30 + Điểm Báo cáo ngày * 0.30`.
- Cập nhật tiêu đề và nội dung bảng tổng hợp trong file báo cáo Markdown [report_kpi_gv_tg.md](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/data/report_kpi_gv_tg.md).

### Web Dashboard Generator

#### [MODIFY] [generate_unified_dashboard.py](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/scratch/generate_unified_dashboard.py)
- **Nhúng dữ liệu**: Nhúng dữ liệu `care_list` và `dashboard_data` trực tiếp vào mã nguồn HTML dưới dạng biến Javascript.
- **Thêm giao diện bộ lọc**:
  - Giao diện tìm kiếm lớp, GV/TG.
  - Bộ lọc khóa học (Tất cả, KS24, KS25, QTKD) và mức độ nguy cơ Care List (Tất cả, Đỏ - Cao, Vàng - Vừa, An toàn).
- **Thêm nút xuất dữ liệu**:
  - Nút xuất Care List (CSV) có BOM UTF-8.
  - Nút xuất bảng đánh giá KPI GV/TG (CSV) có BOM UTF-8.
- **Script lọc động & xuất CSV**:
  - Viết các hàm JS `applyFilters()`, `exportCareListCSV()`, `exportKPICSV()`.
  - Cập nhật hàng bảng `<tr>` với các thuộc tính `class="class-row"` và `data-*` tương ứng.

---

## Verification Plan

### Automated Tests
- Chạy đường ống đồng bộ hóa toàn bộ báo cáo:
  `uv run scratch/run_pipeline.py`
  Yêu cầu: Pipeline kết thúc thành công, các tệp báo cáo Markdown và HTML được cập nhật đầy đủ.

### Manual Verification
1. Xem báo cáo [report_kpi_gv_tg.md](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/data/report_kpi_gv_tg.md), xác nhận điểm KPI tổng hợp của từng GV/TG được tính theo công thức mới.
2. Mở file [unified_dashboard.html](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/output/unified_dashboard.html) trên trình duyệt, thử nghiệm gõ tìm kiếm lớp, chọn lọc khóa học, và xuất dữ liệu ra file CSV để xác nhận tiếng Việt hiển thị chuẩn xác, không lỗi font.
