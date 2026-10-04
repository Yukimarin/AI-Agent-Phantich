# DECISIONS — nhật ký quyết định

> Mỗi quyết định 1 dòng: ngày · quyết định · lý do. Mới nhất ở trên.

| Ngày | Quyết định | Lý do |
|---|---|---|
| 2026-10-04 | Bỏ `super_memory.md`, thay bằng `STATUS.md` (trạng thái) + `domain/quy_chuan_nghiep_vu.md` (tham chiếu) | Bài học đã thành test, danh mục lớp thành registry; văn bản tĩnh dễ lỗi thời và tốn token |
| 2026-10-04 | Không tạo file `docs/plans` cho mỗi phiên; plan xong thì xóa | 33 file plan cũ không ai đọc lại, làm nhiễu tìm kiếm |
| 2026-10-04 | Rút gọn `AGENTS.md`; vai trò Agent 1-5 chuyển `docs/legacy/agent_roles.md` | AGENTS.md được nạp mọi lượt chat |
| 2026-10-04 | Gộp AI-ĐGNL vào `legacy/dgnl/` (subtree, giữ lịch sử); đợt ĐGNL sau làm module M4 | ĐGNL là một phần dự án; dùng chung registry SV |
| 2026-10-04 | Xóa 9 dự án anh em (đã nén `_archive_20261004/`); gộp template NN vào `config/templates/` | Không còn dùng; `generate_hcm_report.py` phụ thuộc template NN |
| 2026-10-04 | Chia tái cấu trúc 2 đợt; chuyển code legacy vào `legacy/` chỉ khi cắt chuyển P6 | Script cũ ghi cứng đường dẫn tương đối |
| 2026-10-04 | Data Agent tự đồng bộ registry từ `lms_list_course_classes` mỗi kỳ | Phát hiện 3 courseClassId cũ (bài học #3) |
| 2026-10-04 | Python là ngôn ngữ duy nhất cho công thức chỉ số; khóa bằng test đối chiếu bản JS | Chấm dứt 3 bản công thức song song |
| 2026-10-04 | Chuyển sang PMO Data Hub: 1 Data Agent, kho theo kỳ, gates, modules | Chồng chéo agent, số liệu lệch, lỗi tái phạm |
