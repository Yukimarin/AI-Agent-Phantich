# Tài Liệu Thiết Kế: Báo Cáo Kiểm Toán Hiệu Suất & Giờ Công Worklane (Tháng 08/2026)

- **Người yêu cầu:** Giám đốc Đào tạo - Thầy Nguyễn Duy Quang
- **Đơn vị thực hiện:** PMO & Ban Đào Tạo
- **Ngày lập:** 04/09/2026
- **Trạng thái:** Đã phê duyệt thiết kế (Chuyển sang triển khai)

---

## 1. Bối Cảnh & Mục Tiêu

### 1.1. Ba câu hỏi trực diện từ Giám đốc Đào tạo:
1. *Hiệu suất công việc của các nhân sự hiện tại thế nào?*
2. *Trên Worklane có phản ánh đúng hiệu suất không?*
3. *Còn trường hợp nào khai báo cho đủ giờ nữa không?*

### 1.2. Mục tiêu sản phẩm:
- Xuất bản một **Báo cáo Kiểm toán Chuyên đề Độc lập** dạng Markdown chuẩn chỉnh tại `docs/reports/2026-09-04-kiem-toan-hieu-suat-va-khai-bao-worklane.md`.
- Xuất bản một **Interactive Audit Dashboard (HTML)** tối ưu UI/UX 1 màn hình duy nhất (Single-Pane Master-Detail với Slide-over Drawer) tại `output/dashboards/audit/worklane_staff_audit.html` để Giám đốc và Leader có thể trực tiếp tra cứu, lọc và drill-down vào từng nhân sự trong tích tắc.

---

## 2. Quy Chuẩn Đánh Giá Dưới Góc Nhìn Quản Trị Của Leader

Khi một nhân sự (Ví dụ: Thầy/Cô Rank 3) thực hiện công việc có định mức chuẩn trong KPI Master là $T_{chuẩn} = 1.0h$ nhưng lại khai báo $T_{khai\_báo} = 2.0h$ (+100% thời gian), hệ thống phân loại thành 3 kịch bản xử lý:

1. **Kịch bản A: Năng lực chưa đạt chuẩn Rank (Làm chậm thật)**
   - *Dấu hiệu:* Có sản phẩm bàn giao, nhưng thời gian thực hiện kéo dài liên tục qua nhiều ngày.
   - *Khuyến nghị cho Leader:* Đưa vào danh sách cảnh báo năng lực chuyên môn, xem xét phỏng vấn đánh giá lại hoặc hạ Rank (từ R3 xuống R2).
2. **Kịch bản B: Khai báo bù giờ / Khai khống cho đủ 8 tiếng**
   - *Dấu hiệu:* Không có sản phẩm đầu ra kiểm chứng, các task chung chung ("đọc tài liệu", "họp trao đổi", "hỗ trợ ngoài giờ"), tổng giờ trong ngày luôn làm tròn 8.0h.
   - *Khuyến nghị cho Leader:* Cắt giảm số giờ công ảo dôi dư (chỉ công nhận theo định mức chuẩn), trừ điểm kỷ luật tác nghiệp của nhân sự.
3. **Kịch bản C: Định mức KPI Master chưa sát thực tế**
   - *Dấu hiệu:* Đa số nhân sự cùng làm task đó đều vượt giờ tương tự.
   - *Khuyến nghị cho Leader:* Đề xuất Giám đốc Đào tạo hiệu chỉnh lại barem chuẩn cho bộ môn.

---

## 3. Kiến Trúc Dữ Liệu & Pipeline Kiểm Toán

1. **Nguồn dữ liệu đầu vào:**
   - Dữ liệu nhật ký báo cáo ngày: `data/processed/daily_reports_raw_cache.json` & `daily_log_analysis.json` (39 nhân sự, toàn bộ tháng 08/2026).
   - Dữ liệu định mức KPI chuẩn theo Rank: Barem từ `Quản lý hiệu suất đào tạo.xlsx` (CNTT) và `_Task Management_ QL Khối QTKD.xlsx` (QTKD).
   - Dữ liệu danh mục nhân sự & Rank: `data/inputs/staff_roles_ranks.md`.
   - Dữ liệu dự án & ticket Worklane: `data/processed/project_issues_worklane.json`.
2. **Xử lý & Tổng hợp (Python Script `agents/audit/audit_worklane_performance.py`):**
   - Tính toán tổng giờ khai báo, tổng giờ định mức, độ vênh giờ theo từng nhân sự.
   - Trích xuất chi tiết từng task bị vượt chuẩn (ngày, tên việc, giờ khai, giờ chuẩn, chênh lệch).
   - Tự động gán nhãn kịch bản xử lý: *Cần rà soát Rank*, *Cảnh báo khai bù giờ*, *Đạt chuẩn*.
   - Xuất file kết quả tổng hợp `data/processed/worklane_audit_detailed.json`.

---

## 4. Thiết Kế UI/UX: Màn Hình Liền Mạch (Không Chuyển Tab Sidebar)

- **Thanh điều hướng & Bộ lọc trên cùng:**
  - Bộ lọc Khối: Tất cả / Khối CNTT / Khối QTKD / Khối Ngoại ngữ & KNM / Khối QLCLĐT.
  - Bộ lọc Phân loại: Tất cả / Cần rà soát Rank / Cảnh báo bù giờ / Chuẩn mực.
  - Ô tìm kiếm nhanh nhân sự theo tên.
- **4 Thẻ Chỉ số Cốt lõi (Summary Cards):**
  - Tỷ lệ tuân thủ báo cáo ngày (%).
  - Tổng số giờ dôi dư cần kiểm toán (Giờ).
  - Số nhân sự cần xem xét lại Rank (Người).
  - Số nhân sự cần cắt giảm giờ công ảo (Người).
- **Bảng Master (Danh sách 39 nhân sự):**
  - Cột: Họ tên, Khối, Cơ sở, Vị trí & Rank, Giờ khai báo, Giờ chuẩn KPI, Chênh lệch giờ, Tỷ lệ tuân thủ, Đề xuất xử lý, Thao tác [Soi chi tiết].
- **Slide-over Drawer (Ngăn trượt chi tiết bên phải):**
  - Mở tức thì khi click vào bất kỳ dòng nào trong bảng (không load lại trang, không nhảy tab).
  - Chi tiết từng ngày, từng task bị đội giờ của nhân sự đó kèm chênh lệch.
  - Khuyến nghị hành động cụ thể cho Leader (Kèm nút in phiếu làm việc 1-1).

---

## 5. Kế Hoạch Triển Khai & Kiểm Thử

1. **Bước 1:** Viết script phân tích chuyên sâu `agents/audit/audit_worklane_performance.py` để bóc tách 100% dữ liệu tháng 8 của 39 nhân sự và xuất `data/processed/worklane_audit_detailed.json`.
2. **Bước 2:** Biên soạn Báo cáo Kiểm toán Chuyên đề `docs/reports/2026-09-04-kiem-toan-hieu-suat-va-khai-bao-worklane.md` gửi Giám đốc Đào tạo.
3. **Bước 3:** Xây dựng Dashboard HTML tương tác `output/dashboards/audit/worklane_staff_audit.html` với cơ chế Slide-over Drawer 1 màn hình.
4. **Bước 4:** Kiểm thử trực quan (Visual QA) và test truy xuất thử một số nhân sự điển hình theo yêu cầu của User (Ví dụ: Thầy/Cô Rank 3 vượt giờ, các ca khai bù giờ).
