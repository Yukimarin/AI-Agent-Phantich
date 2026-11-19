# Quy tắc Dự án: Phân tích Chỉ số Đào tạo & KPI GV/TG (PTIT x Rikkei)

## 1. Đầu phiên / cuối phiên (Tối ưu Token)
- **Đầu phiên**: chỉ đọc `docs/STATUS.md` (≤ 40 dòng). Không đọc thêm tài liệu khác trừ khi task yêu cầu.
- **Khi viết nhận định / báo cáo**: chỉ đọc `output/<kỳ>/ai_digest.md` (≤ 4.5KB, đã tổng hợp sẵn KS26 M1+M4, Excel KS25 mới nhất, Worklane Audit và `dataAt`). Không viết script lẻ để đọc lại Excel/JSON trừ khi truy vấn sâu cá nhân.
- **Cuối phiên**: cập nhật gọn `docs/STATUS.md`; quyết định kiến trúc/nghiệp vụ → 1 dòng trong `docs/DECISIONS.md`.

## 2. Mô hình PMO Data Hub (mặc định cho mọi yêu cầu dữ liệu / thống kê / báo cáo)
- Skill `run-analytics`. Lệnh: `uv run python -m pmo run [--refresh]` hoặc trọn gói `uv run python -m pmo pipeline [--refresh] [--fast]`.
- **Script tính, AI nhận định**: AI không tự tính chỉ số, không sửa số trong đầu ra; đọc `output/<kỳ>/ai_digest.md` để viết `nhan_dinh.json` (khớp `dataAt`) và `tong_hop.md`.
- **Gate là trọng tài (G1 Dữ liệu · G2 Chỉ số · G4 Giao diện)**: gate FAIL ⇒ dừng và báo lỗi theo `run_report.md`.
- **Bài học = test**: lỗi người dùng phát hiện ⇒ thêm test vào `tests/regression/` hoặc `tests/golden/`.
- **Tách cấu hình khỏi code**: Lớp-môn LMS tại `config/registry_seed.json`; Nhân sự, phòng ban, lịch nghỉ lễ Worklane tại `config/worklane_roster.json`. Bí mật trong `.env`.

## 3. Phân công Model Agent & Subagent (Model Routing)
| Tầng | Model | Nhiệm vụ |
|---|---|---|
| **Tầng 0 (Deterministic)** | **Pure Python (0 token)** | Lấy API, đọc Excel/MySQL, tính CC/BT/EL (`pmo/metrics/lms_fe.py`), chạy Gate G1–G4, render HTML |
| **Tầng 1 (Worker Subagent)** | `flash_lite` / `flash` | Phân loại ngữ nghĩa task Worklane, kiểm tra giao diện (`automated-visual-testing`), tra cứu hồ sơ SV lẻ |
| **Tầng 2 (Lead Mặc định)** | `pro` (Medium) | Chạy pipeline định kỳ, đọc `ai_digest.md`, viết `nhan_dinh.json` & `tong_hop.md`, cập nhật config |
| **Tầng 3 (Deep Architect)** | `pro` (High Thinking) | Chẩn đoán nhân quả chéo đa nguồn (Worklane GV ↔ LMS SV), thiết kế module mới, refactoring lớn |

## 4. Cấu trúc thư mục chuẩn AI Agent
| Thư mục | Vai trò |
|---|---|
| `.agents/` | `AGENTS.md` (luật cốt lõi) · `skills/` (5 domain skills đang hoạt động) |
| `config/` | Nguồn cấu hình duy nhất: `registry_seed.json` (LMS) · `worklane_roster.json` (Nhân sự/Lịch nghỉ) · `templates/` |
| `pmo/` | Core Engine: `cli.py` · `data_agent.py` · `digest.py` · `connectors/` · `metrics/` · `gates/` (G1, G2, G4) · `modules/` |
| `data/` | `inbox/` & `inputs/` (Excel/SQL đầu vào) · `warehouse/<kỳ>/` (kho snapshot bất biến) · `processed/` (cache legacy) |
| `output/` | `01_Bao_Cao_Su_Dung_Thuong_Xuyen/` (`HTML_Dashboards/`, `Markdown_Tong_Hop/` — tên Tiếng Việt đánh số 00..08) · `02_Thong_Ke_Dot_Xuat_Theo_Task/` (`Excel_Xlsx/`, `Word_Docx/`, `Markdown_Phan_Tich_Le/`, `HTML_Chuyen_De_Le/`) · `2026-Wxx/` (chỉ giữ 2 kỳ gần nhất, kỳ cũ tự động nén `.zip` vào `legacy/archive_periods/` qua `pmo/retention.py`) |
| `tests/` | `test_pipeline.py` · `golden/` (chuẩn LMS FE có `asOf`) · `regression/` (khóa lỗi lịch sử & roster) |
| `docs/` | `STATUS.md` (≤ 40 dòng) · `DECISIONS.md` · `architecture/` · `domain/` · `archive/` |
| `legacy/` | `dgnl/` · `skills_archive/` · `scratch_archive/` · (và `agents/`, `scripts/` khi cắt chuyển P6) |

## 5. Chống Nhiễm Chéo Ngữ Cảnh & Cách Ly Nghiệp Vụ (Context Hygiene)
- **Tách bạch Học vụ (Đào tạo) vs Tài chính (Kế toán)**: Tuyệt đối không xử lý nghiệp vụ Kế toán (Công nợ, Tín chỉ thu phí, Danh sách đóng tiền, Email đình chỉ) chung luồng với nghiệp vụ Đào tạo (Giảng viên bộ môn, Chuyên cần, Bài tập LMS, Xét thi). Khi có task Kế toán đột xuất, chuyển sang Worker Subagent hoặc dùng `/compact`.
- **Phân định rõ vai trò nhân sự (Triệt tiêu nhầm lẫn)**:
  * `subject_lecturer`: Giảng viên giảng dạy bộ môn (Lấy duy nhất từ `config/registry_seed.json` theo cặp `[className, courseCode]`).
  * `class_advisor`: Cố vấn học tập (CVHT).
  * `finance_officer`: Nhân sự phụ trách thu hồi nợ / Kế toán.
  * *Cấm dùng khái niệm 'GV' chung chung gây nhầm lẫn giữa GV bộ môn và CVHT.*
- **Nguyên tắc Tầng 0 cho truy vấn nhân sự**: Mọi truy vấn về giảng viên/lớp phải xuất phát từ script đọc trực tiếp `config/registry_seed.json`, không suy luận hoặc đoán từ trí nhớ context.
