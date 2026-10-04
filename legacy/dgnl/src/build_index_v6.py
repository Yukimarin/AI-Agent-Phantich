# -*- coding: utf-8 -*-
"""
Central Portal Index v6 - Ultra-Modern Bento Grid Architecture
"""
import os
import sys

sys.path.append(os.path.dirname(__file__))
from modern_theme import get_shared_css

def build_index_v6():
    css = get_shared_css(primary_color="#3b82f6", accent_color="#8b5cf6")
    html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cổng Báo Cáo Khảo Thí ĐGNL | PTIT Rikkei Education</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        {css}
        .hero {{
            text-align: center;
            padding: 3rem 1rem 2.5rem 1rem;
            max-width: 900px;
            margin: 0 auto;
        }}
        .hero-badge {{
            display: inline-flex; align-items: center; gap: 0.5rem;
            background: rgba(59,130,246,0.12); color: #60a5fa; border: 1px solid rgba(59,130,246,0.3);
            padding: 0.35rem 0.9rem; border-radius: 999px; font-size: 0.78rem; font-weight: 700;
            margin-bottom: 1.25rem; font-family: var(--font-heading);
        }}
        .hero-title {{
            font-family: var(--font-heading); font-size: 2.35rem; font-weight: 800; color: #fff;
            letter-spacing: -0.5px; line-height: 1.2; margin-bottom: 0.85rem;
        }}
        .hero-desc {{
            font-size: 0.95rem; color: var(--text-muted); line-height: 1.6;
        }}
        .portal-grid {{
            display: grid; grid-template-columns: repeat(2, 1fr); gap: 1.5rem; max-width: 1200px; margin: 0 auto 3rem auto;
        }}
        .portal-card {{
            background: var(--bg-card); border: 1px solid var(--border-subtle);
            border-radius: var(--radius-lg); padding: 1.75rem; text-decoration: none;
            color: inherit; display: flex; flex-direction: column; transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative; overflow: hidden;
        }}
        .portal-card:hover {{
            transform: translateY(-4px); border-color: var(--border-focus);
            box-shadow: 0 12px 30px rgba(0,0,0,0.5);
        }}
        .portal-card::before {{
            content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
            background: var(--card-accent, #3b82f6);
        }}
        .portal-icon {{
            width: 48px; height: 48px; border-radius: var(--radius-md);
            display: flex; align-items: center; justify-content: center;
            font-size: 1.5rem; margin-bottom: 1.25rem;
            background: rgba(255,255,255,0.03); border: 1px solid var(--border-subtle);
        }}
        .portal-card-title {{
            font-family: var(--font-heading); font-size: 1.2rem; font-weight: 700; color: #fff;
            margin-bottom: 0.4rem; display: flex; align-items: center; justify-content: space-between;
        }}
        .portal-card-desc {{
            font-size: 0.82rem; color: var(--text-muted); line-height: 1.5; margin-bottom: 1.25rem;
        }}
        .portal-meta {{
            margin-top: auto; padding-top: 1rem; border-top: 1px solid var(--border-subtle);
            display: flex; justify-content: space-between; align-items: center; font-size: 0.76rem; color: var(--text-dim);
        }}
        .portal-btn-text {{
            color: var(--card-accent, #3b82f6); font-weight: 700; display: flex; align-items: center; gap: 0.35rem; font-size: 0.82rem;
        }}
    </style>
</head>
<body>

    <header class="header">
        <div class="header-inner">
            <div class="logo-wrap">
                <div class="logo-badge">RKE</div>
                <div>
                    <div class="logo-title">Hệ Thống Báo Cáo Khảo Thí ĐGNL Lần 1</div>
                    <div class="logo-sub">Viện Công Nghệ &amp; Đào Tạo PTIT – Rikkei Education</div>
                </div>
            </div>
            <div class="header-meta">
                Hội Đồng Chuyên Môn &amp; Khảo Thí<br>
                Năm Học 2026 – 2027
            </div>
        </div>
    </header>

    <div class="container">

        <div class="hero">
            <div class="hero-badge">🏛️ Hệ Thống Quản Trị Khảo Thí &amp; Kiểm Định Giáo Dục</div>
            <h1 class="hero-title">Báo Cáo Phân Tích Năng Lực Sinh Viên Toàn Hệ Thống</h1>
            <p class="hero-desc">
                Cung cấp bức tranh toàn cảnh 735 sinh viên qua 6 lăng kính khảo thí chuyên sâu, ma trận chẩn đoán phân hóa, quyết sách điều chỉnh khung chương trình đào tạo và lộ trình can thiệp sư phạm 3 tầng.
            </p>
        </div>

        <div class="portal-grid">

            <!-- Executive Summary -->
            <a href="Executive_Summary_DGNL_Report.html" class="portal-card" style="--card-accent: #3b82f6; grid-column: span 2;">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                    <div class="portal-icon" style="color:#60a5fa;">🏛️</div>
                    <span class="action-tag core" style="background:rgba(59,130,246,0.15);color:#60a5fa;">Dành Cho Ban Giám Đốc</span>
                </div>
                <div class="portal-card-title">
                    Báo Cáo Tổng Hợp Toàn Hệ Thống (Executive Summary)
                    <span style="font-size:1.1rem;">→</span>
                </div>
                <p class="portal-card-desc">
                    Tổng hợp 735 SV (KS24, KS25, QTKD), 4 điểm nghẽn chiến lược, 6 lăng kính học thuật, quyết sách điều chỉnh khung chương trình đào tạo và kế hoạch can thiệp 3 tầng cấp bách cho Ban Giám Đốc.
                </p>
                <div class="portal-meta">
                    <span>📊 Tổng Sĩ Số: 735 SV • 20 Lớp Học (HN &amp; HCM)</span>
                    <span class="portal-btn-text">Truy Cập Báo Cáo Ban Giám Đốc →</span>
                </div>
            </a>

            <!-- KS24 Report -->
            <a href="KS24_DGNL_Report.html" class="portal-card" style="--card-accent: #10b981;">
                <div class="portal-icon" style="color:#34d399;">☕</div>
                <div class="portal-card-title">
                    Khóa KS24 CNTT (Java / Spring Boot)
                    <span style="font-size:1.1rem;">→</span>
                </div>
                <p class="portal-card-desc">
                    Đánh giá nghiệm thu Cuối Kỳ III. Điều chỉnh môn Microservices, DevOps, AI và đề xuất 2 môn tự chọn mới ở Kỳ V mở rộng cơ hội việc làm.
                </p>
                <div class="portal-meta">
                    <span>👨‍🎓 Sĩ số: 200 SV • 5 Lớp</span>
                    <span class="portal-btn-text" style="color:#34d399;">Xem Chi Tiết KS24 →</span>
                </div>
            </a>

            <!-- KS25 Report -->
            <a href="KS25_DGNL_Report.html" class="portal-card" style="--card-accent: #3b82f6;">
                <div class="portal-icon" style="color:#60a5fa;">🐍</div>
                <div class="portal-card-title">
                    Khóa KS25 CNTT (FastAPI / Python)
                    <span style="font-size:1.1rem;">→</span>
                </div>
                <p class="portal-card-desc">
                    Khảo sát Giữa Kỳ II. Giảm tải lý thuyết môn Phân tích thiết kế/Agile, bồi dưỡng FastAPI Intensive 2 tuần, bổ sung môn ReactJS/NextJS và DSA ở Kỳ III.
                </p>
                <div class="portal-meta">
                    <span>👨‍🎓 Sĩ số: 429 SV • 12 Lớp</span>
                    <span class="portal-btn-text" style="color:#60a5fa;">Xem Chi Tiết KS25 →</span>
                </div>
            </a>

            <!-- QTKD Report -->
            <a href="QTKD_DGNL_Report.html" class="portal-card" style="--card-accent: #f59e0b; grid-column: span 2;">
                <div class="portal-icon" style="color:#fbbf24;">💼</div>
                <div class="portal-card-title">
                    Khối K25 Quản Trị Kinh Doanh
                    <span style="font-size:1.1rem;">→</span>
                </div>
                <p class="portal-card-desc">
                    Nghiệm thu 11 nhóm đề án kinh doanh thực chiến. Điều chỉnh tích hợp Business English Workshop và chuẩn TOEIC 450+ tốt nghiệp.
                </p>
                <div class="portal-meta">
                    <span>👨‍🎓 Sĩ số: 105 SV • 3 Lớp • 11 Nhóm Đề Án</span>
                    <span class="portal-btn-text" style="color:#fbbf24;">Xem Chi Tiết QTKD →</span>
                </div>
            </a>

        </div>

        <div class="footer-bar">
            <div>Viện Công Nghệ &amp; Đào Tạo PTIT Rikkei Education | Phòng Khảo Thí &amp; Đảm Bảo Chất Lượng</div>
            <div>Báo Cáo Khảo Thí ĐGNL Lần 1 © 2026.</div>
        </div>

    </div>

</body>
</html>
"""
    with open("outputs/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Compiled outputs/index.html v6 successfully!")

if __name__ == "__main__":
    build_index_v6()
