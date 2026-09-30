# Super Memory - Quy Chuẩn Cốt Lõi & Kiến Trúc Dự Án PMO

> **Lưu ý**: Tài liệu này lưu trữ các quyết định thiết kế và quy chuẩn nghiệp vụ sống còn của hệ thống. Lịch sử chi tiết các phiên làm việc cũ được lưu trữ đầy đủ tại `docs/archive/historical_super_memory.md` và `docs/changelog_archive.md`.

---

## 1. Danh Mục 16 Lớp Học Chính Quy PTIT (Phạm Vi Chốt Chặn)
Hệ thống **chỉ duyệt đúng 16 lớp chính quy PTIT** hiện tại đang đào tạo, loại bỏ 100% lớp rác/ngoại ngữ/đình chỉ từ DB:
1. **Khóa KS24 CNTT (5 lớp - Môn `Microservices System Design` [IT-214])**:
   - `HN-K24-CNTT1` (Bùi Thanh Hải - GV R5)
   - `HN-K24-CNTT2` (Bùi Thanh Hải - GV R5)
   - `HN-K24-CNTT3` (Hồ Xuân Hùng - Leader R5)
   - `HN-K24-CNTT4` (Bùi Thanh Hải - GV R5)
   - `HCM-K24-CNTT1` (Nguyễn Bá Minh Đạo - Leader R5)
2. **Khóa KS25 CNTT (9 lớp - Môn `Phân tích & thiết kế hệ thống` [IT105-K25])**:
   - Hà Nội (5 lớp): `HN-K25-CNTT1`, `HN-K25-CNTT2`, `HN-K25-CNTT5` (GV Nguyễn Quảng An - R4); `HN-K25-CNTT3`, `HN-K25-CNTT4` (GV Phạm Tuấn Bình - R3).
   - TP. HCM (4 lớp): `HCM-K25-CNTT5`, `HCM-K25-CNTT7` (GV Nguyễn Đức Minh - R4); `HCM-K25-CNTT6`, `HCM-K25-CNTT8` (GV Trần Quốc Tuấn - R3).
3. **Khóa KS25 QTKD (2 lớp - Môn `Quản trị chiến lược doanh nghiệp` [MAN107])**:
   - `HN-K25-QTKD1` (46 SV), `HN-K25-QTKD2` (42 SV) do cô Đặng Quỳnh Trang (GV R3) phụ trách.

---

## 2. Quy Chuẩn Dự Báo Học Thuật & Chốt Chặn Cấm Thi (Agent 2)
- **Hệ số độ khó môn học (CDC)**: Microservices (1.45), PTTKHT (1.25), MAN107 (1.10).
- **Điểm Kỷ luật môn trước**: KS25 đọc `total_score` từ bảng `auto_rpoints`. KS24 đọc cột `rpoints` trong bảng `final_results`.
- **Chốt chặn cấm thi**: 
  - Chỉ áp dụng cấm thi theo kỷ luật môn hiện tại khi **số buổi học > 3**. Nếu $\le 3$ buổi, bỏ qua chốt chặn kỷ luật môn hiện tại để tránh cảnh báo ảo.
  - **Không chặn Project giữa kỳ**: Điểm Project là điểm thi cuối kỳ, không dùng làm điều kiện cấm thi giữa kỳ.
- **Hệ số nề nếp lớp học ($Multiplier_{env}$)**: Áp dụng khi tỷ lệ vi phạm trung bình của lớp $> 10\%$: $P_{final} = P_{eligible} \times Multiplier_{env}$.
- **Hiệu chuẩn (Calibration)**: Chuyên cần scale theo tỷ lệ vắng lớp trung bình; Bài tập đảo ngược tỷ lệ nợ thành tỷ lệ hoàn thành (`100.0 - bt_debt`); Elearning giữ nguyên số bài vi phạm tuyệt đối để xét cấm thi theo quy chế.

---

## 3. Bộ 3 Barem KPI Master & Quy Tắc Khai Báo Giờ Công
1. **Khối CNTT (Bản FINAL)** (`KPI_MASTER_Giang_vien_Tro_giang_FINAL.xlsx`):
   - Chuẩn hóa giảng dạy trực tiếp: **120 phút/buổi (2.0h)** cho Lý thuyết, Thực hành, Mini-project.
   - 18 Task Type Review độc lập (có checklist, biên bản góp ý, kết luận Đạt/Không đạt). Không nghiệm thu giờ sản xuất học liệu tự do ngoài barem.
   - Khảo thí khoán theo lớp: **120 phút/lớp** (không nhân theo số lượng SV).
2. **Khối QTKD (Draft T8/2026)** (`[QTKDS] KPI Master (Draft - 8_2026).xlsx`):
   - Giảng dạy lý thuyết/thực hành: **180 phút (3.0h)**.
   - Trợ giảng CVHT: Rank 1 chuẩn **90 phút (1.5h/ngày)**, Rank 2 chuẩn **120 phút (2.0h/ngày)**.
3. **Khối Ngoại ngữ** (`[ENG&JPN] KPI MASTER KHỐI ĐÀO TẠO NGOẠI NGỮ.xlsx`):
   - 118 định mức Rank 1-5, 270 mapping Worklane tasks.

---

## 4. Quy Tắc Kiểm Toán Task Quá Hạn & Đánh Giá Nhân Sự
- **Quy tắc vàng về lỗi task trễ hạn**:
  - Task trễ hạn **CHỈ tính lỗi cho nhân sự** khi task đang ở trạng thái **"Cần làm"** hoặc **"Đang làm"**.
  - Nếu task đang ở trạng thái **"Chờ duyệt"** (nhân sự đã làm xong, PIC/Leader chưa nghiệm thu) thì **HOÀN TOÀN MIỄN TRỪ LỖI** cho nhân sự.
- **Quy chuẩn giờ công tiêu chuẩn**: Quỹ làm việc 40h/tuần (8h/ngày). Tỷ lệ đạt công suất $(\%) = (\text{Giờ thực tế} / \text{Giờ tiêu chuẩn}) \times 100\%$.

---

## 5. Danh Mục 6 Khối & 6 Leader Chịu Trách Nhiệm
1. **Khối CNTT Hà Nội (12 NS)**: Leader Hồ Xuân Hùng (Rank 5).
2. **Khối QTKD (8 NS)**: Leader Hoàng Thị Kim Oanh (Rank 5).
3. **Khối Ngoại ngữ & KNM (3 NS)**: Leader Giáp Thị Minh Hằng (Rank 5).
4. **Khối QLCLĐT (3 NS)**: Leader Nguyễn Thị Tươi (Rank 4).
5. **Khối CNTT HCM (8 NS)**: Leader Nguyễn Bá Minh Đạo (Rank 5).
6. **Nhóm Dự án LMS AI (2 NS)**: Leader Trần Minh Cường (Rank 5).

---

## 6. Kiến Trúc Pipeline 1-Nguồn Chân Lý (Single Cache Architecture)
- **DataSanitizer** (`agents/common/data_sanitizer.py`): Đọc Excel một lần duy nhất, chuẩn hóa dữ liệu ngày và xuất toàn diện ra `data/processed/classes_metrics_cache.json`.
- **Nguyên tắc Fast-path**: Các Agent 1, 2, 3, 5 đọc dữ liệu trực tiếp từ file JSON cache, không đọc lại file Excel thô để duy trì thời gian thực thi toàn đường ống $< 20$ giây.
- **Auto-Watcher**: Dịch vụ giám sát `watch_and_sync.py` theo dõi `PTIT_Chiso.xlsx` và tự động kích hoạt `run_pipeline.py --fast` khi có thay đổi.

---

## 7. Chuẩn Dashboard Học Vụ Môn FastAPI KS25
- **Đường dẫn**: `output/dashboards/academic/bao_cao_chuyen_sau_fastapi_ks25.html` (chạy script `scripts/generate_academic_fastapi_dashboard.py`).
- **Nguyên tắc thiết kế**: Tuyệt đối hạn chế text dài, loại bỏ hoàn toàn từ ngữ AI-like; sử dụng ngôn ngữ quản lý đào tạo chuẩn mực; tập trung số liệu định lượng và 5 biểu đồ Chart.js trực quan (Phễu hao hụt, 3 môn tiên quyết, Radar ĐGNL, Hackathon 1 vs 2, Phân luồng cứu vãn 271 SV).
- **Điểm nghẽn cốt lõi**: 87/273 SV (31.9% số đủ điều kiện) bỏ thi vì bế tắc đồ án 5 ngày *Construction Site Management API* (30 task, RBAC/ABAC quá tải nhận thức). Tỷ lệ đỗ khi đi bảo vệ đạt 80.1% (TP.HCM đạt 90.6%). Quy chế mới chỉ cấm thi thêm 2 SV (-0.5%), không phải nguyên nhân tăng tỷ lệ trượt.

---

## 8. Mốc Kiểm Toán Worklane Chốt Ngày 18/09/2026 & Bóc Tách Vi Phạm KPI Master
- **Điều chỉnh Roster nhân sự (Chỉ đạo 19/09/2026)**:
  - **Bỏ khỏi danh sách từ ngày 15/09**: Đặng Minh Luân và Nguyễn Ngọc Sơn (Khối CNTT HCM) — không còn trong danh sách đánh giá từ 15/09.
  - **Bổ sung 3 nhân sự Khối Ngoại ngữ & KNM**:
    1. Đỗ Hà Khanh (Giảng viên R3, onboard từ 08/09/2026): Tuần W38 đạt 41.0h/40.0h (102.5% - Đạt chuẩn).
    2. Huỳnh Thị Kim Khánh (Giảng viên R3, onboard từ 15/09/2026): Tuần W38 đạt 31.0h/32.0h định mức làm việc thực tế 4 ngày (96.9%).
    3. Nguyễn Hồng Nhung (Giảng viên R3, onboard từ 18/09/2026): Ngày 18/09 đạt 8.0h/8.0h định mức làm việc thực tế 1 ngày (100.0%).
- **Phạm vi kiểm toán & Quy mô**: 42 nhân sự đang hoạt động.
- **Kết quả kiểm toán Tuần W38 (14/09 - 18/09/2026)**:
  - 14/42 nhân sự (33.3%) hoàn thành/vượt định mức giờ công: Nguyễn Công Hưởng (45.0h), Hoàng Thị Kim Oanh (44.5h), Hoàng Thị Hậu (41.0h), Lâm Tùng Dương (41.0h), Lại Trung Lâm (41.0h), Đỗ Hà Khanh (41.0h), Phạm Ngọc Kiên (40.5h), Nguyễn Ngọc Vân Khanh (40.0h), Nguyễn Thị Hồng Minh (40.0h), Nguyễn Thị Như Quỳnh (40.0h), Phạm Tuấn Bình (40.0h), Nguyễn Quảng An (40.0h), Lê Thị Đỏ (40.0h), Trần Thị Mỹ Phước (40.0h).
  - 28/42 nhân sự còn lại có số giờ công chưa đạt 40.0h/tuần (trong đó cô Nguyễn Hồng Nhung đạt 100% định mức 8h cho 1 ngày công thực tế, cô Huỳnh Thị Kim Khánh đạt 96.9% định mức 32h cho 4 ngày công thực tế).
  - Nhóm vi phạm bỏ trống 100% báo cáo (0.0h/40h): Trần Minh Cường, Hồ Xuân Hùng, Nguyễn Bá Minh Đạo, Ngô Quang Huấn.
- **Bóc tách nhân sự khai báo ngoài KPI Master (Wildcard / Ngoài Barem)**:
  - 38/42 nhân sự có khai báo task ngoài barem KPI Master với tổng cộng 869 task và 1,514.8 giờ tự do.
  - Các dạng vi phạm phổ biến:
    1. *Tự ý nghiên cứu / tự học*: Khai 3h - 6h/ngày đọc tài liệu, tìm hiểu môn mới mà không có đầu ra/nghiệm thu.
    2. *Sản xuất học liệu tự do ngoài barem*: Viết slide, quiz, mindmap ngoài 18 task chuẩn của CNTT hoặc chưa được phân công.
    3. *Khai báo chung chung / hành chính*: Khai "chăm sóc sinh viên", "hỗ trợ sinh viên", "phản hồi thông tin" không gắn mã ticket hoặc không theo định mức CVHT khoán.

---

## 9. Nâng Cấp Báo Cáo Kiểm Toán Nhân Sự Worklane Đa Kỳ (worklane_staff_audit.html)
- **Đường dẫn**: [output/dashboards/audit/worklane_staff_audit.html](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/output/dashboards/audit/worklane_staff_audit.html)
- **Kiến trúc Đa Kỳ (3 Period Modes)**:
  1. `week_14_18` (Mặc định khi mở): **Tuần qua 14/09 - 18/09/2026 (5 ngày làm việc)** — Chuyên biệt đo hiệu suất chuẩn 40h/tuần cho 42 nhân sự.
  2. `sept_01_08`: **Lũy kế Tháng 9 (01/09 - 18/09/2026 - 12 ngày làm việc)**.
  3. `august`: **Tháng 08/2026 (20 ngày làm việc - Lịch sử đối chuẩn)**.
- **Tính năng mới**:
  - Tích hợp đo chuẩn 40h/tuần: Hiển thị cột *Giờ Khai / Chuẩn* kèm tiến độ % (ví dụ: `40.0h / 40h (100%)`).
  - Badge phân loại trực quan: `🔴 Chưa đạt 40h/tuần (Thiếu -...h)`, `⚫ Bỏ trống báo cáo (0%)`, `🟡 Cần rà soát hạ Rank`, `🟠 Cắt giảm giờ ảo / Ngoài barem`, `🟢 Chuẩn mực (≥40h)`.
  - Bộ lọc Đề xuất tích hợp trực tiếp lọc nhanh danh sách nhân sự thiếu giờ 40h và nhân sự khai ngoài barem.
  - Ma trận Công suất (Capacity Matrix) và Biểu đồ Chart.js tự động đồng bộ theo 42 nhân sự và 6 Khối.
  - Slide-over Drawer mở nhanh thông tin chi tiết từng cá nhân và tính năng *Sao chép Phiếu làm việc 1-1* cho lãnh đạo.
- **Kiểm thử**: Đã chạy Visual QA bằng `browser_subagent` đạt 100% tiêu chí, 0 lỗi JavaScript.

---

## 10. Đồng Bộ Dữ Liệu Học Vụ Mới Nhất Ngày 21/09/2026 (PTIT_Chiso.xlsx)
- **Nguồn dữ liệu**: `C:\Users\DELL\Desktop\Backup\PTIT\PTIT_Chiso.xlsx` (Cập nhật ngày 21/09/2026).
- **Phạm vi cập nhật**: Đã tích hợp cột dữ liệu ngày học mới nhất **21/09/2026** cho cả 3 môn học hiện tại của 16 lớp chính quy:
  1. `KS24_AI_Microservice`: Cột ngày 21/09/2026 (HN-K24-CNTT1, HN-K24-CNTT2, HN-K24-CNTT3, HN-K24-CNTT4, HCM-K24-CNTT1).
  2. `KS25_Phantichthietkehethong`: Cột ngày 21/09/2026 (5 lớp Hà Nội + 4 lớp TP.HCM).
  3. `KS25_QTKD_MAN107`: Cột ngày 21/09/2026 (HN-K25-QTKD1, HN-K25-QTKD2).
- **Cảnh báo học vụ ngày 21/09/2026**:
  - Khối QTKD (MAN107): Tỷ lệ vắng chuyên cần tăng đột biến ở mức nguy cơ cao: Lớp QTKD1 vắng **43.48%** (20/46 SV), QTKD2 vắng **28.57%** (12/42 SV), vi phạm Elearning lớp QTKD2 tăng lên **26.19%**.
  - Khối KS25 CNTT: Xuất hiện biến động vắng tại lớp HCM-K25-CNTT7 (vắng **29.55%**), HN-K25-CNTT1 (vắng **13.16%**).
  - Khối KS24 CNTT: Duy trì ổn định, lớp HCM-K24-CNTT1 vắng **16.28%**, HN-K24-CNTT3 vắng **15.38%**.
- **Tình trạng pipeline**: Toàn bộ hệ thống pipeline (DataSanitizer, Agent 1 -> Agent 5, Director Cockpit, QLDT Report, HCM Report) đã được chạy lại và đồng bộ hoàn tất 100%. Đã kiểm thử Visual QA bằng Browser Subagent đạt chuẩn.

---

## 11. Báo Cáo Chuyên Sâu Lớp Điểm HN-KS24-CNTT2 (bao_cao_chi_so_HN_KS24_CNTT2.html)
- **Đường dẫn**: [output/dashboards/academic/bao_cao_chi_so_HN_KS24_CNTT2.html](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/output/dashboards/academic/bao_cao_chi_so_HN_KS24_CNTT2.html)
- **Đặc điểm học vụ lớp HN-KS24-CNTT2 (Môn Microservices [IT-214] - GV Bùi Thanh Hải)**:
  - **Lớp học xuất sắc số 1 khóa KS24**: Giữ vững 100% sĩ số (39/39 SV, 0 hao hụt).
  - **Tỷ lệ vi phạm nề nếp kỷ lục**: Đạt **3.56%** (thấp nhất toàn viện), vắng chuyên cần chỉ **1.79%** (chỉ 1 SV vắng/buổi có phép), nợ BT < 3.8%. Hệ số phạt môi trường $Mult_{env} = 1.000$ (không bị phạt).
  - **Dự báo đỗ dẫn đầu**: Đạt **59.63%** (cao nhất 5 lớp KS24). Tỷ lệ đỗ thực tế môn tiên quyết IT-213 đạt **71.79%** (28/39 SV đỗ).
  - **Tỷ lệ cấm thi 0%**: Toàn bộ 39 SV đủ điều kiện dự thi. Danh sách Care List chỉ có 7 SV (17.9% sĩ số) thuộc nhóm GREEN (cần bồi dưỡng kiến thức thực chiến Hackathon bù đắp độ vênh bài tập về nhà).
- **Kiểm thử VisualQA**: Đã kiểm thử tự động bằng `browser_subagent` đạt 100% tiêu chí qua 5 tab, 0 lỗi console JavaScript.

---

## 12. Cập Nhật Báo Cáo Agent 1 (Bổ sung Khóa KS26 Kỹ năng mềm) & Agent 4 (Worklane đến hết 21/09/2026)
- **Agent 1 (Bổ sung Khóa KS26 - Môn Kỹ năng mềm học tập chủ động)**:
  - **Nguồn dữ liệu**: `C:\Users\DELL\Desktop\Backup\PTIT\PTIT_Chiso.xlsx` (Sheet `KS26_SKL_Chudong`).
  - **Quy mô**: 9 lớp hoạt động với ngày bắt đầu học 22/09/2026:
    - Hà Nội (6 lớp): `HN-K26-CNTT1` (40 SV - GV Trần Minh Cường), `HN-K26-CNTT2` (42 SV - GV Hồ Xuân Hùng), `HN-K26-CNTT3` (41 SV - GV Nguyễn Duy Quang), `HN-K26-QTKD1` (44 SV - GV Hoàng Thị Hậu), `HN-K26-QTKD2` (44 SV - GV Hoàng Thị Kim Oanh), `HN-K26-QTKD3` (44 SV - GV Hoàng Thị Hậu).
    - TP. HCM (3 lớp): `HCM-K26-CNTT1` (47 SV - GV Nguyễn Bá Minh Đạo), `HCM-K26-CNTT2` (45 SV - GV Nguyễn Bá Minh Đạo), `HCM-K26-QTKD1` (23 SV - GV Lê Nhựt Mi).
  - **Đầu ra**: Xuất thành công báo cáo Markdown tại [agent_1_student_discipline.md](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/output/reports/core/agent_1_student_discipline.md) và Dashboard HTML tại [agent_1_student_discipline.html](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/output/dashboards/core/agent_1_student_discipline.html).
- **Agent 4 (Dữ liệu Worklane tính đến hết ngày 21/09/2026)**:
  - **Chốt kiểm toán**: Ngày 21/09/2026. Lũy kế Tháng 9: 13 ngày làm việc (104h chuẩn).
  - **Tình trạng nộp ngày 21/09/2026**: 35/42 nhân sự đã nộp (83.3%), 7 nhân sự vắng báo cáo (Trần Minh Cường, Hồ Xuân Hùng, Nguyễn Bá Minh Đạo, Ngô Quang Huấn, Lê Thị Đỏ, Nguyễn Thị Tươi, Nguyễn Huyền Trang).
  - **Tỷ lệ nộp Tháng 9 theo Khối**: QTKD (92.3%), CNTT (79.4%), Ngoại ngữ & KNM (76.8%), QLCLĐT (76.9%). Toàn viện: 82.1%.
  - **Đầu ra**: Xuất thành công báo cáo Markdown tại [agent_4_daily_logs.md](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/output/reports/core/agent_4_daily_logs.md), Dashboard HTML tại [agent_4_daily_logs.html](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/output/dashboards/core/agent_4_daily_logs.html) và bảng kiểm toán nhân sự [worklane_staff_audit.html](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/output/dashboards/audit/worklane_staff_audit.html).

---

## 13. Đồng Bộ Dữ Liệu Học Vụ Mới Nhất Ngày 23/09/2026 (PTIT_Chiso.xlsx)
- **Nguồn dữ liệu**: `C:\Users\DELL\Desktop\Backup\PTIT\PTIT_Chiso.xlsx` (Cập nhật ngày 23/09/2026).
- **Phạm vi cập nhật**: Đã tích hợp cột dữ liệu ngày học mới nhất **22/09/2026** và **23/09/2026** cho cả 4 khối/môn học:
  1. `KS24_AI_Microservice`: Cột ngày 22/09 và 23/09 (5 lớp: HN1, HN2, HN3, HN4, HCM1).
  2. `KS25_Phantichthietkehethong`: Cột ngày 22/09 và 23/09 (5 lớp Hà Nội + 4 lớp TP. HCM).
  3. `KS25_QTKD_MAN107`: Cột ngày 22/09 và 23/09 (HN-K25-QTKD1, HN-K25-QTKD2).
  4. `KS26_SKL_Chudong`: Cột ngày 22/09 và cột buổi 2 ngày 23/09 (đã xử lý khử lỗi gõ nhầm năm `22/09/2027` ➔ `2026-09-23` tại `data_sanitizer.py`, `calculate_kpi_json.py`, `generate_kpi_report.py`).
- **Chuẩn hóa cấu hình Master Portal**: Cập nhật `active_classes_config` trong `generate_unified_dashboard.py` tương thích tuyệt đối với 16 lớp chính quy và môn học kỳ hiện tại (`KS24_AI_Microservice`, `KS25_Phantichthietkehethong`, `KS25_QTKD_MAN107`), loại bỏ text cảnh báo tĩnh "đầu môn mới".
- **Cảnh báo học vụ trọng tâm ngày 23/09/2026**:
  - **Khối QTKD (MAN107)**: Tỷ lệ vắng chuyên cần tiếp tục ở mức báo động rất cao: QTKD1 vắng **52.17%** (24/46 SV), QTKD2 vắng **33.33%** (14/42 SV), vi phạm Elearning QTKD2 ở mức **26.19%**.
  - **Khối KS25 CNTT**: HCM-K25-CNTT8 tăng vọt vắng **37.50%** (nợ BT 15.63%, EL 31.25%); HCM-K25-CNTT7 vắng **32.61%**; HN-K25-CNTT1 vắng **23.68%**; HN-K25-CNTT5 vắng **15.56%**.
  - **Khối KS24 CNTT**: HN-K24-CNTT3 tăng vọt tỷ lệ vắng lên **23.08%** (9/39 SV); HCM-K24-CNTT1 duy trì vắng **16.28%**; lớp HN-K24-CNTT2 tiếp tục giữ kỷ luật tốt nhất (vắng chỉ 5.13%).
  - **Khối KS26 Kỹ năng mềm**: Buổi 2 ghi nhận HN-KS26-CNTT1 vắng **42.50%** (EL 60.00%); HN-K26-CNTT3 vắng **39.02%**; HN-K26-QTKD2 EL vi phạm **61.38%**.
- **Tình trạng pipeline**: Toàn bộ hệ thống pipeline (`run_pipeline.py --with-advanced`) đã thực thi hoàn tất trong 42.74s: toàn bộ cache, reports Markdown (`report_kpi_gv_tg.md`, `agent_1_student_discipline.md`, `agent_4_daily_logs.md`, `director_cockpit.md`, `qldt_monthly_report.md`) và Dashboards HTML (`agent_5_master_portal.html`, `agent_1_student_discipline.html`, `agent_2_academic_prediction.html`, `director_cockpit.html`, `qldt_monthly_report.html`, `Bao_Cao_Tong_Hop_HCM.html`) đã được đồng bộ chuẩn xác 100%.

---

## 14. Tích Hợp LMS MCP API & Chỉ Số Học Tập Khóa KS26 (24/09/2026)
- **Cấu hình MCP Server**:
  - `lms`: `https://lmsapi.rikkeiedu.com/v1/mcp`
  - `lms-analytics`: `https://lmsapi.rikkeiedu.com/v1/mcp/analytics`
  - Giao thức: JSON-RPC 2.0 over HTTP POST với Bearer Token. Yêu cầu header `Accept: application/json, text/event-stream`.
- **Phạm vi dữ liệu Khóa KS26**:
  - Gồm 10 lớp học: 6 lớp CNTT (`HN-KS26-CNTT1` đến `4`, `HCM-KS26-CNTT1` đến `2`) và 4 lớp QTKD (`HN-K26-QTKD1` đến `3`, `HCM-K26-QTKD1`).
  - Môn học đang diễn ra tích cực: `SSK101` (*Kỹ năng Học tập chủ động & Phát triển bản thân*). Riêng lớp `HN-KS26-CNTT4` mới khởi tạo, chuẩn bị vào môn.
  - Các công cụ MCP đã khai thác: `lms_find_classes`, `lms_list_course_classes`, `lms_course_class_statistics`, `lms_attendance_by_class`, `lms_homework_completion_by_class`, `lms_academic_warnings`.
- **Tổng quan học vụ KS26 ghi nhận từ LMS MCP**:
  - Khối QTKD đạt tỷ lệ hoàn thành BTVN vượt trội: HCM-K26-QTKD1 (92.8%), HN-K26-QTKD1 (91.7%), HN-K26-QTKD3 (84.1%).
  - Khối CNTT có tỷ lệ hoàn thành BTVN thấp (0% - 25%), cần đôn đốc nộp và chấm bài (đặc biệt lớp HN2 do thầy Hùng phụ trách chưa ghi nhận bài chấm).
  - Điểm nóng vắng chuyên cần: `HCM-KS26-CNTT1` vắng cao nhất (18.3%, 43/236 lượt), `HN-K26-QTKD3` vắng 12.7%. Các lớp còn lại duy trì nề nếp tốt (2.4% - 7.8%).
- **Đồng bộ ngày học 24/09/2026**:
  - **KS24**: Đã tích hợp chỉ số mới ngày 24/09 từ `PTIT_Chiso.xlsx` (HN-K24-CNTT1 vắng 12.90%, HN2 vắng 7.69%, HN3 vắng 25.64%, HN4 vắng 9.68%, HCM1 vắng 16.28%).
  - **KS25**: Giữ nguyên chỉ số ngày 23/09 do ngày 24/09 sinh viên thi Hackathon theo quy định.
  - **KS26 (Chuẩn hóa công thức PMO)**:
    - *Chuyên cần*: Tỉ lệ SV vi phạm chuyên cần (nghỉ học hoặc đi muộn từ 10% / `absent + late > 0`). Ví dụ: `HN-KS26-CNTT1` đạt đúng **50.0%** (20/40 SV).
    - *Bài tập về nhà*: Tỉ lệ SV thiếu BTVN từ 10% (chưa nộp hoặc chưa đạt BTVN / `notSubmitted + notCompleted > 0`). Ví dụ: `HN-KS26-CNTT1` đạt đúng **15.0%** (6/40 SV).
    - *Elearning*: Tỉ lệ SV vi phạm không chuẩn bị bài (`Elearning rate < 100%`). Ví dụ: `HN-KS26-CNTT1` đạt đúng **60.0%** (24/40 SV).
    - Đã ghi dữ liệu chuẩn xác vào file `C:\Users\DELL\Desktop\Backup\PTIT\PTIT_Chiso.xlsx` (sheet `KS26_SKL_Chudong`, cột 29-31).
  - **Agent 1**: Đã cập nhật thành công cả Báo cáo Markdown `output/reports/core/agent_1_student_discipline.md` và Dashboard HTML `output/dashboards/core/agent_1_student_discipline.html` (đồng bộ cả `deploy_web/`).
  - **Tối ưu luồng xử lý siêu tốc**: Đã xây dựng pipeline `scripts/fast_sync_ks26_agent1.py` gom 4 bước tự động hóa (LMS fetch -> Excel write -> Cache rebuild -> Agent 1 render) hoàn tất trong **45 giây** (thay vì 10-15 phút).

---

## 15. Quy Hoạch Toàn Diện Cấu Trúc Báo Cáo & Tối Ưu Pipeline Đào Tạo (25/09/2026)
- **Quy hoạch chuẩn hóa thư mục Báo cáo & Dashboard (`output/dashboards/`)**:
  1. `output/dashboards/core/`: Lưu trữ 5 dashboard trụ cột vận hành (Agent 1 đến Agent 5):
     - `agent_1_student_discipline.html` (Kỷ luật SV)
     - `agent_2_academic_prediction.html` (Dự báo học vụ & Care List)
     - `agent_3_ops_discipline.html` (Kỷ luật tác nghiệp GV/TG)
     - `agent_4_daily_logs.html` (Nhật ký công việc)
     - `agent_5_master_portal.html` (Executive Master Lead Portal)
  2. `output/dashboards/management/`: Gom toàn bộ báo cáo quản trị và kiểm toán nhân sự về một mối:
     - `director_cockpit.html` (Báo cáo Giám đốc Đào tạo / BOD)
     - `worklane_staff_audit.html` (Kiểm toán Nhân sự Worklane Đa Kỳ)
  3. `output/dashboards/academic/`: Quy hoạch phân tách thành 3 khối khóa đào tạo (`ks24/`, `ks25/`, `ks26/`), có cổng trung tâm `index.html`:
     - `index.html`: Cổng điều hướng tổng quan học vụ toàn viện.
     - `ks24/it214_microservices_cntt.html`: Môn *Microservices System Design* [IT-214] (5 lớp CNTT: độ khó CDC 1.45, độ vênh Hackathon, phân luồng cứu vãn 69 SV).
     - `ks25/it105_fastapi_cntt.html`: Môn *FastAPI / PTTKHT* [IT105-K25] (9 lớp CNTT: phễu hao hụt đồ án 5 ngày, 87/273 SV bỏ thi, cứu vãn 271 SV).
     - `ks25/man107_qtkd.html`: Môn *Quản trị chiến lược* [MAN107] (2 lớp QTKD: điểm nóng vắng chuyên cần 52.17% & 33.33%, nợ Elearning 26.19%).
     - `ks26/ssk101_cntt.html`: Môn *Kỹ năng Học tập chủ động* [SSK101] (6 lớp CNTT: nợ BTVN 0-25%, điểm nóng HCM1 44.7% trượt & HN1 37.2% trượt, danh sách bảo lãnh).
     - `ks26/ssk101_qtkd.html`: Môn *Kỹ năng Học tập chủ động* [SSK101] (4 lớp QTKD: BTVN >84% nhưng vắng CC 12.7% và EL 61.38%, đối chuẩn lớp kiểu mẫu HCM1 và danh sách bảo lãnh).
     - Tích hợp thanh Top Navbar điều hướng liên kết tức thì giữa tất cả các môn/khóa và Master Portal/Director Cockpit.
- **Dọn dẹp triệt để file dư thừa**:
  - Đã xóa `danh_gia_nhan_su.html` (root), `Bao_Cao_Tong_Hop_HCM.html`, `qldt_monthly_report.html`, `danh_gia_nhan_su_truc_quan.html`, `bao_cao_chi_so_HN_KS24_CNTT2.html`.
  - Đã xóa 2 folder cũ `output/dashboards/advanced/` và `output/dashboards/audit/`.
  - Đã di chuyển toàn bộ script nháp sang `scratch/archive/`.
- **Tối ưu quy trình cập nhật khi có dữ liệu mới**:
  - File điều phối `run_pipeline.py` đã được nâng cấp toàn diện: tự động làm sạch cache -> chạy song song 2 nhánh A (Học thuật) và B (Tác nghiệp) -> render Master Portal -> render Management Dashboards -> render Academic Cohort Issues (5 báo cáo trong 3 folder) -> đồng bộ sang `deploy_web/`.
  - File thực thi 1-click: `Cap_Nhat_Bao_Cao.bat` đặt tại thư mục gốc, chỉ cần double click là toàn bộ hệ thống được làm mới hoàn tất.
  - Tích hợp dịch vụ ngầm `watch_and_sync.py`: tự động kích hoạt pipeline khi file `PTIT_Chiso.xlsx` được lưu.

---

## 16. Kiểm Toán Toàn Diện Tuần 21/09 - 25/09/2026 & Chỉ Số KS26 Theo Chỉ Đạo Giám Đốc Đào Tạo
- **Đồng bộ dữ liệu thời gian thực (26/09/2026)**:
  - `PTIT_Chiso.xlsx`: Tích hợp đầy đủ dữ liệu đến ngày 25/09/2026 cho 16 lớp chính quy.
  - Worklane Daily Reports: Nạp đủ 77 ngày làm việc (bổ sung 22, 23, 24, 25/09 với 130 báo cáo).
  - LMS MCP Analytics: Nạp dữ liệu học tập chi tiết 371 sinh viên môn SSK101 khóa KS26.
- **Kết quả Kiểm toán Giờ công Tuần 21/09 - 25/09/2026 (40h/tuần - 42 NS)**:
  - **26/42 NS (61.9%) chưa đạt 40h/tuần**:
    - Nhóm bỏ trống 100% (0.0h/40h - 0/5 ngày): Hồ Xuân Hùng, Nguyễn Bá Minh Đạo, Trần Minh Cường, Ngô Quang Huấn, Lê Thị Đỏ, Nguyễn Thị Tươi, Nguyễn Huyền Trang.
    - Nhóm thiếu nặng (<30h/40h): Đinh Thành Nam (13.0h), Phạm Ngọc Kiên (15.0h), Phạm Tuấn Bình (24.0h), Nguyễn Xuân Bách (25.5h), Bùi Thanh Hải (28.0h), Ngọ Văn Quý (29.0h).
    - Nhóm thiếu vừa & tiệm cận (32.0h - 39.5h): 13 nhân sự.
    - 16 nhân sự còn lại đạt chuẩn/vượt định mức 40h - 45h/tuần (dẫn đầu: Nguyễn Công Hưởng 45.0h, Hoàng Thị Hậu 42.0h, Đỗ Hà Khanh 41.0h, v.v.).
  - **34/42 NS khai sai/ngoài KPI Master**: Phát hiện phổ biến 3 dạng: Tự học/R&D không nghiệm thu, Sản xuất học liệu ngoài 18 task chuẩn CNTT, Khai báo CSSV/hành chính chung chung vượt barem CVHT khoán.
- **Học vụ Khóa KS26 (Môn Kỹ năng Học tập chủ động SSK101)**:
  - **Tỷ lệ đủ điều kiện thi & Bảo lãnh**:
    - Khối CNTT: 6 lớp (241 SV) có 155 SV đủ điều kiện thi trực tiếp (64.3%), 31 SV được giáo viên đề xuất/làm đơn bảo lãnh (12.9%), nâng tổng số đủ điều kiện sau bảo lãnh lên **186/241 SV (77.2%)**.
    - Khối QTKD: 4 lớp (155 SV) có 128 SV đủ điều kiện thi trực tiếp (82.6%), 6 SV được đề xuất/làm đơn bảo lãnh (3.9%), nâng tổng số đủ điều kiện sau bảo lãnh lên **134/155 SV (86.5%)**.
  - **Phân nhóm 4 dải vi phạm học tập tuần đầu tiên (371 SV)**:
    - *Chuyên cần vi phạm*: [20-40%): 31 SV; [40-60%): 16 SV; [60-80%): 10 SV; [80-100%): 13 SV.
    - *Elearning vi phạm/chưa chuẩn bị*: [20-40%): 93 SV; [40-60%): 9 SV; [60-80%): 44 SV; [80-100%): 30 SV (Điểm nóng: HCM1 95.7%, HCM2 91.1%).
    - *Bài tập về nhà thiếu/nợ*: [20-40%): 27 SV; [40-60%): 0 SV; [60-80%): 88 SV; [80-100%): 143 SV (Điểm nghẽn: HN3 100% nợ bài).

---

## 17. Form Chuẩn Báo Cáo Giao Ban Tuần Cho Giám Đốc Đào Tạo (`weekly_director_report.html`)
- **Tập tin Dashboard Executive độc lập**:
  - `output/dashboards/management/weekly_director_report.html` (Đồng bộ sang `deploy_web/weekly_director_report.html`).
  - Tích hợp 3 Tab hoàn chỉnh:
    1. **Tab 1 (Học vụ & Kỷ luật KS24, KS25 CNTT, KS25 QTKD, KS26)**: Đánh giá so với tuần trước, Điểm nóng & Giải pháp, Bảng chuẩn định dạng Agent 1 (Chuyên cần, Bài tập, Elearning kèm delta ▲ / ▼ / -- và Badge xu hướng). Đã bỏ hoàn toàn cột "Trợ giảng" ở tất cả các bảng để khớp với dữ liệu nguồn Excel.
    2. **Tab 2 (Kiểm toán Báo cáo ngày Worklane)**:
       - Hiệu suất 6 phòng ban (Đạt giờ %, Đạt KPI Master %, Thiếu hụt).
       - Danh sách **chính xác 17 nhân sự thiếu 40h/tuần** sau khi **bỏ qua toàn bộ Leader, Thầy Ngô Quang Huấn, Cô Lê Thị Đỏ, Thầy Đinh Thành Nam**.
       - Bóc tách chi tiết các công việc chung chung: Ngày khai, tên việc nguyên văn, số giờ và lý do chưa đạt chuẩn.
    3. **Tab 3 (Chuyên đề KS26 & Đối Soát 9 Đơn Bảo Lãnh LMS)**:
       - Đối soát chuẩn xác 100% với màn hình LMS Admin (`https://lms-admin.rikkei.edu.vn/exam-guarantees` chốt 25/09/2026): **Tổng cộng 9 đơn bảo lãnh, 100% ở trạng thái CHỜ DUYỆT (Đã duyệt: 0, Từ chối: 0)**:
         1. Vương Thị Thơ (`B26DTQT086` - HN-K26-QTKD3 - GV Hoàng Thị Hậu)
         2. Nguyễn Gia Hân (`B26DTQT030` - HN-K26-QTKD1 - GV Hoàng Thị Hậu)
         3. Thân Hoàng Linh (`B26DTQT049` - HN-K26-QTKD1 - GV Hoàng Thị Hậu)
         4. Trần Đức Hùng (`B26DTQT038` - HN-K26-QTKD1 - GV Hoàng Thị Hậu)
         5. Nguyễn Đức Gia Huy (`B26DTCN137` - HN-KS26-CNTT2 - GV Hồ Xuân Hùng)
         6. Cao Bảo Lâm (`B26DTCN092` - HN-KS26-CNTT2 - GV Hồ Xuân Hùng)
         7. Nguyễn Ngọc Lan Anh (`B26DTQT003` - HCM-KS26-QTKD1 - GV Lê Nhựt Mi)
         8. Trần Minh Tiến 2 (`B26DTCN163` - HN-KS26-CNTT2 - GV Hồ Xuân Hùng)
         9. Nguyễn Tiến Dũng 11 (`e4bd96` - HN-KS26-CNTT3 - GV Nguyễn Duy Quang)
       - Công thức quản trị: `Không đủ điều kiện = Tổng SV - Đủ điều kiện`. Phân luồng rõ nhóm cần/có thể bảo lãnh bổ sung (102 SV CC >= 60%) và nhóm vi phạm nặng (19 SV vắng CC > 40%).
       - Ma trận phân nhóm 374 SV theo 4 dải vi phạm [20-40%), [40-60%), [60-80%), [80-100%].
       - Đã xuất file Excel đa sheet (1 sheet tổng hợp + 9 sheet lớp) tại `output/reports/K26_Danh_Sach_Sinh_Vien_Va_Phan_Nhom.xlsx`.
  - Tích hợp nút 1-Click: **"Sao chép Tóm tắt Giao ban (Zalo/Slack)"** chuẩn văn bản điều hành.
  - Tích hợp nút: **"Phóng To Chụp Ảnh"** (`toggleScreenshotMode`) tự động tăng cỡ chữ và khoảng đệm để chụp ảnh màn hình gửi Zalo/Slack không bị nhỏ.

---

## 18. Quy Chuẩn Hiển Thị Chỉ Số Học Vụ Khóa Mới Theo Chuẩn LMS Frontend (Bắt Buộc Duy Trì Lâu Dài)
- **Quy tắc Chuyên cần (Attendance)**:
  - Backend lưu: `presenceRate` (% đi học, ví dụ 100%).
  - Frontend LMS hiển thị: **Vi phạm chuyên cần (%)** = `100% - presenceRate` (hoặc `absence.rate`).
  - *Ví dụ*: SV đi đủ 100% buổi &rarr; Vi phạm CC = **0%**.
- **Quy tắc Bài tập về nhà (BTVN)**:
  - Backend API: Thường tính `homework.rate = done / total_homework_ca_mon` (ví dụ `1 / 4 = 25%`).
  - Frontend LMS hiển thị: **Vi phạm BTVN (%)** tính trên **số bài tập thực tế đã giao/đến hạn trong tuần** (`current_due_homework`).
  - *Ví dụ tuần 1 môn SSK101*: Giảng viên mới giao 1 bài tập. SV đã làm 1 bài (`done >= 1`) &rarr; Tỷ lệ hoàn thành 100% &rarr; **Vi phạm BTVN = 0%** (Đủ ĐK thi). Chỉ những SV chưa làm bài (`done = 0`) mới bị tính nợ bài (**Vi phạm BTVN = 100%**). Tuyệt đối không lấy tỷ lệ 25% của API chia cho cả môn làm sinh viên bị tính ảo thành vi phạm 75%.
- **Quy tắc Elearning (Tự học trực tuyến)**:
  - Backend API: Trả về `elearning.rate` (% on-time sessions).
  - Frontend LMS hiển thị: **Số bài vi phạm / chậm tuyệt đối** (ví dụ: `Chậm 1 bài`, `Chậm 2 bài`, `0 bài`).
  - Theo Quy chế mới của trường, chế tài thi Elearning dựa trên **số bài vi phạm tuyệt đối** (không cào bằng theo tỷ lệ % để tránh cấm thi ảo do unit mismatch).
  - *Trường hợp điển hình kiểm chứng*: SV `Nguyễn Thị Ngọc Ánh 2` (Lớp `HN-KS26-CNTT1`): Vi phạm CC = **0%**, Vi phạm BTVN = **0%**, Elearning = **Chậm 1 bài**, Trạng thái = **ĐỦ ĐIỀU KIỆN THI**.

---

## 19. Tổ Chức Báo Cáo & File Excel KS26 Theo Từng Nhóm Vi Phạm & Cơ Chế Môn Đầu Tiên
- **Cơ chế đặc thù môn đầu tiên SSK101 (User chỉ đạo)**:
  - Vì SSK101 là môn đầu tiên của tân sinh viên KS26, toàn bộ sinh viên không đủ điều kiện đều được xem xét cơ chế bảo lãnh nếu có tham gia học tập.
  - **Chỉ sinh viên không đi học buổi nào (Chuyên cần = 0% / Vi phạm CC 100%) mới tính vào diện cấm thi / không được bảo lãnh**:
    - Điển hình: SV `Mai Hoàng Việt` (`RK2600075` - Lớp `HN-K26-QTKD1` - vắng 5/5 buổi, vi phạm CC 100%, BTVN 0%, chậm 4 bài EL); SV `Nguyễn Công Trứ` (`RE26431` - Lớp `HCM-KS26-QTKD1`); cùng các sinh viên có mặt 0 buổi tại HN-K26-QTKD2, HN-K26-QTKD3, HCM-KS26-CNTT2.
    - *Lưu ý kỹ thuật*: Bản snapshot cũ từng ghi nhầm `presenceRate` của Mai Hoàng Việt là 60% và mã code là email cá nhân nên đã bị lọc sót. Cần luôn truy vấn trực tiếp LMS Analytics theo mã `RK2600075`.
- **Quy chuẩn hiển thị Dashboard Tab 3 (`weekly_director_report.html`)**:
  - Tại "Bảng Tổng Hợp Điều Kiện Thi & Tình Trạng Bảo Lãnh Từng Lớp KS26", toàn bộ các cột số lượng ở cả dòng từng lớp và dòng tổng toàn khóa đều được bổ sung hiển thị tỷ lệ phần trăm mở ngoặc bên cạnh: ví dụ `248 (66.3%)`, `126 (33.7%)`, `125 (33.4%)`, `9 (2.4%)`.
  - Tích hợp thanh nút lọc nhanh 1-Click theo đúng từng nhóm Mục 2 (Nợ BTVN 69 SV, Chậm Elearning 118 SV, Vắng Chuyên cần 87 SV, Nhóm bảo lãnh 125 SV, 9 Đơn LMS, Dải 80-100%, Dải 40-60%) và nút Tải trực tiếp file Excel.
- **Tái cấu trúc File Excel theo từng Nhóm Vi Phạm (Tránh mất thời gian tra từng lớp)**:
  - Đường dẫn file:
    - [output/dashboards/management/K26_Danh_Sach_Theo_Tung_Nhom_Vi_Pham.xlsx](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/output/dashboards/management/K26_Danh_Sach_Theo_Tung_Nhom_Vi_Pham.xlsx)
    - [output/dashboards/management/K26_Danh_Sach_Sinh_Vien_Va_Phan_Nhom.xlsx](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/output/dashboards/management/K26_Danh_Sach_Sinh_Vien_Va_Phan_Nhom.xlsx)
  - Kiến trúc 11 Sheet độc lập phục vụ tổ chức trực tiếp các buổi làm việc / phụ đạo:
    1. `TONG_HOP_TOAN_KHOA`: Dashboard tổng hợp toàn diện mở ngoặc % ở mọi cột.
    2. `1. No_BTVN (69 SV)`: Danh sách 69 SV nợ bài tập tuần 1 từ tất cả 10 lớp, gom về 1 sheet để CVHT tổ chức đôn đốc nộp bù.
    3. `2. Cham_Elearning (118 SV)`: Danh sách 118 SV chậm Elearning, sắp xếp từ chậm 4 bài đến chậm 1 bài.
    4. `3. Vang_Chuyen_Can (87 SV)`: Danh sách 87 SV vắng chuyên cần $\ge 20\%$ của toàn khóa.
    5. `4. Nhom_Bao_Lanh (125 SV)`: Toàn bộ 125 SV diện bảo lãnh để Ban Đào tạo tổ chức phiên họp xét duyệt.
    6. `5. 9_Don_Bao_Lanh_LMS`: Chi tiết 9 sinh viên gửi đơn trên hệ thống LMS Admin.
    7. `6. Dai_80-100%_Bao_Dong_Do`: Danh sách sinh viên thuộc dải rủi ro Báo động Đỏ.
    8. `7. Dai_60-80%_Nguy_Co_Cao`: Danh sách sinh viên thuộc dải rủi ro Nguy cơ Cao.
    9. `8. Dai_40-60%_Canh_Bao_TB`: Danh sách sinh viên thuộc dải Cảnh báo Trung bình.
    10. `9. Dai_20-40%_Canh_Bao_Nhe`: Danh sách sinh viên thuộc dải Cảnh báo Nhẹ.
    11. `10. DS_Day_Du_374_SV`: Bảng dữ liệu gốc toàn bộ 374 sinh viên tích hợp sẵn AutoFilter.

---

## 20. Cập Nhật Dữ Liệu Ngày 28/09/2026, 5 Môn Mới KS26 & Đồng Bộ Worklane
- **Tình trạng học vụ chốt ngày 28/09/2026**:
  - **Khóa KS24**: Đã chốt toàn bộ RPoint môn `Microservices System Design` [IT-214] để kết thúc môn và chuẩn bị thi hết môn.
  - **Khóa KS25 CNTT**: Hà Nội tiếp tục học môn `Phân tích & thiết kế hệ thống` [IT105-K25], TP.HCM đã chốt RPoint.
  - **Khóa KS25 QTKD**: Hôm nay thi môn `MAN107` nên chưa có dữ liệu môn mới, môn kế tiếp là `Business Intelligence (BI)`.
- **Cập nhật các sheet môn mới vào `PTIT_Chiso.xlsx`**:
  - Đã trích xuất chính xác từ hệ thống LMS và bổ sung thành công 7 sheet mới vào file `C:\Users\DELL\Desktop\Backup\PTIT\PTIT_Chiso.xlsx` (và đồng bộ vào `data/inputs/PTIT_Chiso.xlsx`):
    1. `KS26_Nhapmon_CNTT`: Môn *Nhập Môn CNTT* [IT108-K26] (6 lớp: HN1, HN2, HN3, HN4, HCM1, HCM2).
    2. `KS26_KN_Lamviecnhom`: Môn *Kỹ năng làm việc nhóm* [SKL01] (5 lớp: HN1, HN2, HN3, HCM1, HCM2).
    3. `KS26_Basic_Speaking`: Môn *Basic Speaking* [ENG105-K26] (8 lớp: HCM-QTKD1, HCM-CNTT2, HN-QTKD3, HN-CNTT3, v.v.).
    4. `KS26_QTKD_Tuduyphantich` & `KS25_QTKD_Tuduyphantich`: Môn *Tư duy phân tích* [SSK103] (4 lớp QTKD).
    5. `KS26_QTKD_Tinhocungdung` & `KS25_QTKD_Tinhocungdung`: Môn *Tin học ứng dụng* [SSK102] (4 lớp QTKD).
- **Đồng bộ Worklane chốt ngày 28/09/2026**:
  - Đã nạp thêm báo cáo ngày 26, 27 và 28/09/2026 (ngày 28/09 ghi nhận 25 báo cáo đã nộp).
  - Đã chạy đồng bộ toàn bộ 47 dự án và issues từ Worklane về `data/processed/project_issues_worklane.json`.
- **Thực thi Pipeline**:
  - DataSanitizer, Agent 1 (Kỷ luật SV), Agent 2 (Dự báo học vụ), Agent 3 (Tác nghiệp), Agent 4 (Worklane Daily Logs), Agent 5 (Master Portal & Báo cáo KPI Markdown `report_kpi_gv_tg.md`), Director Cockpit, Worklane Staff Audit, Weekly Director Report và Academic Cohort Dashboards đã chạy hoàn tất và đồng bộ sang `deploy_web/`.

---

## 21. Quy Chuẩn Hiệu Chuẩn Chỉ Số LMS Frontend & Ma Trận Đa Môn KS26 (Phiên 28/09/2026)
1. **Phân tách File Excel theo dõi chuyên biệt**:
   - `C:\Users\DELL\Desktop\Backup\PTIT\PTIT_Chiso_KS24_KS25.xlsx`: Dành riêng cho User theo dõi và điền thủ công chỉ số cho các lớp KS24 và KS25 (20 sheet chuẩn nguyên vẹn định dạng, công thức, độ rộng cột, không chứa dữ liệu KS26).
   - `C:\Users\DELL\Desktop\Backup\PTIT\PTIT_Chiso.xlsx`: File tổng hợp toàn diện kết nối tự động cả KS24, KS25 và 6 môn học mới của KS26.
2. **Cơ chế tính chỉ số kỷ luật đúng chuẩn LMS Frontend (Ground-Truth)**:
   - **Chuyên cần vi phạm > 10%**: `len([s for s in students if s.absence.rate > 10.0]) / total_sv * 100`. Ở buổi 1/22 của môn IT108, sinh viên vắng 1 buổi có absence rate là $1/22 = 4.55\% \le 10.0\% \rightarrow$ 0 sinh viên vượt ngưỡng 10% $\rightarrow$ **Vi phạm CC > 10% = 0.00%**.
   - **Bài tập vi phạm > 10%**: Chỉ tính trên số bài tập đã giao và đến hạn nộp trong tuần (`current_due_hw`). Ở buổi đầu tiên chưa có bài tập đến hạn nộp $\rightarrow$ **Vi phạm BTVN > 10% = 0.00%**. Tuyệt đối không chia cho 21 bài cả môn gây phạt ảo 100%.
   - **Elearning**: Tỷ lệ sinh viên trễ hạn hoặc chưa hoàn thành nội dung lý thuyết LMS. Ví dụ lớp `HN-KS26-CNTT1` có 2/43 SV trễ hạn $\rightarrow$ **4.65%**. Khớp 100% với hiển thị trên LMS Frontend của người dùng.
3. **Cấu trúc Đào tạo Đa Môn Đồng Thời Khóa KS26**:
   - Tân sinh viên KS26 học đồng thời nhiều môn (Chuyên ngành: IT108/SSK102/SSK103; Ngoại ngữ: ENG105; Kỹ năng mềm: SKL01/SSK101).
   - Agent 1 (`calculate_kpi_json.py`, `generate_kpi_report.py`, `generate_report.py`) và Director Dashboard (`generate_weekly_director_dashboard.py`) đã chuyển sang cơ chế **Ma Trận Đào Tạo Đa Môn (Multi-Course Matrix)**: hiển thị rõ ràng từng môn, từng giảng viên phụ trách, và chỉ số kỷ luật độc lập của từng môn cho từng lớp.
4. **Đồng bộ toàn bộ báo cáo**:
   - Toàn bộ đường ống từ DataSanitizer, Agent 1, Agent 2, Agent 3, Agent 4, Agent 5, Director Cockpit, Weekly Director Report đến Academic Cohort Dashboards đã chạy thành công 100% và đồng bộ sang `deploy_web/`.

---

## 22. Cải Tiến Giao Diện Mục 3.2 (Đa Môn KS26) & Loại Bỏ Hoàn Toàn Lớp HCM-K25-CNTT8 (28/09/2026)
1. **Thiết kế lại toàn diện Mục 3.2 Báo cáo Giao ban Tuần (`weekly_director_report.html`)**:
   - **Vấn đề trước đây**: Bảng HTML sử dụng `rowspan="2"` gây khó nhìn, lệch dòng giữa các lớp có 1 môn và 2 môn, đồng thời khó so sánh cùng một môn học trên nhiều lớp.
   - **Giải pháp thiết kế mới (Đa góc nhìn tương tác 1-Click)**:
     - **Chế độ 1: 🗂️ Thẻ Lớp Học Đa Môn (Class Cards Grid - Mặc định / Khuyên dùng)**: 10 thẻ tương ứng với 10 lớp KS26. Mỗi thẻ chứa các môn học của lớp dưới dạng các sub-panel bo góc riêng biệt, hiển thị tên môn, giảng viên, và 3 chỉ số kỷ luật (CC > 10%, BT > 10%, Elearning) cùng Badge trạng thái trực quan (`🟢 Chuẩn mực`, `🟡 Đôn đốc EL`, `🚨 Nhắc EL`, `⏳ Chuẩn bị học`).
     - **Chế độ 2: 📚 Phân Bảng Theo Môn Học (Subject Tabs View)**: Tách riêng 5 bảng độc lập cho từng môn (`IT108 Nhập môn CNTT`, `SKL01 Teamwork`, `ENG105 Tiếng Anh`, `SSK103 Tư duy PT`, `SSK102 Tin học UD`). Kèm thanh nút lọc (Pill Filters) 1-click giúp Giám đốc lọc tức thì xem riêng từng môn.
     - **Chế độ 3: 📋 Bảng Phẳng (Flat Matrix View)**: Bảng dữ liệu phẳng, mỗi dòng là một cặp `(Lớp, Môn)` duy nhất, không dùng `rowspan`, dễ tra cứu và copy-paste.
     - **Thanh thống kê nhanh (Quick Stat Chips)** trên đầu Mục 3.2 tóm tắt chỉ số trung bình và điểm nóng của cả 5 môn.
2. **Loại bỏ triệt để Lớp HCM-K25-CNTT8 khỏi toàn bộ hệ thống**:
   - Theo quyết định tổ chức đào tạo, lớp `HCM-K25-CNTT8` đã giải thể/sáp nhập học viên, khối KS25 CNTT TP. HCM chính thức duy trì **3 lớp**: `HCM-K25-CNTT5`, `HCM-K25-CNTT6`, `HCM-K25-CNTT7`.
   - Đã loại bỏ hoàn toàn `HCM-K25-CNTT8` khỏi:
     - `scripts/generate_weekly_director_dashboard.py`: Cập nhật quy mô 8 lớp (5 HN, 3 HCM), tính lại trung bình chuyên cần HCM (21.53%), xóa điểm nóng và dòng bảng CNTT8, chuyển điểm nóng sang lớp CNTT7 (34.78%).
     - `agents/core/agent_1_class_kpi/`: Cập nhật cấu hình nhóm lớp `KS25_CNTT_HCM`, loại bỏ bộ lọc CNTT8 trong tính toán KPI (`calculate_kpi_json.py`) và sinh báo cáo (`generate_kpi_report.py`).
     - `agents/master/agent_5_master_portal/`: Loại bỏ khỏi danh sách `active_classes_config` trong `generate_unified_dashboard.py` và cập nhật nhận xét nhân sự Thầy Trần Quốc Tuấn trong `generate_kpi_report.py`.
     - `agents/core/agent_2_academic_pred/generate_report.py`: Cập nhật đánh giá giáo vụ cho cơ sở HCM còn 3 lớp.
   - Toàn bộ pipeline đã được biên dịch lại và xác minh: 0 kết quả tìm thấy `HCM-K25-CNTT8` trên toàn bộ báo cáo Markdown và HTML trong `output/` và `deploy_web/`.---

## 23. Chuẩn Hóa Số Liệu Môn Kỹ Năng Học Tập Chủ Động (SSK101) Khóa KS26 (29/09/2026)
1. **Rà soát & Xử lý Triệt để Sai lệch Thống kê**:
   - **Trường hợp Trần Tuấn Anh 4 (`B26DTCN119` - Lớp `HN-KS26-CNTT1`) & Quy chuẩn Chuyên cần Frontend**:
     - *Phân biệt Backend vs Frontend*: Trên Backend (`course_class_statistics`), `absence.rate = 0%` vì chỉ đếm số buổi vắng không phép (`absentUnexcused = 0`). Tuy nhiên trên **Frontend LMS**, công thức tính **Vi phạm Chuyên cần** quy đổi:
       $$\text{Số buổi vi phạm} = \text{Vắng KP} \times 1.0 + \text{Vắng có phép} \times 0.5 + \text{Đi muộn} \times 0.5$$
       Trần Tuấn Anh 4 đi học 4 buổi, muộn 1 buổi $\rightarrow$ Số buổi vi phạm $= 1 \times 0.5 = 0.5$ buổi $\rightarrow$ Tỷ lệ vi phạm chuyên cần Frontend $= 0.5 / 5 = \mathbf{10\%}$!
     - *Vi phạm BTVN*: Đã hoàn thành 3 bài tập $\rightarrow$ Vi phạm BTVN $= \mathbf{0\%}$.
     - *Elearning*: Chậm 1 bài lý thuyết LMS.
     - *Quy chuẩn hiển thị Báo cáo/Excel*: **LOẠI BỎ HOÀN TOÀN** các cột "Độ hoàn thành" (như BTVN Hoàn thành 75%) để không gây nhầm lẫn với tỷ lệ vi phạm. Chỉ hiển thị thuần túy **TỶ LỆ VI PHẠM (%)**.
   - **Trường hợp Dương Gia Khiêm (`B26DTCN143` - Lớp `HN-KS26-CNTT2`)**:
     - Vi phạm Chuyên cần: **20%** (vắng 1/5 buổi, đi học 4/5 buổi).
     - Vi phạm BTVN: **80%** (theo đúng ghi nhận màn hình LMS).
     - Vi phạm Elearning: **0 bài** (0%).
     - Trạng thái chính thức trên LMS: **ĐỦ ĐIỀU KIỆN THI** (`exam.eligible: true`).
2. **Quy chuẩn Duyệt Sheet `0_BUOI_DI_HOC_VI_PHAM_100%`**:
   - Sheet này CHỈ ĐƯỢC CHỨA đúng các học viên có tỷ lệ vắng mặt $100\%$ hoặc số buổi đi học bằng 0 trên tổng số buổi đã lên lớp ($attendedSessions == 0$ và $absentSessions == plannedSessions$).
   - Toàn bộ khóa KS26 môn SSK101 (374 SV trên 9 lớp có lịch học) **CHỈ CÓ DUY NHẤT 4 HỌC VIÊN** vi phạm 100% chuyên cần:
     1. `Mai Hoàng Việt` (`RK2600075` - Lớp `HN-K26-QTKD1`) - Vắng 5/5 buổi (100%).
     2. `Nguyễn Nhật Vy` (`RK2600069` - Lớp `HN-K26-QTKD2`) - Vắng 5/5 buổi (100%).
     3. `Trần Vũ Hoàng` (`RK2600071` - Lớp `HN-K26-QTKD2`) - Vắng 5/5 buổi (100%).
     4. `Nguyễn Công Trứ` (`RE26431` - Lớp `HCM-K26-QTKD1`) - Vắng 5/5 buổi (100%).
3. **Tối Ưu Quy Trình & Đường Ống Dữ Liệu Tốc Độ Cao (Sub-3s Pipeline)**:
   - Script `pipeline_fast_ks26_align.py` sử dụng `Promise.all` quét đồng thời toàn bộ 18 endpoints API (9 lớp điểm danh + 9 lớp thống kê) trong ~3.3 giây.
   - Quá trình tính toán ma trận vi phạm in-memory và xuất toàn bộ 6 file Excel + đồng bộ HTML chỉ mất **~2.2 giây**.
   - Báo cáo Excel đã được lưu đầy đủ tại:
     - `output/dashboards/management/K26_Danh_Sach_Sinh_Vien_Va_Phan_Nhom.xlsx`
     - `output/dashboards/management/K26_Danh_Sach_Theo_Tung_Nhom_Vi_Pham.xlsx`
     - `data/K26_Danh_Sach_Sinh_Vien_Va_Phan_Nhom.xlsx`
     - `output/dashboards/management/K26_Danh_Sach_Sinh_Vien_Va_Phan_Nhom_MoiNhat.xlsx`
   - Báo cáo HTML `weekly_director_report.html` (và bản deploy tại `deploy_web/`) đã được đồng bộ 100%.

---

## 24. Cập Nhật Chỉ Số Thời Gian Thực KS26 & Đồng Bộ Worklane Chốt Ngày 29/09/2026
1. **Chỉ số Học vụ Khóa KS26 (LMS Realtime)**:
   - **Môn Kỹ năng Học tập chủ động (SSK101)**: Đã quét realtime từ LMS MCP toàn bộ 9 lớp (374 SV) với chuẩn hiển thị Frontend:
     - Vi phạm Chuyên cần tính quy đổi: đi muộn = 0.5 buổi, nghỉ có phép = 0.5 buổi, nghỉ không phép = 1.0 buổi.
     - Vi phạm BTVN tuần đầu = 0% nếu đã hoàn thành >= 1 bài; chỉ SV chưa nộp bài mới tính nợ bài (100%).
     - Elearning tính theo số bài trễ tuyệt đối (ví dụ `Chậm 1 bài`, `0 bài`).
     - Sheet `0_BUOI_DI_HOC_VI_PHAM_100%` duy trì đúng 4 học viên vắng 5/5 buổi: Mai Hoàng Việt, Nguyễn Nhật Vy, Trần Vũ Hoàng, Nguyễn Công Trứ.
   - **5 Môn học mới Khóa KS26**: Đã quét dữ liệu từ LMS Analytics và cập nhật vào `PTIT_Chiso.xlsx` cột ngày 29/09/2026:
     - `IT108-K26` (*Nhập Môn CNTT*): 6 lớp (HN1: CC 4.65%, EL 4.65%; HN2: CC 2.50%, EL 0%; HN3: CC 2.38%, EL 4.76%; HN4: CC 31.03%, EL 34.48% - điểm nóng vắng; HCM1: CC 10.87%, EL 6.52%; HCM2: CC 13.33%, EL 8.89%).
     - `SKL01` (*Kỹ năng làm việc nhóm*): 5 lớp (HN1: CC 4.65%, EL 16.28%; HN2: CC 2.50%, EL 5.00%; HN3, HCM1, HCM2: CC 0.00%, EL 0.00%).
     - `ENG105-K26` (*Basic Speaking*): 8 lớp (Điểm nóng vắng: HN-QTKD3 vắng 25.0%, HN-QTKD2 vắng 22.2%, HCM-CNTT2 vắng 20.0%, HN-QTKD1 vắng 13.6%).
     - `SSK103` (*Tư duy phân tích*): 4 lớp (HN-QTKD3: CC 15.91%, EL 20.45%; HN-QTKD1: CC 9.09%, EL 6.82%; HCM-QTKD1: 0.00%).
     - `SSK102` (*Tin học ứng dụng*): 4 lớp (HN-QTKD3: CC 29.55%, EL 18.18%; HCM-QTKD1, HN-QTKD1, HN-QTKD2: 0.00%).
2. **Dữ liệu Worklane PM (Chốt ngày 29/09/2026)**:
   - **Đồng bộ Dự án & Issues**: Nạp thành công toàn bộ 47 dự án phòng Đào tạo và các issues tương ứng về `data/processed/project_issues_worklane.json`.
   - **Báo cáo Ngày (Daily Reports)**:
     - Cập nhật thêm ngày 28/09 (34 báo cáo) và ngày 29/09 (29 báo cáo). Tổng số ngày tích lũy trong cache đạt 81 ngày.
     - Cửa sổ kiểm toán tuần 5 ngày gần nhất: `23/09, 24/09, 25/09, 28/09, 29/09`.
     - Phân tích giờ công đạt chuẩn 40h/tuần, giờ ngoài barem KPI Master và bóc tách các công việc chung chung.
3. **Thực thi Pipeline Toàn diện & Đồng bộ**:
   - Toàn bộ pipeline đã chạy hoàn tất: DataSanitizer -> Agent 1 (Kỷ luật SV) -> Agent 2 (Dự báo học vụ) -> Agent 3 (Tác nghiệp) -> Agent 4 (Worklane Daily Logs) -> Agent 5 (Master Portal & `data/report_kpi_gv_tg.md`).
   - Các dashboard quản trị: `weekly_director_report.html`, `worklane_staff_audit.html`, `director_cockpit.html`, và 5 dashboard chuyên sâu học vụ theo môn đã được biên dịch và đồng bộ 100% sang `deploy_web/`.

---

## 25. Đồng Bộ Dữ Liệu Học Vụ Mới Nhất Ngày 29/09/2026 (PTIT_Chiso.xlsx)
1. **Nguồn dữ liệu & Tích hợp**:
   - File nguồn: `C:\Users\DELL\Desktop\Backup\PTIT\PTIT_Chiso.xlsx` (Cập nhật ngày 29/09/2026).
   - Đã đồng bộ sang `data/inputs/PTIT_Chiso.xlsx` và tái lập Single Source of Truth Cache `data/processed/classes_metrics_cache.json`.
2. **Biến động chỉ số học vụ ngày 29/09/2026**:
   - **Khối KS25 CNTT (Môn PTTKHT [IT105-K25])**: Bổ sung dữ liệu buổi ngày 29/09/2026 cho 5 lớp Hà Nội:
     - `HN-K25-CNTT1`: CC vắng tăng mạnh lên **31.58%** (12/38 SV), Nợ BTVN: 15.79%, Elearning: 23.68%.
     - `HN-K25-CNTT2`: CC vắng 18.60%, Nợ BTVN: 4.65%, Elearning: 11.63%.
     - `HN-K25-CNTT3`: CC vắng 13.95%, Nợ BTVN: 0.00%, Elearning: 11.63%.
     - `HN-K25-CNTT4`: CC vắng 4.76%, Nợ BTVN: 2.38%, Elearning: 7.14%.
     - `HN-K25-CNTT5`: CC vắng 24.44% (11/45 SV), Nợ BTVN: 4.44%, Elearning: 13.33%.
   - **Khối KS25 QTKD (Môn mới: Business Intelligence [BI])**:
     - Chính thức khởi động buổi 1 ngày 29/09/2026 (sau khi thi xong môn MAN107):
     - `HN-K25-QTKD1` (46 SV - GV Hoàng Thị Kim Oanh): Chuyên cần vi phạm **0.00%** (100% sinh viên đi học đầy đủ!), BTVN **0.00%**, Elearning **6.52%**.
     - `HN-K25-QTKD2` (42 SV - GV Lê Thành Ngọc): Chuyên cần vi phạm **0.00%** (100% sinh viên đi học đầy đủ!), BTVN **0.00%**, Elearning **7.14%**.
     - Khởi sắc vượt bậc so với giai đoạn môn MAN107 (từng vắng đến 56.52%).
3. **Thực thi Pipeline & Đồng bộ Báo cáo**:
   - Toàn bộ đường ống đào tạo (DataSanitizer, Agent 1 đến Agent 5, Weekly Director Report, Director Cockpit, Worklane Staff Audit, Academic Cohort Dashboards) đã hoàn tất trong 72.02 giây.
   - Báo cáo Markdown `data/report_kpi_gv_tg.md`, các trang HTML trong `output/dashboards/` và cổng triển khai `deploy_web/` đã được đồng bộ 100%.

---

## 26. Chẩn Đoán Chuyển Dịch Hành Vi Khóa K26 & Kế Hoạch Tác Chiến 5-15 Phút Trực Tiếp Tại Lớp (30/09/2026)
1. **Bối Cảnh Nghiệp Vụ & Quyết Định Quản Trị**:
   - Theo chỉ đạo của Giám đốc Đào tạo (Anh Nguyễn Duy Quang), cần theo dõi sự chuyển dịch của tân sinh viên K26 từ Môn đầu tiên (`SSK101`) sang các môn học mới (`IT108`, `SKL01`, `ENG105`, `SSK102`, `SSK103`).
   - **Quy tắc tác chiến thực địa**: Không tổ chức họp online đông người (tránh lãng phí thời gian, sinh viên tắt camera, trốn họp). Quản lý Đào tạo và CVHT sẽ **vào trực tiếp từng lớp 5–15 phút** giải quyết triệt để.
   - **Bóc tách lỗi thích nghi**: Sinh viên tuần 1 vi phạm do bỡ ngỡ tài khoản/LMS, sang môn mới đã sạch lỗi 100% (TH3) &rarr; **Miễn can thiệp kỷ luật, biểu dương khích lệ**.
2. **Quy Chuẩn 4 Nhóm Hành Vi & Kết Quả Toàn Khóa (374 SV / 9 Lớp)**:
   - **Tỷ lệ Cải thiện Toàn khóa**: Đạt **95.2%** (356/374 SV đã sạch lỗi hoặc giảm vi phạm mạnh).
   - **TH3 (Thích nghi tốt / Sạch 100% lỗi môn mới)**: **351 SV (93.9%)** &rarr; Tuyên dương qua nhóm Zalo lớp.
   - **TH2 (Đang tiến bộ rõ rệt)**: **5 SV (1.3%)** &rarr; Gặp nhanh 3p đầu giờ, CVHT đôn đốc giữ phong độ.
   - **TH1 (Nguy cơ bỏ học / Báo động Đỏ)**: **5 SV (1.3%)** &rarr; Gặp riêng 5p cuối giờ, lập biên bản cam kết, gọi điện phụ huynh. PIC: Quản lý ĐT + CVHT (Deadline: 48h). (Bao gồm Mai Hoàng Việt, Trần Vũ Hoàng, Nguyễn Nhật Vy,...).
   - **TH4 (Sốc môn mới chuyên ngành)**: **13 SV (3.5%)** &rarr; Môn 1 tốt nhưng môn mới (IT108 / ENG105) nợ bài/vắng. Gặp 5p giữa giờ, bàn giao GV bộ môn + Trợ giảng kèm cặp (Deadline: Trước buổi học tới).
3. **Bảng Xếp Hạng Tỷ Lệ Cải Thiện 9 Lớp K26**:
   - 100% Cải thiện: `HCM-KS26-CNTT1` (47 SV), `HCM-KS26-CNTT2` (45 SV), `HCM-KS26-QTKD1` (23 SV), `HN-K26-QTKD3` (44 SV).
   - Tiến bộ cao: `HN-K26-CNTT3` (97.6%), `HN-K26-QTKD2` (95.5%), `HN-K26-QTKD1` (90.9%), `HN-K26-CNTT2` (90.7%).
   - Điểm nóng cần hỗ trợ: `HN-KS26-CNTT1` (83.7% cải thiện, có 3 SV TH1 và 4 SV TH4).
4. **Hệ Thống Báo Cáo & File Đầu Ra**:
   - File Excel tác chiến 14 Sheet: `output/dashboards/management/K26_Theo_Doi_Chuyen_Dich_Hanh_Vi_Va_Giai_Phap.xlsx` (Sheet cải thiện 9 lớp, 4 sheet nhóm tác chiến TH1-TH4, 9 sheet chi tiết từng lớp).
   - Dashboard HTML Executive: `output/dashboards/management/bao_cao_k26_chuyen_dich_hanh_vi.html` (đồng bộ `deploy_web/`) tích hợp Chart.js, 1-Click Copy Zalo/Slack, Chế độ Chụp Ảnh Màn Hình.
   - Đã nhúng banner chuyên đề vào Tab 3 của Báo cáo Giao ban Giám đốc `weekly_director_report.html`.

