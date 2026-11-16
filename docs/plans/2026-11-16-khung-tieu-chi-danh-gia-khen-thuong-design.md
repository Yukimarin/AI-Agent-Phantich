# Thiết Kế Hệ Thống Khung Tiêu Chí Đánh Giá & Khen Thưởng Nội Bộ
*Áp dụng cho: Khối Đào tạo (GV/TG), Phòng Thiết kế giải pháp LMS và Ban QLĐT (PTIT x Rikkei)*
*Dịp áp dụng: Lễ 20/11 và các kỳ vinh danh định kỳ (Quý / Năm học)*
*Cập nhật: Bám sát chuẩn 100% 2 sheet đầu tiên do Trưởng ban QLĐT trực tiếp định hình.*

---

## 1. Bối cảnh & Nguyên Tắc Cốt Lõi: Tỷ Trọng 75% / 25%

Toàn bộ hệ thống đánh giá được vận hành theo cơ cấu **75% Chỉ số cốt lõi từ hệ thống + 25% Khảo sát & Đổi mới thích ứng**:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        TỔNG ĐIỂM: 100 ĐIỂM                             │
├──────────────────────────────────────┬─────────────────────────────────┤
│            TỶ TRỌNG 75%              │          TỶ TRỌNG 25%           │
│    (Chỉ số Hệ thống & Quy trình)     │    (Khảo sát & Đổi mới cải tiến)│
├──────────────────────────────────────┼─────────────────────────────────┤
│ • 40% - 50% Chỉ số chuyên môn nghiệp │ • 10% Khảo sát định kỳ          │
│   vụ cốt lõi (LMS AI, Worklane)      │   (Sinh viên / Phụ huynh / GV)  │
│ • 25% - 35% Tuân thủ quy trình, quy  │ • 15% Cải tiến tối ưu & Sẵn sàng│
│   định đào tạo, ổn định hệ thống     │   nhận mọi nhiệm vụ được giao   │
└──────────────────────────────────────┴─────────────────────────────────┘
```

---

## 2. Khung Tiêu Chí Chi Tiết theo từng Khối

### 2.1. Khối Đào tạo (Giảng viên & Trợ giảng) — *13 Tiêu chí (100%)*
*(Giữ nguyên vẹn 100% theo Sheet `Khối đào tạo`)*

* **1. Hiệu quả Đào tạo (50%)**:
  * `DT-01` (5% | 10đ): Tỷ lệ Chuyên cần sinh viên trung bình *(Nguồn: LMS AI)*.
  * `DT-02` (5% | 10đ): Tỷ lệ hoàn thành Bài tập về nhà (BTVN) *(Nguồn: LMS AI)*.
  * `DT-03` (5% | 10đ): Tỷ lệ hoàn thành eLearning đúng hạn *(Nguồn: LMS AI)*.
  * `DT-04` (15% | 10đ): Tỷ lệ SV Đủ điều kiện dự thi *(Nguồn: LMS AI)*.
  * `DT-05` (20% | 10đ): Tỷ lệ sinh viên qua môn *(Nguồn: LMS AI sau khảo thí)*.
* **2. Kỷ luật Vận hành (25%)**:
  * `DT-06` (10% | 10đ): Nắm vững quy trình đào tạo *(Base khảo thí, LMS AI)*.
  * `DT-07` (10% | 10đ): Tham gia đầy đủ các sự kiện của phòng và công ty *(Danh sách tham gia)*.
  * `DT-08` (5% | 5đ): Tuân thủ quy định đào tạo: Nộp báo cáo ngày đầy đủ, tham gia giao ban 100% *(Worklane, Biên bản đào tạo nội bộ)*.
* **3. Khảo sát Sinh viên (10%)**:
  * `DT-09` (5% | 5đ): Điểm hài lòng sinh viên (Student CSAT) *(Khảo sát tự động LMS AI)*.
  * `DT-10` (5% | 5đ): Tính tương tác & Truyền cảm hứng bài học *(LMS AI)*.
* **4. Cống hiến & Cải tiến (15%)**:
  * `DT-11` (5% | 5đ): Kèm cặp & Phụ đạo ngoài giờ cho SV yếu *(Log Support & Minh chứng)*.
  * `DT-12` (5% | 5đ): Đóng góp cải tiến chất lượng giảng dạy *(Hội đồng Chuyên môn phê duyệt)*.
  * `DT-13` (5% | 5đ): Tinh thần trách nhiệm & Hỗ trợ việc khẩn: Sẵn sàng nhận dạy thay, sự kiện, coi thi *(Trưởng ban QLĐT đánh giá)*.

---

### 2.2. Phòng Thiết kế Giải pháp LMS (LMS AI & Tech) — *9 Tiêu chí (100%)*
*(Đồng bộ theo Sheet `Tổng quan`)*

* **1. Tiến độ & Chất lượng task (50%)**:
  * `LMS-01` (25% | 10đ): Đảm bảo về tiến độ các task được giao trong Sprint / Roadmap *(Worklane / Jira)*.
  * `LMS-02` (15% | 10đ): Đảm bảo chất lượng các task bàn giao, không phát sinh lỗi sau release *(Hệ thống kiểm thử / Log lỗi)*.
  * `LMS-03` (10% | 10đ): Tốc độ xử lý các yêu cầu phát sinh khẩn cấp từ Ban Lãnh đạo & Khối Đào tạo *(Worklane / Biên bản yêu cầu)*.
* **2. Hệ thống Ổn định & An toàn (25%)**:
  * `LMS-04` (15% | 10đ): Đảm bảo hệ thống hoạt động ổn định, không gặp lỗi hay bị tấn công, Uptime $\ge 99.5\%$ *(Server Monitoring Log)*.
  * `LMS-05` (10% | 10đ): Tốc độ xử lý và khắc phục khi hệ thống gặp lỗi (SLA $< 1-2$h) *(Báo cáo sự cố kỹ thuật)*.
* **3. Khảo sát Người dùng (10%)**:
  * `LMS-06` (5% | 5đ): Khảo sát định kỳ từ sinh viên về trải nghiệm hệ thống LMS AI *(Khảo sát định kỳ của sinh viên)*.
  * `LMS-07` (5% | 5đ): Khảo sát định kỳ của các GV/TG về tính năng quản lý lớp học *(Khảo sát định kỳ của các GV/TG)*.
* **4. Cải tiến & Tối ưu hóa (15%)**:
  * `LMS-08` (10% | 10đ): Tối ưu hóa các quy trình để tăng hiệu suất cho các thầy/cô GV: Auto-grading, RPoint, Telemetry *(LMS AI)*.
  * `LMS-09` (5% | 5đ): Nghiên cứu và ứng dụng giải pháp công nghệ AI mới vào hệ thống *(Hội đồng Chuyên môn / BLĐ)*.

---

### 2.3. Ban QLĐT (QLĐT, CVHT, Khảo thí) — *10 Tiêu chí (100%)*
*(Đồng bộ theo Sheet `Tổng quan`)*

* **1. Giữ chân SV & Cảnh báo sớm (40%)**:
  * `QL-01` (15% | 10đ): Tăng tỷ lệ giữ chân sinh viên, giảm tỷ lệ bảo lưu, thôi học, bỏ học *(LMS AI & Báo cáo học vụ)*.
  * `QL-02` (15% | 10đ): Đưa ra hệ thống cảnh báo nguy cơ cho từng lớp, từng sinh viên (can thiệp 100% SV dải đỏ) *(LMS AI & Biên bản tư vấn)*.
  * `QL-03` (10% | 10đ): Hỗ trợ sinh viên nợ môn và giải quyết các trường hợp bảo lãnh học tập *(LMS AI & Danh sách mở lớp học lại)*.
* **2. Chuẩn xác Khảo thí & Thời khóa biểu (35%)**:
  * `QL-04` (15% | 10đ): Tối ưu hệ thống khảo thí và chuẩn xác quy trình xét duyệt thi, đối soát điểm 100% *(Base khảo thí & LMS AI)*.
  * `QL-05` (10% | 10đ): Chuẩn xác và tối ưu về thời khóa biểu giảng dạy, zero trùng lịch *(Thời khóa biểu thực tế)*.
  * `QL-06` (10% | 10đ): Chuẩn hóa lại toàn bộ quy trình đào tạo và kỷ luật báo cáo giao ban tuần *(Worklane & Biên bản đào tạo)*.
* **3. Khảo sát Hài lòng (10%)**:
  * `QL-07` (5% | 5đ): Mức độ hài lòng từ sinh viên đối với sự hỗ trợ của Ban QLĐT / CVHT *(Khảo sát định kỳ từ sinh viên)*.
  * `QL-08` (5% | 5đ): Mức độ hài lòng từ phụ huynh và giải quyết thủ tục hành chính học vụ *(Nhật ký liên hệ phụ huynh & Sổ tiếp nhận)*.
* **4. Phối hợp Liên phòng ban (15%)**:
  * `QL-09` (10% | 10đ): Phối hợp liên phòng ban đảm bảo tiến độ và chất lượng giữa Đào tạo - Tuyển sinh - OJT Doanh nghiệp - Kế toán *(Biên bản đào tạo nội bộ)*.
  * `QL-10` (5% | 5đ): Thích ứng và sẵn sàng trong mọi nhiệm vụ được giao từ phía đào tạo *(Trưởng ban QLĐT đánh giá)*.

---

## 3. Cơ Cấu Danh Hiệu Vinh Danh Khớp Chuẩn Sheet Tổng Quan

1. **Khối Đào tạo (Giảng viên & Trợ giảng) — Trọng tâm 20/11**:
   * 🏆 **Nhà giáo Cống hiến 20/11**
   * 🥈 **Giảng viên Truyền cảm hứng**
   * 🌟 **Trợ giảng Thắp lửa**
2. **Phòng Thiết kế giải pháp LMS**:
   * 🚀 **Kỹ sư Giải pháp Tiên phong**
   * 🛡️ **Chiến binh Vận hành Ổn định**
   * 💡 **Sáng kiến Công nghệ của năm**
3. **Ban QLĐT**:
   * 💼 **Ngôi sao Vận hành Học vụ**
   * 🤝 **Cố vấn Học tập Tận tâm**
   * 🎖️ **Cán bộ Khảo thí Chuẩn mực**
4. **Giải Toàn Viện (Grand Award)**:
   * 👑 **Gương mặt Xuất sắc Toàn viện (Grand Excellence Award)**

---

## 4. Danh Sách Sheet Chuẩn Trong Workbook Excel
File: `output/02_Thong_Ke_Dot_Xuat_Theo_Task/Excel_Xlsx/Bo_Tieu_Chi_Danh_Gia_Khen_Thuong_Khoi_Dao_Tao_LMS_QLDT_20261116.xlsx`

1. `Tổng quan` *(Giữ nguyên 100% bản người dùng đã sửa)*.
2. `Khối đào tạo` *(Giữ nguyên 100% bản người dùng đã sửa)*.
3. `Phòng LMS` *(Được làm lại chuẩn từ ngữ và tỷ trọng 50/25/10/15)*.
4. `Ban QLĐT` *(Được làm lại chuẩn từ ngữ và tỷ trọng 40/35/10/15)*.
5. `Cơ cấu danh hiệu` *(Khớp 100% tên danh hiệu tại Sheet Tổng quan)*.
6. `Mẫu Import LarkBase` *(Bảng phẳng 32 tiêu chí chuẩn hóa field types để import trực tiếp)*.
