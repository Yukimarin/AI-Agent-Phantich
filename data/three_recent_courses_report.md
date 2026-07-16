# BÁO CÁO THỐNG KÊ KẾT QUẢ HỌC TẬP & DỰ BÁO 3 MÔN GẦN NHẤT

*Báo cáo được chốt dữ liệu từ Excel backup **PTIT_Chiso.xlsx** và MySQL vào ngày 09/07/2026.*

## 📌 MỤC 1: ĐO SAI SỐ DỰ BÁO TRUNG BÌNH 3 MÔN GẦN NHẤT
Bảng dưới đây thống kê kết quả dự báo và thực tế trung bình cộng của 3 môn gần đây nhất của từng lớp học.

### 🔹 Khóa KS24-CNTT

#### 🔸 Các lớp chính quy (Regular Classes)

| Tên Lớp | Giảng viên / Trợ giảng | Dự báo trung bình% | Thực tế trung bình% | Sai số% |
| :--- | :--- | :---: | :---: | :---: |
| HN-KS24-CNTT1 | Chưa phân công / Hồ Xuân Hùng | **68.7%** | **64.8%** | +3.9% |
| HN-KS24-CNTT2 | Chưa phân công / Bùi Thanh Hải | **43.6%** | **66.7%** | -23.1% |
| HN-KS24-CNTT4 | Chưa phân công / Bùi Thanh Hải | **71.5%** | **60.4%** | +11.1% |
| HCM-KS24-CNTT1 | Nguyễn Bá Minh Đạo | **53.9%** | **84.1%** | -30.2% |
| HCM-KS24-CNTT2 | Chưa phân công / Nguyễn Bá Minh Đạo | **91.2%** | **91.5%** | -0.3% |
| HCM-KS24-CNTT3 | Chưa phân công | **91.2%** | **79.4%** | +11.8% |
| HN-KS24-CNTT3 | Chưa phân công / Bùi Thanh Hải | **45.2%** | **95.5%** | -50.2% |

👉 **Đánh giá chung khóa KS24-CNTT (Lớp Chính Quy)**: MAE = **18.66%**

#### 🔸 Các lớp học lại / Học kỳ phụ / Lớp đặc biệt (Special / Retake Classes)

| Tên Lớp | Giảng viên / Trợ giảng | Dự báo trung bình% | Thực tế trung bình% | Sai số% |
| :--- | :--- | :---: | :---: | :---: |
| HN-KS24-CNTT6	 | Chưa phân công | **83.0%** | **14.1%** | +69.0% |

👉 **Đánh giá chung khóa KS24-CNTT (Lớp Đặc Biệt)**: MAE = **69.00%**

> [!IMPORTANT]
> *Lưu ý về các lớp đặc biệt: Các lớp này thường có tỷ lệ trượt thực tế rất cao (do sinh viên bỏ thi hoặc nợ project kéo dài), mặc dù ý thức điểm danh trên lớp vẫn đối phó đầy đủ. Do đó, mô hình dự báo dựa trên kỷ luật lớp học sẽ có sai số cao hơn và cần phương án giám sát riêng biệt.*

*Đề xuất chỉ số giúp đánh giá chính xác hơn*:
- **Chỉ số nợ Project cá nhân**: Đối với các môn CNTT cốt lõi, việc trượt Project chiếm tới 80% nguyên nhân trượt môn. Cần đưa thêm trạng thái nộp bài tập lớn/Project trên Git vào mô hình.
- **Chỉ số tương tác hệ thống (LMS/Elearning)**: Số buổi đăng nhập và làm bài muộn Elearning phản ánh 85% tính tự giác học tập của lớp trước khi thi.

### 🔹 Khóa KS25-CNTT

#### 🔸 Các lớp chính quy (Regular Classes)

| Tên Lớp | Giảng viên / Trợ giảng | Dự báo trung bình% | Thực tế trung bình% | Sai số% |
| :--- | :--- | :---: | :---: | :---: |
| HN-KS25-CNTT7 | Chưa phân công / Ngọ Văn Quý | **91.2%** | **47.3%** | +43.9% |
| HN-KS25-CNTT5 | Chưa phân công / Lương Quốc Tuấn | **50.9%** | **85.7%** | -34.8% |
| HN-KS25-CNTT4 | Chưa phân công / Nguyễn Quảng An | **65.4%** | **86.9%** | -21.5% |
| HN-KS25-CNTT3 | Chưa phân công / Nguyễn Quảng An | **51.9%** | **87.8%** | -36.0% |
| HN-KS25-CNTT2 | Chưa phân công / Lương Quốc Tuấn | **40.2%** | **80.6%** | -40.5% |
| HN-KS25-CNTT1 | Chưa phân công / Trịnh Quốc Hai | **42.0%** | **83.3%** | -41.3% |
| HCM-KS25-CNTT4 | Chưa phân công / Trần Quốc Tuấn | **24.6%** | **68.9%** | -44.2% |
| HCM-KS25-CNTT3 | Chưa phân công / Nguyễn Bá Minh Đạo | **59.5%** | **63.4%** | -3.9% |
| HCM-KS25-CNTT2 | Chưa phân công / Lê Hà Thanh Sang | **11.2%** | **70.8%** | -59.6% |
| HCM-KS25-CNTT1 | Chưa phân công / Trần Quốc Tuấn | **1.5%** | **79.6%** | -78.1% |

👉 **Đánh giá chung khóa KS25-CNTT (Lớp Chính Quy)**: MAE = **40.38%**

#### 🔸 Các lớp học lại / Học kỳ phụ / Lớp đặc biệt (Special / Retake Classes)

| Tên Lớp | Giảng viên / Trợ giảng | Dự báo trung bình% | Thực tế trung bình% | Sai số% |
| :--- | :--- | :---: | :---: | :---: |
| HN-KS25-CNTT6 | Chưa phân công / Nguyễn Quảng An | **61.1%** | **80.3%** | -19.2% |
| HCM-KS25-CNTT5_HK2 | Chưa phân công / Lê Hà Thanh Sang | **47.0%** | **79.6%** | -32.6% |
| HCM-KS25-CNTT6_HK2 | Trần Quốc Tuấn / Chưa phân công | **41.0%** | **75.6%** | -34.6% |
| HCM-KS25-CNTT7_HK2 | Trần Quốc Tuấn / Chưa phân công / Lê Hà Thanh Sang | **22.4%** | **74.6%** | -52.2% |
| HCM-KS25-CNTT8_HK2 | Trần Quốc Tuấn / Chưa phân công / Lê Hà Thanh Sang | **14.0%** | **36.5%** | -22.5% |
| HN-KS25-CNTT8_HL | Tạ Quang Tùng / Chưa phân công | **55.0%** | **50.0%** | +5.0% |

👉 **Đánh giá chung khóa KS25-CNTT (Lớp Đặc Biệt)**: MAE = **27.68%**

> [!IMPORTANT]
> *Lưu ý về các lớp đặc biệt: Các lớp này thường có tỷ lệ trượt thực tế rất cao (do sinh viên bỏ thi hoặc nợ project kéo dài), mặc dù ý thức điểm danh trên lớp vẫn đối phó đầy đủ. Do đó, mô hình dự báo dựa trên kỷ luật lớp học sẽ có sai số cao hơn và cần phương án giám sát riêng biệt.*

*Đề xuất chỉ số giúp đánh giá chính xác hơn*:
- **Chỉ số nợ Project cá nhân**: Đối với các môn CNTT cốt lõi, việc trượt Project chiếm tới 80% nguyên nhân trượt môn. Cần đưa thêm trạng thái nộp bài tập lớn/Project trên Git vào mô hình.
- **Chỉ số tương tác hệ thống (LMS/Elearning)**: Số buổi đăng nhập và làm bài muộn Elearning phản ánh 85% tính tự giác học tập của lớp trước khi thi.

### 🔹 Khóa KS25-QTKD

#### 🔸 Các lớp chính quy (Regular Classes)

| Tên Lớp | Giảng viên / Trợ giảng | Dự báo trung bình% | Thực tế trung bình% | Sai số% |
| :--- | :--- | :---: | :---: | :---: |
| HN-K25-QTKD3 | Chưa phân công / Lê Thành Ngọc / Nguyễn Ngọc Vân Khanh | **11.2%** | **35.2%** | -24.0% |
| HN-K25-QTKD2 | Nguyễn Ngọc Vân Khanh | **0.0%** | **42.5%** | -42.5% |

👉 **Đánh giá chung khóa KS25-QTKD (Lớp Chính Quy)**: MAE = **33.25%**

#### 🔸 Các lớp học lại / Học kỳ phụ / Lớp đặc biệt (Special / Retake Classes)

| Tên Lớp | Giảng viên / Trợ giảng | Dự báo trung bình% | Thực tế trung bình% | Sai số% |
| :--- | :--- | :---: | :---: | :---: |
| HN-K25-QTKD1 | Chưa phân công / Lê Thành Ngọc / Nguyễn Ngọc Vân Khanh | **20.9%** | **28.4%** | -7.5% |

👉 **Đánh giá chung khóa KS25-QTKD (Lớp Đặc Biệt)**: MAE = **7.50%**

> [!IMPORTANT]
> *Lưu ý về các lớp đặc biệt: Các lớp này thường có tỷ lệ trượt thực tế rất cao (do sinh viên bỏ thi hoặc nợ project kéo dài), mặc dù ý thức điểm danh trên lớp vẫn đối phó đầy đủ. Do đó, mô hình dự báo dựa trên kỷ luật lớp học sẽ có sai số cao hơn và cần phương án giám sát riêng biệt.*

*Đề xuất chỉ số giúp đánh giá chính xác hơn*:
- **Chỉ số nợ Project cá nhân**: Đối với các môn CNTT cốt lõi, việc trượt Project chiếm tới 80% nguyên nhân trượt môn. Cần đưa thêm trạng thái nộp bài tập lớn/Project trên Git vào mô hình.
- **Chỉ số tương tác hệ thống (LMS/Elearning)**: Số buổi đăng nhập và làm bài muộn Elearning phản ánh 85% tính tự giác học tập của lớp trước khi thi.


---

## 📌 MỤC 2: DỰ BÁO QUA MÔN HIỆN TẠI DỰA TRÊN KẾT QUẢ MÔN TRƯỚC (GẦN NHẤT)
Bảng dưới đây lấy kết quả thực tế môn trước làm đầu vào để dự đoán tỷ lệ qua môn ở môn hiện tại (môn thứ 3). Nếu môn hiện tại chưa có điểm Hackathon, mô hình dự đoán hoàn toàn dựa trên kết quả môn trước.

### 🔹 Khóa KS24-CNTT

| Tên Lớp | GV Môn Hiện Tại | Môn Trước | Thực tế Trước% | Môn Hiện Tại | Hackathon Hiện Tại | Dự báo Hiện Tại% | Thực tế Hiện Tại% | Sai số |
| :--- | :--- | :--- | :---: | :--- | :---: | :---: | :---: | :---: |
| HN-KS24-CNTT1 | Hồ Xuân Hùng | Java Web Application (KS24) | 88.2% | AI (KS24) | 80.9% | **48.3%** | **0.0%** | +48.3% |
| HN-KS24-CNTT2 | Bùi Thanh Hải | Java Web Application (KS24) | 92.3% | AI (KS24) | 82.3% | **63.4%** | **5.1%** | +58.3% |
| HN-KS24-CNTT4 | Bùi Thanh Hải | Java Web Application (KS24) | 96.6% | AI (KS24) | 80.1% | **62.8%** | **0.0%** | +62.8% |
| HCM-KS24-CNTT1 | Nguyễn Bá Minh Đạo | Java Web Application (KS24) | 93.2% | AI (KS24) | Chưa thi | **63.1%** | **Chưa kết thúc** | N/A |
| HN-KS24-CNTT3 | Bùi Thanh Hải | Java Web Application (KS24) | 90.9% | AI (KS24) | 65.0% | **0.0%** | **Chưa kết thúc** | N/A |

👉 **Đánh giá chung khóa KS24-CNTT**: MAE dự báo môn hiện tại = **56.47%**

### 🔹 Khóa KS25-CNTT

| Tên Lớp | GV Môn Hiện Tại | Môn Trước | Thực tế Trước% | Môn Hiện Tại | Hackathon Hiện Tại | Dự báo Hiện Tại% | Thực tế Hiện Tại% | Sai số |
| :--- | :--- | :--- | :---: | :--- | :---: | :---: | :---: | :---: |
| HN-KS25-CNTT6 | Nguyễn Quảng An | Python (KS25) | 28.6% | Python Web (KS25) | 51.9% | **33.9%** | **60.6%** | -26.7% |
| HN-KS25-CNTT5 | Lương Quốc Tuấn | Python (KS25) | 30.0% | Python Web (KS25) | 66.7% | **0.0%** | **71.4%** | -71.4% |
| HN-KS25-CNTT4 | Nguyễn Quảng An | Python (KS25) | 50.0% | Python Web (KS25) | 62.1% | **47.1%** | **73.8%** | -26.7% |
| HN-KS25-CNTT3 | Nguyễn Quảng An | Python (KS25) | 53.8% | Python Web (KS25) | 61.4% | **0.0%** | **75.7%** | -75.7% |
| HN-KS25-CNTT2 | Trịnh Quốc Hai | Python (KS25) | 34.9% | Python Web (KS25) | 72.2% | **0.0%** | **65.1%** | -65.1% |
| HN-KS25-CNTT1 | Lương Quốc Tuấn | Python (KS25) | 56.2% | Python Web (KS25) | 59.1% | **0.0%** | **66.7%** | -66.7% |
| HCM-KS25-CNTT5_HK2 | Lê Hà Thanh Sang | Python (KS25) | 69.2% | Python Web (KS25) | 70.8% | **63.5%** | **69.2%** | -5.7% |
| HCM-KS25-CNTT6_HK2 | Trần Quốc Tuấn | Python (KS25) | 65.8% | Python Web (KS25) | 58.5% | **48.0%** | **65.8%** | -17.8% |
| HCM-KS25-CNTT7_HK2 | Trần Quốc Tuấn | Python (KS25) | 68.8% | Python Web (KS25) | 54.7% | **0.0%** | **68.8%** | -68.8% |
| HCM-KS25-CNTT8_HK2 | Lê Hà Thanh Sang | Python (KS25) | 38.9% | Python Web (KS25) | 42.2% | **0.0%** | **38.9%** | -38.9% |
| HN-KS25-CNTT8_HL | Tạ Quang Tùng | Python (KS25) | 0.0% | Python Web (KS25) | 63.9% | **16.2%** | **0.0%** | +16.2% |

👉 **Đánh giá chung khóa KS25-CNTT**: MAE dự báo môn hiện tại = **43.61%**

### 🔹 Khóa KS25-QTKD

| Tên Lớp | GV Môn Hiện Tại | Môn Trước | Thực tế Trước% | Môn Hiện Tại | Hackathon Hiện Tại | Dự báo Hiện Tại% | Thực tế Hiện Tại% | Sai số |
| :--- | :--- | :--- | :---: | :--- | :---: | :---: | :---: | :---: |
| HN-K25-QTKD3 | Nguyễn Ngọc Vân Khanh | DTB201 (KS25) | 70.4% | DTB202 (KS25) | Chưa thi | **0.0%** | **0.0%** | +0.0% |
| HN-K25-QTKD2 | Nguyễn Ngọc Vân Khanh | DTB201 (KS25) | 85.0% | DTB202 (KS25) | Chưa thi | **0.0%** | **0.0%** | +0.0% |
| HN-K25-QTKD1 | Lê Thành Ngọc | DTB201 (KS25) | 56.8% | DTB202 (KS25) | Chưa thi | **30.9%** | **0.0%** | +30.9% |

👉 **Đánh giá chung khóa KS25-QTKD**: MAE dự báo môn hiện tại = **10.30%**

