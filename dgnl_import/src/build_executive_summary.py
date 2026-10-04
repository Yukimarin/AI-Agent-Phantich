import json
import os
import sys

sys.path.append(os.path.dirname(__file__))
from build_complete_suite import load_data

def build_executive_summary(data):
    ks24 = data["ks24"]
    ks25 = data["ks25"]
    qtkd = data["qtkd"]

    # Compute master KPIs
    total_reg = len(ks24) + len(ks25) + len(qtkd)
    took_ks24 = len([s for s in ks24 if not s["is_absent"]])
    took_ks25 = len([s for s in ks25 if not s["is_absent"]])
    took_qtkd = len([s for s in qtkd if not s["is_absent"]])
    total_took = took_ks24 + took_ks25 + took_qtkd

    pass_ks24 = len([s for s in ks24 if s["is_pass"] and not s["is_absent"]])
    pass_ks25 = len([s for s in ks25 if s["is_pass"] and not s["is_absent"]])
    pass_qtkd = len([s for s in qtkd if s["is_pass"] and not s["is_absent"]])
    total_pass = pass_ks24 + pass_ks25 + pass_qtkd

    ready_ks24 = len([s for s in ks24 if s["tier"] in [2, 3]])
    ready_ks25 = len([s for s in ks25 if s["tier"] in [2, 3]])
    ready_qtkd = len([s for s in qtkd if s["tier"] in [2, 3]])
    total_ready = ready_ks24 + ready_ks25 + ready_qtkd

    avg_ks24 = round(sum(s["final_10"] for s in ks24 if not s["is_absent"]) / took_ks24, 2) if took_ks24 else 0.0
    avg_ks25 = round(sum(s["final_10"] for s in ks25 if not s["is_absent"]) / took_ks25, 2) if took_ks25 else 0.0
    avg_qtkd = round(sum(s["final_10"] for s in qtkd if not s["is_absent"]) / took_qtkd, 2) if took_qtkd else 0.0

    avg_knm_ks24 = round(sum(s["knm"] for s in ks24 if s["knm"] > 0) / len([s for s in ks24 if s["knm"] > 0]), 1) if any(s["knm"] > 0 for s in ks24) else 0.0
    avg_knm_ks25 = round(sum(s["knm"] for s in ks25 if s["knm"] > 0) / len([s for s in ks25 if s["knm"] > 0]), 1) if any(s["knm"] > 0 for s in ks25) else 0.0
    avg_knm_qtkd = round(sum(s["knm"] for s in qtkd if s["knm"] > 0) / len([s for s in qtkd if s["knm"] > 0]), 1) if any(s["knm"] > 0 for s in qtkd) else 0.0

    avg_ta_ks24 = round(sum(s["ta"] for s in ks24 if s["ta"] > 0) / len([s for s in ks24 if s["ta"] > 0]), 1) if any(s["ta"] > 0 for s in ks24) else 0.0
    avg_ta_ks25 = round(sum(s["ta"] for s in ks25 if s["ta"] > 0) / len([s for s in ks25 if s["ta"] > 0]), 1) if any(s["ta"] > 0 for s in ks25) else 0.0
    avg_ta_qtkd = round(sum(s["ta"] for s in qtkd if s["ta"] > 0) / len([s for s in qtkd if s["ta"] > 0]), 1) if any(s["ta"] > 0 for s in qtkd) else 0.0

    # Regional breakdown KS24
    hn_ks24 = [s for s in ks24 if "HN" in s["branch"] or "HN" in s["class"]]
    hcm_ks24 = [s for s in ks24 if "HCM" in s["branch"] or "HCM" in s["class"]]
    hn_ks24_took = len([s for s in hn_ks24 if not s["is_absent"]])
    hcm_ks24_took = len([s for s in hcm_ks24 if not s["is_absent"]])
    hn_ks24_avg = round(sum(s["final_10"] for s in hn_ks24 if not s["is_absent"]) / hn_ks24_took, 2) if hn_ks24_took else 0.0
    hcm_ks24_avg = round(sum(s["final_10"] for s in hcm_ks24 if not s["is_absent"]) / hcm_ks24_took, 2) if hcm_ks24_took else 0.0

    # Regional breakdown KS25
    hn_ks25 = [s for s in ks25 if "HN" in s["branch"] or "HN" in s["class"]]
    hcm_ks25 = [s for s in ks25 if "HCM" in s["branch"] or "HCM" in s["class"]]
    hn_ks25_took = len([s for s in hn_ks25 if not s["is_absent"]])
    hcm_ks25_took = len([s for s in hcm_ks25 if not s["is_absent"]])
    hn_ks25_avg = round(sum(s["final_10"] for s in hn_ks25 if not s["is_absent"]) / hn_ks25_took, 2) if hn_ks25_took else 0.0
    hcm_ks25_avg = round(sum(s["final_10"] for s in hcm_ks25 if not s["is_absent"]) / hcm_ks25_took, 2) if hcm_ks25_took else 0.0

    html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Báo Cáo Tổng Hợp ĐGNL Lần 1 (Toàn hệ thống: KS24, KS25 CNTT & K25 QTKD) | Giám Đốc Đào Tạo</title>
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
            --color-ks24:    #10b981;   /* Emerald - KS24 Java */
            --color-ks25:    #3b82f6;   /* Blue    - KS25 Python */
            --color-qtkd:    #f59e0b;   /* Amber   - K25 QTKD */
            --color-purple:  #8b5cf6;
            --color-danger:  #ef4444;
            --color-success: #10b981;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', sans-serif; }}
        body {{ background: var(--bg-main); color: var(--text-primary); padding-bottom: 80px; }}

        /* Sticky Header */
        .header {{
            background: rgba(18,18,21,0.85);
            backdrop-filter: blur(14px);
            border-bottom: 1px solid var(--border-color);
            position: sticky; top: 0; z-index: 200;
        }}
        .header-inner {{
            max-width: 1440px; margin: 0 auto;
            padding: 1rem 2rem;
            display: flex; justify-content: space-between; align-items: center;
        }}
        .logo-wrap {{ display: flex; align-items: center; gap: 0.75rem; }}
        .logo-badge {{
            background: linear-gradient(135deg, var(--color-ks24), var(--color-ks25), var(--color-qtkd));
            color: #fff; width: 42px; height: 42px; border-radius: 10px;
            display: flex; align-items: center; justify-content: center;
            font-family: 'Outfit', sans-serif; font-weight: 800; font-size: 1.1rem;
            box-shadow: 0 4px 16px rgba(59,130,246,0.3);
        }}
        .logo-text {{ font-family: 'Outfit', sans-serif; font-weight: 700; font-size: 1.1rem; color: #fff; }}
        .header-meta {{ font-size: 0.78rem; color: var(--text-muted); text-align: right; line-height: 1.4; }}

        .container {{ max-width: 1440px; margin: 2rem auto; padding: 0 2rem; }}

        /* Alert Banner */
        .alert-banner {{
            background: linear-gradient(135deg, rgba(16,185,129,0.08), rgba(59,130,246,0.06), rgba(245,158,11,0.06));
            border: 1px solid rgba(59,130,246,0.3);
            border-left: 5px solid var(--color-ks25);
            border-radius: 12px;
            padding: 1.25rem 1.5rem;
            margin-bottom: 2rem;
            display: flex; gap: 1rem; align-items: flex-start;
        }}
        .alert-title {{ font-size: 1.05rem; font-weight: 700; color: #93c5fd; margin-bottom: 0.35rem; }}
        .alert-body {{ font-size: 0.88rem; color: var(--text-secondary); line-height: 1.6; }}

        /* Master KPI Grid */
        .kpi-grid {{
            display: grid; grid-template-columns: repeat(6, 1fr); gap: 1rem; margin-bottom: 2.25rem;
        }}
        .kpi-card {{
            background: var(--bg-card); border: 1px solid var(--border-color);
            border-radius: 12px; padding: 1.25rem; position: relative; overflow: hidden;
        }}
        .kpi-card::before {{
            content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
            background: linear-gradient(90deg, var(--accent-l), var(--accent-r));
        }}
        .kpi-card.blue   {{ --accent-l: #3b82f6; --accent-r: #60a5fa; }}
        .kpi-card.green  {{ --accent-l: #10b981; --accent-r: #34d399; }}
        .kpi-card.gold   {{ --accent-l: #f59e0b; --accent-r: #fbbf24; }}
        .kpi-card.purple {{ --accent-l: #8b5cf6; --accent-r: #a78bfa; }}
        .kpi-card.red    {{ --accent-l: #ef4444; --accent-r: #f87171; }}
        .kpi-card.cyan   {{ --accent-l: #06b6d4; --accent-r: #22d3ee; }}

        .kpi-label {{ font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.5px; color: var(--text-muted); margin-bottom: 0.4rem; }}
        .kpi-value {{ font-family: 'Outfit', sans-serif; font-size: 1.85rem; font-weight: 800; color: #fff; }}
        .kpi-sub   {{ font-size: 0.73rem; color: var(--text-secondary); margin-top: 0.25rem; }}

        /* Section Title */
        .section-title {{
            font-family: 'Outfit', sans-serif; font-size: 1.2rem; font-weight: 700;
            color: #fff; border-left: 4px solid var(--color-ks25); padding-left: 0.75rem;
            margin-bottom: 1.25rem; display: flex; justify-content: space-between; align-items: center;
        }}

        /* 3-Cohort Grid */
        .cohort-grid {{
            display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.25rem; margin-bottom: 2.5rem;
        }}
        .cohort-card {{
            background: var(--bg-card); border: 1px solid var(--border-color);
            border-radius: 12px; padding: 1.5rem; display: flex; flex-direction: column;
        }}
        .cohort-card.ks24 {{ border-top: 3px solid var(--color-ks24); }}
        .cohort-card.ks25 {{ border-top: 3px solid var(--color-ks25); }}
        .cohort-card.qtkd {{ border-top: 3px solid var(--color-qtkd); }}

        .cohort-badge {{
            display: inline-block; padding: 0.3rem 0.8rem; border-radius: 999px;
            font-size: 0.8rem; font-weight: 700; margin-bottom: 0.85rem;
        }}
        .cohort-badge.ks24 {{ background: rgba(16,185,129,0.12); color: var(--color-ks24); border: 1px solid rgba(16,185,129,0.25); }}
        .cohort-badge.ks25 {{ background: rgba(59,130,246,0.12); color: var(--color-ks25); border: 1px solid rgba(59,130,246,0.25); }}
        .cohort-badge.qtkd {{ background: rgba(245,158,11,0.12); color: var(--color-qtkd); border: 1px solid rgba(245,158,11,0.25); }}

        .cohort-stats {{
            display: grid; grid-template-columns: 1fr 1fr; gap: 0.6rem; margin: 1rem 0;
        }}
        .cohort-stat-box {{
            background: rgba(255,255,255,0.025); border: 1px solid var(--border-color);
            border-radius: 8px; padding: 0.75rem 0.85rem;
        }}
        .cohort-stat-label {{ font-size: 0.7rem; color: var(--text-muted); text-transform: uppercase; }}
        .cohort-stat-val {{ font-family: 'Outfit', sans-serif; font-size: 1.35rem; font-weight: 700; margin-top: 0.15rem; }}

        .cohort-sub-info {{ font-size: 0.8rem; color: var(--text-secondary); line-height: 1.5; margin-top: auto; padding-top: 0.75rem; border-top: 1px solid var(--border-color); }}

        /* Diagnostic Matrix Quadrants */
        .diag-grid {{
            display: grid; grid-template-columns: repeat(2, 1fr); gap: 1.25rem; margin-bottom: 2.5rem;
        }}
        .diag-card {{
            background: var(--bg-card); border: 1px solid var(--border-color);
            border-radius: 12px; padding: 1.5rem;
        }}
        .diag-card-header {{
            display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;
        }}
        .diag-card-title {{ font-size: 0.95rem; font-weight: 700; color: #fff; }}
        .diag-count {{ font-family: 'Outfit', sans-serif; font-size: 1.25rem; font-weight: 800; }}

        /* Matrix Table */
        .custom-table {{ width: 100%; border-collapse: collapse; font-size: 0.85rem; }}
        .custom-table th, .custom-table td {{ padding: 0.75rem 1rem; border: 1px solid var(--border-color); text-align: center; }}
        .custom-table th {{ background: rgba(255,255,255,0.03); color: var(--text-secondary); font-weight: 600; }}
        .custom-table td.left {{ text-align: left; }}

        /* Action list */
        .action-card {{
            background: var(--bg-card); border: 1px solid var(--border-color);
            border-radius: 12px; padding: 1.5rem; margin-bottom: 2rem;
        }}
        .action-item {{
            display: flex; gap: 1rem; padding: 1rem 0; border-bottom: 1px solid var(--border-color);
            font-size: 0.85rem; line-height: 1.6; color: var(--text-secondary);
        }}
        .action-item:last-child {{ border-bottom: none; }}
        .action-num {{
            background: var(--color-ks25); color: #fff; width: 26px; height: 26px;
            border-radius: 50%; display: flex; align-items: center; justify-content: center;
            font-weight: 700; flex-shrink: 0; margin-top: 0.15rem; font-size: 0.8rem;
        }}
        .action-num.urgent {{ background: var(--color-danger); }}
        .action-num.warning {{ background: var(--color-qtkd); color: #000; }}

        /* Footer */
        .report-footer {{
            margin-top: 3.5rem; border-top: 1px solid var(--border-color);
            padding-top: 1.5rem; display: flex; justify-content: space-between; align-items: center;
            font-size: 0.8rem; color: var(--text-muted);
        }}
    </style>
</head>
<body>

    <!-- ── HEADER ───────────────────────────────────────────────────────────── -->
    <header class="header">
        <div class="header-inner">
            <div class="logo-wrap">
                <div class="logo-badge">RKE</div>
                <div>
                    <div class="logo-text">Báo Cáo Tổng Hợp ĐGNL Lần 1 (Toàn Khóa Đào Tạo)</div>
                    <div style="font-size:0.75rem;color:var(--text-muted);">Khối Công Nghệ Thông Tin (KS24, KS25) &amp; Khối Quản Trị Kinh Doanh (K25)</div>
                </div>
            </div>
            <div class="header-meta">
                Dành cho Giám Đốc Đào Tạo &amp; Ban Quản Trị Học Thuật<br>
                Cập nhật: 02/09/2026 (Dữ liệu sau Khảo thí Bổ sung)
            </div>
        </div>
    </header>

    <div class="container">

        <!-- ── ALERT SUMMARY ────────────────────────────────────────────────── -->
        <div class="alert-banner">
            <div style="font-size:1.8rem;flex-shrink:0;">📑</div>
            <div>
                <div class="alert-title">Thông Điệp Học Thuật Cốt Lõi Dành Cho Ban Giám Đốc Đào Tạo</div>
                <div class="alert-body">
                    Hệ thống khảo thí ĐGNL Lần 1 đã hoàn tất thu thập và đối soát dữ liệu trên toàn bộ <strong>{total_reg} sinh viên</strong> thuộc 3 khối đào tạo.
                    Tổng số sinh viên tham gia khảo thí thực tế đạt <strong>{total_took}/{total_reg} sinh viên ({round(total_took/total_reg*100, 1)}%)</strong>.
                    Phân tích đối soát cho thấy: <strong>Chất lượng đào tạo có sự phân hóa sâu sắc theo từng giai đoạn học tập</strong>. Việc đánh giá năng lực ra trường cần tích hợp đồng thời <strong>3 Trụ Cột: Năng lực Chuyên môn – Năng lực Vấn đáp &amp; Kỹ năng Mềm – Năng lực Ngoại ngữ Quốc tế</strong> để xây dựng kế hoạch can thiệp sư phạm chính xác cho từng đối tượng người học.
                </div>
            </div>
        </div>

        <!-- ── MASTER KPI STRIP ─────────────────────────────────────────────── -->
        <div class="kpi-grid">
            <div class="kpi-card blue">
                <div class="kpi-label">Tổng Sĩ Số Đăng Ký</div>
                <div class="kpi-value">{total_reg}</div>
                <div class="kpi-sub">KS24: {len(ks24)} • KS25: {len(ks25)} • QTKD: {len(qtkd)}</div>
            </div>
            <div class="kpi-card green">
                <div class="kpi-label">Dự Thi Thực Tế</div>
                <div class="kpi-value">{total_took}</div>
                <div class="kpi-sub">Tỷ lệ tham gia: {round(total_took/total_reg*100, 1)}%</div>
            </div>
            <div class="kpi-card gold">
                <div class="kpi-label">Đạt Chuẩn Chuyên Môn</div>
                <div class="kpi-value">{total_pass}</div>
                <div class="kpi-sub">Tỷ lệ Đạt: {round(total_pass/total_reg*100, 1)}%</div>
            </div>
            <div class="kpi-card purple">
                <div class="kpi-label">Chuẩn Đầu Ra Toàn Diện</div>
                <div class="kpi-value">{total_ready}</div>
                <div class="kpi-sub">Mức 2 &amp; Mức 3 ({round(total_ready/total_reg*100, 1)}%)</div>
            </div>
            <div class="kpi-card cyan">
                <div class="kpi-label">Điểm TB Kỹ Năng Mềm</div>
                <div class="kpi-value">{round((avg_knm_ks24*len(ks24) + avg_knm_ks25*len(ks25) + avg_knm_qtkd*len(qtkd))/total_reg, 1)}</div>
                <div class="kpi-sub">Thang điểm 100</div>
            </div>
            <div class="kpi-card blue">
                <div class="kpi-label">Điểm TB Tiếng Anh</div>
                <div class="kpi-value">{round((avg_ta_ks24*len(ks24) + avg_ta_ks25*len(ks25) + avg_ta_qtkd*len(qtkd))/total_reg, 0):.0f}</div>
                <div class="kpi-sub">Quy đổi chuẩn TOEIC / 990</div>
            </div>
        </div>

        <!-- ── 3-COHORT MASTER COMPARATIVE SECTION ──────────────────────────── -->
        <div class="section-title">
            <span>🏛️ Đối Chiếu Tổng Quan Chỉ Số Chất Lượng 3 Khối Đào Tạo</span>
        </div>

        <div class="cohort-grid">
            <!-- COHORT 1: KS24 CNTT -->
            <div class="cohort-card ks24">
                <div class="cohort-badge ks24">☕ Khóa KS24 CNTT – Java / Spring Boot (Cuối Kỳ III)</div>
                <div style="font-size:0.83rem;color:var(--text-secondary);line-height:1.5;">
                    Kỳ đánh giá nghiệm thu cuối kỳ III nhằm phân luồng chuẩn bị Đồ án Tốt nghiệp và Thực tập Doanh nghiệp.
                </div>
                <div class="cohort-stats">
                    <div class="cohort-stat-box">
                        <div class="cohort-stat-label">Sĩ số / Dự thi</div>
                        <div class="cohort-stat-val" style="color:var(--color-ks24);">{len(ks24)} / {took_ks24}</div>
                    </div>
                    <div class="cohort-stat-box">
                        <div class="cohort-stat-label">Điểm TB Final</div>
                        <div class="cohort-stat-val" style="color:var(--color-ks24);">{avg_ks24}/10</div>
                    </div>
                    <div class="cohort-stat-box">
                        <div class="cohort-stat-label">Đạt Chuẩn (Mức 2+3)</div>
                        <div class="cohort-stat-val" style="color:var(--color-ks24);">{ready_ks24} SV ({round(ready_ks24/len(ks24)*100, 1)}%)</div>
                    </div>
                    <div class="cohort-stat-box">
                        <div class="cohort-stat-label">Điểm TB KNM / TA</div>
                        <div class="cohort-stat-val" style="font-size:1.1rem;color:#34d399;">{avg_knm_ks24}đ / {avg_ta_ks24:.0f}</div>
                    </div>
                </div>
                <div class="cohort-sub-info">
                    📍 <strong>Cơ sở Hà Nội:</strong> {hn_ks24_took}/{len(hn_ks24)} SV (TB: {hn_ks24_avg}/10)<br>
                    📍 <strong>Cơ sở TP.HCM:</strong> {hcm_ks24_took}/{len(hcm_ks24)} SV (TB: {hcm_ks24_avg}/10)<br>
                    <span style="color:#f87171;font-weight:600;">⚠ Vấn đề nổi cộm:</span> 29 SV làm sản phẩm/code giỏi nhưng vấn đáp &lt; 50đ.
                </div>
                <div style="margin-top:1rem;">
                    <a href="KS24_DGNL_Report.html" style="display:block;text-align:center;padding:0.5rem;background:rgba(16,185,129,0.15);color:var(--color-ks24);border:1px solid rgba(16,185,129,0.3);border-radius:6px;font-size:0.82rem;font-weight:600;text-decoration:none;">Xem Báo Cáo Chi Tiết KS24 →</a>
                </div>
            </div>

            <!-- COHORT 2: KS25 CNTT -->
            <div class="cohort-card ks25">
                <div class="cohort-badge ks25">🐍 Khóa KS25 CNTT – FastAPI / Python (Giữa Kỳ II)</div>
                <div style="font-size:0.83rem;color:var(--text-secondary);line-height:1.5;">
                    Kỳ đánh giá giữa kỳ II nhằm kiểm tra năng lực lập trình hướng đối tượng và kỹ năng xây dựng API backend căn bản.
                </div>
                <div class="cohort-stats">
                    <div class="cohort-stat-box">
                        <div class="cohort-stat-label">Sĩ số / Dự thi</div>
                        <div class="cohort-stat-val" style="color:var(--color-ks25);">{len(ks25)} / {took_ks25}</div>
                    </div>
                    <div class="cohort-stat-box">
                        <div class="cohort-stat-label">Điểm TB Final</div>
                        <div class="cohort-stat-val" style="color:var(--color-ks25);">{avg_ks25}/10</div>
                    </div>
                    <div class="cohort-stat-box">
                        <div class="cohort-stat-label">Đạt Chuẩn (Mức 2+3)</div>
                        <div class="cohort-stat-val" style="color:var(--color-ks25);">{ready_ks25} SV ({round(ready_ks25/len(ks25)*100, 1)}%)</div>
                    </div>
                    <div class="cohort-stat-box">
                        <div class="cohort-stat-label">Điểm TB KNM / TA</div>
                        <div class="cohort-stat-val" style="font-size:1.1rem;color:#60a5fa;">{avg_knm_ks25}đ / {avg_ta_ks25:.0f}</div>
                    </div>
                </div>
                <div class="cohort-sub-info">
                    📍 <strong>Cơ sở Hà Nội:</strong> {hn_ks25_took}/{len(hn_ks25)} SV (TB: {hn_ks25_avg}/10)<br>
                    📍 <strong>Cơ sở TP.HCM:</strong> {hcm_ks25_took}/{len(hcm_ks25)} SV (TB: {hcm_ks25_avg}/10)<br>
                    <span style="color:#f87171;font-weight:600;">⚠ Vấn đề nổi cộm:</span> 151 SV trắc nghiệm cao (&ge;65đ) nhưng thực hành viết code &lt; 50đ.
                </div>
                <div style="margin-top:1rem;">
                    <a href="KS25_DGNL_Report.html" style="display:block;text-align:center;padding:0.5rem;background:rgba(59,130,246,0.15);color:var(--color-ks25);border:1px solid rgba(59,130,246,0.3);border-radius:6px;font-size:0.82rem;font-weight:600;text-decoration:none;">Xem Báo Cáo Chi Tiết KS25 →</a>
                </div>
            </div>

            <!-- COHORT 3: K25 QTKD -->
            <div class="cohort-card qtkd">
                <div class="cohort-badge qtkd">💼 Khóa K25 QTKD – Quản Trị Kinh Doanh (Giữa Kỳ II)</div>
                <div style="font-size:0.83rem;color:var(--text-secondary);line-height:1.5;">
                    Kỳ đánh giá nghiệm thu dự án kinh doanh thực chiến và bản lĩnh thuyết trình bảo vệ trước Hội đồng giám khảo.
                </div>
                <div class="cohort-stats">
                    <div class="cohort-stat-box">
                        <div class="cohort-stat-label">Sĩ số / Dự thi</div>
                        <div class="cohort-stat-val" style="color:var(--color-qtkd);">{len(qtkd)} / {took_qtkd}</div>
                    </div>
                    <div class="cohort-stat-box">
                        <div class="cohort-stat-label">Điểm TB Final</div>
                        <div class="cohort-stat-val" style="color:var(--color-qtkd);">{avg_qtkd}/10</div>
                    </div>
                    <div class="cohort-stat-box">
                        <div class="cohort-stat-label">Đạt Chuẩn (Mức 2+3)</div>
                        <div class="cohort-stat-val" style="color:var(--color-qtkd);">{ready_qtkd} SV ({round(ready_qtkd/len(qtkd)*100, 1)}%)</div>
                    </div>
                    <div class="cohort-stat-box">
                        <div class="cohort-stat-label">Điểm TB KNM / TA</div>
                        <div class="cohort-stat-val" style="font-size:1.1rem;color:#fbbf24;">{avg_knm_qtkd}đ / {avg_ta_qtkd:.0f}</div>
                    </div>
                </div>
                <div class="cohort-sub-info">
                    👥 <strong>Hình thức thi:</strong> 11 Nhóm dự án kinh doanh (Tỷ lệ đỗ: {round(pass_qtkd/len(qtkd)*100, 1)}%)<br>
                    🌟 <strong>Thế mạnh:</strong> Kỹ năng mềm TB đạt {avg_knm_qtkd}/100, thuyết trình tự tin.<br>
                    <span style="color:#f87171;font-weight:600;">⚠ Vấn đề nổi cộm:</span> 40 SV giỏi chuyên môn nhưng Tiếng Anh sơ cấp (&lt;350đ).
                </div>
                <div style="margin-top:1rem;">
                    <a href="QTKD_DGNL_Report.html" style="display:block;text-align:center;padding:0.5rem;background:rgba(245,158,11,0.15);color:var(--color-qtkd);border:1px solid rgba(245,158,11,0.3);border-radius:6px;font-size:0.82rem;font-weight:600;text-decoration:none;">Xem Báo Cáo Chi Tiết QTKD →</a>
                </div>
            </div>
        </div>

        <!-- ── ACADEMIC COMPARISON CHARTS ───────────────────────────────────── -->
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;margin-bottom:2.5rem;">
            <div style="background:var(--bg-card);border:1px solid var(--border-color);border-radius:12px;padding:1.5rem;">
                <div style="font-family:'Outfit',sans-serif;font-size:0.95rem;font-weight:700;color:#fff;margin-bottom:1rem;">
                    📈 So Sánh Điểm Trung Bình Chuyên Môn &amp; Kỹ Năng Mềm 3 Khối
                </div>
                <div style="height:260px;position:relative;">
                    <canvas id="mainCompChart"></canvas>
                </div>
            </div>

            <div style="background:var(--bg-card);border:1px solid var(--border-color);border-radius:12px;padding:1.5rem;">
                <div style="font-family:'Outfit',sans-serif;font-size:0.95rem;font-weight:700;color:#fff;margin-bottom:1rem;">
                    🎯 Tỷ Lệ Phân Bố Mức Độ Năng Lực Toàn Hệ Thống ({total_reg} Sinh Viên)
                </div>
                <div style="display:flex;align-items:center;gap:1.5rem;height:260px;">
                    <div style="width:200px;height:200px;position:relative;flex-shrink:0;">
                        <canvas id="readinessDoughnut"></canvas>
                    </div>
                    <div style="font-size:0.83rem;color:var(--text-secondary);display:flex;flex-direction:column;gap:0.6rem;">
                        <div><span style="color:#ef4444;font-weight:700;">● Mức 0 - Chưa Đạt:</span> {len([s for s in ks24+ks25+qtkd if s['tier']==0])} SV ({round(len([s for s in ks24+ks25+qtkd if s['tier']==0])/total_reg*100, 1)}%)</div>
                        <div><span style="color:#f59e0b;font-weight:700;">● Mức 1 - Cơ Bản:</span> {len([s for s in ks24+ks25+qtkd if s['tier']==1])} SV ({round(len([s for s in ks24+ks25+qtkd if s['tier']==1])/total_reg*100, 1)}%)</div>
                        <div><span style="color:#3b82f6;font-weight:700;">● Mức 2 - Chuẩn Doanh Nghiệp:</span> {len([s for s in ks24+ks25+qtkd if s['tier']==2])} SV ({round(len([s for s in ks24+ks25+qtkd if s['tier']==2])/total_reg*100, 1)}%)</div>
                        <div><span style="color:#10b981;font-weight:700;">● Mức 3 - Làm Chủ Tốt:</span> {len([s for s in ks24+ks25+qtkd if s['tier']==3])} SV ({round(len([s for s in ks24+ks25+qtkd if s['tier']==3])/total_reg*100, 1)}%)</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- ── CROSS-FACULTY COMPARISON TABLE ───────────────────────────────── -->
        <div class="section-title">🔥 Bảng Ma Trận Đối Chiếu Học Thuật Giữa 3 Khối Đào Tạo</div>
        <div style="background:var(--bg-card);border:1px solid var(--border-color);border-radius:12px;padding:1.5rem;margin-bottom:2.5rem;overflow-x:auto;">
            <table class="custom-table">
                <thead>
                    <tr>
                        <th style="text-align:left;">Chỉ Số Khảo Thí &amp; Đào Tạo</th>
                        <th style="color:var(--color-ks24);">☕ KS24 CNTT</th>
                        <th style="color:var(--color-ks25);">🐍 KS25 CNTT</th>
                        <th style="color:var(--color-qtkd);">💼 K25 QTKD</th>
                        <th style="text-align:left;">Nhận Định Sư Phạm &amp; Hướng Xử Lý</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td class="left" style="color:#fff;font-weight:600;">Sĩ số đăng ký / Dự thi</td>
                        <td>{len(ks24)} / {took_ks24}</td>
                        <td>{len(ks25)} / {took_ks25}</td>
                        <td>{len(qtkd)} / {took_qtkd}</td>
                        <td class="left">Quy mô KS25 lớn nhất; Khối QTKD có tỷ lệ dự thi cao nhất ({round(took_qtkd/len(qtkd)*100, 1)}%)</td>
                    </tr>
                    <tr>
                        <td class="left" style="color:#fff;font-weight:600;">Điểm TB Chuyên môn (Thang 10)</td>
                        <td style="color:#34d399;font-weight:700;">{avg_ks24}/10</td>
                        <td style="color:#f87171;font-weight:700;">{avg_ks25}/10</td>
                        <td style="color:#fbbf24;font-weight:700;">{avg_qtkd}/10</td>
                        <td class="left">KS25 phản ánh giai đoạn giữa kỳ II; KS24 và QTKD có nền tảng hoàn thiện hơn</td>
                    </tr>
                    <tr>
                        <td class="left" style="color:#fff;font-weight:600;">Điểm TB Kỹ năng Mềm (Thang 100)</td>
                        <td style="color:#34d399;font-weight:700;">{avg_knm_ks24}</td>
                        <td style="color:#60a5fa;font-weight:700;">{avg_knm_ks25}</td>
                        <td style="color:#fbbf24;font-weight:700;">{avg_knm_qtkd}</td>
                        <td class="left">Khối QTKD vượt trội về thuyết trình nhóm; Khối CNTT cần rèn luyện diễn đạt</td>
                    </tr>
                    <tr>
                        <td class="left" style="color:#fff;font-weight:600;">Điểm TB Tiếng Anh (TOEIC / 990)</td>
                        <td>{avg_ta_ks24:.0f}</td>
                        <td>{avg_ta_ks25:.0f}</td>
                        <td>{avg_ta_qtkd:.0f}</td>
                        <td class="left">Cả 3 khối đều gặp khoảng trống năng lực ngoại ngữ so với chuẩn đầu ra quốc tế</td>
                    </tr>
                    <tr>
                        <td class="left" style="color:#fff;font-weight:600;">Tỷ lệ Đạt Chuẩn Đầu ra (Mức 2+3)</td>
                        <td style="color:#34d399;font-weight:700;">{round(ready_ks24/len(ks24)*100, 1)}%</td>
                        <td style="color:#f87171;font-weight:700;">{round(ready_ks25/len(ks25)*100, 1)}%</td>
                        <td style="color:#fbbf24;font-weight:700;">{round(ready_qtkd/len(qtkd)*100, 1)}%</td>
                        <td class="left">Khối QTKD và KS24 đạt tỷ lệ sẵn sàng cao; KS25 cần phân luồng tăng cường thực hành</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- ── OBJECTIVE DIAGNOSTIC SECTION ────────────────────────────────── -->
        <div class="section-title">
            <span>🎯 Chẩn Đoán Khách Quan: Nền Tảng Kỹ Thuật vs Kỹ Năng Phỏng Vấn / Diễn Đạt</span>
        </div>

        <div class="diag-grid">
            <!-- DIAG 1 -->
            <div class="diag-card" style="border-top:3px solid #ef4444;">
                <div class="diag-card-header">
                    <span class="diag-card-title" style="color:#f87171;">🔇 Nhóm Năng Lực Kỹ Thuật Vững - Hạn Chế Diễn Đạt Vấn Đáp (29 SV KS24)</span>
                    <span class="diag-count" style="color:#f87171;">14.9%</span>
                </div>
                <div style="font-size:0.83rem;color:var(--text-secondary);line-height:1.6;margin-bottom:0.75rem;">
                    <strong>Bản chất học thuật:</strong> Sinh viên có năng lực lập trình và làm sản phẩm thực tế rất tốt (70 - 100đ), nhưng điểm Vấn đáp trực tiếp dưới 45đ do rào cản tâm lý phòng thi và thiếu kỹ năng cấu trúc câu trả lời (phương pháp STAR).
                </div>
                <div style="background:rgba(239,68,68,0.08);border:1px solid rgba(239,68,68,0.25);border-radius:6px;padding:0.6rem 0.85rem;font-size:0.8rem;color:#fca5a5;">
                    👉 <strong>Giải pháp Sư phạm: KHÔNG DẠY LẠI CODE</strong>. Bắt buộc tham gia <em>Phòng Phỏng vấn Chuyên môn Giả định (Simulated Technical Interview)</em> 1-on-1 với Tech Lead doanh nghiệp.
                </div>
            </div>

            <!-- DIAG 2 -->
            <div class="diag-card" style="border-top:3px solid #fbbf24;">
                <div class="diag-card-header">
                    <span class="diag-card-title" style="color:#fbbf24;">🗣️ Nhóm Thế Mạnh Giao Tiếp - Hạn Chế Lập Trình Sâu (20 SV KS24 &amp; 12 SV KS25)</span>
                    <span class="diag-count" style="color:#fbbf24;">~10%</span>
                </div>
                <div style="font-size:0.83rem;color:var(--text-secondary);line-height:1.6;margin-bottom:0.75rem;">
                    <strong>Bản chất học thuật:</strong> Sinh viên có kỹ năng mềm và giao tiếp xuất sắc (&ge; 75 - 100đ), nhưng năng lực viết code chi tiết bị hổng (&lt; 50đ). Dễ vượt qua vòng sơ loại HR nhưng sẽ không đáp ứng yêu cầu Live-Coding của lập trình viên thuần túy.
                </div>
                <div style="background:rgba(245,158,11,0.08);border:1px solid rgba(245,158,11,0.25);border-radius:6px;padding:0.6rem 0.85rem;font-size:0.8rem;color:#fde68a;">
                    👉 <strong>Giải pháp Sư phạm: TƯ VẤN PHÂN LUỒNG NGHỀ NGHIỆP</strong> sang các vị trí: <em>IT Business Analyst (BA), Software QA/QC Tester, IT Project Coordinator, IT Sales</em>.
                </div>
            </div>

            <!-- DIAG 3 -->
            <div class="diag-card" style="border-top:3px solid #ef4444;">
                <div class="diag-card-header">
                    <span class="diag-card-title" style="color:#f87171;">🚨 Nhóm Nắm Vững Lý Thuyết - Hạn Chế Vận Dụng Thực Hành (151 SV KS25)</span>
                    <span class="diag-count" style="color:#f87171;">51.5%</span>
                </div>
                <div style="font-size:0.83rem;color:var(--text-secondary);line-height:1.6;margin-bottom:0.75rem;">
                    <strong>Bản chất học thuật:</strong> Điểm trắc nghiệm lý thuyết đạt rất cao (&ge; 65 - 90đ) nhưng điểm thực hành viết code trên máy dưới 50đ. Học viên học vẹt định nghĩa nhưng chưa hình thành phản xạ tự xây dựng API 4 lớp từ đầu.
                </div>
                <div style="background:rgba(239,68,68,0.08);border:1px solid rgba(239,68,68,0.25);border-radius:6px;padding:0.6rem 0.85rem;font-size:0.8rem;color:#fca5a5;">
                    👉 <strong>Giải pháp Sư phạm: PHÂN TẦNG KỲ III</strong>. Bắt buộc tham gia <em>Khóa Học Bổ trợ Tăng cường FastAPI Live-Coding 2 tuần</em> trước khi học các môn DSA/AI.
                </div>
            </div>

            <!-- DIAG 4 -->
            <div class="diag-card" style="border-top:3px solid #f59e0b;">
                <div class="diag-card-header">
                    <span class="diag-card-title" style="color:#fbbf24;">💼 Nhóm Vững Chuyên Môn QTKD - Khoảng Trống Ngoại Ngữ (40 SV QTKD)</span>
                    <span class="diag-count" style="color:#fbbf24;">38.1%</span>
                </div>
                <div style="font-size:0.83rem;color:var(--text-secondary);line-height:1.6;margin-bottom:0.75rem;">
                    <strong>Bản chất học thuật:</strong> Sinh viên đạt điểm chuyên môn và thuyết trình rất giỏi (&ge; 70đ), nhưng điểm Tiếng Anh chỉ đạt mức sơ cấp (&lt; 350đ TOEIC).
                </div>
                <div style="background:rgba(245,158,11,0.08);border:1px solid rgba(245,158,11,0.25);border-radius:6px;padding:0.6rem 0.85rem;font-size:0.8rem;color:#fde68a;">
                    👉 <strong>Giải pháp Sư phạm:</strong> Triển khai <em>Khóa Học Bổ trợ Tiếng Anh Thương Mại (Business English Workshop)</em> bắt buộc từ Kỳ III để nâng chuẩn TOEIC &ge; 450+.
                </div>
            </div>
        </div>

        <!-- ── STRATEGIC RECOMMENDATIONS ────────────────────────────────────── -->
        <div class="section-title">
            <span>📋 Kế Hoạch Quản Lý Đào Tạo &amp; Can Thiệp Sư Phạm Cho Giám Đốc Đào Tạo</span>
        </div>

        <div class="action-card">
            <div class="action-item">
                <div class="action-num urgent">1</div>
                <div>
                    <strong style="color:#f87171;">Thành lập Phòng Phỏng vấn Chuyên môn Giả định (Simulated Technical Interview Lab) cho KS24:</strong><br>
                    Tổ chức cho 29 sinh viên vững kỹ thuật nhưng hạn chế vấn đáp tham gia 3 buổi phỏng vấn 1-1 với Chuyên gia doanh nghiệp (quay video phân tích ngôn ngữ cơ thể, rèn luyện cấu trúc trả lời STAR) nhằm đảm bảo tỷ lệ vượt qua vòng phỏng vấn tuyển dụng đạt &gt; 85%.
                </div>
            </div>

            <div class="action-item">
                <div class="action-num urgent">2</div>
                <div>
                    <strong style="color:#f87171;">Phân tầng Học thuật và Tăng cường Live-Coding cho Khóa KS25 ngay trong Kỳ III:</strong><br>
                    Tách riêng 151 sinh viên bị hổng thực hành để tổ chức Khóa Học Bổ trợ Tăng cường FastAPI trong 2 tuần đầu kỳ III. Cung cấp sẵn Project Skeleton để giảm áp lực dựng khung, tập trung rèn luyện tầng Service và Router logic.
                </div>
            </div>

            <div class="action-item">
                <div class="action-num warning">3</div>
                <div>
                    <strong style="color:#fbbf24;">Tư vấn Phân luồng Nghề nghiệp Sớm (Career Pivoting):</strong><br>
                    Chủ động tư vấn cho nhóm sinh viên có kỹ năng mềm tốt nhưng không có thế mạnh lập trình sâu chuyển hướng học chuyên sâu sang <em>Phân tích Nghiệp vụ (BA), Kiểm thử Phần mềm (QA/QC), Điều phối Dự án (Scrum Master)</em>.
                </div>
            </div>

            <div class="action-item">
                <div class="action-num">4</div>
                <div>
                    <strong style="color:#93c5fd;">Triển khai Chuẩn Hóa Phương Pháp "Live-Code Review &amp; Pitching" Hàng Tuần:</strong><br>
                    Dành 30% thời lượng mỗi buổi Lab thực hành để sinh viên thuyết trình giải pháp code trong 3 phút, triệt tiêu hoàn toàn hiện tượng sinh viên khép kín và tăng cường phản xạ giao tiếp chuyên môn.
                </div>
            </div>
        </div>

        <!-- ── FOOTER ───────────────────────────────────────────────────────── -->
        <div class="report-footer">
            <div>
                <div style="font-weight:600;color:var(--text-secondary);">Báo Cáo Tổng Hợp ĐGNL Lần 1 – Hệ Thống Đào Tạo PTIT Rikkei Education</div>
                <div>Phòng Chuyên Môn &amp; Khảo Thí Đào Tạo | Ban Hành: 02/09/2026</div>
            </div>
            <div style="text-align:right;">
                <div>Xem chi tiết từng khối:</div>
                <div style="display:flex;gap:0.75rem;margin-top:0.25rem;">
                    <a href="KS24_DGNL_Report.html" style="color:var(--color-ks24);text-decoration:none;">☕ Báo Cáo KS24</a> |
                    <a href="KS25_DGNL_Report.html" style="color:var(--color-ks25);text-decoration:none;">🐍 Báo Cáo KS25</a> |
                    <a href="QTKD_DGNL_Report.html" style="color:var(--color-qtkd);text-decoration:none;">💼 Báo Cáo QTKD</a>
                </div>
            </div>
        </div>

    </div>

    <script>
    // Master Comparison Bar Chart
    const ctx1 = document.getElementById('mainCompChart').getContext('2d');
    new Chart(ctx1, {{
        type: 'bar',
        data: {{
            labels: ['☕ KS24 CNTT', '🐍 KS25 CNTT', '💼 K25 QTKD'],
            datasets: [
                {{
                    label: 'Điểm TB Chuyên Môn (Thang 10)',
                    data: [{avg_ks24}, {avg_ks25}, {avg_qtkd}],
                    backgroundColor: ['rgba(16,185,129,0.7)', 'rgba(59,130,246,0.7)', 'rgba(245,158,11,0.7)'],
                    borderColor: ['#10b981', '#3b82f6', '#f59e0b'],
                    borderWidth: 1.5, borderRadius: 6
                }},
                {{
                    label: 'Điểm TB Kỹ Năng Mềm (Quy đổi / 10)',
                    data: [{round(avg_knm_ks24/10.0, 2)}, {round(avg_knm_ks25/10.0, 2)}, {round(avg_knm_qtkd/10.0, 2)}],
                    backgroundColor: 'rgba(139,92,246,0.6)',
                    borderColor: '#8b5cf6',
                    borderWidth: 1.5, borderRadius: 6
                }}
            ]
        }},
        options: {{
            responsive: true, maintainAspectRatio: false,
            plugins: {{ legend: {{ labels: {{ color: '#a1a1aa' }} }} }},
            scales: {{
                y: {{ beginAtZero: true, max: 10, grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ color: '#a1a1aa' }} }},
                x: {{ grid: {{ display: false }}, ticks: {{ color: '#a1a1aa' }} }}
            }}
        }}
    }});

    // Master Readiness Doughnut
    const ctx2 = document.getElementById('readinessDoughnut').getContext('2d');
    new Chart(ctx2, {{
        type: 'doughnut',
        data: {{
            labels: ['Mức 0 - Chưa Đạt', 'Mức 1 - Cơ Bản', 'Mức 2 - Chuẩn Doanh Nghiệp', 'Mức 3 - Làm Chủ Tốt'],
            datasets: [{{
                data: [
                    {len([s for s in ks24+ks25+qtkd if s['tier']==0])},
                    {len([s for s in ks24+ks25+qtkd if s['tier']==1])},
                    {len([s for s in ks24+ks25+qtkd if s['tier']==2])},
                    {len([s for s in ks24+ks25+qtkd if s['tier']==3])}
                ],
                backgroundColor: ['#ef4444', '#f59e0b', '#3b82f6', '#10b981'],
                borderWidth: 2, borderColor: '#18181b'
            }}]
        }},
        options: {{
            responsive: true, maintainAspectRatio: false,
            cutout: '68%',
            plugins: {{ legend: {{ display: false }} }}
        }}
    }});
    </script>
</body>
</html>
"""
    with open("outputs/Executive_Summary_DGNL_Report.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated outputs/Executive_Summary_DGNL_Report.html successfully!")

if __name__ == "__main__":
    data = load_data()
    build_executive_summary(data)
