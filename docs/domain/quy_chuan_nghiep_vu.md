# Quy chuẩn Nghiệp vụ Đào tạo (tham chiếu)

> Trích từ `super_memory.md` ngày 04/10/2026. Đây là **tài liệu tham chiếu**, không nạp mỗi phiên.
> Khi một mục đã được mã hóa (registry, config, test) thì code là nguồn sự thật — mục ở đây chỉ để giải thích.
> - Danh mục lớp/GV K26: tự đồng bộ từ LMS (`data/warehouse/<kỳ>/registry.json`) — mục 1 có thể lỗi thời.
> - Công thức CC/BT/EL (mục 7): `pmo/metrics/lms_fe.py` + `tests/`.

## 1. Danh Mục 16+ Lớp Học Chính Quy PTIT (Phạm Vi Chốt Chặn)
Hệ thống **chỉ duyệt đúng lớp chính quy PTIT** hiện tại đang đào tạo:
1. **Khóa KS24 CNTT (5 lớp - Môn `DevOps & CI/CD Pipeline`)**:
   - `HN-K24-CNTT1` (Bùi Thanh Hải), `HN-K24-CNTT2` (Bùi Thanh Hải), `HN-K24-CNTT3` (Hồ Xuân Hùng), `HN-K24-CNTT4` (Bùi Thanh Hải), `HCM-K24-CNTT1` (Nguyễn Bá Minh Đạo).
2. **Khóa KS25 CNTT (8 lớp - Môn `Phân tích & thiết kế hệ thống` [IT105-K25])**:
   - Hà Nội (5 lớp): `HN-K25-CNTT1` - `HN-K25-CNTT5` (GV Nguyễn Quảng An R4, Phạm Tuấn Bình R3).
   - TP. HCM (3 lớp): `HCM-K25-CNTT5`, `HCM-K25-CNTT6`, `HCM-K25-CNTT7` (GV Nguyễn Đức Minh R4, Trần Quốc Tuấn R3). **Lớp HCM-K25-CNTT8 đã giải thể**.
3. **Khóa KS25 QTKD (2 lớp - Môn `Business Intelligence [BI]`)**:
   - `HN-K25-QTKD1` (46 SV - GV Hoàng Thị Kim Oanh), `HN-K25-QTKD2` (42 SV - GV Lê Thành Ngọc).
4. **Khóa KS26 (10 lớp - Đa môn đồng thời)**:
   - HN CNTT: `HN-KS26-CNTT1` (43 SV), `HN-KS26-CNTT2` (40 SV), `HN-KS26-CNTT3` (41 SV), `HN-KS26-CNTT4` (29 SV).
   - HCM CNTT: `HCM-KS26-CNTT1` (46 SV), `HCM-KS26-CNTT2` (45 SV).
   - QTKD: `HN-K26-QTKD1` (44 SV), `HN-K26-QTKD2` (45 SV), `HN-K26-QTKD3` (44 SV), `HCM-K26-QTKD1` (21 SV).

---

## 2. Quy Chuẩn Dự Báo Học Thuật & Chốt Chặn Cấm Thi (Agent 2)
- **Hệ số độ khó môn học (CDC)**: Microservices (1.45), PTTKHT (1.25), MAN107 (1.10).
- **Điểm Kỷ luật môn trước**: KS25 đọc `total_score` từ bảng `auto_rpoints`. KS24 đọc cột `rpoints` trong bảng `final_results`.
- **Chốt chặn cấm thi**: Chỉ áp dụng khi **số buổi học > 3**. Không chặn Project giữa kỳ.
- **Hệ số nề nếp lớp học**: Áp dụng khi tỷ lệ vi phạm > 10%.

---

## 3. Bộ 3 Barem KPI Master & Quy Tắc Khai Báo Giờ Công
1. **Khối CNTT** (`KPI_MASTER_Giang_vien_Tro_giang_FINAL.xlsx`): Chuẩn 120 phút/buổi (2.0h). 18 Task Type Review. Khảo thí khoán 120 phút/lớp.
2. **Khối QTKD** (Draft T8/2026): GV 180 phút (3.0h). TG CVHT: R1 = 90 phút, R2 = 120 phút.
3. **Khối Ngoại ngữ**: 118 định mức R1-5, 270 mapping Worklane tasks.

---

## 4. Quy Tắc Kiểm Toán Task Quá Hạn & Đánh Giá Nhân Sự
- Task trễ hạn **CHỈ tính lỗi** khi task ở trạng thái **"Cần làm"** hoặc **"Đang làm"**.
- Trạng thái **"Chờ duyệt"** → **MIỄN TRỪ LỖI** hoàn toàn cho nhân sự.
- Giờ công chuẩn: 40h/tuần (8h/ngày).

---

## 5. Danh Mục 6 Khối & 6 Leader
1. **Khối CNTT Hà Nội (12 NS)**: Leader Hồ Xuân Hùng (R5).
2. **Khối QTKD (8 NS)**: Leader Hoàng Thị Kim Oanh (R5).
3. **Khối Ngoại ngữ & KNM (3 NS)**: Leader Giáp Thị Minh Hằng (R5).
4. **Khối QLCLĐT (3 NS)**: Leader Nguyễn Thị Tươi (R4).
5. **Khối CNTT HCM (8 NS)**: Leader Nguyễn Bá Minh Đạo (R5).
6. **Nhóm Dự án LMS AI (2 NS)**: Leader Trần Minh Cường (R5).

---

## 6. Kiến Trúc Pipeline & Cấu Trúc Đầu Ra
- **DataSanitizer** → Single Source Cache `data/processed/classes_metrics_cache.json`.
- **Pipeline song song**: Nhánh A (Agent 1+2 Học thuật) // Nhánh B (Agent 3+4 Tác nghiệp) → Agent 5 (Master Portal).
- **Cấu trúc Dashboard**:
  - `output/dashboards/core/`: Agent 1-5
  - `output/dashboards/management/`: Director Cockpit, Worklane Staff Audit, Weekly Director Report
  - `output/dashboards/academic/`: KS24, KS25, KS26 theo môn
  - `deploy_web/`: Mirror cho hosting web

---

## 7. 🔴 QUY CHUẨN VÀNG: Hiển Thị Chỉ Số Học Vụ Theo Chuẩn LMS Frontend (BẮT BUỘC)

> **CẢNH BÁO NGHIÊM TRỌNG**: Backend API trả giá trị KHÁC với LMS Frontend. Lỗi này đã tái phạm **8 lần** (Mục 30-34 trong archive). Module `lib/lms_fe_formulas.js` là Single Source of Truth duy nhất.

### 7.1 Chuyên cần (CC ≥ 10%)
- **Backend API**: `absence.rate` chỉ có `absentSessions / plannedSessions × 100`. KHÔNG tách riêng Vắng KP / CP / Muộn.
- **Frontend LMS**: Quy đổi: `Vắng_KP×1.0 + CP×0.5 + Muộn×0.5` / tổng buổi > 10%.
- **Giới hạn chấp nhận**: Dùng `absence.rate > 10` từ API. Sai lệch 1-2 SV so với FE do thiếu field chi tiết.
- **Muốn chính xác 100%**: Phải scrape FE bằng `browser_subagent`.

### 7.2 Bài tập về nhà (BTVN)
- **Backend API**: `homework.rate = done / total_hw_cả_môn` → **GÂY PHẠT ẢO 75-100%**.
- **Frontend LMS**: CHỈ tính bài **ĐÃ ĐẾN HẠN** (`current_due_hw`). SV nộp đủ bài đến hạn → 0%.
- **Công thức chuẩn**: Dùng Q3 (percentile 75) của `done` để suy luận `currentDueHw`. Nếu ≥80% SV done=0 → chưa giao bài → 0%.
- ⛔ **TUYỆT ĐỐI KHÔNG dùng `homework.rate` từ API**.

### 7.3 Elearning
- **Backend API**: `elearning.rate` (% hoàn thành đúng hạn). Gần khớp FE.
- **Frontend LMS**: Đếm số bài trễ tuyệt đối ("Chậm 1 bài", "0 bài").
- **Công thức**: SV có `elearning.rate < 100` → vi phạm.

---

## 8. Kiến Trúc Data-Driven KS26 (Mới — 02/10/2026)

### 8.1 Vấn đề đã xử lý
- `generate_weekly_director_dashboard.py` (295KB / 3,607 dòng) hardcode HTML tĩnh → lỗi tái phạm 8 lần.
- Nguyên nhân: snapshot data cũ, courseClassId stale, sửa 1 view quên 2 view.

### 8.2 Kiến trúc mới
```
LMS MCP API → scripts/fetch_ks26_live.js → data/processed/ks26_live_metrics.json → Dashboard JS render
                   ↑                                                                      ↑
            lib/lms_fe_formulas.js                                              Template-driven HTML
         (Single Source of Truth)                                              (đọc JSON, render động)
```

### 8.3 Các file chính
- `lib/lms_fe_formulas.js`: Module công thức FE duy nhất (CC, BT, EL).
- `scripts/fetch_ks26_live.js`: Unified data fetcher → xuất JSON cache.
- `data/processed/ks26_live_metrics.json`: JSON chuẩn hóa (Single Source).
- `scratch/ks26_course_material_audit.json`: Config courseClassId (source of truth).

### 8.4 Quy tắc bắt buộc khi cập nhật dữ liệu
1. **LUÔN** chạy `node scripts/fetch_ks26_live.js` trước khi render dashboard.
2. **KHÔNG BAO GIỜ** sửa tay giá trị trong HTML.
3. Dashboard đọc `ks26_live_metrics.json` → render động 3 views.
4. Kiểm tra chéo: `scratch/compare_report_vs_live.py` parse HTML so với JSON.

---

## 9. Cấu Trúc Đào Tạo Đa Môn Đồng Thời Khóa KS26
- **Khối CNTT**: IT108-K26 (Nhập môn CNTT), SKL01 (Làm việc nhóm), JPN105-K26 (Tiếng Nhật — chỉ HN-KS26-CNTT1).
- **Khối QTKD**: SSK103 (Tư duy phân tích), SSK102 (Tin học ứng dụng).
- **Chung**: ENG105-K26 (Basic Speaking — 8 lớp).
- **Hoàn thành**: SSK101 (Kỹ năng Học tập chủ động — đã kết thúc).

---

## 10. LMS MCP API Configuration
- **Endpoint**: `https://lmsapi.rikkeiedu.com/v1/mcp/analytics`
- **Giao thức**: JSON-RPC 2.0 over HTTP POST. Bearer Token.
- **Các tools đang dùng**: `lms_find_classes`, `lms_list_course_classes`, `lms_course_class_statistics`, `lms_attendance_by_class`, `lms_homework_completion_by_class`, `lms_academic_warnings`.
- **API response fields**:
  - `absence`: `{ absentSessions, attendedSessions, plannedSessions, rate }` — KHÔNG có KP/CP/Muộn riêng.
  - `homework`: `{ done, total, rate }` — `total` = cả môn, `rate = done/total × 100`.
  - `elearning`: `{ rate }` — % hoàn thành đúng hạn.

---

