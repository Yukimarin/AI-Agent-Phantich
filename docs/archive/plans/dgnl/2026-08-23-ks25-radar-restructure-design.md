# THIẾT KẾ TÁI CẤU TRÚC RADAR CHART & BỔ SUNG CHẨN ĐOÁN HỌC THUẬT KHÓA KS25
**Ngày lập:** 2026-08-23  
**Trạng thái:** Được phê duyệt bởi Leader  

---

## 1. MỤC TIÊU
Tái cấu trúc biểu đồ Radar từ 5 chiều kỹ thuật CNTT sang 4 chiều năng lực toàn diện của học viên tại thời điểm Học kỳ II (Thái độ & Kỷ luật, Yếu tố IT, Ngoại ngữ, Kỹ năng mềm). Lồng ghép các nhãn chẩn đoán học thuật để chỉ ra chính xác sinh viên nào bị yếu lập trình nền tảng hoặc hổng ứng dụng framework.

---

## 2. CÔNG THỨC QUY ĐỔI 4 CHIỀU NĂNG LỰC (THANG 100)

### 2.1. Thái độ & Kỷ luật (Attitude & Discipline)
*   **Điểm khởi điểm:** 100 điểm.
*   **Trừ điểm vắng thi:** Trừ 30 điểm cho mỗi môn vắng thi trong 3 môn (CNTT, Ngoại ngữ, KNM). 
    *   *Xác định vắng CNTT:* Cột `Điểm danh P1` hoặc `Điểm danh P2` có giá trị là "Vắng".
    *   *Xác định vắng Ngoại ngữ/KNM:* Cột `Điểm danh` của sheet tương ứng có giá trị là "Vắng" hoặc 0.
*   **Trừ điểm vi phạm quy chế:** Trừ 50 điểm (hoặc gán về 0) nếu cột `Biên bản` ở bất kỳ môn thi nào ghi nhận vi phạm quy chế.

### 2.2. Yếu tố IT (IT Skills)
*   **Công thức tính:** $\text{Thực hành (Đ1)} \times 0.7 + \text{Trắc nghiệm (Đ1)} \times 0.3$.
*   Nếu học viên vắng thi cả 2 phần $\rightarrow$ Điểm nhận được là 0.

### 2.3. Ngoại ngữ (Foreign Language)
*   **Lớp Tiếng Anh:** Quy đổi điểm thi TOEIC (thang 990) về thang 100:  
    $$\text{Điểm Ngoại ngữ} = \frac{\text{Điểm final ĐGNL (Lần 1)}}{990} \times 100$$
*   **Lớp Tiếng Nhật:** Gán mức điểm mặc định là **70 điểm** (do đang học bình thường và chưa có dữ liệu điểm thi trong Excel).

### 2.4. Kỹ năng mềm (Soft Skills)
*   Lấy trực tiếp từ cột `Điểm final ĐGNL (Lần 1)` trong sheet `Danh sách ĐGNL Kỹ năng mềm`.
*   Nếu vắng thi $\rightarrow$ Điểm nhận được là 0.

---

## 3. THIẾT KẾ BỘ CHẨN ĐOÁN HỌC THUẬT & GIAO DIỆN (UI/UX)

### 3.1. Phân loại Nhãn học thuật (Academic Labels)
*   🔴 **"Yếu nền tảng" (Weak Foundation):** Trắc nghiệm (Đ1) $< 50/100$ hoặc điểm trung bình của 3 tiêu chí thuật toán (1.1, 1.2, 1.3 - Python Core, Linear Search, Bubble Sort) $< 40/100$.
*   🟡 **"Hổng ứng dụng" (Framework Gap):** Học viên không thuộc nhóm "Yếu nền tảng" nhưng có điểm trung bình của các tiêu chí framework (2.x, 3.x, 4.x - FastAPI, ORM, Pydantic) $< 50/100$.
*   🟢 **"Bình thường / Tốt":** Các trường hợp còn lại.

### 3.2. Cải tiến giao diện Dashboard (`outputs/KS25_DGNL_Report.html`)
*   **Radar Chart 4 chiều:** Hiển thị 4 góc Thái độ - IT - Ngoại ngữ - KNM.
*   **Bộ lọc nhãn học thuật:** Dropdown cho phép lọc danh sách theo 3 nhãn trên.
*   **Badge hiển thị trong bảng:** Thêm cột hiển thị Badge màu (Đỏ / Vàng / Xanh lá) tương ứng với nhãn.
*   **Card chi tiết (Row Click):** Hiển thị chi tiết điểm 4 chiều và đề xuất bổ trợ tương ứng với nhãn chẩn đoán học thuật.
