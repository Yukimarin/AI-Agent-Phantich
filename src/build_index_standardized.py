# Master Index Portal Generator with Clean UI and Natural Industry Terms
import os
import sys

def build_index():
    html = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cổng Báo Cáo ĐGNL Lần 1 | Rikkei Education & PTIT</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-main:       #09090b;
            --bg-card:       #18181b;
            --border-color:  #27272a;
            --text-primary:  #f4f4f5;
            --text-secondary:#a1a1aa;
            --text-muted:    #71717a;
            --color-ks24:    #10b981;
            --color-ks25:    #3b82f6;
            --color-qtkd:    #f59e0b;
            --color-master:  #8b5cf6;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', sans-serif; }
        body { background: var(--bg-main); color: var(--text-primary); padding-bottom: 70px; }

        .header {
            background: rgba(18,18,21,0.85); backdrop-filter: blur(14px);
            border-bottom: 1px solid var(--border-color); position: sticky; top: 0; z-index: 200;
        }
        .header-inner {
            max-width: 1200px; margin: 0 auto; padding: 1rem 2rem;
            display: flex; justify-content: space-between; align-items: center;
        }
        .logo-wrap { display: flex; align-items: center; gap: 0.75rem; }
        .logo-badge {
            background: linear-gradient(135deg, var(--color-ks24), var(--color-ks25), var(--color-qtkd));
            color: #fff; width: 42px; height: 42px; border-radius: 10px;
            display: flex; align-items: center; justify-content: center;
            font-family: 'Outfit', sans-serif; font-weight: 800; font-size: 1.15rem;
            box-shadow: 0 4px 16px rgba(59,130,246,0.3);
        }
        .logo-text { font-family: 'Outfit', sans-serif; font-weight: 700; font-size: 1.1rem; color: #fff; }

        .container { max-width: 1200px; margin: 2.5rem auto; padding: 0 2rem; }

        .hero {
            text-align: center; margin-bottom: 2.75rem;
        }
        .hero-title {
            font-family: 'Outfit', sans-serif; font-size: 2.1rem; font-weight: 800;
            color: #fff; margin-bottom: 0.5rem; line-height: 1.3;
        }
        .hero-desc {
            font-size: 0.95rem; color: var(--text-secondary); max-width: 760px; margin: 0 auto; line-height: 1.55;
        }

        .portal-grid {
            display: grid; grid-template-columns: repeat(2, 1fr); gap: 1.25rem; margin-bottom: 2.5rem;
        }

        .portal-card {
            background: var(--bg-card); border: 1px solid var(--border-color);
            border-radius: 14px; padding: 1.5rem; text-decoration: none; color: inherit;
            transition: all 0.25s ease; display: flex; flex-direction: column; position: relative; overflow: hidden;
        }
        .portal-card:hover {
            transform: translateY(-3px); border-color: #52525b;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
        }
        .portal-card::before {
            content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
            background: linear-gradient(90deg, var(--card-accent), #fff);
        }

        .portal-card.master { --card-accent: var(--color-master); grid-column: 1 / -1; }
        .portal-card.ks24   { --card-accent: var(--color-ks24); }
        .portal-card.ks25   { --card-accent: var(--color-ks25); }
        .portal-card.qtkd   { --card-accent: var(--color-qtkd); grid-column: 1 / -1; }

        .card-tag {
            display: inline-block; padding: 0.2rem 0.6rem; border-radius: 999px;
            font-size: 0.72rem; font-weight: 700; margin-bottom: 0.75rem; width: fit-content;
        }
        .card-tag.master { background: rgba(139,92,246,0.15); color: #a78bfa; border: 1px solid rgba(139,92,246,0.3); }
        .card-tag.ks24   { background: rgba(16,185,129,0.15); color: #34d399; border: 1px solid rgba(16,185,129,0.3); }
        .card-tag.ks25   { background: rgba(59,130,246,0.15); color: #60a5fa; border: 1px solid rgba(59,130,246,0.3); }
        .card-tag.qtkd   { background: rgba(245,158,11,0.15); color: #fbbf24; border: 1px solid rgba(245,158,11,0.3); }

        .card-title {
            font-family: 'Outfit', sans-serif; font-size: 1.15rem; font-weight: 700;
            color: #fff; margin-bottom: 0.4rem;
        }
        .card-desc {
            font-size: 0.82rem; color: var(--text-secondary); line-height: 1.5; margin-bottom: 1rem;
        }

        .card-meta-list {
            display: flex; gap: 1rem; font-size: 0.75rem; color: var(--text-muted);
            margin-top: auto; padding-top: 0.75rem; border-top: 1px solid var(--border-color);
        }

        .footer {
            text-align: center; font-size: 0.75rem; color: var(--text-muted);
            margin-top: 2.5rem; border-top: 1px solid var(--border-color); padding-top: 1.25rem;
        }
    </style>
</head>
<body>

    <header class="header">
        <div class="header-inner">
            <div class="logo-wrap">
                <div class="logo-badge">RKE</div>
                <div>
                    <div class="logo-text">Cổng Báo Cáo Khảo Thí &amp; ĐGNL Lần 1</div>
                    <div style="font-size:0.72rem;color:var(--text-muted);">Phòng Chuyên Môn &amp; Khảo Thí Đào Tạo | PTIT Rikkei Education</div>
                </div>
            </div>
            <div style="font-size:0.76rem;color:var(--text-muted);text-align:right;">
                Ban Giám Đốc Đào Tạo<br>
                Cập nhật: 02/09/2026
            </div>
        </div>
    </header>

    <div class="container">

        <div class="hero">
            <h1 class="hero-title">Hệ Thống Báo Cáo Khảo Thí Đa Chiều</h1>
            <p class="hero-desc">
                Quản trị và tra cứu dữ liệu khảo thí ĐGNL Lần 1 cho toàn bộ <strong>735 sinh viên</strong>: 
                <strong>Khóa KS24 CNTT (Java)</strong>, <strong>Khóa KS25 CNTT (Python)</strong> và <strong>Khối K25 QTKD</strong>.
            </p>
        </div>

        <div class="portal-grid">

            <!-- MASTER EXECUTIVE CARD -->
            <a href="Executive_Summary_DGNL_Report.html" class="portal-card master">
                <span class="card-tag master">🏛️ BÁO CÁO CẤP ĐIỀU HÀNH DÀNH CHO GIÁM ĐỐC ĐÀO TẠO</span>
                <div class="card-title">Báo Cáo Tổng Hợp Toàn Hệ Thống (KS24, KS25 &amp; K25 QTKD)</div>
                <div class="card-desc">
                    Tổng hợp đối soát 3 khối đào tạo (735 SV), phân tích 6 lăng kính chuyên sâu, ma trận chẩn đoán phân hóa năng lực và 4 điểm nghẽn học thuật kèm kế hoạch can thiệp 3 tầng.
                </div>
                <div class="card-meta-list">
                    <span>👥 Quy mô: 735 SV (594 đã thi)</span>
                    <span>📊 3 Khối Đào Tạo</span>
                    <span>🎯 Mock Interview &amp; Live-Coding</span>
                </div>
            </a>

            <!-- KS24 CARD -->
            <a href="KS24_DGNL_Report.html" class="portal-card ks24">
                <span class="card-tag ks24">☕ KHÓA KS24 CNTT – JAVA / SPRING BOOT</span>
                <div class="card-title">Báo Cáo ĐGNL Khóa KS24 (Cuối Kỳ III)</div>
                <div class="card-desc">
                    Đánh giá 200 SV thuộc 5 lớp (HN &amp; HCM). Chẩn đoán phân hóa giữa 29 SV giỏi code yếu vấn đáp (Mock Interview 1-on-1) và 20 SV thế mạnh KNM cần chuyển luồng BA/QA.
                </div>
                <div class="card-meta-list">
                    <span>👥 200 SV</span>
                    <span>☕ Spring Boot</span>
                    <span>🔇 Mock Interview 1-on-1</span>
                </div>
            </a>

            <!-- KS25 CARD -->
            <a href="KS25_DGNL_Report.html" class="portal-card ks25">
                <span class="card-tag ks25">🐍 KHÓA KS25 CNTT – FASTAPI / PYTHON</span>
                <div class="card-title">Báo Cáo ĐGNL Khóa KS25 (Giữa Kỳ II)</div>
                <div class="card-desc">
                    Đánh giá 429 SV thuộc 12 lớp (HN &amp; HCM). Phân tích độ lệch giữa lý thuyết trắc nghiệm và Live-Coding (151 SV), kế hoạch phân tầng Live-Coding Bootcamp Kỳ III.
                </div>
                <div class="card-meta-list">
                    <span>👥 429 SV</span>
                    <span>🐍 FastAPI/Python</span>
                    <span>💻 Live-Coding Bootcamp</span>
                </div>
            </a>

            <!-- QTKD CARD -->
            <a href="QTKD_DGNL_Report.html" class="portal-card qtkd">
                <span class="card-tag qtkd">💼 KHỐI K25 QTKD – QUẢN TRỊ KINH DOANH</span>
                <div class="card-title">Báo Cáo ĐGNL Khối K25 Quản Trị Kinh Doanh</div>
                <div class="card-desc">
                    Đánh giá 105 SV thuộc 3 lớp và 11 nhóm dự án thực chiến. Đánh giá thế mạnh thuyết trình dự án và giải pháp bù đắp khoảng trống chuẩn đầu ra Ngoại ngữ (40 SV).
                </div>
                <div class="card-meta-list">
                    <span>👥 105 SV</span>
                    <span>📁 11 Nhóm Dự Án</span>
                    <span>🌐 Business English Workshop</span>
                </div>
            </a>

        </div>

        <div class="footer">
            <div>Phòng Chuyên Môn &amp; Khảo Thí Đào Tạo – Hệ Thống PTIT Rikkei Education</div>
            <div style="margin-top:0.25rem;">Bản quyền báo cáo nội bộ © 2026. Tất cả dữ liệu đã được bảo mật theo quy định học thuật.</div>
        </div>

    </div>

</body>
</html>
"""
    with open("outputs/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Updated outputs/index.html successfully!")

if __name__ == "__main__":
    build_index()
