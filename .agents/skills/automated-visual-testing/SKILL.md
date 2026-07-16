---
name: automated-visual-testing
description: "Instructions for using browser_subagent to test HTML reports and verify page element visibility and click interactions before completion."
---

# Automated Visual Testing Skill

## 1. Nguyên tắc hoạt động
Mọi tệp HTML giao diện (Dashboard, Báo cáo trực quan) được sinh ra hoặc sửa đổi phải được kiểm thử thực tế trên môi trường đồ họa để đảm bảo:
*   Không bị lỗi trắng trang (Blank screen).
*   Không bị lỗi crash JavaScript làm tê liệt các tương tác click tab.
*   Biểu đồ (Canvas/SVG) hiển thị đúng tỉ lệ và màu sắc.

## 2. Quy trình kiểm thử visual bằng Browser Subagent
Trước khi báo cáo hoàn thành công việc hiển thị giao diện cho người dùng, Agent **bắt buộc phải thực hiện các bước sau**:

1.  **Khởi động Browser Subagent**: Gọi công cụ `browser_subagent` trỏ vào đường dẫn file HTML vừa tạo (ví dụ: `file:///c:/Users/DELL/Desktop/AI-Agent/AI_PhantichchisoDT/unified_dashboard.html`).
2.  **Giả lập tương tác**:
    *   Yêu cầu Subagent click thử vào từng nút chọn Tab (Tab 1, Tab 2, Tab 3, Tab 4, Tab 5, Tab 6).
    *   Yêu cầu Subagent click thử vào các thẻ Accordion học viên nguy cơ để kiểm tra xem panel có mở rộng xuống dưới không.
    *   Click nút chuyển đổi Dark/Light mode để kiểm tra khả năng đổi màu.
3.  **Chụp ảnh màn hình (Screenshot)**: Chụp lại ảnh màn hình của từng tab và lưu lại làm bằng chứng kiểm thử visual.
4.  **Kiểm tra Console Logs**: Đọc logs của trình duyệt để đảm bảo không có lỗi `Redeclaration of let/const` hoặc `Uncaught ReferenceError`.
