# Tài liệu Thiết kế: Agent 2 — Action-Oriented Report Redesign

**Ngày:** 2026-08-13
**Phiên bản:** 2.0
**Trạng thái:** Đã được người dùng duyệt

---

## 1. Triết lý thiết kế (Core Design Principle)

Mỗi Tab phải trả lời một câu hỏi trung tâm rõ ràng, hướng đến một đối tượng đọc cụ thể và kết thúc bằng một hành động rõ ràng (Clear Call-to-Action).

| Tab | Câu hỏi trung tâm | Đối tượng chính |
|---|---|---|
| Tab 1 | *"Tuần này hệ thống đào tạo đang ổn không? Ai phải làm gì ngay?"* | PMO / Giám đốc |
| Tab 2 | *"Lớp nào đang nguy hiểm nhất? GV/TG phải ưu tiên lớp nào?"* | GV / Trợ giảng |
| Tab 3 | *"Nhóm sinh viên nào cần kiểu can thiệp gì? Ai chịu trách nhiệm?"* | GVCN / Cố vấn HT |

---

## 2. Thiết kế Tab 1 — Tổng quan Điều hành (PMO)

### Giữ nguyên
- Hàng 3 thẻ KPI (Sai số đánh giá MAE | Học viên Đỏ | Học viên Vàng)
- Biểu đồ tỉ lệ đỗ Chart.js

### Thay đổi chính: Kế hoạch Can thiệp Tuần này
Thay thế bảng 2 cột Hạn chế/Giải pháp hiện tại bằng **3 thẻ phân theo đối tượng thực thi**:

**Thẻ 1 — 🔴 Việc của Giảng viên / Trợ giảng (Cần làm trong 24–48h)**
- Viền trái màu đỏ, nền đỏ nhẹ
- Liệt kê hành động cụ thể gắn tên lớp: mở phụ đạo, siết điểm danh, hiệu chỉnh lỗi tác nghiệp trên QLĐT

**Thẻ 2 — 🟡 Việc của Cố vấn / GVCN (Cần làm trong tuần này)**
- Viền trái màu vàng, nền vàng nhẹ
- Liệt kê: liên hệ gia đình sinh viên vắng nhiều, nhắc nhở kỷ luật giờ giấc toàn khối

**Thẻ 3 — 🔵 Việc của PMO Điều phối (Giám sát & Phân bổ)**
- Viền trái màu xanh dương, nền xanh nhẹ
- Liệt kê: điều phối nguồn lực GV dạy bù, theo dõi KPI lỗi tác nghiệp

Mỗi mục trong thẻ là 1 hành động cụ thể gắn tên lớp/nhóm người.

---

## 3. Thiết kế Tab 2 — Phân tích Lớp học (GV/TG)

### Thay đổi 1: Thêm cột "Mức ưu tiên can thiệp"
| Mức | Điều kiện | Hiển thị |
|---|---|---|
| 🔴 Khẩn | Tỉ lệ đỗ < 50% HOẶC vi phạm > 20% | Badge đỏ |
| 🟡 Cần theo dõi | Tỉ lệ đỗ 50–70% HOẶC vi phạm 10–20% | Badge vàng |
| 🟢 Ổn định | Còn lại | Badge xanh |

Bảng mặc định sắp xếp theo mức ưu tiên (Khẩn lên đầu).

### Thay đổi 2: Nội dung Slide-over Drawer
Khi click `🔍 Chi tiết`, Drawer hiện 3 phần:
1. **Tình trạng lớp:** Tỉ lệ đỗ dự kiến, sĩ số, vi phạm lớp, cảnh báo tác nghiệp GV (nếu có).
2. **Hành động GV cần làm ngay:** Danh sách hành động cụ thể sinh tự động theo tình trạng của lớp đó.
3. **Học viên nguy cơ của lớp:** Thẻ mini như hiện tại (giữ nguyên).

---

## 4. Thiết kế Tab 3 — Can thiệp Sinh viên (GVCN/GV)

### Cấu trúc 4 Nhóm Vấn đề (Accordion)

Header mỗi nhóm: `[Icon + Tên nhóm] — [N] học viên — [Giải pháp tóm tắt 1 dòng]`

**Nhóm 1 🔴 — Nguy cơ Cấm thi (Chuyên cần / Elearning)**
- Tiêu chí: Vắng > ngưỡng cấm thi HOẶC Elearning vi phạm >= 2 bài
- Ngữ cảnh hiển thị: *"Học viên này có thể không được vào phòng thi nếu không khắc phục ngay."*
- Giải pháp: Yêu cầu học viên nộp đơn xin phép bổ sung + Cố vấn liên hệ gia đình trong 24h

**Nhóm 2 🟡 — Học lực yếu (Điểm dự kiến thấp)**
- Tiêu chí: Xác suất đỗ < 40%, không thuộc nhóm 1
- Ngữ cảnh: *"Học viên này có thể rớt môn dù không bị cấm thi."*
- Giải pháp: GV sắp xếp gặp trực tiếp, giao bài luyện tập cơ bản trước buổi học tiếp theo

**Nhóm 3 🟠 — Bất thường Kỷ luật (Copy / Học vẹt)**
- Tiêu chí: Flag `copy_suspect` hoặc `passive_learner`
- Ngữ cảnh: *"Học viên này có hành vi đáng lo ngại cần xác minh thực tế."*
- Giải pháp: GV kiểm tra trực tiếp trong buổi học gần nhất (yêu cầu giải thích code/bài tập)

**Nhóm 4 🟣 — Học giỏi nhưng Kỷ luật kém (Discipline Paradox)**
- Tiêu chí: Flag `discipline_paradox`
- Ngữ cảnh: *"Học viên này có năng lực tốt nhưng đang tự phá kỷ luật của mình."*
- Giải pháp: GVCN gặp gỡ trao đổi về cam kết chuyên cần

### Nút Xuất CSV
Giữ nguyên nhưng xuất kèm thêm 2 cột: **"Nhóm can thiệp"** và **"Giải pháp đề xuất"**.

---

## 5. File cần sửa đổi
- `agents/core/agent_2_academic_pred/generate_report.py` — toàn bộ template HTML/CSS/JS
