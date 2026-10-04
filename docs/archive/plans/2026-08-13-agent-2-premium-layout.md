# Agent 2 Premium Layout Implementation Plan

> **For Antigravity:** REQUIRED WORKFLOW: Use `.agent/workflows/execute-plan.md` to execute this plan in single-flow mode.

**Goal:** Tái cấu trúc giao diện HTML Dashboard của Agent 2 thành dạng 3 Tab chuyên nghiệp (Executive Summary, Class List, Care List), tích hợp Slide-over Drawer cho lớp học và loại bỏ hoàn toàn các thuật ngữ AI.

**Architecture:** Sử dụng CSS absolute/fixed cho Slide-over Drawer, JS để quản lý tabs điều hướng, tooltips cho lỗi GV/TG, lọc và xuất dữ liệu CSV trực tiếp trên client.

**Tech Stack:** Python (generate_report.py), HTML, CSS, JavaScript (Chart.js / TailwindCSS style hoặc Vanilla CSS).

---

### Task 1: Thiết kế hệ thống Tab và cấu trúc HTML mới trong `generate_report.py`

**Files:**
* Modify: [`generate_report.py`](file:///C:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/agents/core/agent_2_academic_pred/generate_report.py)

**Step 1: Run verification to check generation execution**
Chạy thử generator: `uv run python agents/core/agent_2_academic_pred/generate_report.py`
Expected: Sinh thành công HTML.

**Step 2: Replace report generator HTML body with 3-tab layout structure**
Sửa đổi hàm `build_unified_prediction_dashboard` trong `generate_report.py` để chèn thanh điều hướng Tabs (không reload trang) và cấu trúc 3 container tương ứng cho 3 tab. Đồng thời thay thế hoàn toàn các từ mang tính AI (ví dụ đổi "AI Model Error" thành "Sai số đánh giá lịch sử", "Dự báo (Luật cũ)" thành "Tỷ lệ đỗ dự kiến").

**Step 3: Run script to verify compilation passes**
Chạy: `uv run python agents/core/agent_2_academic_pred/generate_report.py`
Expected: Báo cáo HTML được sinh thành công mà không gặp lỗi cú pháp.

**Step 4: Commit**
```bash
git add agents/core/agent_2_academic_pred/generate_report.py
git commit -m "feat: restructure Agent 2 report body with 3-tab skeleton and non-AI wording"
```

---

### Task 2: Triển khai Slide-over Drawer & Cảnh báo tác nghiệp tinh giản

**Files:**
* Modify: [`generate_report.py`](file:///C:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/agents/core/agent_2_academic_pred/generate_report.py)

**Step 1: Implement Slide-over drawer styling and JS handler**
Cập nhật CSS trong `generate_report.py` để định nghĩa Slide-over drawer (`#class-drawer`) trượt ra từ góc phải khi có class `.open`, và thẻ backdrop mờ tối màu (`#drawer-backdrop`).
Viết hàm JavaScript `openClassDrawer(class_name)` và `closeClassDrawer()` để quản lý trạng thái hiển thị của drawer, đồng thời tải thông tin chi tiết của lớp được chọn vào drawer (đọc từ dữ liệu JSON nhúng trong trang).

**Step 2: Restructure classes table list**
Sửa đổi hàm tạo bảng danh sách lớp học ở Tab 2:
* Thay thế nút `⚠️ Rà soát` cũ bằng nút `🔍 Chi tiết` kích hoạt drawer.
* Rút gọn lỗi tác nghiệp GV thành icon tam giác cam, hover chuột hiển thị chi tiết qua tooltip CSS thay vì chèn banner lớn làm rối mắt.

**Step 3: Run script and verify output dashboard exists**
Chạy: `uv run python agents/core/agent_2_academic_pred/generate_report.py`
Expected: PASS

**Step 4: Commit**
```bash
git add agents/core/agent_2_academic_pred/generate_report.py
git commit -m "feat: add slide-over drawer and simplified tooltips for Agent 2"
```

---

### Task 3: Tích hợp Care List tập trung và bộ lọc tương tác có nút Export CSV

**Files:**
* Modify: [`generate_report.py`](file:///C:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/agents/core/agent_2_academic_pred/generate_report.py)

**Step 1: Implement Care List table and interactive filters**
Bổ sung bảng tổng hợp toàn bộ sinh viên nguy cơ vào container Tab 3.
Viết JavaScript lắng nghe click các nút filter (`All`, `Red`, `Yellow`, `CNTT`, `QTKD`) để ẩn/hiển thị tương ứng các dòng trong bảng Care List.

**Step 2: Add client-side CSV export function**
Viết hàm JavaScript `exportCareListCSV()` để gom các dòng sinh viên đang hiển thị trên bảng, chuyển đổi thành định dạng CSV (hỗ trợ UTF-8 BOM) và tải xuống trực tiếp trên trình duyệt.

**Step 3: Run full pipeline check**
Chạy: `uv run run_pipeline.py`
Expected: Biên dịch hoàn thành không lỗi. Trang dashboard `output/dashboards/core/agent_2_academic_prediction.html` hiển thị giao diện 3 Tab chuyên nghiệp và các tính năng hoạt động trơn tru.

**Step 4: Commit**
```bash
git add agents/core/agent_2_academic_pred/
git commit -m "feat: implement centralized Care List with filters and CSV export capability"
```
