---
name: premium-dashboard-charts
description: "Guidelines and code templates for building premium SaaS/CRM-style charts using Chart.js or ApexCharts with rich visual aesthetics, gradients, and custom tooltips."
---

# Premium Dashboard Charts Skill

## 1. Thiết kế biểu đồ dạng SaaS/CRM (Aesthetics Guidelines)
Để biểu đồ trông giống các hệ thống CRM hiện đại thay vì biểu đồ mặc định thô sơ:
*   **Gradient Fill (Đổ màu chuyển sắc)**: Thay vì tô một màu đặc (solid color), sử dụng gradient mờ dần từ trên xuống dưới cho biểu đồ đường (Area Chart) và biểu đồ cột.
*   **Shadows (Phủ bóng)**: Thêm bóng đổ mờ bên dưới đường kẻ (line path) để tạo chiều sâu 3D.
*   **Gridlines ẩn**: Tắt các đường lưới dọc (`grid: { x: { display: false } }`), chỉ giữ lại các đường lưới ngang mỏng màu xám nhạt (`rgba(0,0,0,0.05)` hoặc `rgba(255,255,255,0.05)` trong dark mode).
*   **Custom Tooltips**: Định dạng lại tooltip hiển thị khi di chuột để có nền kính mờ (glassmorphism), chữ màu trắng/slate đậm và hiển thị icon tròn màu sắc tương ứng.

## 2. Template cấu hình Chart.js Premium (Area Chart)
```javascript
const ctx = document.getElementById('myChart').getContext('2d');

// Tạo gradient fill
const gradient = ctx.createLinearGradient(0, 0, 0, 400);
gradient.addColorStop(0, 'rgba(99, 102, 241, 0.4)');   // Indigo mờ
gradient.addColorStop(1, 'rgba(99, 102, 241, 0.0)');   // Trong suốt

const myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['Ngày 1', 'Ngày 2', 'Ngày 3', 'Ngày 4'],
        datasets: [{
            label: 'Chỉ số',
            data: [12, 19, 3, 5],
            borderColor: '#6366f1',
            borderWidth: 3,
            fill: true,
            backgroundColor: gradient,
            tension: 0.4, // Tạo đường cong mượt mà
            pointBackgroundColor: '#6366f1',
            pointHoverRadius: 7
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: { display: false } // Ẩn legend thô sơ
        },
        scales: {
            x: { grid: { display: false } },
            y: { 
                grid: { 
                    color: 'rgba(226, 232, 240, 0.3)' // Lưới ngang mờ
                } 
            }
        }
    }
});
```

## 3. Template cấu hình Doughnut Chart Premium (Glassmorphism Center)
*   Thiết lập thuộc tính `cutout: '75%'` để tạo vòng tròn thanh mảnh.
*   Đặt một thẻ `div` định vị tuyệt đối (`absolute`) ở chính giữa vòng tròn để hiển thị số lượng tổng và nhãn chữ với font `Fira Sans` / `Fira Code`.
*   Sử dụng các màu sắc tương phản cao đạt chuẩn WCAG: Emerald Green (`#22C55E`), Royal Blue (`#3B82F6`), Amber (`#D97706`), Crimson Red (`#EF4444`).
