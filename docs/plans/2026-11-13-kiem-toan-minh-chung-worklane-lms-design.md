# Thiết Kế Hệ Thống Kiểm Toán Minh Chứng Báo Cáo Công Việc: Worklane vs LMS Telemetry

> **Tài liệu thiết kế kiến trúc & quy chuẩn nghiệp vụ (Design Specification)**  
> **Ngày phê duyệt:** 13/11/2026 | **Phiên bản:** 1.0  
> **Chủ trì phê duyệt:** Trưởng ban Quản lý Đào tạo (Acting Head)  
> **Phạm vi áp dụng:** Toàn bộ Giảng viên cơ hữu, Giảng viên thỉnh giảng, Trợ giảng, Chuyên viên học vụ (Loại trừ Ban Lãnh đạo & Trưởng ban QLĐT)

---

## 1. Bối Cảnh & Vấn Đề Cần Giải Quyết

Trong công tác quản lý chất lượng đào tạo và kiểm toán hiệu suất nhân sự hàng ngày qua Worklane, hiện tồn tại 2 nhóm sai lệch nghiêm trọng giữa **kê khai trên giấy** và **hành vi thực tế trên hệ thống**:
1. **Khai khống đầu việc (Ghost Tasks):** Nhân sự khai báo hoàn thành 100% các task chăm sóc sinh viên, trao đổi phụ huynh (0.5h – 1.0h/ngày) nhưng không có bất kỳ dữ liệu nhật ký (log) nào được lưu lại trên hệ thống LMS/CRM.
2. **Phóng đại thời gian (Time Inflation):** Nhân sự khai báo chấm bài tập về nhà (BTVN) từ 1.0h – 2.0h/lớp, nhưng thực tế hệ thống LMS AI đã tự động chấm (Auto-grading) và nhân sự chỉ bấm duyệt trạng thái hàng loạt trong thời gian từ 5 – 7 phút (tương đương 10 – 15 giây/bài).

**Mục tiêu hệ thống:** Tự động đối soát dữ liệu Worklane với dữ liệu vết hệ thống (System Telemetry & Activity Logs) của LMS AI, tính toán lại **Giờ công Hiệu dụng (Effective Hours)**, và xuất **Phiếu Minh chứng Vi phạm** chi tiết làm căn cứ xử lý kỷ luật và KPI.

---

## 2. Quy Tắc Nghiệp Vụ & Phân Loại Vi Phạm

### 2.1. Phân loại 2 nhóm vi phạm
* **Vi phạm Loại 1 — Khai khống đầu việc (Ghost Task / Zero Evidence):**
  - Khai báo hoàn thành các tác vụ chăm sóc SV, họp 1-1 nhưng hệ thống không ghi nhận bản ghi log nào trong ngày.
  - *Mức độ:* **Báo động Đỏ (Nghiêm trọng)**.
  - *Chế tài:* Ghi nhận **0.0h hợp lệ**, thu hồi toàn bộ số giờ khai khống, trừ điểm KPI Tuân thủ.
* **Vi phạm Loại 2 — Phóng đại thời gian (Time Inflation / Bulk Approval):**
  - Khai báo chấm bài thời gian dài (1.0h – 2.0h) nhưng thời gian thực hiện thao tác trên LMS $\le 15$ phút và không có nhận xét viết tay.
  - *Mức độ:* **Báo động Vàng**.
  - *Chế tài:* Cắt giảm về giờ định mức duyệt AI (**0.25h / lớp**), phần dôi dư chuyển thành giờ không hợp lệ.

### 2.2. Khung định mức chuẩn hóa bổ sung KPI Master

| Nghiệp vụ | Hình thức thực hiện | Bằng chứng hệ thống bắt buộc (System Evidence) | Định mức giờ công công nhận |
|---|---|---|:---:|
| **Chấm BTVN (Duyệt AI)** | Bấm duyệt kết quả AI chấm sẵn trên portal | Timestamp bài đầu $\rightarrow$ bài cuối $\le 15$ phút; không có feedback viết tay | **0.25h / lớp** (tối đa 15–20 phút) |
| **Chấm BTVN (Chấm tay chi tiết)** | Đọc code/bài luận, chấm điểm và viết nhận xét | Timestamp trải đều $\ge 2$ phút/bài; **có text nhận xét $\ge 30$ ký tự** trên từng bài nộp | **1.5h – 2.0h / lớp** (tùy sĩ số) |
| **Chăm sóc sinh viên** | Nhắn tin/gọi điện hỗ trợ sinh viên nghỉ học, nợ bài | Bắt buộc có **Log ghi chú chăm sóc** trên hệ thống (kèm MSSV, ngày giờ, nội dung tóm tắt) | **10–15 phút / 1 SV** (Khai 0.5h phải có tối thiểu 2–3 SV; khai 1.0h phải có 4–5 SV) |

### 2.3. Quy tắc Ngoại lệ Cấp Quản lý (Management Exemption Gate)
* **Loại trừ 100%:** Trưởng ban Quản lý Đào tạo (tài khoản `bachnx@rikkeiacademy.com` và danh sách Ban Lãnh đạo Viện).
* Các đầu việc quản lý điều hành, xử lý đối tác, phát sinh, họp chiến lược không áp dụng định mức tác vụ kỹ thuật của GV/TG.

---

## 3. Kiến Trúc Luồng Dữ Liệu 2 Giai Đoạn

```
┌────────────────────────────────────────────────────────────────────────┐
│                        WORKLANE DAILY REPORTS                          │
│               (Lấy tự động qua Worklane MCP hàng ngày)                  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
         ┌─────────────────────────────────────────────────────┐
         │ 1. BỘ LỌC ĐẦU VÀO & NGOẠI LỆ (EXEMPTION GATE)       │
         │ - Loại trừ: Trưởng ban QLĐT (Nguyễn Xuân Bách)      │
         │ - Đối tượng quét: Giảng viên, Trợ giảng, Chuyên viên│
         └──────────────────────────┬──────────────────────────┘
                                    │
                  ┌─────────────────┴─────────────────┐
                  ▼                                   ▼
┌───────────────────────────────────┐ ┌───────────────────────────────────┐
│ GIAI ĐOẠN 1: HEURISTIC AUDIT      │ │ GIAI ĐOẠN 2: TELEMETRY AUDIT      │
│ (Áp dụng ngay lập tức)            │ │ (Tích hợp log chi tiết LMS AI)    │
├───────────────────────────────────┤ ├───────────────────────────────────┤
│ • Bóc tách Task Chấm bài & Chăm   │ │ • Lấy log bài nộp: T_start & T_end│
│   sóc SV qua Regex/NLP.           │   để tính ΔT thực tế                │
│ • Áp trần định mức cứng:          │ • Kiểm tra độ dài nhận xét:         │
│   - Chấm BTVN: Trần max 0.5h/lớp  │   Nếu không có text nhận xét        │
│     nếu không ghi rõ chấm tay.    │   -> Khóa phân loại "Duyệt AI".     │
│   - Chăm sóc SV: Bắt buộc kèm mã  │ • Quét log bảng chăm sóc SV:        │
│     MSSV; thiếu mã -> Cảnh báo    │   Số bản ghi thực = 0 -> Khẳng      │
│     thiếu bằng chứng.             │   định vi phạm 100%.                │
└─────────────────┬─────────────────┘ └─────────────────┬─────────────────┘
                  │                                     │
                  └─────────────────┬───────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│              3. BỘ MÁY XỬ LÝ GIỜ CÔNG & XUẤT MINH CHỨNG                │
│ • Giờ công thực tế (Actual Hours): Giữ nguyên số liệu nhân sự tự khai  │
│ • Giờ công hiệu dụng (Effective Hours): Tự động tính lại theo định mức  │
│ • Phiếu Minh chứng Vi phạm: Đính kèm từng mốc timestamp làm bằng chứng │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Cấu Trúc Báo Cáo & Minh Chứng Vi Phạm (Evidence Dossier)

### 4.1. Bảng Tổng Hợp Kiểm Toán Hiệu Dụng
Báo cáo định kỳ hàng tuần xuất bảng tổng hợp:
- **Giờ tự khai (Claimed Hours):** Số giờ nhân sự khai trên Worklane.
- **Giờ hiệu dụng công nhận (Effective Hours):** Số giờ được hệ thống phê duyệt sau kiểm toán.
- **Giờ không hợp lệ / Dôi dư (Deducted Hours):** Hiệu số bị trừ.
- **Tỷ lệ trung thực khai báo (Integrity Rate):** $\frac{\text{Effective Hours}}{\text{Claimed Hours}} \times 100\%$.

### 4.2. Cấu trúc Phiếu Minh Chứng Vi Phạm Chi Tiết
Mỗi trường hợp vi phạm được đính kèm bằng chứng kỹ thuật:
- **Vụ việc Chấm BTVN:**
  * Lớp, bài tập, sĩ số bài nộp.
  * Mốc thời gian bài nộp đầu tiên được duyệt ($T_{start}$).
  * Mốc thời gian bài nộp cuối cùng được duyệt ($T_{end}$).
  * Tổng thời lượng thực tế ($\Delta T = T_{end} - T_{start}$).
  * Tốc độ thao tác trung bình (giây/bài).
  * Số lượng bài có nhận xét viết tay ($\ge 30$ ký tự).
  * Chế tài: Cắt giảm giờ dôi dư, công nhận định mức 0.25h.
- **Vụ việc Chăm sóc SV:**
  * Truy vấn nhật ký chăm sóc trong ngày theo email nhân sự: Kết quả 0 bản ghi.
  * Task trên Worklane thiếu MSSV đối tượng.
  * Chế tài: Ghi nhận 0.0h, gắn cờ vi phạm mức độ Đỏ.

---

## 5. Quy Trình Vận Hành & Chế Tài (3 Bước)

1. **Bước 1 (Gửi Phiếu Đối Soát):** Thứ Sáu hàng tuần, hệ thống tự động xuất Bảng tổng hợp & Phiếu minh chứng vi phạm, gửi thông báo riêng đến nhân sự liên quan.
2. **Bước 2 (Giải trình 24h):** Nhân sự có quyền phản hồi hoặc cung cấp bằng chứng bổ sung (ảnh chụp tin nhắn Zalo, ghi chú offline) trong vòng 24h.
3. **Bước 3 (Chốt Giờ Công & Điểm Kỷ Luật):** Nếu không giải trình hoặc giải trình không thỏa đáng, số giờ không hợp lệ chính thức bị khấu trừ khỏi giờ công hiệu dụng gửi sang Kế toán, đồng thời trừ điểm tiêu chí "Tuân thủ kỷ luật" trong đánh giá KPI tháng.

---

## 6. Kế Hoạch Triển Khai Tiếp Theo
Chuyển tiếp sang bước lập kế hoạch thực thi chi tiết (`writing-plans`):
- **Task 1:** Bổ sung cấu hình định mức Duyệt AI và Chăm sóc SV vào `config/kpi_masters/`.
- **Task 2:** Xây dựng module kiểm toán Heuristic Giai đoạn 1 trong `pmo/modules/m2_worklane_audit.py` (loại trừ tài khoản Trưởng ban QLĐT).
- **Task 3:** Thiết kế schema và tích hợp telemetry logs LMS AI cho Giai đoạn 2.
- **Task 4:** Viết unit test & regression test khóa bộ quy tắc kiểm toán.
