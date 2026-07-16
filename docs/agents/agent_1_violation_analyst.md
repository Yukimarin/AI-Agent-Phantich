# Sub Agent 1: ViolationAnalyst (Compliance Auditor) - Tài liệu tổng hợp hoạt động

Báo cáo này tổng hợp vai trò, cấu trúc dữ liệu, thuật toán tính điểm và các thay đổi phát triển đối với **Sub Agent 1 (ViolationAnalyst)** trong dự án đánh giá hiệu suất đào tạo.

---

## 1. Vai trò & Mục tiêu
ViolationAnalyst đóng vai trò là kiểm toán viên tuân thủ học đường. Nhiệm vụ chính là:
- Đọc và phân tích tệp Excel chỉ số học vụ của sinh viên.
- Tính toán tỷ lệ vi phạm kỷ luật học tập trung bình của từng lớp (bao gồm chuyên cần, nợ bài tập, vi phạm elearning).
- Tính toán điểm số kỷ luật học viên của lớp để đóng góp vào điểm Tuân thủ tổng hợp của giảng viên/trợ giảng phụ trách lớp đó.

---

## 2. Dữ liệu Đầu vào & Đầu ra

### Dữ liệu Đầu vào (Inputs)
- **Tệp Excel chỉ số**: [PTIT_Chiso.xlsx](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/data/PTIT_Chiso.xlsx). Tệp này chứa nhiều sheets ứng với các lớp và môn học khác nhau (ví dụ: `KS24-JavaAdvance`, `KS25_Javascript`, `KS25_QTKD_PRJ302`).

### Dữ liệu Đầu ra (Outputs)
- **Chỉ số vi phạm trung bình của lớp**: Được tính toán và chuyển giao trực tiếp cho Agent Lead (MasterEvaluator) và Agent 2 (AcademicPredictor) để phục vụ cho các thuật toán tương ứng.

---

## 3. Quy tắc & Công thức tính toán
- **Cấu trúc dòng tiêu đề**:
  - Dòng 3 của các sheet Excel chứa thông tin ngày học.
  - Dòng 4 chứa tiêu đề các cột chỉ số vi phạm cụ thể của ngày học đó: **CC** (Chuyên cần), **BT** (Bài tập), **EL** (Elearning).
- **Cách duyệt dữ liệu**:
  - Thuật toán duyệt qua các cột ngày học của lớp, với mỗi ngày học sẽ kiểm tra 3 cột liên tiếp (CC, BT, EL).
  - Tính trung bình cộng tỷ lệ vi phạm của từng học viên qua các cột này, sau đó tính trung bình cộng toàn lớp để ra chỉ số vi phạm trung bình của lớp học ($Violation_{avg}$).
- **Điểm Kỷ luật SV**:
  $$\text{Điểm Kỷ luật SV} = 100.0 - Violation_{avg}$$
  *Lưu ý:* Điểm số này luôn được giới hạn trong khoảng $[0.0, 100.0]$.

---

## 4. Lịch sử Thay đổi & Quyết định quan trọng
- **[2026-07-04] Đồng bộ hóa môn học mới và lớp mới**: Cập nhật logic chuyển đổi sheet học của khối QTKD K25 (chuyển đổi từ sheet môn `DTB202` sang môn thực tế `PRJ302`) và bổ sung lớp `HN-K25-CNTT8` vào danh sách quét chỉ số.
- **[2026-07-09] Sửa lỗi Nhận diện cột Rpoint chốt**: Khắc phục lỗi quét ngược cột từ cuối sheet làm thuật toán nhận diện nhầm các cột Elearning ở giữa sheet là Rpoint chốt (do các lớp KS25 không có cột Rpoint chốt ở cuối). Giải pháp: Enforce chỉ tìm kiếm cột Rpoint chốt ở phía sau cột ngày học cuối cùng.
- **[2026-07-09] Sửa lỗi parse Excel chốt vi phạm**: Sửa thuật toán parse để tính trung bình cộng tỷ lệ vi phạm lớp thực tế qua tất cả các cột buổi học tương ứng (offset 3 cột liên tiếp CC, BT, EL cho mỗi ngày học), sửa lỗi trước đó khiến vi phạm lớp luôn trả về 0.0% do nhảy lệch cột.
- **[2026-07-10] Phân tách điểm Elearning và Bài tập**: Đảo ngược tỷ lệ nợ bài tập của Excel thành tỷ lệ hoàn thành trước khi chuyển cho Agent 2 hiệu chuẩn. Đối với Elearning, giữ nguyên số bài vi phạm tuyệt đối từ DB để xét cấm thi theo Quy chế mới, tránh scale theo tỷ lệ phần trăm của Excel để không gây cấm thi ảo.

---

## 5. Mã nguồn liên quan
- **Script đọc và xử lý chính**: Tích hợp trong [generate_kpi_report.py](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/scratch/generate_kpi_report.py) và [excel_loader.py](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/scratch/excel_loader.py).
