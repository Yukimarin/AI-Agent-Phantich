# Super Memory - Quy chuẩn Sống còn & Kiến trúc Dự Án PMO

Tài liệu này lưu trữ các quyết định thiết kế và quy chuẩn kỹ thuật sống còn của hệ thống.
*(Lịch sử chi tiết các phiên làm việc cũ được lưu trữ tại `docs/changelog_archive.md`).*

---

## 2. Công Thức & Quy Chuẩn Dự Báo Học Thuật (Agent 2: AcademicPredictor)
- **Căn nguyên Bug Dự Báo Thấp ở KS24 (`HN-K24-CNTT2`, `HN-K24-CNTT4`, `HCM-K24-CNTT1`)**: 
  - Trong quá trình học dở (In-progress), học viên chưa nộp Đồ án tốt nghiệp cuối kỳ (điểm Project đang là null/0).
  - Thuật toán cũ áp dụng điều kiện `proj >= 50.0` để cấm thi giữa kỳ khi một vài học viên có điểm mẫu, dẫn đến 95% học viên ngoan, kỷ luật tốt trong lớp bị đánh cấm thi nhầm (`is_failed_new = True`).
- **Giải pháp dứt điểm**:
  - Gỡ bỏ chốt chặn Project ra khỏi điều kiện cấm thi giữa kỳ (Điểm Project là điểm thi cuối kỳ, không phải điều kiện cấm thi quá trình).
  - Tỷ lệ đỗ các lớp KS24 đã phục hồi đúng thực tế: `HN-K24-CNTT1` (**68.0%**), `HN-K24-CNTT2` (**58.0%**), `HN-K24-CNTT4` (**60.1%**), `HCM-K24-CNTT1` (**59.2%**).

## 3. Kiến Trúc Tab Con Trong Agent 5 (Scroll-Free Full-Bleed Viewport)
- **Căn nguyên lỗi Double Scroll**: Trước đây các iframe tab con đặt trong box card `h-[88vh]` lồng trong trang chính, dẫn đến thanh cuộn lồng nhau (2 thanh cuộn cùng lúc).
- **Giải pháp dứt điểm**:
  - Tạo khung viewport toàn màn hình `fixed inset-x-0 bottom-0 top-[76px] w-full h-[calc(100vh-76px)] z-30 bg-slate-950`.
  - Khi chuyển tab con: Đặt `document.body.style.overflow = 'hidden'` để khóa cuộn trang ngoài và để iframe con hiển thị 100% chiều cao không viền, mang lại trải nghiệm mượt mà 1-scroll tự nhiên.
  - Khi quay lại "Cockpit Điều Hành": Đặt lại `document.body.style.overflow = 'auto'`.

## 2. Đường Ống Tự Động Hóa 1-Click (`run_pipeline.py`)
- **Cơ chế thực thi**: Sử dụng `uv run --with <deps>` cho các worker agents yêu cầu thư viện đặc thù (`mysql-connector-python`, `openpyxl`, `numpy`) và `sys.executable` cho các bước Master biên dịch HTML/Markdown.
- **Quy trình chạy tuần tự 5 bước**:
  1. `DataSanitizer` (`agents/common/data_sanitizer.py`): Khởi tạo cache metrics `classes_metrics_cache.json`.
  2. `Agent 1: Kỷ luật học viên` (`agents/core/agent_1_class_kpi/run.py`): Xuất `agent1_output.json` & dashboard Agent 1.
  3. `Agent 2: Dự báo học thuật & Care List` (`agents/core/agent_2_academic_pred/run.py`): Xuất `agent2_output.json` & dashboard Agent 2.
  4. `Agent 4: Báo cáo ngày PMO & Worklane` (`agents/core/agent_4_daily_logs/run.py`): Xuất `daily_log_analysis.json` & dashboard Agent 4.
  5. `Agent 3: Kỷ luật tác nghiệp GV/TG` (`agents/core/agent_3_ops_discipline/run.py`): Đọc MySQL + Worklane, xuất `agent3_output.json` & dashboard Agent 3.
  6. `Agent 5: Master Portal & Báo cáo KPI` (`generate_unified_dashboard.py` + `generate_kpi_report.py`): Xuất `output/dashboards/core/agent_5_master_portal.html` & `data/report_kpi_gv_tg.md`.
- **Hiệu năng & Thời gian thực thi**: 100% các Agent chạy trơn tru, không có lỗi ngoại lệ, sinh đầy đủ dashboard và báo cáo Markdown.

---

## 3. Quy chuẩn JavaScript & CSS trong SPA (Chống xung đột)
- **Scoped Namespace JS:** Toàn bộ script của mỗi Agent con phải bọc trong IIFE độc lập.
  - Đặt tên hàm và biến có tiền tố rõ ràng (`a1_`, `a2_`, `a3_`, `a4_`).
  - Tuyệt đối không đặt tên biến toàn cục trùng với ID của thẻ HTML Canvas (ví dụ thẻ `<canvas id="trendChart">` tự động tạo `window.trendChart = HTMLCanvasElement`, làm crash nếu gọi `window.trendChart.destroy()`). Dùng biến riêng: `window.opsDisciplineTrendChart`.
- **Auto-resize Chart.js:** Khi chuyển tab trong SPA, luôn kích hoạt `window.dispatchEvent(new Event('resize'))` để Chart.js trong tab vừa hiện tự động vẽ lại đúng tỷ lệ.
- **CSS Nesting Isolation:** Bao bọc CSS của từng Agent bằng selector vùng chứa (ví dụ: `#tab-agent1-container { ... }`), thay thế `:root`, `html`, `body` thành `&`.

---

## 4. Danh mục Nhân sự & Phòng ban
- Nguồn chân lý thông tin nhân sự và Rank (R1-R5) nằm tại: `data/inputs/staff_roles_ranks.md`.
- Chuẩn hóa họ tên tiếng Việt không dấu bằng hàm `strip_accents` trước khi đối chiếu chéo.

---

## 5. Quy Chuẩn Xử Lý Sĩ Số Lớp Học & Cảnh Báo Biến Động
- **Quy tắc trích xuất Sĩ số (`extract_class_size`)**: Số nằm trong ngoặc đơn `()` phản ánh sĩ số lớp. Khi có chuỗi biến động (ví dụ `HN-K24-CNTT1(36-33)` hoặc `HN-K24-CNTT3(48-43-42)`):
  - Luôn lấy **con số cuối cùng** làm sĩ số hiện tại của lớp (`current_size = nums[-1]`).
  - Con số đầu tiên là sĩ số ban đầu (`initial_size = nums[0]`).
- **Cơ chế Cảnh báo Biến động Sĩ số (`size_alerts`)**: Tự động phát hiện và cảnh báo các lớp có `len(nums) > 1` để hiển thị trong `classes_metrics_cache.json`, `agent1_output.json` và khối `[!WARNING]` đầu báo cáo `data/report_kpi_gv_tg.md`.

---

## 6. Quy Chuẩn Bóc Tách 3 Chỉ Số Kỷ Luật Học Viên (Agent 1)
- **Căn nguyên Bug ẩn Elearning / Chuyên cần**: Khi chỉ hiển thị 1 con số vi phạm trung bình tổng hợp (ví dụ $11.54\%$), sẽ che khuất biến động của từng thành phần (ví dụ $EL = 23.08\%$, $CC = 11.54\%$, $BT = 0\%$).
- **Quy chuẩn hiển thị bắt buộc**: 
  - Trong mọi báo cáo và bảng phân tích của Agent 1, luôn hiển thị chi tiết đầy đủ 4 cột: **Chuyên cần (%)**, **Bài tập (%)**, **Elearning (%)**, và **Tổng hợp / Xu hướng**.
  - Báo động đỏ `🚨 Tăng` ngay khi bất kỳ chỉ số nào (đặc biệt là Elearning $\ge 20\%$ hoặc tăng $\ge +5\%$) có xu hướng xấu đi so với ngày trước.
  - Luôn khai báo biến toàn cục `class_sizes = {}` trong `agents/core/agent_1_class_kpi/generate_kpi_report.py` để tránh lỗi `NameError`.

---

## 7. Quy Chuẩn Kiểm Toán Dữ Liệu Báo Cáo Ngày & Dự Án Worklane (Tháng 8/2026)
- **Số ngày làm việc tiêu chuẩn Tháng 8/2026**: 20 ngày (từ 03/08 đến 28/08/2026, T2-T6; ngày 31/08/2026 nghỉ lễ Quốc khánh công ty).
- **Ngày nghỉ phép được phê duyệt**: Nguyễn Thị Như Quỳnh (10/08), Nguyễn Thị Tươi (13/08), Nguyễn Ngọc Vân Khanh (12/08), Trần Minh Cường (14/08).
- **Phân loại địa bàn & cơ sở chuẩn**:
  - Khối CNTT: Cơ sở HCM (9 NS), Cơ sở HN - Ngọc Trục (7 NS), Cơ sở HN - HPC (7 NS), Leader chung (1 NS).
  - Khối QTKD: Cơ sở HN - Ngọc Trục (10 NS).
  - Khối Ngoại ngữ & KNM: Cơ sở HN (4 NS - Tiếng Nhật và Tiếng Anh/KNM).
  - Khối QLCLĐT: Cơ sở HN (2 NS: Tươi, Trang), Cơ sở HCM (1 NS: Mỹ Phước).
- **Chốt kiểm toán deadline dự án**: Lấy mốc `dueDate <= 2026-08-31` và trạng thái chưa hoàn thành (`state` không phải DONE/COMPLETED/CANCELLED).

---

## 8. Quy Chuẩn Kiểm Toán Hiệu Suất Giờ Công Worklane & Kiến Trúc 6 Leader

### A. Báo Cáo Chuyên Đề & Dashboard:
- Báo cáo Markdown: `docs/reports/2026-09-04-kiem-toan-hieu-suat-va-khai-bao-worklane.md`.
- Dashboard tương tác: `output/dashboards/audit/worklane_staff_audit.html`.
- Engine phân tích: `agents/audit/audit_worklane_performance.py` và `agents/audit/generate_audit_dashboard.py`.

### B. Danh Mục Chuẩn 41 Nhân Sự Theo 6 Khối & 6 Leader (Chỉ đạo Giám đốc Đào tạo Thầy Nguyễn Duy Quang):
1. **Khối CNTT Hà Nội (12 nhân sự + Leader Hồ Xuân Hùng - Rank 5):**
   - *Cơ sở HN - Ngọc Trục (6 NS):* Lương Quốc Tuấn (GV R3), Nguyễn Quảng An (GV R4), Lâm Tùng Dương (GV R3), Ngọ Văn Quý (GV R4), Lại Trung Lâm (TG R2), Phạm Ngọc Kiên (TG R2).
   - *Cơ sở HN - HPC (6 NS):* Bùi Thanh Hải (GV R5), Trịnh Quốc Hai (GV R4), Nguyễn Công Hưởng (GV R3), Phạm Tuấn Bình (GV R3), Đinh Thành Nam (TG R2), Mai Xuân Chinh (TG R2).
2. **Khối Quản trị Kinh doanh (8 nhân sự + Leader Hoàng Thị Kim Oanh - Rank 5):**
   - *Cơ sở HN - Ngọc Trục (6 NS):* Hoàng Thị Hậu (GV R5), Đặng Quỳnh Trang (GV R3), Nguyễn Ngọc Vân Khanh (GV R3), Nguyễn Thị Hồng Minh (GV R3), Nguyễn Thị Như Quỳnh (TG R1), Triệu Thị Thanh Tâm (TG R1).
   - *Cơ sở TP. Hồ Chí Minh (2 NS):* Lê Nhựt Mi (GV R3), Lê Thị Bảo Yến (TG R2).
3. **Khối Ngoại ngữ & KNM (3 nhân sự + Leader Giáp Thị Minh Hằng - Rank 5 - Cơ sở HN - HPC):**
   - Lò Thị Ngọc Anh (GV R5), Lê Thị Đỏ (GV R3), Ngô Quang Huấn (GV R3).
4. **Khối QLCLĐT Hà Nội (3 nhân sự + Leader Nguyễn Thị Tươi - Rank 4):**
   - Nguyễn Huyền Trang (Giáo vụ R2 - HPC), Trần Thị Mỹ Phước (Giáo vụ R2 - HCM), Nguyễn Xuân Bách (GV R4 - HPC).
5. **Khối CNTT HCM (8 nhân sự + Leader Nguyễn Bá Minh Đạo - Rank 5 - Cơ sở HCM):**
   - Lê Hà Thanh Sang (GV R4), Lưu Hoàng Xuân Nguyên (TG R2), Phạm Viết Hùng (TG R2), Trần Quốc Tuấn (GV R3), Đặng Minh Luân (TG thử việc R1), Nguyễn Đức Minh (GV R4), Nguyễn Ngọc Sơn (TG thử việc R1), Phan Ngọc Tài (TG thử việc R1).
6. **Nhóm Dự Án LMS AI (2 nhân sự + Leader Trần Minh Cường - Rank 5):**
   - Ngọ Văn Quý (GV R4 - kiêm nhiệm), Lê Thành Ngọc (GV R3 - HCM).

### C. Triết Lý Thiết Kế Trực Quan Dành Cho Giám Đốc (3 Câu Hỏi Cốt Lõi):
1. **Leader này quản lý bao nhiêu nhân sự?**
2. **Bản thân Leader làm gương thế nào?** (Tỷ lệ báo cáo ngày, giờ dôi dư, badge đánh giá tính gương mẫu).
3. **Nhân sự trực thuộc Leader này có ai vượt định mức giờ, ai cần rà soát Rank?** (Thống kê tổng giờ dôi dư, clickable tags nhảy ngay vào nhân sự diện rà soát Rank hoặc cắt giờ ảo).

### D. Kiến Trúc Giao Diện 1 Màn Hình (Single-Pane of Glass):
- **Tầng 1 (Top Layer):** Cố định Overview toàn diện cho Trung tâm Đào tạo Công nghệ & Kinh tế số (41 nhân sự).
- **Tầng 2 (Filter Layer):** Bộ lọc Khối (6 Khối) + Cơ sở (3 Cơ sở) + Phân loại đề xuất + Tìm kiếm tức thì.
- **Tầng 3 (Leader Accountability Layer):**
  - Chế độ *Tất cả các Khối*: Grid 3 cột so sánh 6 Leader (Leader, quy mô nhân sự, % làm gương, giờ dôi dư, số nhân sự rà soát Rank) - hiển thị trọn vẹn không bị cắt chữ.
  - Chế độ *Chọn 1 Khối*: Thẻ Trách nhiệm Chi tiết của Leader khối đó kèm thanh điều hướng chuyển nhanh giữa các Leader và nút quay lại tổng quan.
- **Tầng 4 (Staff Master Table):** Danh sách nhân sự trực thuộc khối đào tạo tương ứng với bộ lọc, sắp xếp ưu tiên diện cần rà soát hạ Rank lên đầu.
- **Tầng 5 (Slide-over Offcanvas Drawer):** 4 Tab chi tiết (Task vượt chuẩn KPI Master, Task tự do bù giờ, Vênh Issue, Toàn bộ 20 ngày nhật ký) + Nút Sao Chép Phiếu Kiểm Toán 1-1 cho Leader.

---

## 9. Cập Nhật KPI Master Khối QTKD (Draft Tháng 8/2026)
- **Nguồn chân lý KPI QTKD mới:** `C:\Users\DELL\Downloads\[QTKDS] KPI Master (Draft - 8_2026).xlsx` (Sheet: `Sheet1`, 124 mục định mức chuẩn).
- **Cấu trúc Schema mới:** 9 cột, lấy định mức mới từ cột 6 `Standard Time (New)`.
- **Quy tắc mapping động khối QTKD trong engine kiểm toán:**
  - Nhận diện khối: `is_qtkd = "qtkd" in group.lower() or "kinh doanh" in group.lower()`.
  - Giảng dạy lý thuyết: Chuẩn hóa **180 phút (3.0h)** cho 1 session.
  - Triển khai buổi thực hành / Trợ giảng lên lớp: Chuẩn hóa **180 phút (3.0h)**.
  - Họp chuyên môn / giao ban: Chuẩn hóa **120 phút (2.0h)**; Họp triển khai: **60 phút (1.0h)**.
  - Trợ giảng CVHT: Rank 1 chuẩn hóa **90 phút (1.5h/ngày)**; Rank 2 chuẩn hóa **120 phút (2.0h/ngày)**.
  - Chấm thi sản phẩm có LMS AI hỗ trợ: **20 phút/SV**.
  - Trợ giảng kiểm tra BTVN: **40 phút/session**.
- **Nguyên nhân giờ dôi dư QTKD tăng (+277.9h):**
  - Barem mới đã cắt bỏ các "task bong bóng giờ ảo" của bản cũ (BTVN 960p, verify PM 960p, đề project 960p) làm tổng giờ chuẩn giảm từ 1,496h về 999h.
  - Tháng 8/2026 có tới 90.8% công việc phi giảng dạy (nghiên cứu tự do, làm việc ngoài lề chưa nghiệm thu), bộc lộ đúng bản chất các khoảng thời gian khai báo bù giờ của nhân sự.

---

## 10. Tối Ưu Hóa Fast Pipeline & Dịch Vụ Auto-Watcher (Cập Nhật 05/09/2026)

### A. Dữ Liệu Học Thuật Mới (KS24 Microservice & KS25 HCM PTTKHT):
- **Khối KS24 CNTT bắt đầu môn Microservice**: Dữ liệu ngày 04/09/2026 ghi nhận tại sheet `KS24_AI_Intergration (2)`:
  - `HN-K24-CNTT1(33-35)`: Bùi Thanh Hải (CC 0%, BT 0%, EL 20%, biến động +2 SV).
  - `HN-K24-CNTT2(39)`: Bùi Thanh Hải (EL 2.56%).
  - `HN-K24-CNTT3(41)`: Hồ Xuân Hùng (EL 12.20%).
  - `HN-K24-CNTT4(32)`: Bùi Thanh Hải (EL 6.25%).
  - `HCM-K24-CNTT1(43)`: Nguyễn Bá Minh Đạo (EL 4.65%).
- **Khối KS25 HCM tiếp tục ghi nhận ngày 04/09/2026 môn PTTKHT (`KS25_Phantichthietkehethong`)**:
  - `HCM-K25-CNTT8(36)`: Trần Quốc Tuấn (EL 27.27% - cảnh báo đỏ vi phạm môn mới).
  - `HCM-K25-CNTT7(39)`: Nguyễn Đức Minh (EL 7.69%).
  - `HCM-K25-CNTT6(38)`: Trần Quốc Tuấn (EL 5.26%).
  - `HCM-K25-CNTT5(39)`: Nguyễn Đức Minh (EL 0.00% - giữ kỷ luật hoàn hảo).

### B. Giải Pháp Đột Phá Triệt Tiêu Nghẽn 15 Phút:
1. **Auto-Watcher Daemon (`watch_and_sync.py` & `Bat_Dau_Tu_Dong_Dong_Bo.bat`)**:
   - Theo dõi thời gian thực file `C:\Users\DELL\Desktop\Backup\PTIT\PTIT_Chiso.xlsx`.
   - Ngay khi người dùng nhấn `Ctrl + S`, watcher kích hoạt `run_pipeline.py --fast` tự động sau 0.5s. Người dùng không cần mở AI chat hay gõ lệnh thủ công.
2. **Cơ Chế Fast Pipeline (`--fast`)**:
   - **DataSanitizer**: Bỏ thao tác mở và lưu đè Excel qua openpyxl (tiết kiệm 15s, chống lỗi định dạng). Chỉ copy nhanh và xuất Single Cache JSON trong ~3s.
   - **Worklane Smart Cache**: Bỏ qua 46 API request nặng khi chỉ cập nhật chỉ số đào tạo (tiết kiệm 82s).
   - **TKB Sessions Cache (`data/processed/tkb_rows_cache.json`)**: Cache hóa 11,132 ca học TKB, giúp Agent 3 đọc xong tức thì thay vì parse lại 2 sheet Excel khổng lồ.
   - Toàn bộ đường ống hoàn thành tự động trong dưới 45 giây và cập nhật đồng thời Markdown `data/report_kpi_gv_tg.md` cùng Master Dashboard HTML.

## 11. Danh Mục KPI Master Khối Ngoại Ngữ (Tiếng Nhật & Tiếng Anh)
- **Tệp Excel chuẩn**: `output/reports/KPI_Master_Khoi_Ngoai_Ngu.xlsx`.
- **Phạm vi áp dụng**: 3 nhân sự bộ môn Ngoại ngữ (Giáp Thị Minh Hằng - R5, Lò Thị Ngọc Anh - R5, Lê Thị Đỏ - R3); loại trừ Kỹ năng mềm theo chỉ đạo của Quản lý.
- **Cấu trúc 3 Sheets toàn diện**:
  1. `KPI_MASTER_MA_TRAN`: Ma trận tổng hợp 26 đầu việc chuẩn phân chia theo 6 Nhóm công việc (R&D CTĐT, Học liệu số, Giảng dạy, Khảo thí, LMS AI & Đối tác, Quản trị chuyên môn), định mức giờ và phút chi tiết cho 5 cấp Rank (R1 ➔ R5).
  2. `IMPORT_WORKLANE_DROPDOWN`: 119 bản ghi cấu hình chuẩn xác theo form file CNTT (`Quản lý hiệu suất đào tạo.xlsx`) và QTKD (`_Task Management_ QL Khối QTKD.xlsx`) để nạp trực tiếp vào cơ sở dữ liệu dropdown trên Worklane.
  3. `MAPPING_WORKLANE_TASKS`: Ánh xạ toàn bộ 283 tasks thực tế trên Worklane của Khối Ngoại ngữ sang các Mã Key chuẩn, đảm bảo độ bao phủ 100% nghiệp vụ thực tế.

---

## 12. Cập Nhật Dữ Liệu Ngày 07/09/2026 & Tinh Chỉnh So Sánh Tiến Độ (Agent 1)
- **Dữ liệu mới ngày 07/09/2026**:
  - `KS24_AI_Intergration (2)`: Ghi nhận cột ngày `07/09/2026`. `HN-K24-CNTT1` vắng chuyên cần đột biến **11.43%**, Elearning giữ **20.00%**. `HN-K24-CNTT4` Elearning tăng lên **12.50%**.
  - `KS25_Phantichthietkehethong`: Ghi nhận cột ngày `07/09/2026`. `HCM-K25-CNTT8` biến động sĩ số `(36-33)`, chuyên cần tăng vọt **24.24%**, Elearning lên **33.33%** (báo động đỏ). `HCM-K25-CNTT7` Elearning tăng lên **12.82%**. `HCM-K25-CNTT6` biến động sĩ số `(38-37)`, Elearning giảm còn **2.70%**.
- **Bài học kinh nghiệm & Sửa lỗi logic Agent 1**:
  - `size_alerts_list`: Khai báo bên ngoài vòng lặp sheets để tránh bị ghi đè rỗng ở sheet cuối trong `calculate_kpi_json.py`.
  - Cơ chế `is_new_course`: Chỉ áp dụng mốc so sánh 0% khi môn mới **có dưới 2 buổi học** (`len(valid_dates) < 2`). Khi đã có từ 2 buổi trở lên (buổi 2, buổi 3...), phải so sánh chính xác tiến độ của buổi hiện tại với buổi liền trước cùng môn để phản ánh đúng gia số vi phạm thực tế.
## 13. Cập Nhật KPI Master Khối CNTT (Bản FINAL - 08/09/2026)
- **Nguồn dữ liệu chân lý mới**: `C:\Users\DELL\Downloads\KPI_MASTER_Giang_vien_Tro_giang_FINAL.xlsx` (249 định mức chi tiết).
- **Tệp Markdown hệ thống**: `data/inputs/kpi_master_cntt_final.md`.
- **Báo cáo chuyên đề phân tích so sánh**: `docs/reports/2026-09-08-so-sanh-kpi-master-cntt-va-cai-thien-hieu-suat.md`.
- **Quy tắc cấu trúc & Kiến trúc định mức mới**:
  - **Mã Key chuẩn hóa**: Cấu trúc `Role-Rank-Task Type` (100% duy nhất, 0 trùng lặp).
  - **Triệt tiêu giờ ảo học liệu**: 0 nhiệm vụ sản xuất học liệu tự do. Thay vào đó là **18 Task Type Review Độc Lập** (162 định mức từ R1 đến R8) với điều kiện đầu ra khắt khe (*Checklist + Danh sách lỗi/góp ý + Kết luận Đạt/Không đạt; người review độc lập với người sản xuất*).
  - **Khống chế Re-review**: Ghi nhận tối đa 50% thời gian review lần đầu (tối thiểu 15 phút), không tạo task riêng.
  - **Chuẩn hóa Giảng dạy trực tiếp**: Đồng bộ **120 phút/buổi (2.0h)** cho cả Lý thuyết, Thực hành và Mini-project. Mỗi buổi chỉ ghi nhận 1 loại triển khai.
  - **Khảo thí khoán theo lớp**: Chấm KT 30 phút đầu giờ cố định **120 phút/lớp** (không nhân theo số sinh viên).
  - **Phân định Giảng viên Rank 6-8**: Không dạy hoặc vận hành lớp; chỉ làm Chuyên gia Review và Khảo thí cấp cao (Tổng định mức 1 vòng chỉ còn 21.4h so với 44.1h ở bản cũ).
  - **Trợ giảng**: Bổ sung Rank 3 (chuẩn 44.1h).
- **Đồng bộ hóa hệ thống Agents & Dashboards**:
  - `agents/audit/audit_worklane_performance.py`: Tự động ưu tiên đọc bản FINAL, ánh xạ chuẩn thực hành 120p và 18 loại review.
  - **Triệt tiêu hoàn toàn Fallback cũ (Bugfix 08/09/2026)**: Đã xóa bỏ toàn bộ heuristic cũ gán "Làm slide = 0.75h", "Làm mindmap = 0.25h-0.5h", "Xây dựng Quiz/Bài đọc" cho CNTT. Trong KPI Master FINAL CNTT, mọi task tự sản xuất không qua Review lệnh được chuyển đúng bản chất thành `is_wildcard = True` (Sản xuất học liệu ngoài Master Barem - Cần nghiệm thu sản phẩm), tránh kết luận sai lệch là "vượt định mức 100%".
  - `agents/core/agent_4_daily_logs/analyze_daily_logs.py`: Tối ưu hóa khớp Key format mới, loại bỏ "soạn slide" khỏi nhóm chuẩn bị giảng dạy, và pre-index Worklane issues theo assignee (O(1) lookup), rút ngắn thời gian chạy từ >60s xuống 3s.
  - `agents/master/agent_5_master_portal/analyze_kpi_opportunities.py`: Nạp 249 định mức mới để xuất ma trận đề xuất `output/reports/proposed_kpi_master.xlsx`.
  - `output/dashboards/audit/worklane_staff_audit.html` & `output/dashboards/core/agent_5_master_portal.html`: Tự động làm mới 100% số liệu.

## 14. Nâng Cấp Auto-Watcher Vĩnh Viễn & Cập Nhật Dữ Liệu 08/09/2026
- **Căn nguyên vấn đề không tự động hóa**:
  - Script watcher trước đó (`Bat_Dau_Tu_Dong_Dong_Bo.bat`) chỉ chạy khi người dùng tự mở cửa sổ CMD. Khi máy khởi động lại hoặc tắt terminal, không có tiến trình nào theo dõi file Excel trên Desktop.
  - Xung đột file lock: Khi người dùng bấm Ctrl + S trên Excel, Excel tạm thời khóa file trong 0.5 - 1s, dễ dẫn đến lỗi PermissionError nếu đọc ngay.
- **Giải pháp dứt điểm đã triển khai**:
  1. **Chạy ngầm vĩnh viễn (Silent Daemon)**: Sử dụng `scripts/run_watcher_silent.vbs` để chạy ngầm hoàn toàn qua `wscript.exe` với `WindowStyle = 0` (không hiện cửa sổ console).
  2. **Tự khởi động cùng Windows (Startup Folder)**: Đăng ký shortcut `AutoSync_PTIT_Chiso.lnk` vào `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup` để tự động kích hoạt mỗi khi mở máy.
  3. **Cơ chế chống đọc sớm (Debounce & File Lock Safety)**: Tự động chờ Excel ghi xong file hoàn toàn trước khi kích hoạt `run_pipeline.py --fast`.
  4. **Singleton Lock**: Quản lý PID chính xác, đối chiếu tên tiến trình để tránh sinh nhiều bản sao watcher.
  5. **Thông báo Windows Native**: Bật thông báo Windows Balloon Tip ngay khi đồng bộ xong để người dùng biết báo cáo đã sẵn sàng mà không cần kiểm tra thủ công.
- **Dữ liệu mới ngày 08/09/2026 đã tích hợp vào hệ thống**:
  - Ghi nhận 11 lớp có số liệu mới:
    - *KS24 CNTT*: `HN-K24-CNTT1` (CC 8.57%, BT 5.71%, EL 20.0%), `HN-K24-CNTT2` (EL 5.13%), `HN-K24-CNTT3` (CC 9.52%, EL 14.29%), `HN-K24-CNTT4` (CC 3.13%, BT 3.13%, EL 12.5%), `HCM-K24-CNTT1` (EL 6.98%).
    - *KS25 HCM (PTTKHT)*: `HCM-K25-CNTT8` (CC 21.88%, EL 31.25%), `HCM-K25-CNTT5` (CC 6.82%, EL 2.27%), `HCM-K25-CNTT6` (EL 4.26%), `HCM-K25-CNTT7` (EL 19.57%).
    - *KS25 QTKD*: `HN-K25-QTKD1` (CC 4.0%), `HN-K25-QTKD2` (CC 3.0%).
  - Tất cả Dashboard HTML và Báo cáo Markdown `data/report_kpi_gv_tg.md` đã được làm mới đồng bộ 100%.

## 15. Tái Cơ Cấu Khối QTKD (MAN107) & Triệt Tiêu Hardcode Sheet
- **Căn nguyên vấn đề số liệu QTKD không cập nhật**:
  - `weekly_groups` trong `generate_kpi_report.py` (Agent 1 & Agent 5) và `calculate_kpi_json.py` từng bị gán cứng vào môn cũ `KS25_QTKD_BA201` với 3 lớp (`QTKD1`, `QTKD2`, `QTKD3`).
  - Khi Excel có môn mới `KS25_QTKD_MAN107`, hệ thống bỏ qua và không nhận diện được biến động giảm lớp và tăng sĩ số.
- **Quy chuẩn tái cơ cấu Khối QTKD (Từ 08/09/2026 - Môn MAN107)**:
  - **Giảm số lượng lớp**: Khối QTKD giảm từ **3 lớp xuống 2 lớp** (`HN-K25-QTKD1` và `HN-K25-QTKD2`). Lớp `HN-K25-QTKD3` đã giải thể và sáp nhập sinh viên sang 2 lớp còn lại.
  - **Biến động sĩ số tăng lên**:
    - `HN-K25-QTKD1(46)`: Sĩ số tăng mạnh từ **33 ➔ 46 SV (+13 SV, +39.4%)**.
    - `HN-K25-QTKD2(42)`: Sĩ số tăng từ **39 ➔ 42 SV (+3 SV, +7.7%)**.
    - Tổng quy mô: **88 SV** (giảm 10 SV so với 98 SV ở môn BA201).
  - **Giảng viên phụ trách**: Cô **Đặng Quỳnh Trang** đảm nhận giảng dạy cả 2 lớp môn MAN107.
  - **Chỉ số kỷ luật thực tế**: 100% SV đi học đủ (Vắng CC **0.00%** cả 2 lớp); Nợ BT **0.00%**; Vi phạm Elearning: QTKD1 là **2.17%** (1/46 SV), QTKD2 là **9.52%** (4/42 SV).
- **Cơ chế đồng bộ tự động**:
  - `data_sanitizer.py`: Tự động phát hiện biến động sĩ số liên môn (cross-course size change) và cảnh báo tái cơ cấu quy mô số lượng lớp.
  - Tự động ưu tiên chọn sheet mới nhất `KS25_QTKD_MAN107` khi tồn tại trong workbook.

---

## 16. Đồng Bộ Bộ 3 KPI Master & Kiểm Toán Worklane (01/09 - 08/09/2026)
- **Bộ 3 KPI Master chuẩn hóa**:
  1. **Khối Ngoại ngữ & KNM**: Nạp trực tiếp từ `C:\Users\DELL\Downloads\[ENG&JPN] KPI MASTER KHỐI ĐÀO TẠO NGOẠI NGỮ.xlsx` (118 định mức Rank 1-5, 270 mapping Worklane tasks). Tỷ lệ vênh giờ thấp nhất toàn viện (**+33.1%**, dôi dư +24.8h), chứng minh tính thực tiễn cao của barem.
  2. **Khối CNTT**: Nạp từ `C:\Users\DELL\Downloads\KPI_MASTER_Giang_vien_Tro_giang_FINAL.xlsx` (249 định mức, 18 loại review độc lập, thực hành/lý thuyết 120p, khảo thí khoán theo lớp 120p). Phía HCM tuân thủ tốt (+37.4%), phía Hà Nội còn dôi dư cao (+184.6%) do cần dứt điểm chuyển đổi sang 18 Task Review.
  3. **Khối QTKD**: Nạp từ `C:\Users\DELL\Downloads\[QTKDS] KPI Master (Draft - 8_2026).xlsx` (124 định mức, giảng dạy 180p, CVHT 90-120p). 100% nộp báo cáo ngày môn MAN107.
- **Quy chuẩn kiểm toán 01/09 - 08/09/2026**:
  - **Số ngày làm việc tiêu chuẩn**: 4 ngày (03, 04, 07, 08/09; ngày 01-02/09 nghỉ lễ Quốc khánh; 05-06/09 cuối tuần). Định mức chuẩn toàn thời gian là 32h/nhân sự.
  - **Tỷ lệ nộp báo cáo ngày**: 86.0% (141/164 lượt). 3 nhân sự bỏ trống (Hồ Xuân Hùng, Trần Minh Cường, Ngô Quang Huấn).
  - **Giờ khai báo**: 1,067.9h | Chuẩn Master: 604.0h | Dôi dư: +468.4h (+77.5%).
- **Kiến trúc Dashboard Đa Kỳ (`worklane_staff_audit.html`)**:
  - Hỗ trợ Period Switcher cho phép Giám đốc chuyển đổi mượt mà giữa:
    - `[⚡ Kỳ 01/09 - 08/09/2026 (Mới)]`
    - `[📅 Tháng 08/2026 (Lịch sử)]`
  - Động hóa 100% thẻ 6 Leader (`getDynamicLeaderInfo`) theo từng kỳ kiểm toán, không còn hardcode số liệu tĩnh.
  - Slide-over Drawer hỗ trợ 4 Tab (Task Vượt Chuẩn, Task Ngoài Barem, Vênh Ticket, Nhật Ký Đầy Đủ) kèm nút Sao chép Phiếu làm việc 1-1 cho Leader.
- **Báo cáo chuyên đề mới**: `docs/reports/2026-09-09-kiem-toan-worklane-01-08-thang-9-theo-kpi-master-moi.md`.

---

## 17. Quy Chuẩn So Sánh T8 vs T9 & Kiến Trúc Dashboard Chống Vỡ Khung (09/09/2026)
- **Chuẩn Hóa Thước Đo So Sánh Khi Số Ngày Làm Việc Khác Biệt**:
  - Khi so sánh 2 kỳ kiểm toán lệch nhau về thời gian (Tháng 8 có 20 ngày công, Kỳ 01-08/09 có 4 ngày công), tuyệt đối không so sánh tổng số giờ dôi dư tuyệt đối vì sẽ tạo ra sai lệch ảo (105h của 4 ngày trông nhỏ hơn 500h của 20 ngày nhưng thực tế cường độ dôi dư cao hơn).
  - Bắt buộc áp dụng 2 chỉ số chuẩn hóa:
    1. **Tỷ lệ vênh giờ (%)**: $\frac{\text{Tổng giờ dôi dư}}{\text{Tổng giờ chuẩn}} \times 100\%$.
    2. **Giờ dôi dư trung bình / ngày / nhân sự (h/ngày/NS)**: $\frac{\text{Tổng giờ dôi dư}}{\text{Số ngày làm việc} \times \text{Số nhân sự}}$.
  - Dữ liệu so sánh được tính toán và lưu tại `data/processed/worklane_comparison_t8_t9.json`.
- **Quy Chuẩn Chart.js Lifecycle Management (Tránh Lỗi Canvas Reuse)**:
  - Khi render biểu đồ Chart.js trong SPA động hoặc khi chuyển đổi kỳ kiểm toán:
    - Bắt buộc lưu instance của Chart vào biến toàn cục (`window.chartExcessInstance`, `window.chartDailyInstance`).
    - Trước khi khởi tạo biểu đồ mới `new Chart(ctx, ...)`, luôn kiểm tra và gọi `instance.destroy()`.
    - Thao tác này triệt tiêu hoàn toàn lỗi runtime `Error: Canvas is already in use. Chart with ID 'x' must be destroyed before the canvas with ID 'y' can be reused`.
- **Kiến Trúc Giao Diện Chống Tràn Dòng & Giữ Cân Bằng Thẻ Leader**:
  - **Header Thẻ Leader (2 tầng)**:
    - Dòng 1: Họ và tên nhân sự hiển thị độc lập, font chữ `font-bold text-sm tracking-tight text-white`, bọc trong `truncate` để không bao giờ bị rớt dòng khi tên dài (ví dụ: *Nguyễn Bá Minh Đạo*, *Hoàng Thị Kim Oanh*).
    - Dòng 2: Chứa Rank Badge (ví dụ: `R5-Leader`) và Trạng thái nộp log (`4/4 ngày (100%)`) sử dụng `flex items-center gap-1.5 flex-wrap` để tự co giãn linh hoạt.
    - Cấu trúc khung thẻ: `h-full flex flex-col justify-between` đảm bảo cả 6 thẻ trên grid luôn có chiều cao bằng nhau tuyệt đối, không có tình trạng thẻ dài thẻ ngắn.
  - **Danh sách Tag nhân sự diện Rà soát Rank & Cắt giờ ảo**:
    - Dùng `inline-flex max-w-full items-center text-xs truncate px-2 py-0.5 rounded-md` thay vì để text tự do, đảm bảo dù tên giảng viên dài cỡ nào thì tag vẫn vừa vặn trong ô và tự động hiển thị dấu `...` khi thiếu không gian.

---

## 18. Cập Nhật Môn Mới KS25 Hà Nội & KS24 Microservices (Ngày 09/09/2026)
- **Cột Mốc Môn Học Mới Ngày 09/09/2026**:
  1. **Khóa KS25 CNTT Hà Nội**:
     - Chính thức bắt đầu học môn mới **Phân tích thiết kế hệ thống** (chung sheet `KS25_Phantichthietkehethong` với cơ sở HCM).
     - Ghi nhận 5 lớp hoạt động:
       - `HN-K25-CNTT1(40-27)` (GV Nguyễn Quảng An): Sĩ số giảm mạnh từ 40 ➔ 27 SV (-13 SV). Buổi đầu: CC 0.0%, BT 0.0%, EL vi phạm 20.0% (báo động đỏ).
       - `HN-K25-CNTT2(38-30)` (GV Nguyễn Quảng An): Sĩ số giảm từ 38 ➔ 30 SV (-8 SV). Buổi đầu: CC 0.0%, BT 0.0%, EL 4.88%.
       - `HN-K25-CNTT3(35)` (GV Phạm Tuấn Bình): Sĩ số 35 SV. Buổi đầu: CC 0.0%, BT 0.0%, EL 11.63%.
       - `HN-K25-CNTT4(38-38)` (GV Phạm Tuấn Bình): Sĩ số 38 SV (giảm 2 SV so với môn trước 40 SV). Buổi đầu: CC 0.0%, BT 0.0%, EL 5.26%.
       - `HN-K25-CNTT5(41-31)` (GV Nguyễn Quảng An): Sĩ số giảm từ 41 ➔ 31 SV (-10 SV). Buổi đầu: CC 0.0%, BT 0.0%, EL 4.88%.
     - Điểm tích cực: 100% sinh viên đi học đầy đủ buổi khai giảng (CC vắng 0.0%), nợ bài tập 0.0%.
  2. **Khóa KS24 CNTT (Hà Nội & HCM-CNTT1)**:
     - Bắt đầu học môn mới **KS24_AI_Microservice** (thay cho `KS24_AI_Intergration`).
     - Ghi nhận 5 lớp: `HN-K24-CNTT1(35-31)` (GV Bùi Thanh Hải), `HN-K24-CNTT2(39)` (GV Bùi Thanh Hải), `HN-K24-CNTT3(42)` (Leader Hồ Xuân Hùng), `HN-K24-CNTT4(32-31)` (GV Bùi Thanh Hải), `HCM-K24-CNTT1(43)` (Leader Nguyễn Bá Minh Đạo).
  3. **Khóa KS25 QTKD Hà Nội (MAN107)**:
     - Tiếp tục buổi học thứ hai ngày 09/09: `HN-K25-QTKD1(46)` (CC 2.17%, EL 2.17%), `HN-K25-QTKD2(42)` (CC 9.52%, EL 9.52%). GV Đặng Quỳnh Trang đảm nhiệm.
- **Quy Chuẩn Đồng Bộ Codebase**:
  - `calculate_kpi_json.py`, `generate_kpi_report.py` (Agent 1 & Agent 5): Đã cập nhật `weekly_groups['KS25_CNTT_HN']['sheet_curr'] = 'KS25_Phantichthietkehethong'` và `weekly_groups['KS24_CNTT_HN']['sheet_curr'] = 'KS24_AI_Microservice'`.
  - Toàn bộ pipeline tự động hóa `run_pipeline.py` đã thực thi trơn tru, đồng bộ dữ liệu vào `data/report_kpi_gv_tg.md`, các dashboard HTML và cache JSON.

---

## 19. Cập Nhật Dữ Liệu Ngày 10/09/2026 & Nâng Cấp Dự Báo Học Thuật Agent 2 (KS24 Microservice, KS25 PTTKHT, KS25 QTKD MAN107)
- **Đồng bộ Dữ liệu Mới Ngày 10/09/2026**:
  - `PTIT_Chiso.xlsx`: Tích hợp cột ngày 10/09/2026 trên cả 3 sheet:
    - `KS24_AI_Microservice`: `HN-K24-CNTT1(35-31)` (CC 0%, BT 3.13%, EL 19.35%), `HN-K24-CNTT2(39)` (CC 2.56%, BT 7.69%, EL 5.13%), `HN-K24-CNTT3(42)` (CC 11.90%, BT 7.14%, EL 16.67% - cảnh báo đỏ), `HN-K24-CNTT4(32-31)` (CC 0%, BT 0%, EL 9.68%), `HCM-K24-CNTT1(43)` (CC 0%, BT 0%, EL 6.98%).
    - `KS25_Phantichthietkehethong`: Hà Nội kết thúc buổi thứ hai ngày 10/09/2026 (`HN-K25-CNTT1` EL 19.51%, các lớp khác EL < 5%); Phía HCM đã học 5-6 buổi, lớp `HCM-K25-CNTT8(36-33-32)` vắng CC tích lũy 37.5%, EL 31.25% (báo động đỏ).
    - `KS25_QTKD_MAN107`: Ghi nhận cột ngày 10/09/2026 cho 2 lớp: `HN-K25-QTKD1(46)` (CC 8.70%, BT 0%, EL 0%), `HN-K25-QTKD2(42)` (CC 11.90%, BT 2.38%, EL 7.14%).
- **Nâng Cấp Động Agent 2 (AcademicPredictor)**:
  - **Ánh xạ 3 Môn Hiện Tại**:
    - KS24 CNTT: Current Course `[IT-214] Microservices System Design` (ID: 216), Verification Course `[IT-213] AI Integration in Action` (ID: 220), CDC = 1.45.
    - KS25 CNTT: Current Course `[IT105-K25] Phân tích & thiết kế hệ thống` (ID: 224), Verification Course `[IT-215] Python Web` (ID: 217), CDC = 1.25.
    - KS25 QTKD: Current Course `[MAN107] Quản trị chiến lược doanh nghiệp` (ID: 213), Verification Course `[BA201] Phân tích nghiệp vụ` (ID: 222), CDC = 1.10.
308: 
309: ---
310: 
311: ## 20. Chốt Chặn 16 Lớp PTIT Chính Quy & Nâng Cấp Presentation Mode Cho Agent 2
312: - **Khắc Phục Dứt Điểm Lỗi Lấy Toàn Bộ Lớp Trong DB**:
313:   - **Nguyên nhân**: Trong `agents/core/agent_2_academic_pred/run.py`, logic cũ quét bảng `qldt_el.classes` bằng regex `KS24|KS25` lỏng lẻo, vô tình kéo theo các lớp tiếng Nhật (`HN-JPN-...`), tiếng Anh (`HN-ENG-...`), các lớp đình chỉ hoặc giải thể.
314:   - **Quy chuẩn chốt chặn**: Agent 2 bắt buộc phải đọc trực tiếp danh sách 16 lớp chính quy từ `data/processed/agent1_output.json` (`active_a1_map`). Chỉ duyệt đúng 16 lớp PTIT hiện tại đang học (5 lớp KS24, 9 lớp KS25 CNTT, 2 lớp KS25 QTKD). 100% lớp rác, ngoại ngữ, đình chỉ bị loại bỏ ngay từ đầu pipeline.
315: - **Nâng Cấp Giao Diện Báo Cáo Trực Quan Cho Giám Đốc (Presentation Mode)**:
316:   - Bổ sung nút **"Chế độ Chụp Báo Cáo"** (`togglePresentationMode`): Khi kích hoạt, thanh điều hướng tab được ẩn đi, bố cục trang được co gọn chuẩn tỷ lệ 16:9 để chụp màn hình đưa vào slide báo cáo không bị vướng navigation.
317:   - **3 Biểu đồ Chart.js Chuẩn SaaS Executive**:
318:     1. `pred-compare-chart`: Biểu đồ cột kép so sánh Quy chuẩn cũ vs Quy chế mới cho 16 lớp, tích hợp 2 đường mốc chuẩn nét đứt (Xanh 70% An toàn, Đỏ 50% Báo động) và bộ 4 nút lọc khối lớp nhanh (`Tất cả`, `KS24`, `KS25`, `QTKD`).
319:     2. `risk-doughnut-chart`: Biểu đồ donut 3 màu tương phản cao (Xanh - Vàng - Đỏ) kèm tâm số hiển thị tổng sĩ số sinh viên toàn viện.
321:   - Đã kiểm toán tự động bằng Visual QA qua `browser_subagent`: 0 lỗi JavaScript, giao diện sắc nét, biểu đồ phản hồi tức thì.
322: 
323: ---
324: 
325: ## 21. Chuẩn Hóa Thuật Ngữ Đào Tạo Chính Quy & Tách Biệt 3 Khối Đào Tạo (Agent 2)
326: - **Chuẩn Hóa Ngôn Từ Quản Lý Đào Tạo (Loại Bỏ Hoàn Toàn AI-Like Terms)**:
327:   - *Nguy cơ Cao (Báo động Đỏ)* ➔ **Cảnh Báo Mức 1 (Nguy Cơ Cấm Thi)**.
328:   - *Cảnh báo Vàng (Theo dõi)* ➔ **Cảnh Báo Mức 2 (Học Lực Cần Theo Dõi / Cận Ngưỡng)**.
329:   - *An toàn & Đạt chuẩn* ➔ **Tiến Độ Học Tập Đạt Chuẩn**.
330:   - *Care List / Can thiệp* ➔ **Sổ Tay Theo Dõi Học Viên Diện Cảnh Báo Học Vụ / Biện Pháp Hỗ Trợ**.
331:   - *Quy chuẩn cũ vs Quy chế mới* ➔ **Quy Chế Cũ vs Quy Chế Hiện Hành**.
332:   - *Hệ số phạt môi trường Peer Pressure / Hệ số Env* ➔ **Hệ Số Nề Nếp Lớp Học**.
333:   - *Chế độ Chụp Báo Cáo* ➔ **Chế Độ Trích Xuất Báo Cáo**.
334: - **Phân Tách Rạch Ròi Overview Theo 3 Khối Ngành Đào Tạo**:
335:   - Bổ sung cụm 3 thẻ chuyên sâu (3-Cohort Breakdown Cards) ngay đầu Tab 1:
336:     1. **Khóa KS24 CNTT** (Môn Microservices - 5 lớp): Sĩ số, Tỷ lệ dự kiến đỗ, Tỷ lệ vi phạm lớp, Cảnh báo học vụ, Đánh giá giáo vụ.
337:     2. **Khóa KS25 CNTT** (Môn PTTKHT - 9 lớp): Phân tích phân hóa rõ rệt giữa cơ sở Hà Nội (5 lớp mới học 2 buổi) và cơ sở HCM (4 lớp, điểm nóng `HCM-K25-CNTT8` vắng 37.5%).
338:     3. **Khóa KS25 QTKD** (Môn MAN107 - 2 lớp): 100% học viên an toàn, nề nếp đạt chuẩn.
339: - **Minh Bạch Hóa Phương Pháp Luận Xác Định Tỷ Lệ Dự Kiến Qua Môn**:
340:   - Tích hợp Hộp Giải trình Giáo vụ: Tỷ lệ dự kiến là **Kỳ vọng xác suất qua môn trung bình ($E[Pass]$)** kết hợp Điểm kỷ luật quá trình (40%), Năng lực học thuật tích lũy (60% - chia CDC độ khó) và Chốt chặn cấm thi quy chế.
341:   - Giải trình rõ lý do con số giai đoạn này ở mức khả quan (61% – 78%): Các lớp Hà Nội mới học 2 buổi đầu nên chuyên cần cao kéo điểm kỳ vọng lên; Bài thi cuối kỳ / Đồ án tốt nghiệp (50% trọng số) chưa diễn ra.
