# Thiết kế Kỹ thuật: Bảng KPI Master Khối Ngoại ngữ (Tiếng Nhật & Tiếng Anh)

## 1. Bối cảnh & Mục tiêu
- **Bối cảnh**: Khối CNTT và QTKD đã có danh mục KPI Master chuẩn hóa phân theo 5 cấp Rank (R1-R5) với thời gian tiêu chuẩn cho từng đầu việc. Khối Ngoại ngữ (Tiếng Nhật & Tiếng Anh) trước đây chưa có file Excel riêng, dẫn đến việc thiếu định mức khi khai báo trên Worklane.
- **Mục tiêu**:
  1. Xây dựng file Excel KPI Master chuẩn cho Khối Ngoại ngữ dựa trên định mức chuẩn CNTT/QTKD và 283+ tasks thực tế trên Worklane.
  2. Cung cấp 2 Sheet:
     - **Sheet 1: `KPI_MASTER_NGOAI_NGU`**: Ma trận danh mục đầu việc chuẩn phân theo 6 nhóm công việc, định mức thời gian chi tiết theo 5 cấp Rank (R1 ➔ R5) theo cả giờ và phút, có Mã Key để import Worklane.
     - **Sheet 2: `MAPPING_WORKLANE_TASKS`**: Bảng ánh xạ toàn bộ 283+ tasks thực tế của 3 nhân sự Ngoại ngữ (Giáp Thị Minh Hằng, Lò Thị Ngọc Anh, Lê Thị Đỏ) sang mã KPI Master chuẩn để phục vụ đối soát và kiểm chứng.

## 2. Danh mục 6 Nhóm Công việc Chuẩn
1. **Phát triển CTĐT & Giáo án (Curriculum R&D)**: Khung CTĐT, Timeline chi tiết, Lesson Plan, Quy trình đào tạo.
2. **Sản xuất Học liệu Số (Digital Content Production)**: Slide bài giảng, Video bài giảng, Quiz tương tác, Flashcards, Upload LMS.
3. **Giảng dạy & Triển khai Lớp (Teaching & Delivery)**: Chuẩn bị giảng dạy, Giảng dạy chính khóa / Talent, Demo & Orientation, Hỗ trợ học viên.
4. **Khảo thí & Đánh giá Năng lực (Assessment & Testing)**: Xây dựng ngân hàng đề thi, Thẩm định duyệt đề, Coi thi khảo sát, Chấm thi Nói - Viết, Báo cáo kết quả.
5. **Vận hành LMS AI & Quản lý Đối tác (Operations & Partners)**: Cấu hình môn học LMS AI, Order tính năng & nghiệm thu LMS AI, Bản quyền giáo trình, Giám sát đối tác liên kết (Prep, Jaxtina).
6. **Quản trị Chuyên môn & Nhân sự (Management & Meetings)**: Họp giao ban, Phỏng vấn & Demo tuyển dụng GV, Báo cáo tiến độ & quản trị nhân sự.

## 3. Quy chuẩn Định dạng Tệp Excel
- Đường dẫn file: `output/reports/KPI_Master_Khoi_Ngoai_Ngu.xlsx`.
- Bảng màu: Chuyên nghiệp (Deep Navy `#1F4E79`, Emerald `#2E75B6`, Soft Gray `#F2F4F7`, Border xám thanh lịch).
- Định dạng số: Giờ (1 chữ số thập phân), Phút (số nguyên), Căn chỉnh chuẩn công sở.
