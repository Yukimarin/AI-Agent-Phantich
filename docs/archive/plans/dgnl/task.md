# Nhiệm vụ Dự án Phân tích Năng lực SV (ĐGNL Lần 1)

- `[x]` Chuyển đổi file chương trình đào tạo `CTĐT.xlsx` sang file Markdown [CTĐT.md](file:///c:/Users/DELL/Desktop/AI-Agent/AI-ĐGNL/docs/reports/CTĐT.md)
- `[x]` Đánh giá chuyên sâu lộ trình học tập các khóa KS24, KS25 CNTT và KS25 QTKD tại [roadmap_evaluation.md](file:///c:/Users/DELL/Desktop/AI-Agent/AI-ĐGNL/docs/reports/roadmap_evaluation.md)
- `[x]` Thiết lập cấu trúc thư mục dự án theo kiến trúc **Harness Engineering**
- `[x]` Cài đặt quy trình tối ưu hóa token tại [token_optimization_process.md](file:///c:/Users/DELL/Desktop/AI-Agent/AI-ĐGNL/docs/plans/token_optimization_process.md)
- `[x]` Thiết lập cấu hình ngưỡng năng lực (job thresholds) tại [job_thresholds.json](file:///c:/Users/DELL/Desktop/AI-Agent/AI-ĐGNL/harness/config/job_thresholds.json)
- `[x]` Khởi tạo bộ kiểm soát (Guardrails) tại [guardrails.py](file:///c:/Users/DELL/Desktop/AI-Agent/AI-ĐGNL/harness/guardrails.py)
- `[x]` Khởi tạo bộ nhớ dự án tại [Super Memory.md](file:///c:/Users/DELL/Desktop/AI-Agent/AI-ĐGNL/docs/Super%20Memory.md)
- `[x]` Phân tích năng lực khối KS24 (Hoàn thành hiệu chỉnh điểm và báo cáo)
- `[x]` Phân tích năng lực khối KS25 (Hoàn thành đối soát 429 học viên và ca lỗi)
- `[ ]` Theo dõi kết quả thi bổ sung ngày 22/08/2026 và tổng hợp báo cáo chung cuối cùng


## Tiến trình Brainstorming Giải pháp Tính % Đáp ứng Công việc & Đề xuất CTĐT:
- `[x]` 1. Khảo sát ngữ cảnh dự án & Nhận diện dữ liệu
- `[x]` 2. Thảo luận các câu hỏi làm rõ (Clarifying Questions)
- `[x]` 3. Đề xuất 2-3 phương án tính toán (Approaches) & Nhận phản biện tuyển dụng
- `[x]` 4. Thống nhất thiết kế giải pháp & Đề xuất điều chỉnh lộ trình tại [2026-08-20-KS24-curriculum-proposals.md](file:///c:/Users/DELL/Desktop/AI-Agent/AI-ĐGNL/docs/plans/2026-08-20-KS24-curriculum-proposals.md)
- `[x]` 5. Chuyển đổi sang kế hoạch triển khai chi tiết (Transition to implementation-plan)

## Kế hoạch Thực thi Báo cáo HTML KS24:
- `[x]` 1. Viết mã nguồn xử lý dữ liệu ĐGNL: [process_dgnl_data.py](file:///c:/Users/DELL/Desktop/AI-Agent/AI-ĐGNL/src/process_dgnl_data.py)
- `[x]` 2. Tạo file dữ liệu trung gian: `scratch/ks24_stats.json`
- `[x]` 3. Viết mã nguồn sinh dashboard HTML: [generate_dashboard.py](file:///c:/Users/DELL/Desktop/AI-Agent/AI-ĐGNL/src/generate_dashboard.py)
- `[x]` 4. Xác minh kết quả & tạo walkthrough tại `docs/reports/walkthrough.md`
- `[x]` 5. Thực hiện đối soát so sánh chuyên sâu với Báo cáo Tổ chức thi của Leader tại [comparison_leader_report.md](file:///c:/Users/DELL/Desktop/AI-Agent/AI-ĐGNL/docs/reports/comparison_leader_report.md)
