# Báo cáo Kiểm định Thuật toán & Hiệu năng Dự báo Học vụ

> [!NOTE]
> Báo cáo này là một phần của **Evaluation Harness**, đánh giá chéo trực tiếp kết quả dự đoán của mô hình với kết quả thi chốt thực tế thu được trong cơ sở dữ liệu học vụ MySQL.

## 1. Chỉ số Hiệu năng Hệ thống (Global Metrics)

| Chỉ số hiệu năng | Kết quả đạt được | Ý nghĩa lâm sàng / Vận hành |
| :--- | :---: | :--- |
| **Sai số Tuyệt đối TB (MAE)** | **11.49%** | Lệch tỷ lệ đỗ trung bình giữa dự báo và thực tế trên mỗi lớp |
| **Độ chính xác (Accuracy)** | **79.12%** | Tỷ lệ dự đoán đúng đỗ/trượt trên tổng số học sinh |
| **Độ xác thực (Precision)** | **57.26%** | Tỷ lệ học sinh thực sự trượt trong tổng số học sinh bị cảnh báo trượt (Tránh cảnh báo ảo) |
| **Độ phủ (Recall/Sensitivity)** | **55.91%** | Tỷ lệ phát hiện được học sinh trượt thực tế (Tránh bỏ sót học viên nguy cơ) |
| **Điểm F1-Score** | **0.566** | Chỉ số hài hòa cân bằng giữa Precision và Recall |

### Ma trận nhầm lẫn toàn cục (Global Confusion Matrix):
- **True Positive (TP)**: 71 học viên (Dự báo Trượt $\rightarrow$ Thực tế Trượt)
- **False Positive (FP)**: 53 học viên (Dự báo Trượt $\rightarrow$ Thực tế Đỗ - *Cảnh báo ảo*)
- **True Negative (TN)**: 342 học viên (Dự báo Đỗ $\rightarrow$ Thực tế Đỗ)
- **False Negative (FN)**: 56 học viên (Dự báo Đỗ $\rightarrow$ Thực tế Trượt - *Bỏ sót*)

## 2. Chi tiết Đánh giá theo từng lớp học

| Tên lớp | Sĩ số | Tỷ lệ Đỗ Thực tế | Tỷ lệ Đỗ Dự báo | Sai số (MAE) | TP / FP / TN / FN |
| :--- | :---: | :---: | :---: | :---: | :---: |
| [[student_risk_report#Lớp: HN-KS24-CNTT1|HN-KS24-CNTT1]] | 35 | 94.3% | 71.4% | 22.86% | 2 / 8 / 25 / 0 |
| [[student_risk_report#Lớp: HN-KS24-CNTT2|HN-KS24-CNTT2]] | 39 | 94.9% | 100.0% | 5.13% | 0 / 0 / 37 / 2 |
| [[student_risk_report#Lớp: HN-KS24-CNTT3|HN-KS24-CNTT3]] | 33 | 90.9% | 57.6% | 33.33% | 2 / 3 / 27 / 1 |
| [[student_risk_report#Lớp: HN-KS24-CNTT4|HN-KS24-CNTT4]] | 32 | 81.2% | 84.4% | 3.12% | 3 / 2 / 24 / 3 |
| [[student_risk_report#Lớp: HCM-KS24-CNTT1|HCM-KS24-CNTT1]] | 40 | 75.0% | 90.0% | 15.00% | 1 / 1 / 29 / 9 |
| [[student_risk_report#Lớp: HN-KS25-CNTT1|HN-KS25-CNTT1]] | 42 | 66.7% | 50.0% | 16.67% | 9 / 12 / 16 / 5 |
| [[student_risk_report#Lớp: HN-KS25-CNTT2|HN-KS25-CNTT2]] | 43 | 65.1% | 88.4% | 23.26% | 4 / 1 / 27 / 11 |
| [[student_risk_report#Lớp: HN-KS25-CNTT3|HN-KS25-CNTT3]] | 37 | 75.7% | 75.7% | 0.00% | 6 / 3 / 25 / 3 |
| [[student_risk_report#Lớp: HN-KS25-CNTT4|HN-KS25-CNTT4]] | 42 | 73.8% | 78.6% | 4.76% | 7 / 2 / 29 / 4 |
| [[student_risk_report#Lớp: HN-KS25-CNTT5|HN-KS25-CNTT5]] | 42 | 71.4% | 81.0% | 9.52% | 3 / 5 / 25 / 9 |
| [[student_risk_report#Lớp: HN-KS25-CNTT6|HN-KS25-CNTT6]] | 33 | 60.6% | 48.5% | 12.12% | 10 / 7 / 13 / 3 |
| [[student_risk_report#Lớp: HN-K25-QTKD1|HN-K25-QTKD1]] | 37 | 56.8% | 59.5% | 2.70% | 13 / 2 / 19 / 3 |
| [[student_risk_report#Lớp: HN-K25-QTKD2|HN-K25-QTKD2]] | 40 | 85.0% | 80.0% | 5.00% | 5 / 3 / 31 / 1 |
| [[student_risk_report#Lớp: HN-K25-QTKD3|HN-K25-QTKD3]] | 27 | 70.4% | 63.0% | 7.41% | 6 / 4 / 15 / 2 |

---

## 3. Đánh giá & Khuyến nghị Kỹ thuật từ Harness

> [!TIP]
> Thuật toán hiện tại đang hoạt động cực kỳ tốt với MAE = 11.49% (đạt mục tiêu Grid Search < 12%). Trọng số Hyperparameters hiện tại phù hợp với hành vi học tập thực tế.
> [!CAUTION]
> Độ phủ (Recall) hiện tại chỉ đạt 55.91%. Mô hình đang bỏ sót khá nhiều học sinh có nguy cơ trượt thực tế. Hãy cân nhắc nới lỏng các chốt chặn kỷ luật hoặc giảm ngưỡng an toàn của p_eligible từ 50% lên 55% để cảnh báo sớm nhạy hơn.
