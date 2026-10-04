# BLUEPRINT: QUY TRÌNH PHÂN TÍCH DỮ LIỆU & LẬP BÁO CÁO ĐGNL KHÓA KS25 (FASTAPI & PYTHON)
**Tài liệu chuẩn hóa dành cho Ban Đào tạo & Chuyên viên Phân tích (Curriculum Engineer)**
**Áp dụng:** Khóa KS25 Hệ Công nghệ Thông tin (FastAPI & Python Core)

---

## I. XÁC NHẬN CHỐT BÁO CÁO KHÓA KS24 (JAVA & REACT)

Toàn bộ kết quả phân tích và báo cáo của khóa KS24 đã được chốt và khóa cứng trạng thái hoàn thiện:
1.  **Dashboard HTML báo cáo chính thức:** [KS24_DGNL_Report.html](file:///c:/Users/DELL/Desktop/AI-Agent/AI-ĐGNL/outputs/KS24_DGNL_Report.html).
2.  **Tài liệu phân tích chuyên sâu lộ trình:** [roadmap_evaluation.md](file:///c:/Users/DELL/Desktop/AI-Agent/AI-ĐGNL/docs/reports/roadmap_evaluation.md).
3.  **Tài liệu đề xuất điều chỉnh:** [2026-08-20-KS24-curriculum-proposals.md](file:///c:/Users/DELL/Desktop/AI-Agent/AI-ĐGNL/docs/plans/2026-08-20-KS24-curriculum-proposals.md) và [2026-08-21-KS24-curriculum-proposal-design.md](file:///c:/Users/DELL/Desktop/AI-Agent/AI-ĐGNL/docs/plans/2026-08-21-KS24-curriculum-proposal-design.md).
*Lưu ý:* Nghiêm cấm mọi hành vi ghi đè hoặc làm thay đổi kết quả số liệu của khóa KS24 trong các tệp tin trên.

---

## II. BLUEPRINT QUY TRÌNH ÁP DỤNG CHO KHÓA KS25 CNTT (FASTAPI & PYTHON)

Dựa trên các bài học kinh nghiệm và quy chuẩn đã được Ban Đào tạo thông qua từ khóa KS24, dưới đây là quy trình 4 bước bắt buộc để xử lý dữ liệu và tạo báo cáo ĐGNL cho khóa KS25 CNTT.

---

### BƯỚC 1: XỬ LÝ & MAPPING DỮ LIỆU THÔ (DATA PROCESSING)

#### 1. Bộ dữ liệu đầu vào của KS25 CNTT
*   **Tệp điểm tổng:** `Danh sách thi ĐGNL.xlsx` (Sheet `Danh sách ĐGNL CNTT`).
    - Lọc học viên theo cột `Mã lớp hiện tại` có chứa từ khóa `KS25` hoặc `K25` (Danh sách lớp gồm: `HN-KS25-CNTT1` đến `CNTT8` và `HCM-KS25-CNTT5` đến `CNTT8`).
*   **Trang ôn luyện hè gốc:** [https://pythonsummer.netlify.app/](https://pythonsummer.netlify.app/) (Lộ trình 14 ngày ôn luyện FastAPI & Python Core).
*   **Tệp chấm điểm tự luận chi tiết:** Các tệp Excel chấm điểm ca thi thực tế của KS25.

#### 2. Công thức tính Điểm Final ĐGNL hệ Python (KS25)
Khác với hệ Java (KS24), đối với hệ Python (KS25), công thức tính điểm Final ĐGNL được chuẩn hóa đồng nhất cho cả HN và HCM theo quy định PM:
$$\text{Điểm Final ĐGNL} = \text{Thực hành (Đ1)} \times 0.7 + \text{Trắc nghiệm (Đ1)} \times 0.3$$
*Lưu ý:* Điểm trắc nghiệm và thực hành trong tệp Excel gốc là thang điểm 100. Khi hiển thị trên Dashboard, cần quy đổi về thang điểm 10 (chia cho 10) để thống nhất trực quan.

#### 3. Phân loại Mức độ Sẵn sàng (Readiness Levels)
Dựa trên điểm số Final (thang 10) và điểm tiêu chí kỹ năng thực hành (thang 100):
*   **Mức 3 (Làm chủ tốt - Advanced Mastery):** Điểm Final $\ge 8.0$ VÀ các tiêu chí kỹ năng cốt lõi (Đa luồng/Concurrency, Bảo mật API/Security) $\ge 75.0$.
*   **Mức 2 (Đạt chuẩn - Proficient):** Điểm Final $\ge 6.0$ VÀ các tiêu chí kỹ năng cốt lõi $\ge 50.0$.
*   **Mức 1 (Cần bổ trợ - Basic Pass):** Điểm Final $\ge 4.0$ VÀ các tiêu chí kỹ năng cốt lõi $\ge 40.0$.
*   **Mức 0 (Chưa đạt chuẩn - Below Standard):** Các trường hợp còn lại hoặc điểm yếu kém.

---

### BƯỚC 2: THỐNG KÊ & ĐÁNH GIÁ ĐỀ TRẮC NGHIỆM (MCQ EVALUATION)

Để đánh giá chất lượng đề trắc nghiệm Python/FastAPI của KS25, cần chạy thống kê điểm của toàn bộ học viên KS25 dự thi theo các chỉ số:

1.  **Điểm trung bình (Average):** Phản ánh mức độ tiếp thu lý thuyết chung.
2.  **Độ lệch chuẩn (Standard Deviation - Std Dev):** Đo lường tính phân hóa.
    - *Công thức Python thuần:*
      ```python
      avg = sum(scores) / len(scores)
      variance = sum((x - avg) ** 2 for x in scores) / len(scores)
      std_dev = variance ** 0.5
      ```
    - *Chuẩn đánh giá:* Std Dev $\ge 15.0$ (trên thang 100) thể hiện đề thi có **độ phân hóa tốt**, phân loại rõ nét học viên.
3.  **Phân bổ dải điểm (Thang 100):**
    - Xuất sắc (90 - 100): Nhóm học viên giỏi lý thuyết hệ thống.
    - Giỏi (80 - 89) & Khá (70 - 79): Nhóm nòng cốt lực lượng.
    - Trung bình (50 - 69): Nhóm đạt chuẩn, cần củng cố thực hành.
    - Yếu kém (< 50): Tỷ lệ trượt lý thuyết (nếu thấp chứng minh đề bám sát ôn tập).

---

### BƯỚC 3: ĐỐI SOÁT HỌC THUẬT & TÍNH CHỈ SỐ PHÙ HỢP TỔNG THỂ (%)

Đây là bước cực kỳ quan trọng, yêu cầu **chỉ so sánh nội dung thiết kế của đề thi thực tế với chương trình ôn luyện hè 14 ngày**, tuyệt đối không đưa số liệu điểm số hay bài làm của sinh viên vào phần đối soát này.

#### 1. Bản đồ đối chiếu học thuật KS25
*   **Nội dung ôn luyện (Dữ liệu từ pythonsummer.netlify.app):**
    - *Python Core (Bài 1-4):* List Comp, Dictionary, Set, Swap, logic nghiệp vụ, Try-Except, Linear Search & Bubble Sort.
    - *FastAPI Basics (Bài 5-7):* Uvicorn, RESTful API, Pydantic Schema validations, Path & Query parameters, In-Memory CRUD.
    - *SQLAlchemy ORM (Bài 8-12):* MySQL, ORM Models, Service layer, Depends() DI, Project Structure 4 lớp, quan hệ 1-N (ForeignKey).
    - *Final Exam (Bài 13-14):* Tích hợp CSDL & Transaction.
*   **Nội dung đề thi thực tế yêu cầu:** Đối chiếu với các đề thi trắc nghiệm (90 câu) và đề thực hành cụ thể của khóa KS25.
*   **Xác định Khoảng trống kiến thức (Omission):** Chỉ ra các chủ đề đề thi có yêu cầu nhưng chương trình ôn luyện 14 ngày không đề cập hoặc ngược lại.

#### 2. Công thức tính Chỉ số Độ phù hợp Tổng thể (Overall Suitability Index)
Phân bổ trọng số đánh giá chất lượng đề thi để triển khai ĐGNL:
*   Trọng số Đề Trắc nghiệm (MCQ): **40%**
*   Trọng số Đề Tự luận (Thực hành): **60%**
*   **Ví dụ:** Nếu MCQ bám sát 90% nội dung đã học, Tự luận bám sát 90% nghiệp vụ cơ bản đã học $\rightarrow$ Chỉ số phù hợp tổng thể đạt **90%** (Phù hợp rất cao để triển khai làm chuẩn đo lường).

---

### BƯỚC 4: QUY CHUẨN THIẾT KẾ BÁO CÁO GIAO DIỆN (UI/UX STANDARDS)

Để báo cáo đạt chuẩn thẩm mỹ cao, wow người xem, giao diện Dashboard HTML của KS25 bắt buộc tuân thủ:

1.  **Chủ đề giao diện (Visual Theme):** Sử dụng SLEEK DARK MODE kết hợp glassmorphism.
    - Màu nền: `#09090b` (Dark Base), Thẻ card: `#18181b`, Viền: `#27272a`.
    - Màu điểm nhấn chính (FastAPI/Python): Xanh dương kết hợp Vàng hoặc Xanh lá (RGB).
2.  **Biểu đồ mạng nhện (Radar Chart - Chart.js):**
    - Biểu đồ phải to, hiển thị rõ ràng chính giữa thẻ.
    - **Quy tắc sửa lỗi co kéo chữ:** Tăng kích thước font chữ của nhãn (Ticks/Labels) và căn chỉnh padding hợp lý để chữ nhãn không bao giờ bị đè lên biểu đồ hay bị kéo dài.
3.  **Khối hợp nhất Đánh giá đề thi ĐGNL (Tab 3):**
    - Đặt thanh tiến độ (Progress bar) hiển thị % phù hợp tổng thể ở đầu Tab 3.
    - Chia bố cục grid 2 cột cân đối: Cột trái thống kê điểm MCQ (Bảng dải điểm, Std Dev); Cột phải đối soát học thuật Tự luận (Concurrency, Security, System Design).
    - Đưa ra nhận định kết luận chuyên môn rõ ràng từ Ban chuyên môn.
4.  **Bảng danh sách tương tác (Tab 4):**
    - Thiết kế bảng danh sách học viên có chức năng tìm kiếm realtime theo tên, lớp học, và lọc theo mức độ sẵn sàng (Level 0 - 3).
    - Khi click vào từng dòng, sẽ mở rộng hiển thị chi tiết điểm số các tiêu chí và định hướng nghề nghiệp cụ thể của học viên đó.
