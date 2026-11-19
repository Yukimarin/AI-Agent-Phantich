# Golden set — số liệu LMS Frontend đã được người dùng xác nhận

Đây là **thước đo đúng/sai** của hệ thống. Gate 2 so sánh kết quả tính toán với các file ở đây.
Không có golden set thì Gate 2 chỉ cảnh báo (WARN), chưa khẳng định được số liệu khớp LMS.

## Cách thêm

1. Mở LMS Frontend, chọn lớp-môn, ghi lại **số SV vi phạm** CC / BT / EL đang hiển thị.
2. Tạo file `tests/golden/<kỳ>.json`, ví dụ `2026-W40.json`:

```json
{
  "period": "2026-W40",
  "asOf": "2026-10-02",
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

- `tolerance.cc = 2`: API không tách vắng KP/CP/Muộn nên chấp nhận lệch tối đa 2 SV (docs/domain/quy_chuan_nghiep_vu.md mục 7.1).
- Thiếu `period` thì áp dụng cho mọi kỳ.
- `asOf` (ngày giờ VN chụp màn hình FE) — **nên có**. Số LMS đổi theo từng buổi học/bài tập, nên Gate 2 chỉ so chặt (FAIL nếu lệch) khi dữ liệu được lấy **cùng ngày**; khác ngày thì WARN kèm danh sách biến động (bài học 06/10/2026, `tests/regression/test_golden_asof.py`). Thiếu `asOf` thì luôn so chặt.
- Muốn khẳng định khớp FE cho ngày mới: chụp FE rồi chạy `pmo run --refresh` **trong cùng ngày**.

## Khi phát hiện số sai
1. Thêm/sửa mục trong golden set → Gate 2 sẽ FAIL.
2. Sửa ở `pmo/metrics/lms_fe.py` cho đến khi Gate 2 PASS.
3. Thêm một test vào `tests/regression/test_lessons.py` mô tả bài học.
