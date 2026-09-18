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
