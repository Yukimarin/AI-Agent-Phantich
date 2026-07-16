# Quy tắc Dự án: Đánh giá KPI GV/TG

Tài liệu này định nghĩa các nguyên tắc hoạt động, vai trò của các Subagent và định dạng dữ liệu trong dự án phân tích chỉ số đào tạo và đánh giá KPI Giảng viên (GV) & Trợ giảng (TG).

## 1. Nguyên tắc hoạt động chung
- **Không tự ý viết thêm code agent ứng dụng (multi-agent code)**: Mọi hoạt động phân tích và điều phối phải được thực hiện trực tiếp bởi Antigravity và các Subagent tích hợp sẵn.
- **Ngôn ngữ báo cáo**: Toàn bộ báo cáo KPI, phản hồi và phân tích phải sử dụng tiếng Việt chuẩn, chuyên nghiệp, rõ ràng.
- **Xử lý lỗi dữ liệu**: Nếu thiếu dữ liệu hoặc file bị lỗi, Agent phải báo cáo chi tiết lỗi và đưa ra cảnh báo thay vì dừng chạy đột ngột.

## 2. Vai trò của các Subagent
Khi thực hiện nhiệm vụ, Antigravity sẽ phân chia công việc cho các Subagent và Agent Lead có cấu hình chuyên biệt sau:

### 2.1 Agent Lead: MasterEvaluator
- **Nhiệm vụ**: Tổng hợp kết quả từ các Subagent và tính điểm KPI tổng hợp theo trọng số:
  - Điểm Kỷ luật (40%): Gộp trung bình cộng từ Kỷ luật học viên (Sub Agent 1) và Kỷ luật tác nghiệp của GV/TG (Sub Agent 3).
  - Điểm Học tập (30%): Hiệu suất học tập của sinh viên do Sub Agent 2 đánh giá.
  - Điểm Báo cáo ngày (30%): Chất lượng báo cáo ngày của GV/TG do Sub Agent 4 đánh giá.
- **Đầu ra yêu cầu**: Xuất file báo cáo Markdown đẹp mắt tại `data/report_kpi_gv_tg.md`.

### 2.2 Sub Agent 1: ViolationAnalyst (Compliance Auditor)
- **Nhiệm vụ**: Phân tích lỗi vi phạm của sinh viên từ `data/vi_pham.xlsx` và tính toán Điểm Kỷ Luật học viên.
- **Đầu ra yêu cầu**: JSON chứa thông tin chi tiết lỗi của học viên từng lớp và điểm số tương ứng.

### 2.3 Sub Agent 2: AcademicPredictor
- **Nhiệm vụ**: Đọc database SQLite/SQL script `data/qldt.sql` (hoặc database MySQL `qldt_el`) để tính điểm trung bình (GPA), tỷ lệ sinh viên qua/rớt môn của từng lớp.
- **Quy tắc làm việc và dự báo**:
  - **Hệ số độ khó môn học (CDC)**: Kết hợp tự động từ dữ liệu tỷ lệ trượt lịch sử trong DB (nếu có), file cấu hình cấu trúc môn học tại `data/course_metadata.json`, và thuật toán phán đoán Heuristics dựa trên từ khóa tên môn học nếu chưa được cấu hình.
  - **Điểm Kỷ luật môn trước**: Đối với khóa KS25, truy cập trường `total_score` từ bảng `auto_rpoints` của môn học trước. Đối với khóa KS24, truy cập cột `rpoints` trong bảng `final_results` của môn học trước.
  - **Quy tắc chặn cứng cấm thi**: Chỉ áp dụng cấm thi dựa trên kỷ luật của môn hiện tại khi thời lượng môn học đã đạt trên 30% (số buổi học > 3). Nếu số buổi học <= 3, bỏ qua các chốt chặn kỷ luật môn hiện tại để tránh cảnh báo ảo.
  - **Hiệu chuẩn chỉ số (Calibration)**:
    - **Chuyên cần**: Scale tỷ lệ vắng theo tỷ lệ vắng lớp trung bình của Excel.
    - **Bài tập**: DB là tỷ lệ hoàn thành, Excel là tỷ lệ nợ. Cần đảo ngược tỷ lệ nợ Excel thành tỷ lệ hoàn thành (`100.0 - excel_disc['bt']`) trước khi hiệu chuẩn.
    - **Elearning**: DB là số bài vi phạm tuyệt đối, Excel là tỷ lệ phần trăm vi phạm lớp. Giữ nguyên số bài vi phạm tuyệt đối từ DB để xét cấm thi theo Quy chế mới (không scale theo % của Excel để tránh cấm thi ảo do unit mismatch).
    - **Đọc dữ liệu Excel**: Tiêu đề các cột CC, BT, EL nằm ở Dòng 4 (dưới ngày học ở Dòng 3). Cần duyệt qua 3 cột liên tiếp (CC, BT, EL) của tất cả các cột ngày học và tính trung bình cộng để ra chỉ số vi phạm thực chất của lớp.
  - **Hệ số phạt môi trường (Peer Pressure)**: Áp dụng hệ số Env $Multiplier_{env}$ khi tỷ lệ vi phạm trung bình của lớp > 10% để điều chỉnh xác suất đỗ của từng cá nhân ($P_{final} = P_{eligible} \times Multiplier_{env}$).
- **Đầu ra yêu cầu**: Thống kê số lượng sinh viên đạt/trượt và dự đoán hiệu suất học tập của các lớp và cá nhân học viên.

### 2.4 Sub Agent 3: TaskAggregator (Phân tích Công việc & Kỷ luật tác nghiệp)
- **Nhiệm vụ**: Phân tích lỗi kỷ luật tác nghiệp của GV/TG (chậm trễ, quên điểm danh, phản hồi muộn) và tiến độ lớp học.
- **Đầu ra yêu cầu**: Điểm kỷ luật tác nghiệp của từng GV/TG.

### 2.5 Sub Agent 4: Báo cáo ngày (Daily Log Auditor)
- **Nhiệm vụ**: Phân tích tiến độ và chất lượng báo cáo ngày của GV/TG trong `data/daily_logs.txt`.
- **Đầu ra yêu cầu**: Tỷ lệ hoàn thành công việc và điểm hiệu suất báo cáo ngày.

### 2.6 Agent Hỗ Trợ 1: DataSanitizer (Làm sạch & Đồng bộ hóa Dữ liệu)
- **Nhiệm vụ**: Khởi chạy ở đầu pipeline, tự động phân tích và làm sạch dữ liệu thô (chuẩn hóa tên nhân sự không dấu, xử lý unit mismatch).
- **Quy tắc**: Tuân thủ hướng dẫn tại skill `data-cleaner-and-aligner`.

### 2.7 Agent Hỗ Trợ 2: VisualQA (Kiểm toán Giao diện Tự động)
- **Nhiệm vụ**: Chạy tự động ở cuối pipeline, sử dụng browser_subagent mô phỏng click các tab, kiểm tra lỗi console log và trắng màn hình của Master Dashboard.
- **Quy tắc**: Tuân thủ hướng dẫn tại skill `automated-visual-testing`.

### 2.8 Agent Hỗ Trợ 3: ContextPreserver (Duy trì Bối cảnh liên phiên)
- **Nhiệm vụ**: Đúc rút các lỗi kỹ thuật, quyết định thiết kế của User ở cuối phiên để tự động cập nhật vào `super_memory.md`.

## 3. Quy chuẩn Báo cáo cuối cùng (report_kpi_gv_tg.md)
Báo cáo KPI cuối cùng phải tuân theo cấu trúc sau:
1. **Tiêu đề**: Báo cáo Đánh giá KPI GV/TG Học kỳ.
2. **Bảng tổng hợp KPI**: Chứa các cột: Họ và tên, Vai trò, Lớp phụ trách, Điểm Kỷ luật SV & Tác nghiệp (40%), Điểm Học tập (30%), Điểm Báo cáo ngày (30%), Điểm KPI tổng.
3. **Đánh giá chi tiết từng cá nhân**:
   - Điểm mạnh.
   - Điểm yếu / Lỗi vi phạm đã mắc.
   - Đề xuất cải thiện cụ thể.

## 4. Quy trình Ghi nhớ (Super Memory)
Để duy trì tính liên tục của dự án qua các session khác nhau, Agent bắt buộc phải thực hiện quy trình sau:
- **Đầu session / task mới**: Đọc file [super_memory.md](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/docs/super_memory.md) để tải các quyết định thiết kế, tùy chọn giao diện và bài học kinh nghiệm trước đó.
- **Cuối session / task**: Cập nhật thông tin mới (nếu có bài học kinh nghiệm mới, điều chỉnh logic, hoặc sửa bug quan trọng) vào [super_memory.md](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/docs/super_memory.md).

