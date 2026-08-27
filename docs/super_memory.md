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
