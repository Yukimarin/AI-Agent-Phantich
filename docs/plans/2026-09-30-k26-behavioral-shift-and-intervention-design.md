# Kế Hoạch Thiết Kế: Theo Dõi Chuyển Dịch Hành Vi & Can Thiệp Sinh Viên K26

> **Ngày lập**: 30/09/2026  
> **Người yêu cầu**: Giám đốc Đào tạo (anh Nguyễn Duy Quang)  
> **Chủ trì thực hiện**: Quản lý Đào tạo / Antigravity Agent  
> **Mục tiêu**: Đánh giá sự chuyển biến nề nếp học tập của tân sinh viên K26 từ Môn đầu tiên (`SSK101` - Kỹ năng Học tập chủ động) sang các Môn học hiện tại (`IT108`, `SKL01`, `ENG105`, `SSK102`, `SSK103`), bóc tách tỷ lệ cải thiện từng lớp, phân loại 4 nhóm hành vi và xây dựng kế hoạch hành động trực tiếp 5–15 phút tại lớp kèm chỉ định PIC và Deadline.

---

## 1. Bối Cảnh & Động Lực Nghiệp Vụ

### 1.1 Yêu cầu của Giám đốc Đào tạo
- Phân nhóm sinh viên K26 có vấn đề chuyên cần, chuẩn bị bài Elearning, làm bài tập về nhà theo 4 dải % vi phạm: `20% - 40%`, `40% - 60%`, `60% - 80%`, `80% - 100%`.
- Tìm hiểu lý do, tháo gỡ khó khăn và đưa ra giải pháp xử lý triệt để nhằm đảm bảo các chỉ số đào tạo.

### 1.2 Phản biện & Hiệu chỉnh Thực Tế Tác Chiến
- **Phương thức can thiệp**: Không tổ chức họp online đông người (tránh tình trạng sinh viên vắng mặt, tắt camera, lãng phí thời gian và thụ động). Thay vào đó, Quản lý Đào tạo và CVHT sẽ **vào trực tiếp lớp 5–15 phút** vào đầu giờ, giữa giờ hoặc cuối giờ để làm việc trực diện.
- **Bóc tách lỗi thích nghi ban đầu**: Ở tuần đầu tiên môn SSK101, nhiều sinh viên vi phạm do chưa quen LMS / chưa kích hoạt tài khoản (trường đã xóa lỗi EL buổi 1). Nếu sinh viên sang môn mới đã học nghiêm túc, đạt 100% chỉ số thì **miễn can thiệp kỷ luật** để tránh gây tâm lý tiêu cực.
- **Bổ sung nhóm TH4 (Sốc môn mới)**: Sinh viên môn 1 học tốt nhưng sang môn chuyên ngành (IT108 Nhập môn CNTT, ENG105 Tiếng Anh) bắt đầu nợ bài, vắng mặt do độ khó kiến thức. Cần phát hiện sớm để giảng viên bộ môn và trợ giảng kèm cặp.

---

## 2. Kiến Trúc Phân Loại 4 Nhóm Chuyển Dịch Hành Vi

Hệ thống tính toán độ biến động vi phạm cho từng sinh viên:
$$\Delta_{\text{vi phạm}} = \% \text{Vi phạm Môn Mới (Trung bình)} - \% \text{Vi phạm Môn SSK101}$$

| Nhóm | Tên Nhóm | Định Nghĩa Định Lượng | Bản Chất Vấn Đề | Giải Pháp Tác Chiến 5-15 Phút | Người Phụ Trách (PIC) | Hạn Chót (Deadline) |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- |
| **TH1** | **Nguy cơ bỏ học (Báo động Đỏ)** | Môn 1 vi phạm CC $\ge 40\%$ $\rightarrow$ Môn mới tiếp tục vắng $\ge 20\%$ | Ý thức yếu, nợ nần, làm thêm quá giờ hoặc muốn bỏ học | Gặp riêng 5 phút cuối giờ, lập biên bản cam kết, gọi phụ huynh | Quản lý ĐT + CVHT | Trong 48 giờ |
| **TH4** | **Sốc môn mới (Cần hỗ trợ học thuật)** | Môn 1 vi phạm $< 20\%$ $\rightarrow$ Môn mới nợ BTVN $\ge 40\%$ | Không hiểu bài lập trình IT108, rào cản tiếng Anh | Gặp 5 phút giữa giờ, kết nối giảng viên bộ môn và trợ giảng kèm | Giảng viên bộ môn + Trợ giảng | Trước buổi học tới |
| **TH2** | **Đang cải thiện (Cần đôn đốc)** | Môn 1 vi phạm cao $\rightarrow$ Môn mới vi phạm giảm mạnh ($< 20\%$) | Đã có ý thức nhưng kỹ năng quản lý thời gian còn yếu | Nhắc nhở nhanh 3 phút đầu giờ, đôn đốc lịch nộp bài | CVHT lớp | Hết tuần |
| **TH3** | **Thích nghi tốt (Biểu dương)** | Môn 1 có vi phạm $\rightarrow$ Môn mới vi phạm 0% | Lỗi tuần đầu do bỡ ngỡ kỹ thuật LMS, nay đã vào guồng | Miễn can thiệp, gửi tin nhắn chúc mừng và biểu dương | CVHT lớp | Hoàn thành ngay |

---

## 3. Cấu Trúc Bảng Chỉ Số Cải Thiện Từng Lớp (Class Improvement Matrix)

Công thức Tỷ lệ Cải thiện của Lớp:
$$\text{Tỷ lệ Cải thiện} = \frac{\text{Số SV TH3 (Đã sạch lỗi)} + \text{Số SV TH2 (Đang tiến bộ)}}{\text{Tổng sĩ số lớp}} \times 100\%$$

Bảng xếp hạng 9 lớp K26:
1. `HN-KS26-CNTT1`
2. `HN-KS26-CNTT2`
3. `HN-KS26-CNTT3`
4. `HN-K26-QTKD1`
5. `HN-K26-QTKD2`
6. `HN-K26-QTKD3`
7. `HCM-KS26-CNTT1`
8. `HCM-KS26-CNTT2`
9. `HCM-KS26-QTKD1`

Mỗi lớp phân rã số lượng & tỷ lệ % của 4 nhóm TH1, TH2, TH3, TH4; xác định Môn học mới đang là điểm nghẽn (ví dụ `IT108` hay `ENG105`) và mức độ ưu tiên can thiệp.

---

## 4. Các Sản Phẩm Đầu Ra (Deliverables)

1. **File Excel Tác Chiến (`output/dashboards/management/K26_Theo_Doi_Chuyen_Dich_Hanh_Vi_Va_Giai_Phap.xlsx`)**:
   - `BANG_CHI_SO_CAI_THIEN_TUNG_LOP`: Bảng xếp hạng 9 lớp kèm chỉ số cải thiện và môn gây nghẽn.
   - `TH1_CAN_THIEP_NGAY`: Danh sách SV nguy cơ bỏ học (có sẵn cột ghi chú lý do để bạn điền tại lớp).
   - `TH4_SOC_MON_MOI`: Danh sách SV cần GV bộ môn phụ đạo.
   - `TH2_DANG_TIEN_BO`: Danh sách SV tiến bộ cần CVHT đôn đốc.
   - `TH3_DA_KHAC_PHUC`: Danh sách SV sạch vi phạm để biểu dương.
   - `9 Sheet chi tiết từng lớp`: Định dạng in/cầm theo khi vào từng lớp 5–15 phút.

2. **Báo Cáo HTML Trực Quan Dành Cho Giám Đốc Đào Tạo (`output/dashboards/management/bao_cao_k26_chuyen_dich_hanh_vi.html`)**:
   - Thẻ chỉ số KPI lớn: Tỷ lệ Cải thiện Toàn khóa, Số SV Nguy cơ cao TH1, Số SV Sốc môn mới TH4, Số SV Thích nghi TH3.
   - Biểu đồ thanh ngang so sánh Tỷ lệ Cải thiện của 9 lớp.
   - Biểu đồ phân bổ 4 nhóm hành vi TH1–TH4 toàn khóa.
   - Bảng tổng hợp Kế hoạch Hành động Thực chiến: Vấn đề $\rightarrow$ Giải pháp 5-15p $\rightarrow$ PIC $\rightarrow$ Deadline.
   - Tích hợp nút **"Sao chép tóm tắt gửi Giám đốc"** và nút **"Tải File Excel"**.

3. **Cập nhật Báo Cáo Giao Ban Tuần (`output/dashboards/management/weekly_director_report.html`)**:
   - Nhúng liên kết và tóm tắt nhanh chuyên đề K26 Chuyển dịch Hành vi vào Tab 3.
