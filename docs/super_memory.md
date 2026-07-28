# Super Memory - Nhật ký & Quy chuẩn Dự Án PMO

Tài liệu này lưu trữ các quyết định thiết kế, lỗi thường gặp và bài học kinh nghiệm để các Agent kế thừa khi chạy session mới.

## 1. Quyết định Thiết kế UI/UX (Báo cáo PMO)
- **Concept chung:** Giao diện SPA (Single Page Application), tabbed-layout, không load lại trang. Render hoàn toàn bằng HTML + Vanilla JS (không dùng framework phức tạp) để tối ưu dung lượng và tốc độ.
- **Theme:** Ưu tiên Dark Mode hiện đại (Slate/Blue-gray scheme). Cảm giác sang trọng, Dashboard executive.
- **Tiêu chuẩn dữ liệu:**
  - **Cột Số lượng:** Thay vì hiện text thô, luôn dùng **Mini Progress Bar** đa sắc (Xanh lá - Xanh dương - Đỏ) để thể hiện tỷ trọng hoàn thành / đang làm / trễ hạn.
  - **Cảnh báo Nhân sự:**
    - `IDLE (Đỏ)`: Không được giao bất kỳ công việc nào (Active = 0, Completed = 0).
    - `AVAILABLE (Xanh lơ / Cyan)`: Vừa hoàn thành toàn bộ công việc, hiện không có task chạy (Active = 0, Completed > 0). Rất quan trọng để không đánh đồng với người "ngồi chơi".

## 2. Kỹ thuật Xử lý Data & API
- **Match Dự án Worklane:** 
  - KHÔNG chỉ dựa vào trường `PIC` của project. Rất nhiều nhân sự làm mem trong project nhưng không phải PIC. 
  - **Bài học:** Phải lặp qua toàn bộ danh sách `issues` (task con) bên trong project để gom danh sách `assignee`, sau đó convert về chữ thường và so khớp chuỗi để nhận diện nhân sự có tham gia dự án.
- **Quy ước Màu (Tag Dự án):**
  - Dựa vào trường `status` và `health` của Worklane.
  - `status = COMPLETED`: Màu Xanh lá (Hoàn thành).
  - `status = ACTIVE` & `health = ON_TRACK`: Màu Xanh dương (Đang chạy tốt).
  - `health = OFF_TRACK` hoặc `AT_RISK`: Màu Đỏ (Báo động rủi ro / Trễ hạn).

- **Xác thực chéo tiến độ (Cross-verification):**
  - Đối chiếu tỷ lệ hoàn thành từ báo cáo ngày với trạng thái thực tế trên hệ thống Worklane (`DONE`/`COMPLETED`).
  - Gắn cờ `UNVERIFIED` (Khai khống) và trừ điểm hiệu suất nếu nhân sự báo cáo xong nhưng Worklane chưa xong.
- **Tính toán mốc thời gian báo cáo tuần:** Khi chạy đánh giá vào đầu tuần (VD: Thứ 2), nếu dùng `today` để tính ngày bắt đầu tuần sẽ dẫn đến lấy nhầm chu kỳ của tuần mới. Cần sử dụng mốc `yesterday - timedelta(days=yesterday.weekday())` để đảm bảo luôn quét đúng chu kỳ làm việc của tuần hoàn chỉnh gần nhất.

## 3. Lịch sử Triển khai (Đã chốt)
- **Agent 1 (Kỷ luật SV):** Hoàn tất phân tích dữ liệu Excel, tự động vẽ biểu đồ Chart.js so sánh vi phạm đa chiều.
- **Agent 2 (Dự báo & Care List):** Hoàn thiện phân tích học thuật, UI đồng bộ Dark-theme Vanilla CSS. Có cơ chế fallback tự động (MySQL -> SQLite). Biểu đồ Chart.js so sánh Luật cũ vs Quy chế mới.
- **Agent 4 (Báo cáo & Dự án):** Tích hợp phân tích ma trận công việc hàng ngày, đối chiếu chéo trạng thái với Worklane PM.

## 4. Các lỗi kỹ thuật cần tránh (Troubleshooting)
- **UnicodeEncodeError (Python trên Windows):** Gọi `sys.stdout.reconfigure(encoding='utf-8')` đầu file script chạy qua `uv run` để tránh lỗi in text có dấu/emoji.
- **Lỗi hiển thị HTML block trong Markdown:** Tránh thụt lề các khối HTML (như `<div class="...">`) trong Markdown vì parser sẽ hiểu là code block.
- **SyntaxError & Chart.js không render:** Khi tạo HTML/JS động bằng Python `f-string`, cực kỳ cẩn thận với việc escape `{` thành `{{`. Đặc biệt, các dấu ngoặc `}}` thừa ở cuối block `<script>` có thể gây lỗi cú pháp JavaScript làm Chart.js không thể chạy (biểu đồ trống) dù không báo lỗi ở Python.
- **Truyền dữ liệu cho Chart.js:** Xuất data trực tiếp thành JSON variable trên template JS thay vì parse DOM để thư viện tự lấy dữ liệu dễ dàng.

## 5. Kiến trúc Pipeline (Harness, Loop, Graph)
- Mọi file Excel/SQL gốc trước khi đưa vào Agent xử lý đều phải đi qua `DataSanitizer` (Harness) để làm sạch khoảng trắng (tên GV/TG) và lấp giá trị `NaN`, tránh lỗi tính toán (Ví dụ: `PTIT_Chiso.xlsx`).
- Output JSON/HTML của các Agent đều phải đi qua cổng `Validator` (Loop) để check format và syntax lỗi (như lỗi `{}` của Chart.js). Nếu lỗi sẽ tự động đưa vào LLM (`google-genai`) sửa tối đa 2 lần.
- Pipeline `run_pipeline.py` không bao giờ được dùng `sys.exit(1)` khi một Agent con lỗi. Luôn phải bắt Exception, trả về cờ rẽ nhánh (Graph Fallback) để các Agent khác vẫn có thể tiếp tục chạy. Mọi file output cần được validate tại chỗ ngay sau mỗi bước.

## 6. Phân lớp Thư mục Dữ liệu (Data Pipeline Layering)
Để giữ thư mục gốc sạch sẽ, các file dữ liệu và báo cáo phải tuân thủ phân lớp sau:
- **`data/inputs/`**: Chứa dữ liệu đầu vào thô/tĩnh (Excel, SQL, MD). Không ghi đè hay sinh file mới ở đây ngoài file backup dữ liệu gốc.
- **`data/processed/`**: Chứa dữ liệu trung gian dạng JSON hoặc log do các Agent sinh ra để giao tiếp chéo.
- **`output/reports/`**: Chứa báo cáo thô dạng Markdown `.md`.
- **`output/dashboards/`**: Chứa các dashboard dạng HTML phục vụ hiển thị trực quan cuối cùng.

## 7. Quản lý Tri thức Tiết kiệm Token (LLMWiki / RAG)
- Tránh chèn trực tiếp các file quy định lớn (`quy_dinh.md`, `Khung_Phat_Khenthuong_ĐT_T62026.md`) vào Prompt của Agent.
- Sử dụng thư viện độc lập `LLMWiki` (`agents/llmwiki.py`) sử dụng FAISS + Gemini Embeddings (`text-embedding-004`) để truy xuất ngữ nghĩa cục bộ.
- Dữ liệu Vector được lưu tại `data/processed/wiki_index.faiss`. Agent chỉ cần gọi hàm `LLMWiki().query("câu hỏi")` để chèn đúng 2-3 block tri thức liên quan nhất, giúp giảm 95% chi phí Token.
