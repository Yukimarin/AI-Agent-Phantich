# Walkthrough - Báo cáo Phân tích Năng lực KS24 ĐGNL Lần 1 (Đã hiệu chỉnh)

Dự án đã hoàn thành hiệu chỉnh phân tích toàn bộ **200 sinh viên** khối KS24 dựa trên kết quả thi ĐGNL Lần 1 (áp dụng đúng công thức trọng số điểm sản phẩm HN) và xuất bản thành công Dashboard HTML tương tác cao cấp.

---

## 1. Kết quả Phân tích Số liệu (Thống kê chính sau hiệu chỉnh)
*   **Tổng số sinh viên:** 200 học viên (HN: 156 SV, HCM: 44 SV).
*   **Điểm trung bình ĐGNL:** **5.33 / 10** (HN: 5.35/10, HCM: 5.29/10).
*   **Tỷ lệ Sẵn sàng Doanh nghiệp (Level 2 + Level 3):** **33.0%** (66/200 sinh viên).
*   **Tỷ lệ Chưa sẵn sàng (Level 0 - Cần đào tạo lại):** **21.5%** (43/200 sinh viên).
*   **Điểm nghẽn kỹ năng thực tế:**
    *   **Tư duy hệ thống (System Thinking):** Điểm trung bình chỉ đạt **12.57%** (HN là 10.0%, HCM là 21.62%). Đây là phần yếu nhất của sinh viên khi phải đưa ra các quyết định ưu tiên sửa lỗi và giải thích trade-offs.
    *   **Giao dịch & Đồng thời (Concurrency):** Điểm trung bình đạt **52.07%** (HN là 46.42%, HCM là 71.89%).
    *   **Bảo mật & Ủy quyền (Security):** Điểm trung bình đạt **58.60%** (HN là 53.55%, HCM là 76.35%).

---

## 2. Các sản phẩm đã tạo/cập nhật
1.  **Dashboard HTML tương tác mới:** [outputs/KS24_DGNL_Report.html](file:///c:/Users/DELL/Desktop/AI-Agent/AI-ĐGNL/outputs/KS24_DGNL_Report.html)
    *   *Tính năng:* Chứa 4 biểu đồ trực quan (Phân bố điểm, Tỷ lệ Sẵn sàng, Radar kỹ năng thực tế, Độ tương thích vị trí tuyển dụng 2026).
    *   *Tính tương tác:* Thanh tìm kiếm sinh viên, bộ lọc theo ca thi, bộ lọc theo mức độ sẵn sàng, và xem chi tiết nhận xét từng sinh viên.
2.  **Mã nguồn xử lý dữ liệu tối ưu:** [src/process_all_data.py](file:///c:/Users/DELL/Desktop/AI-Agent/AI-ĐGNL/src/process_all_data.py)
    *   *Tính năng:* Tối ưu hóa token đầu vào, sửa lỗi cú pháp trùng khớp chuỗi (không đạt/đạt) và áp dụng đúng công thức trọng số HN/HCM.
3.  **Báo cáo Đối soát chuyên sâu:** [ks24_ks25_detailed_analysis.md](file:///c:/Users/DELL/Desktop/AI-Agent/AI-ĐGNL/docs/reports/ks24_ks25_detailed_analysis.md)
    *   *Tính năng:* Phân tích chi tiết chênh lệch HN/HCM, đối soát điểm tự luận (phát hiện 3 ca đặc biệt) và làm rõ 61 ca lỗi hệ thống khảo thí cùng danh sách thi lại.

---

## 3. Cách mở và xem báo cáo
Anh Bách có thể mở trực tiếp tệp [KS24_DGNL_Report.html](file:///c:/Users/DELL/Desktop/AI-Agent/AI-ĐGNL/outputs/KS24_DGNL_Report.html) bằng bất kỳ trình duyệt nào (Chrome, Edge, Firefox) để bắt đầu duyệt dữ liệu và xem các biểu đồ trực quan hóa.
