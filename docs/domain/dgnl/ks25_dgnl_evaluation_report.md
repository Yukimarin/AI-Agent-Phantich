# BÁO CÁO ĐÁNH GIÁ NĂNG LỰC LẦN 1 - KHÓA KS25 CNTT
**Ban chuyên môn - Học viện Công nghệ**  
*Ngày báo cáo: 22/08/2026*  
*Đối tượng đánh giá: Học viên khóa KS25 CNTT (Hà Nội & TP. HCM)*

---

## 1. TỔNG QUAN KPIs & CẢNH BÁO ĐỎ

Kết quả đợt Đánh giá Năng lực (ĐGNL) Lần 1 của khóa **KS25 CNTT** ghi nhận các chỉ số học tập **báo động đỏ** ở phần thực hành lập trình và tỷ lệ vắng thi thực tế cao kỷ lục do sự cố hệ thống.

*   **Tổng quy mô đăng ký:** 429 học viên (không bao gồm các lớp QTKD).
*   **Số lượng tham gia thi thực tế:** 249 học viên (đạt 58.0%).
*   **Số lượng vắng thi/lỗi bài nộp:** 180 học viên (chiếm 42.0%) – *Tập trung chủ yếu tại cơ sở Hà Nội*.
*   **Điểm trung bình trắc nghiệm (MCQ):** **58.42 / 100** (Phân hóa tốt, lý thuyết nắm cơ bản).
*   **Điểm trung bình thực hành (Tự luận):** **20.24 / 100** (Rất kém, hầu hết bị điểm liệt hoặc bài trống).
*   **Điểm Final trung bình (Quy đổi thang 10):** **3.17 / 10** (Theo công thức PM: `TH * 0.7 + MCQ * 0.3`).
*   **Tỷ lệ trượt thực hành (Điểm thực hành < 50):** **85.9%** (Chỉ có 35/249 học viên tham gia thi đạt điểm thực hành &ge; 50).

> [!CAUTION]
> **CẢNH BÁO ĐỎ TỪ LEADER:**
> Tỷ lệ trượt thực hành thực tế lên tới **85.9%** thể hiện lỗ hổng cực kỳ nghiêm trọng trong năng lực code thực tế của sinh viên KS25 sau 2 học kỳ đầu. Nếu không có những điều chỉnh mang tính bước ngoặt trong Học kỳ III, chất lượng đầu ra của khóa này sẽ đối mặt với rủi ro rất lớn.

---

## 2. PHÂN TÍCH CHUYÊN SÂU TÌNH TRẠNG VẮNG THI (HN VS HCM)

Sự phân hóa về tỷ lệ vắng thi giữa hai miền thể hiện sự cố nghiêm trọng trong khâu vận hành hệ thống khảo thí tại Hà Nội:

| Cơ sở đào tạo | Tổng học viên | Tham gia thi | Số lượng vắng | Tỷ lệ vắng (%) | Ghi chú nguyên nhân |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Hà Nội (HN)** | 280 | 102 | 178 | **63.6%** | Sự cố crash hệ thống ca 7h-9h ngày 10/08; lỗi nộp bài, mất bài làm tự luận. |
| **TP. HCM (HCM)**| 149 | 147 | 2 | **1.3%** | Thi ca chiều, hệ thống ổn định, ghi nhận bài thi đầy đủ. |

### Đánh giá nguyên nhân từ Ban chuyên môn:
Tỷ lệ vắng thi lên tới **63.6% tại Hà Nội** không phải do sinh viên bỏ thi hàng loạt, mà do **sự cố kỹ thuật của nền tảng thi trực tuyến** trong ca thi đầu tiên (7h00 - 9h00 ngày 10/08/2026). 
1. Hệ thống không tải nổi lượng truy cập đồng thời lớn, dẫn đến việc nhiều học viên không thể đăng nhập hoặc bị tự động nộp bài khi đang làm.
2. Nhiều bài thi tự luận gửi lên server bị ghi nhận trống (0 byte) hoặc mất link Git bài làm, khiến giám thị phải đánh dấu "Vắng" hoặc "Lỗi bài nộp" trên hệ thống điểm danh tổng.
3. HCM thi vào các ca muộn hơn khi tải hệ thống đã giảm và được vá lỗi tạm thời, nên đạt tỷ lệ tham gia thi **98.7%**.

---

## 3. BẢN ĐỒ 5 CHIỀU NĂNG LỰC CỐT LÕI (RADAR CHART)

Ánh xạ điểm thi thực hành 11 tiêu chí lên 5 chiều năng lực cốt lõi hệ Python/FastAPI (điểm trung bình của 249 sinh viên tham gia thi):

```mermaid
radar
    title Bản đồ Năng lực Trung bình KS25 (%)
    labels ["Python Core & Thuật toán", "Pydantic Validation", "SQLAlchemy ORM", "FastAPI Endpoints", "Logic Nghiệp vụ & Xử lý lỗi"]
    data [28.8, 30.7, 45.8, 27.3, 13.9]
```

### Chi tiết điểm nghẽn kỹ thuật theo 11 tiêu chí:
1.  **Logic Nghiệp vụ & Xử lý lỗi (13.9% - Thấp nhất):**
    *   *Tiêu chí 4.2 (Bẫy lỗi logic trùng/404):* **Chỉ 10.4% học viên đạt**. Hầu hết không biết sử dụng `raise HTTPException` để xử lý các lỗi nghiệp vụ như trùng khóa chính, không tìm thấy khóa ngoại.
    *   *Tiêu chí 4.4 (Ràng buộc toàn vẹn khi DELETE):* **Chỉ 15.3% đạt**. Học viên không xử lý kiểm tra các bản ghi con trước khi xóa bản ghi cha.
2.  **FastAPI Endpoints & API Design (27.3%):**
    *   *Tiêu chí 4.1 (Folder Structure phân tầng):* **39.2% đạt** (Học viên biết tạo thư mục nhưng code bên trong rỗng).
    *   *Tiêu chí 4.3 (API GET kèm query relationship):* **Chỉ 15.3% đạt** (Không biết join bảng hoặc load relationship).
3.  **Python Core & Cấu trúc thuật toán (28.8%):**
    *   *Tiêu chí 1.2 (Linear Search lọc điều kiện):* **Chỉ 27.3% đạt**.
    *   *Tiêu chí 1.3 (Bubble Sort):* **31.8% đạt**. Học viên không tự code được thuật toán sắp xếp nếu không được tra tài liệu.
4.  **SQLAlchemy ORM (45.8% - Cao nhất):**
    *   *Tiêu chí 3.1 (database.py yield get_db):* **59.7% đạt** (Học viên chép được code kết nối khuôn mẫu).
    *   *Tiêu chí 3.2 (SQLAlchemy model quan hệ 1-N):* **Chỉ 31.8% đạt** (Khai báo sai cú pháp relationship).

---

## 4. PHÂN TÍCH NGUYÊN NHÂN GỐC RỄ (ROOT CAUSE)
Đứng ở góc độ quản lý đào tạo, điểm nghẽn thực hành hiện tại của KS25 không chỉ nằm ở học phần Python/FastAPI vừa qua, mà là hệ quả của **Hiệu ứng Domino mất gốc**:

1.  **Lịch sử học tập Kỳ I rất kém:** 
    *   Khóa KS25 ghi nhận **237 sinh viên trượt môn Javascript** và **161 sinh viên trượt lập trình C** ở Kỳ I.
    *   Tư duy lập trình cơ bản (biến, vòng lặp, mảng, điều kiện) chưa được định hình vững chắc.
2.  **Mất gốc chuyển tiếp sang Kỳ II:** 
    *   Khi bước vào học Python OOP và FastAPI ở Kỳ II, học viên lập tức bị ngợp trước các khái niệm phức tạp hơn như lập trình hướng đối tượng, bất đồng bộ (async/await), và ánh xạ cơ sở dữ liệu quan hệ (ORM).
    *   Do không làm chủ được thuật toán cơ bản, sinh viên không có khả năng tự suy luận logic khi viết các hàm xử lý API.

---

## 5. KIẾN NGHỊ ĐIỀU CHỈNH LỘ TRÌNH HỌC KỲ III

Học kỳ III của KS25 sẽ áp dụng khung chương trình mới định hướng AI (giống KS26): **Toán ứng dụng cho AI, Cấu trúc dữ liệu & Giải thuật (DSA), Học máy ứng dụng (Applied ML), Xây dựng hệ thống RAG & LLMs, Thực tập Lab**. 

Để cứu vãn tỷ lệ trượt thực hành 85.9%, Ban chuyên môn đề xuất 3 điều chỉnh cấp bách:

### 1. Tích hợp Bridge Module (Hệ đệm) vào 2 tuần đầu môn DSA:
*   **Thực trạng:** Học viên yếu Bubble Sort và Linear Search thì không thể học các thuật toán Tree, Graph hay Dynamic Programming của DSA.
*   **Giải pháp:** Dành 2 tuần đầu môn DSA để củng cố lại toàn bộ kỹ năng mảng (List/Dict) trong Python, viết lại các thuật toán sắp xếp/tìm kiếm cơ bản, kiểm tra bắt buộc trước khi chuyển sang cấu trúc dữ liệu nâng cao.

### 2. Cung cấp API Boilerplate trong môn RAG & LLMs:
*   **Thực trạng:** Học viên đang gãy ở khâu thiết lập API FastAPI và kết nối Database ORM (tiêu chí 4.2 và 2.2). Nếu bắt các em tự viết API từ đầu để gọi LLM/RAG, các em sẽ tiếp tục bị tắc ở phần FastAPI cơ bản.
*   **Giải pháp:** Giảng viên cung cấp sẵn bộ khung Project (Boilerplate) đã cấu hình sẵn Database, Router và các endpoint CRUD cơ bản. Học viên chỉ việc tập trung viết code gọi API OpenAI/Gemini và xử lý Vector Database.

### 3. Tập trung kỹ năng Data Preprocessing trong môn Applied Machine Learning:
*   **Thực trạng:** Tiêu chí 1.1 (Clean & Validate dữ liệu) chỉ đạt 27.3%.
*   **Giải pháp:** Các bài thực hành ML Lab nên được thiết kế tập trung nhiều vào khâu tiền xử lý dữ liệu (Data Cleaning, Handling Missing Values, Normalization) sử dụng Pandas và Numpy, giúp học viên rèn luyện tư duy xử lý dữ liệu thô.
