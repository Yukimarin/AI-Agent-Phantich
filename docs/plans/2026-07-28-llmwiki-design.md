# Design Doc: LLMWiki (RAG Integration)

**Ngày:** 2026-07-28
**Vấn đề:** Các tài liệu nội bộ (ví dụ: `quy_dinh.md`, `Khung_Phat_Khenthuong_ĐT_T62026.md`) có dung lượng rất lớn. Nếu chèn toàn bộ vào System Prompt của Agent mỗi lần chạy sẽ làm ngốn token nghiêm trọng, tốn kém chi phí API, đồng thời làm giảm khả năng tập trung (attention) của mô hình ngôn ngữ.
**Mục tiêu:** Xây dựng một lớp truy xuất tri thức nội bộ bằng kỹ thuật Retrieval-Augmented Generation (RAG).

## 1. Kiến trúc (Architecture)
- **Thành phần mới:** `agents/llmwiki.py` đóng vai trò như một thư viện nội bộ.
- **Thư viện bên thứ 3:** `faiss-cpu` (lưu trữ vector), `numpy`, `google-genai` (tạo vector).
- **Quy trình hoạt động:**
  1. Khi chạy, LLMWiki đọc toàn bộ tài liệu Markdown trong thư mục `data/inputs`.
  2. Băm văn bản (Chunking) thành các block dài khoảng 500 ký tự.
  3. Dùng API Embedding của Google (`text-embedding-004`) biến đổi các block thành Vector.
  4. Lưu trữ các Vector xuống file vật lý `data/processed/wiki_index.faiss` để tái sử dụng, không cần tốn token cho các lần chạy sau.
  5. Agent con gọi hàm `LLMWiki.query("text")`. LLMWiki tìm Top K khối văn bản liên quan nhất và trả về text thô để Agent chèn vào Prompt.

## 2. Ưu điểm & Giảm thiểu Rủi ro (Trade-offs & Mitigations)
- Hệ thống được đóng gói gọn trong **duy nhất 1 file `llmwiki.py`**. Không làm cấu trúc dự án trở nên cồng kềnh hay "hỗn tạp". Các Agent hiện tại chỉ việc thêm 2 dòng code (import và query) để sử dụng.
- Dễ dàng tháo gỡ (Plug-and-play): Nếu sau này muốn tắt RAG, chỉ việc bỏ import đi là xong.
- Vector database cục bộ FAISS rất nhẹ, không yêu cầu thiết lập Docker hay Server Database cồng kềnh.
