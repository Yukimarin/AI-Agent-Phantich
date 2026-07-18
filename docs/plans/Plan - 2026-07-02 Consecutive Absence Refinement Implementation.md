# Kế hoạch Triển khai: Dự báo Cải tiến với Kỷ luật Đa môn, Phạt Nghỉ/Nợ Liên tiếp và Xử lý Học viên Bảo lưu

> **For Antigravity:** REQUIRED WORKFLOW: Use `.agent/workflows/execute-plan.md` to execute this plan in single-flow mode.

**Goal:** Tích hợp logic xử lý kỷ luật đa môn, phạt nghỉ/nợ liên tiếp ở môn hiện tại, nhận diện học viên bảo lưu, ước lượng điểm thi tối ưu và đồng bộ hóa tỷ lệ dự báo lớp học từ trung bình cộng xác suất học viên.

**Architecture:**
1. Sửa `scratch/analyze_student_risk_real.py` để:
   * Tìm Rpoint của tối đa 2 môn trước làm điểm kỷ luật môn trước (\(discipline\_prev\)).
   * Nhận diện học viên bảo lưu (không học 2 môn gần nhất) để gán mặc định \(P_{prev\_student} = 50.0\), \(discipline\_prev = 70.0\) và nhân phạt thích nghi `0.85`.
   * Ước lượng điểm thi Hackathon môn hiện tại (khi chưa thi) bằng `0.65 * P_prev + 0.35 * discipline_curr`.
   * Truy vấn chuỗi nghỉ/nợ liên tiếp gần nhất và phạt nhân xác suất đỗ (phạt `0.5` cho nghỉ liên tiếp >= 2 buổi, `0.6` cho nợ bài tập liên tiếp >= 2 bài).
2. Sửa `scratch/run_academic_predictions_v3.py` để đồng bộ mô hình tính toán cá nhân tương tự như trên. Đồng thời, tính tỷ lệ dự báo đỗ của lớp bằng trung bình cộng xác suất đỗ của từng học viên.
3. Sửa `scratch/generate_three_recent_courses_report.py` để cập nhật cả Mục 1 và Mục 2 của Dashboard, tính tỷ lệ qua môn dự báo của lớp học bằng trung bình cộng xác suất đỗ cá nhân thực tế lấy từ DB.

**Tech Stack:** Python 3, mysql-connector-python, openpyxl, numpy

---

## Proposed Changes

### Component 1: Tinh chỉnh Mô hình Học viên Cá nhân (analyze_student_risk_real.py)

#### [MODIFY] [analyze_student_risk_real.py](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/scratch/analyze_student_risk_real.py)
*   Sửa logic tìm sequence các môn học của lớp để tự động lấy điểm Rpoint của tối đa 2 môn gần nhất tính trung bình.
*   Bổ sung logic check bảo lưu: Nếu học viên không có điểm ở cả 2 môn gần nhất của lớp, gán mặc định học lực `50.0`, kỷ luật `70.0` và hệ số phạt thích nghi `0.85`.
*   Cập nhật công thức ước lượng điểm thi Hackathon môn hiện tại: `0.65 * P_prev + 0.35 * discipline_curr`.
*   Thêm truy vấn database và duyệt ngược lịch sử điểm danh và bài tập của môn hiện tại để đếm chuỗi nghỉ/nợ liên tiếp gần nhất và áp dụng hệ số phạt tương ứng (`0.5` và `0.6`).
*   Đồng bộ hóa cách tính \(p\_eligible\) hiệu chỉnh cuối cùng và lý do hiển thị tương ứng.

---

### Component 2: Đồng bộ hóa Dự báo Lớp học (run_academic_predictions_v3.py & generate_three_recent_courses_report.py)

#### [MODIFY] [run_academic_predictions_v3.py](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/scratch/run_academic_predictions_v3.py)
*   Đồng bộ logic tính toán cá nhân (Rpoint 1-2 môn gần nhất, check bảo lưu, phạt nghỉ/nợ liên tiếp, ước lượng điểm thi).
*   Sửa đổi cách tính dự báo tỷ lệ đỗ lớp học `pred_pass_rate_old` and `pred_pass_rate_new` thành trung bình cộng xác suất đỗ của từng sinh viên trong lớp thay vì Class-level Model cũ.

#### [MODIFY] [generate_three_recent_courses_report.py](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/scratch/generate_three_recent_courses_report.py)
*   Sửa đổi hoàn toàn Mục 1 và Mục 2: Sử dụng logic tính trung bình cộng xác suất đỗ cá nhân từ DB (gồm đầy đủ các biến số kỷ luật đa môn, bảo lưu, nghỉ/nợ liên tiếp và ước lượng điểm thi) để làm tỷ lệ dự báo qua môn của các lớp học ứng với các môn học lịch sử và môn học hiện tại.

---

## Detailed Tasks

### Task 1: Sửa logic mô hình cá nhân trong analyze_student_risk_real.py

**Files:**
*   Modify: [analyze_student_risk_real.py](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/scratch/analyze_student_risk_real.py)

*   **Step 1: Truy vấn chuỗi điểm danh và bài tập đầy đủ chi tiết của sinh viên**
    *   Truy vấn chi tiết điểm danh và bài tập môn hiện tại sắp xếp theo thời gian để chuẩn bị cho việc đếm chuỗi nghỉ/nợ liên tiếp gần nhất.
*   **Step 2: Cập nhật logic Rpoint 2 môn gần nhất & check bảo lưu**
    *   Tự động xác định 2 môn gần nhất của lớp. Kiểm tra xem sinh viên có điểm ở 2 môn này không. Nếu không, gán diện bảo lưu (\(P_{prev\_student} = 50.0\), \(discipline\_prev = 70.0\), \(penalty\_resumption = 0.85\)). Nếu có, tính trung bình Rpoint môn trước.
*   **Step 3: Ước lượng điểm thi Hackathon và đếm chuỗi nghỉ/nợ liên tiếp**
    *   Ước lượng điểm Hackathon bằng tỷ lệ 65-35 nếu chưa có điểm thi.
    *   Duyệt ngược danh sách điểm danh và bài tập để tính chuỗi nghỉ/nợ liên tiếp và áp phạt `0.5` / `0.6`.
*   **Step 4: Cập nhật xác suất đỗ hiệu chỉnh và lý do cảnh báo**
    *   Nhân các hệ số phạt thích nghi, nghỉ/nợ liên tiếp vào \(p\_eligible\). Cập nhật lý do hiển thị chi tiết.

---

### Task 2: Đồng bộ hóa logic và tính trung bình cộng xác suất lớp học trong run_academic_predictions_v3.py

**Files:**
*   Modify: [run_academic_predictions_v3.py](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/scratch/run_academic_predictions_v3.py)

*   **Step 1: Đồng bộ logic tính toán cá nhân mịn**
    *   Áp dụng các logic tương tự Task 1 cho từng học viên khi tính toán dự báo.
*   **Step 2: Tính tỷ lệ dự báo đỗ của lớp**
    *   Thay đổi cách tính tỷ lệ qua môn dự báo của lớp học bằng trung bình cộng xác suất đỗ cá nhân của các sinh viên trong lớp học đó.

---

### Task 3: Sửa đổi và đồng bộ hóa báo cáo lớp học trong generate_three_recent_courses_report.py

**Files:**
*   Modify: [generate_three_recent_courses_report.py](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/scratch/generate_three_recent_courses_report.py)

*   **Step 1: Áp dụng mô hình dự báo cá nhân cho Dashboard lớp học**
    *   Thay thế toàn bộ logic Class-level Model cũ bằng việc chạy mô hình cá nhân chi tiết (với đầy đủ các chỉ số kỷ luật đa môn, bảo lưu, nghỉ/nợ liên tiếp và ước lượng điểm thi) cho từng sinh viên trong lớp học, từ đó lấy trung bình cộng làm tỷ lệ dự báo qua môn của lớp ở cả Mục 1 và Mục 2.

---

## Verification Plan

### Automated Verification
Chạy lại các script phân tích và báo cáo để kiểm tra kết quả đầu ra:
1. Chạy phân tích sinh viên yếu:
   `uv run --with mysql-connector-python --with openpyxl --with numpy scratch/analyze_student_risk_real.py`
2. Chạy dự báo tỷ lệ qua môn:
   `uv run --with mysql-connector-python --with openpyxl --with numpy scratch/run_academic_predictions_v3.py`
3. Chạy xuất báo cáo Dashboard:
   `uv run --with mysql-connector-python --with openpyxl --with numpy scratch/generate_three_recent_courses_report.py`
4. Xuất HTML Dashboard:
   `uv run --with markdown --with requests scratch/export_prediction_html.py`


---
Trở về: [[Bản đồ Tri thức MOC|Bản đồ Tri thức dự án]]
