# QUY TRÌNH TỐI ƯU HÓA SỬ DỤNG TOKEN (TOKEN OPTIMIZATION PROCESS)

Để đảm bảo hiệu năng tối đa của Agent, giảm chi phí, tăng tốc độ xử lý và tránh tràn cửa sổ ngữ cảnh (Context Window), dự án `AI-ĐGNL` áp dụng các nguyên tắc tối ưu hóa token như sau:

---

## 1. Nguyên Tắc Tra Cứu và Phân Tích Dữ Liệu Lớn

- **Không in toàn bộ dữ liệu thô ra màn hình terminal:** 
  - *Lỗi thường gặp:* Dùng `print()` hoặc `cat` toàn bộ nội dung file CSV/Excel/JSON lớn vào stdout. Điều này làm tăng hàng nghìn dòng văn bản không cần thiết trong lịch sử hội thoại.
  - *Quy trình chuẩn:* Viết code Python thực hiện xử lý dữ liệu và chỉ in ra các thống kê tổng hợp (tổng số hàng, số lượng null, phân bố giá trị, KPIs). Dữ liệu chi tiết lỗi hoặc danh sách đầy đủ sẽ được ghi ra tệp tin trung gian (ví dụ: `scratch/errors.json` hoặc `docs/reports/detail.md`), sau đó sử dụng công cụ `view_file` với tham số `StartLine` và `EndLine` giới hạn để chỉ đọc vùng cần thiết.

- **Đọc file Excel/Word một cách chọn lọc:**
  - Chỉ đọc các sheet hoặc cột cần thiết thay vì tải toàn bộ file vào bộ nhớ và chuyển đổi thành văn bản lớn.
  - Sử dụng tham số `read_only=True` trong `openpyxl` để tải dữ liệu nhanh và tiết kiệm tài nguyên hệ thống.

---

## 2. Nguyên Tắc Cấu Trúc và Quản Lý Tệp Tin

- **Phân tách rõ ràng giữa mã nguồn và dữ liệu:**
  - File dữ liệu thô (Input): đặt trong thư mục [inputs/](file:///c:/Users/DELL/Desktop/AI-Agent/AI-ĐGNL/inputs).
  - Tệp tạm phân tích (Scratch): đặt trong thư mục `scratch/` của artifacts hoặc hệ thống, dọn dẹp ngay sau khi hoàn thành.
  - Báo cáo chính thức (Output): đặt trong thư mục [docs/reports/](file:///c:/Users/DELL/Desktop/AI-Agent/AI-ĐGNL/docs/reports) hoặc [outputs/](file:///c:/Users/DELL/Desktop/AI-Agent/AI-ĐGNL/outputs).

- **Tránh trùng lặp mã nguồn:**
  - Gom các chức năng tái sử dụng (như vẽ biểu đồ, chuẩn hóa tên tiếng Việt, tính toán chỉ số) thành các module dùng chung trong thư mục `src/` thay vì viết lặp lại ở nhiều tệp tin.

---

## 3. Nguyên Tắc Giao Tiếp & Phản Hồi

- **Giữ phản hồi ngắn gọn và trực diện:**
  - Không tóm tắt lại hoặc lặp lại toàn bộ nội dung của các tệp tin/kế hoạch đã được tạo. Trình bày ngắn gọn và trỏ liên kết đến tệp tương ứng.
  - Chỉ làm rõ các quyết định lớn hoặc câu hỏi mở thay vì liệt kê chi tiết quá trình code.

---

## 4. Kiểm Soát Bộ Nhớ Dài Hạn (Super Memory)

- Sử dụng tệp [docs/Super Memory.md](file:///c:/Users/DELL/Desktop/AI-Agent/AI-ĐGNL/docs/Super Memory.md) để cập nhật liên tục trạng thái hiện tại của dự án, các lựa chọn công nghệ và tiến độ của từng khối. Việc này giúp Agent nhớ được toàn bộ bối cảnh ở các phiên làm việc tiếp theo mà không cần người dùng phải giải thích lại từ đầu.
