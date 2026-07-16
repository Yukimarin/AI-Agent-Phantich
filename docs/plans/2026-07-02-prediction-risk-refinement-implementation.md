# Tinh chỉnh Dự báo & Phân loại Sinh viên Yếu Implementation Plan

> **For Antigravity:** REQUIRED WORKFLOW: Use `.agent/workflows/execute-plan.md` to execute this plan in single-flow mode.

**Goal:** Loại bỏ cảnh báo cấm thi ảo do môn học trước, làm mịn điểm năng lực môn tiên quyết dựa trên điểm thi thực tế, và phân loại danh sách sinh viên yếu thành 2 nhóm Kỷ luật (Cấm thi) và Học lực (Nguy cơ trượt) để nâng cao độ chính xác dự báo và hiệu quả hỗ trợ giáo vụ.

**Architecture:** 
1. Sửa `scratch/analyze_student_risk_real.py` để loại bỏ `is_prev_forbidden_hard` khỏi phần cấm thi môn hiện tại, bổ sung check cấm thi kỷ luật môn hiện tại (chuyên cần, bài tập, Elearning, Rpoint), làm mịn điểm năng lực môn trước dựa trên điểm trung bình thi thực tế, và phân loại Markdown đầu ra thành 2 bảng riêng biệt cho mỗi lớp.
2. Sửa `scratch/run_academic_predictions_v3.py` và `scratch/generate_three_recent_courses_report.py` để đồng bộ hóa logic tính điểm năng lực học tập môn trước mịn hơn (dựa trên điểm thi thực tế thay vì nhị phân 0-1) nhằm cải thiện độ chính xác dự báo lớp học (MAE).

**Tech Stack:** Python 3, mysql-connector-python, openpyxl, numpy

---

## Proposed Changes

### Component 1: Tinh chỉnh danh sách sinh viên yếu (Student Risk Analysis)

#### [MODIFY] [analyze_student_risk_real.py](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/scratch/analyze_student_risk_real.py)
*   Sửa logic tính điểm năng lực học tập môn trước mịn hơn: Lấy điểm thi trung bình thực tế môn trước quy đổi làm baseline thay vì nhị phân 0-1.
*   Bỏ chốt chặn cấm thi môn hiện tại do môn trước (`is_prev_forbidden_hard = True` không làm `is_failed = True` môn hiện tại).
*   Thêm Rpoint môn hiện tại < 80 vào diện cấm thi kỷ luật môn hiện tại (khi số buổi > 3).
*   Phân chia sinh viên có nguy cơ thành 2 nhóm: Nhóm Kỷ luật (Cấm thi) và Nhóm Học lực (Nguy cơ trượt).
*   Xuất bản định dạng bảng Markdown mới chia rõ 2 nhóm này dưới mỗi lớp học.

---

### Component 2: Đồng bộ hóa Mô hình Dự báo Lớp học (Class Prediction Model)

#### [MODIFY] [run_academic_predictions_v3.py](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/scratch/run_academic_predictions_v3.py)
*   Sửa logic tính `prev_student_pass` từ nhị phân (0.0 hoặc 1.0) sang tỷ lệ điểm thi thực tế môn trước (0.0 đến 1.0) để làm mịn năng lực học tập đầu vào.

#### [MODIFY] [generate_three_recent_courses_report.py](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/scratch/generate_three_recent_courses_report.py)
*   Đồng bộ hóa cách tính `prereq_fail` hoặc `prev_actual_pass` và các trọng số dự báo tương tự như trên nhằm đảm bảo sai số MAE chênh lệch tối thiểu và thống nhất mô hình.

---

## Detailed Tasks

### Task 1: Sửa logic cấm thi và làm mịn điểm năng lực môn trước trong analyze_student_risk_real.py

**Files:**
*   Modify: [analyze_student_risk_real.py](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/scratch/analyze_student_risk_real.py)

**Step 1: Cập nhật logic tính P_prereq và bỏ cấm thi do môn trước**
Tìm đoạn code tính `P_prereq` và `is_prev_forbidden_hard` từ dòng 366-407:
```python
            is_prev_forbidden_hard = False
            prev_fr = student_pass_history.get((sid, prev_co_id)) if (prev_co_id and prev_co_id != co_id) else None
            if prev_fr:
                ...
                if prev_att > 30.0 or is_prev_failed_hard_test:
                    is_prev_forbidden_hard = True
                    P_prereq = 0.0
                else:
                    ...
```
Sửa lại để `is_prev_forbidden_hard` không còn làm cấm thi môn hiện tại, và làm mịn `P_prereq` bằng cách sử dụng điểm thi môn trước thực tế làm baseline thay vì 100%.

**Step 2: Cập nhật logic check kỷ luật môn hiện tại**
Sửa phần `CRITERIA CHECKS` ở dòng 425-455:
*   Loại bỏ check `if is_prev_forbidden_hard: is_failed = True`.
*   Thêm kiểm tra Rpoint môn hiện tại < 80 (`discipline_val < 80.0`) vào diện cấm thi kỷ luật môn hiện tại.
*   Gán lý do rõ ràng cho từng nhóm kỷ luật hoặc học lực.

**Step 3: Phân loại sinh viên và xuất báo cáo chia bảng**
*   Phân loại sinh viên nguy cơ thành `discipline_risks` và `academic_risks`.
*   Sửa code render Markdown ở cuối file (dòng 500 trở đi) để in ra 2 bảng riêng biệt cho mỗi lớp học ứng với 2 nhóm nguy cơ trên.

---

### Task 2: Đồng bộ hóa logic làm mịn điểm môn trước trong run_academic_predictions_v3.py

**Files:**
*   Modify: [run_academic_predictions_v3.py](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/scratch/run_academic_predictions_v3.py)

**Step 1: Tính điểm trung bình thi môn trước thực tế**
*   Tìm và sửa đoạn lấy `prev_student_pass` ở dòng 382-389. Thay vì lấy nhị phân từ `student_pass_history`, ta truy vấn điểm thi trung bình thực tế môn trước của sinh viên đó trong DB và quy đổi về thang điểm 0.0 - 1.0.

---

### Task 3: Đồng bộ hóa logic dự báo lớp học trong generate_three_recent_courses_report.py

**Files:**
*   Modify: [generate_three_recent_courses_report.py](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/scratch/generate_three_recent_courses_report.py)

**Step 1: Đồng bộ hóa cách tính và kiểm chứng dự báo**
*   Sửa đổi cách tính toán điểm môn trước của lớp học và hiệu chỉnh mô hình cho đồng bộ với cải tiến trên để đảm bảo báo cáo Dashboard đầu ra khớp chính xác với kết quả phân tích.

---

## Verification Plan

### Automated Verification
Chạy lại các script phân tích và báo cáo để kiểm tra kết quả đầu ra:
1. Chạy phân tích sinh viên yếu:
   `uv run --with mysql-connector-python --with openpyxl --with numpy scratch/analyze_student_risk_real.py`
   *Kết quả mong đợi:* Script hoàn thành không lỗi. File [data/student_risk_report.md](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/data/student_risk_report.md) được cập nhật và chứa danh sách sinh viên được phân chia rõ ràng làm 2 nhóm (Kỷ luật & Học lực) dưới mỗi lớp học. Không còn sinh viên đi học đầy đủ bị ghi cấm thi ảo.
2. Chạy dự báo tỷ lệ qua môn:
   `uv run --with mysql-connector-python --with openpyxl --with numpy scratch/run_academic_predictions_v3.py`
   *Kết quả mong đợi:* Báo cáo dự báo được cập nhật thành công, sai số MAE của các khóa được in ra đầy đủ và ổn định.
3. Chạy xuất báo cáo Dashboard:
   `uv run --with mysql-connector-python --with openpyxl --with numpy scratch/generate_three_recent_courses_report.py`
   *Kết quả mong đợi:* Báo cáo `data/three_recent_courses_report.md` được cập nhật chính xác với các dự báo tương thích.
