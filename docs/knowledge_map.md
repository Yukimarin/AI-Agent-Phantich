# Bản đồ Tri thức Dự án (Knowledge Map MOC)

Chào mừng bạn đến với Bản đồ Tri thức Trung tâm của dự án Phân tích Chỉ số Đào tạo và Đánh giá KPI GV/TG. Tài liệu này đóng vai trò là Map of Content (MOC) để kết nối toàn bộ các tài liệu ghi chú trong Vault Obsidian, giúp hiển thị liên kết đồ thị (Graph view) rõ ràng.

---

## 1. Tri thức cốt lõi & Quy trình
*   [[docs/super_memory|Bộ nhớ siêu cấp (Super Memory)]]: Nhật ký quyết định thiết kế, bài học kinh nghiệm và lịch sử sửa lỗi liên phiên.
*   [[docs/HOW_TO_USE_OBSIDIAN|Hướng dẫn sử dụng Obsidian]]: Cấu hình Vault và cộng đồng plugin cho dự án.
*   [[docs/MULTI_AGENT_WORKFLOW|Quy trình Multi-Agent]]: Mô hình hoạt động và điều phối giữa các Agent.
*   [[docs/ghi_nhan_hieu_chuan|Ghi nhận Hiệu chuẩn]]: Tài liệu phân tích và hiệu chuẩn tham số cho thuật toán dự báo học tập.

---

## 2. Hệ thống Agent hỗ trợ & Lead
*   [[docs/agents/agent_lead_master_evaluator|Agent Lead: MasterEvaluator]]: Tổng hợp điểm KPI và xuất bản báo cáo.
*   [[docs/agents/agent_1_violation_analyst|Sub Agent 1: ViolationAnalyst]]: Chuyên phân tích lỗi kỷ luật học viên.
*   [[docs/agents/agent_2_academic_predictor|Sub Agent 2: AcademicPredictor]]: Phân tích học lực, GPA và cảnh báo nguy cơ trượt.
*   [[docs/agents/agent_3_task_aggregator|Sub Agent 3: TaskAggregator]]: Kiểm soát vi phạm tác nghiệp GV/TG.
*   [[docs/agents/agent_4_daily_log_auditor|Sub Agent 4: DailyLogAuditor]]: Kiểm toán chất lượng và tiến độ báo cáo ngày.

---

## 3. Báo cáo Nghiệp vụ Hiện tại
*   [[data/report_kpi_gv_tg|Báo cáo KPI GV/TG]]: Kết quả tổng hợp điểm hiệu suất học kỳ của toàn bộ GV/TG.
*   [[data/student_risk_report|Báo cáo Nguy cơ Học viên]]: Danh sách sinh viên thuộc diện chăm sóc đặc biệt (Care List).
*   [[data/evaluation_metrics|Đánh giá Hiệu năng]]: Đo lường sai số MAE của mô hình dự báo học tập.
*   [[data/Khung_Phat_Khenthuong_ĐT_T62026|Khung Chế tài & Khen thưởng]]: Quy chế thưởng phạt năng suất đào tạo.
*   [[data/QUY_DINH_KHUNG_CHE_TAI_VA_KHEN_THUONG_NANG_SUAT_DAO_TAO|Quy chế Chế tài & Khen thưởng Đào tạo]]: Văn bản quy chế khung chế tài chính thức.
*   [[data/quy_dinh|Quy định chung]]: Các lỗi và quy chế kỷ luật lớp học.
*   [[data/kpi_giao_ban_tuan|Báo cáo Giao ban Tuần]]: Đánh giá chỉ số đào tạo tuần.
*   [[data/vi_pham_gvtg_khoa_ks25|Chi tiết vi phạm tác nghiệp KS25]]: Lịch sử các ca vi phạm của giảng viên.

---

## 4. Kế hoạch Thiết kế & Phát triển (Plans)
*   [[docs/plans/2026-07-15-automate-agent4-daily-logs|Tự động hóa Agent 4 qua Cronjob]]
*   [[docs/plans/2026-07-15-agent4-dashboard-integration-plan|Tích hợp Tab 3 Tailwind CSS]]
*   [[docs/plans/2026-07-13-daily-logs-integrated-report-plan|Kiểm toán Báo cáo ngày qua Worklane]]
*   [[docs/plans/2026-07-13-daily-logs-kpi-matching|Định mức KPI Công việc]]
*   [[docs/plans/2026-07-10-unified-dashboard-interactive-filters|Bộ lọc động Web Dashboard]]
*   [[docs/plans/2026-07-09-unified-dashboard-premium-design|Thiết kế Master Dashboard Premium]]
*   [[docs/plans/2026-07-09-model-calibration-kpi|Hiệu chuẩn thuật toán giảm sai số]]
*   [[docs/plans/2026-07-02-consecutive-absence-refinement-implementation|Hiệu chỉnh cấm thi chuyên cần]]
*   [[docs/plans/2026-07-02-prediction-risk-refinement-implementation|Phân tầng nguy cơ học viên]]
*   [[docs/plans/2026-06-29-academic-prediction-design|Mô hình dự báo học tập SQLite]]

---

## 5. Báo cáo Lịch sử & Lưu trữ
*   [[reports/student_care_list_multi_level|Care List phân cấp đa tầng (reports/)]]
*   [[reports/student_care_list|Care List gốc (reports/)]]
*   [[reports/academic_predictions_v3|Dự báo học tập v3 (reports/)]]
*   [[reports/khoi_k24_k25_predictions|Dự báo học lực CNTT (reports/)]]
