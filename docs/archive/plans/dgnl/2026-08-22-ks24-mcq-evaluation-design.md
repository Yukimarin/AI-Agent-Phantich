# THIẾT KẾ: BÁO CÁO ĐÁNH GIÁ CHẤT LƯỢNG ĐỀ THI ĐGNL & ĐỘ PHÙ HỢP TRIỂN KHAI (KHÓA KS24) - V2

**Mục tiêu:** Hiệu chỉnh báo cáo đánh giá đề thi tự luận và chỉ số độ phù hợp dựa trên so sánh học thuật chính xác giữa đề thi gốc và nội dung ôn tập (loại bỏ sự nhầm lẫn từ bài làm của sinh viên). Gộp toàn bộ vào một phần duy nhất trên Tab 3 và tính toán độ phù hợp tổng thể để triển khai ĐGNL.

---

## 1. PHÂN TÍCH ĐỘ PHÙ HỢP THỰC TẾ GIỮA ĐỀ THI GỐC VS. NỘI DUNG ÔN TẬP

Sau khi rà soát kỹ lưỡng cấu trúc đề thi tự luận gốc (bộ tiêu chí chấm điểm và mã đề 001 - 011) đối chiếu với nội dung chương trình ôn tập hè (PHẦN B), chúng tôi xác nhận **đề thi tự luận có độ phù hợp rất cao (~90%)** với nội dung học viên đã được ôn tập, cụ thể:

### A. Giao dịch & Kiểm soát đồng thời
*   **Yêu cầu trong đề thi tự luận:** Phát hiện một phương thức ghi dữ liệu thiếu `@Transactional` và có nguy cơ xảy ra tranh chấp dữ liệu (race condition); đề xuất thêm transaction và cơ chế đồng bộ/khóa cơ bản.
*   **Nội dung đã ôn tập hè:** Lý thuyết ACID trong transaction, các annotation `@Transactional`, cơ chế Propagation và Isolation levels (Sheet `PHẦN B`, Dòng 24-26).
*   **Đánh giá độ phù hợp: 90%**. Việc rà soát thiếu sót `@Transactional` là kiến thức cốt lõi đã được huấn luyện kỹ. Đề thi không yêu cầu code các kiến thức nâng cao ngoài phạm vi.

### B. Xác thực & Phân quyền mức dữ liệu
*   **Yêu cầu trong đề thi tự luận:** Phát hiện lỗ hổng logic nghiệp vụ: (1) tin tưởng tham số giá tiền do client truyền lên (`unitPrice` / `ticketPrice`) mà không truy vấn DB; (2) thiếu kiểm tra quyền sở hữu bản ghi (`patientId` không khớp với `prescriptionId` trong ngữ cảnh người dùng).
*   **Nội dung đã ôn tập hè:** RESTful API design, cấu trúc phân tầng Spring Boot (Controller - Service - Repository), xác thực JWT và phân quyền URL (Sheet `PHẦN B`, Dòng 20, 66, 68).
*   **Đánh giá độ phù hợp: 90%**. Đây là các lỗi logic nghiệp vụ căn bản của lập trình web. Đề thi chỉ yêu cầu rà soát code (code auditing) và sửa lỗi phân quyền/validations cơ bản trên lớp Service, hoàn toàn nằm trong tầm kiến thức của học viên.

### C. Tư duy thiết kế hệ thống
*   **Yêu cầu trong đề thi tự luận:** Câu hỏi 2 điểm yêu cầu học viên giải thích giải pháp ưu tiên hoặc phân tích ảnh hưởng của lỗi đặt vé trùng dưới tải cao (giờ cao điểm / suất chiếu hot).
*   **Nội dung đã ôn tập hè:** Lý thuyết về Scalability, Bottleneck hệ thống, các kỹ thuật mở rộng như Caching (Redis), Database Indexing (Sheet `PHẦN B`, Dòng 61-63).
*   **Đánh giá độ phù hợp: 90%**. Đây là câu hỏi tư duy logic hệ thống dựa trên nền tảng lý thuyết tối ưu hóa đã học.

---

## 2. CHỈ SỐ PHÙ HỢP TỔNG THỂ ĐỂ TRIỂN KHAI ĐGNL: 90%

Với việc cả hai phần thi đều bám sát chương trình ôn tập:
*   **Đề trắc nghiệm (Trọng số 40%):** Đạt **90%** độ phù hợp (Std Dev 16.88 thể hiện phân hóa tốt, dải điểm hình chuông chuẩn).
*   **Đề tự luận (Trọng số 60%):** Đạt **90%** độ phù hợp (rà soát lỗi logic và transaction cơ bản trên Spring Boot).
*   **Độ phù hợp tổng thể:** `90% * 0.4 + 90% * 0.6 = 90%` (Mức Phù hợp rất cao).

### Kết luận chuyên môn:
*   Bộ đề thi ĐGNL **hoàn toàn đảm bảo chất lượng, bám sát nội dung đào tạo** và đủ tiêu chuẩn làm thước đo năng lực học viên Rikkei Education.
*   *Lý giải điểm số thực tế:* Tỷ lệ trượt thực hành cao (53.8% concurrency, 54.0% security) không phải do đề thi ra ngoài chương trình ôn tập, mà do học viên còn yếu kỹ năng rà soát lỗi (code review/auditing) và chuyển đổi lý thuyết thành mã nguồn thực tế.
*   *Khuyến nghị sư phạm:* Giữ nguyên cấu trúc đề thi ĐGNL để bảo vệ chuẩn đầu ra doanh nghiệp. Điều chỉnh chương trình ôn tập hè theo hướng tăng cường các bài tập rà soát lỗi bảo mật (OWASP Top 10) và giả lập tranh chấp dữ liệu thực tế.
