# Phân tích Chỉ số Đào tạo & KPI GV/TG — PTIT x Rikkei

## Chạy
```powershell
uv run python -m pmo run            # lấy dữ liệu (cache trong tuần) → kiểm định → báo cáo
uv run python -m pmo run --refresh  # lấy lại dữ liệu mới
uv run python -m pmo verify         # chỉ chạy cổng kiểm định
uv run pytest -q                    # toàn bộ test
```
Hoặc nói với AI: *"Lấy dữ liệu và phân tích tuần này"* (skill `run-analytics`).
Kết quả: `output/<YYYY-Www>/run_report.md` và `output/<kỳ>/<module>/`.

Cần file `.env` ở thư mục gốc: `LMS_TOKEN=<token>`.

## Cấu trúc
```
pmo/            Pipeline mới: connectors → data_agent → warehouse → metrics → gates → modules
config/         registry_seed.json, templates/
data/           inbox/ (thả file mới) · inputs/ · warehouse/ (kho theo kỳ) · processed/ (legacy)
output/         <kỳ>/ (mới) · dashboards/, reports/ (legacy)
tests/          regression/ · golden/ · test_*.py
legacy/         dgnl/ (ĐGNL Đợt 1, Pages submodule)
agents/ scripts/ lib/ run_pipeline.py deploy_web/   Agent 1-5 — chuyển vào legacy/ khi cắt chuyển
docs/           STATUS · DECISIONS · architecture/ · domain/ · reports/ · legacy/ · archive/
```

Bắt đầu đọc: [`docs/STATUS.md`](docs/STATUS.md) · Kiến trúc: [`docs/architecture/data-hub.md`](docs/architecture/data-hub.md)
