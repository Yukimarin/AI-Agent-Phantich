# Báo Cáo Chuyên Đề: So Sánh Toàn Diện KPI Master Cũ & Mới Khối CNTT (Bản FINAL)
### Đánh Giá Cải Thiện Hiệu Suất, Chuẩn Hóa Giờ Làm & Quản Trị Chất Lượng Đào Tạo

> **Người thực hiện**: Hệ thống AI Phân tích Chỉ số Đào tạo (Antigravity & Subagents)  
> **Kính gửi**: Ban Giám đốc Đào tạo & Khối Công nghệ Thông tin (CNTT)  
> **Thời điểm lập báo cáo**: 08/09/2026  
> **Tài liệu nguồn chuyển đổi**: `KPI_MASTER_Giang_vien_Tro_giang_FINAL.xlsx` ➔ [`data/inputs/kpi_master_cntt_final.md`](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/data/inputs/kpi_master_cntt_final.md)  
> **Cơ sở dữ liệu kiểm toán**: 22 nhân sự khối CNTT (Hà Nội Ngọc Trục, Hà Nội HPC, Hồ Chí Minh) - Dữ liệu Tháng 8/2026.

---

## 1. TỔNG QUAN BỐI CẢNH & Ý NGHĨA BƯỚC NGOẶT

Trước đây, Khối CNTT vận hành dựa trên bảng KPI cũ trích xuất từ `Quản lý hiệu suất đào tạo.xlsx` (152 định mức). Bản cũ bộc lộ nhiều kẽ hở quản trị nghiêm trọng:
1. **Bong bóng giờ ảo trong sản xuất học liệu**: Cho phép nhân sự tự do khai báo sản xuất bài tập, project mẫu, ra đề thi với định mức khổng lồ từ **480 phút (8h) đến 1,920 phút (32h)** mà không có tiêu chuẩn nghiệm thu độc lập.
2. **Định mức ca thực hành thiếu thực tế**: Áp định mức 180 phút (3.0h) cho ca thực hành, trong khi nhiều buổi học thực tế chỉ kéo dài 120 phút.
3. **Chấm thi nhân lũy tiến theo đầu học viên**: Dẫn đến việc nhân hệ số giờ chấm thi quá lớn, không sát với thực tế quản lý lớp.
4. **Thiếu phân định chuyên môn hóa cho Rank cao (R6 - R8)**: Giảng viên cấp cao vẫn gán nhiệm vụ dạy lớp hoặc tự khai giờ tự do không kiểm soát.

Bản **KPI MASTER FINAL** (`KPI_MASTER_Giang_vien_Tro_giang_FINAL.xlsx` - 249 định mức) là một bước chuyển đổi mang tính cách mạng: **Chuyển từ cơ chế "Khai báo bù giờ để đủ công" sang cơ chế "Định mức chuẩn xác & Kiểm soát chất lượng độc lập"**.

---

## 2. MA TRẬN SO SÁNH ĐỐI ĐẦU: KPI MASTER CŨ VS. KPI MASTER MỚI

| Tiêu Chí So Sánh | KPI Master Cũ (Bản 152 mục) | KPI Master Mới FINAL (Bản 249 mục) | Bản Chất Cải Thiện & Ý Nghĩa Quản Trị |
| :--- | :--- | :--- | :--- |
| **Quy mô danh mục** | 152 định mức (nhiều mục rỗng, trùng lặp) | **249 định mức chuẩn hóa** (Phủ trọn R0 ➔ R8) | Tăng độ bao phủ thêm **+63.8%**, đảm bảo 100% công việc đều có barem chuẩn trên Worklane. |
| **Tính duy nhất của Mã (Key)** | Cấu trúc không đồng nhất (`name-role-rank` hoặc không có key) | **`Role-Rank-Task Type`** duy nhất 100% (0 trùng) | Dễ dàng tích hợp vào hệ thống Dropdown Worklane, tự động điền giờ theo Rank nhân sự. |
| **Sản xuất học liệu tự do** | Tồn tại các task "bong bóng": BTVN 720p (12h), Project mẫu 1,440p (24h), PM 1,920p (32h) | **Đưa về 0 nhiệm vụ tự do** (`Nhiệm vụ sản xuất học liệu còn lại: 0`) | **Triệt tiêu hoàn toàn giờ ảo**. Không còn tình trạng nhân sự tự nhận định mức 2-4 ngày công để làm slide/quiz tự do. |
| **Hệ thống Kiểm soát chất lượng** | Chỉ có 1 task chung chung "Review Học liệu" (240 phút) | **Thiết lập 18 Task Type Review Độc Lập** (162 định mức chi tiết từ R1 ➔ R8) | Chuyển dịch trọng tâm sang thẩm định: Review slide, video, mindmap, quiz, project, đề thi, PM chương trình/môn học. |
| **Điều kiện nghiệm thu Review** | Không có quy định | **Bắt buộc**: Checklist + Danh sách lỗi/góp ý + Kết luận Đạt/Không đạt | Ngăn chặn nghiệm thu hình thức, nâng cao chất lượng học liệu số toàn hệ thống. |
| **Tính độc lập & Re-review** | "Vừa đá bóng vừa thổi còi" (tự làm tự duyệt) | Người review độc lập với người sản xuất; **Re-review tối đa 50% giờ lần 1** (tối thiểu 15p) | Đảm bảo tính khách quan và khống chế không để phát sinh chi phí review dây dưa. |
| **Giảng dạy trực tiếp** | Lý thuyết 180p (3.0h), Thực hành 180p (3.0h) | **Đồng bộ chuẩn 120 phút/buổi (2.0h)** cho cả Lý thuyết, Thực hành, Mini-project | Cắt giảm 1.0h giờ ảo mỗi ca thực hành; khống chế: *Mỗi buổi chỉ ghi nhận 1 loại triển khai*. |
| **Chấm KT 30 phút đầu giờ** | Tính theo lớp hoặc nhân lẻ tẻ | **Cố định 120 phút/lớp** (trọn gói cho toàn bộ SV) | Chống gian lận khai báo nhân hệ số theo từng bài sinh viên. |
| **Phân định Giảng viên Rank 6 - 8** | Vẫn có task dạy lý thuyết 180p, chuẩn 1 vòng 44.1h | **Không dạy hoặc vận hành lớp**; chỉ làm Chuyên gia Review và Khảo thí cấp cao (Tổng chuẩn: **21.4h**) | Định vị đúng vai trò chuyên gia chiến lược, tránh lãng phí chi phí nhân sự cấp cao vào việc vận hành cơ bản. |
| **Lộ trình Trợ giảng** | Chỉ có Rank 1 và Rank 2 | **Bổ sung Trợ giảng Rank 3** (Tổng chuẩn 44.1h) | Mở rộng khung chức danh, tạo động lực thăng tiến rõ ràng cho đội ngũ Trợ giảng. |
| **Công việc đột xuất (Rank 0)** | Gộp vào các task không định mức (hỗ trợ, họp...) | **Quy chuẩn riêng Rank 0**: Tự mô tả, khai báo giờ thực tế | Minh bạch hóa việc đột xuất ngoài kế hoạch, không cho phép mượn danh task đào tạo. |

---

## 3. PHÂN TÍCH ĐỘ DỐC NĂNG SUẤT THEO CẤP RANK (PRODUCTIVITY GRADIENT)

Một trong những điểm ưu việt nhất của KPI Master FINAL là **Độ dốc năng suất tỷ lệ nghịch với Cấp Rank**: Nhân sự rank càng cao thì thời gian định mức để hoàn thành cùng một đơn vị công việc càng ngắn, thể hiện trình độ chuyên môn cao hơn và tốc độ xử lý nhanh hơn.

### Tổng định mức khi thực hiện 01 vòng toàn bộ danh mục nhiệm vụ:
- **Trợ giảng**:
  - **Rank 1**: 30 nhiệm vụ ➔ **3,140 phút (52.3h)**
  - **Rank 2**: 30 nhiệm vụ ➔ **2,795 phút (46.6h)** *(Nhanh hơn Rank 1: -11.0%)*
  - **Rank 3**: 32 nhiệm vụ ➔ **2,645 phút (44.1h)** *(Nhanh hơn Rank 2: -5.4%)*
- **Giảng viên**:
  - **Rank 3**: 32 nhiệm vụ ➔ **2,645 phút (44.1h)**
  - **Rank 4**: 30 nhiệm vụ ➔ **2,405 phút (40.1h)** *(Nhanh hơn Rank 3: -9.1%)*
  - **Rank 5**: 30 nhiệm vụ ➔ **2,195 phút (36.6h)** *(Nhanh hơn Rank 4: -8.7%)*
  - **Rank 6, 7, 8**: 21 nhiệm vụ ➔ **1,285 phút (21.4h)** *(Tập trung 100% vào Review & Khảo thí, tốc độ thẩm định chuyên sâu)*

> [!TIP]
> **Ý nghĩa quản trị**: Cơ chế này loại bỏ hoàn toàn tình trạng cào bằng giờ làm. Giảng viên Rank 5 khi chuẩn bị giảng dạy chỉ được tính 30 phút (thay vì 50 phút của Rank 3), review kịch bản chỉ 20 phút (thay vì 25 phút), chấm thi sản phẩm chỉ 20 phút/SP (thay vì 30 phút). Điều này buộc nhân sự cấp cao phải chứng minh giá trị qua chất lượng và tốc độ vượt trội.

---

## 4. TÁC ĐỘNG THỰC TẾ LÊN GIỜ CÔNG & HIỆU SUẤT KHỐI CNTT (THÁNG 8/2026)

Áp dụng bộ barem KPI Master FINAL vào dữ liệu kiểm toán 22 nhân sự khối CNTT trong Tháng 8/2026 (43 ngày làm việc, 20 ngày tiêu chuẩn), kết quả phản ánh bức tranh hoàn toàn chân thực:

### 4.1 Bảng Tổng Hợp Theo Cơ Sở (Khối CNTT)

| Cơ Sở Đào Tạo | Quy Mô Nhân Sự | Tổng Giờ Khai Báo | Tổng Giờ Chuẩn Thực Tế | Giờ Dôi Dư (Bù Giờ/Học Liệu) | Tỷ Lệ Dôi Dư | Tỷ Lệ Tuân Thủ Báo Cáo |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Cơ sở Hà Nội - Ngọc Trục** | 7 NS | 878.2h | 363.1h | **515.3h** | **58.7%** | 88.6% |
| **Cơ sở Hà Nội - HPC** | 6 NS | 840.5h | 273.3h | **567.3h** | **67.5%** | 90.0% |
| **Cơ sở TP. Hồ Chí Minh** | 9 NS | 1,029.2h | 581.8h | **447.4h** | **43.5%** | 81.1% |
| **TOÀN KHỐI CNTT** | **22 NS** | **2,747.9h** | **1,218.2h** | **1,530.0h** | **55.7%** | **86.4%** |

### 4.2 Nhận Định Cốt Lõi Từ Dữ Liệu
1. **Cắt bỏ hoàn toàn 1,530 giờ ảo**: Trước đây, 1,530 giờ này thường được "hợp thức hóa" dưới dạng *Xây dựng bài tập BTVN (12h)*, *Soạn slide/project (16h - 24h)*, hoặc *Nghiên cứu công nghệ tự do*. Với KPI Master FINAL, các task này bị chặn cứng hoặc gán nhãn `Đầu việc tự do cần nghiệm thu`, làm rõ bản chất nhân sự đang nhàn rỗi trong tháng hè/chuyển giao môn.
2. **Cơ sở HCM có hiệu suất thực chất cao nhất (Tỷ lệ dôi dư thấp nhất: 43.5%)**:
   - Đội ngũ Trợ giảng HCM (Đặng Minh Luân, Phan Ngọc Tài, Nguyễn Ngọc Sơn, Phạm Viết Hùng) có tỷ lệ bám lớp và ca thực hành rất cao (chuẩn đạt từ 77h - 97h/tháng).
   - Ca thực hành chuẩn 120 phút giúp các bạn Trợ giảng HCM ghi nhận đúng số giờ đứng lớp thực tế (từ 4-6h/ngày lên lớp) mà không bị phụ thuộc vào giờ khai bù.
3. **Cơ sở HN - HPC có tỷ lệ dôi dư cao nhất (67.5%)**:
   - Các giảng viên như Bùi Thanh Hải (Khai 132.5h / Chuẩn 25h ➔ Dôi 81.1%), Mai Xuân Chinh (Khai 132.5h / Chuẩn 30h ➔ Dôi 77.4%), Phạm Tuấn Bình (Khai 155h / Chuẩn 43.5h ➔ Dôi 71.9%) có khối lượng giảng dạy trực tiếp trong tháng 8 thấp, chủ yếu khai báo việc chuẩn bị và tự học bù giờ.

---

## 5. BẢNG KIỂM TOÁN CHI TIẾT 22 NHÂN SỰ KHỐI CNTT

Dưới đây là dữ liệu chuẩn hóa của từng nhân sự sau khi cập nhật toàn bộ vào hệ thống:

| STT | Họ và Tên | Vai Trò & Cấp Rank | Cơ Sở Phụ Trách | Giờ Khai Báo | Giờ Chuẩn | Giờ Dôi Dư | % Dôi Dư | Đề Xuất Quản Trị Của Agent |
| :---: | :--- | :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| **I** | **CƠ SỞ HÀ NỘI - NGỌC TRỤC** | | | **878.2h** | **363.1h** | **515.3h** | **58.7%** | |
| 1 | **Ngọ Văn Quý** | GV R4 | Ngọc Trục | 159.0h | 33.0h | 126.0h | 79.2% | `CẢNH BÁO BÙ GIỜ` (Chuyển sang giao Review đề/PM) |
| 2 | **Phạm Ngọc Kiên** | TG R2 | Ngọc Trục | 143.0h | 58.0h | 85.0h | 59.4% | `CẦN RÀ SOÁT RANK` (Tăng cường hỗ trợ SV thực hành) |
| 3 | **Nguyễn Quảng An** | GV R4 | Ngọc Trục | 111.5h | 27.9h | 83.6h | 75.0% | `CẢNH BÁO BÙ GIỜ` (Giao thẩm định bộ câu hỏi & quiz) |
| 4 | **Lại Trung Lâm** | TG R2 | Ngọc Trục | 158.8h | 77.8h | 81.0h | 51.0% | `CẦN RÀ SOÁT RANK` (Tác nghiệp đều, cần bám sát TKB) |
| 5 | **Lâm Tùng Dương** | GV R3 | Ngọc Trục | 159.2h | 93.7h | 65.6h | 41.2% | `CẦN RÀ SOÁT RANK` (Giờ chuẩn cao, năng suất tốt) |
| 6 | **Lương Quốc Tuấn** | GV R3 | Ngọc Trục | 122.5h | 61.2h | 61.3h | 50.0% | `CẢNH BÁO BÙ GIỜ` (Kiểm tra lại khai báo tự do) |
| 7 | **Hồ Xuân Hùng** | Leader R5 | Ngọc Trục / HPC | 24.2h | 11.5h | 12.8h | 52.9% | `CHUẨN MỰC` (Làm gương điều hành chuyên môn) |
| **II** | **CƠ SỞ HÀ NỘI - HPC** | | | **840.5h** | **273.3h** | **567.3h** | **67.5%** | |
| 8 | **Phạm Tuấn Bình** | GV R3 | HPC | 155.0h | 43.5h | 111.5h | 71.9% | `CẦN RÀ SOÁT RANK` (Nhiều giờ tự học/R&D chưa nghiệm thu) |
| 9 | **Bùi Thanh Hải** | GV R5 | HPC | 132.5h | 25.0h | 107.5h | 81.1% | `CẢNH BÁO BÙ GIỜ` (Phân công Lead Review đề Project) |
| 10 | **Mai Xuân Chinh** | TG R2 | HPC | 132.5h | 30.0h | 102.5h | 77.4% | `CẢNH BÁO BÙ GIỜ` (Tăng cường hỗ trợ SV ca tối) |
| 11 | **Đinh Thành Nam** | TG R2 | HPC | 124.5h | 38.8h | 85.8h | 68.9% | `CẦN RÀ SOÁT RANK` (Tập trung chấm KT 30p & BTVN) |
| 12 | **Nguyễn Công Hưởng**| GV R3 | HPC | 157.5h | 76.5h | 81.0h | 51.4% | `CẢNH BÁO BÙ GIỜ` (Giờ dạy tốt, giảm bớt task họp) |
| 13 | **Trịnh Quốc Hai** | GV R4 | HPC | 138.5h | 59.5h | 79.0h | 57.0% | `CẢNH BÁO BÙ GIỜ` (Giao thẩm định kịch bản & slide) |
| **III**| **CƠ SỞ TP. HỒ CHÍ MINH**| | | **1,029.2h**| **581.8h** | **447.4h** | **43.5%** | |
| 14 | **Trần Quốc Tuấn** | GV R3 | HCM | 149.5h | 54.3h | 95.2h | 63.7% | `CẦN RÀ SOÁT RANK` (Cần bổ sung task Review chuyên môn) |
| 15 | **Đặng Minh Luân** | TG R1 | HCM | 149.5h | 88.5h | 61.0h | 40.8% | `CẢNH BÁO BÙ GIỜ` (Hiệu suất thực hành rất tốt: 88.5h) |
| 16 | **Phạm Viết Hùng** | TG R2 | HCM | 137.8h | 77.3h | 60.5h | 43.9% | `CẦN RÀ SOÁT RANK` (Tác nghiệp đều, bám sát lớp) |
| 17 | **Nguyễn Đức Minh** | GV R4 | HCM | 109.5h | 54.8h | 54.7h | 50.0% | `CẢNH BÁO BÙ GIỜ` (Giờ chuẩn vững, giảm task tự do) |
| 18 | **Phan Ngọc Tài** | TG R1 | HCM | 146.2h | 97.0h | 49.2h | 33.7% | `CẢNH BÁO BÙ GIỜ` (Hiệu suất cao nhất khối: 97h chuẩn) |
| 19 | **Nguyễn Ngọc Sơn** | TG R1 | HCM | 128.5h | 80.0h | 48.5h | 37.7% | `CẢNH BÁO BÙ GIỜ` (Trợ giảng thực chiến tốt: 80h chuẩn) |
| 20 | **Lê Hà Thanh Sang** | GV R4 | HCM | 127.2h | 85.4h | 41.8h | 32.9% | `CẦN RÀ SOÁT RANK` (Giảng viên chuẩn mực nhất HCM) |
| 21 | **Lưu H. Xuân Nguyên**| TG R2 | HCM | 81.0h | 44.5h | 36.5h | 45.1% | `CẢNH BÁO BÙ GIỜ` (Số ngày báo cáo còn thiếu) |
| 22 | **Nguyễn B. Minh Đạo**| Leader R5 | HCM | 0.0h | 0.0h | 0.0h | 0.0% | `CHƯA NỘP BÁO CÁO` (Cần đôn đốc báo cáo làm gương) |

---

## 6. ĐỀ XUẤT HÀNH ĐỘNG DÀNH CHO BAN GIÁM ĐỐC & LEADER KHỐI

1. **Khóa chức năng tạo task tự do trên Worklane**:
   - Nhập toàn bộ 249 Key chuẩn từ [`data/inputs/kpi_master_cntt_final.md`](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/data/inputs/kpi_master_cntt_final.md) vào hệ thống Worklane.
   - Khi nhân sự chọn đầu việc, hệ thống tự động khóa cứng số phút theo Rank (ví dụ: GV R4 chọn "Chuẩn bị giảng dạy" tự động nhận 40 phút; TG R2 chọn "Triển khai thực hành" tự động nhận 120 phút).
2. **Kích hoạt cơ chế "Giao Task Review Chất Lượng" để triệt tiêu thời gian nhàn rỗi**:
   - Đối với các Giảng viên có tỷ lệ dôi dư cao trong tháng hè (Bùi Thanh Hải, Ngọ Văn Quý, Nguyễn Quảng An): Phân bổ ngay các gói **Review đề Project (195-225 phút/đề)**, **Review đề thi trắc nghiệm (50-55 phút/đề)**, **Review PM môn học (105-120 phút/môn)**.
   - Chỉ nghiệm thu giờ công khi có Biên bản review + Checklist lỗi/góp ý được phê duyệt.
3. **Áp dụng chính sách Re-review 50%**:
   - Khống chế việc sửa đổi tài nguyên: Nếu học liệu chưa đạt phải sửa và review lại, người review chỉ được ghi nhận tối đa 50% thời gian lần đầu (tối thiểu 15 phút), tránh việc nhân sự thông đồng review nhiều lần để lấy giờ công.
4. **Chuẩn hóa ca học thực tế theo chuẩn 120 phút**:
   - Yêu cầu Trợ giảng các cơ sở tổ chức thực hành đúng 120 phút/buổi. Nếu lớp có nhu cầu phụ đạo thêm ngoài giờ, phải khai báo dưới dạng `Hoạt động nhóm độc lập (60 - 90 phút)` và phải có danh sách sinh viên tham gia cụ thể.

---

> [!NOTE]
> Báo cáo này đã được đồng bộ hóa vào toàn bộ các Dashboard tương tác:
> - **Master Executive Cockpit**: [`output/dashboards/core/agent_5_master_portal.html`](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/output/dashboards/core/agent_5_master_portal.html)
> - **Staff Audit Dashboard**: [`output/dashboards/audit/worklane_staff_audit.html`](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/output/dashboards/audit/worklane_staff_audit.html)
> - **Báo cáo KPI Tổng Hợp**: [`data/report_kpi_gv_tg.md`](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/data/report_kpi_gv_tg.md)
