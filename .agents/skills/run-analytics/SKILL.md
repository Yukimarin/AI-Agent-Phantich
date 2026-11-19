---
name: run-analytics
description: Use when the user asks to fetch data and analyze / produce statistics or reports ("lấy dữ liệu và phân tích", "thống kê tuần này", "chạy báo cáo", "cập nhật số liệu", "đánh giá chỉ số lớp"). Runs the PMO Data Hub pipeline with verification gates instead of ad-hoc scripts.
---

# Run Analytics (PMO Data Hub)

## Nguyên tắc bắt buộc (Zero-Hallucination & Token Optimization)
- **Script tính, AI nhận định.** KHÔNG tự tính CC/BT/EL, KHÔNG gọi LMS/Worklane trực tiếp, KHÔNG sửa số trong HTML/JSON đầu ra.
- **Gate là trọng tài.** Nếu `run_report.md` có ❌ FAIL → báo lỗi cho người dùng, KHÔNG xuất nhận định, KHÔNG "chỉnh cho khớp".
- **Tối ưu Token:** Chỉ đọc duy nhất `output/<kỳ>/ai_digest.md` (≤ 4.5KB) để lấy toàn bộ số liệu KS26 (M1/M4), biến động Excel KS25 mới nhất, `dataAt` và kiểm toán Worklane. Chỉ mở `result.json` khi cần trích danh sách cá nhân cụ thể.

## Quy trình
1. Chạy lệnh:
   - Chỉ cập nhật PMO Data Hub (KS26 + Gate + AI Digest): `uv run python -m pmo run [--refresh]`
   - Cập nhật trọn gói (PMO Data Hub + Toàn bộ Dashboards + `deploy_web/`): `uv run python -m pmo pipeline [--refresh] [--fast]`
2. Đọc `output/<kỳ>/run_report.md`. Nếu có ❌ FAIL → báo rõ gate lỗi và dừng.
3. Nếu ✅ ĐẠT: đọc `output/<kỳ>/ai_digest.md`:
   - Cập nhật `output/<kỳ>/m4_chan_doan_lop/nhan_dinh.json` (bắt buộc gắn đúng `dataAt` trong `ai_digest.md`).
   - Viết `output/<kỳ>/tong_hop.md` (Tình hình chung, Điểm nóng & nguyên nhân, Phương án hành động).
4. Báo người dùng trạng thái Gate + đường dẫn báo cáo.

## Khi thay đổi nhân sự / lịch nghỉ Worklane
- Chỉ sửa duy nhất tại `config/worklane_roster.json` (`staffRoster`, `excludedStaff`, `companyHolidays`), sau đó chạy `agents/audit/audit_worklane_performance.py` → `compute_worklane_comparisons.py` → `generate_audit_dashboard.py`.

## Lệnh tham khảo
| Lệnh | Tác dụng |
|---|---|
| `uv run python -m pmo run [--refresh]` | Chạy PMO Data Hub + Gate G1/G2/G4 + sinh `ai_digest.md` |
| `uv run python -m pmo pipeline [--refresh] [--fast]` | Chạy trọn gói PMO + Legacy Dashboards song song + `deploy_web/` |
| `uv run python -m pmo digest` | Chỉ sinh lại `output/<kỳ>/ai_digest.md` |
| `uv run python -m pmo verify` | Chỉ chạy cổng kiểm định G1, G2, G4 |
| `uv run pytest -q` | Chạy toàn bộ regression & unit tests |
