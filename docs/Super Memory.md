# Super Memory - Dự án Phân tích Năng lực SV K24/K25 (Hệ PTIT)

## 1. User Preferences (Sở thích & Lựa chọn của Người dùng)
- **Độc lập dự án:** Dự án này là hoàn toàn độc lập, không liên hệ hay chia sẻ dữ liệu với các dự án Agent khác trên hệ thống.
- **Tiến trình xử lý:** Phân tích và làm báo cáo riêng cho từng khối (KS24 trước, sau đó đến KS25). Sau khi kiểm duyệt xong từng khối mới tiến hành xây dựng báo cáo tích hợp chung.
- **Tính thực chiến:** Ưu tiên đánh giá dựa trên yêu cầu năng lực thực tế của doanh nghiệp, bám sát các xu hướng công nghệ hiện đại.

## 2. Core Logic (Quy tắc & Thuật toán lõi)
- Phân tích độ tương thích năng lực theo công thức tỉ lệ phần trăm (%) đáp ứng yêu cầu công việc.
- So sánh năng lực thực tế (điểm đánh giá ĐGNL lần 1) với dữ liệu chương trình đào tạo để tìm ra khoảng trống kỹ năng (skill gaps) và đề xuất điều chỉnh CTĐT.
- Tối ưu hóa token theo quy trình chuẩn (không dump raw stdout, phân tách module, lưu trữ trung gian).

## 3. Current State (Trạng thái Hiện tại)
- **Khóa KS24:** Đã hiệu chỉnh công thức tính điểm Final (HN: có Sản phẩm 30%, Vấn đáp 20%, Exam 50%; HCM: Vấn đáp 40%, Exam 60%), sửa lỗi parser tiêu chí và cập nhật Dashboard HTML tương tác thành công.
- **Khóa KS25 (CNTT):** Đã phân tích dữ liệu ĐGNL lần 1, xác minh công thức `Final = Thực hành * 70% + Trắc nghiệm * 30%` khớp 100% cho toàn bộ 429 học viên.
- **Khóa KS25 (QTKD):** Đang học môn *BA201* (Business Analyst).
- **File dữ liệu CTĐT:** Đã lưu trữ tại [inputs/CTĐT.xlsx](file:///c:/Users/DELL/Desktop/AI-Agent/AI-ĐGNL/inputs/CTĐT.xlsx) và chuyển đổi sang [CTĐT.md](file:///c:/Users/DELL/Desktop/AI-Agent/AI-ĐGNL/docs/reports/CTĐT.md).
- **Kiến trúc Harness Engineering:** Đã thiết lập cấu hình nghiệp vụ tại [job_thresholds.json](file:///c:/Users/DELL/Desktop/AI-Agent/AI-ĐGNL/harness/config/job_thresholds.json) và bộ kiểm soát tại [guardrails.py](file:///c:/Users/DELL/Desktop/AI-Agent/AI-ĐGNL/harness/guardrails.py).
- **Phân tích Roadmap:** Đã lưu trữ tại [roadmap_evaluation.md](file:///c:/Users/DELL/Desktop/AI-Agent/AI-ĐGNL/docs/reports/roadmap_evaluation.md).
- **Báo cáo Đối soát chuyên sâu & Sự cố hệ thống:** Đã hoàn thành tại [ks24_ks25_detailed_analysis.md](file:///c:/Users/DELL/Desktop/AI-Agent/AI-ĐGNL/docs/reports/ks24_ks25_detailed_analysis.md).

## 4. Active Task (Nhiệm vụ đang thực hiện)
- `[x]` Phân tích chi tiết và đối soát dữ liệu ĐGNL Đợt 1 của khối KS24 và KS25.
- `[ ]` Theo dõi kết quả thi bổ sung ngày 22/08/2026 của 263 sinh viên và cập nhật báo cáo tổng kết tích hợp cuối cùng gửi Ban Giám đốc.
