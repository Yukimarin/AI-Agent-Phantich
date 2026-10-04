# Design Document: Quy Hoạch Hệ Thống Báo Cáo Chuyên Sâu Học Vụ (`output/dashboards/academic/`)

- **Ngày ban hành**: 25/09/2026
- **Mục tiêu**: Phân tách thư mục `output/dashboards/academic/` thành 3 khối khóa đào tạo (`ks24/`, `ks25/`, `ks26/`), bên trong chứa các báo cáo chuyên sâu bóc tách riêng từng môn và từng khối ngành (CNTT, QTKD), kèm theo thanh điều hướng liên kết thống nhất toàn hệ thống.

---

## 1. Cấu Trúc Thư Mục & Tệp Tin

```
output/dashboards/academic/
├── ks24/
│   └── it214_microservices_cntt.html     # Khóa KS24 Kỳ IV - Môn Microservices System Design (5 lớp CNTT)
│
├── ks25/
│   ├── it105_fastapi_cntt.html           # Khóa KS25 Kỳ II - Môn FastAPI / PTTKHT (9 lớp CNTT)
│   └── man107_qtkd.html                  # Khóa KS25 Kỳ II - Môn MAN107 Chiến lược doanh nghiệp (2 lớp QTKD)
│
└── ks26/
    ├── ssk101_cntt.html                  # Khóa KS26 Tân sinh viên - Môn SSK101 (6 lớp CNTT)
    └── ssk101_qtkd.html                  # Khóa KS26 Tân sinh viên - Môn SSK101 (4 lớp QTKD)
```

---

## 2. Đặc Tả Chi Tiết Từng Báo Cáo Chuyên Sâu

### 2.1. `ks24/it214_microservices_cntt.html`
- **Môn học**: Microservices System Design (`[IT-214]`) & Tiên quyết Backend (`[IT-213]`).
- **Quy mô**: 5 lớp CNTT (`HN1` đến `4`, `HCM1`), 192 sinh viên.
- **Điểm nghẽn học thuật**:
  - Độ khó môn học cao nhất chương trình ($CDC = 1.45$).
  - Độ vênh lớn giữa BTVN làm ở nhà (>85%) và điểm thi Hackathon thực chiến (trung bình 45.3 điểm) do khó khăn khi debug hệ thống phân tán (Kafka, Docker Compose, API Gateway).
  - Dự báo qua môn trung bình: 51.5% (HN2 kiểu mẫu 59.5%, HN3 báo động đỏ 43.3% do vắng CC 25.64%).
  - Care List: 69 sinh viên phân luồng (RED, ORANGE, YELLOW, GREEN) kèm bảng tra cứu chi tiết.

### 2.2. `ks25/it105_fastapi_cntt.html`
- **Môn học**: FastAPI / Phân tích và Thiết kế Hệ thống (`IT105-K25`).
- **Quy mô**: 9 lớp CNTT (5 Hà Nội, 4 TP.HCM), 420 sinh viên.
- **Điểm nghẽn học thuật**:
  - Phễu hao hụt học vụ và rào cản đề tài đồ án 5 ngày *Construction Site Management API*.
  - 87/273 sinh viên (31.9% số đủ điều kiện) bỏ thi vì quá tải nhận thức bài toán RBAC/ABAC.
  - Phân tích chuỗi 3 môn tiên quyết, khảo thí ĐGNL độc lập và phân luồng cứu vãn 271 SV.

### 2.3. `ks25/man107_qtkd.html`
- **Môn học**: Quản trị chiến lược doanh nghiệp (`MAN107`).
- **Quy mô**: 2 lớp QTKD (`HN-K25-QTKD1` 46 SV, `HN-K25-QTKD2` 42 SV - GV Đặng Quỳnh Trang).
- **Điểm nghẽn học thuật**:
  - Tỷ lệ vắng chuyên cần tăng vọt ở mức báo động rất cao: QTKD1 vắng 52.17%, QTKD2 vắng 33.33%.
  - Tỷ lệ vi phạm Elearning 26.19%.
  - Chẩn đoán nguyên nhân: Sinh viên lơ là giữa kỳ, thiếu kiểm soát điểm danh từ GV/TG.
  - Đề xuất can thiệp: CVHT gọi điện phụ huynh, giao bài tập tình huống bù đắp chuyên cần.

### 2.4. `ks26/ssk101_cntt.html`
- **Môn học**: Kỹ năng Học tập chủ động & Phát triển bản thân (`SSK101`).
- **Quy mô**: 6 lớp CNTT (`HN1` đến `4`, `HCM1` đến `2`), 242 sinh viên.
- **Điểm nghẽn học thuật**:
  - Tâm lý chủ quan xem môn Kỹ năng mềm là môn phụ $\rightarrow$ tỷ lệ hoàn thành BTVN cực thấp (0% - 25%).
  - Điểm nóng báo động đỏ: `HCM-KS26-CNTT1` (44.7% trượt thi), `HN-KS26-CNTT1` (37.2% trượt thi).
  - Lớp `HN-K26-CNTT3`: 8 sinh viên lỗi dữ liệu định danh trên LMS.
  - Lớp `HN-K26-CNTT2` (GV Hồ Xuân Hùng): Xuất sắc số 1 với 93.0% đủ ĐK thi.
  - Danh sách chi tiết các sinh viên cần làm thủ tục bảo lãnh khẩn cấp.

### 2.5. `ks26/ssk101_qtkd.html`
- **Môn học**: Kỹ năng Học tập chủ động & Phát triển bản thân (`SSK101`).
- **Quy mô**: 4 lớp QTKD (`HN1` đến `3`, `HCM1`), 155 sinh viên.
- **Điểm nghẽn học thuật**:
  - Tỷ lệ nộp BTVN rất cao (>84%), sinh viên năng nổ tương tác.
  - Điểm nóng: `HN-K26-QTKD3` vắng chuyên cần 12.7%, `HN-K26-QTKD2` nợ Elearning 61.38%.
  - Lớp kiểu mẫu `HCM-KS26-QTKD1` (GV Lê Nhựt Mi): Đạt 87.0% đủ ĐK thi.
  - Danh sách chi tiết sinh viên QTKD thuộc diện cần bảo lãnh hoặc phụ đạo.

---

## 3. Hệ Thống Thanh Điều Hướng (Unified Top Navbar)

Mỗi file báo cáo đều được tích hợp thanh điều hướng chuẩn mực:
```html
<div class="flex items-center space-x-1.5 bg-slate-800/80 p-1 rounded-lg border border-slate-700 text-xs">
    <a href="../ks24/it214_microservices_cntt.html">KS24 Microservices</a>
    <a href="../ks25/it105_fastapi_cntt.html">KS25 FastAPI</a>
    <a href="../ks25/man107_qtkd.html">KS25 MAN107</a>
    <a href="../ks26/ssk101_cntt.html">KS26 CNTT SSK101</a>
    <a href="../ks26/ssk101_qtkd.html">KS26 QTKD SSK101</a>
    <a href="../../core/agent_5_master_portal.html" class="text-indigo-400">Master Portal ↗</a>
</div>
```

---

## 4. Tích Hợp Pipeline & Tự Động Hóa
- Nâng cấp `scripts/generate_academic_cohort_dashboards.py` để tự động render toàn bộ 5 báo cáo chuyên sâu vào 3 thư mục `ks24/`, `ks25/`, `ks26/`.
- `run_pipeline.py` kích hoạt script này trong Bước 5 và đồng bộ sang `deploy_web/academic/`.
