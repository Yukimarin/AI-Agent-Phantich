# Golden set — số liệu LMS Frontend đã được người dùng xác nhận

Đây là **thước đo đúng/sai** của hệ thống. Gate 2 so sánh kết quả tính toán với các file ở đây.
Không có golden set thì Gate 2 chỉ cảnh báo (WARN), chưa khẳng định được số liệu khớp LMS.

## Cách thêm

1. Mở LMS Frontend, chọn lớp-môn, ghi lại **số SV vi phạm** CC / BT / EL đang hiển thị.
2. Tạo file `tests/golden/<kỳ>.json`, ví dụ `2026-W40.json`:

```json
{
  "period": "2026-W40",
  "confirmedBy": "Tên người xác nhận",
  "items": [
    {
      "className": "HN-KS26-CNTT1",
      "courseCode": "IT108-K26",
      "cc_count": 4,
      "bt_count": 2,
      "el_count": 7,
      "tolerance": {"cc": 2}
    }
  ]
}
```

- `tolerance.cc = 2`: API không tách vắng KP/CP/Muộn nên chấp nhận lệch tối đa 2 SV (super_memory mục 7.1).
- Bỏ `period` nếu muốn áp dụng cho mọi kỳ.

## Khi phát hiện số sai
1. Thêm/sửa mục trong golden set → Gate 2 sẽ FAIL.
2. Sửa ở `pmo/metrics/lms_fe.py` cho đến khi Gate 2 PASS.
3. Thêm một test vào `tests/regression/test_lessons.py` mô tả bài học.
