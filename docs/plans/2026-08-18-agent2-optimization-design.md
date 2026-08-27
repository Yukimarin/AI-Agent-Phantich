# Tài liệu Thiết kế: Tối ưu hóa và Hiệu chuẩn Tự động Bộ tham số Dự báo Học vụ (Agent 2)

- **Ngày tạo**: 18/08/2026
- **Tác giả**: Antigravity
- **Trạng thái**: Đã phê duyệt bởi User

---

## 1. Bối cảnh & Mục tiêu

### Bối cảnh
Hệ thống dự báo học vụ (Agent 2 - AcademicPredictor) trước đó sử dụng các tham số dự báo (trọng số, hệ số scale, ngưỡng cấm thi) được thiết lập tĩnh (hardcoded) dựa trên Heuristics sơ khởi. Khi có dữ liệu cơ sở dữ liệu QLĐT mới nhất (`qldt_el` dump 1.25 GB), chúng ta cần đối chiếu kết quả dự báo của mô hình với kết quả thực tế (Đỗ/Trượt) đã xảy ra để đánh giá sai số và hiệu chuẩn lại bộ tham số.

### Mục tiêu
- Xây dựng quy trình tự động hiệu chuẩn (Feedback Loop) để tìm bộ tham số dự báo tối ưu trên toàn bộ các khối (KS24 CNTT, KS25 CNTT, KS25 QTKD).
- Đưa sai số dự báo tỷ lệ đỗ lớp học và tỷ lệ nhận diện sai sinh viên nguy cơ về **quanh mức 5%**.
- Tích hợp động bộ tham số tối ưu vào Agent 2 mà không làm ảnh hưởng đến cấu trúc pipeline hiện tại.

---

## 2. Thiết kế Kỹ thuật

### 2.1 Luồng dữ liệu hiệu chuẩn (Calibration Data Flow)

Quy trình hiệu chuẩn được thực thi thông qua script độc lập `agents/core/agent_2_academic_pred/calibrate_weights.py`.

```
[MySQL qldt_el] 
      │
      ▼ (Lấy dữ liệu các lớp & môn học đã hoàn thành)
[calibrate_weights.py] ──(Grid Search & Cực tiểu hóa Loss)──► [Tìm bộ tham số tối ưu]
      │                                                                  │
      │                                                                  ▼
      │                                                     [course_metadata.json]
      │                                                                  │
      ▼ (Đọc cấu hình động tại runtime)                                  │
[Agent 2 run.py] ◄───────────────────────────────────────────────────────┘
      │
      ▼
[Báo cáo dự báo chính xác cao (Sai số < 5%)]
```

### 2.2 Giải thuật Tối ưu hóa (Hyperparameter Grid Search)

Script `calibrate_weights.py` sẽ thực hiện quét cạn (Grid Search) trên không gian tham số của từng khối học:

1. **Không gian quét tham số**:
   - `w1, w2` (Trọng số môn học trước vs Điểm thi/Project): Quét từ `0.0` đến `1.0` với bước nhảy `0.1` (thỏa mãn $w1 + w2 = 1.0$).
   - `p_hack_mult` (Hệ số nhân điểm Hackathon/Project): Quét từ `1.0` đến `1.5` với bước nhảy `0.05`.
   - `base_scale` (Hệ số scale nền của lớp): Quét từ `0.8` đến `1.1` với bước nhảy `0.05`.
   - `env_threshold` (Ngưỡng vi phạm lớp bắt đầu phạt): Quét từ `5.0%` đến `15.0%` với bước nhảy `2.5%`.

2. **Hàm mất mát tối ưu hóa (Loss Function)**:
   Để cân bằng giữa độ chính xác ở cấp độ báo cáo quản trị (lớp học) và cấp độ hành động can thiệp (cá nhân sinh viên), hàm Loss được định nghĩa như sau:
   
   $$\text{Loss} = 0.6 \times \text{Misclassification Rate} + 0.4 \times \text{Class Pass Rate MAE}$$
   
   *Trong đó:*
   - $\text{Misclassification Rate} = \frac{\text{Số sinh viên bị dự báo sai nhãn Đỗ/Trượt}}{\text{Tổng số sinh viên kiểm tra}}$ (Cực tiểu hóa lỗi bỏ sót sinh viên phát sinh trượt).
   - $\text{Class Pass Rate MAE} = \frac{1}{M}\sum_{i=1}^{M} |P_{\text{pred}, i} - P_{\text{actual}, i}|$ (Sai lệch trung bình giữa tỷ lệ đỗ dự báo và tỷ lệ đỗ thực tế của các lớp).

3. **Ghi nhận cấu hình**:
   Bộ tham số có Loss thấp nhất cho từng khối (`KS24`, `KS25`, `QTKD`) sẽ được lưu vào file cấu hình `data/inputs/course_metadata.json` theo định dạng:
   ```json
   {
     "KS24": {
       "w1": 0.3,
       "w2": 0.7,
       "p_hack_mult": 1.2,
       "base_scale": 0.95,
       "env_threshold": 10.0
     },
     "KS25": { ... },
     "QTKD": { ... }
   }
   ```

### 2.3 Sửa đổi tích hợp trong Agent 2 (`run.py`)

- **Đọc cấu hình động**: Thay vì các dòng lệnh gán cứng tham số, Agent 2 sẽ đọc từ `data/inputs/course_metadata.json`.
- **Logic tự động Fallback**: Nếu không tìm thấy file cấu hình hoặc cấu hình thiếu khối tương ứng, hệ thống tự động sử dụng bộ tham số mặc định an toàn trước đây để chạy tiếp mà không gây crash pipeline.

---

## 3. Kế hoạch Xác minh & Tiêu chí Thành công

- **Tiêu chí thành công**:
  - Script hiệu chuẩn chạy thành công và xuất ra file cấu hình hợp lệ.
  - Tỷ lệ sai số trung bình (Class Pass Rate MAE) trên dữ liệu lịch sử đạt **dưới 5%**.
  - Tỷ lệ dự báo sai nhãn sinh viên (Misclassification Rate) giảm đáng kể so với trước khi hiệu chuẩn.
  - Pipeline chạy trơn tru với file cấu hình mới mà không phát sinh lỗi.
