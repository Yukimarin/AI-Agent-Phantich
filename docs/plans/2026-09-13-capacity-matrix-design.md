# Thiết Kế Ma Trận Công Suất & Hiệu Suất Khối (Block Capacity & Efficiency Matrix)
### Tích Hợp Vào Báo Cáo Kiểm Toán Worklane (`worklane_staff_audit.html`)

> **Người lập kế hoạch**: Antigravity AI (Lead Architect)  
> **Kính gửi**: Thầy Nguyễn Duy Quang - Giám đốc Đào tạo  
> **Thời điểm**: 13/09/2026  
> **Nguồn dữ liệu kiểm toán**: `data/processed/capacity_matrix_data.json` & `data/processed/worklane_comparison_t8_t9.json`  

---

## 1. MỤC TIÊU & TÍNH CẤP THIẾT
- **Lấp đầy khoảng trống quản trị vĩ mô (Macro Capacity Utilization)**:
  - Hiện tại Dashboard tập trung vào góc nhìn vi phạm cá nhân (vượt định mức, khai bù giờ, rà soát Rank).
  - Thiếu thước đo công suất tổng thể theo tuần (40h/tuần/NS) và theo kỳ làm việc (7 ngày công = 56h/NS; Tháng 8 = 160h/NS).
- **Cân bằng tải công việc**: Giúp Giám đốc phát hiện ngay các khối đang vượt trần 40h/tuần (Khối QTKD 135.6%, CNTT Hà Nội 119.2%) và các khối còn dư dung lượng (CNTT HCM 73.6%, LMS AI 50.0%).
- **Kiểm toán hiệu suất thực chất**: So sánh số giờ khai báo với số giờ chuẩn theo KPI Master mới để tính toán % Hiệu suất thực chất (`Standard Master / Declared Hours`).

---

## 2. KIẾN TRÚC GIAO DIỆN & TƯƠNG TÁC (UI/UX)
- **Vị trí**: Đặt trực tiếp dưới cụm 4 Card KPI Tổng quan và trên Khối Biểu đồ Chart.js so sánh tiến độ.
- **Dạng thức**: **Collapsible Matrix Card** (Card thu gọn có thể bật/tắt mở rộng).
  - *Chế độ Thu gọn (Default)*:
    - Chiều cao ~50px, gọn gàng, không làm đẩy lệch cụm 6 Leader.
    - Hiển thị 2 chỉ số cốt lõi: Toàn Viện Đào tạo (**105.9%** công suất tuần) và Toàn Khối CNTT (**100.6%** công suất tuần).
    - Nút bấm Toggle: `<button onclick="toggleCapacityMatrix()">`.
  - *Chế độ Mở rộng (Expanded)*:
    - Trượt mở bảng Dark theme cao cấp (8 cột dữ liệu).
    - Có thanh mini progress bar thể hiện tỷ lệ lấp đầy giờ công.
    - 2 hàng Highlight đặc biệt: **Toàn Khối CNTT (22 NS)** và **Toàn Viện Đào Tạo (41 NS)**.
- **Tính Động Đa Kỳ**:
  - Tự động đồng bộ với `switchPeriod(periodKey)`:
    - Khi chọn `[Kỳ 01/09 - 11/09 (Mới)]`: Áp dụng định mức 7 ngày (56h/NS).
    - Khi chọn `[Tháng 08/2026 (Lịch sử)]`: Tự động chuyển sang định mức 20 ngày (160h/NS).

---

## 3. DỮ LIỆU ĐÃ ĐƯỢC KIỂM TOÁN TÍNH ĐÚNG ĐẮN

### Kỳ Mới (01/09 - 11/09/2026 - 7 ngày công):
1. **CNTT Hà Nội (13 NS)**: 40h/tuần = 520h | Khai báo = 619.8h (**119.2%**) | 7 ngày = 728h (85.1%) | Master = 245.3h (39.6%).
2. **QTKD (9 NS)**: 40h/tuần = 360h | Khai báo = 488.2h (**135.6%**) | 7 ngày = 504h (96.9%) | Master = 326.2h (66.8%).
3. **Ngoại Ngữ & KNM (4 NS)**: 40h/tuần = 160h | Khai báo = 142.0h (**88.8%**) | 7 ngày = 224h (63.4%) | Master = 122.3h (86.1%).
4. **QLCLĐT (4 NS)**: 40h/tuần = 160h | Khai báo = 181.0h (**113.1%**) | 7 ngày = 224h (80.8%) | Master = 120.5h (66.6%).
5. **CNTT HCM (9 NS)**: 40h/tuần = 360h | Khai báo = 265.1h (**73.6%**) | 7 ngày = 504h (52.6%) | Master = 208.6h (78.7%).
6. **LMS AI (2 NS)**: 40h/tuần = 80h | Khai báo = 40.0h (**50.0%**) | 7 ngày = 112h (35.7%) | Master = 12.9h (32.2%).
- **TỔNG CNTT (22 NS)**: 40h/tuần = 880h | Khai báo = 884.9h (**100.6%**) | 7 ngày = 1,232h (71.8%) | Master = 453.9h (51.3%).
- **TOÀN VIỆN (41 NS)**: 40h/tuần = 1,640h | Khai báo = 1,736.1h (**105.9%**) | 7 ngày = 2,296h (75.6%) | Master = 1,035.8h (59.7%).
