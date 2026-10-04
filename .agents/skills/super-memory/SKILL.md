---
name: super-memory
description: Use when starting any new task or conversation to load project context, or when finishing a milestone / learning a lesson that must persist across sessions.
---

# Project Memory (STATUS + DECISIONS + Tests)

> Thay cho `super_memory.md` từ 04/10/2026 (bản cũ: `docs/archive/super_memory_20261004.md`).

## Nguyên tắc
Bộ nhớ dự án được tách theo **loại thông tin**, không dồn vào một file:

| Loại | Nơi lưu | Khi nào đọc |
| :--- | :--- | :--- |
| Trạng thái hiện tại + việc tiếp theo | `docs/STATUS.md` (≤ 1 trang) | **Đầu mọi phiên** |
| Quyết định thiết kế (ADR rút gọn) | `docs/DECISIONS.md` (append, 1–3 dòng/mục) | Khi cần lý do |
| Bài học / lỗi đã sửa | **Test** trong `tests/regression/` hoặc `tests/golden/` | Tự động qua `pytest` + gates |
| Quy chuẩn nghiệp vụ | `docs/domain/quy_chuan_nghiep_vu.md` | Khi làm chỉ số |
| Kiến trúc | `docs/architecture/` | Khi sửa pipeline |

## Quy trình
- **Đầu phiên:** đọc `docs/STATUS.md`.
- **Cuối phiên:** cập nhật `docs/STATUS.md` **tại chỗ** (xóa việc đã xong, không ghi nhật ký theo ngày).
- **Có quyết định mới của người dùng:** thêm 1 mục vào `docs/DECISIONS.md` (hỏi người dùng trước nếu chưa chắc).
- **Người dùng phát hiện lỗi:** viết test tái hiện → sửa → test pass. Không chỉ ghi chữ.

## Lỗi thường gặp
- Ghi bài học bằng chữ mà không có test → lỗi tái phạm.
- Để STATUS phình thành nhật ký → chuyển chi tiết vào commit message.
