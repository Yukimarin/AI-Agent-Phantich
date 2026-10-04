# BÁO CÁO ĐỐI SOÁT & PHÂN TÍCH CHUYÊN SÂU KẾT QUẢ ĐGNL ĐỢT 1 (KHÓA KS24 & KS25)

**Người thực hiện:** Chuyên gia Đào tạo & Phân tích Dữ liệu  
**Dự án:** Phân tích Năng lực Sinh viên hệ PTIT - Rikkei Education  
**Đối tượng:** Khối Công nghệ thông tin (KS24 & KS25) và các phân môn liên quan  

---

## I. TỔNG QUAN HỆ THỐNG CÔNG THỨC ĐIỂM FINAL

Theo yêu cầu điều chỉnh nghiệp vụ, công thức tính điểm Final cho từng khối được thiết lập lại để phản ánh đúng thực tế tổ chức đào tạo và thi cử:

1. **Khóa HN-KS24 (Có làm dự án môn học trước đó):**  
   $$\text{Final} = \text{Sản phẩm} \times 30\% + \text{Vấn đáp} \times 20\% + (\text{Thực hành} \times 20\% + \text{Trắc nghiệm} \times 80\%) \times 50\%$$  
   *Lưu ý:* Đối soát công thức gốc trong tệp Excel cho thấy điểm `Sản phẩm` thực tế bị bỏ quên (gán trọng số 0%). Hệ thống đã thực hiện tính toán lại thủ công toàn bộ 156 học viên theo công thức chuẩn ở trên để cập nhật điểm chính xác.

2. **Khóa HCM-KS24 (Không làm dự án môn học):**  
   $$\text{Final} = \text{Vấn đáp} \times 40\% + (\text{Thực hành} \times 20\% + \text{Trắc nghiệm} \times 80\%) \times 60\%$$

3. **Khóa KS25 (Cả HN và HCM):**  
   $$\text{Final} = \text{Thực hành} \times 70\% + \text{Trắc nghiệm} \times 30\%$$

---

## II. SO SÁNH HIỆU NĂNG ĐÀO TẠO KS24 HN VS. HCM

Dữ liệu sau khi tính toán lại bằng công thức chuẩn cho thấy sự phân hóa rõ rệt giữa hai cơ sở:

| Chỉ số (Khối CNTT) | Khối HN-KS24 (Toàn bộ) | Khối HCM-KS24 (Toàn bộ) | Tổng cộng KS24 |
| :--- | :---: | :---: | :---: |
| **Tổng số đăng ký** | 156 học viên | 44 học viên | 200 học viên |
| **Số lượng tham gia thi** | 142 học viên (91.0%) | 36 học viên (81.8%) | 178 học viên (89.0%) |
| **Điểm Final TB (Toàn bộ)** | **53.46 / 100** | **52.91 / 100** | **53.34 / 100** |
| **Điểm Final TB (Đã thi)** | **58.73 / 100** | **64.67 / 100** | **59.93 / 100** |
| **Điểm Thực hành TB** | 49.29 / 100 | 65.91 / 100 | 52.95 / 100 |
| **Điểm Trắc nghiệm TB** | 57.41 / 100 | 66.95 / 100 | 59.51 / 100 |
| **Điểm Vấn đáp TB** | **49.61 / 100** | **32.16 / 100** | 45.77 / 100 |
| **Điểm Sản phẩm TB** | **52.15 / 100** | **0.00 / 100** | 40.67 / 100 |
| **Tỷ lệ Sẵn sàng (Mức 2+3)**| **32.05%** (50 SV) | **36.36%** (16 SV) | **33.00%** (66 SV) |

### Nhận xét chuyên sâu:
- **Ưu thế thi viết của HCM:** Sinh viên HCM có điểm thi tự luận (Thực hành - 65.91 vs. 49.29) và trắc nghiệm (66.95 vs. 57.41) cao hơn hẳn sinh viên HN. 
- **Điểm nghẽn vấn đáp của HCM:** Điểm vấn đáp của HCM cực kỳ thấp (**32.16** so với **49.61** của HN), đồng thời không có điểm sản phẩm do không làm dự án trước đó. Đây là lý do khiến điểm Final trung bình của sinh viên HCM bị kéo xuống, làm tỷ lệ sẵn sàng doanh nghiệp đạt mức tương đồng với Hà Nội (36.36% vs. 32.05%).
- **Tỷ lệ vắng thi:** Cơ sở HCM có tỷ lệ vắng thi và hoãn thi cao hơn HN (18.2% vs. 9.0%), cho thấy cần siết chặt hơn nữa công tác vận hành lớp học tại cơ sở phía Nam.

---

## III. BÁO CÁO ĐỐI SOÁT ĐIỂM TỰ LUẬN (PRACTICAL SCORE AUDIT)

Bằng thuật toán khớp tên thông minh (loại bỏ hậu tố phân biệt trùng tên như " 2", " 3"), hệ thống đã tiến hành đối soát chi tiết điểm tự luận trong file chính với 3 file điểm chi tiết của Chuyên gia chấm trước đó:

1. **Khớp hoàn toàn (164 học viên):** Điểm số thực hành trên tệp tổng hợp khớp 100% với điểm chi tiết (sau khi nhân hệ số 10 để đưa về thang 100).
2. **Sai lệch thực tế (03 trường hợp đặc biệt):**
   - **`Phan Thuận Thành` (HN-KS24-CNTT2):** Điểm chấm chi tiết là `10.0/10` (100 điểm) nhưng trong tệp tổng hợp bị bỏ trống (`None`/`0.0`). Điều này khiến điểm Final của em bị kéo xuống **60.7** thay vì **76.1** (lệch **15.4 điểm**). Đây là một lỗi nhập liệu nghiêm trọng cần được hiệu chỉnh lại ngay để trả lại quyền lợi cho sinh viên.
   - **`Đỗ Minh Tuyến` (HN-KS24-CNTT1):** Điểm chấm chi tiết đạt `10.0/10` (100 điểm) nhưng tệp tổng hợp gán `0.0`. Ghi chú ghi rõ: **"Sử dụng AI trong quá trình làm bài"**. Việc hủy điểm thi này là chính xác theo biên bản vi phạm quy chế thi.
   - **`Võ Thanh Khang` (HCM-KS24-CNTT1):** Điểm chấm chi tiết là `0.0` nhưng tệp tổng hợp ghi nhận `80.0`. Biên bản ghi chú: **"T Phước 50"** (thể hiện việc chấm bổ sung hoặc phúc khảo bởi giảng viên Phước).
3. **Danh sách 33 học viên không có bài chấm chi tiết:**  
   Toàn bộ 33 học viên này đều ghi nhận điểm Thực hành là `0.0` hoặc `None` trên tệp tổng hợp. Đây là các học viên vắng thi, có đơn hoãn thi chính thức (như `Hoàng Cương Cát`, `Cao Tất Thành`) hoặc gặp sự cố Simple Care nghiêm trọng nên không có bài làm để chấm.

---

## IV. BÁO CÁO LỆCH PHA SỰ CỐ HỆ THỐNG & ĐỀ XUẤT LỊCH THI BỔ SUNG

Sự "lệch pha" giữa báo cáo của Agent trước đó và Leader xuất phát từ việc Agent cũ chỉ phân tích dựa trên dữ liệu các bài thi đã được chấm điểm chi tiết (167 bài làm), bỏ qua các trường hợp bị lỗi hệ thống ngay từ khâu phát đề hoặc nộp bài.

Dưới đây là thống kê chi tiết các sự cố kỹ thuật quét được từ nhật ký ghi chú và biên bản của kỳ thi:

### 1. Tổng hợp lỗi hệ thống phần mềm khảo thí
- **Tổng số ca ghi nhận lỗi hệ thống:** **61 ca** trên toàn kỳ thi.
  - **Khóa KS24:** **16 ca** (4 ca CNTT, 12 ca Ngoại ngữ).
  - **Khóa KS25:** **45 ca** (29 ca CNTT, 16 ca Ngoại ngữ/KNM).

### 2. Chi tiết lỗi hệ thống khối KS24 (CNTT)
Có 4 học viên KS24 gặp lỗi hệ thống Simple Care nghiêm trọng trong ca thi CNTT ngày 10/08/2026 (ca thi 12:10 - 14:10):
- **`Nguyễn Thế Kiên` (HN-KS24-CNTT3):** Lỗi Simple Care (Không nộp được bài) $\rightarrow$ Đăng ký thi bổ sung.
- **`Phạm Ngọc Linh` (HN-KS24-CNTT4):** Lỗi Simple Care (Không nộp được bài) $\rightarrow$ Đăng ký thi bổ sung.
- **`Trịnh Khắc Hưng` (HN-KS24-CNTT3):** Lỗi Simple Care (Không chạy được phần mềm) $\rightarrow$ Đăng ký thi bổ sung.
- **`Đỗ Hồng Kỳ` (HN-KS24-CNTT3):** Lỗi Simple Care (Bị out ra ngoài và không vào lại được) $\rightarrow$ Đăng ký thi bổ sung.

### 3. Chi tiết lỗi hệ thống khối KS25 (CNTT) - Tập trung ca đầu tiên
Trong số 29 học viên KS25 CNTT bị lỗi hệ thống:
- **Ca 1 (07:00 - 09:00 ngày 10/08/2026):** Ghi nhận **16 học viên** bị lỗi hệ thống (chiếm 55% tổng số ca lỗi của KS25). Các lỗi phổ biến: "Hệ thống không ghi nhận bài làm", "Lỗi nộp bài", "Lỗi đề thi thực hành câu 36".
- **Ca 2 (12:10 - 14:10 ngày 10/08/2026):** Ghi nhận **12 học viên** bị lỗi hệ thống (100% tại cơ sở HCM-KS25), chủ yếu là lỗi "Hệ thống không nộp được bài" kèm tệp chụp ảnh minh chứng.

---

## V. DANH SÁCH ĐĂNG KÝ THI BỔ SUNG NGÀY 22/08/2026

Để giải quyết triệt lại các ca vắng thi và lỗi hệ thống, nhà trường tổ chức thi lại/thi bổ sung vào ngày **22/08/2026** với tổng cộng **263 lượt sinh viên** đăng ký:

### 1. Phân bổ theo Khóa học & Địa bàn
- **Khóa KS24:** **49 lượt** đăng ký thi bổ sung.
- **Khóa KS25:** **214 lượt** đăng ký thi bổ sung (chủ yếu do sự cố ca đầu và các ca vắng thi).

### 2. Phân bổ theo Môn thi & Khóa
- **Khối KS24 (49 lượt):**
  - *Ngoại ngữ (Tiếng Anh):* 24 học viên.
  - *Công nghệ thông tin:* 15 học viên (bao gồm các ca lỗi Simple Care).
  - *Kỹ năng mềm:* 10 học viên.
- **Khối KS25 (214 lượt):**
  - *Công nghệ thông tin:* **122 học viên** (phản ánh đúng quy mô ảnh hưởng của lỗi hệ thống ca đầu).
  - *Ngoại ngữ (Tiếng Anh):* 53 học viên.
  - *Kỹ năng mềm:* 31 học viên.
  - *Quản trị kinh doanh:* 8 học viên.

---

## VI. KHUYẾN NGHỊ & ĐỀ XUẤT CHO BAN GIÁM ĐỐC

1. **Hiệu chỉnh điểm Phan Thuận Thành:** Cần cập nhật lại điểm thực hành của học viên Phan Thuận Thành lên hệ thống quản lý học tập LMS thành 100 điểm, nâng điểm Final của em lên **76.1** để đảm bảo công bằng.
2. **Nâng cấp Hệ thống Khảo thí:** Tỷ lệ lỗi hệ thống 11.45% (ở báo cáo Leader) và số lượng thi bổ sung CNTT lên tới 137 học viên (15 KS24 + 122 KS25) cho thấy phần mềm thi Simple Care và hệ thống nộp bài cần được tối ưu hóa tải trọng trước ngày thi bổ sung 22/08/2026 để tránh lặp lại sự cố.
3. **Bồi dưỡng Kỹ năng Vấn đáp cho HCM:** Cơ sở HCM cần tổ chức các buổi mock-interview và hướng dẫn thuyết trình dự án cho học viên KS24 để cải thiện điểm số vấn đáp (hiện đang rất thấp ở mức 32.16 điểm).

---

## VII. CẬP NHẬT KẾT QUẢ THỰC TẾ SAU ĐỢT THI BỔ SUNG (22/08/2026)

Ngày 02/09/2026, tệp dữ liệu tổng hợp mới (`Danh sách thi ĐGNL (1).xlsx`) đã ghi nhận kết quả thi bổ sung ngày 22/08/2026 và hoàn tất nhập bổ sung điểm trắc nghiệm (MCQ) cùng điểm tự luận:

| Chỉ số Toàn hệ thống | Dữ liệu Đợt 1 Ban đầu (21/08) | Sau Thi Bổ sung (02/09) | Thay đổi |
| :--- | :---: | :---: | :---: |
| **Tổng số thí sinh đăng ký** | 629 SV | **630 SV** | +1 SV |
| **Số lượng dự thi thực tế** | 401 SV (63.8%) | **491 SV (77.9%)** | **+90 SV (+14.1%)** |
| **Số lượng vắng thi** | 228 SV (36.2%) | **139 SV (22.1%)** | **-89 SV (-14.1%)** |
| **Sẵn sàng Nghề nghiệp (L2 + L3)** | 86 SV (13.7%) | **108 SV (17.1%)** | **+22 SV (+3.4%)** |
| **Mức 0 (Chưa đạt chuẩn)** | 507 SV (80.6%) | **453 SV (71.9%)** | **-54 SV (-8.7%)** |

### Chi tiết theo từng Khóa học:
1. **Khóa KS24 (Java/Spring Boot - Cuối Kỳ III):**
   - Đăng ký: **201 SV** | Dự thi: **185 SV (92.0%)** | Vắng: **16 SV (8.0%)**.
   - Điểm Final TB: **5.58/10**. Tỷ lệ Sẵn sàng (L2+L3): **32.8% (66 SV)**.
   - Hà Nội: Dự thi 143/156, Điểm TB 5.95, Sẵn sàng 32.1% (50 SV).
   - TP.HCM: Dự thi 42/44, Điểm TB 6.43, Sẵn sàng 36.4% (16 SV).

2. **Khóa KS25 (FastAPI/Python - Giữa Kỳ II):**
   - Đăng ký: **429 SV** | Dự thi: **306 SV (71.3%)** (tăng mạnh từ 223 SV đợt 1) | Vắng: **123 SV (28.7%)**.
   - Điểm Final TB: **3.23/10**. Tỷ lệ Sẵn sàng (L2+L3): **9.8% (42 SV)** (tăng từ 4.7%).
   - Hà Nội: Dự thi 181/278 (tăng 80 SV sau thi bù), Điểm TB 2.96, Sẵn sàng 9.7% (27 SV).
   - TP.HCM: Dự thi 125/151, Điểm TB 3.62, Sẵn sàng 9.9% (15 SV).

