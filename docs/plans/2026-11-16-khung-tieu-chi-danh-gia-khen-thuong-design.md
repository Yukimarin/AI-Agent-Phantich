# Thiết Kế Hệ Thống Khung Tiêu Chí Đánh Giá & Khen Thưởng Nội Bộ
*Áp dụng cho: Khối Đào tạo (GV/TG), Phòng Thiết kế giải pháp LMS và Phòng Quản lý Đào tạo (PTIT x Rikkei)*
*Dịp áp dụng: Lễ 20/11 và các kỳ vinh danh định kỳ (Quý / Năm học)*

---

## 1. Bối cảnh & Mục tiêu Thiết kế
Nhân dịp Lễ Kỷ niệm Ngày Nhà giáo Việt Nam 20/11 và chuẩn hóa quy trình thi đua khen thưởng lâu dài, Học viện cần một **Bộ Khung Tiêu chí Đánh giá & Khen thưởng (Academic & Operations Recognition Framework)**:
1. **Minh bạch & Định lượng**: Triệt tiêu cảm tính, cào bằng hoặc "bình bầu dĩ hòa vi quý".
2. **Có minh chứng số liệu cứng (Telemetry)**: 70% điểm số quét tự động từ LMS API và Worklane Forensic Audit.
3. **Bao quát giá trị con người**: 30% điểm số đo lường cái tâm của người thầy, trải nghiệm người dùng thực tế và tinh thần cống hiến hỗ trợ sinh viên yếu qua Rubric chuẩn hóa.
4. **Tương thích hoàn toàn với Lark Base**: Cấu trúc dữ liệu dạng bảng phẳng dễ dàng import và vận hành form đánh giá.

---

## 2. Mô hình Tổng quan: Tỷ trọng 70 / 30

```
┌────────────────────────────────────────────────────────────────────────┐
│                        TỔNG ĐIỂM: 100 ĐIỂM                             │
├──────────────────────────────────────┬─────────────────────────────────┤
│    70% ĐỊNH LƯỢNG HỆ THỐNG           │    30% ĐÁNH GIÁ PHẢN HỒI        │
│    (Telemetry & Forensic Data)       │    (Feedback & Management Rubric│
├──────────────────────────────────────┼─────────────────────────────────┤
│ • 35% Hiệu quả chuyên môn cốt lõi    │ • 15% Khảo sát Người dùng/SV    │
│   (Chuyên cần, BTVN, Uptime, TKB)    │   (Student/Internal User CSAT)  │
│ • 35% Kỷ luật vận hành & SLA         │ • 15% Tinh thần Cống hiến       │
│   (Chấm bài, Báo cáo, Khắc phục lỗi) │   (Phụ đạo SV yếu, Đổi mới AI)  │
└──────────────────────────────────────┴─────────────────────────────────┘
```

---

## 3. Khung Tiêu chí Chi tiết theo từng Khối

### 3.1. Khối Đào tạo (Giảng viên & Trợ giảng) — Trọng tâm 20/11
* **Nhóm 1: Hiệu quả Đào tạo (35 điểm - LMS Telemetry)**:
  * `DT-01` (10đ): Tỷ lệ chuyên cần sinh viên lớp phụ trách ($\ge 92\%$).
  * `DT-02` (10đ): Tỷ lệ nộp và hoàn thành BTVN ($\ge 85\%$).
  * `DT-03` (5đ): Tỷ lệ hoàn thành eLearning đúng hạn ($\ge 90\%$).
  * `DT-04` (10đ): Tỷ lệ sinh viên đủ điều kiện dự thi ($\ge 90\%$).
* **Nhóm 2: Kỷ luật Vận hành (35 điểm - Worklane & LMS Audit)**:
  * `DT-05` (10đ): Kỷ luật lên lớp đúng giờ 100%, zero bỏ tiết/đổi lịch tùy tiện.
  * `DT-06` (10đ): Tốc độ và chất lượng chấm bài / feedback cho SV (SLA $\le 48$h).
  * `DT-07` (10đ): Tính chuẩn xác báo cáo công việc (Zero vi phạm log khống Worklane).
  * `DT-08` (5đ): Cập nhật nề nếp, nộp daily report đúng hạn trước 21h00.
* **Nhóm 3: Khảo sát Sinh viên (15 điểm - Student CSAT)**:
  * `DT-09` (10đ): Điểm hài lòng của sinh viên cuối môn qua form ẩn danh ($\ge 4.5/5.0$).
  * `DT-10` (5đ): Tính tương tác, truyền cảm hứng và không khí học tập tích cực.
* **Nhóm 4: Cống hiến & Cải tiến (15 điểm - Academic Rubric)**:
  * `DT-11` (5đ): Chủ động phụ đạo, kèm cặp ngoài giờ kéo điểm cho SV yếu (có log).
  * `DT-12` (5đ): Đóng góp cải tiến học liệu, cập nhật bài lab AI thực chiến.
  * `DT-13` (5đ): Tinh thần trách nhiệm, sẵn sàng hỗ trợ việc khẩn cấp / sự kiện chung.

---

### 3.2. Phòng Thiết kế Giải pháp LMS (LMS AI & Tech)
* **Nhóm 1: Tiến độ & Sản phẩm (35 điểm - Jira / GitHub)**:
  * `LMS-01` (15đ): Tỷ lệ hoàn thành Sprint / Roadmap đúng hạn ($\ge 85\%$).
  * `LMS-02` (10đ): Tốc độ xử lý các yêu cầu nghiệp vụ khẩn phục vụ kỳ học/thi cử.
  * `LMS-03` (10đ): Chất lượng code & tỷ lệ lỗi sau release (Defect Leakage $< 5\%$).
* **Nhóm 2: Ổn định & Năng lực Vận hành (35 điểm - System SLA)**:
  * `LMS-04` (15đ): Độ sẵn sàng hệ thống (System Uptime $\ge 99.5\%$, zero lỗi giờ thi).
  * `LMS-05` (10đ): Thời gian khắc phục sự cố nghiêm trọng (SLA Recovery $< 2$h).
  * `LMS-06` (10đ): Hiệu quả tự động hóa tối ưu giờ công cho GV/QLĐT (Auto-grading, RPoint).
* **Nhóm 3: Khách hàng Nội bộ (15 điểm - Internal CSAT)**:
  * `LMS-07` (10đ): Điểm đánh giá trải nghiệm từ GV, TG và QLĐT ($\ge 4.2/5.0$).
  * `LMS-08` (5đ): Thái độ và tốc độ hỗ trợ sự cố kỹ thuật cho người dùng.
* **Nhóm 4: Sáng tạo & Công nghệ (15 điểm - Tech Innovation)**:
  * `LMS-09` (10đ): Sáng kiến ứng dụng AI & tính năng đột phá đưa vào thực tế.
  * `LMS-10` (5đ): Chuẩn hóa tài liệu kiến trúc, Wiki hướng dẫn sử dụng.

---

### 3.3. Phòng Quản lý Đào tạo (QLĐT / CVHT / Khảo thí)
* **Nhóm 1: Nề nếp & Giữ chân Sinh viên (35 điểm - Operations Metrics)**:
  * `QL-01` (15đ): Tỷ lệ duy trì sinh viên tiếp tục theo học (Retention Rate $\ge 95\%$).
  * `QL-02` (10đ): Tỷ lệ phát hiện và can thiệp SV nguy cơ (100% SV dải đỏ có biên bản).
  * `QL-03` (10đ): Tỷ lệ hỗ trợ trả nợ môn & đơn bảo lãnh hợp lệ cho sinh viên.
* **Nhóm 2: Chuẩn xác Học vụ (35 điểm - Academic SLA)**:
  * `QL-04` (10đ): Đúng hạn và chuẩn xác trong xếp TKB, điều phối phòng học (Zero xung đột).
  * `QL-05` (10đ): Độ chính xác xét duyệt điều kiện thi, chốt danh sách thi đúng hạn 100%.
  * `QL-06` (10đ): Quản lý dữ liệu điểm, chứng chỉ và đối soát Jaxtina/Lark Base khớp 100%.
* **Nhóm 3: Khảo sát Khách hàng (15 điểm - Service Mindset)**:
  * `QL-07` (10đ): Mức độ hài lòng của SV & Phụ huynh với công tác CVHT ($\ge 4.5/5.0$).
  * `QL-08` (5đ): Tốc độ xử lý thủ tục hành chính, giấy tờ học vụ (SLA $\le 24$h).
* **Nhóm 4: Phối hợp & Đổi mới (15 điểm - Cross-functional Rubric)**:
  * `QL-09` (10đ): Hiệu quả điều phối liên phòng ban giữa Đào tạo - Doanh nghiệp (OJT) - Tuyển sinh.
  * `QL-10` (5đ): Chủ động cải tiến quy trình học vụ, số hóa form mẫu tinh gọn.

---

## 4. Cơ cấu Danh hiệu & Khen thưởng Dự kiến

| Khối | Tên danh hiệu chính thức | Đối tượng áp dụng | Điều kiện tối thiểu | Số lượng | Mức thưởng gợi ý |
| :--- | :--- | :--- | :--- | :---: | :---: |
| **Đào tạo** | 🏆 **Nhà giáo Cống hiến Vàng 20/11** | Giảng viên | Tổng điểm $\ge 90$đ, CSAT $\ge 4.8$, CC $\ge 92\%$ | 02 | 3,000,000 VNĐ |
| **Đào tạo** | 🥈 **Giảng viên Truyền cảm hứng** | Giảng viên | Điểm CSAT SV cao nhất, phương pháp dạy mới | 02 | 2,000,000 VNĐ |
| **Đào tạo** | 🌟 **Trợ giảng Thắp lửa** | Trợ giảng | BTVN $\ge 85\%$, kèm cặp SV yếu xuất sắc | 02 | 1,500,000 VNĐ |
| **LMS Tech** | 🚀 **Kỹ sư Giải pháp Tiên phong** | Kỹ sư LMS | Sáng kiến AI/Automation đột phá | 01 | 2,500,000 VNĐ |
| **LMS Tech** | 🛡️ **Chiến binh Vận hành Ổn định** | System/DevOps | Uptime $\ge 99.8\%$, zero sự cố thi cử | 01 | 1,500,000 VNĐ |
| **QLĐT** | 💼 **Ngôi sao Vận hành Học vụ** | QLĐT / Khảo thí | SLA xử lý 100%, đối soát chuẩn xác tuyệt đối | 01 | 2,000,000 VNĐ |
| **QLĐT** | 🤝 **Cố vấn Học tập Tận tâm** | CVHT | Giữ chân SV $\ge 96\%$, can thiệp 100% SV đỏ | 02 | 1,500,000 VNĐ |
| **Toàn Viện**| 👑 **GƯƠNG MẶT XUẤT SẮC TOÀN VIỆN** | Toàn thể CBNV | Điểm cao nhất hệ thống, không vi phạm | 01 | 5,000,000 VNĐ |

---

## 5. Cấu trúc Tệp Excel và Khả năng Tương thích Lark Base
File Excel xuất ra tại:
`output/02_Thong_Ke_Dot_Xuat_Theo_Task/Excel_Xlsx/Bo_Tieu_Chi_Danh_Gia_Khen_Thuong_Khoi_Dao_Tao_LMS_QLDT_20261116.xlsx`

Gồm 6 Sheet tiêu chuẩn:
1. `00_Tong_Quan_Khung_Danh_Gia`: Khung tổng thể và bảng so sánh 3 khối.
2. `01_Khoi_Dao_Tao_GVTG`: 13 tiêu chí chi tiết cho Giảng viên & Trợ giảng.
3. `02_Phong_LMS_Giai_Phap`: 10 tiêu chí chi tiết cho Đội ngũ Kỹ thuật LMS.
4. `03_Phong_Quan_Ly_Dao_Tao`: 10 tiêu chí chi tiết cho Đội ngũ Quản lý Học vụ & CVHT.
5. `04_Co_Cau_Danh_Hieu_Khen_Thuong`: Bảng chi tiết điều kiện, giải thưởng và quyền lợi.
6. `05_Mau_Import_LarkBase`: Bảng phẳng (Flat Table) 33 tiêu chí, định dạng sẵn kiểu dữ liệu trường (Single Select, Number, Text) để nhập 1-click vào Lark Base.
