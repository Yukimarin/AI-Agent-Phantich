# Agent Lead: MasterEvaluator - Tài liệu tổng hợp hoạt động

Báo cáo này tổng hợp vai trò, cấu trúc dữ liệu, thuật toán tính điểm và các thay đổi phát triển đối với **Agent Lead (MasterEvaluator)** trong dự án đánh giá hiệu suất đào tạo.

---

## 1. Vai trò & Mục tiêu
MasterEvaluator đóng vai trò là Agent điều phối trung tâm. Nhiệm vụ chính là:
- Đọc kết quả phân tích từ các Subagent 1, 2, 3, và 4.
- Tổng hợp và tính toán điểm KPI cuối cùng của Giảng viên (GV) & Trợ giảng (TG) theo các trọng số quy định.
- Tự động tạo báo cáo KPI tổng hợp dưới định dạng Markdown, chèn Wiki-links liên kết chéo sang Care List của từng lớp học trong Obsidian.
- Đồng bộ hóa kết quả chấm điểm và nhận xét vào Web Dashboard tích hợp.

---

## 2. Dữ liệu Đầu vào & Đầu ra

### Dữ liệu Đầu vào (Inputs)
1. **Điểm Kỷ luật SV**: Điểm số kỷ luật của sinh viên do **Agent 1** (ViolationAnalyst) phân tích từ tệp Excel học vụ `data/PTIT_Chiso.xlsx`.
2. **Điểm Kỷ luật Tác nghiệp GV/TG**: Điểm trừ do vi phạm tác nghiệp thực tế của GV/TG do **Agent 3** (TaskAggregator) quét đối chiếu từ Excel thời khóa biểu.
3. **Điểm Học tập**: Tỷ lệ sinh viên đỗ thực tế hoặc dự đoán do **Agent 2** (AcademicPredictor) phân tích từ database MySQL/SQLite.
4. **Điểm Báo cáo ngày**: Điểm hiệu suất báo cáo ngày (Work Score) do **Agent 4** (Daily Log Auditor) phân tích từ Worklane qua MCP.

### Dữ liệu Đầu ra (Outputs)
1. **Báo cáo KPI Markdown**: Lưu tại [report_kpi_gv_tg.md](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/data/report_kpi_gv_tg.md) để đồng bộ vào Obsidian Vault.
2. **Web Dashboard tích hợp**: Tích hợp các điểm số và nhận xét định tính vào Tab 1 của [5_unified_dashboard.html](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/output/5_unified_dashboard.html).

---

## 3. Quy tắc & Công thức tính KPI
Điểm KPI tổng hợp được tính theo công thức trọng số sau:

$$KPI = Compliance \times 0.40 + Academic \times 0.30 + Work \times 0.30$$

Trong đó:
- **Compliance (Điểm Kỷ luật & Tuân thủ - 40%)**:
  $$Compliance = \frac{\text{Điểm Kỷ luật SV (Agent 1)} + \text{Điểm Kỷ luật Tác nghiệp GV/TG (Agent 3)}}{2.0}$$
  *Lưu ý:* Điểm kỷ luật SV xuất phát từ 100 điểm, trừ đi tỷ lệ vi phạm trung bình của lớp. Điểm tác nghiệp GV/TG xuất phát từ 100 điểm, trừ theo số lỗi tác nghiệp thực tế (1 lỗi nhắc nhở: trừ 0đ; 2 lỗi: trừ 5đ; 3 lỗi: trừ 15đ; $\ge$ 4 lỗi: trừ 30đ).
- **Academic (Điểm Học tập - 30%)**:
  Lấy điểm trung bình tỷ lệ đỗ của các lớp do GV/TG phụ trách (từ dữ liệu dự đoán hoặc thực tế của Agent 2).
- **Work (Điểm Báo cáo ngày - 30%)**:
  Lấy điểm hiệu suất báo cáo ngày (Work Score) từ phân tích dữ liệu Worklane của Agent 4.

---

## 4. Lịch sử Thay đổi & Quyết định quan trọng
- **[2026-07-10] Tái cấu trúc logic tính KPI**: Chuyển đổi công thức tính điểm cũ sang công thức mới phân định rõ ranh giới trách nhiệm: Gộp Kỷ luật SV và Kỷ luật tác nghiệp làm Điểm Tuân thủ (40%), Điểm Học tập (30%), và tách riêng Điểm Báo cáo ngày làm một cột độc lập (30%).
- **[2026-07-10] Tích hợp nhận xét định tính động**: Đọc các lỗi vi phạm tác nghiệp thực tế và lỗi báo cáo ngày (chậm trễ, thiếu logs, vượt định mức) để tự động sinh ra Điểm yếu và Đề xuất cải thiện chi tiết cho từng cá nhân, thay vì dùng các mẫu nhận xét tĩnh.
- **[2026-07-13] Đồng bộ hóa chu kỳ đánh giá**: Đồng bộ chu kỳ đánh giá Work Score mới (bắt đầu từ 13/07/2026) vào tính toán KPI tổng hợp.

---

## 5. Mã nguồn liên quan
- **Script tính toán chính**: [generate_kpi_report.py](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/scratch/generate_kpi_report.py)
- **Script ghép dashboard**: [generate_unified_dashboard.py](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/scratch/generate_unified_dashboard.py)
- **Đường ống tự động**: [run_pipeline.py](file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/scratch/run_pipeline.py)
