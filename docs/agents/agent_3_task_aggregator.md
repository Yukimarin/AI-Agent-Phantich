# Sub Agent 3: TaskAggregator (Operations Auditor) - Tài liệu tổng hợp hoạt động

Báo cáo này tổng hợp vai trò, cấu trúc dữ liệu, thuật toán tính điểm và các thay đổi phát triển đối với **Sub Agent 3 (TaskAggregator)** trong dự án đánh giá hiệu suất đào tạo.

---

## 1. Vai trò & Mục tiêu
TaskAggregator đóng vai trò là kiểm toán viên kỷ luật tác nghiệp của giảng viên và trợ giảng. Nhiệm vụ chính là:
- Quét và đối chiếu lịch giảng dạy thực tế với nhật ký đào tạo để phát hiện các lỗi vi phạm tác nghiệp (đi muộn, quên điểm danh, phản hồi muộn, thiếu tài liệu...).
- Áp dụng các quy chế thưởng phạt của phòng Đào tạo để chấm điểm Kỷ luật Tác nghiệp cho từng GV/TG.
- Cung cấp điểm số kỷ luật tác nghiệp để kết hợp với điểm Kỷ luật SV (Agent 1) tạo thành điểm Tuân thủ tổng hợp của MasterEvaluator.

---

## 2. Dữ liệu Đầu vào & Đầu ra

### Dữ liệu Đầu vào (Inputs)
- **Thời khóa biểu tổng**: [1. Thời khóa biểu tổng .xlsx](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/data/1.%20Th%E1%BB%9Di%20kh%C3%B3a%20bi%E1%BB%83u%20t%E1%BB%95ng%20.xlsx).
- **Quy chế thưởng phạt**: [Khung_Phat_Khenthuong_ĐT_T62026.md](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/data/Khung_Phat_Khenthuong_%C4%90T_T62026.md) và [QUY ĐỊNH KHUNG CHẾ TÀI VÀ KHEN THƯỞNG NĂNG SUẤT ĐÀO TẠO.md](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/data/QUY%20%C4%90%E1%BB%8ANH%20KHUNG%20CH%E1%BA%BE%20T%C3%80I%20V%C3%80%20KHEN%20TH%C6%AF%E1%BB%9ENG%20N%C4%82NG%20SU%E1%BA%A4T%20%C4%90%C3%80O%20T%E1%BA%A0O.md).

### Dữ liệu Đầu ra (Outputs)
- **Tệp JSON lỗi vi phạm**: [vi_pham_gvtg.json](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/data/vi_pham_gvtg.json) chứa danh sách chi tiết các ca học có lỗi vi phạm tác nghiệp thực tế của GV/TG.
- **Báo cáo Markdown chi tiết theo khóa**: [vi_pham_gvtg_khoa_ks25.md](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/data/vi_pham_gvtg_khoa_ks25.md).
- **Báo cáo HTML trực quan**: [3_gvtg_violations_report.html](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/output/3_gvtg_violations_report.html).

---

## 3. Quy tắc & Thuật toán đối chiếu
- **Đối chiếu tự động 6 lỗi tác nghiệp thực tế**:
  1. *Quên điểm danh*: Ca học đã qua nhưng không ghi nhận trạng thái điểm danh.
  2. *Bỏ sót phép*: Tỷ lệ sinh viên xin nghỉ phép vượt quá định mức quy định nhưng GV/TG không cập nhật đơn hoặc xử lý phê duyệt.
  3. *Chậm tài nguyên*: Giáo án/slide/tài liệu bài giảng không được upload lên hệ thống trước giờ học quy định.
  4. *Thiếu chăm sóc*: Điểm số hoặc feedback bài tập không được cập nhật cho sinh viên sau thời gian tối đa cho phép.
  5. *Chậm học liệu*: Video recording hoặc mã nguồn buổi học không được gửi sau ca học.
  6. *Cố tình sửa chỉ số*: Tự ý thay đổi điểm số/chuyên cần sau khi đã chốt kết quả kỳ học mà không thông qua QLĐT.
- **Chốt chặn thời gian thực**: Bỏ qua các ca học trong tương lai dựa trên thời gian thực tế của hệ thống.
- **Loại bỏ trùng lặp**: Sử dụng `drop_duplicates` trên thời khóa biểu Excel để loại bỏ các ca học trùng lặp ảo (ví dụ các lớp ghép hoặc môn học phân bổ trùng phòng).
- **Chế tài trừ điểm tác nghiệp**:
  - Điểm tác nghiệp xuất phát từ 100 điểm.
  - Số lỗi vi phạm thực tế chốt theo kỳ:
    - 0 lỗi: 100 điểm.
    - 1 lỗi: 100 điểm (nhắc nhở không trừ điểm).
    - 2 lỗi: 95 điểm (trừ 5 điểm).
    - 3 lỗi: 85 điểm (trừ 15 điểm).
    - $\ge$ 4 lỗi: 70 điểm (trừ 30 điểm).

---

## 4. Lịch sử Thay đổi & Quyết định quan trọng
- **[2026-07-10] Tự động hóa quét lỗi tác nghiệp**: Chuyển đổi từ mô hình nhập lỗi thủ công sang quét tự động bằng script Python đối chiếu trực tiếp thời khóa biểu Excel và nhật ký giảng dạy thực tế.
- **[2026-07-10] Nhận diện khung chế tài thưởng phạt mới**: Tích hợp quy định khung chế tài và khen thưởng năng suất đào tạo tháng 6/2026 của phòng Đào tạo làm cơ sở chấm điểm kỷ luật tác nghiệp.

---

## 5. Mã nguồn liên quan
- **Script phân tích lỗi**: [analyze_gvtg_violations.py](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/scratch/analyze_gvtg_violations.py)
- **Script xuất bản báo cáo**: [generate_agent3_report.py](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/scratch/generate_agent3_report.py)
