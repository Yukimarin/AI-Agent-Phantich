---
name: run-analytics
description: Use when the user asks to fetch data and analyze / produce statistics or reports ("lấy dữ liệu và phân tích", "thống kê tuần này", "chạy báo cáo", "cập nhật số liệu", "đánh giá chỉ số lớp"). Runs the PMO Data Hub pipeline with verification gates instead of ad-hoc scripts.
---

# Run Analytics (PMO Data Hub)

## Nguyên tắc bắt buộc
- **Script tính, AI nhận định.** KHÔNG tự tính CC/BT/EL, KHÔNG gọi LMS/Worklane trực tiếp, KHÔNG sửa số trong HTML/JSON đầu ra.
- **Gate là trọng tài.** Nếu `run_report.md` có ❌ FAIL → báo lỗi cho người dùng, KHÔNG xuất nhận định, KHÔNG "chỉnh cho khớp".
- Chỉ đọc file `summary.json` của module (≤ 5KB). Chỉ mở `result.json` khi cần trích danh sách cụ thể.

## Quy trình
1. Nếu người dùng thả file mới hoặc yêu cầu "dữ liệu mới nhất" → chạy:
   `uv run python -m pmo run --refresh`
   Ngược lại: `uv run python -m pmo run` (dùng cache trong kỳ).
2. Đọc `output/<kỳ>/run_report.md`.
3. Nếu có FAIL:
   - Nêu đúng gate, check, các mục lỗi (copy từ report).
   - Đề xuất hướng xử lý (ví dụ: courseClassId cũ → cập nhật `config/registry_seed.json`).
   - Dừng.
4. Nếu ĐẠT: đọc `output/<kỳ>/<module>/summary.json`, viết `output/<kỳ>/tong_hop.md` gồm:
   - Tình hình chung (số liệu lấy nguyên văn từ summary).
   - Điểm nóng và nguyên nhân.
   - Phương án hành động: việc gì, ai chịu trách nhiệm, hạn.
   - Cảnh báo WARN còn tồn tại (ví dụ chưa có golden set).
5. Báo người dùng: trạng thái gate + đường dẫn tổng hợp.

## Khi người dùng chỉ ra số liệu sai
1. Ghi số đúng vào golden set (`tests/golden/`, xem README).
2. Chạy `uv run python -m pmo verify` → phải FAIL ở G2.
3. Sửa `pmo/metrics/lms_fe.py` hoặc registry cho đến khi PASS.
4. Thêm test vào `tests/regression/test_lessons.py`; ghi 1 dòng vào `docs/super_memory.md` trỏ tới test.

## Lệnh tham khảo
| Lệnh | Tác dụng |
|---|---|
| `uv run python -m pmo run` | Kỳ hiện tại, dùng cache |
| `uv run python -m pmo run --refresh` | Lấy lại dữ liệu |
| `uv run python -m pmo run --only m1` | Chỉ chạy module M1 |
| `uv run python -m pmo verify` | Chỉ chạy cổng kiểm định |
| `uv run pytest -q` | Toàn bộ test |
