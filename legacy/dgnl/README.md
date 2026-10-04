# ĐGNL — Báo cáo Khảo thí Đánh giá Năng lực (Đợt 1, chốt 02/09/2026)

Gộp từ dự án `AI-ĐGNL` ngày 04/10/2026 (giữ nguyên lịch sử git qua subtree merge).

| Thư mục | Nội dung |
|---|---|
| `src/` | Bộ sinh báo cáo v7 (bản đang dùng). Các bản v3–v6 và generator cũ đã xóa — xem lịch sử git nếu cần |
| `inputs/` | Excel kết quả chấm, danh sách thi, CTĐT, QĐ16.2026 |
| `harness/` | Ngưỡng đánh giá theo vị trí việc làm |
| `outputs/` | **Git submodule** → GitHub Pages `https://yukimarin.github.io/dgnl-reports/` (link đã gửi lãnh đạo, không đổi) |

Tài liệu phân tích: `docs/domain/dgnl/`. Kế hoạch cũ: `docs/archive/plans/dgnl/`.

## Chạy lại báo cáo Đợt 1
Script dùng đường dẫn tương đối `inputs/`, `outputs/` nên phải chạy với thư mục làm việc là `legacy/dgnl`:

```powershell
uv run --with openpyxl python src/build_all_reports_v7.py      # Executive Summary
uv run --with openpyxl python src/update_cohort_reports_clean.py  # KS24 / KS25 / QTKD
uv run --with openpyxl python src/build_index_v6.py            # Trang chủ
```

Xuất bản: commit + push trong `outputs/` (repo `dgnl-reports`), sau đó commit con trỏ submodule ở repo chính.

## Đợt ĐGNL tiếp theo
Không sửa tiếp các script này. Xây **module M4** trong `pmo/modules/m4_dgnl/` đọc `data/inputs/dgnl/<đợt>/`, dùng chung registry Lớp ↔ SV với M1/M2 để đối chiếu năng lực với chỉ số học tập.
