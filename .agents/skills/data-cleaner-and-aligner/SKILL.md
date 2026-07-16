---
name: data-cleaner-and-aligner
description: "Guidelines and algorithms for cleaning raw educational data, resolving unit mismatches, and normalizing Vietnamese names."
---

# Data Cleaning & Alignment Skill

## 1. Họ tên Nhân sự (Vietnamese Name Normalization)
Khi liên kết dữ liệu giữa các hệ thống (Worklane logs, Excel, SQL), họ tên tiếng Việt thường bị lệch do viết hoa/thường, khoảng trắng thừa hoặc dấu tiếng Việt.
*   **Thuật toán chuẩn hóa tên**:
    ```python
    import re
    import unicodedata

    def normalize_vietnamese_name(name):
        if not name:
            return ""
        # 1. Loại bỏ khoảng trắng thừa
        name = " ".join(name.strip().split())
        # 2. Chuyển về chữ thường
        name = name.lower()
        # 3. Loại bỏ dấu tiếng Việt (nếu cần so khớp không dấu)
        # Sử dụng unicodedata để phân tách các ký tự tổ hợp
        name = unicodedata.normalize('NFKD', name)
        name = "".join([c for c in name if not unicodedata.combining(c)])
        # Thay thế chữ đ/Đ
        name = name.replace("đ", "d")
        return name
    ```

## 2. Đồng bộ hóa đơn vị đo lường (Unit Mismatch Calibration)
*   **Quy đổi Elearning**:
    *   Trong cơ sở dữ liệu: Thường lưu số lượng bài vi phạm tuyệt đối (ví dụ: `14` bài).
    *   Trong file Excel: Thường lưu tỷ lệ phần trăm vi phạm của lớp (ví dụ: `15%`).
    *   *Quy tắc*: Giữ nguyên số bài vi phạm tuyệt đối từ DB để xét cấm thi theo Quy chế mới (không scale theo % của Excel để tránh cấm thi ảo do unit mismatch).
*   **Quy đổi Bài tập**:
    *   Trong cơ sở dữ liệu: Thường lưu tỷ lệ hoàn thành (ví dụ: `85%`).
    *   Trong file Excel: Thường lưu tỷ lệ nợ (ví dụ: `15%`).
    *   *Quy tắc*: Đảo ngược tỷ lệ nợ Excel thành tỷ lệ hoàn thành trước khi hiệu chuẩn: `completion_rate = 100.0 - excel_debt_rate`.

## 3. Quét dòng dữ liệu dị thường (Anomaly Detection)
*   Đối với file Excel chỉ số đào tạo:
    *   Dòng 3: Chứa ngày học thực tế.
    *   Dòng 4: Chứa tiêu đề cột CC, BT, EL.
    *   *Quy tắc*: Duyệt qua 3 cột liên tiếp (CC, BT, EL) của tất cả các cột ngày học để tính trung bình cộng chỉ số vi phạm thực chất của lớp, bỏ qua các ô trống hoặc chứa ký tự đặc biệt (e.g., `-`, `N/A`).
