# Sub Agent 2: AcademicPredictor - Tài liệu tổng hợp hoạt động

Báo cáo này tổng hợp vai trò, cấu trúc dữ liệu, thuật toán tính điểm và các thay đổi phát triển đối với **Sub Agent 2 (AcademicPredictor)** trong dự án đánh giá hiệu suất đào tạo.

---

## 1. Vai trò & Mục tiêu
AcademicPredictor là Agent cốt lõi về dự báo học vụ và phân tích rủi ro học tập. Nhiệm vụ chính là:
- Đọc cơ sở dữ liệu để tính toán điểm trung bình (GPA) lịch sử, tỷ lệ sinh viên qua/trượt môn của từng lớp.
- Áp dụng các thuật toán hiệu chuẩn chỉ số và dự báo nguy cơ trượt học tập của từng học viên ở môn hiện tại.
- Phân tầng nguy cơ học lực và lập danh sách cần quan tâm (Care List) theo 3 cấp độ (Đỏ, Vàng, Xanh) cho từng lớp học.
- Cung cấp tỷ lệ qua môn (Pass Rate) dự kiến/thực tế để làm điểm Học tập (trọng số 30%) cho giảng viên phụ trách.

---

## 2. Dữ liệu Đầu vào & Đầu ra

### Dữ liệu Đầu vào (Inputs)
- **Database**: Hệ quản trị MySQL `qldt_el` (cổng 3307) hoặc SQLite `data/qldt.db`.
- **Tệp cấu hình**: [course_metadata.json](file:///C:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/data/inputs/course_metadata.json) chứa cấu trúc buổi học, định mức và trọng số môn học.
- **Tỷ lệ vi phạm từ Excel**: Chuyển giao từ Agent 1.

### Dữ liệu Đầu ra (Outputs)
- **Tệp JSON dự báo**: [agent2_output.json](file:///C:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/data/processed/agent2_output.json).
- **Báo cáo Care List Markdown**: [agent_2_academic_prediction.md](file:///C:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/output/reports/core/agent_2_academic_prediction.md).
- **HTML Dashboards**: [agent_2_academic_prediction.html](file:///C:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/output/dashboards/core/agent_2_academic_prediction.html) và Tab 2 của [agent_5_master_portal.html](file:///C:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/output/dashboards/core/agent_5_master_portal.html).

---

## 3. Quy tắc & Thuật toán dự báo

### 3.1 Hệ số độ khó môn học (CDC - Course Difficulty Coefficient)
Được kết hợp tự động từ:
- Dữ liệu tỷ lệ trượt môn học lịch sử có trong cơ sở dữ liệu.
- Định mức độ khó trong `data/course_metadata.json`.
- Thuật toán phán đoán Heuristics dựa trên từ khóa tên môn học (ví dụ: các môn lập trình chuyên ngành Java, Python có CDC cao; môn Kỹ năng mềm/Thực tập được gán tỷ lệ đỗ mặc định 93% để tránh áp sai công thức).

### 3.2 Điểm kỷ luật môn học trước
- **Khóa KS25**: Truy cập trường `total_score` từ bảng `auto_rpoints` của môn học trước.
- **Khóa KS24**: Truy cập cột `rpoints` trong bảng `final_results` của môn học trước.

### 3.3 Hiệu chuẩn chỉ số (Calibration)
- **Chuyên cần**: Scale tỷ lệ vắng của từng cá nhân từ database theo tỷ lệ vắng lớp trung bình của Excel.
- **Bài tập**: Đảo ngược tỷ lệ nợ (debt rate) của Excel thành tỷ lệ hoàn thành (`100.0 - excel_disc['bt']`) trước khi đem đi hiệu chuẩn với tỷ lệ nộp bài tập trong DB.
- **Elearning**: Giữ nguyên số bài vi phạm tuyệt đối từ DB để xét cấm thi theo Quy chế mới (không scale theo % của Excel để tránh cấm thi ảo do unit mismatch).

### 3.4 Hệ số phạt môi trường (Peer Pressure)
Khi tỷ lệ vi phạm trung bình của lớp học vượt quá 10%, áp dụng hệ số phạt môi trường tuyến tính $Multiplier_{env}$ để giảm xác suất đỗ của từng cá nhân trong lớp học đó:

$$P_{final} = P_{eligible} \times Multiplier_{env}$$

### 3.5 Chốt chặn cấm thi
- Đối với các môn học hiện tại, chỉ áp dụng chốt chặn cấm thi (xác suất đỗ = 0%) khi thời lượng môn học đã đi qua được trên 30% (số buổi học > 3). Nếu số buổi học $\le$ 3, bỏ qua chốt chặn cấm thi của môn hiện tại để tránh đưa ra cảnh báo ảo.

---

## 4. Lịch sử Thay đổi & Quyết định quan trọng
- **[2026-07-04] Xử lý điểm danh ảo**: Giảng viên dạy Project thường quên tắt điểm danh tự động gây tăng ảo tỷ lệ vi phạm. Giải pháp: Lấy điểm Rpoint chốt thực tế từ database để hiệu chỉnh ngược lại tỷ lệ vi phạm thực chất của lớp (Vi phạm = 100 - Rpoint).
- **[2026-07-09] Nới lỏng luật cấm thi cho khóa cũ K24**: Kết quả Harness chỉ ra MAE toàn cục ở mức ~31.9% do mô hình áp dụng luật cấm thi cứng quá nghiêm ngặt với khóa cũ, trong khi thực tế giảng viên vẫn cho thi. Giải pháp: Tháo bỏ chốt chặn cấm thi cứng đối với khóa K24 (chỉ lưu cảnh báo), giúp đưa sai số MAE toàn cục giảm mạnh từ **30.76%** xuống còn **11.49%** (đạt chuẩn chất lượng < 12%).
- **[2026-07-09] Bộ tham số tối ưu sau Grid Search**:
  - KS24: w1=0.40, w2=0.60 | Prereq Pass Base = 0.98, Fail Base = 0.10 | Hackathon Multiplier = 1.25.
  - KS25: w1=0.00, w2=1.00 | Prereq Pass Base = 0.85, Fail Base = 0.10 | Hackathon Multiplier = 1.30.
- **[2026-07-09] Accordion Care List**: Thiết kế danh sách học viên nguy cơ trượt tích hợp dạng Accordion xếp gọn ngay dưới dòng lớp của bảng dự báo học lực trên unified dashboard.

---

## 5. Mã nguồn liên quan
- **Script dự báo chính**: [analyze_student_risk_real.py](file:///C:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/agents/core/agent_2_academic_pred/analyze_student_risk_real.py)
- **Script xuất bản dashboard**: [generate_report.py](file:///C:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/agents/core/agent_2_academic_pred/generate_report.py)
- **Bộ khung đo đạc sai số**: [evaluation_harness.py](file:///C:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/agents/core/agent_2_academic_pred/evaluation_harness.py)



---

*   Xem chi tiết: [[output/reports/core/agent_2_academic_prediction|Báo cáo Dự báo Học thuật & Danh sách Can thiệp (Care List)]]
*   Dashboard trực quan: [agent_2_academic_prediction.html](file:///C:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/output/dashboards/core/agent_2_academic_prediction.html)
---
Trở về: [[Bản đồ Tri thức MOC|Bản đồ Tri thức dự án]]
