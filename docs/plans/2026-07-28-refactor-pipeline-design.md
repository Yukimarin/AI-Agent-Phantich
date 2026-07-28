# Refactor Pipeline: Harness, Loop & Graph Integration

Mục tiêu là cải tiến độ ổn định của hệ thống đánh giá KPI bằng cách áp dụng kiến trúc Harness (môi trường an toàn), Loop (vòng lặp kiểm chứng), và Graph (rẽ nhánh khi lỗi thay vì crash).

## 1. Harness Layer (Làm sạch dữ liệu)

**File mới: `agents/data_sanitizer.py`**
- Sẽ chạy **ngay đầu đường ống**. Script này dùng `openpyxl` hoặc `pandas` để đọc file Excel/SQL gốc.
- Chuẩn hóa tên GV/TG (xóa khoảng trắng thừa), fill giá trị rỗng (`NaN`) bằng 0 để các phép tính toán (sum, avg) không bị lỗi.
- Chuẩn hóa Encoding (`utf-8`).

## 2. Loop Layer (Vòng lặp kiểm chứng tự động)

**File mới: `agents/validator.py`**
- Đây là cổng kiểm duyệt đầu ra của các Agent.
- Cung cấp method `validate_json(file_path)` để bắt lỗi JSON format.
- Cung cấp method `validate_chartjs(html_path)` để bắt lỗi các ngàm `{}` trong Javascript (lỗi Chart.js không render từ `super_memory.md`).
- Kèm theo hàm `fix_with_llm(content, error_msg)` sẽ gọi Gemini (hoặc LLM tương đương) để tự động sửa nội dung file với cấu hình `MAX_RETRY = 2`.

## 3. Graph Layer (Luồng rẽ nhánh và Fallback)

**Chỉnh sửa: `run_pipeline.py`**
- Xóa bỏ toàn bộ `sys.exit(1)`.
- Xây dựng lại hàm `run_agent()` thành hàm `run_node_with_retry()`.
- **Logic Routing**: Chạy sub-process. Nếu Return Code != 0 hoặc Output JSON/HTML lỗi (check bởi `validator.py`), nó sẽ gửi lại cho LLM hoặc báo lỗi. Nếu vẫn lỗi sau 2 lần, nó bỏ qua tác vụ đó (trả về file Fallback), in Log cảnh báo, và CHẠY TIẾP tác vụ tiếp theo thay vì sập toàn hệ thống.

## 4. Kiểm thử
- Test tự động với file Excel lỗi.
- Test bằng tay trên Master Dashboard.
