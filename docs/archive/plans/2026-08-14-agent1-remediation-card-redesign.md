# Design: Tái thiết kế Thẻ Giải Pháp Agent 1 (Remediation Card v2.0)

**Ngày:** 2026-08-14  
**Phạm vi:** `agents/core/agent_1_class_kpi/generate_kpi_report.py` — hàm `generate_cohort_section()`

---

## Vấn đề

Thẻ giải pháp hiện tại (3 cột GV/TG · GVCN · PMO) có 2 vấn đề:
1. Chiếm quá nhiều không gian dọc, phải cuộn xuống mới thấy bảng dữ liệu lớp
2. Lẫn lộn vai trò — trong báo cáo hằng ngày chỉ có 2 người thực thi: **Giảng viên lớp** và **Cố vấn học tập**

---

## Design Đã Chốt

### Cấu trúc: Banner + 2 Hàng xếp dọc

```
┌─────────────────────────────────────────────────────┐
│ 🚨 N vấn đề phát hiện tuần này                      │  ← Banner đỏ cố định
│  • Vắng chuyên cần tăng (+X.X%)                     │
│  • Nợ bài tập tăng (+X.X%)                          │
└─────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────┐
│ 👨‍🏫 Giảng Viên Lớp — Thực hiện trong 24–48h         │  ← Hàng 1
│  • [Action 1 cụ thể theo vi phạm phát hiện]        │
│  • [Action 2 cụ thể theo vi phạm phát hiện]        │
└─────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────┐
│ 🧑‍💼 Cố Vấn Học Tập — Thực hiện trong tuần này       │  ← Hàng 2
│  • [Action 1 cụ thể theo vi phạm phát hiện]        │
│  • [Action 2 cụ thể theo vi phạm phát hiện]        │
└─────────────────────────────────────────────────────┘
```

### Quy tắc nội dung

- **Mỗi hàng có tối thiểu 2 hành động** (không giới hạn trên, tối đa 3)
- Actions được **tổng hợp từ tất cả vi phạm được phát hiện** (CC + BT + EL) thay vì liệt kê riêng từng loại
- Khi không có vi phạm tăng → hiện banner xanh `✅ Ổn định` ngắn gọn, **không hiện 2 hàng**

### Màu sắc

| Phần | Màu viền trái | Màu nền |
|---|---|---|
| Banner vấn đề | `#ef4444` (đỏ) | `rgba(239,68,68,0.1)` |
| Hàng GV | `#f59e0b` (cam vàng) | `rgba(245,158,11,0.08)` |
| Hàng Cố vấn | `#3b82f6` (xanh dương) | `rgba(59,130,246,0.08)` |
| Banner ổn định | `#10b981` (xanh lá) | `rgba(16,185,129,0.1)` |

---

## Thay đổi Code

**File:** `generate_kpi_report.py`  
**Hàm:** `generate_cohort_section()` — phần build `ai_insights`

Xóa `render_remediation_cards()` 3-cột cũ. Thay bằng logic mới:
1. Thu thập tất cả actions GV và Cố vấn từ các vi phạm phát hiện
2. Deduplicate (tránh lặp action khi nhiều vi phạm cùng lúc)
3. Render 2 hàng dọc

---

## Phê duyệt

- [x] User đã approve design (14/08/2026 18:36)
