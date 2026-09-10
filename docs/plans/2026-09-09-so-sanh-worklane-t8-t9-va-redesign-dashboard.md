# Tài Liệu Thiết Kế: Cụm Biểu Đồ So Sánh Hiệu Suất T8 vs T9 & Tái Cấu Trúc Giao Diện Chống Tràn Dòng

> **Ngày thiết kế:** 09/09/2026  
> **Dự án:** Kiểm toán Hiệu suất Worklane & Đánh giá KPI GV/TG  
> **Người phê duyệt:** Người dùng / Giám đốc Đào tạo  
> **Mục tiêu:** 
> 1. Tích hợp cụm biểu đồ so sánh đa chiều giữa Tháng 08/2026 (20 ngày) và Kỳ 01/09 - 08/09/2026 (4 ngày) theo chuẩn hóa trung bình ngày & tỷ lệ vênh %.
> 2. Khắc phục triệt để lỗi tràn dòng, cắt chữ tên thầy cô trên các thẻ Leader Cards, Tags và Table.
> 3. Cập nhật lại toàn diện Báo cáo chuyên đề Markdown và Dashboard tương tác.

---

## 1. Cụm Biểu Đồ So Sánh Tiến Độ (Tháng 8 vs Tháng 9)

### 1.1. Thách thức dữ liệu & Giải pháp chuẩn hóa:
- **Tháng 8/2026**: 20 ngày làm việc ($N_1 = 20$).
- **Tháng 9/2026 (01/09 - 08/09)**: 4 ngày làm việc ($N_2 = 4$).
- **Công thức chuẩn hóa**:
  $$\text{Tỷ lệ vênh giờ (\%)} = \frac{\text{Tổng giờ khai báo} - \text{Tổng giờ chuẩn}}{\text{Tổng giờ chuẩn}} \times 100\%$$
  $$\text{Giờ dôi dư TB (h/ngày/NS)} = \frac{\text{Tổng giờ dôi dư}}{\text{Số ngày làm việc} \times \text{Số nhân sự}}$$

### 1.2. Kiến trúc 2 Biểu Đồ So Sánh (Chart.js SaaS Style):
1. **Biểu đồ Cột Kép 1: So sánh Tỷ Lệ Vênh Giờ (%) Theo 6 Khối**:
   - Khối Ngoại ngữ: T8 (+63.5%) ➔ T9 (+33.1%) — **Giảm mạnh 30.4%** (Cải thiện xuất sắc nhất).
   - Khối CNTT HCM: T8 (+49.4%) ➔ T9 (+37.4%) — **Giảm 12.0%** (Duy trì kỷ luật cao).
   - Khối QTKD: T8 (+48.6%) ➔ T9 (+59.5%) — Tăng nhẹ do các task nghiên cứu MAN107.
   - Khối QLCLĐT: T8 (+53.2%) ➔ T9 (+56.6%) — Ổn định.
   - Khối CNTT Hà Nội: T8 (+115.8%) ➔ T9 (+184.6%) — Tăng cao do dôi dư tự làm học liệu.
   - Nhóm LMS AI: T8 (+29.8%) ➔ T9 (+363.8%) — Tăng do chưa có barem R&D riêng.
2. **Biểu đồ Cột Kép 2: Giờ Dôi Dư Trung Bình / Ngày / Nhân Sự (h/ngày/NS)**:
   - Trực quan hóa công bằng lượng giờ khai dôi dư trên mỗi ngày công thực tế của từng khối.

---

## 2. Thiết Kế Header Thẻ Leader & Tags Chống Tràn Dòng

### 2.1. Cấu trúc Header thẻ Leader (Vertical Stacking & Adaptive Flexbox):
- Avatar nằm bên trái (44x44px).
- Cụm tên và thông tin nằm bên phải nhưng tách làm 2 dòng:
  - Dòng 1: Họ tên trọn vẹn (`text-sm font-bold text-white tracking-tight leading-snug`).
  - Dòng 2: Badge Rank (`Rank 5`) và Badge làm gương (`🟢 Làm gương xuất sắc (4/4 ngày)`) nằm hàng dưới, co giãn tự nhiên, không chiếm chiều ngang của tên.
- Thẻ Leader có `h-full flex flex-col justify-between` để 6 thẻ luôn bằng nhau tăm tắp.

### 2.2. Tags Nhân sự diện Rà soát & Cắt giờ ảo:
- Áp dụng `inline-flex items-center gap-1.5 max-w-full truncate px-2.5 py-1 rounded-lg text-xs`.
- Tooltip khi hover hiển thị đầy đủ tên, rank và số giờ dôi dư.

---

## 3. Quy Trình Cập Nhật Báo Cáo & Dashboard

1. **Engine**:
   - Xuất dữ liệu so sánh 6 Khối và 41 nhân sự vào file `data/processed/worklane_comparison_t8_t9.json`.
2. **Dashboard**:
   - Nhúng cụm biểu đồ Chart.js so sánh T8 vs T9 vào `worklane_staff_audit.html`.
   - Áp dụng CSS layout chống tràn dòng cho toàn bộ thẻ Leader, tags và bảng.
3. **Báo cáo Chuyên Đề**:
   - Cập nhật tài liệu phân tích chuyên sâu tại `docs/reports/2026-09-09-kiem-toan-worklane-01-08-thang-9-theo-kpi-master-moi.md`.
