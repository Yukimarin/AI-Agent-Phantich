# Master Report Generator v3: Concise UI, Natural Technical Terms, and Executive Bottlenecks Section
import json
import os
import sys

sys.path.append(os.path.dirname(__file__))
from build_complete_suite import load_data

def build_all_v3():
    data = load_data()
    ks24 = data["ks24"]
    ks25 = data["ks25"]
    qtkd = data["qtkd"]

    # Master numbers
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

    # ════════════════════════════════════════════════════════════════════════
    # 1. GENERATE EXECUTIVE SUMMARY HTML
    # ════════════════════════════════════════════════════════════════════════
    html_exec = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Báo Cáo Tổng Hợp ĐGNL Toàn Hệ Thống | Ban Giám Đốc Đào Tạo</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {{
            --bg-main:       #09090b;
            --bg-card:       #18181b;
            --border-color:  #27272a;
            --text-primary:  #f4f4f5;
            --text-secondary:#a1a1aa;
            --text-muted:    #71717a;
            --color-ks24:    #10b981;
            --color-ks25:    #3b82f6;
            --color-qtkd:    #f59e0b;
            --color-danger:  #ef4444;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', sans-serif; }}
        body {{ background: var(--bg-main); color: var(--text-primary); padding-bottom: 70px; }}

        .header {{
            background: rgba(18,18,21,0.85); backdrop-filter: blur(16px);
            border-bottom: 1px solid var(--border-color); position: sticky; top: 0; z-index: 200;
        }}
        .header-inner {{
            max-width: 1440px; margin: 0 auto; padding: 0.85rem 2rem;
            display: flex; justify-content: space-between; align-items: center;
        }}
        .logo-wrap {{ display: flex; align-items: center; gap: 0.75rem; }}
        .logo-badge {{
            background: linear-gradient(135deg, var(--color-ks24), var(--color-ks25), var(--color-qtkd));
            color: #fff; width: 40px; height: 40px; border-radius: 10px;
            display: flex; align-items: center; justify-content: center;
            font-family: 'Outfit', sans-serif; font-weight: 800; font-size: 1.15rem;
        }}
        .logo-text {{ font-family: 'Outfit', sans-serif; font-weight: 700; font-size: 1.1rem; color: #fff; }}
        .header-meta {{ font-size: 0.76rem; color: var(--text-muted); text-align: right; line-height: 1.35; }}

        .container {{ max-width: 1440px; margin: 1.5rem auto; padding: 0 2rem; }}

        /* Clean Executive Tabs (No "Tab 1:" prefix) */
        .exec-tabs {{
            display: flex; gap: 0.5rem; border-bottom: 1px solid var(--border-color);
            margin-bottom: 1.75rem; overflow-x: auto;
        }}
        .exec-tab-btn {{
            background: transparent; border: none; color: var(--text-muted);
            font-family: 'Outfit', sans-serif; font-size: 0.92rem; font-weight: 700;
            padding: 0.7rem 1.25rem; border-radius: 8px 8px 0 0; cursor: pointer;
            transition: all 0.2s; border-bottom: 3px solid transparent;
            display: flex; align-items: center; gap: 0.4rem; white-space: nowrap;
        }}
        .exec-tab-btn:hover {{ color: var(--text-primary); background: rgba(255,255,255,0.03); }}
        .exec-tab-btn.active {{
            color: #fff; border-bottom: 3px solid var(--color-ks25);
            background: rgba(59,130,246,0.08);
        }}

        .tab-pane {{ display: none; }}
        .tab-pane.active {{ display: block; animation: fadeIn 0.25s ease; }}
        @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(4px); }} to {{ opacity: 1; transform: translateY(0); }} }}

        /* KPI Strip */
        .kpi-grid {{
            display: grid; grid-template-columns: repeat(6, 1fr); gap: 0.85rem; margin-bottom: 1.75rem;
        }}
        .kpi-card {{
            background: var(--bg-card); border: 1px solid var(--border-color);
            border-radius: 10px; padding: 1rem; position: relative; overflow: hidden;
        }}
        .kpi-card::before {{
            content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
            background: linear-gradient(90deg, var(--accent-l), var(--accent-r));
        }}
        .kpi-card.blue   {{ --accent-l: #3b82f6; --accent-r: #60a5fa; }}
        .kpi-card.green  {{ --accent-l: #10b981; --accent-r: #34d399; }}
        .kpi-card.gold   {{ --accent-l: #f59e0b; --accent-r: #fbbf24; }}
        .kpi-card.purple {{ --accent-l: #8b5cf6; --accent-r: #a78bfa; }}
        .kpi-card.cyan   {{ --accent-l: #06b6d4; --accent-r: #22d3ee; }}

        .kpi-label {{ font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.5px; color: var(--text-muted); margin-bottom: 0.25rem; font-weight: 600; }}
        .kpi-value {{ font-family: 'Outfit', sans-serif; font-size: 1.65rem; font-weight: 800; color: #fff; }}
        .kpi-sub   {{ font-size: 0.7rem; color: var(--text-secondary); margin-top: 0.15rem; }}

        .section-header {{
            display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;
        }}
        .section-title {{
            font-family: 'Outfit', sans-serif; font-size: 1.15rem; font-weight: 700;
            color: #fff; border-left: 4px solid var(--color-ks25); padding-left: 0.6rem;
            display: flex; align-items: center; gap: 0.5rem;
        }}

        .cohort-grid {{
            display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 1.75rem;
        }}
        .cohort-card {{
            background: var(--bg-card); border: 1px solid var(--border-color);
            border-radius: 12px; padding: 1.25rem; display: flex; flex-direction: column;
        }}
        .cohort-card.ks24 {{ border-top: 3px solid var(--color-ks24); }}
        .cohort-card.ks25 {{ border-top: 3px solid var(--color-ks25); }}
        .cohort-card.qtkd {{ border-top: 3px solid var(--color-qtkd); }}

        .pill {{
            display: inline-block; padding: 0.2rem 0.6rem; border-radius: 999px;
            font-size: 0.72rem; font-weight: 700; width: fit-content; margin-bottom: 0.6rem;
        }}
        .pill.ks24 {{ background: rgba(16,185,129,0.12); color: var(--color-ks24); border: 1px solid rgba(16,185,129,0.25); }}
        .pill.ks25 {{ background: rgba(59,130,246,0.12); color: var(--color-ks25); border: 1px solid rgba(59,130,246,0.25); }}
        .pill.qtkd {{ background: rgba(245,158,11,0.12); color: var(--color-qtkd); border: 1px solid rgba(245,158,11,0.25); }}

        .stat-duo {{ display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; margin: 0.75rem 0; }}
        .stat-mini {{ background: rgba(255,255,255,0.025); border: 1px solid var(--border-color); border-radius: 8px; padding: 0.6rem; }}
        .stat-mini-label {{ font-size: 0.65rem; color: var(--text-muted); text-transform: uppercase; font-weight: 600; }}
        .stat-mini-val {{ font-family: 'Outfit', sans-serif; font-size: 1.25rem; font-weight: 800; margin-top: 0.1rem; }}

        .lens-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; margin-bottom: 1.5rem; }}
        .lens-card {{
            background: var(--bg-card); border: 1px solid var(--border-color);
            border-radius: 12px; padding: 1.25rem; display: flex; flex-direction: column;
        }}
        .lens-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem; }}
        .lens-title {{ font-family: 'Outfit', sans-serif; font-size: 0.95rem; font-weight: 700; color: #fff; display: flex; align-items: center; gap: 0.4rem; }}

        .metric-tag-row {{ display: flex; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 0.75rem; }}
        .metric-tag {{
            background: rgba(255,255,255,0.04); border: 1px solid var(--border-color);
            border-radius: 6px; padding: 0.35rem 0.65rem; font-size: 0.75rem; color: var(--text-secondary);
        }}
        .metric-tag strong {{ color: #fff; font-family: 'Outfit', sans-serif; font-size: 0.85rem; }}

        /* Bottlenecks executive card */
        .bottleneck-card {{
            background: rgba(239,68,68,0.04); border: 1px solid rgba(239,68,68,0.3);
            border-radius: 12px; padding: 1.25rem 1.5rem; margin-bottom: 1.75rem;
        }}
        .bottleneck-grid {{
            display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-top: 1rem;
        }}
        .bottleneck-item {{
            background: rgba(0,0,0,0.3); border: 1px solid var(--border-color);
            border-radius: 8px; padding: 0.85rem; font-size: 0.78rem; line-height: 1.45;
        }}
        .bottleneck-item strong {{ color: #f87171; display: block; margin-bottom: 0.25rem; font-size: 0.82rem; }}

        .timeline-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 1.5rem; }}
        .timeline-card {{
            background: var(--bg-card); border: 1px solid var(--border-color);
            border-radius: 12px; padding: 1.25rem; position: relative;
        }}
        .timeline-badge {{
            display: inline-flex; align-items: center; gap: 0.3rem; padding: 0.25rem 0.65rem;
            border-radius: 6px; font-size: 0.72rem; font-weight: 800; margin-bottom: 0.85rem;
            text-transform: uppercase; letter-spacing: 0.5px;
        }}
        .timeline-badge.t1 {{ background: rgba(239,68,68,0.15); color: #f87171; border: 1px solid rgba(239,68,68,0.3); }}
        .timeline-badge.t2 {{ background: rgba(245,158,11,0.15); color: #fbbf24; border: 1px solid rgba(245,158,11,0.3); }}
        .timeline-badge.t3 {{ background: rgba(16,185,129,0.15); color: #34d399; border: 1px solid rgba(16,185,129,0.3); }}

        .action-bullet-list {{ list-style: none; display: flex; flex-direction: column; gap: 0.65rem; font-size: 0.8rem; color: var(--text-secondary); }}
        .action-bullet-list li {{ display: flex; gap: 0.5rem; align-items: flex-start; line-height: 1.45; }}
        .action-bullet-list li::before {{ content: '👉'; flex-shrink: 0; }}
        .action-bullet-list strong {{ color: #fff; }}

        .table-compact {{ width: 100%; border-collapse: collapse; font-size: 0.82rem; }}
        .table-compact th, .table-compact td {{ padding: 0.6rem 0.75rem; border: 1px solid var(--border-color); text-align: center; }}
        .table-compact th {{ background: rgba(255,255,255,0.03); color: var(--text-muted); font-size: 0.72rem; font-weight: 700; text-transform: uppercase; }}
        .table-compact tr:hover {{ background: rgba(255,255,255,0.02); }}

        .footer-bar {{
            margin-top: 3rem; border-top: 1px solid var(--border-color);
            padding-top: 1.25rem; display: flex; justify-content: space-between; align-items: center;
            font-size: 0.75rem; color: var(--text-muted);
        }}
    </style>
</head>
<body>

    <header class="header">
        <div class="header-inner">
            <div class="logo-wrap">
                <div class="logo-badge">RKE</div>
                <div>
                    <div class="logo-text">Báo Cáo Tổng Hợp Khảo Thí ĐGNL Lần 1</div>
                    <div style="font-size:0.72rem;color:var(--text-muted);">Toàn Hệ Thống PTIT Rikkei Education (Khối KS24, KS25 CNTT &amp; Khối K25 QTKD)</div>
                </div>
            </div>
            <div class="header-meta">
                Ban Giám Đốc Đào Tạo &amp; Hội Đồng Chuyên Môn<br>
                Cập nhật: 02/09/2026
            </div>
        </div>
    </header>

    <div class="container">

        <!-- EXECUTIVE TABS (Cleaned - No Tab prefixes) -->
        <div class="exec-tabs">
            <button class="exec-tab-btn active" onclick="switchExecTab('tab-dash', event)">📊 Tổng Quan &amp; KPI</button>
            <button class="exec-tab-btn" onclick="switchExecTab('tab-lens', event)">🔬 6 Lăng Kính Khảo Thí</button>
            <button class="exec-tab-btn" onclick="switchExecTab('tab-diag', event)">🎯 Ma Trận Chẩn Đoán</button>
            <button class="exec-tab-btn" onclick="switchExecTab('tab-plan', event)">📋 Kế Hoạch Can Thiệp</button>
        </div>

        <!-- MASTER KPI STRIP -->
        <div class="kpi-grid">
            <div class="kpi-card blue">
                <div class="kpi-label">Tổng Sĩ Số Đăng Ký</div>
                <div class="kpi-value">{total_reg}</div>
                <div class="kpi-sub">KS24: {len(ks24)} | KS25: {len(ks25)} | QTKD: {len(qtkd)}</div>
            </div>
            <div class="kpi-card green">
                <div class="kpi-label">Dự Thi Thực Tế</div>
                <div class="kpi-value">{total_took}</div>
                <div class="kpi-sub">Tỷ lệ: {round(total_took/total_reg*100, 1)}%</div>
            </div>
            <div class="kpi-card gold">
                <div class="kpi-label">Đạt Chuẩn Chuyên Môn</div>
                <div class="kpi-value">{total_pass}</div>
                <div class="kpi-sub">Tỷ lệ Đạt: {round(total_pass/total_reg*100, 1)}%</div>
            </div>
            <div class="kpi-card purple">
                <div class="kpi-label">Chuẩn Đầu Ra (L2+L3)</div>
                <div class="kpi-value">{total_ready}</div>
                <div class="kpi-sub">Tỷ lệ: {round(total_ready/total_reg*100, 1)}%</div>
            </div>
            <div class="kpi-card cyan">
                <div class="kpi-label">Điểm TB Kỹ Năng Mềm</div>
                <div class="kpi-value">{round((avg_knm_ks24*len(ks24) + avg_knm_ks25*len(ks25) + avg_knm_qtkd*len(qtkd))/total_reg, 1)}</div>
                <div class="kpi-sub">Thang điểm 100</div>
            </div>
            <div class="kpi-card blue">
                <div class="kpi-label">Điểm TB Tiếng Anh</div>
                <div class="kpi-value">{round((avg_ta_ks24*len(ks24) + avg_ta_ks25*len(ks25) + avg_ta_qtkd*len(qtkd))/total_reg, 0):.0f}</div>
                <div class="kpi-sub">Chuẩn TOEIC / 990</div>
            </div>
        </div>

        <!-- ── TAB 1: TỔNG QUAN ────────────────────────────────────────────── -->
        <div id="tab-dash" class="tab-pane active">

            <!-- Executive Bottlenecks Card -->
            <div class="bottleneck-card">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div style="font-family:'Outfit',sans-serif;font-size:0.95rem;font-weight:700;color:#f87171;display:flex;align-items:center;gap:0.4rem;">
                        ⚠️ 4 Điểm Nghẽn Cốt Lõi Cần Giám Đốc Đào Tạo Quyết Sách
                    </div>
                    <span style="font-size:0.75rem;color:var(--text-muted);">Trích xuất từ dữ liệu khảo thí Lần 1</span>
                </div>
                <div class="bottleneck-grid">
                    <div class="bottleneck-item">
                        <strong>1. Độ Lệch Giảng Viên 7.7 Lần</strong>
                        Điểm thực hành giữa các lớp KS25 chênh từ 45.8đ xuống 5.9đ &rarr; Cần chuẩn hóa giáo án Live-Coding.
                    </div>
                    <div class="bottleneck-item">
                        <strong>2. Nghịch Lý Trắc Nghiệm (r = 0.14)</strong>
                        Trắc nghiệm đạt 70-80đ nhưng không code được API &rarr; Cần giảm 50% trắc nghiệm ở Lần 2.
                    </div>
                    <div class="bottleneck-item">
                        <strong>3. Phễu Rơi Rụng Phỏng Vấn (53%)</strong>
                        29 SV KS24 giỏi code nhưng liệt vấn đáp &rarr; Bắt buộc tham gia Mock Interview 1-on-1.
                    </div>
                    <div class="bottleneck-item">
                        <strong>4. Khoảng Trống Tiếng Anh</strong>
                        Điểm TOEIC cả 3 khối chỉ đạt 260-280đ &rarr; Bổ sung Business English &amp; TOEIC 450+ trước tốt nghiệp.
                    </div>
                </div>
            </div>

            <div class="section-header">
                <div class="section-title">🏛️ Đối Chiếu 3 Khối Đào Tạo (735 Sinh Viên)</div>
            </div>

            <div class="cohort-grid">
                <!-- KS24 -->
                <div class="cohort-card ks24">
                    <span class="pill ks24">☕ KS24 CNTT – JAVA / SPRING BOOT (CUỐI KỲ III)</span>
                    <div style="font-size:0.78rem;color:var(--text-secondary);line-height:1.4;">
                        Nghiệm thu chuẩn bị Đồ án Tốt nghiệp &amp; Tuyển dụng Doanh nghiệp.
                    </div>
                    <div class="stat-duo">
                        <div class="stat-mini">
                            <div class="stat-mini-label">Dự Thi / Sĩ Số</div>
                            <div class="stat-mini-val" style="color:var(--color-ks24);">{took_ks24} / {len(ks24)}</div>
                        </div>
                        <div class="stat-mini">
                            <div class="stat-mini-label">Điểm TB Final</div>
                            <div class="stat-mini-val" style="color:var(--color-ks24);">{avg_ks24}/10</div>
                        </div>
                        <div class="stat-mini">
                            <div class="stat-mini-label">Chuẩn Đầu Ra</div>
                            <div class="stat-mini-val" style="color:#34d399;">{ready_ks24} SV ({round(ready_ks24/len(ks24)*100, 1)}%)</div>
                        </div>
                        <div class="stat-mini">
                            <div class="stat-mini-label">Kỹ Năng Mềm / TA</div>
                            <div class="stat-mini-val" style="color:#a7f3d0;font-size:1.05rem;">{avg_knm_ks24}đ / {avg_ta_ks24:.0f}</div>
                        </div>
                    </div>
                    <div style="font-size:0.75rem;color:#f87171;margin-top:auto;padding-top:0.5rem;border-top:1px solid var(--border-color);">
                        ⚠ <strong>Điểm nghẽn:</strong> 29 SV code giỏi nhưng vấn đáp &lt; 50đ.
                    </div>
                    <a href="KS24_DGNL_Report.html" style="margin-top:0.6rem;text-align:center;padding:0.4rem;background:rgba(16,185,129,0.15);color:var(--color-ks24);border:1px solid rgba(16,185,129,0.3);border-radius:6px;font-size:0.78rem;font-weight:700;text-decoration:none;">Xem Chi Tiết KS24 →</a>
                </div>

                <!-- KS25 -->
                <div class="cohort-card ks25">
                    <span class="pill ks25">🐍 KS25 CNTT – FASTAPI / PYTHON (GIỮA KỲ II)</span>
                    <div style="font-size:0.78rem;color:var(--text-secondary);line-height:1.4;">
                        Khảo sát giữa kỳ phục vụ phân tầng học thuật chuyên sâu Kỳ III.
                    </div>
                    <div class="stat-duo">
                        <div class="stat-mini">
                            <div class="stat-mini-label">Dự Thi / Sĩ Số</div>
                            <div class="stat-mini-val" style="color:var(--color-ks25);">{took_ks25} / {len(ks25)}</div>
                        </div>
                        <div class="stat-mini">
                            <div class="stat-mini-label">Điểm TB Final</div>
                            <div class="stat-mini-val" style="color:var(--color-ks25);">{avg_ks25}/10</div>
                        </div>
                        <div class="stat-mini">
                            <div class="stat-mini-label">Chuẩn Đầu Ra</div>
                            <div class="stat-mini-val" style="color:#60a5fa;">{ready_ks25} SV ({round(ready_ks25/len(ks25)*100, 1)}%)</div>
                        </div>
                        <div class="stat-mini">
                            <div class="stat-mini-label">Kỹ Năng Mềm / TA</div>
                            <div class="stat-mini-val" style="color:#93c5fd;font-size:1.05rem;">{avg_knm_ks25}đ / {avg_ta_ks25:.0f}</div>
                        </div>
                    </div>
                    <div style="font-size:0.75rem;color:#f87171;margin-top:auto;padding-top:0.5rem;border-top:1px solid var(--border-color);">
                        ⚠ <strong>Điểm nghẽn:</strong> 151 SV trắc nghiệm cao nhưng liệt code thực hành.
                    </div>
                    <a href="KS25_DGNL_Report.html" style="margin-top:0.6rem;text-align:center;padding:0.4rem;background:rgba(59,130,246,0.15);color:var(--color-ks25);border:1px solid rgba(59,130,246,0.3);border-radius:6px;font-size:0.78rem;font-weight:700;text-decoration:none;">Xem Chi Tiết KS25 →</a>
                </div>

                <!-- QTKD -->
                <div class="cohort-card qtkd">
                    <span class="pill qtkd">💼 K25 QTKD – QUẢN TRỊ KINH DOANH (GIỮA KỲ II)</span>
                    <div style="font-size:0.78rem;color:var(--text-secondary);line-height:1.4;">
                        Nghiệm thu 11 nhóm đề án kinh doanh và bảo vệ trước Hội đồng.
                    </div>
                    <div class="stat-duo">
                        <div class="stat-mini">
                            <div class="stat-mini-label">Dự Thi / Sĩ Số</div>
                            <div class="stat-mini-val" style="color:var(--color-qtkd);">{took_qtkd} / {len(qtkd)}</div>
                        </div>
                        <div class="stat-mini">
                            <div class="stat-mini-label">Điểm TB Final</div>
                            <div class="stat-mini-val" style="color:var(--color-qtkd);">{avg_qtkd}/10</div>
                        </div>
                        <div class="stat-mini">
                            <div class="stat-mini-label">Chuẩn Đầu Ra</div>
                            <div class="stat-mini-val" style="color:#fbbf24;">{ready_qtkd} SV ({round(ready_qtkd/len(qtkd)*100, 1)}%)</div>
                        </div>
                        <div class="stat-mini">
                            <div class="stat-mini-label">Kỹ Năng Mềm / TA</div>
                            <div class="stat-mini-val" style="color:#fde68a;font-size:1.05rem;">{avg_knm_qtkd}đ / {avg_ta_qtkd:.0f}</div>
                        </div>
                    </div>
                    <div style="font-size:0.75rem;color:#f87171;margin-top:auto;padding-top:0.5rem;border-top:1px solid var(--border-color);">
                        ⚠ <strong>Điểm nghẽn:</strong> 40 SV giỏi chuyên môn nhưng Tiếng Anh sơ cấp (&lt;350đ).
                    </div>
                    <a href="QTKD_DGNL_Report.html" style="margin-top:0.6rem;text-align:center;padding:0.4rem;background:rgba(245,158,11,0.15);color:var(--color-qtkd);border:1px solid rgba(245,158,11,0.3);border-radius:6px;font-size:0.78rem;font-weight:700;text-decoration:none;">Xem Chi Tiết QTKD →</a>
                </div>
            </div>

            <!-- Charts Duo -->
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-bottom:1.5rem;">
                <div style="background:var(--bg-card);border:1px solid var(--border-color);border-radius:12px;padding:1.25rem;">
                    <div style="font-family:'Outfit',sans-serif;font-size:0.9rem;font-weight:700;color:#fff;margin-bottom:0.75rem;">
                        📈 So Sánh Điểm Chuyên Môn &amp; Kỹ Năng Mềm 3 Khối
                    </div>
                    <div style="height:230px;position:relative;">
                        <canvas id="chartCompDash"></canvas>
                    </div>
                </div>
                <div style="background:var(--bg-card);border:1px solid var(--border-color);border-radius:12px;padding:1.25rem;">
                    <div style="font-family:'Outfit',sans-serif;font-size:0.9rem;font-weight:700;color:#fff;margin-bottom:0.75rem;">
                        🎯 Phân Bố Mức Độ Năng Lực Toàn Hệ Thống ({total_reg} SV)
                    </div>
                    <div style="height:230px;position:relative;">
                        <canvas id="chartDoughnutDash"></canvas>
                    </div>
                </div>
            </div>
        </div>

        <!-- ── TAB 2: 6 LĂNG KÍNH KHẢO THÍ ─────────────────────────────────── -->
        <div id="tab-lens" class="tab-pane">
            <div class="section-header">
                <div class="section-title">🔬 6 Lăng Kính Chuyên Sâu Khảo Thí &amp; Quản Trị Đào Tạo</div>
            </div>

            <div class="lens-grid">
                <!-- LENS 1 -->
                <div class="lens-card" style="border-left:4px solid #ef4444;">
                    <div class="lens-header">
                        <div class="lens-title">🌐 1. Nghịch Lý Đo Lường: Lý Thuyết vs Thực Hành (KS25)</div>
                        <span style="background:rgba(239,68,68,0.2);color:#f87171;padding:0.2rem 0.5rem;border-radius:4px;font-size:0.72rem;font-weight:700;">r = 0.14</span>
                    </div>
                    <div class="metric-tag-row">
                        <div class="metric-tag">Trắc nghiệm TB: <strong>65.6 - 73.0đ</strong></div>
                        <div class="metric-tag">Thực hành Code TB: <strong>29.0 / 100đ</strong></div>
                        <div class="metric-tag">Tỷ lệ Lệch: <strong>151 SV (51.5%)</strong></div>
                    </div>
                    <div style="font-size:0.78rem;color:var(--text-secondary);line-height:1.45;">
                        • Hệ số tương quan r=0.14 cho thấy trắc nghiệm <em>không đo lường được năng lực Live-Coding</em>.<br>
                        • Sinh viên học thuộc định nghĩa cú pháp nhưng không có phản xạ mở IDE tự xây dựng API 4 lớp từ đầu.
                    </div>
                </div>

                <!-- LENS 2 -->
                <div class="lens-card" style="border-left:4px solid #fbbf24;">
                    <div class="lens-header">
                        <div class="lens-title">👥 2. Hiện Tượng "Ỷ Lại Nhóm" Trong Đồ Án (KS24)</div>
                        <span style="background:rgba(245,158,11,0.2);color:#fbbf24;padding:0.2rem 0.5rem;border-radius:4px;font-size:0.72rem;font-weight:700;">r = 0.71 vs 0.17</span>
                    </div>
                    <div class="metric-tag-row">
                        <div class="metric-tag">KNM vs Sản Phẩm: <strong>r = 0.71</strong></div>
                        <div class="metric-tag">KNM vs Vấn Đáp 1-1: <strong>r = 0.17</strong></div>
                    </div>
                    <div style="font-size:0.78rem;color:var(--text-secondary);line-height:1.45;">
                        • Sinh viên có KNM tốt thường làm mượt phần thuyết trình đồ án nhóm, đạt điểm Sản phẩm cao.<br>
                        • Tuy nhiên, khi Hội đồng vấn đáp cá nhân 1-1 về xử lý đa luồng/bảo mật, sinh viên bị lộ lỗ hổng kỹ thuật.
                    </div>
                </div>

                <!-- LENS 3 -->
                <div class="lens-card" style="border-left:4px solid #3b82f6;">
                    <div class="lens-header">
                        <div class="lens-title">🏫 3. Điểm Nghẽn Chất Lượng Giữa Các Lớp (Giảng Viên)</div>
                        <span style="background:rgba(59,130,246,0.2);color:#60a5fa;padding:0.2rem 0.5rem;border-radius:4px;font-size:0.72rem;font-weight:700;">Chênh 7.7 Lần</span>
                    </div>
                    <div class="metric-tag-row">
                        <div class="metric-tag">Lớp Cao Nhất (HN-CNTT8): <strong>45.8đ TH</strong></div>
                        <div class="metric-tag">Lớp Thấp Nhất (HCM-CNTT8): <strong>5.9đ TH</strong></div>
                    </div>
                    <div style="font-size:0.78rem;color:var(--text-secondary);line-height:1.45;">
                        • Cùng 1 chương trình nhưng lớp dạy theo phương pháp Hands-on Live Coding có điểm cao gấp 7.7 lần lớp dạy lý thuyết slide.<br>
                        • Cần chuẩn hóa đồng bộ giáo án thực hành giữa tất cả các giảng viên trong bộ môn.
                    </div>
                </div>

                <!-- LENS 4 -->
                <div class="lens-card" style="border-left:4px solid #10b981;">
                    <div class="lens-header">
                        <div class="lens-title">💼 4. Mô Phỏng Phễu Tuyển Dụng Doanh Nghiệp (KS24)</div>
                        <span style="background:rgba(16,185,129,0.2);color:#34d399;padding:0.2rem 0.5rem;border-radius:4px;font-size:0.72rem;font-weight:700;">Đỗ 47.0%</span>
                    </div>
                    <div class="metric-tag-row">
                        <div class="metric-tag">Vòng 1 (CV/HR): <strong>75.1% Qua</strong></div>
                        <div class="metric-tag">Vòng 2 (Vấn đáp): <strong>69.2% Qua</strong></div>
                        <div class="metric-tag">Vòng 3 (Live Code): <strong>73.5% Qua</strong></div>
                    </div>
                    <div style="font-size:0.78rem;color:var(--text-secondary);line-height:1.45;">
                        • Chỉ <strong>87 / 185 SV (47.0%)</strong> đỗ đồng thời cả 3 vòng nếu phỏng vấn tại doanh nghiệp tiêu chuẩn.<br>
                        • 29 SV rơi rụng oan ở vòng vấn đáp; 20 SV rơi rụng ở vòng Live-Coding.
                    </div>
                </div>
            </div>

            <!-- Visual Funnel & Class Disparity Charts -->
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-bottom:1.5rem;">
                <div style="background:var(--bg-card);border:1px solid var(--border-color);border-radius:12px;padding:1.25rem;">
                    <div style="font-family:'Outfit',sans-serif;font-size:0.9rem;font-weight:700;color:#fff;margin-bottom:0.75rem;">
                        📉 Mô Phỏng Tỷ Lệ Đỗ Qua 4 Vòng Tuyển Dụng (KS24)
                    </div>
                    <div style="height:210px;position:relative;">
                        <canvas id="chartFunnel"></canvas>
                    </div>
                </div>
                <div style="background:var(--bg-card);border:1px solid var(--border-color);border-radius:12px;padding:1.25rem;">
                    <div style="font-family:'Outfit',sans-serif;font-size:0.9rem;font-weight:700;color:#fff;margin-bottom:0.75rem;">
                        🏫 Độ Phân Hóa Điểm Thực Hành Giữa Các Lớp KS25 (FastAPI)
                    </div>
                    <div style="height:210px;position:relative;">
                        <canvas id="chartClassDisp"></canvas>
                    </div>
                </div>
            </div>
        </div>

        <!-- ── TAB 3: MA TRẬN CHẨN ĐOÁN ────────────────────────────────────── -->
        <div id="tab-diag" class="tab-pane">
            <div class="section-header">
                <div class="section-title">🎯 Ma Trận Chẩn Đoán Phân Hóa Năng Lực Học Viên</div>
            </div>

            <div style="display:grid;grid-template-columns:repeat(4, 1fr);gap:1rem;margin-bottom:1.5rem;">
                <div style="background:var(--bg-card);border:1px solid var(--border-color);border-top:3px solid #ef4444;border-radius:10px;padding:1.15rem;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5rem;">
                        <span style="font-size:0.85rem;font-weight:700;color:#f87171;">🔇 Vững Kỹ Thuật - Yếu Vấn Đáp</span>
                        <span style="font-family:'Outfit',sans-serif;font-size:1.1rem;font-weight:800;color:#fff;">29 SV</span>
                    </div>
                    <div style="font-size:0.75rem;color:var(--text-secondary);line-height:1.4;margin-bottom:0.6rem;">
                        Code TH &ge; 65đ, Vấn đáp &lt; 50đ. Rào cản tâm lý và thiếu phản xạ trả lời STAR.
                    </div>
                    <div style="background:rgba(239,68,68,0.1);padding:0.4rem 0.6rem;border-radius:6px;font-size:0.73rem;color:#fca5a5;">
                        👉 <strong>Mock Interview 1-on-1</strong> (Không bắt học lại code).
                    </div>
                </div>

                <div style="background:var(--bg-card);border:1px solid var(--border-color);border-top:3px solid #fbbf24;border-radius:10px;padding:1.15rem;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5rem;">
                        <span style="font-size:0.85rem;font-weight:700;color:#fbbf24;">🗣️ Thế Mạnh KNM - Yếu Code</span>
                        <span style="font-family:'Outfit',sans-serif;font-size:1.1rem;font-weight:800;color:#fff;">32 SV</span>
                    </div>
                    <div style="font-size:0.75rem;color:var(--text-secondary);line-height:1.4;margin-bottom:0.6rem;">
                        KNM &ge; 75đ, Thực hành &lt; 50đ. Dễ đỗ vòng HR nhưng trượt vòng Live-Coding.
                    </div>
                    <div style="background:rgba(245,158,11,0.1);padding:0.4rem 0.6rem;border-radius:6px;font-size:0.73rem;color:#fde68a;">
                        👉 <strong>Tư vấn Chuyển luồng BA / QA</strong> / Tech Sales sớm.
                    </div>
                </div>

                <div style="background:var(--bg-card);border:1px solid var(--border-color);border-top:3px solid #ef4444;border-radius:10px;padding:1.15rem;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5rem;">
                        <span style="font-size:0.85rem;font-weight:700;color:#f87171;">🚨 Nắm Lý Thuyết - Hổng Code TH</span>
                        <span style="font-family:'Outfit',sans-serif;font-size:1.1rem;font-weight:800;color:#fff;">151 SV</span>
                    </div>
                    <div style="font-size:0.75rem;color:var(--text-secondary);line-height:1.4;margin-bottom:0.6rem;">
                        TN &ge; 65đ, Thực hành &lt; 50đ. Bệnh học vẹt trắc nghiệm, chưa gõ được code độc lập.
                    </div>
                    <div style="background:rgba(239,68,68,0.1);padding:0.4rem 0.6rem;border-radius:6px;font-size:0.73rem;color:#fca5a5;">
                        👉 <strong>FastAPI Live-Coding Bootcamp 2 tuần</strong> trước Kỳ III.
                    </div>
                </div>

                <div style="background:var(--bg-card);border:1px solid var(--border-color);border-top:3px solid #f59e0b;border-radius:10px;padding:1.15rem;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5rem;">
                        <span style="font-size:0.85rem;font-weight:700;color:#fbbf24;">💼 Giỏi QTKD - Hổng Ngoại Ngữ</span>
                        <span style="font-family:'Outfit',sans-serif;font-size:1.1rem;font-weight:800;color:#fff;">40 SV</span>
                    </div>
                    <div style="font-size:0.75rem;color:var(--text-secondary);line-height:1.4;margin-bottom:0.6rem;">
                        Điểm QTKD &ge; 70đ, Tiếng Anh &lt; 350đ. Rào cản ứng tuyển doanh nghiệp FDI / MNC.
                    </div>
                    <div style="background:rgba(245,158,11,0.1);padding:0.4rem 0.6rem;border-radius:6px;font-size:0.73rem;color:#fde68a;">
                        👉 <strong>Business English Workshop</strong> bắt buộc từ Kỳ III.
                    </div>
                </div>
            </div>

            <!-- Table -->
            <div style="background:var(--bg-card);border:1px solid var(--border-color);border-radius:12px;padding:1.25rem;">
                <div style="font-family:'Outfit',sans-serif;font-size:0.9rem;font-weight:700;color:#fff;margin-bottom:0.75rem;">
                    📊 Bảng Ma Trận Học Thuật Đối Chiếu 3 Khối
                </div>
                <table class="table-compact">
                    <thead>
                        <tr>
                            <th style="text-align:left;">Chỉ Số Khảo Thí</th>
                            <th style="color:var(--color-ks24);">☕ KS24 CNTT</th>
                            <th style="color:var(--color-ks25);">🐍 KS25 CNTT</th>
                            <th style="color:var(--color-qtkd);">💼 K25 QTKD</th>
                            <th style="text-align:left;">Kết Luận Sư Phạm</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td style="text-align:left;font-weight:600;color:#fff;">Sĩ số / Dự thi</td>
                            <td>{len(ks24)} / {took_ks24}</td>
                            <td>{len(ks25)} / {took_ks25}</td>
                            <td>{len(qtkd)} / {took_qtkd}</td>
                            <td style="text-align:left;">QTKD có tỷ lệ dự thi cao nhất ({round(took_qtkd/len(qtkd)*100, 1)}%)</td>
                        </tr>
                        <tr>
                            <td style="text-align:left;font-weight:600;color:#fff;">Điểm TB Final / 10</td>
                            <td style="color:#34d399;font-weight:700;">{avg_ks24}</td>
                            <td style="color:#f87171;font-weight:700;">{avg_ks25}</td>
                            <td style="color:#fbbf24;font-weight:700;">{avg_qtkd}</td>
                            <td style="text-align:left;">KS25 phản ánh giai đoạn giữa kỳ II; KS24 đã vững vàng</td>
                        </tr>
                        <tr>
                            <td style="text-align:left;font-weight:600;color:#fff;">Điểm TB KNM / 100</td>
                            <td style="color:#34d399;">{avg_knm_ks24}</td>
                            <td style="color:#60a5fa;">{avg_knm_ks25}</td>
                            <td style="color:#fbbf24;font-weight:700;">{avg_knm_qtkd}</td>
                            <td style="text-align:left;">Khối QTKD vượt trội về thuyết trình nhóm thực chiến</td>
                        </tr>
                        <tr>
                            <td style="text-align:left;font-weight:600;color:#fff;">Điểm TB Tiếng Anh (TOEIC)</td>
                            <td>{avg_ta_ks24:.0f}</td>
                            <td>{avg_ta_ks25:.0f}</td>
                            <td>{avg_ta_qtkd:.0f}</td>
                            <td style="text-align:left;">Điểm nghẽn chung của cả 3 khối so với chuẩn quốc tế</td>
                        </tr>
                        <tr>
                            <td style="text-align:left;font-weight:600;color:#fff;">Chuẩn Đầu Ra (Mức 2+3)</td>
                            <td style="color:#34d399;font-weight:700;">{round(ready_ks24/len(ks24)*100, 1)}%</td>
                            <td style="color:#f87171;font-weight:700;">{round(ready_ks25/len(ks25)*100, 1)}%</td>
                            <td style="color:#fbbf24;font-weight:700;">{round(ready_qtkd/len(qtkd)*100, 1)}%</td>
                            <td style="text-align:left;">Khối QTKD và KS24 sẵn sàng tốt nghiệp; KS25 cần phân tầng</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- ── TAB 4: KẾ HOẠCH CAN THIỆP ───────────────────────────────────── -->
        <div id="tab-plan" class="tab-pane">
            <div class="section-header">
                <div class="section-title">📋 Kế Hoạch Can Thiệp Sư Phạm 3 Tầng Dành Cho Giám Đốc Đào Tạo</div>
            </div>

            <div class="timeline-grid">
                <div class="timeline-card" style="border-top:3px solid #ef4444;">
                    <span class="timeline-badge t1">⚡ TẦNG 1: CẤP BÁCH (0 – 30 NGÀY)</span>
                    <ul class="action-bullet-list">
                        <li>
                            <div>
                                <strong>Mock Interview 1-on-1 (KS24):</strong><br>
                                Tổ chức 3 buổi phỏng vấn giả định với Tech Lead doanh nghiệp cho 29 SV giỏi code yếu vấn đáp theo phương pháp STAR.
                            </div>
                        </li>
                        <li>
                            <div>
                                <strong>FastAPI Live-Coding Bootcamp (KS25):</strong><br>
                                Khóa bổ trợ 2 tuần cho 151 SV hổng code; cung cấp Project Skeleton sẵn để rèn phản xạ viết API.
                            </div>
                        </li>
                        <li>
                            <div>
                                <strong>Hội Thảo Phân Luồng BA / QA Sớm:</strong><br>
                                Tư vấn chuyển luồng chuyên ngành cho 32 SV có KNM tốt nhưng không có thế mạnh code sâu.
                            </div>
                        </li>
                    </ul>
                </div>

                <div class="timeline-card" style="border-top:3px solid #fbbf24;">
                    <span class="timeline-badge t2">🔄 TẦNG 2: QUY TRÌNH &amp; GIẢNG VIÊN (KỲ III - IV)</span>
                    <ul class="action-bullet-list">
                        <li>
                            <div>
                                <strong>Quy Định "Live-Code Review 3 Phút":</strong><br>
                                Bắt buộc dành 30% thời lượng mỗi buổi Lab để sinh viên thuyết trình giải pháp code cá nhân.
                            </div>
                        </li>
                        <li>
                            <div>
                                <strong>Chuẩn Hóa Giáo Án Giảng Viên:</strong><br>
                                Chấn chỉnh phương pháp giảng dạy tại các lớp điểm thực hành dưới 20đ (HCM-CNTT8, HN-CNTT6).
                            </div>
                        </li>
                        <li>
                            <div>
                                <strong>Business English Workshop (QTKD):</strong><br>
                                Triển khai học phần tiếng Anh thương mại bắt buộc từ Kỳ III để nâng chuẩn TOEIC &ge; 450+.
                            </div>
                        </li>
                    </ul>
                </div>

                <div class="timeline-card" style="border-top:3px solid #10b981;">
                    <span class="timeline-badge t3">🎯 TẦNG 3: KHẢO THÍ &amp; CHUẨN ĐẦU RA (DÀI HẠN)</span>
                    <ul class="action-bullet-list">
                        <li>
                            <div>
                                <strong>Tái Cấu Trúc Đề Thi ĐGNL Lần 2:</strong><br>
                                Giảm 50% câu hỏi trắc nghiệm lý thuyết, tăng thời lượng bài thi Live-Coding &amp; Vấn đáp thực tế.
                            </div>
                        </li>
                        <li>
                            <div>
                                <strong>Áp Dụng Bộ Chỉ Số GEI Tốt Nghiệp:</strong><br>
                                GEI = Code (40%) + Vấn đáp/KNM (35%) + Ngoại ngữ (25%).
                            </div>
                        </li>
                        <li>
                            <div>
                                <strong>Cam Kết Chuẩn Đầu Ra Doanh Nghiệp:</strong><br>
                                Đảm bảo tỷ lệ sinh viên đỗ phỏng vấn thử việc đúng chuyên ngành đạt &gt; 85% sau tốt nghiệp.
                            </div>
                        </li>
                    </ul>
                </div>
            </div>

            <div style="background:rgba(255,255,255,0.02);border:1px solid var(--border-color);border-radius:10px;padding:1rem 1.25rem;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:0.75rem;">
                <div style="font-size:0.8rem;color:var(--text-secondary);">
                    📑 Tra cứu danh bạ chi tiết và kế hoạch can thiệp từng sinh viên:
                </div>
                <div style="display:flex;gap:0.6rem;">
                    <a href="KS24_DGNL_Report.html" style="padding:0.35rem 0.75rem;background:rgba(16,185,129,0.15);color:#34d399;border:1px solid rgba(16,185,129,0.3);border-radius:6px;font-size:0.78rem;font-weight:700;text-decoration:none;">☕ Chi Tiết KS24</a>
                    <a href="KS25_DGNL_Report.html" style="padding:0.35rem 0.75rem;background:rgba(59,130,246,0.15);color:#60a5fa;border:1px solid rgba(59,130,246,0.3);border-radius:6px;font-size:0.78rem;font-weight:700;text-decoration:none;">🐍 Chi Tiết KS25</a>
                    <a href="QTKD_DGNL_Report.html" style="padding:0.35rem 0.75rem;background:rgba(245,158,11,0.15);color:#fbbf24;border:1px solid rgba(245,158,11,0.3);border-radius:6px;font-size:0.78rem;font-weight:700;text-decoration:none;">💼 Chi Tiết QTKD</a>
                </div>
            </div>
        </div>

        <!-- FOOTER -->
        <div class="footer-bar">
            <div>Phòng Chuyên Môn &amp; Khảo Thí Đào Tạo | PTIT Rikkei Education</div>
            <div>Báo Cáo Tổng Hợp ĐGNL Lần 1 © 2026. Chuẩn Hóa Quản Trị Giáo Dục.</div>
        </div>

    </div>

    <!-- CHARTS JS -->
    <script>
    function switchExecTab(tabId, evt) {{
        document.querySelectorAll('.tab-pane').forEach(el => el.classList.remove('active'));
        document.querySelectorAll('.exec-tab-btn').forEach(el => el.classList.remove('active'));
        document.getElementById(tabId).classList.add('active');
        if (evt && evt.currentTarget) evt.currentTarget.classList.add('active');
    }}

    const ctx1 = document.getElementById('chartCompDash').getContext('2d');
    new Chart(ctx1, {{
        type: 'bar',
        data: {{
            labels: ['☕ KS24 CNTT', '🐍 KS25 CNTT', '💼 K25 QTKD'],
            datasets: [
                {{
                    label: 'Điểm TB Chuyên Môn (/10)',
                    data: [{avg_ks24}, {avg_ks25}, {avg_qtkd}],
                    backgroundColor: ['rgba(16,185,129,0.7)', 'rgba(59,130,246,0.7)', 'rgba(245,158,11,0.7)'],
                    borderColor: ['#10b981', '#3b82f6', '#f59e0b'],
                    borderWidth: 1.5, borderRadius: 6
                }},
                {{
                    label: 'Điểm TB Kỹ Năng Mềm (/10 quy đổi)',
                    data: [{round(avg_knm_ks24/10.0, 2)}, {round(avg_knm_ks25/10.0, 2)}, {round(avg_knm_qtkd/10.0, 2)}],
                    backgroundColor: 'rgba(139,92,246,0.6)',
                    borderColor: '#8b5cf6',
                    borderWidth: 1.5, borderRadius: 6
                }}
            ]
        }},
        options: {{
            responsive: true, maintainAspectRatio: false,
            plugins: {{ legend: {{ labels: {{ color: '#a1a1aa', font: {{ size: 11 }} }} }} }},
            scales: {{
                y: {{ beginAtZero: true, max: 10, grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ color: '#a1a1aa' }} }},
                x: {{ grid: {{ display: false }}, ticks: {{ color: '#a1a1aa' }} }}
            }}
        }}
    }});

    const ctx2 = document.getElementById('chartDoughnutDash').getContext('2d');
    new Chart(ctx2, {{
        type: 'doughnut',
        data: {{
            labels: ['Mức 3 - Làm Chủ Tốt', 'Mức 2 - Chuẩn Doanh Nghiệp', 'Mức 1 - Cơ Bản', 'Mức 0 - Chưa Đạt'],
            datasets: [{{
                data: [
                    {len([s for s in ks24+ks25+qtkd if s['tier']==3])},
                    {len([s for s in ks24+ks25+qtkd if s['tier']==2])},
                    {len([s for s in ks24+ks25+qtkd if s['tier']==1])},
                    {len([s for s in ks24+ks25+qtkd if s['tier']==0])}
                ],
                backgroundColor: ['#10b981', '#3b82f6', '#f59e0b', '#ef4444'],
                borderWidth: 2, borderColor: '#18181b'
            }}]
        }},
        options: {{
            responsive: true, maintainAspectRatio: false,
            cutout: '68%',
            plugins: {{ legend: {{ position: 'right', labels: {{ color: '#a1a1aa', font: {{ size: 10 }} }} }} }}
        }}
    }});

    const ctx3 = document.getElementById('chartFunnel').getContext('2d');
    new Chart(ctx3, {{
        type: 'bar',
        data: {{
            labels: ['Dự Thi (185 SV)', 'V1: CV/HR (139 SV)', 'V2: Vấn Đáp (128 SV)', 'V3: Live-Code (136 SV)', 'Đỗ Chung Cuộc (87 SV)'],
            datasets: [{{
                data: [100, 75.1, 69.2, 73.5, 47.0],
                backgroundColor: ['#3f3f46', '#3b82f6', '#f59e0b', '#8b5cf6', '#10b981'],
                borderRadius: 6
            }}]
        }},
        options: {{
            indexAxis: 'y', responsive: true, maintainAspectRatio: false,
            plugins: {{ legend: {{ display: false }} }},
            scales: {{
                x: {{ beginAtZero: true, max: 100, grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ callback: v => v + '%', color: '#a1a1aa' }} }},
                y: {{ grid: {{ display: false }}, ticks: {{ color: '#a1a1aa', font: {{ size: 10 }} }} }}
            }}
        }}
    }});

    const ctx4 = document.getElementById('chartClassDisp').getContext('2d');
    new Chart(ctx4, {{
        type: 'bar',
        data: {{
            labels: ['HN-CNTT8 (Top 1)', 'HCM-CNTT5', 'HN-CNTT4', 'HN-CNTT1', 'HCM-CNTT6', 'HN-CNTT2', 'HN-CNTT6', 'HCM-CNTT8 (Thấp nhất)'],
            datasets: [{{
                label: 'Điểm Thực Hành TB / 100',
                data: [45.8, 35.8, 27.3, 25.9, 25.4, 16.3, 14.8, 5.9],
                backgroundColor: [
                    '#10b981', '#34d399', '#3b82f6', '#60a5fa', '#f59e0b', '#fbbf24', '#f87171', '#ef4444'
                ],
                borderRadius: 6
            }}]
        }},
        options: {{
            responsive: true, maintainAspectRatio: false,
            plugins: {{ legend: {{ display: false }} }},
            scales: {{
                y: {{ beginAtZero: true, max: 50, grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ color: '#a1a1aa' }} }},
                x: {{ grid: {{ display: false }}, ticks: {{ color: '#a1a1aa', font: {{ size: 9 }} }} }}
            }}
        }}
    }});
    </script>
</body>
</html>
"""
    with open("outputs/Executive_Summary_DGNL_Report.html", "w", encoding="utf-8") as f:
        f.write(html_exec)
    print("Compiled outputs/Executive_Summary_DGNL_Report.html v3!")

if __name__ == "__main__":
    build_all_v3()
