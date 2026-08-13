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
  - **Giảm tải thị giác cho dữ liệu lớn (Progressive Disclosure):**
    - Sử dụng **Department Tabs** để chia cụm nhân sự theo khối (CNTT, QTKD, etc.) giảm tải 75% lượng thông tin ban đầu.
    - Tích hợp **Workload Toggles** để sếp khoanh vùng nhanh giảng viên quá tải/trống việc.
    - Giới hạn biểu đồ trễ hạn ở **Top 5** thay vì vẽ toàn bộ 36 dự án.
    - Thiết kế **Slide-over Drawer** (Bảng trượt cạnh phải) để chứa toàn bộ thông tin drill-down chi tiết của giảng viên khi click, giữ trang Cockpit chính luôn sạch sẽ.
  - **Đa chu kỳ & Dynamic Refresh (Aug 2026):**
    - Nâng cấp Báo cáo QLĐT thành Dashboard SPA 3 Tab: Ngày, Tuần, Tháng. Client-side JS quản lý state, chuyển đổi tabs, tự động vẽ lại Chart.js và cập nhật bảng dữ liệu động.
    - Tích hợp nút **"🔄 Cập nhật dữ liệu"** cho Dashboard Agent 4 (`agent_4_daily_logs.html`) sử dụng cơ chế dynamic fetching từ file JSON payload cục bộ (`agent4_payload.json`) giúp cập nhật dữ liệu realtime mà không cần load lại trang.
- **Quyết định chốt cấu trúc Báo cáo Agent 1 (Class KPI):** Toàn bộ cấu trúc báo cáo, logic trung bình có trọng số theo sỉ số lớp, cơ chế đối chiếu tuần linh hoạt (tự động lùi tuần học thực tế gần nhất, tự động so sánh chéo môn học liền kề dựa trên dòng thời gian dạy học) và cách phân khối CNTT/QTKD đã được chốt và đóng băng thiết kế. Từ các phiên làm việc sau, hệ thống sẽ duy trì giao diện này và chỉ nạp dữ liệu Excel mới nhất để cập nhật chỉ số hiển thị tự động.
- **Quyết định chốt cấu trúc Báo cáo Agent 2 (Academic Predictor) (Aug 2026):** Tái cấu trúc Dashboard Agent 2 thành dạng 3 Tab SPA (Đánh giá & Giải pháp hệ thống, Phân tích Lớp học, Danh sách can thiệp). Tích hợp Slide-over Drawer tương tác trượt từ cạnh phải màn hình để xem thông tin drill-down lớp học chi tiết. Rút gọn lỗi tác nghiệp GV/TG thành tooltip tam giác cam tại chỗ thay vì accordion cũ. Loại bỏ hoàn toàn các thuật ngữ mang tính chất kỹ thuật AI.

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

## 3. Các lỗi kỹ thuật cần tránh (Troubleshooting)
- **UnicodeEncodeError (Python trên Windows):** Gọi `sys.stdout.reconfigure(encoding='utf-8')` đầu file script chạy qua `uv run` để tránh lỗi in text có dấu/emoji.
- **Lỗi hiển thị HTML block trong Markdown:** Tránh thụt lề các khối HTML (như `<div class="...">`) trong Markdown vì parser sẽ hiểu là code block.
- **Lỗi truy vấn SQLite thiếu bảng (Mock mode):** Trong chế độ chạy SQLite Fallback, bao bọc toàn bộ fallback query bằng khối `try-except` và bắt lỗi để trả về danh sách rỗng (`[]`) thay vì làm crash pipeline khi DB SQLite thiếu các bảng nghiệp vụ.
- **SyntaxError & Chart.js không render:** Khi tạo HTML/JS động bằng Python `f-string`, cực kỳ cẩn thận với việc escape `{` thành `{{`. Đặc biệt, các dấu ngoặc `}}` thừa ở cuối block `<script>` có thể gây lỗi cú pháp JavaScript làm Chart.js không thể chạy (biểu đồ trống) dù không báo lỗi ở Python. **Giải pháp tối ưu:** Tránh sử dụng Python `f-string` trực tiếp cho các template HTML lớn; thay vào đó, định nghĩa HTML template dưới dạng chuỗi thô (raw string) thông thường và dùng `.replace()` cho các placeholder dạng `__PLACEHOLDER__`, kết hợp `json.dumps()` để nhúng dữ liệu JSON chuẩn, tránh lỗi convert kiểu dữ liệu của Python (dấu nháy đơn, boolean viết hoa).
- **Truyền dữ liệu cho Chart.js:** Xuất data trực tiếp thành JSON variable trên template JS thay vì parse DOM để thư viện tự lấy dữ liệu dễ dàng.
- **Lỗi mất dữ liệu do `window.onload` trong SPA:** Khi tích hợp nhiều dashboard độc lập vào một trang SPA duy nhất, tránh sử dụng `window.onload` vì sự kiện này có thể đã kích hoạt trước khi script con chạy. Hãy tự động chuyển hóa thành lệnh kích hoạt ngay lập tức (`handler(); window.onload = handler;`) trong IIFE để nạp dữ liệu tức thời.
- **Tránh xung đột CSS trong SPA bằng CSS Nesting:** Tránh dùng Regex thay thế chuỗi selector (như thay `.card` dễ làm hỏng `.card-header`). Hãy tận dụng CSS Nesting tiêu chuẩn bằng cách thay thế `:root`, `html`, `body` thành `&` và bao bọc toàn bộ CSS của tab con trong một selector cha (ví dụ: `#tab-container { ... }`).
- **Lỗi ReferenceError do thiếu hàm JS helper trên Client-side:** Khi di chuyển các logic tính toán sang client-side và gọi trực tiếp các hàm điều hướng (như `populateDateSelect()`, `switchTimeRange()`, `switchDate()`, `switchMainTab()`, `filterTasks()`) từ các sự kiện HTML (`onclick`, `onchange`), bắt buộc phải khai báo và định nghĩa đầy đủ các hàm này trong thẻ `<script>`, nếu không trang web sẽ bị trắng màn hình do trình duyệt ngắt chạy script khi gặp lỗi ReferenceError.
- **Lỗi lặp qua dict keys thay vì values:** Khi load dữ liệu JSON lưu dưới dạng dictionary của các dự án Worklane (`project_issues_worklane.json`), việc lặp qua `for proj in worklane_projects:` sẽ lặp qua các chuỗi keys (project key) thay vì đối tượng dự án. Cần kiểm tra kiểu dữ liệu và dùng `worklane_projects.values()` để lấy các đối tượng dự án thực tế khi thực hiện đối chiếu chéo (cross-verification).
- **So khớp họ tên có dấu tiếng Việt lệch pha:** Họ tên nhân sự từ Worklane và daily logs có thể không khớp do dấu tiếng Việt viết lệch pha hoặc viết không dấu. Bắt buộc chuẩn hóa cả hai chuỗi tên về dạng không dấu, viết thường, không khoảng trắng bằng hàm `normalize_vietnamese_name` trước khi so sánh.
- **Graceful DB Mock Fallbacks:** Khi thiết kế các Agent truy vấn DB (MySQL/SQLite), luôn chuẩn bị chế độ mock/fallback tự động khi cơ sở dữ liệu ngoại tuyến (như MySQL port 3307 không kết nối được). Thiết kế các class wrapper `MockConnection` và `MockCursor` để chặn các lệnh gọi `execute()`, `fetchone()`, `fetchall()` và trả về dữ liệu mẫu/mock an toàn để tránh làm gãy pipeline tự động (`run_pipeline.py`).
- **Tách biệt giao diện (HTML) và logic (Python):** Đối với các Agent sinh dashboard HTML lớn (như Báo cáo QLĐT), việc viết chuỗi template HTML dài hàng nghìn dòng trong file Python rất dễ dẫn đến lỗi encoding UTF-8 trên Windows, hoặc lỗi cú pháp f-string khi agent chỉnh sửa. **Quy chuẩn mới:** Tách template HTML ra một tệp `.html` riêng biệt (ví dụ: `qldt_report_template.html`), dùng Python đọc tệp này, thay thế các placeholder JSON và xuất ra tệp HTML cuối cùng.
- **Lỗi bỏ sót dữ liệu do giới hạn sheet Excel:** Tránh việc giới hạn hoặc hardcode danh sách sheet mục tiêu trong các agent phân tích dữ liệu chỉ số đào tạo. Hãy sử dụng **tự động quét sheet động (Dynamic Sheet Scanning)** bằng cách duyệt qua `wb.sheetnames`, lọc các sheet của lớp học thực tế (ví dụ chứa từ khóa KS24, KS25, SKL) và bỏ qua các sheet nháp/mặc định (Sheet1). Điều này giúp tự động nhận diện và xử lý chính xác khi người dùng bổ sung các sheet lớp mới (như `KS24_AI_Intergration` hay `KS25_QTKD_BA201`).
- **Lỗi gán sai vai trò nhân sự do suy đoán đơn giản:** Tránh việc suy đoán vai trò dựa trên logic cột Lớp trong Excel hoặc gán cứng `'GV'` khi nộp logs. Phải tải tệp cấu hình nguồn chân lý `data/inputs/staff_roles_ranks.md` và so khớp họ tên (chuẩn hóa loại bỏ dấu bằng `strip_accents`) để gán chính xác vai trò thực tế (Leader, Giáo vụ, Trợ giảng, Thực tập sinh, Giảng viên).
- **Lỗi bỏ sót cơ sở Hồ Chí Minh khi đối chiếu thời khóa biểu:** Khi kiểm toán vi phạm tác nghiệp (Agent 3), hãy luôn quét và gộp dữ liệu từ cả hai cơ sở Hà Nội (`1.1. TKB Hà Nội tổng`) và Hồ Chí Minh (`1.2. TKB Hồ Chí Minh tổng`) trong file thời khóa biểu tổng để đảm bảo kiểm toán đầy đủ lịch dạy của nhân sự ở cả hai miền.
- **Lỗi tính trung bình khối không có trọng số (Simple vs Weighted Mean):** Khi tính toán tỷ lệ vi phạm hoặc xu hướng của cả khối học (ví dụ: KS25 HN, KS24 HN, QTKD), việc lấy trung bình cộng đơn giản của các lớp là sai lệch dữ liệu lớn. Bắt buộc phải tính **trung bình có trọng số (weighted average)** bằng cách nhân tỷ lệ của từng lớp với sỉ số của lớp đó (trích xuất từ ngoặc đơn tên lớp, ví dụ `(42)` $\rightarrow$ 42 sinh viên), sau đó chia cho tổng sỉ số của cả khối.
- **Lỗi đọc cột bị ẩn trong Excel (Hidden Columns):** Thư viện `openpyxl` mặc định sẽ đọc dữ liệu từ tất cả các cột, kể cả cột bị ẩn (hidden columns). Trong quản trị đào tạo, cột bị ẩn thường là cột ngày học cũ hoặc cột nháp cần bỏ qua. Bắt buộc phải kiểm tra thuộc tính `hidden` của column dimensions (`sheet.column_dimensions[col_letter].hidden`) và bỏ qua cột đó để đảm bảo tính đúng đắn của dữ liệu đầu ra.


## 4. Kiến trúc Pipeline & Thư mục Báo cáo Nâng cao (Advanced Reports)
- Mọi báo cáo nâng cao, báo cáo ngoài luồng (như báo cáo tháng QLĐT, báo cáo Giám đốc) đều được tổ chức mã nguồn tại thư mục `agents/advanced/` (ví dụ: `agents/advanced/management_audit/`).
- Kết quả đầu ra (HTML/MD) của các báo cáo này được xuất trực tiếp vào các thư mục tương ứng trong `output/dashboards/` và `output/reports/`. Các tệp này được khai báo trong danh sách `whitelist` của `run_pipeline.py` để tránh bị xóa nhầm khi chạy dọn dẹp.
- Mọi file Excel/SQL gốc trước khi đưa vào Agent xử lý đều phải đi qua `DataSanitizer` (Harness) tại `agents/common/data_sanitizer.py` để làm sạch khoảng trắng (tên GV/TG) và lấp giá trị `NaN`, tránh lỗi tính toán (Ví dụ: `PTIT_Chiso.xlsx`).

- Output JSON/HTML của các Agent đều phải đi qua cổng `Validator` (Loop) tại `agents/common/validator.py` để check format và syntax lỗi (như lỗi `{}` của Chart.js). Nếu lỗi sẽ tự động đưa vào LLM (`google-genai`) sửa tối đa 2 lần.
- Pipeline `run_pipeline.py` không bao giờ được dùng `sys.exit(1)` khi một Agent con lỗi. Luôn phải bắt Exception, trả về cờ rẽ nhánh (Graph Fallback) để các Agent khác vẫn có thể tiếp tục chạy. Mọi file output cần được validate tại chỗ ngay sau mỗi bước.
- Tích hợp báo cáo nâng cao: **Bước 4.6** (Advanced QLDT Report: Báo cáo tháng QLĐT) đã được đăng ký và xác thực đầu ra tự động trong `run_pipeline.py`.

## 5. Phân lớp Thư mục Dự án (Project Layering Structure)
Để giữ thư mục gốc sạch sẽ, toàn bộ hệ thống được phân lớp nghiêm ngặt như sau:
- **`agents/core/`**: Chứa các Agent phân tích cốt lõi (1 đến 4).
- **`agents/advanced/`**: Chứa các Agent báo cáo nâng cao (Học tập & Quản lý).
- **`agents/master/`**: Chứa Portal tổng hợp KPI của Master Lead (Agent 5).
- **`agents/common/`**: Chứa các thư viện và script tiện ích dùng chung (Sanitizer, Validator, LLMWiki).
- **`data/inputs/`**: Chứa dữ liệu đầu vào thô/tĩnh (Excel, SQL, MD). Không ghi đè hay sinh file mới ở đây ngoài file backup dữ liệu gốc.
- **`data/processed/`**: Chứa dữ liệu trung gian dạng JSON hoặc log do các Agent sinh ra để giao tiếp chéo.
- **`output/reports/`**: Chứa các báo cáo Markdown phân nhỏ thành `output/reports/core/` (Agent 1-5) và `output/reports/advanced/` (QLĐT, Giám đốc).
- **`output/dashboards/`**: Chứa các dashboard HTML trực quan phân nhỏ thành `output/dashboards/core/` (SPA Portal, các Agent con) và `output/dashboards/advanced/` (Cockpit Giám đốc, QLĐT).
- **`scripts/`**: Chứa các script vận hành chạy nền hoặc đồng bộ tự động (`sync_director.ps1`).
- **`scratch/`**: Chứa các tệp nháp, tệp chuyển đổi dữ liệu tạm thời.

## 6. Đồng bộ Dữ liệu Thời gian chéo (Temporal Cross-Sync)
- **Tránh tự ước lượng điểm số client-side**: Đối với các chu kỳ dài hạn (Weekly, Monthly), điểm số tuân thủ và tổng giờ làm việc phải được lấy trực tiếp từ dữ liệu tính toán chính thống của Python. Tự ước lượng trên client-side dễ gây lệch pha do sự khác biệt trong việc xác định tổng số ngày làm việc thực tế (ví dụ: tuần làm việc 5 ngày nhưng chỉ có 3 ngày nộp log làm cho phép chia client-side ra 100% trong khi Python ra 60%).
- **Linh hoạt hóa logic daily**: Chỉ áp dụng quét và tính toán động client-side đối với chế độ DAILY để phản ánh đúng thực trạng logs và tình trạng nộp báo cáo của ngày được chọn.
- **Động hóa biểu đồ xu hướng theo Khối**: Biểu đồ xu hướng logs theo tuần phải được thiết kế tính toán động theo Khối phòng ban đang chọn, giúp phản ánh đúng tiến trình thực chất của từng bộ phận khi tương tác bộ lọc.
- **Quy chuẩn kích cỡ chữ cho màn hình Widescreen**: Để đảm bảo dễ đọc trên màn hình lớn, cỡ chữ tối thiểu cho bảng thống kê chính là `13px` (không dùng `text-xs` của Tailwind), bảng logs chi tiết là `12px`, và cỡ chữ nhãn ticks trên Chart.js tối thiểu là `10px`.
- **Bộ lọc Khối toàn cầu (Global Department Filtering)**: Khi người dùng lọc Khối phòng ban, bộ lọc phải được áp dụng đồng bộ toàn trang (lọc lại cả các Metric Cards, biểu đồ Top 5 dự án trễ hạn của riêng khối đó, và chuyển đổi biểu đồ khối thành Doughnut vẽ tỉ lệ tải riêng của khối).
- **Phân trang Bảng nhân sự (Table Pagination)**: Đối với danh sách nhân sự đông (như khối CNTT 20+ người), bắt buộc phải áp dụng phân trang (10 dòng/trang) kết hợp màu dòng xen kẽ (Zebra striping) để giữ chiều cao dashboard cố định, giao diện sạch sẽ, tránh cuộn trang quá dài.

## 7. Quản lý Tri thức Tiết kiệm Token (LLMWiki / RAG)
- Tránh chèn trực tiếp các file quy định lớn (`quy_dinh.md`, `Khung_Phat_Khenthuong_ĐT_T62026.md`) vào Prompt của Agent.
- Sử dụng thư viện độc lập `LLMWiki` (`agents/llmwiki.py`) sử dụng FAISS + Gemini Embeddings (`text-embedding-004`) để truy xuất ngữ nghĩa cục bộ.
- Dữ liệu Vector được lưu tại `data/processed/wiki_index.faiss`. Agent chỉ cần gọi hàm `LLMWiki().query("câu hỏi")` để chèn đúng 2-3 block tri thức liên quan nhất, giúp giảm 95% chi phí Token.

## 8. Báo cáo Giám đốc Đào tạo (Director Cockpit)
- **Chuẩn hóa KPI Thời lượng (8h/ngày):** 
  - Khái niệm "Điểm tuân thủ" (0-100) đã bị loại bỏ.
  - Áp dụng chuẩn đánh giá cứng: Thời lượng yêu cầu = `Số ngày làm việc * 8h`. Nếu `Tổng giờ thực tế (calculatedHours) < Thời lượng yêu cầu` sẽ bị gắn thẻ đỏ **CẢNH BÁO (THIẾU GIỜ)**, ngược lại là **ĐẠT CHUẨN**.
- **Tính toán Client-Side Động (Dynamic JS):** 
  - Các thống kê tuần/tháng (`weekly`, `monthly`) đã được chuyển đổi từ việc lấy dữ liệu tĩnh của Python sang quét mảng `rawReports` trực tiếp trên Frontend bằng vòng lặp `datesWeekly` và `datesMonthly`. Điều này giúp bộ lọc Thời gian và Khối hoạt động hoàn toàn chính xác.
  - **Biểu đồ năng suất tuần (Per Capita Daily Hours):** Đã được chuyển đổi sang hiển thị số giờ trung bình/ngày trên đầu người (Mapped và Unmapped) thay vì tổng số giờ thô tích lũy để tránh mất cân đối quy mô nhân sự khi lọc khối phòng ban. Đường định mức được giữ cố định ở mốc `8.0` giờ/ngày.
  - **Tối ưu bố cục UX bộ lọc:** Thanh bộ lọc (Khối/Tải/Tìm kiếm) đã được di chuyển lên phía trên cụm biểu đồ để tạo luồng tương tác tự nhiên từ trên xuống dưới.
- **Bổ sung Tính năng Cập nhật Dữ liệu Động & Cá nhân hóa (Aug 2026):**
  - Đã xuất file dữ liệu chuẩn JSON riêng biệt tại `data/processed/director_dashboard_data.json` và bổ sung nút **"🔄 Cập nhật dữ liệu"** (Dynamic Fetching với fallback offline).
  - Cá nhân hóa Header: *Kính gửi Thầy Nguyễn Duy Quang (Giám đốc Đào tạo)*.
  - Phân loại trực quan lỗi vi phạm trong Drawer xem chi tiết bằng các Badge chuẩn: 🔴 **Lỗi Thi Công** vs 🟧 **Lỗi Chậm Duyệt (PIC)**.
- **Cải tiến & Sửa lỗi Báo cáo Giám đốc Đào tạo (06/08/2026):**
  - **Sửa lỗi lặp dữ liệu biểu đồ:** Khắc phục triệt để lỗi nhân bản dữ liệu cột của biểu đồ Năng suất tuần (Trend Chart) khi chuyển bộ lọc bằng cách chuyển các biến mảng `window._unmappedHoursData` và `window._plannedKpiData` thành các biến cục bộ bên trong hàm `updateTrendChart()` của Frontend.
  - **Tích hợp Pipeline gốc:** Báo cáo Giám đốc Đào tạo đã được tích hợp làm Bước 4.5 trong `run_pipeline.py` và đầu ra `output/dashboards/4_daily_logs_report_director.html` được kiểm duyệt tự động thông qua `validator.py`.
  - **Script tự động hóa chạy nền:** Cung cấp script PowerShell `scripts/sync_director.ps1` hỗ trợ đồng bộ dữ liệu tự động theo chu kỳ định sẵn (mặc định 5 phút) để phục vụ chạy nền.
  - **Thiết kế Bộ lọc Chu kỳ & Tính toán động:** Thay thế dropdown chọn ngày đơn lẻ bằng Bộ chọn Chu kỳ nghiệp vụ (`Tháng 8`, `Tháng 7`, `Tùy chỉnh khoảng ngày`). Toàn bộ việc tính toán giờ logs, số ngày làm việc thực tế/kỳ vọng và điểm tuân thủ KPI đều được tái tính toán động 100% ở phía client-side JS dựa trên khoảng thời gian được lọc.
  - **Sao lưu phục hồi (Rollback):** Đã sao lưu tệp hoạt động ổn định trước đó tại `scratch/generate_report_director_v4.2_bak.py` để phòng ngừa rủi ro.
- **Nhiệm vụ cho phiên kế tiếp:** Phối hợp cùng Thầy Nguyễn Duy Quang kiểm toán trực tiếp dữ liệu sau khi chạy nền đồng bộ ổn định.

## 9. Danh Sách Nhân Sự & Phân Bổ Phòng Ban (44 Nhân sự chính thức)
- Nguồn chân lý duy nhất cho danh sách, vai trò và rank của nhân sự được khai báo tại file [staff_roles_ranks.md](file:///C:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/data/inputs/staff_roles_ranks.md) (hoặc liên kết wiki [[data/inputs/staff_roles_ranks|Danh sách Vai trò & Rank Nhân sự]]). Vui lòng tham chiếu và cập nhật trực tiếp tại tệp đó để đảm bảo đồng bộ với code xử lý báo cáo.

## 10. Quy tắc Kiến trúc Ngữ cảnh Tinh gọn (Clean Context Architecture Rules)
Để tối ưu hóa Token, tăng tốc độ xử lý của Agent và tránh lỗi xung đột chỉ thị/ngữ cảnh lệch pha, bắt buộc toàn bộ Agent trong các phiên làm việc tiếp theo phải tuân thủ nghiêm ngặt các quy tắc sau:
- **Nguyên lý Độc lập Ngữ cảnh (Context Isolation)**:
  - Khi làm việc ở Agent con nào (1 đến 5), chỉ nạp duy nhất file đặc tả của Agent đó (ví dụ: `Agent 1 - Violation Analyst.md` đối với Agent 1) và file `super_memory.md`. Tuyệt đối không nạp chéo tài liệu đặc tả của các Agent con khác.
- **Tách biệt Dữ liệu và Prompt**:
  - Không nhúng danh sách dữ liệu thô (như danh sách nhân sự, định mức thời gian, lịch dạy...) trực tiếp vào prompt hệ thống hay các file Markdown ngữ cảnh.
  - Toàn bộ dữ liệu thô phải được lưu ở các file cấu hình chuyên biệt ở tầng dữ liệu (`data/inputs/*.md` hoặc `.xlsx`). Agent sẽ viết code Python để đọc và xử lý các tệp này ở runtime.
- **Không quét thư mục Archive**:
  - Thư mục `docs/plans/archive/` chứa các tệp kế hoạch lịch sử đã hoàn thành, chỉ dùng cho con người đối chiếu. Toàn bộ các Agent không được quét, đọc hoặc phân tích nội dung của thư mục này để tránh lãng phí Token và nhiễu ngữ cảnh.
- **Đặc tả Động (Living Specification)**:
  - Tài liệu của mỗi Agent tại `docs/agents/` là nguồn chân lý duy nhất (Single Source of Truth) cho logic nghiệp vụ của Agent đó. Khi có thay đổi, phải cập nhật trực tiếp (in-place update) vào file tương ứng, thay vì tạo thêm file kế hoạch mới.



