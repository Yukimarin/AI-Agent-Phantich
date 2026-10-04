# Standardized Builder for KS24 Report
import json
import os
import sys

sys.path.append(os.path.dirname(__file__))
from build_complete_suite import load_data

def build_ks24_report(data):
    students = data["ks24"]
    total_reg = len(students)
    active = [s for s in students if not s["is_absent"]]
    total_took = len(active)
    total_pass = len([s for s in students if s["is_pass"] and not s["is_absent"]])
    pass_pct = round(total_pass / total_reg * 100, 1) if total_reg else 0.0

    ready_students = [s for s in students if s["tier"] in [2, 3]]
    ready_pct = round(len(ready_students) / total_reg * 100, 1) if total_reg else 0.0

    avg_final = round(sum(s["final_10"] for s in active) / total_took, 2) if total_took else 0.0
    avg_knm = round(sum(s["knm"] for s in active if s["knm"] > 0) / len([s for s in active if s["knm"] > 0]), 1) if any(s["knm"] > 0 for s in active) else 0.0
    avg_ta = round(sum(s["ta"] for s in active if s["ta"] > 0) / len([s for s in active if s["ta"] > 0]), 1) if any(s["ta"] > 0 for s in active) else 0.0

    # Class stats
    classes = sorted(list(set(s["class"] for s in students)))
    class_stats = {}
    for c in classes:
        c_studs = [s for s in students if s["class"] == c]
        c_act = [s for s in c_studs if not s["is_absent"]]
        c_pass = [s for s in c_studs if s["is_pass"] and not s["is_absent"]]
        c_ready = [s for s in c_studs if s["tier"] in [2, 3]]
        class_stats[c] = {
            "total": len(c_studs),
            "took": len(c_act),
            "pass": len(c_pass),
            "pass_pct": round(len(c_pass) / len(c_studs) * 100, 1),
            "ready": len(c_ready),
            "ready_pct": round(len(c_ready) / len(c_studs) * 100, 1),
            "avg_final": round(sum(s["final_10"] for s in c_act) / len(c_act), 2) if c_act else 0.0,
            "avg_sp": round(sum(s["sp"] for s in c_act) / len(c_act), 1) if c_act else 0.0,
            "avg_vd": round(sum(s["vd"] for s in c_act) / len(c_act), 1) if c_act else 0.0,
            "avg_th": round(sum(s["th"] for s in c_act) / len(c_act), 1) if c_act else 0.0,
            "avg_tn": round(sum(s["tn"] for s in c_act) / len(c_act), 1) if c_act else 0.0,
        }

    # Diagnostics
    diag_counts = {
        "silent": len([s for s in students if "Vững Thực hành Kỹ thuật - Hạn chế Diễn đạt Vấn đáp" in s["persona"]]),
        "shifter": len([s for s in students if "Thế mạnh Giao tiếp" in s["persona"]]),
        "allround": len([s for s in students if "Đạt Chuẩn Năng lực Toàn diện" in s["persona"]]),
        "atrisk": len([s for s in students if "Chưa đạt Chuẩn Kiến thức Cốt lõi" in s["persona"]]),
        "mid": len([s for s in students if "Đạt Mức Trung bình Cơ bản" in s["persona"]]),
        "absent": len([s for s in students if s["is_absent"]])
    }

    students_json = json.dumps(students, ensure_ascii=False)

    # Render class table rows
    class_rows = ""
    for c, st in class_stats.items():
        class_rows += f"""
        <tr>
            <td style="text-align:left;"><strong>{c}</strong></td>
            <td>{st['total']} SV</td>
            <td>{st['took']} SV</td>
            <td><strong style="color:var(--color-primary);">{st['avg_final']}/10</strong></td>
            <td>{st['avg_sp']}</td>
            <td>{st['avg_vd']}</td>
            <td>{st['avg_th']}</td>
            <td>{st['avg_tn']}</td>
            <td><span class="badge pass">{st['pass']} SV ({st['pass_pct']}%)</span></td>
            <td><strong style="color:#34d399;">{st['ready']} SV ({st['ready_pct']}%)</strong></td>
        </tr>
        """

    # Render student table rows
    tbody_rows = ""
    for idx, s in enumerate(students):
        p_badge = f'<span class="badge {s["persona_cls"]}">{s["persona"]}</span>'
        tier_badge = f'<span class="badge lvl-{s["tier"]}">{s["tier_label"].split(" (")[0]}</span>'
        sc_color = "#34d399" if s['final_10'] >= 8.0 else ("#60a5fa" if s['final_10'] >= 6.0 else ("#fbbf24" if s['final_10'] >= 4.0 else "#f87171"))
        
        tbody_rows += f"""
        <tr class="student-row" data-name="{s['name'].lower()}" data-class="{s['class']}" data-tier="{s['tier']}" data-persona="{s['persona']}">
            <td>{idx+1}</td>
            <td style="text-align:left;font-weight:600;color:#fff;">{s['name']}</td>
            <td style="text-align:left;">{s['class']}</td>
            <td><strong style="color:{sc_color};font-size:1.05rem;">{s['final_10']}</strong></td>
            <td>{s['sp']}</td>
            <td>{s['vd']}</td>
            <td>{s['th']}</td>
            <td>{s['tn']}</td>
            <td>{s['knm']}</td>
            <td>{f"{s['ta']:.0f}" if s['ta'] > 0 else '<span style="color:var(--text-muted);">-</span>'}</td>
            <td>{tier_badge}</td>
            <td style="text-align:left;">{p_badge}</td>
            <td style="text-align:left;font-size:0.78rem;color:var(--text-secondary);max-width:280px;">{s['action_plan']}</td>
        </tr>
        """

    html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Báo Cáo ĐGNL Khóa KS24 CNTT (Java / Spring Boot) | Rikkei Education</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <style>
        :root {{
            --bg-main:       #09090b;
            --bg-card:       #18181b;
            --bg-card2:      #1c1c1f;
            --border-color:  #27272a;
            --text-primary:  #f4f4f5;
            --text-secondary:#a1a1aa;
            --text-muted:    #71717a;
            --color-primary: #10b981;   /* Emerald - KS24 Java */
            --color-accent:  #3b82f6;
            --color-success: #10b981;
            --color-warning: #f59e0b;
            --color-danger:  #ef4444;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', sans-serif; }}
        body {{ background: var(--bg-main); color: var(--text-primary); padding-bottom: 80px; }}

        .header {{
            background: rgba(18,18,21,0.85); backdrop-filter: blur(14px);
            border-bottom: 1px solid var(--border-color); position: sticky; top: 0; z-index: 200;
        }}
        .header-inner {{
            max-width: 1440px; margin: 0 auto; padding: 1rem 2rem;
            display: flex; justify-content: space-between; align-items: center;
        }}
        .logo-wrap {{ display: flex; align-items: center; gap: 0.75rem; }}
        .logo-badge {{
            background: linear-gradient(135deg, var(--color-primary), var(--color-accent));
            color: #fff; width: 42px; height: 42px; border-radius: 10px;
            display: flex; align-items: center; justify-content: center;
            font-family: 'Outfit', sans-serif; font-weight: 800; font-size: 1.1rem;
            box-shadow: 0 4px 16px rgba(16,185,129,0.3);
        }}
        .logo-text {{ font-family: 'Outfit', sans-serif; font-weight: 700; font-size: 1.05rem; color: #fff; }}
        .header-meta {{ font-size: 0.78rem; color: var(--text-muted); text-align: right; line-height: 1.4; }}

        .container {{ max-width: 1440px; margin: 2rem auto; padding: 0 2rem; }}

        .nav-tabs {{
            display: flex; gap: 0.5rem; border-bottom: 1px solid var(--border-color);
            margin-bottom: 2rem; overflow-x: auto; padding-bottom: 0.2rem;
        }}
        .tab-btn {{
            background: transparent; border: none; color: var(--text-muted);
            font-family: 'Outfit', sans-serif; font-size: 0.95rem; font-weight: 600;
            padding: 0.75rem 1.25rem; border-radius: 8px 8px 0 0; cursor: pointer;
            transition: all 0.2s; border-bottom: 2px solid transparent;
        }}
        .tab-btn:hover {{ color: var(--text-primary); background: rgba(255,255,255,0.03); }}
        .tab-btn.active {{
            color: var(--color-primary); border-bottom: 2px solid var(--color-primary);
            background: rgba(16,185,129,0.05);
        }}

        .kpi-grid {{
            display: grid; grid-template-columns: repeat(6, 1fr); gap: 1rem; margin-bottom: 2rem;
        }}
        .kpi-card {{
            background: var(--bg-card); border: 1px solid var(--border-color);
            border-radius: 12px; padding: 1.25rem; position: relative; overflow: hidden;
        }}
        .kpi-card::before {{
            content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
            background: linear-gradient(90deg, var(--color-primary), #34d399);
        }}
        .kpi-label {{ font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.5px; color: var(--text-muted); margin-bottom: 0.4rem; }}
        .kpi-value {{ font-family: 'Outfit', sans-serif; font-size: 1.8rem; font-weight: 800; color: #fff; }}
        .kpi-sub   {{ font-size: 0.73rem; color: var(--text-secondary); margin-top: 0.25rem; }}

        .section-title {{
            font-family: 'Outfit', sans-serif; font-size: 1.15rem; font-weight: 700;
            color: #fff; border-left: 4px solid var(--color-primary); padding-left: 0.75rem;
            margin-bottom: 1.25rem; display: flex; justify-content: space-between; align-items: center;
        }}

        .card {{
            background: var(--bg-card); border: 1px solid var(--border-color);
            border-radius: 12px; padding: 1.5rem;
        }}

        .custom-table {{ width: 100%; border-collapse: collapse; font-size: 0.85rem; }}
        .custom-table th, .custom-table td {{ padding: 0.75rem 0.85rem; border: 1px solid var(--border-color); text-align: center; }}
        .custom-table th {{ background: rgba(255,255,255,0.03); color: var(--text-secondary); font-weight: 600; font-size: 0.78rem; text-transform: uppercase; }}
        .custom-table tr:hover {{ background: rgba(255,255,255,0.02); }}

        .badge {{
            display: inline-block; padding: 0.25rem 0.6rem; border-radius: 6px;
            font-size: 0.75rem; font-weight: 700; line-height: 1.3;
        }}
        .badge.pass {{ background: rgba(16,185,129,0.15); color: #34d399; border: 1px solid rgba(16,185,129,0.3); }}
        .badge.fail {{ background: rgba(239,68,68,0.15); color: #f87171; border: 1px solid rgba(239,68,68,0.3); }}
        .badge.lvl-3 {{ background: rgba(139,92,246,0.15); color: #a78bfa; border: 1px solid rgba(139,92,246,0.3); }}
        .badge.lvl-2 {{ background: rgba(16,185,129,0.15); color: #34d399; border: 1px solid rgba(16,185,129,0.3); }}
        .badge.lvl-1 {{ background: rgba(245,158,11,0.15); color: #fbbf24; border: 1px solid rgba(245,158,11,0.3); }}
        .badge.lvl-0 {{ background: rgba(239,68,68,0.15); color: #f87171; border: 1px solid rgba(239,68,68,0.3); }}

        .badge.badge-danger  {{ background: rgba(239,68,68,0.15); color: #f87171; border: 1px solid rgba(239,68,68,0.3); }}
        .badge.badge-warning {{ background: rgba(245,158,11,0.15); color: #fbbf24; border: 1px solid rgba(245,158,11,0.3); }}
        .badge.badge-success {{ background: rgba(16,185,129,0.15); color: #34d399; border: 1px solid rgba(16,185,129,0.3); }}
        .badge.badge-info    {{ background: rgba(59,130,246,0.15); color: #60a5fa; border: 1px solid rgba(59,130,246,0.3); }}
        .badge.badge-muted   {{ background: rgba(255,255,255,0.05); color: #71717a; border: 1px solid #27272a; }}

        .filter-bar {{
            display: flex; gap: 0.75rem; flex-wrap: wrap; margin-bottom: 1.5rem;
            background: var(--bg-card); border: 1px solid var(--border-color);
            padding: 1rem; border-radius: 10px; align-items: center;
        }}
        .filter-input, .filter-select {{
            background: #121214; border: 1px solid var(--border-color);
            color: #fff; padding: 0.55rem 0.85rem; border-radius: 6px; font-size: 0.85rem; outline: none;
        }}

        .tab-pane {{ display: none; }}
        .tab-pane.active {{ display: block; animation: fadeIn 0.3s ease; }}
        @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(6px); }} to {{ opacity: 1; transform: translateY(0); }} }}

        .diag-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 1.5rem; }}
        .diag-box {{
            background: rgba(255,255,255,0.02); border: 1px solid var(--border-color);
            border-radius: 10px; padding: 1rem; cursor: pointer; transition: all 0.2s;
        }}
        .diag-box:hover {{ transform: translateY(-2px); border-color: #52525b; }}

        .report-footer {{
            margin-top: 3rem; border-top: 1px solid var(--border-color);
            padding-top: 1.5rem; display: flex; justify-content: space-between; align-items: center;
            font-size: 0.78rem; color: var(--text-muted);
        }}
    </style>
</head>
<body>

    <header class="header">
        <div class="header-inner">
            <div class="logo-wrap">
                <div class="logo-badge">KS24</div>
                <div>
                    <div class="logo-text">Báo Cáo ĐGNL Khóa KS24 – Hệ CNTT (Java / Spring Boot)</div>
                    <div style="font-size:0.72rem;color:var(--text-muted);">Đánh Giá Nghiệm Thu Cuối Kỳ III – Chuẩn Bị Tốt Nghiệp &amp; Thực Tập Doanh Nghiệp</div>
                </div>
            </div>
            <div class="header-meta">
                Dành cho Giám Đốc Đào Tạo &amp; Hội Đồng Chuyên Môn<br>
                Cập nhật: 02/09/2026 (Dữ liệu sau Khảo thí Bổ sung)
            </div>
        </div>
    </header>

    <div class="container">

        <!-- Navigation Tabs -->
        <div class="nav-tabs">
            <button class="tab-btn active" onclick="switchTab('tab1', event)">📊 Tab 1: Tổng Quan &amp; Lớp Học</button>
            <button class="tab-btn" onclick="switchTab('tab2', event)">🔬 Tab 2: Phân Môn &amp; Tiêu Chí</button>
            <button class="tab-btn" onclick="switchTab('tab3', event)">🎯 Tab 3: Chẩn Đoán Năng Lực</button>
            <button class="tab-btn" onclick="switchTab('tab4', event)">📋 Tab 4: Danh Bạ &amp; Can Thiệp Sư Phạm</button>
        </div>

        <!-- Master KPI Strip -->
        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-label">Sĩ Số Đăng Ký</div>
                <div class="kpi-value">{total_reg}</div>
                <div class="kpi-sub">5 Lớp (HN: 4, HCM: 1)</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Dự Thi Thực Tế</div>
                <div class="kpi-value">{total_took}</div>
                <div class="kpi-sub">Tỷ lệ: {round(total_took/total_reg*100, 1)}%</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Điểm TB Final</div>
                <div class="kpi-value">{avg_final}/10</div>
                <div class="kpi-sub">Thang điểm 10 quy đổi</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Chuẩn Đầu Ra (L2+L3)</div>
                <div class="kpi-value">{len(ready_students)}</div>
                <div class="kpi-sub">Tỷ lệ: {ready_pct}%</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Điểm TB Kỹ Năng Mềm</div>
                <div class="kpi-value">{avg_knm}</div>
                <div class="kpi-sub">Thang điểm 100</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Điểm TB Tiếng Anh</div>
                <div class="kpi-value">{avg_ta:.0f}</div>
                <div class="kpi-sub">Quy đổi TOEIC / 990</div>
            </div>
        </div>

        <!-- TAB 1: TỔNG QUAN -->
        <div id="tab1" class="tab-pane active">
            <div style="background:var(--bg-card);border:1px solid var(--border-color);border-radius:12px;padding:1.5rem;margin-bottom:2rem;">
                <div class="section-title">🏫 Bảng Thống Kê Chỉ Số Khảo Thí Theo Từng Lớp Học (KS24)</div>
                <div style="overflow-x:auto;">
                    <table class="custom-table">
                        <thead>
                            <tr>
                                <th>Mã Lớp</th>
                                <th>Sĩ Số</th>
                                <th>Dự Thi</th>
                                <th>Điểm TB Final</th>
                                <th>Sản Phẩm</th>
                                <th>Vấn Đáp</th>
                                <th>Thực Hành</th>
                                <th>Trắc Nghiệm</th>
                                <th>Tỷ Lệ Đạt</th>
                                <th>Chuẩn Đầu Ra</th>
                            </tr>
                        </thead>
                        <tbody>
                            {class_rows}
                        </tbody>
                    </table>
                </div>
            </div>

            <div style="display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;margin-bottom:2rem;">
                <div class="card">
                    <div class="section-title">📊 So Sánh Điểm TB Theo Cơ Sở (HN vs HCM)</div>
                    <div style="height:260px;position:relative;">
                        <canvas id="branchChart"></canvas>
                    </div>
                </div>
                <div class="card">
                    <div class="section-title">📈 Phân Bố Mức Độ Năng Lực Khóa KS24</div>
                    <div style="height:260px;position:relative;">
                        <canvas id="tierDistChart"></canvas>
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 2: PHÂN MÔN & TIÊU CHÍ -->
        <div id="tab2" class="tab-pane">
            <div class="card" style="margin-bottom:2rem;">
                <div class="section-title">🔬 Ma Trận Đánh Giá Trọng Số &amp; Cấu Trúc Đề Thi KS24</div>
                <div style="display:grid;grid-template-columns:repeat(4, 1fr);gap:1rem;margin-top:1rem;">
                    <div style="background:rgba(255,255,255,0.025);padding:1.2rem;border-radius:8px;border:1px solid var(--border-color);">
                        <div style="font-size:0.75rem;color:var(--text-muted);text-transform:uppercase;">1. Đồ Án / Sản Phẩm (30% HN)</div>
                        <div style="font-family:'Outfit',sans-serif;font-size:1.5rem;font-weight:700;color:var(--color-primary);margin:0.25rem 0;">54.4 / 100</div>
                        <div style="font-size:0.78rem;color:var(--text-secondary);">Đánh giá kiến trúc Web App &amp; ReactJS</div>
                    </div>
                    <div style="background:rgba(255,255,255,0.025);padding:1.2rem;border-radius:8px;border:1px solid var(--border-color);">
                        <div style="font-size:0.75rem;color:var(--text-muted);text-transform:uppercase;">2. Vấn Đáp Chuyên Môn (20% HN / 40% HCM)</div>
                        <div style="font-family:'Outfit',sans-serif;font-size:1.5rem;font-weight:700;color:#3b82f6;margin:0.25rem 0;">50.8 / 100</div>
                        <div style="font-size:0.78rem;color:var(--text-secondary);">Phỏng vấn trực tiếp trước Hội đồng giám khảo</div>
                    </div>
                    <div style="background:rgba(255,255,255,0.025);padding:1.2rem;border-radius:8px;border:1px solid var(--border-color);">
                        <div style="font-size:0.75rem;color:var(--text-muted);text-transform:uppercase;">3. Thực Hành Code (10% HN / 12% HCM)</div>
                        <div style="font-family:'Outfit',sans-serif;font-size:1.5rem;font-weight:700;color:#fbbf24;margin:0.25rem 0;">62.7 / 100</div>
                        <div style="font-size:0.78rem;color:var(--text-secondary);">Viết code API Spring Boot &amp; Xử lý Bug</div>
                    </div>
                    <div style="background:rgba(255,255,255,0.025);padding:1.2rem;border-radius:8px;border:1px solid var(--border-color);">
                        <div style="font-size:0.75rem;color:var(--text-muted);text-transform:uppercase;">4. Trắc Nghiệm (40% HN / 48% HCM)</div>
                        <div style="font-family:'Outfit',sans-serif;font-size:1.5rem;font-weight:700;color:#a78bfa;margin:0.25rem 0;">72.2 / 100</div>
                        <div style="font-size:0.78rem;color:var(--text-secondary);">Lý thuyết OOP, Spring Core, Database</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 3: CHẨN ĐOÁN NĂNG LỰC -->
        <div id="tab3" class="tab-pane">
            <div class="card" style="margin-bottom:2rem;">
                <div class="section-title">🎯 Ma Trận Chẩn Đoán Sư Phạm: Nền Tảng Kỹ Thuật vs Kỹ Năng Phỏng Vấn / Diễn Đạt</div>
                <div style="font-size:0.85rem;color:var(--text-secondary);line-height:1.6;margin-bottom:1.25rem;">
                    Nhấp vào từng nhóm dưới đây để tự động lọc danh bạ học viên tương ứng tại Tab 4:
                </div>

                <div class="diag-grid">
                    <div class="diag-box" onclick="quickFilterDiag('Vững Thực hành Kỹ thuật')" style="border-top:3px solid #ef4444;">
                        <div style="display:flex;justify-content:space-between;align-items:center;">
                            <strong style="color:#f87171;font-size:0.9rem;">🔇 Vững Kỹ Thuật - Yếu Vấn Đáp</strong>
                            <span style="font-weight:800;font-size:1.15rem;color:#fff;">{diag_counts['silent']} SV</span>
                        </div>
                        <div style="font-size:0.75rem;color:var(--text-secondary);margin-top:0.35rem;">
                            Code &ge; 65đ, Vấn đáp &lt; 50đ &rarr; <span style="color:#fca5a5;">Phòng Phỏng Vấn Giả Định 1-1</span>
                        </div>
                    </div>

                    <div class="diag-box" onclick="quickFilterDiag('Thế mạnh Giao tiếp')" style="border-top:3px solid #fbbf24;">
                        <div style="display:flex;justify-content:space-between;align-items:center;">
                            <strong style="color:#fbbf24;font-size:0.9rem;">🗣️ Thế Mạnh KNM - Hạn Chế Code</strong>
                            <span style="font-weight:800;font-size:1.15rem;color:#fff;">{diag_counts['shifter']} SV</span>
                        </div>
                        <div style="font-size:0.75rem;color:var(--text-secondary);margin-top:0.35rem;">
                            KNM &ge; 75đ, Code &lt; 50đ &rarr; <span style="color:#fde68a;">Phân Luồng BA / QA / Sales</span>
                        </div>
                    </div>

                    <div class="diag-box" onclick="quickFilterDiag('Đạt Chuẩn Năng lực Toàn diện')" style="border-top:3px solid #10b981;">
                        <div style="display:flex;justify-content:space-between;align-items:center;">
                            <strong style="color:#34d399;font-size:0.9rem;">🌟 Đạt Chuẩn Toàn Diện</strong>
                            <span style="font-weight:800;font-size:1.15rem;color:#fff;">{diag_counts['allround']} SV</span>
                        </div>
                        <div style="font-size:0.75rem;color:var(--text-secondary);margin-top:0.35rem;">
                            Vững cả Kỹ thuật lẫn Vấn đáp &rarr; <span style="color:#a7f3d0;">Doanh nghiệp Quốc tế / Onsite</span>
                        </div>
                    </div>

                    <div class="diag-box" onclick="quickFilterDiag('Chưa đạt Chuẩn Kiến thức Cốt lõi')" style="border-top:3px solid #a1a1aa;">
                        <div style="display:flex;justify-content:space-between;align-items:center;">
                            <strong style="color:#e4e4e7;font-size:0.9rem;">⚠️ Cần Phụ Đạo / Trung Gian</strong>
                            <span style="font-weight:800;font-size:1.15rem;color:#fff;">{diag_counts['atrisk'] + diag_counts['mid']} SV</span>
                        </div>
                        <div style="font-size:0.75rem;color:var(--text-secondary);margin-top:0.35rem;">
                            Cần củng cố Java Core &amp; Spring Boot 3 tuần
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 4: DANH BẠ HỌC VIÊN -->
        <div id="tab4" class="tab-pane">
            <div class="filter-bar">
                <input type="text" id="searchInput" class="filter-input" placeholder="🔍 Tìm kiếm sinh viên theo tên..." style="flex:1;min-width:200px;" oninput="applyFilters()">
                <select id="classFilter" class="filter-select" onchange="applyFilters()">
                    <option value="">-- Tất cả Lớp --</option>
                    {''.join([f'<option value="{c}">{c}</option>' for c in classes])}
                </select>
                <select id="tierFilter" class="filter-select" onchange="applyFilters()">
                    <option value="">-- Mức Độ Năng Lực --</option>
                    <option value="3">Mức 3: Làm Chủ Tốt</option>
                    <option value="2">Mức 2: Đạt Chuẩn Doanh Nghiệp</option>
                    <option value="1">Mức 1: Đạt Cơ Bản / Cần Bổ Trợ</option>
                    <option value="0">Mức 0: Chưa Đạt / Vắng Thi</option>
                </select>
                <select id="personaFilter" class="filter-select" onchange="applyFilters()">
                    <option value="">-- Chẩn Đoán Sư Phạm --</option>
                    <option value="Vững Thực hành Kỹ thuật">🔇 Vững Kỹ thuật - Yếu Vấn đáp ({diag_counts['silent']} SV)</option>
                    <option value="Thế mạnh Giao tiếp">🗣️ Thế mạnh KNM - Hạn chế Code ({diag_counts['shifter']} SV)</option>
                    <option value="Đạt Chuẩn Năng lực Toàn diện">🌟 Đạt Chuẩn Toàn diện ({diag_counts['allround']} SV)</option>
                    <option value="Chưa đạt Chuẩn Kiến thức Cốt lõi">🚨 Cần Phụ đạo Kiến thức ({diag_counts['atrisk']} SV)</option>
                    <option value="Đạt Mức Trung bình Cơ bản">🔷 Mức Trung bình Cơ bản ({diag_counts['mid']} SV)</option>
                    <option value="Vắng thi">⚪ Vắng thi / Chưa có bài ({diag_counts['absent']} SV)</option>
                </select>
            </div>

            <div class="card">
                <div class="section-title">
                    <span>📋 Danh Bạ Khảo Thí &amp; Kế Hoạch Can Thiệp Sư Phạm (<span id="recCount">{len(students)}</span> SV)</span>
                </div>
                <div style="overflow-x:auto;">
                    <table class="custom-table" id="studentTable">
                        <thead>
                            <tr>
                                <th>STT</th>
                                <th>Họ và Tên</th>
                                <th>Lớp</th>
                                <th>Final / 10</th>
                                <th>Sản Phẩm</th>
                                <th>Vấn Đáp</th>
                                <th>Thực Hành</th>
                                <th>Trắc Nghiệm</th>
                                <th>KNM</th>
                                <th>Tiếng Anh</th>
                                <th>Mức Độ</th>
                                <th>Chẩn Đoán Sư Phạm</th>
                                <th>Kế Hoạch Can Thiệp</th>
                            </tr>
                        </thead>
                        <tbody id="studentTableBody">
                            {tbody_rows}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- Footer -->
        <div class="report-footer">
            <div>
                <div style="font-weight:600;color:var(--text-secondary);">Báo Cáo ĐGNL Khóa KS24 – Hệ CNTT PTIT Rikkei Education</div>
                <div>Phòng Chuyên Môn &amp; Khảo Thí Đào Tạo | Cập nhật: 02/09/2026</div>
            </div>
            <div style="text-align:right;">
                <div><a href="Executive_Summary_DGNL_Report.html" style="color:var(--color-primary);text-decoration:none;">📑 Về Báo Cáo Tổng Hợp</a></div>
            </div>
        </div>

    </div>

    <script>
    function switchTab(tabId, evt) {{
        document.querySelectorAll('.tab-pane').forEach(el => el.classList.remove('active'));
        document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
        document.getElementById(tabId).classList.add('active');
        if (evt && evt.currentTarget) evt.currentTarget.classList.add('active');
    }}

    function quickFilterDiag(val) {{
        switchTab('tab4');
        document.getElementById('personaFilter').value = val;
        applyFilters();
        document.getElementById('studentTable').scrollIntoView({{ behavior: 'smooth' }});
    }}

    function applyFilters() {{
        const sText = document.getElementById('searchInput').value.toLowerCase().trim();
        const cVal = document.getElementById('classFilter').value;
        const tVal = document.getElementById('tierFilter').value;
        const pVal = document.getElementById('personaFilter').value.toLowerCase();

        const rows = document.querySelectorAll('#studentTableBody tr');
        let count = 0;

        rows.forEach(r => {{
            const name = r.getAttribute('data-name');
            const cName = r.getAttribute('data-class');
            const tier = r.getAttribute('data-tier');
            const persona = r.getAttribute('data-persona').toLowerCase();

            const matchSearch = !sText || name.includes(sText);
            const matchClass = !cVal || cName === cVal;
            const matchTier = tVal === "" || tier === tVal;
            const matchPersona = !pVal || persona.includes(pVal);

            if (matchSearch && matchClass && matchTier && matchPersona) {{
                r.style.display = '';
                count++;
            }} else {{
                r.style.display = 'none';
            }}
        }});

        document.getElementById('recCount').innerText = count;
    }}

    // Charts
    const ctx1 = document.getElementById('branchChart').getContext('2d');
    new Chart(ctx1, {{
        type: 'bar',
        data: {{
            labels: ['📍 Cơ sở Hà Nội (HN-KS24)', '📍 Cơ sở TP.HCM (HCM-KS24)'],
            datasets: [{{
                label: 'Điểm TB Final (Thang 10)',
                data: [{round(sum(s['final_10'] for s in students if 'HN' in s['class'] and not s['is_absent'])/len([s for s in students if 'HN' in s['class'] and not s['is_absent']]), 2)},
                       {round(sum(s['final_10'] for s in students if 'HCM' in s['class'] and not s['is_absent'])/len([s for s in students if 'HCM' in s['class'] and not s['is_absent']]), 2)}],
                backgroundColor: ['rgba(16,185,129,0.7)', 'rgba(59,130,246,0.7)'],
                borderColor: ['#10b981', '#3b82f6'],
                borderWidth: 1.5, borderRadius: 6
            }}]
        }},
        options: {{
            responsive: true, maintainAspectRatio: false,
            plugins: {{ legend: {{ display: false }} }},
            scales: {{
                y: {{ beginAtZero: true, max: 10, grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ color: '#a1a1aa' }} }},
                x: {{ grid: {{ display: false }}, ticks: {{ color: '#a1a1aa' }} }}
            }}
        }}
    }});

    const ctx2 = document.getElementById('tierDistChart').getContext('2d');
    new Chart(ctx2, {{
        type: 'doughnut',
        data: {{
            labels: ['Mức 3 - Làm Chủ Tốt', 'Mức 2 - Đạt Chuẩn Doanh Nghiệp', 'Mức 1 - Cơ Bản', 'Mức 0 - Chưa Đạt / Vắng'],
            datasets: [{{
                data: [
                    {len([s for s in students if s['tier']==3])},
                    {len([s for s in students if s['tier']==2])},
                    {len([s for s in students if s['tier']==1])},
                    {len([s for s in students if s['tier']==0])}
                ],
                backgroundColor: ['#10b981', '#3b82f6', '#f59e0b', '#ef4444'],
                borderWidth: 2, borderColor: '#18181b'
            }}]
        }},
        options: {{
            responsive: true, maintainAspectRatio: false,
            cutout: '68%',
            plugins: {{ legend: {{ labels: {{ color: '#a1a1aa' }} }} }}
        }}
    }});
    </script>
</body>
</html>
"""
    with open("outputs/KS24_DGNL_Report.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated outputs/KS24_DGNL_Report.html successfully!")

if __name__ == "__main__":
    data = load_data()
    build_ks24_report(data)
