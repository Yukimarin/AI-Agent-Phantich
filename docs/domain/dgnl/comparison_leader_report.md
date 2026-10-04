# ĐỐI SOÁT & SO SÁNH BÁO CÁO CHUYÊN GIA VS. BÁO CÁO CỦA BAN TỔ CHỨC THI (LEADER)

**Mục tiêu:** Chỉ rõ điểm khác biệt về mặt số liệu, góc nhìn và giải pháp đối với khối KS24 giữa Báo cáo Năng lực của Chuyên gia đào tạo (Agent) và Báo cáo Tổ chức thi của Trưởng ban ĐGNL (Leader).

---

## I. SO SÁNH PHẠM VI & ĐỐI TƯỢNG BÁO CÁO

| Tiêu chí | Báo cáo của Chuyên gia đào tạo (Agent) | Báo cáo của Trưởng ban Tổ chức thi (Leader) |
| :--- | :--- | :--- |
| **Phạm vi dữ liệu** | Tập trung **100% vào khối KS24** (CNTT) đã thi và có kết quả chấm điểm thực tế. | Bao phủ **toàn bộ kỳ thi** (K24 & K25; cả 4 cơ sở/khối ngành: CNTT, QTKD, Ngoại ngữ, Kỹ năng mềm). |
| **Quy mô số liệu** | Phân tích chi tiết **167 sinh viên KS24** có bài thi được ghi nhận điểm trên hệ thống. | Thống kê tổng quan **629 sinh viên** đăng ký, **459 sinh viên** tham gia thi và **170 sinh viên** vắng thi. |
| **Bản chất số liệu** | Số liệu **đo lường năng lực và kỹ năng** (điểm số, tiêu chí đạt/không đạt của rubric chấm tự luận). | Số liệu **vận hành và log hệ thống** (số lượt vắng, số ca lỗi kỹ thuật, số ca vi phạm quy chế). |

---

## II. SO SÁNH CHI TIẾT SỐ LIỆU ĐỐI VỚI KHỐI CNTT (ĐẶC BIỆT LÀ KS24)

### 1. Số liệu về sự hiện diện và tham gia thi
*   **Báo cáo của Agent:** Ghi nhận **167 bài thi** có điểm số hoàn chỉnh của khối KS24.
*   **Báo cáo của Leader:** 
    *   Tổng số sinh viên CNTT tham gia thi và có điểm ghi nhận là **377 sinh viên** (bao gồm cả K24 và K25).
    *   Tổng số sinh viên CNTT vắng thi là **170 sinh viên** (chiếm 27%).
    *   Trong 170 sinh viên vắng thi này, khối **KS24 chiếm 33.6%** (khoảng **57 sinh viên**, trong đó K24 HN vắng 26 SV và K24 HCM vắng 31 SV).
*   **Nhận định đối soát:** 
    *   Quy mô thực tế khối KS24 CNTT đăng ký thi là khoảng **224 sinh viên** (167 SV có điểm + 57 SV vắng thi). 
    *   Tỷ lệ vắng thi riêng của khối KS24 CNTT rất cao, lên tới **25.4%** (57/224 SV). Đây là một chỉ số báo động về tính chủ động học tập của sinh viên trước khi ra trường.

### 2. Số liệu về sự cố hệ thống và độ tin cậy của điểm số
*   **Báo cáo của Agent:** Đi theo luồng dữ liệu "sạch" từ các bài thi đã được chấm điểm trên Excel, tính toán dựa trên kết quả 167 bài làm.
*   **Báo cáo của Leader:** Chỉ ra có tới **72 sinh viên CNTT gặp sự cố hệ thống/kỹ thuật** (chiếm 11.45% tổng số sinh viên đăng ký). 
*   **Nhận định đối soát:** 
    *   Các sự cố nghiêm trọng như mất bài, tự động nộp bài hoặc không hiện đề khiến điểm số của 72 sinh viên này không được ghi nhận trong danh sách 167 SV ban đầu. 
    *   Điều này đồng nghĩa với việc có một tỷ lệ sinh viên bị chấm "Không đạt" hoặc có điểm rất thấp có thể do lỗi hệ thống khảo thí chứ không hoàn toàn do năng lực yếu kém. Báo cáo của Leader giúp bảo vệ tính khách quan cho nhóm sinh viên gặp sự cố này.

---

## III. SỰ KHÁC BIỆT VỀ GÓC NHÌN & NHẬN ĐỊNH CHỐT

### 1. Góc nhìn chuyên môn Đào tạo (Agent) vs. Góc nhìn Vận hành (Leader)
*   **Agent (Nhìn vào Chất lượng Học tập):**
    *   *Nhận định:* Sinh viên trượt nhiều do **khoảng trống kiến thức** về Giao dịch và Concurrency (đồng thời). Giáo trình ôn tập hè lệch pha với đề thi thực tế.
    *   *Giải pháp:* Đề xuất cải tiến chương trình học kỳ IV/V, lồng ghép Distributed Locks, DevSecOps và Response Caching.
*   **Leader (Nhìn vào Quy trình Tổ chức):**
    *   *Nhận định:* Kỳ thi gặp nhiều vấn đề do **hệ thống phần mềm khảo thí chưa ổn định**, quy trình kiểm duyệt đề chưa kỹ (lỗi hiển thị, đề quá khó/lệch tiến độ học) và giám thị coi thi chưa sát (vẫn để sinh viên dùng AI làm bài).
    *   *Giải pháp:* Đề xuất Phòng Rika kiểm tra lại hệ thống; CVHT nhắc nhở sinh viên; tổ chức thi lại/thi bổ sung vào ngày **22/08/2026**.

### 2. Vấn đề vi phạm quy chế (Gian lận)
*   **Agent:** Chưa có dữ liệu này trong file điểm của giáo viên.
*   **Leader:** Ghi nhận **10 sinh viên vi phạm quy chế** (sử dụng AI, dùng máy thi có tài liệu cũ). Điều này chỉ ra rằng một số bài thi đạt điểm 9-10 trong dữ liệu của Agent có thể bị "nhiễu" do gian lận không được kiểm soát hết.

---

## IV. ĐỀ XUẤT TÍCH HỢP ĐỂ CHỐT PHƯƠNG ÁN CHO KS24

Để báo cáo gửi lên Ban Giám đốc Rikkei Education đạt chất lượng cao nhất, chúng ta cần tích hợp hai báo cáo này thành một thể thống nhất:

1.  **Hiệu chỉnh dữ liệu trượt thực tế:** Khi phân tích 49 sinh viên "Chưa sẵn sàng" (Mức 0) của KS24, cần đối chiếu xem có bao nhiêu sinh viên nằm trong danh sách **72 SV gặp sự cố hệ thống** của Leader để loại trừ lỗi kỹ thuật trước khi đánh giá học lực thực tế của các em.
2.  **Định hướng thi lại ngày 22/08/2026:** Đối với nhóm sinh viên vắng thi (57 SV KS24) và nhóm gặp sự cố kỹ thuật, cần áp dụng ngay đề cương ôn tập có bổ sung phần **Concurrency (Locking) và Security (IDOR/Path Traversal)** trước ngày thi lại để đảm bảo chất lượng bài làm.
3.  **Siết chặt quy chế thi bằng công cụ:** Đồng ý với giải pháp của Leader về việc sử dụng phần mềm quét AI/Simple Care để đảm bảo điểm số ĐGNL phản ánh 100% năng lực tự thân của sinh viên.
