# STATUS — đọc đầu mỗi phiên

> Cập nhật: 04/10/2026. Giữ file này ≤ 50 dòng. Lịch sử: `git log`. Quyết định: `DECISIONS.md`.

## Đang ở đâu
- **Pipeline mới PMO Data Hub** chạy được: `uv run python -m pmo run [--refresh]` → Data Agent (LMS) → G1 → Metric Engine → G2 → M1 Chỉ số lớp. Kỳ gần nhất: 2026-W40, 28/28 lớp-môn K26, gate ĐẠT (2 cảnh báo).
- **Pipeline cũ** (Agent 1-5, `run_pipeline.py`, dashboards `output/dashboards/`, `deploy_web/`) vẫn chạy song song tới P6.
- **ĐGNL Đợt 1** đã gộp vào `legacy/dgnl/` (Pages submodule giữ nguyên link). Tài liệu: `docs/domain/dgnl/`.
- Workspace `AI-Agent/` chỉ còn dự án này; 10 dự án cũ đã nén ở `AI-Agent/_archive_20261004/`.

## Việc tiếp theo (theo thứ tự)
1. **P0 Golden set** — cần người dùng xác nhận số SV vi phạm CC/BT/EL trên LMS FE cho 3-5 lớp (`tests/golden/README.md`).
2. **M3 Hiệu suất GV/TG** — Worklane connector (báo cáo ngày, task trễ, dự án trễ) vào Data Agent.
3. **M2 Dự báo qua môn** — điểm môn trước (MySQL `auto_rpoints`/`final_results`) + kết quả M1.
4. **Renderer + G3/G4** — dashboard template cố định đọc JSON.
5. **P6 cắt chuyển** — chuyển `agents/ scripts/ lib/ run_pipeline.py deploy_web/` vào `legacy/`; `data/processed`, `mysql_data_97` → `data/legacy/`.

## Vấn đề mở / cảnh báo
- Gate 2 WARN: chưa có golden set.
- CC lệch tối đa 1-2 SV so với FE (API không tách vắng KP/CP/Muộn).
- Token LMS từng nằm trong `scripts/fetch_ks26_live.js` (có trong lịch sử git) → nên đổi token.
- `config/registry_seed.json` chỉ có 10 lớp K26; KS24/KS25 chưa vào registry.
- Script cũ ghi cứng đường dẫn `data/processed/...`, `output/dashboards/...`, `deploy_web/` → không di chuyển trước P6.

## Tham chiếu nhanh
- Quy chuẩn nghiệp vụ (barem KPI, khối/leader, quy tắc task trễ, LMS API): `docs/domain/quy_chuan_nghiep_vu.md`
- Bài học đã khóa bằng test: `tests/regression/`, `tests/test_pipeline.py`
