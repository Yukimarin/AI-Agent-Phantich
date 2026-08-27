# Tích hợp Dữ liệu Mới & Thiết kế Lại Giải pháp Tinh gọn (Agent 1) Implementation Plan

> **For Antigravity:** REQUIRED WORKFLOW: Use `.agent/workflows/execute-plan.md` to execute this plan in single-flow mode.

**Goal:** Đồng bộ tệp dữ liệu chỉ số đào tạo mới nhất (22:09 ngày 17/08) và tối ưu hóa Kế hoạch hành động khắc phục của Agent 1: Rút gọn danh sách hành động xuống còn **2-3 giải pháp đi sâu và thiết thực nhất cho từng vai trò (Giảng viên / Cố vấn học tập)** thay vì liệt kê dài dòng khi lớp mắc nhiều loại vi phạm.

**Architecture:**
1. Định nghĩa một hàm tích hợp giải pháp thông minh `get_integrated_actions(cc_violated, bt_violated, el_violated)` trong `agents/core/agent_1_class_kpi/generate_kpi_report.py`.
2. Hàm này sẽ trả về tối đa **3 giải pháp tích hợp đi sâu** cho GV và **3 giải pháp tích hợp đi sâu** cho CVHT dựa trên các vi phạm thực tế của cohort (thay vì nối tất cả các dòng như trước gây dài dòng).
3. Chạy lại toàn bộ pipeline `run_pipeline.py` để làm sạch dữ liệu mới, chạy lại phân tích và xuất bản báo cáo/dashboard mới.

**Tech Stack:** Python, openpyxl, JSON.

---

### Task 1: Cập nhật logic sinh hành động tích gọn trong `generate_kpi_report.py`

**Files:**
- Modify: `c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/agents/core/agent_1_class_kpi/generate_kpi_report.py`

**Step 1: Write minimal implementation**

Thay đổi logic sinh cảnh báo và hành động tại hàm `generate_cohort_section` để tích hợp giải pháp thông minh và khống chế tối đa 3 hành động.

**Step 2: Run pipeline to verify**

Chạy command: `uv run run_pipeline.py`

**Step 3: Commit**

```bash
git add agents/core/agent_1_class_kpi/generate_kpi_report.py
git commit -m "feat(agent1): consolidate and refine remediation actions to 2-3 deep items per role"
```

---

## Verification Plan

### Automated Tests
- Chạy toàn bộ pipeline để làm sạch dữ liệu mới và xuất bản báo cáo:
  `uv run run_pipeline.py`

### Manual Verification
- Kiểm tra báo cáo sinh ra tại `output/reports/core/agent_1_student_discipline.md`:
  - Số lượng giải pháp của GV và CVHT ở mỗi nhóm lớp/cohort tối đa chỉ là **3 giải pháp tinh gọn, tích hợp**.
  - Không còn tình trạng liệt kê 6-7 giải pháp dài dòng như trước.
- Đảm bảo báo cáo hiển thị số liệu mới từ file Excel vừa cập nhật.
