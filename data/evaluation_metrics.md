# Báo cáo Kiểm định Thuật toán & Hiệu năng Dự báo Học vụ

> [!NOTE]
> Báo cáo này là một phần của **Evaluation Harness**, đánh giá chéo trực tiếp kết quả dự đoán của mô hình với kết quả thi chốt thực tế thu được trong cơ sở dữ liệu học vụ MySQL.

## 1. Chỉ số Hiệu năng Hệ thống (Global Metrics)

| Chỉ số hiệu năng | Kết quả đạt được | Ý nghĩa lâm sàng / Vận hành |
| :--- | :---: | :--- |
| **Sai số Tuyệt đối TB (MAE)** | **9.24%** | Lệch tỷ lệ đỗ trung bình giữa dự báo và thực tế trên mỗi lớp |
| **Độ chính xác (Accuracy)** | **73.47%** | Tỷ lệ dự đoán đúng đỗ/trượt trên tổng số học sinh |
| **Độ xác thực (Precision)** | **50.00%** | Tỷ lệ học sinh thực sự trượt trong tổng số học sinh bị cảnh báo trượt (Tránh cảnh báo ảo) |
| **Độ phủ (Recall/Sensitivity)** | **38.46%** | Tỷ lệ phát hiện được học sinh trượt thực tế (Tránh bỏ sót học viên nguy cơ) |
| **Điểm F1-Score** | **0.435** | Chỉ số hài hòa cân bằng giữa Precision và Recall |

### Ma trận nhầm lẫn toàn cục (Global Confusion Matrix):
- **True Positive (TP)**: 35 học viên (Dự báo Trượt $\rightarrow$ Thực tế Trượt)
- **False Positive (FP)**: 35 học viên (Dự báo Trượt $\rightarrow$ Thực tế Đỗ - *Cảnh báo ảo*)
- **True Negative (TN)**: 217 học viên (Dự báo Đỗ $\rightarrow$ Thực tế Đỗ)
- **False Negative (FN)**: 56 học viên (Dự báo Đỗ $\rightarrow$ Thực tế Trượt - *Bỏ sót*)

## 2. Chi tiết Đánh giá theo từng lớp học

| Tên lớp | Sĩ số | Tỷ lệ Đỗ Thực tế | Tỷ lệ Đỗ Dự báo | Sai số (MAE) | TP / FP / TN / FN |
| :--- | :---: | :---: | :---: | :---: | :---: |
| [[student_risk_report#Lớp: HN-KS25-CNTT1|HN-KS25-CNTT1]] | 42 | 69.0% | 83.3% | 14.29% | 3 / 4 / 25 / 10 |
| [[student_risk_report#Lớp: HN-KS25-CNTT2|HN-KS25-CNTT2]] | 43 | 76.7% | 86.0% | 9.30% | 2 / 4 / 29 / 8 |
| [[student_risk_report#Lớp: HN-KS25-CNTT3|HN-KS25-CNTT3]] | 37 | 75.7% | 78.4% | 2.70% | 6 / 2 / 26 / 3 |
| [[student_risk_report#Lớp: HN-KS25-CNTT4|HN-KS25-CNTT4]] | 42 | 76.2% | 76.2% | 0.00% | 6 / 4 / 28 / 4 |
| [[student_risk_report#Lớp: HN-KS25-CNTT5|HN-KS25-CNTT5]] | 42 | 76.2% | 71.4% | 4.76% | 3 / 9 / 23 / 7 |
| [[student_risk_report#Lớp: HN-KS25-CNTT6|HN-KS25-CNTT6]] | 33 | 72.7% | 66.7% | 6.06% | 4 / 7 / 17 / 5 |
| [[student_risk_report#Lớp: HN-K25-QTKD1|HN-K25-QTKD1]] | 37 | 56.8% | 89.2% | 32.43% | 3 / 1 / 20 / 13 |
| [[student_risk_report#Lớp: HN-K25-QTKD2|HN-K25-QTKD2]] | 40 | 85.0% | 82.5% | 2.50% | 3 / 4 / 30 / 3 |
| [[student_risk_report#Lớp: HN-K25-QTKD3|HN-K25-QTKD3]] | 27 | 70.4% | 81.5% | 11.11% | 5 / 0 / 19 / 3 |

---

## 3. Đánh giá & Khuyến nghị Kỹ thuật từ Harness

> [!TIP]
> Thuật toán hiện tại đang hoạt động cực kỳ tốt với MAE = 9.24% (đạt mục tiêu Grid Search < 12%). Trọng số Hyperparameters hiện tại phù hợp với hành vi học tập thực tế.
> [!CAUTION]
> Độ phủ (Recall) hiện tại chỉ đạt 38.46%. Mô hình đang bỏ sót khá nhiều học sinh có nguy cơ trượt thực tế. Hãy cân nhắc nới lỏng các chốt chặn kỷ luật hoặc giảm ngưỡng an toàn của p_eligible từ 50% lên 55% để cảnh báo sớm nhạy hơn.
