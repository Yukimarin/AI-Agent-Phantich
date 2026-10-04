# Thiết kế điều chỉnh: Danh mục KPI Master cũ và Đầu việc Phát sinh theo Rank

Tài liệu này đặc tả thiết kế kỹ thuật cho công cụ thống kê công việc của Giảng viên & Trợ giảng nhằm mục đích:
1. Trích xuất danh sách đầu việc chuẩn kèm định mức cũ trong KPI Master theo từng mức Rank để cấu hình lên Worklane dropdown.
2. Thống kê, gom nhóm các công việc phát sinh thực tế chưa có định mức, phân chia chi tiết theo Khối và mức Rank để Giám đốc Đào tạo kiểm duyệt bổ sung.

---

## 1. Bối cảnh & Mục tiêu
* **Bối cảnh**: Hệ thống Worklane hiện nay chưa có danh mục công việc chuẩn. Giảng viên đang gõ tự do và không nhớ định mức. Mong muốn là khi giảng viên chọn đầu việc trên Worklane, hệ thống sẽ tự động điền giờ định mức dựa theo mức Rank của giảng viên đó.
* **Mục tiêu**:
  * Trích xuất danh mục đầu việc cũ cùng giờ định mức cũ cho từng mức Rank (1 đến 5).
  * Gom nhóm các công việc tự do thực tế chưa có định mức, phân chia chi tiết theo mức Rank và tính giờ trung bình thực tế khai báo để làm cơ sở đề xuất định mức mới.
  * Xuất dữ liệu tương tác dạng Tab mới trên Master Portal SPA và tệp Excel đề xuất.

---

## 2. Giải pháp Kỹ thuật & Luồng dữ liệu

Script Python `analyze_kpi_opportunities.py` sẽ được cập nhật để thực hiện:
1. **Trích xuất KPI Master cũ**: Đọc từ 2 file Excel nguồn của CNTT và QTKD. Trích xuất danh sách:
   * CNTT: Các đầu việc định nghĩa trong sheet `"Cấu trúc KPI công việc GV. TG"`.
   * QTKD: Các đầu việc định nghĩa trong sheet `"KPI_MASTER"`.
   * Chuyển đổi khóa (ví dụ: `Soạn slide-giảng viên-3` $\rightarrow$ Tên: `Soạn slide`, Rank: `3`, Vai trò: `Giảng viên`).
2. **Gom nhóm & Thống kê việc phát sinh mới (Chưa có định mức)**:
   * Lọc các task thực tế từ logs (daily reports từ 01/07/2026) có trạng thái "Chưa có định mức" (wildcard).
   * Gom nhóm bằng thuật toán chuẩn hóa không dấu và từ điển đồng nghĩa (Nghỉ phép, Làm học liệu video, Họp...).
   * Phân chia thống kê theo Khối và **Rank** của nhân sự đã khai báo (tính số giờ trung bình thực tế khai báo và tần suất cho từng Rank).

---

## 3. Chi tiết Cấu trúc 2 Bảng Thống kê trên Giao diện SPA

### Bảng 1: Danh mục đầu việc chuẩn (Trích xuất từ KPI Master cũ)
* **Khối**: CNTT, QTKD.
* **Đầu công việc**: Tên đầu công việc chuẩn (ví dụ: *"Soạn slide"*, *"Triển khai buổi thực hành"*).
* **Vai trò**: Giảng viên / Trợ giảng.
* **Rank**: 1, 2, 3, 4, 5.
* **Định mức cũ**: Số giờ định mức cũ (phút / giờ).

### Bảng 2: Thống kê đầu việc phát sinh mới (Cần bổ sung/hiệu chỉnh)
* **Khối**: CNTT, QTKD.
* **Đầu công việc (Nhóm đã gộp)**: Tên nhóm việc phát sinh thực tế (ví dụ: *"Sản xuất Video học liệu"*, *"Làm mindmap bài học"*).
* **Rank**: Mức Rank của nhân sự khai báo việc này.
* **Số giờ trung bình thực tế**: Giờ trung bình thực tế khai báo của riêng Rank đó cho nhóm việc này.
* **Tần suất**: Tổng số lần khai báo.
* **Nhân sự khai báo**: Danh sách tên các thầy/cô thuộc Rank đó đã khai báo việc này (để anh/chị tiện đối chứng).

---

## 4. Tệp Excel đề xuất đầu ra (`proposed_kpi_master.xlsx`)
Mỗi sheet (CNTT, QTKD) sẽ có 2 phần riêng biệt:
* **Phần A (Danh mục KPI Master cũ)**: Chứa danh sách các đầu việc chuẩn cũ và định mức tương ứng với từng Rank.
* **Phần B (Đầu việc mới phát sinh đề xuất)**: Chứa danh sách các nhóm công việc mới được đề xuất định mức cho từng Rank dựa trên trung bình thực tế.
