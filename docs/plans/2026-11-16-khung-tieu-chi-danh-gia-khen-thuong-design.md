# Thiết Kế Hệ Thống Khung Tiêu Chí Đánh Giá & Khen Thưởng Nội Bộ
*Áp dụng cho: Khối Đào tạo (GV/TG), Phòng Thiết kế giải pháp LMS và Ban QLĐT (PTIT x Rikkei)*
*Dịp áp dụng: Lễ 20/11 và các kỳ vinh danh định kỳ (Quý / Năm học)*
*Cập nhật: Đồng nhất chuẩn 1-1 giữa Tỷ trọng (%) và Điểm tối đa (1% = 1 điểm). Tổng điểm toàn bảng của mọi khối đều đúng tròn 100 điểm.*

---

## 1. Nguyên Tắc Đồng Nhất Tuyệt Đối: 1% Tỷ Trọng = 1 Điểm Tối Đa

Toàn bộ hệ thống đánh giá của cả 3 đơn vị được đồng nhất theo cơ cấu **Tỷ trọng (%) bao nhiêu thì Điểm tối đa là bấy nhiêu điểm**:
1. **Trực quan, dễ hiểu**: Người chấm nhìn vào là biết ngay tiêu chí đó đóng góp bao nhiêu điểm vào tổng 100 điểm chung cuộc.
2. **Cộng thẳng (Additive Scoring)**: Không cần công thức nhân chia tỷ lệ phức tạp, người chấm chỉ cần cộng tổng điểm các tiêu chí là ra ngay Điểm Tổng kết trên thang 100.
3. **Chuẩn hóa thang đo theo bậc**:
   * Tiêu chí 20 điểm: `20đ - 16đ - 12đ - 8đ - 4đ`
   * Tiêu chí 15 điểm: `15đ - 12đ - 9đ - 6đ - 3đ`
   * Tiêu chí 10 điểm: `10đ - 8đ - 6đ - 4đ - 2đ` *(hoặc `10đ - 8đ - 5đ - 0đ` tùy tính chất vi phạm)*
   * Tiêu chí 5 điểm: `5đ - 4đ - 3đ - 2đ - 1đ` *(hoặc Feedback tốt: 5đ, Feedback tiêu cực: 0đ)*

---

## 2. Bảng Tiêu Chí Chi Tiết 3 Đơn Vị (Đều đúng 100 Điểm)

### 2.1. Khối Đào tạo (Giảng viên & Trợ giảng) — *13 Tiêu chí (100 Điểm)*

| Mã | Nhóm đánh giá | Tên tiêu chí đánh giá | Tỷ trọng | Điểm tối đa | Nguồn dữ liệu | Thang điểm chi tiết (Bậc điểm) |
| :---: | :--- | :--- | :---: | :---: | :--- | :--- |
| `DT-01` | 1. Hiệu quả Đào tạo (50%) | Tỷ lệ Chuyên cần sinh viên trung bình | 5% | **5đ** | LMS AI | • > 90%: 5đ • > 80%: 4đ • > 65%: 3đ • > 50%: 2đ • < 50%: 1đ |
| `DT-02` | 1. Hiệu quả Đào tạo (50%) | Tỷ lệ hoàn thành Bài tập về nhà (BTVN) | 5% | **5đ** | LMS AI | • > 90%: 5đ • > 80%: 4đ • > 65%: 3đ • > 50%: 2đ • < 50%: 1đ |
| `DT-03` | 1. Hiệu quả Đào tạo (50%) | Tỷ lệ hoàn thành eLearning đúng hạn | 5% | **5đ** | LMS AI | • > 90%: 5đ • > 80%: 4đ • > 65%: 3đ • > 50%: 2đ • < 50%: 1đ |
| `DT-04` | 1. Hiệu quả Đào tạo (50%) | Tỷ lệ SV Đủ điều kiện dự thi | 15% | **15đ** | LMS AI | • > 90%: 15đ • > 80%: 12đ • > 65%: 9đ • > 50%: 6đ • < 50%: 3đ |
| `DT-05` | 1. Hiệu quả Đào tạo (50%) | Tỷ lệ sinh viên qua môn | 20% | **20đ** | LMS AI sau thi | • > 90%: 20đ • > 80%: 16đ • > 65%: 12đ • > 50%: 8đ • < 50%: 4đ |
| `DT-06` | 2. Kỷ luật Vận hành (25%) | Nắm vững quy trình đào tạo | 10% | **10đ** | Base khảo thí, LMS | • Không vi phạm: 10đ • Vi phạm 1-2 lỗi: 8đ • 3-4 lỗi: 5đ • > 4 lỗi: 0đ |
| `DT-07` | 2. Kỷ luật Vận hành (25%) | Tham gia đầy đủ sự kiện phòng & cty | 10% | **10đ** | Danh sách tham gia | • Tham gia đầy đủ: 10đ • Có lý do: 7đ • Không lý do: 0đ |
| `DT-08` | 2. Kỷ luật Vận hành (25%) | Tuân thủ quy định đào tạo (báo cáo, giao ban) | 5% | **5đ** | Worklane, Biên bản | • Đầy đủ 100%: 5đ • Trễ 1-2 lần: 3đ • Quên > 2 lần: 0đ |
| `DT-09` | 3. Khảo sát Sinh viên (10%)| Điểm hài lòng sinh viên (Student CSAT) | 5% | **5đ** | LMS AI khảo sát | • Feedback tốt: 5đ • Feedback tiêu cực: 0đ |
| `DT-10` | 3. Khảo sát Sinh viên (10%)| Tính tương tác & Truyền cảm hứng bài học | 5% | **5đ** | LMS AI khảo sát | • Thang điểm 5 quy đổi (Điểm TB * 1.0) |
| `DT-11` | 4. Cống hiến & Cải tiến (15%)| Kèm cặp & Phụ đạo ngoài giờ cho SV yếu | 5% | **5đ** | Log Support | • Hoạt động hiệu quả cải thiện điểm: 5đ • Không có: 0đ |
| `DT-12` | 4. Cống hiến & Cải tiến (15%)| Đóng góp cải tiến chất lượng giảng dạy | 5% | **5đ** | HĐ Chuyên môn | • Đóng góp xuất sắc: 5đ • Đạt yêu cầu: 3đ • Không: 0đ |
| `DT-13` | 4. Cống hiến & Cải tiến (15%)| Tinh thần trách nhiệm & Hỗ trợ việc khẩn | 5% | **5đ** | Trưởng ban QLĐT | • Rất tích cực, xông xáo: 5đ • Hoàn thành: 3đ • Thụ động: 0đ |
| **TỔNG**| | **TỔNG CỘNG KHỐI ĐÀO TẠO** | **100%** | **100đ** | | |

---

### 2.2. Phòng Thiết kế Giải pháp LMS (LMS AI & Tech) — *9 Tiêu chí (100 Điểm)*

| Mã | Nhóm đánh giá | Tên tiêu chí đánh giá | Tỷ trọng | Điểm tối đa | Nguồn dữ liệu | Thang điểm chi tiết (Bậc điểm) |
| :---: | :--- | :--- | :---: | :---: | :--- | :--- |
| `LMS-01` | 1. Tiến độ & Chất lượng (50%) | Đảm bảo về tiến độ các task được giao | 25% | **25đ** | Worklane / Jira | • > 90%: 25đ • > 80%: 20đ • > 65%: 15đ • > 50%: 10đ • < 50%: 5đ |
| `LMS-02` | 1. Tiến độ & Chất lượng (50%) | Đảm bảo chất lượng task, không lỗi release | 15% | **15đ** | Log lỗi / QA test | • > 90%: 15đ • > 80%: 12đ • > 65%: 9đ • > 50%: 6đ • < 50%: 3đ |
| `LMS-03` | 1. Tiến độ & Chất lượng (50%) | Tốc độ xử lý yêu cầu phát sinh khẩn cấp | 10% | **10đ** | Worklane / Yêu cầu | • Hoàn thành 100% đúng hạn: 10đ • Trễ 1 lần: 7đ • Trễ > 1 lần: 2đ |
| `LMS-04` | 2. Hệ thống Ổn định (25%) | Hệ thống hoạt động ổn định, Uptime $\ge 99.5\%$ | 15% | **15đ** | Server Monitoring | • Uptime $\ge 99.5\%$: 15đ • 99.0-99.4%: 11đ • 98.0-98.9%: 7đ • Sập/lỗi thi: 0đ |
| `LMS-05` | 2. Hệ thống Ổn định (25%) | Tốc độ xử lý và khắc phục sự cố (SLA) | 10% | **10đ** | Báo cáo sự cố | • Khắc phục < 1h: 10đ • Dưới 2h: 7đ • Quá 2h: 2đ |
| `LMS-06` | 3. Khảo sát Người dùng (10%)| Khảo sát định kỳ từ sinh viên về LMS AI | 5% | **5đ** | Khảo sát sinh viên | • Feedback tốt: 5đ • Feedback tiêu cực: 0đ |
| `LMS-07` | 3. Khảo sát Người dùng (10%)| Khảo sát định kỳ của các GV/TG về LMS AI | 5% | **5đ** | Khảo sát GV/TG | • Thang điểm 5 quy đổi (Điểm TB * 1.0) |
| `LMS-08` | 4. Cải tiến & Tối ưu (15%) | Tối ưu hóa quy trình tăng hiệu suất cho GV | 10% | **10đ** | Hệ thống LMS AI | • Có tính năng mới hiệu quả: 10đ • Có cải tiến nhỏ: 6đ • Không: 0đ |
| `LMS-09` | 4. Cải tiến & Tối ưu (15%) | Nghiên cứu ứng dụng giải pháp công nghệ AI mới | 5% | **5đ** | HĐ Chuyên môn / BLĐ| • Sáng kiến xuất sắc: 5đ • Đạt yêu cầu: 3đ • Không: 0đ |
| **TỔNG**| | **TỔNG CỘNG PHÒNG LMS** | **100%** | **100đ** | | |

---

### 2.3. Ban QLĐT (QLĐT, CVHT, Khảo thí) — *10 Tiêu chí (100 Điểm)*

| Mã | Nhóm đánh giá | Tên tiêu chí đánh giá | Tỷ trọng | Điểm tối đa | Nguồn dữ liệu | Thang điểm chi tiết (Bậc điểm) |
| :---: | :--- | :--- | :---: | :---: | :--- | :--- |
| `QL-01` | 1. Giữ chân SV & Cảnh báo (40%) | Tăng tỷ lệ giữ chân SV, giảm bảo lưu/thôi học | 15% | **15đ** | LMS AI & Báo cáo HV | • > 95%: 15đ • > 90%: 12đ • > 85%: 9đ • > 80%: 6đ • < 80%: 3đ |
| `QL-02` | 1. Giữ chân SV & Cảnh báo (40%) | Hệ thống cảnh báo nguy cơ sớm từng lớp/SV | 15% | **15đ** | LMS AI & Biên bản | • Can thiệp 100% có biên bản: 15đ • 80-99%: 12đ • 65-79%: 9đ • < 65%: 3đ |
| `QL-03` | 1. Giữ chân SV & Cảnh báo (40%) | Hỗ trợ SV nợ môn & xử lý đơn bảo lãnh | 10% | **10đ** | LMS AI & Danh sách | • Xử lý kịp thời, chuẩn 100%: 10đ • 1 sai sót nhỏ: 7đ • Chậm/bỏ sót: 2đ |
| `QL-04` | 2. Chuẩn xác Khảo thí/TKB (35%)| Tối ưu hệ thống khảo thí & xét duyệt thi | 15% | **15đ** | Base khảo thí & LMS | • Chuẩn 100%: 15đ • Vi phạm 1 lỗi: 10đ • Vi phạm 2 lỗi: 5đ • Lỗi thi: 0đ |
| `QL-05` | 2. Chuẩn xác Khảo thí/TKB (35%)| Chuẩn xác và tối ưu về thời khóa biểu | 10% | **10đ** | Thời khóa biểu | • Đúng hạn, zero trùng lịch: 10đ • 1 lần chỉnh nhỏ: 7đ • Trùng lịch: 2đ |
| `QL-06` | 2. Chuẩn xác Khảo thí/TKB (35%)| Chuẩn hóa quy trình đào tạo & nộp báo cáo | 10% | **10đ** | Worklane & Biên bản | • Đúng hạn 100%: 10đ • Trễ 1-2 lần: 7đ • Trễ > 2 lần: 2đ |
| `QL-07` | 3. Khảo sát Hài lòng (10%) | Hài lòng từ sinh viên với Ban QLĐT / CVHT | 5% | **5đ** | Khảo sát sinh viên | • Feedback tốt: 5đ • Feedback tiêu cực: 0đ |
| `QL-08` | 3. Khảo sát Hài lòng (10%) | Hài lòng từ phụ huynh & thủ tục giấy tờ | 5% | **5đ** | Sổ theo dõi phụ huynh| • Hoàn thành tốt: 5đ • Có phản ánh chậm: 2đ • Bị khiếu nại: 0đ |
| `QL-09` | 4. Phối hợp Liên phòng (15%) | Phối hợp Đào tạo - Tuyển sinh - OJT - Kế toán | 10% | **10đ** | Biên bản đào tạo nội | • Phối hợp xuất sắc: 10đ • Đạt yêu cầu: 7đ • Chậm việc, ách tắc: 2đ |
| `QL-10` | 4. Phối hợp Liên phòng (15%) | Thích ứng & sẵn sàng nhận mọi nhiệm vụ | 5% | **5đ** | Trưởng ban QLĐT | • Rất tích cực, xông xáo: 5đ • Hoàn thành: 3đ • Thụ động: 0đ |
| **TỔNG**| | **TỔNG CỘNG BAN QLĐT** | **100%** | **100đ** | | |

---

## 3. Cơ Cấu Danh Hiệu Vinh Danh (Giữ nguyên vẹn 100%)
* **Khối Đào tạo (Trọng tâm 20/11)**: 🏆 *Nhà giáo Cống hiến 20/11*, 🥈 *Giảng viên Truyền cảm hứng*, 🌟 *Trợ giảng Thắp lửa*.
* **Phòng Thiết kế giải pháp LMS**: 🚀 *Kỹ sư Giải pháp Tiên phong*, 🛡️ *Chiến binh Vận hành Ổn định*, 💡 *Sáng kiến Công nghệ của năm*.
* **Ban QLĐT**: 💼 *Ngôi sao Vận hành Học vụ*, 🤝 *Cố vấn Học tập Tận tâm*, 🎖️ *Cán bộ Khảo thí Chuẩn mực*.
* **Giải Toàn Viện**: 👑 *Gương mặt Xuất sắc Toàn viện (Grand Excellence Award)*.
