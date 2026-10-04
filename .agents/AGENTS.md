# Quy tắc Dự án: Phân tích Chỉ số Đào tạo & KPI GV/TG (PTIT x Rikkei)

## 1. Đầu phiên / cuối phiên
- **Đầu phiên**: đọc `docs/STATUS.md` (trạng thái, việc dở, vấn đề mở). Không cần đọc thêm tài liệu khác trừ khi task yêu cầu.
- **Cuối phiên**: cập nhật `docs/STATUS.md`; quyết định quan trọng → 1 dòng trong `docs/DECISIONS.md`.

## 2. Mô hình PMO Data Hub (mặc định cho mọi yêu cầu lấy dữ liệu / thống kê / phân tích)
- Skill `run-analytics`. Lệnh: `uv run python -m pmo run [--refresh]`. Kiến trúc: `docs/architecture/data-hub.md`.
- **Script tính, AI nhận định**: AI không tự tính chỉ số, không gọi LMS/Worklane trực tiếp, không sửa số trong đầu ra; chỉ đọc `output/<kỳ>/<module>/summary.json` để viết nhận định + phương án hành động.
- **Gate là trọng tài**: gate FAIL ⇒ báo lỗi theo `run_report.md`, không "chỉnh số cho khớp".
- **Bài học = test**: lỗi người dùng phát hiện ⇒ thêm test `tests/regression/` hoặc golden set `tests/golden/`.
- **Báo cáo mới** = module mới trong `pmo/modules/` (chỉ đọc kho), đăng ký `REGISTRY`.
- CC/BT/EL chỉ được tính trong `pmo/metrics/lms_fe.py`. Bí mật trong `.env`.

## 3. Cấu trúc thư mục
| Thư mục | Vai trò |
|---|---|
| `pmo/` | Code mới theo tầng: connectors → data_agent/warehouse → metrics → gates → modules |
| `config/` | registry seed, templates, ngưỡng |
| `data/inbox/` | người dùng thả file mới · `data/warehouse/` kho theo kỳ (không commit) |
| `output/<kỳ>/` | đầu ra pipeline mới · `output/dashboards/` đầu ra legacy |
| `legacy/` | mã đóng băng (ĐGNL Đợt 1). Agent 1-5 (`agents/`, `scripts/`, `run_pipeline.py`) sẽ chuyển vào khi cắt chuyển P6 |
| `docs/` | `STATUS` · `ROADMAP` · `DECISIONS` · `architecture/` · `domain/` · `reports/` · `legacy/` · `archive/` |

## 4. Quy ước tài liệu
- **Không** tạo file kế hoạch cho mỗi phiên. Kế hoạch chỉ khi việc > 1 ngày hoặc nhiều bước → `docs/plans/`, **xóa khi xong** (git giữ lịch sử).
- Kiến trúc: cập nhật tại chỗ trong `docs/architecture/`, không tạo bản mới.
- Việc nhỏ / sửa lỗi: commit message + test là đủ.

## 5. Nguyên tắc chung
- Báo cáo, phản hồi bằng tiếng Việt chuẩn, chuyên nghiệp.
- Thiếu dữ liệu / lỗi file: báo chi tiết và cảnh báo, không dừng đột ngột (với `pmo`: ghi `run_report.md`, chặn xuất báo cáo sai).
- Không tự viết multi-agent code; `pmo/` là pipeline tất định.
- Pipeline cũ (Agent 1-5, KPI 40/30/30): vai trò chi tiết tại `docs/legacy/agent_roles.md`.
