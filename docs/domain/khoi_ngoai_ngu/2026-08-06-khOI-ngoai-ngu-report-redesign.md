# Design Document: Redesign Báo cáo Khối Ngoại Ngữ (Tiếng Nhật & Tiếng Anh)

**Ngày khởi tạo**: 2026-08-06  
**Dự án**: `AI_Report_NN`  
**Mục tiêu**: Loại bỏ triệt để thông tin QTKD, phân tách báo cáo theo 2 bộ môn Tiếng Anh - Tiếng Nhật, tính định mức giờ làm theo loại nhân sự (Full-time vs Part-time/TTS), đánh giá khối lượng công việc (Đủ / Quá tải / Chưa đủ), nâng cấp Biểu đồ Trend giữa các tuần dạng SVG và tối ưu hiển thị Bảng Công việc Dự án bằng Phân trang & Sticky Header.

---

## 1. Loại bỏ thông tin QTKD
- Đổi toàn bộ tiêu đề, header metadata, taglines thành **Khối Ngoại Ngữ (Bộ môn Tiếng Anh & Tiếng Nhật)**.
- Loại bỏ triệt để các mã dự án QTKD (`SXHLDU`, `CAULAC`, `RASOAT`, `QTKDSO`, `QTKDNGHI`, `QTKDPM`, `QTKDCAC`).
- Cập nhật danh sách từ khóa nhận diện công việc KPI cho Ngoại ngữ: `tiếng nhật`, `tiếng anh`, `giảng dạy`, `khảo thí`, `đề thi`, `chấm bài`, `dự giờ`, `chăm sóc sinh viên`, `họp`, `giáo trình`, `slide`, `lesson`, `mindmap`, `video`, `quiz`, `jlpt`, `toeic`, `ielts`.

---

## 2. Phân tách Bộ môn Tiếng Anh & Tiếng Nhật
Tổ chức nhân sự và dự án theo 2 bộ môn chính:

### 🇯🇵 Bộ môn Tiếng Nhật (JPN Team)
- **Nhân sự**:
  - Giáp Thị Minh Hằng (Leader Tiếng Nhật) — Full-time (8.0h/ngày)
  - Lê Thị Đỏ (Giảng viên Tiếng Nhật) — Full-time (8.0h/ngày)
- **Dự án**:
  - `PTITXAY`: 🇯🇵 [PTIT-JPN] Xây dựng CTĐT Tiếng Nhật
  - `PTITQUAN`: 🇯🇵 [PTIT-JPN] Quản lý chất lượng bộ môn Tiếng Nhật
  - `PTITSAN3`: 🇯🇵 [PTIT-JPN] Sản xuất tài nguyên HK1 môn JPN101

### 🇬🇧 Bộ môn Tiếng Anh (ENG Team)
- **Nhân sự**:
  - Lò Thị Ngọc Anh (Leader Tiếng Anh) — Full-time (8.0h/ngày)
  - Hoàng Phương Thảo (Giảng viên Tiếng Anh) — Full-time (8.0h/ngày)
  - Bùi Thị Xuân Mai (Giảng viên/TTS Tiếng Anh) — Part-time / TTS (4.0h/ngày)
- **Dự án**:
  - `REXPENGL`: 🔵 [RE x PTIT] ENGLISH PROGRAM FOR K26
  - `REXPCHUO`: 🔵 [RE x PREP/JAXTINA] CHƯƠNG TRÌNH TIẾNG ANH K24 & K25
  - `REKHAO`: 🔵 [RE] ENGLISH EXAMINATION

### 📁 Công việc Chung / QLĐT
- **Dự án**: `QLDTXAY`: [QLĐT] Xây dựng bộ tiêu chuẩn QLĐT

---

## 3. Cấu hình Định mức Giờ làm & Phân loại Trạng thái Khối lượng

### A. Định mức giờ làm theo Loại Nhân sự (`work_type`)
- **Full-time (FT)**: Standard Target = 8.0h/ngày (40h/tuần)
- **Part-time / TTS**: Standard Target = 4.0h/ngày (20h/tuần) — Áp dụng cho **Bùi Thị Xuân Mai**

### B. Công thức Đánh giá Trạng thái Vận hành (Operational Workload Status)
1. **🟢 Đủ / Đạt chỉ tiêu**:
   - Giờ làm TB/ngày $\ge 100\%$ mục tiêu tương ứng (FT $\ge 8\text{h}$, TTS $\ge 4\text{h}$).
   - Đang phụ trách từ 1 - 5 tasks active.
2. **🔴 Quá tải (Overloaded)**:
   - *Quá tải giờ*: Giờ làm TB/ngày $> 125\%$ mục tiêu (FT $> 10\text{h}$, TTS $> 5\text{h}$).
   - *Quá tải task*: Đang gánh $> 5$ active tasks hoặc có $\ge 2$ tasks quá hạn deadline.
3. **🟡 Chưa đủ (Under-capacity)**:
   - Giờ làm TB/ngày $< 100\%$ mục tiêu (FT $< 8\text{h}$, TTS $< 4\text{h}$).
   - Hoặc tỷ lệ nộp báo cáo $< 80\%$.

---

## 4. Biểu đồ Trend Giờ làm việc giữa các tuần (Pure SVG Chart)
- Xây dựng Biểu đồ SVG thuần hỗ trợ so sánh giờ TB qua các tuần giữa **Bộ môn Tiếng Nhật**, **Bộ môn Tiếng Anh**, và **Toàn khối NN**.
- Tham chiếu mốc chuẩn 8h/ngày và 4h/ngày.
- **Xử lý thiếu dữ liệu**: Nếu tuần chưa diễn ra hoặc 0h nộp, hiển thị node nét đứt với nhãn `N/A (Chưa có dữ liệu)` tránh chia cho 0.

---

## 5. Tối ưu Bảng Công việc Chi tiết trong Quản lý Dự án
- Thêm bộ lọc: Tìm kiếm theo mã/tên/người gán, Lọc trạng thái, Lọc dự án/bộ môn.
- Phân trang (Pagination): Mặc định 10 rows / trang kèm nút chọn trang.
- Khung cuộn `max-height: 480px` cố định Sticky Header.

---

## 6. Verification & Verification Plan
- Chạy pipeline Python tạo lại `output/Bao_Cao_Tong_Hop_NN.html`.
- Kiểm tra tính đúng đắn dữ liệu:
  - Bùi Thị Xuân Mai đạt chỉ tiêu TTS (5.0h >= 4.0h -> ✅ Đủ).
  - Phân tách tab/filter Tiếng Nhật vs Tiếng Anh hoạt động chuẩn.
  - Biểu đồ SVG vẽ đúng.
  - Phân trang bảng task dự án phản hồi mượt mà.
