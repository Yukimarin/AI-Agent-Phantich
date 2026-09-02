# THIẾT KẾ BÁO CÁO ĐGNL LẦN 1 - KHÓA KS25 CNTT (FASTAPI & PYTHON)
**Ngày lập:** 2026-08-22
**Trạng thái:** Được phê duyệt bởi Leader

---

## 1. MỤC TIÊU & ĐỐI TƯỢNG BÁO CÁO
*   **Đối tượng:** Khóa KS25 Hệ Công nghệ Thông tin (học viên đã hoàn thành Học kỳ II, học Python và FastAPI).
*   **Mục tiêu báo cáo:**
    1.  Cung cấp cho Leader (Giám đốc Đào tạo) cái nhìn khách quan, khoa học về chất lượng đào tạo Kỳ II qua số liệu điểm thi ĐGNL Lần 1 (MCQ & Thực hành).
    2.  Định vị chính xác **5 chiều năng lực cốt lõi** thực tế của sinh viên hệ Python/FastAPI.
    3.  Phân tích nguyên nhân gốc rễ và đề xuất điều chỉnh chi tiết cho lộ trình Kỳ III (Toán AI, DSA, Machine Learning, RAG & LLM, Thực tập RK-Lab).

---

## 2. BẢN ĐỒ NĂNG LỰC 5 CHIỀU CỦA KS25 (RADAR CHART)
Radar Chart của học viên KS25 sẽ phản ánh đúng các kỹ năng trong chương trình học của các em, được bóc tách từ 11 tiêu chí chấm trong ca thi thực tế:
1.  **Python Core & Thuật toán (Algorithms & Core):** Khả năng clean/validate dữ liệu thô, cài đặt thuật toán Linear Search và Bubble Sort. *(Tiêu chí 1.1, 1.2, 1.3)*.
2.  **Pydantic Validation (Data Validation):** Sử dụng Pydantic Schema để kiểm soát dữ liệu đầu vào và response_model đầu ra. *(Tiêu chí 2.1, 2.2)*.
3.  **SQLAlchemy ORM (Database & Models):** Cấu hình kết nối database MySQL, viết dependency get_db() bằng yield, thiết lập quan hệ 1-N. *(Tiêu chí 3.1, 3.2)*.
4.  **FastAPI Endpoints (API Design):** Tổ chức thư mục dự án chuẩn 4 lớp (Routers, Services, Schemas, Models), viết các router API GET/POST. *(Tiêu chí 4.1, 4.3)*.
5.  **Logic Nghiệp vụ & Xử lý lỗi (Business Logic & Exception):** Bẫy lỗi trùng lặp dữ liệu (400), khóa ngoại không tồn tại (404), ràng buộc toàn vẹn khi xóa (4.4). *(Tiêu chí 4.2, 4.4)*.

---

## 3. THIẾT KẾ CẤU TRÚC DASHBOARD (outputs/KS25_DGNL_Report.html)
Báo cáo sẽ sử dụng giao diện Dark Mode (glassmorphism) tương tự KS24 nhưng được tinh chỉnh nội dung:

### TAB 1: Tổng quan kết quả (KPIs & Biểu đồ)
*   **KPI Cards:**
    *   Tổng số học viên dự thi (530 học viên, lọc theo mã lớp KS25/K25).
    *   Điểm trung bình Trắc nghiệm (61.38/100) & Thực hành (26.12/100).
    *   Tỷ lệ đạt chuẩn thực hành (18.1%) & Tỷ lệ chưa đạt (81.9% - Cảnh báo đỏ).
*   *Lưu ý:* Bỏ hoàn toàn phần "Tỷ lệ đáp ứng vị trí tuyển dụng" của KS24 (do KS25 mới học xong kỳ II).
*   **Radar Chart trung bình toàn khóa:** Hiển thị 5 chiều năng lực cốt lõi.

### TAB 2: Danh sách Học viên & Chi tiết Năng lực
*   **Bảng danh sách tinh giản cột:** Họ và tên, Lớp, Cơ sở, Điểm Trắc nghiệm, Điểm Thực hành, Điểm Final, Xếp loại Readiness.
*   **Interactive Row Click:** Click vào học viên sẽ hiển thị bảng nhỏ 5 chiều năng lực, nhận xét chi tiết của giảng viên (cột Nhận xét) và định hướng học tập bổ trợ.

### TAB 3: Đánh giá Đề thi & Kiến nghị Sư phạm
*   **Đánh giá Đề thi ĐGNL:** So sánh đề thi với 14 ngày ôn luyện hè trực tuyến trên Python Portal. Tính chỉ số phù hợp tổng thể (Weighted Suitability Index - 90%).
*   **Bản đồ Điểm nghẽn Năng lực Kỹ thuật:** Hiển thị biểu đồ tỷ lệ trượt chi tiết trên 11 tiêu chí thực hành để chỉ ra chính xác sinh viên bị "gãy" ở bước nào.
*   **Đề xuất điều chỉnh lộ trình Kỳ III (KS25):**
    *   *Môn Cấu trúc dữ liệu & Giải thuật:* Bổ sung Bridge Module 2 tuần đầu ôn tập giải thuật tìm kiếm/sắp xếp tuyến tính.
    *   *Môn RAG Systems & LLMs:* Cung cấp sẵn template cấu trúc API FastAPI và kết nối Database để học viên tập trung tích hợp LLM.
    *   *Môn Học máy ứng dụng:* Tập trung thực hành tiền xử lý dữ liệu Pandas.

---

## 4. PHƯƠNG ÁN KỸ THUẬT PHÂN TÍCH DỮ LIỆU
*   Tệp mã nguồn xử lý và sinh HTML độc lập: `src/generate_dashboard_ks25.py`.
*   Tệp ca thi đầu vào: `CNTT_HN_K25_7H_9H.xlsx`, `CNTT_HN_K25_9H10_11H10.xlsx`, `CNTT_HCM_9H30_11H30.xlsx`, `CNTT_K25_HCM_14H20_16H20.xlsx`.
*   **Thuật toán Parser:** Dùng Regex phân tách cột 13 (`Chi tiết tiêu chí`) để lọc trạng thái `ĐẠT` hay `KHÔNG ĐẠT` của 11 tiêu chí, sau đó tính tỷ lệ đạt cho từng tiêu chí và ánh xạ lên 5 chiều năng lực của mỗi học viên.
