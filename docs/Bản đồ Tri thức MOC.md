# Bản đồ Tri thức Dự án (Knowledge Map MOC)

Chào mừng bạn đến với Bản đồ Tri thức Trung tâm của dự án Phân tích Chỉ số Đào tạo và Đánh giá KPI GV/TG. Tài liệu này đóng vai trò là Map of Content (MOC) để kết nối toàn bộ các tài liệu ghi chú trong Vault Obsidian, giúp hiển thị liên kết đồ thị (Graph view) rõ ràng.

---

## 1. Tri thức cốt lõi & Quy trình
*   [[super_memory|Bộ nhớ siêu cấp (Super Memory)]]: Nhật ký quyết định thiết kế, bài học kinh nghiệm và lịch sử sửa lỗi liên phiên.
*   [[Hướng dẫn sử dụng Obsidian|Hướng dẫn sử dụng Obsidian]]: Cấu hình Vault và cộng đồng plugin cho dự án.
*   [[Quy trình Multi-Agent Workflow|Quy trình Multi-Agent]]: Mô hình hoạt động và điều phối giữa các Agent.
*   [[Model Calibration Notes|Ghi nhận Hiệu chuẩn]]: Tài liệu phân tích và hiệu chuẩn tham số cho thuật toán dự báo học tập.

---

## 2. Hệ thống Agent hỗ trợ & Lead
*   [[agents/Agent Lead - Master Evaluator|Agent Lead: MasterEvaluator]]
*   [[agents/Agent 1 - Violation Analyst|Sub Agent 1: ViolationAnalyst]]
*   [[agents/Agent 2 - Academic Predictor|Sub Agent 2: AcademicPredictor]]
*   [[agents/Agent 3 - Task Aggregator|Sub Agent 3: TaskAggregator]]
*   [[agents/Agent 4 - Daily Log Auditor|Sub Agent 4: DailyLogAuditor]]

---

## 3. Báo cáo Nghiệp vụ & Dữ liệu Hiện tại (Cấu trúc mới)
*   [[output/reports/report_kpi_gv_tg|Báo cáo KPI Tổng hợp GV/TG]]: Đánh giá xếp loại năng lực GV/TG học kỳ theo khung tiêu chuẩn mới 2026.
*   [[output/reports/report_agent4|Báo cáo Nhật ký Công việc GV/TG]]: Thống kê nhật ký và khai báo định mức công việc.
*   [[output/reports/student_risk_report|Báo cáo Nguy cơ Học viên]]: Phân tầng học viên có nguy cơ trượt để đưa vào Care List.
*   [[output/reports/evaluation_metrics|Đánh giá Hiệu năng Mô hình (MAE)]]: Đo lường sai số dự đoán.
*   [[output/reports/kpi_giao_ban_tuan|Báo cáo Giao ban Tuần]]: Đánh giá chỉ số đào tạo tuần của giảng viên.
*   [[output/reports/vi_pham_gvtg_khoa_ks25|Chi tiết Vi phạm Tác nghiệp (Khoa KS25)]]: Lịch sử vi phạm của GV/TG.
*   **Tài liệu Quy chế & Quy định gốc:**
    *   [[data/inputs/Khung_Phat_Khenthuong_ĐT_T62026.md|Khung Chế tài & Khen thưởng]]: Quy chế thưởng phạt năng suất đào tạo.
    *   [[data/inputs/quy_dinh|Quy định chung]]: Các lỗi và quy chế kỷ luật lớp học.

---

## 4. Kế hoạch Thiết kế & Phát triển (Plans)
*   [[plans/2026-07-28-llmwiki-design|Thiết kế RAG LLMWiki tiết kiệm Token]]
*   [[plans/2026-07-28-refactor-pipeline-design|Thiết kế Tinh gọn & Phân lớp Dữ liệu]]
*   [[plans/2026-07-26-daily-logs-cross-verification-design|Kiểm toán Báo cáo ngày (Cross-verification)]]
*   [[plans/2026-07-23-agent4-project-management-design|Tích hợp quản lý dự án Agent 4]]
*   [[plans/Plan - 2026-07-15 Automate Agent 4 Daily Logs|Tự động hóa Agent 4 qua Cronjob]]
*   [[plans/Plan - 2026-07-15 Agent 4 Dashboard Integration Plan|Tích hợp Tab 3 Tailwind CSS]]
*   [[plans/Plan - 2026-07-13 Daily Logs Integrated Report Plan|Kiểm toán Báo cáo ngày qua Worklane]]
*   [[plans/Plan - 2026-07-13 Daily Logs KPI Matching|Định mức KPI Công việc]]
*   [[plans/Plan - 2026-07-10 Unified Dashboard Interactive Filters|Bộ lọc động Web Dashboard]]
*   [[plans/Plan - 2026-07-09 Unified Dashboard Premium Design|Thiết kế Master Dashboard Premium]]
*   [[plans/Plan - 2026-07-09 Model Calibration KPI|Hiệu chuẩn thuật toán giảm sai số]]
*   [[plans/Plan - 2026-07-02 Consecutive Absence Refinement Implementation|Hiệu chỉnh cấm thi chuyên cần]]
*   [[plans/Plan - 2026-07-02 Prediction Risk Refinement Implementation|Phân tầng nguy cơ học viên]]
*   [[plans/Plan - 2026-06-29 Academic Prediction Design|Mô hình dự báo học tập SQLite]]

---

## 5. Báo cáo Lịch sử & Báo cáo con các Agent (output/reports/)
*   [[output/reports/report_agent1|Báo cáo Chi tiết Kỷ luật Học viên (Agent 1)]]
*   [[output/reports/report_agent2|Báo cáo Chi tiết Học lực Học viên (Agent 2)]]
*   [[output/reports/report_agent3|Báo cáo Chi tiết Kỷ luật GV/TG (Agent 3)]]
*   [[output/reports/student_care_list_multi_level|Care List phân cấp đa tầng]]
*   [[output/reports/three_recent_courses_report|Báo cáo kết quả 3 môn gần nhất]]
*   [[output/reports/vi_pham_gvtg_cntt1_ks25|Báo cáo vi phạm lớp CNTT1 KS25]]