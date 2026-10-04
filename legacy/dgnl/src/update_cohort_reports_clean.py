# -*- coding: utf-8 -*-
"""
Ultra-Modern Cohort Reports Builder v7 (KS24, KS25, QTKD)
With Consistent Decision-Card Bento Layout, 2-Tone Problem/Solution Blocks, and High-Contrast Visuals
"""
import json
import os
import sys

sys.path.append(os.path.dirname(__file__))
from build_complete_suite import load_data
from modern_theme import get_shared_css
from modern_curriculum_theme import get_enhanced_curriculum_css

def build_cohort_reports_v7():
    data = load_data()
    base_css_24 = get_shared_css(primary_color="#10b981", accent_color="#3b82f6")
    base_css_25 = get_shared_css(primary_color="#3b82f6", accent_color="#8b5cf6")
    base_css_q   = get_shared_css(primary_color="#f59e0b", accent_color="#10b981")
    curric_css  = get_enhanced_curriculum_css()
    
    # ════════════════════════════════════════════════════════════════════════
    # 1. KS24 REPORT
    # ════════════════════════════════════════════════════════════════════════
    ks24 = data["ks24"]
    total_reg_24 = len(ks24)
    active_24 = [s for s in ks24 if not s["is_absent"]]
    took_24 = len(active_24)
    ready_24 = len([s for s in ks24 if s["tier"] in [2, 3]])
    ready_pct_24 = round(ready_24 / total_reg_24 * 100, 1) if total_reg_24 else 0.0
    avg_final_24 = round(sum(s["final_10"] for s in active_24) / took_24, 2) if took_24 else 0.0
    avg_knm_24 = round(sum(s["knm"] for s in active_24 if s["knm"] > 0) / len([s for s in active_24 if s["knm"] > 0]), 1) if any(s["knm"] > 0 for s in active_24) else 0.0
    avg_ta_24 = round(sum(s["ta"] for s in active_24 if s["ta"] > 0) / len([s for s in active_24 if s["ta"] > 0]), 1) if any(s["ta"] > 0 for s in active_24) else 0.0

    classes_24 = sorted(list(set(s["class"] for s in ks24)))
    class_stats_24 = {}
    for c in classes_24:
        c_studs = [s for s in ks24 if s["class"] == c]
        c_act = [s for s in c_studs if not s["is_absent"]]
        c_pass = [s for s in c_studs if s["is_pass"] and not s["is_absent"]]
        c_ready = [s for s in c_studs if s["tier"] in [2, 3]]
        class_stats_24[c] = {
            "total": len(c_studs), "took": len(c_act), "pass": len(c_pass),
            "pass_pct": round(len(c_pass) / len(c_studs) * 100, 1) if c_studs else 0.0,
            "ready": len(c_ready), "ready_pct": round(len(c_ready) / len(c_studs) * 100, 1) if c_studs else 0.0,
            "avg_final": round(sum(s["final_10"] for s in c_act) / len(c_act), 2) if c_act else 0.0,
            "avg_sp": round(sum(s["sp"] for s in c_act) / len(c_act), 1) if c_act else 0.0,
            "avg_vd": round(sum(s["vd"] for s in c_act) / len(c_act), 1) if c_act else 0.0,
            "avg_th": round(sum(s["th"] for s in c_act) / len(c_act), 1) if c_act else 0.0,
            "avg_tn": round(sum(s["tn"] for s in c_act) / len(c_act), 1) if c_act else 0.0,
        }

    diag_counts_24 = {
        "silent": len([s for s in ks24 if "Vững Thực hành Kỹ thuật" in s["persona"]]),
        "shifter": len([s for s in ks24 if "Thế mạnh Giao tiếp" in s["persona"]]),
        "allround": len([s for s in ks24 if "Đạt Chuẩn Năng lực Toàn diện" in s["persona"]]),
        "atrisk": len([s for s in ks24 if "Chưa đạt Chuẩn Kiến thức" in s["persona"]]),
        "mid": len([s for s in ks24 if "Đạt Mức Trung bình Cơ bản" in s["persona"]]),
        "absent": len([s for s in ks24 if s["is_absent"]])
    }

    class_rows_24 = ""
    for c, st in class_stats_24.items():
        class_rows_24 += f"""
        <tr>
            <td style="text-align:left;font-weight:700;color:#fff;">{c}</td>
            <td>{st['total']} SV</td>
            <td>{st['took']} SV</td>
            <td><strong style="color:var(--color-ks24);font-size:0.95rem;">{st['avg_final']}/10</strong></td>
            <td>{st['avg_sp']}</td>
            <td>{st['avg_vd']}</td>
            <td>{st['avg_th']}</td>
            <td>{st['avg_tn']}</td>
            <td><span class="badge pass">{st['pass']} SV ({st['pass_pct']}%)</span></td>
            <td><strong style="color:#34d399;">{st['ready']} SV ({st['ready_pct']}%)</strong></td>
        </tr>
        """

    tbody_rows_24 = ""
    for idx, s in enumerate(ks24):
        p_badge = f'<span class="badge {s["persona_cls"]}">{s["persona"]}</span>'
        tier_badge = f'<span class="badge lvl-{s["tier"]}">{s["tier_label"].split(" (")[0]}</span>'
        sc_color = "#34d399" if s['final_10'] >= 8.0 else ("#60a5fa" if s['final_10'] >= 6.0 else ("#fbbf24" if s['final_10'] >= 4.0 else "#fb7185"))
        tbody_rows_24 += f"""
        <tr class="student-row" data-name="{s['name'].lower()}" data-class="{s['class']}" data-tier="{s['tier']}" data-persona="{s['persona']}">
            <td>{idx+1}</td>
            <td style="text-align:left;font-weight:600;color:#fff;">{s['name']}</td>
            <td style="text-align:left;color:var(--text-muted);">{s['class']}</td>
            <td><strong style="color:{sc_color};font-size:1.05rem;">{s['final_10']}</strong></td>
            <td>{s['sp']}</td>
            <td>{s['vd']}</td>
            <td>{s['th']}</td>
            <td>{s['tn']}</td>
            <td>{s['knm']}</td>
            <td>{f"{s['ta']:.0f}" if s['ta'] > 0 else '<span style="color:var(--text-dim);">-</span>'}</td>
            <td>{tier_badge}</td>
            <td style="text-align:left;">{p_badge}</td>
            <td style="text-align:left;font-size:0.77rem;color:var(--text-muted);max-width:280px;line-height:1.4;">{s['action_plan']}</td>
        </tr>
        """

    html_ks24 = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Báo Cáo ĐGNL Khóa KS24 CNTT (Java / Spring Boot) | Rikkei Education</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        {base_css_24}
        {curric_css}
    </style>
</head>
<body>

    <header class="header">
        <div class="header-inner">
            <div class="logo-wrap">
                <div class="logo-badge" style="background:linear-gradient(135deg, #10b981, #059669);">KS24</div>
                <div>
                    <div class="logo-title">Báo Cáo ĐGNL Khóa KS24 CNTT (Java / Spring Boot)</div>
                    <div class="logo-sub">Đánh Giá Nghiệm Thu Cuối Kỳ III – Chuẩn Bị Tốt Nghiệp &amp; Tuyển Dụng Doanh Nghiệp</div>
                </div>
            </div>
            <div class="header-meta">
                Ban Giám Đốc Đào Tạo &amp; Hội Đồng Chuyên Môn<br>
                Cập nhật: 02/09/2026
            </div>
        </div>
    </header>

    <div class="container">

        <!-- NAV TABS -->
        <div class="nav-tabs-wrapper">
            <button class="nav-tab-btn active" onclick="switchTab('tab1', event)">📊 Tổng Quan &amp; Lớp Học</button>
            <button class="nav-tab-btn" onclick="switchTab('tab2', event)">🔬 Phân Môn &amp; Điều Chỉnh Kỳ IV/V</button>
            <button class="nav-tab-btn" onclick="switchTab('tab3', event)">🎯 Chẩn Đoán Năng Lực</button>
            <button class="nav-tab-btn" onclick="switchTab('tab4', event)">📋 Danh Bạ Học Viên</button>
        </div>

        <!-- Master KPI Strip -->
        <div class="kpi-grid">
            <div class="kpi-card" style="--kpi-accent: #10b981;">
                <div class="kpi-label">Sĩ Số Đăng Ký</div>
                <div class="kpi-value">{total_reg_24}</div>
                <div class="kpi-sub">5 Lớp (HN: 4, HCM: 1)</div>
            </div>
            <div class="kpi-card" style="--kpi-accent: #34d399;">
                <div class="kpi-label">Dự Thi Thực Tế</div>
                <div class="kpi-value">{took_24}</div>
                <div class="kpi-sub">Tỷ lệ: {round(took_24/total_reg_24*100, 1)}%</div>
            </div>
            <div class="kpi-card" style="--kpi-accent: #10b981;">
                <div class="kpi-label">Điểm TB Final</div>
                <div class="kpi-value">{avg_final_24}/10</div>
                <div class="kpi-sub">Thang điểm 10 quy đổi</div>
            </div>
            <div class="kpi-card" style="--kpi-accent: #8b5cf6;">
                <div class="kpi-label">Chuẩn Đầu Ra (L2+L3)</div>
                <div class="kpi-value">{ready_24}</div>
                <div class="kpi-sub">Tỷ lệ: {ready_pct_24}%</div>
            </div>
            <div class="kpi-card" style="--kpi-accent: #06b6d4;">
                <div class="kpi-label">Điểm TB Kỹ Năng Mềm</div>
                <div class="kpi-value">{avg_knm_24}</div>
                <div class="kpi-sub">Thang điểm 100</div>
            </div>
            <div class="kpi-card" style="--kpi-accent: #3b82f6;">
                <div class="kpi-label">Điểm TB Tiếng Anh</div>
                <div class="kpi-value">{avg_ta_24:.0f}</div>
                <div class="kpi-sub">Chuẩn TOEIC / 990</div>
            </div>
        </div>

        <!-- TAB 1: TỔNG QUAN -->
        <div id="tab1" class="tab-pane active">
            <div class="bento-card">
                <div class="section-title">🏫 Bảng Thống Kê Theo Lớp Học (KS24)</div>
                <div class="table-wrapper" style="margin-top:1rem;">
                    <table class="data-table">
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
                            {class_rows_24}
                        </tbody>
                    </table>
                </div>
            </div>

            <div style="display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;margin-bottom:2rem;">
                <div class="bento-card">
                    <div class="section-title" style="font-size:1rem;margin-bottom:1rem;">📊 Điểm TB Theo Cơ Sở (HN vs HCM)</div>
                    <div style="height:230px;position:relative;">
                        <canvas id="branchChart24"></canvas>
                    </div>
                </div>
                <div class="bento-card">
                    <div class="section-title" style="font-size:1rem;margin-bottom:1rem;">📈 Phân Bố Mức Độ Năng Lực KS24</div>
                    <div style="height:230px;position:relative;">
                        <canvas id="tierDistChart24"></canvas>
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 2: PHÂN MÔN & ĐIỀU CHỈNH KỲ IV/V -->
        <div id="tab2" class="tab-pane">
            
            <!-- Ma Trận Trọng Số Card -->
            <div class="bento-card">
                <div class="section-title">🔬 Ma Trận Trọng Số Đề Thi KS24</div>
                <div style="display:grid;grid-template-columns:repeat(4, 1fr);gap:1rem;margin-top:1rem;">
                    <div style="background:var(--bg-surface);padding:1.15rem;border-radius:var(--radius-md);border:1px solid var(--border-subtle);">
                        <div style="font-size:0.7rem;color:var(--text-dim);text-transform:uppercase;font-weight:700;">1. Đồ Án / Sản Phẩm (30% HN)</div>
                        <div style="font-family:var(--font-heading);font-size:1.6rem;font-weight:800;color:var(--color-ks24);margin:0.25rem 0;">54.4 / 100</div>
                        <div style="font-size:0.76rem;color:var(--text-muted);">Fullstack Spring Boot &amp; ReactJS</div>
                    </div>
                    <div style="background:var(--bg-surface);padding:1.15rem;border-radius:var(--radius-md);border:1px solid var(--border-subtle);">
                        <div style="font-size:0.7rem;color:var(--text-dim);text-transform:uppercase;font-weight:700;">2. Vấn Đáp (20% HN / 40% HCM)</div>
                        <div style="font-family:var(--font-heading);font-size:1.6rem;font-weight:800;color:#3b82f6;margin:0.25rem 0;">50.8 / 100</div>
                        <div style="font-size:0.76rem;color:var(--text-muted);">Phỏng vấn trực tiếp trước Hội đồng</div>
                    </div>
                    <div style="background:var(--bg-surface);padding:1.15rem;border-radius:var(--radius-md);border:1px solid var(--border-subtle);">
                        <div style="font-size:0.7rem;color:var(--text-dim);text-transform:uppercase;font-weight:700;">3. Thực Hành (10% HN / 12% HCM)</div>
                        <div style="font-family:var(--font-heading);font-size:1.6rem;font-weight:800;color:#fbbf24;margin:0.25rem 0;">62.7 / 100</div>
                        <div style="font-size:0.76rem;color:var(--text-muted);">Viết code API Spring Boot &amp; Debug</div>
                    </div>
                    <div style="background:var(--bg-surface);padding:1.15rem;border-radius:var(--radius-md);border:1px solid var(--border-subtle);">
                        <div style="font-size:0.7rem;color:var(--text-dim);text-transform:uppercase;font-weight:700;">4. Trắc Nghiệm (40% HN / 48% HCM)</div>
                        <div style="font-family:var(--font-heading);font-size:1.6rem;font-weight:800;color:#a78bfa;margin:0.25rem 0;">72.2 / 100</div>
                        <div style="font-size:0.76rem;color:var(--text-muted);">Lý thuyết OOP, Spring Core, SQL</div>
                    </div>
                </div>
            </div>

            <!-- CURRICULUM BENTO GRID KS24 -->
            <div class="bento-card" style="border-top:3px solid var(--color-ks24);">
                <div class="section-title">🏛️ Chi Tiết Điều Chỉnh Từng Môn Học Kỳ IV (Dựa Trên Lỗ Hổng ĐGNL Lần 1)</div>
                
                <div style="display:grid;grid-template-columns:repeat(3, 1fr);gap:1.25rem;margin-top:1.25rem;">
                    
                    <div class="decision-card">
                        <div class="decision-card-top">
                            <span class="subject-name-tag">Microservices System <span class="code-chip">IT214 • 2.5 TC</span></span>
                            <span class="status-badge upgrade">Cải Tiến Lõi</span>
                        </div>
                        <div class="gap-block">
                            <strong>⚠️ Lỗ hổng ĐGNL:</strong> 53.8% SV trượt tranh chấp dữ liệu; hổng bảo mật IDOR qua Gateway.
                        </div>
                        <div class="action-block">
                            <ul class="action-list green">
                                <li><strong>Bridge 2 buổi đầu:</strong> Củng cố <code>@Transactional</code> &amp; <strong>Pessimistic/Optimistic Locking JPA</strong>.</li>
                                <li><strong>Token Propagation:</strong> Feign Client Interceptor truyền JWT qua Gateway chống IDOR.</li>
                                <li><strong>Modern Tracing:</strong> Tích hợp <strong>Micrometer + OpenTelemetry + Grafana Tempo</strong> (Spring Boot 3+).</li>
                                <li><strong>Tối ưu Docker:</strong> Tái sử dụng Docker Compose từ môn DevOps IT209.</li>
                            </ul>
                        </div>
                    </div>

                    <div class="decision-card">
                        <div class="decision-card-top">
                            <span class="subject-name-tag">DevOps Fundamentals <span class="code-chip">IT209 • 1.9 TC</span></span>
                            <span class="status-badge newmod">DevSecOps</span>
                        </div>
                        <div class="gap-block">
                            <strong>⚠️ Lỗ hổng ĐGNL:</strong> Thiếu công cụ kiểm tra an ninh tĩnh &amp; giám sát tài nguyên VPS.
                        </div>
                        <div class="action-block">
                            <ul class="action-list green">
                                <li><strong>Lightweight DevSecOps:</strong> Quét lỗ hổng tĩnh bằng <strong>Semgrep / Snyk</strong> trên GitHub Actions.</li>
                                <li><strong>PLG Observability:</strong> Setup <strong>Prometheus + Loki + Grafana</strong> (thay thế ELK Stack dễ gây tràn RAM).</li>
                                <li><strong>DB Migration:</strong> Tự động hóa cập nhật schema bằng Flyway / Liquibase.</li>
                            </ul>
                        </div>
                    </div>

                    <div class="decision-card">
                        <div class="decision-card-top">
                            <span class="subject-name-tag">AI Integration <span class="code-chip">IT213 • 1.9 TC</span></span>
                            <span class="status-badge upgrade">GenAI Agent</span>
                        </div>
                        <div class="gap-block">
                            <strong>⚠️ Xu hướng mới:</strong> Chi phí gọi API LLM cao và yêu cầu xử lý Agent dạng đồ thị.
                        </div>
                        <div class="action-block">
                            <ul class="action-list green">
                                <li><strong>Semantic Caching:</strong> Dùng RedisVL / GPTCache giảm 80% chi phí API.</li>
                                <li><strong>Advanced AI Agents:</strong> Xây dựng Agent đồ thị đa tác vụ với <strong>LangGraph / CrewAI</strong>.</li>
                                <li><strong>SSE Streaming:</strong> Server-Sent Events stream câu trả lời về ReactJS.</li>
                            </ul>
                        </div>
                    </div>

                </div>

                <!-- ELECTIVES MASTER BANNER FOR KS24 -->
                <div class="electives-master-banner" style="margin-top:1.5rem;">
                    <div class="electives-banner-header">
                        <div class="electives-banner-title">
                            <span>🌟</span> KHUYẾN NGHỊ 2 MÔN HỌC TỰ CHỌN MỚI Ở KỲ V (MỞ RỘNG VIỆC LÀM)
                        </div>
                        <span class="status-badge upgrade">Mở Rộng Vị Trí Tuyển Dụng</span>
                    </div>
                    <div style="display:grid;grid-template-columns:1fr 1fr;gap:1.25rem;">
                        <div class="elective-card-box">
                            <div>
                                <span class="elective-target-role">🎯 Vị trí: Data Analyst / BI Developer</span>
                                <div class="elective-card-name">1. Python &amp; Data Analytics Fundamentals</div>
                                <p class="elective-card-desc">
                                    Xử lý dữ liệu với Pandas/NumPy, SQL nâng cao và xây dựng Dashboard tương tác bằng Power BI.
                                </p>
                            </div>
                            <div class="elective-skills-tag">
                                <span>Pandas</span> • <span>SQL Analytics</span> • <span>Power BI</span>
                            </div>
                        </div>

                        <div class="elective-card-box">
                            <div>
                                <span class="elective-target-role">🎯 Vị trí: Cloud / DevOps / SRE Engineer</span>
                                <div class="elective-card-name">2. Cloud Native &amp; Kubernetes Scaling</div>
                                <p class="elective-card-desc">
                                    Thực hành chuyên sâu dịch vụ Cloud AWS (EC2/S3/RDS) và điều phối Container với Kubernetes (K8s).
                                </p>
                            </div>
                            <div class="elective-skills-tag">
                                <span>AWS Cloud</span> • <span>Kubernetes (K8s)</span> • <span>Docker</span>
                            </div>
                        </div>
                    </div>
                </div>

            </div>

        </div>

        <!-- TAB 3: CHẨN ĐOÁN -->
        <div id="tab3" class="tab-pane">
            <div class="bento-card">
                <div class="section-title">🎯 Ma Trận Chẩn Đoán Năng Lực KS24</div>
                <div class="section-desc" style="margin-bottom:1.25rem;">
                    Click vào thẻ bất kỳ để lọc danh bạ học viên tương ứng:
                </div>

                <div style="display:grid;grid-template-columns:repeat(4, 1fr);gap:1.25rem;">
                    <div class="decision-card" onclick="quickFilterDiag('Vững Thực hành Kỹ thuật')" style="cursor:pointer;border-top:3px solid var(--color-danger);">
                        <div style="display:flex;justify-content:space-between;align-items:center;">
                            <strong style="color:#fb7185;font-size:0.88rem;">🔇 Vững Kỹ Thuật - Yếu Vấn Đáp</strong>
                            <span style="font-family:var(--font-heading);font-weight:800;font-size:1.2rem;color:#fff;">{diag_counts_24['silent']} SV</span>
                        </div>
                        <p style="font-size:0.76rem;color:var(--text-muted);margin-top:0.4rem;line-height:1.4;">
                            Code &ge; 65đ, Vấn đáp &lt; 50đ &rarr; <span style="color:#fecdd3;font-weight:600;">Mock Interview 1-on-1</span>
                        </p>
                    </div>

                    <div class="decision-card" onclick="quickFilterDiag('Thế mạnh Giao tiếp')" style="cursor:pointer;border-top:3px solid var(--color-warning);">
                        <div style="display:flex;justify-content:space-between;align-items:center;">
                            <strong style="color:#fbbf24;font-size:0.88rem;">🗣️ Thế Mạnh KNM - Hạn Chế Code</strong>
                            <span style="font-family:var(--font-heading);font-weight:800;font-size:1.2rem;color:#fff;">{diag_counts_24['shifter']} SV</span>
                        </div>
                        <p style="font-size:0.76rem;color:var(--text-muted);margin-top:0.4rem;line-height:1.4;">
                            KNM &ge; 75đ, Code &lt; 50đ &rarr; <span style="color:#fde68a;font-weight:600;">Phân Luồng BA / QA / Sales</span>
                        </p>
                    </div>

                    <div class="decision-card" onclick="quickFilterDiag('Đạt Chuẩn Năng lực Toàn diện')" style="cursor:pointer;border-top:3px solid var(--color-success);">
                        <div style="display:flex;justify-content:space-between;align-items:center;">
                            <strong style="color:#34d399;font-size:0.88rem;">🌟 Đạt Chuẩn Toàn Diện</strong>
                            <span style="font-family:var(--font-heading);font-weight:800;font-size:1.2rem;color:#fff;">{diag_counts_24['allround']} SV</span>
                        </div>
                        <p style="font-size:0.76rem;color:var(--text-muted);margin-top:0.4rem;line-height:1.4;">
                            Vững cả Kỹ thuật lẫn Vấn đáp &rarr; <span style="color:#a7f3d0;font-weight:600;">Doanh nghiệp Onsite / FDI</span>
                        </p>
                    </div>

                    <div class="decision-card" onclick="quickFilterDiag('Chưa đạt Chuẩn Kiến thức Cốt lõi')" style="cursor:pointer;border-top:3px solid var(--border-focus);">
                        <div style="display:flex;justify-content:space-between;align-items:center;">
                            <strong style="color:#e4e4e7;font-size:0.88rem;">⚠️ Cần Phụ Đạo / Trung Gian</strong>
                            <span style="font-family:var(--font-heading);font-weight:800;font-size:1.2rem;color:#fff;">{diag_counts_24['atrisk'] + diag_counts_24['mid']} SV</span>
                        </div>
                        <p style="font-size:0.76rem;color:var(--text-muted);margin-top:0.4rem;line-height:1.4;">
                            Củng cố Java Core &amp; Spring Boot 3 tuần
                        </p>
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
                    {''.join([f'<option value="{c}">{c}</option>' for c in classes_24])}
                </select>
                <select id="tierFilter" class="filter-select" onchange="applyFilters()">
                    <option value="">-- Mức Độ Năng Lực --</option>
                    <option value="3">Mức 3: Làm Chủ Tốt</option>
                    <option value="2">Mức 2: Đạt Chuẩn Doanh Nghiệp</option>
                    <option value="1">Mức 1: Đạt Cơ Bản / Cần Bổ Trợ</option>
                    <option value="0">Mức 0: Chưa Đạt / Vắng Thi</option>
                </select>
                <select id="personaFilter" class="filter-select" onchange="applyFilters()">
                    <option value="">-- Chẩn Đoán Năng Lực --</option>
                    <option value="Vững Thực hành Kỹ thuật">🔇 Vững Kỹ thuật - Yếu Vấn đáp ({diag_counts_24['silent']} SV)</option>
                    <option value="Thế mạnh Giao tiếp">🗣️ Thế mạnh KNM - Hạn chế Code ({diag_counts_24['shifter']} SV)</option>
                    <option value="Đạt Chuẩn Năng lực Toàn diện">🌟 Đạt Chuẩn Toàn diện ({diag_counts_24['allround']} SV)</option>
                    <option value="Chưa đạt Chuẩn Kiến thức Cốt lõi">🚨 Cần Phụ đạo Kiến thức ({diag_counts_24['atrisk']} SV)</option>
                    <option value="Đạt Mức Trung bình Cơ bản">🔷 Mức Trung bình Cơ bản ({diag_counts_24['mid']} SV)</option>
                    <option value="Vắng thi">⚪ Vắng thi / Chưa có bài ({diag_counts_24['absent']} SV)</option>
                </select>
            </div>

            <div class="bento-card">
                <div class="section-title">
                    <span>📋 Danh Bạ Khảo Thí &amp; Kế Hoạch Can Thiệp (<span id="recCount">{len(ks24)}</span> SV)</span>
                </div>
                <div class="table-wrapper" style="margin-top:1rem;">
                    <table class="data-table" id="studentTable">
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
                                <th>Chẩn Đoán</th>
                                <th>Kế Hoạch Can Thiệp</th>
                            </tr>
                        </thead>
                        <tbody id="studentTableBody">
                            {tbody_rows_24}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <div class="footer-bar">
            <div>Phòng Chuyên Môn &amp; Khảo Thí Đào Tạo | PTIT Rikkei Education</div>
            <div><a href="Executive_Summary_DGNL_Report.html">📑 Về Báo Cáo Tổng Hợp Ban Giám Đốc</a></div>
        </div>

    </div>

    <script>
    function switchTab(tabId, evt) {{
        document.querySelectorAll('.tab-pane').forEach(el => el.classList.remove('active'));
        document.querySelectorAll('.nav-tab-btn').forEach(el => el.classList.remove('active'));
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

    const ctx1 = document.getElementById('branchChart24').getContext('2d');
    new Chart(ctx1, {{
        type: 'bar',
        data: {{
            labels: ['📍 Cơ sở Hà Nội (HN-KS24)', '📍 Cơ sở TP.HCM (HCM-KS24)'],
            datasets: [{{
                label: 'Điểm TB Final (/10)',
                data: [{round(sum(s['final_10'] for s in ks24 if 'HN' in s['class'] and not s['is_absent'])/len([s for s in ks24 if 'HN' in s['class'] and not s['is_absent']]), 2)},
                       {round(sum(s['final_10'] for s in ks24 if 'HCM' in s['class'] and not s['is_absent'])/len([s for s in ks24 if 'HCM' in s['class'] and not s['is_absent']]), 2)}],
                backgroundColor: ['rgba(16,185,129,0.7)', 'rgba(59,130,246,0.7)'],
                borderColor: ['#10b981', '#3b82f6'],
                borderWidth: 1.5, borderRadius: 6
            }}]
        }},
        options: {{
            responsive: true, maintainAspectRatio: false,
            plugins: {{ legend: {{ display: false }} }},
            scales: {{
                y: {{ beginAtZero: true, max: 10, grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ color: '#94a3b8' }} }},
                x: {{ grid: {{ display: false }}, ticks: {{ color: '#94a3b8' }} }}
            }}
        }}
    }});

    const ctx2 = document.getElementById('tierDistChart24').getContext('2d');
    new Chart(ctx2, {{
        type: 'doughnut',
        data: {{
            labels: ['Mức 3 - Làm Chủ Tốt', 'Mức 2 - Chuẩn Doanh Nghiệp', 'Mức 1 - Cơ Bản', 'Mức 0 - Chưa Đạt / Vắng'],
            datasets: [{{
                data: [
                    {len([s for s in ks24 if s['tier']==3])},
                    {len([s for s in ks24 if s['tier']==2])},
                    {len([s for s in ks24 if s['tier']==1])},
                    {len([s for s in ks24 if s['tier']==0])}
                ],
                backgroundColor: ['#10b981', '#3b82f6', '#f59e0b', '#f43f5e'],
                borderWidth: 2, borderColor: '#171820'
            }}]
        }},
        options: {{
            responsive: true, maintainAspectRatio: false,
            cutout: '70%',
            plugins: {{ legend: {{ labels: {{ color: '#94a3b8', font: {{ size: 10 }} }} }} }}
        }}
    }});
    </script>
</body>
</html>
"""
    with open("outputs/KS24_DGNL_Report.html", "w", encoding="utf-8") as f:
        f.write(html_ks24)
    print("Updated outputs/KS24_DGNL_Report.html v7!")


    # ════════════════════════════════════════════════════════════════════════
    # 2. KS25 REPORT
    # ════════════════════════════════════════════════════════════════════════
    ks25 = data["ks25"]
    total_reg_25 = len(ks25)
    active_25 = [s for s in ks25 if not s["is_absent"]]
    took_25 = len(active_25)
    ready_25 = len([s for s in ks25 if s["tier"] in [2, 3]])
    ready_pct_25 = round(ready_25 / total_reg_25 * 100, 1) if total_reg_25 else 0.0
    avg_final_25 = round(sum(s["final_10"] for s in active_25) / took_25, 2) if took_25 else 0.0
    avg_knm_25 = round(sum(s["knm"] for s in active_25 if s["knm"] > 0) / len([s for s in active_25 if s["knm"] > 0]), 1) if any(s["knm"] > 0 for s in active_25) else 0.0
    avg_ta_25 = round(sum(s["ta"] for s in active_25 if s["ta"] > 0) / len([s for s in active_25 if s["ta"] > 0]), 1) if any(s["ta"] > 0 for s in active_25) else 0.0

    classes_25 = sorted(list(set(s["class"] for s in ks25)))
    class_stats_25 = {}
    for c in classes_25:
        c_studs = [s for s in ks25 if s["class"] == c]
        c_act = [s for s in c_studs if not s["is_absent"]]
        c_pass = [s for s in c_studs if s["is_pass"] and not s["is_absent"]]
        c_ready = [s for s in c_studs if s["tier"] in [2, 3]]
        class_stats_25[c] = {
            "total": len(c_studs), "took": len(c_act), "pass": len(c_pass),
            "pass_pct": round(len(c_pass) / len(c_studs) * 100, 1) if c_studs else 0.0,
            "ready": len(c_ready), "ready_pct": round(len(c_ready) / len(c_studs) * 100, 1) if c_studs else 0.0,
            "avg_final": round(sum(s["final_10"] for s in c_act) / len(c_act), 2) if c_act else 0.0,
            "avg_th": round(sum(s["th"] for s in c_act) / len(c_act), 1) if c_act else 0.0,
            "avg_tn": round(sum(s["tn"] for s in c_act) / len(c_act), 1) if c_act else 0.0,
        }

    diag_counts_25 = {
        "solid": len([s for s in ks25 if "Nắm vững Năng lực Thực hành" in s["persona"]]),
        "rote": len([s for s in ks25 if "Nắm vững Lý thuyết - Hạn chế" in s["persona"]]),
        "baqa": len([s for s in ks25 if "Thế mạnh Giao tiếp" in s["persona"]]),
        "atrisk": len([s for s in ks25 if "Chưa đạt Chuẩn Kiến thức" in s["persona"]]),
        "mid": len([s for s in ks25 if "Đạt Mức Trung bình Cơ bản" in s["persona"]]),
        "absent": len([s for s in ks25 if s["is_absent"]])
    }

    class_rows_25 = ""
    for c, st in class_stats_25.items():
        class_rows_25 += f"""
        <tr>
            <td style="text-align:left;font-weight:700;color:#fff;">{c}</td>
            <td>{st['total']} SV</td>
            <td>{st['took']} SV</td>
            <td><strong style="color:var(--color-ks25);font-size:0.95rem;">{st['avg_final']}/10</strong></td>
            <td>{st['avg_th']}</td>
            <td>{st['avg_tn']}</td>
            <td><span class="badge pass">{st['pass']} SV ({st['pass_pct']}%)</span></td>
            <td><strong style="color:#34d399;">{st['ready']} SV ({st['ready_pct']}%)</strong></td>
        </tr>
        """

    tbody_rows_25 = ""
    for idx, s in enumerate(ks25):
        p_badge = f'<span class="badge {s["persona_cls"]}">{s["persona"]}</span>'
        tier_badge = f'<span class="badge lvl-{s["tier"]}">{s["tier_label"].split(" (")[0]}</span>'
        sc_color = "#34d399" if s['final_10'] >= 8.0 else ("#60a5fa" if s['final_10'] >= 6.0 else ("#fbbf24" if s['final_10'] >= 4.0 else "#fb7185"))
        tbody_rows_25 += f"""
        <tr class="student-row" data-name="{s['name'].lower()}" data-class="{s['class']}" data-tier="{s['tier']}" data-persona="{s['persona']}">
            <td>{idx+1}</td>
            <td style="text-align:left;font-weight:600;color:#fff;">{s['name']}</td>
            <td style="text-align:left;color:var(--text-muted);">{s['class']}</td>
            <td><strong style="color:{sc_color};font-size:1.05rem;">{s['final_10']}</strong></td>
            <td>{s['th']}</td>
            <td>{s['tn']}</td>
            <td>{s['knm']}</td>
            <td>{f"{s['ta']:.0f}" if s['ta'] > 0 else '<span style="color:var(--text-dim);">-</span>'}</td>
            <td>{tier_badge}</td>
            <td style="text-align:left;">{p_badge}</td>
            <td style="text-align:left;font-size:0.77rem;color:var(--text-muted);max-width:280px;line-height:1.4;">{s['action_plan']}</td>
        </tr>
        """

    html_ks25 = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Báo Cáo ĐGNL Khóa KS25 CNTT (FastAPI / Python) | Rikkei Education</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        {base_css_25}
        {curric_css}
    </style>
</head>
<body>

    <header class="header">
        <div class="header-inner">
            <div class="logo-wrap">
                <div class="logo-badge" style="background:linear-gradient(135deg, #3b82f6, #2563eb);">KS25</div>
                <div>
                    <div class="logo-title">Báo Cáo ĐGNL Khóa KS25 CNTT (FastAPI / Python)</div>
                    <div class="logo-sub">Đánh Giá Giữa Kỳ II – Chuẩn Bị Phân Tầng Học Thuật Chuyên Ngành Kỳ III</div>
                </div>
            </div>
            <div class="header-meta">
                Ban Giám Đốc Đào Tạo &amp; Hội Đồng Chuyên Môn<br>
                Cập nhật: 02/09/2026
            </div>
        </div>
    </header>

    <div class="container">

        <!-- NAV TABS -->
        <div class="nav-tabs-wrapper">
            <button class="nav-tab-btn active" onclick="switchTab('tab1', event)">📊 Tổng Quan &amp; Lớp Học</button>
            <button class="nav-tab-btn" onclick="switchTab('tab2', event)">🔬 Phân Môn &amp; Giảm Tải / Bồi Dưỡng Kỳ III</button>
            <button class="nav-tab-btn" onclick="switchTab('tab3', event)">🎯 Chẩn Đoán Năng Lực</button>
            <button class="nav-tab-btn" onclick="switchTab('tab4', event)">📋 Danh Bạ Học Viên</button>
        </div>

        <!-- Master KPI Strip -->
        <div class="kpi-grid">
            <div class="kpi-card" style="--kpi-accent: #3b82f6;">
                <div class="kpi-label">Sĩ Số Đăng Ký</div>
                <div class="kpi-value">{total_reg_25}</div>
                <div class="kpi-sub">12 Lớp (HN: 8, HCM: 4)</div>
            </div>
            <div class="kpi-card" style="--kpi-accent: #60a5fa;">
                <div class="kpi-label">Dự Thi Thực Tế</div>
                <div class="kpi-value">{took_25}</div>
                <div class="kpi-sub">Tỷ lệ: {round(took_25/total_reg_25*100, 1)}%</div>
            </div>
            <div class="kpi-card" style="--kpi-accent: #3b82f6;">
                <div class="kpi-label">Điểm TB Final</div>
                <div class="kpi-value">{avg_final_25}/10</div>
                <div class="kpi-sub">Thang điểm 10 quy đổi</div>
            </div>
            <div class="kpi-card" style="--kpi-accent: #8b5cf6;">
                <div class="kpi-label">Chuẩn Đầu Ra (L2+L3)</div>
                <div class="kpi-value">{ready_25}</div>
                <div class="kpi-sub">Tỷ lệ: {ready_pct_25}%</div>
            </div>
            <div class="kpi-card" style="--kpi-accent: #06b6d4;">
                <div class="kpi-label">Điểm TB Kỹ Năng Mềm</div>
                <div class="kpi-value">{avg_knm_25}</div>
                <div class="kpi-sub">Thang điểm 100</div>
            </div>
            <div class="kpi-card" style="--kpi-accent: #3b82f6;">
                <div class="kpi-label">Điểm TB Tiếng Anh</div>
                <div class="kpi-value">{avg_ta_25:.0f}</div>
                <div class="kpi-sub">Chuẩn TOEIC / 990</div>
            </div>
        </div>

        <!-- TAB 1: TỔNG QUAN -->
        <div id="tab1" class="tab-pane active">
            <div class="bento-card">
                <div class="section-title">🏫 Bảng Thống Kê Theo Lớp Học (KS25)</div>
                <div class="table-wrapper" style="margin-top:1rem;">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Mã Lớp</th>
                                <th>Sĩ Số</th>
                                <th>Dự Thi</th>
                                <th>Điểm TB Final</th>
                                <th>Thực Hành Code (70%)</th>
                                <th>Trắc Nghiệm (30%)</th>
                                <th>Tỷ Lệ Đạt</th>
                                <th>Chuẩn Đầu Ra</th>
                            </tr>
                        </thead>
                        <tbody>
                            {class_rows_25}
                        </tbody>
                    </table>
                </div>
            </div>

            <div style="display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;margin-bottom:2rem;">
                <div class="bento-card">
                    <div class="section-title" style="font-size:1rem;margin-bottom:1rem;">📊 Điểm TB Theo Cơ Sở (HN vs HCM)</div>
                    <div style="height:230px;position:relative;">
                        <canvas id="branchChart25"></canvas>
                    </div>
                </div>
                <div class="bento-card">
                    <div class="section-title" style="font-size:1rem;margin-bottom:1rem;">📈 Phân Bố Mức Độ Năng Lực KS25</div>
                    <div style="height:230px;position:relative;">
                        <canvas id="tierDistChart25"></canvas>
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 2: PHÂN MÔN & GIẢM TẢI / BỒI DƯỠNG KỲ III -->
        <div id="tab2" class="tab-pane">
            
            <!-- Ma Trận Trọng Số Card -->
            <div class="bento-card">
                <div class="section-title">🔬 Ma Trận Trọng Số Đề Thi KS25</div>
                <div style="display:grid;grid-template-columns:repeat(2, 1fr);gap:1.25rem;margin-top:1rem;">
                    <div style="background:var(--bg-surface);padding:1.25rem;border-radius:var(--radius-md);border:1px solid var(--border-subtle);">
                        <div style="font-size:0.72rem;color:var(--text-dim);text-transform:uppercase;font-weight:700;">1. Thực Hành Viết Code API (Trọng số 70%)</div>
                        <div style="font-family:var(--font-heading);font-size:1.8rem;font-weight:800;color:var(--color-ks25);margin:0.25rem 0;">29.0 / 100</div>
                        <div style="font-size:0.8rem;color:var(--text-muted);line-height:1.45;">
                            Thời gian: 120 phút. Xây dựng hoàn chỉnh Backend API 4 lớp (Router, Schema, Service, Repository) kết nối PostgreSQL với FastAPI.
                        </div>
                    </div>
                    <div style="background:var(--bg-surface);padding:1.25rem;border-radius:var(--radius-md);border:1px solid var(--border-subtle);">
                        <div style="font-size:0.72rem;color:var(--text-dim);text-transform:uppercase;font-weight:700;">2. Trắc Nghiệm Chuyên Ngành (Trọng số 30%)</div>
                        <div style="font-family:var(--font-heading);font-size:1.8rem;font-weight:800;color:#a78bfa;margin:0.25rem 0;">65.6 / 100</div>
                        <div style="font-size:0.8rem;color:var(--text-muted);line-height:1.45;">
                            Đánh giá kiến thức lý thuyết: Python Core, Asynchronous, Dependency Injection, Validation Pydantic, HTTP Status Codes.
                        </div>
                    </div>
                </div>
            </div>

            <!-- CURRICULUM BENTO GRID KS25 -->
            <div class="bento-card" style="border-top:3px solid var(--color-ks25);">
                <div class="section-title">🏛️ Chi Tiết Giảm Tải Học Thuật &amp; Bồi Dưỡng Thực Chiến Kỳ III (KS25)</div>
                
                <div style="display:grid;grid-template-columns:repeat(2, 1fr);gap:1.25rem;margin-top:1.25rem;">
                    
                    <div class="decision-card">
                        <div class="decision-card-top">
                            <span class="subject-name-tag">Phân Tích Thiết Kế &amp; Agile <span class="code-chip">IT105/106</span></span>
                            <span class="status-badge reduce">Giảm Tải Sơ Đồ</span>
                        </div>
                        <div class="gap-block">
                            <strong>⚠️ Lỗ hổng ĐGNL:</strong> 151 SV điểm trắc nghiệm cao nhưng không biết chuyển sơ đồ thành code.
                        </div>
                        <div class="action-block">
                            <ul class="action-list blue">
                                <li><strong>Cắt bỏ vẽ sơ đồ suông:</strong> Chuyển 100% sang mô hình <strong>Design-to-Code</strong>.</li>
                                <li><strong>Thiết kế gắn liền API:</strong> Vẽ Schema ERD &rarr; Chuyển thành Pydantic Schema / SQLAlchemy Models trên FastAPI.</li>
                                <li><strong>Agile thực chiến:</strong> Chia Sprint trên Jira/Trello và push code GitHub.</li>
                            </ul>
                        </div>
                    </div>

                    <div class="decision-card">
                        <div class="decision-card-top">
                            <span class="subject-name-tag">FastAPI Live-Coding <span class="code-chip">2 Tuần Đầu Kỳ III</span></span>
                            <span class="status-badge upgrade">Bồi Dưỡng Cấp Tốc</span>
                        </div>
                        <div class="gap-block">
                            <strong>⚠️ Lỗ hổng ĐGNL:</strong> Điểm thực hành TB chỉ 29.0/100; học viên thiếu phản xạ viết API độc lập.
                        </div>
                        <div class="action-block">
                            <ul class="action-list blue">
                                <li><strong>Project Skeleton Chuẩn:</strong> Cung cấp khung code có sẵn Router/Repo để rèn phản xạ.</li>
                                <li><strong>Tái cấu trúc kiểm tra:</strong> Live-Coding <strong>70%</strong>, Trắc nghiệm <strong>15%</strong>, Vấn đáp <strong>15%</strong>.</li>
                            </ul>
                        </div>
                    </div>

                    <div class="decision-card" style="border-left:3px solid var(--color-ks25);">
                        <div class="decision-card-top">
                            <span class="subject-name-tag" style="color:#60a5fa;">Frontend Framework <span class="code-chip">ReactJS / NextJS</span></span>
                            <span class="status-badge newmod">Bổ Sung Bắt Buộc</span>
                        </div>
                        <div class="gap-block">
                            <strong>⚠️ Khoảng trống CTĐT:</strong> KS25 thiếu hoàn toàn Frontend nâng cao &rarr; Không thể làm đồ án Fullstack.
                        </div>
                        <div class="action-block">
                            <ul class="action-list blue">
                                <li><strong>Bổ sung gấp ở Kỳ III:</strong> Dạy ReactJS Hooks, TailwindCSS và NextJS App Router để hoàn thiện ứng dụng <strong>Fullstack Web/AI</strong>.</li>
                            </ul>
                        </div>
                    </div>

                    <div class="decision-card">
                        <div class="decision-card-top">
                            <span class="subject-name-tag">Applied DSA &amp; DB <span class="code-chip">Kỳ III</span></span>
                            <span class="status-badge upgrade">Nền Tảng AI</span>
                        </div>
                        <div class="gap-block">
                            <strong>⚠️ Nền tảng:</strong> Cần vững tối ưu truy vấn trước khi học Machine Learning Kỳ IV.
                        </div>
                        <div class="action-block">
                            <ul class="action-list blue">
                                <li><strong>Tối ưu hóa DB:</strong> Indexing PostgreSQL, Query Profiling &amp; Thuật toán cơ bản.</li>
                            </ul>
                        </div>
                    </div>

                </div>
            </div>

        </div>

        <!-- TAB 3: CHẨN ĐOÁN -->
        <div id="tab3" class="tab-pane">
            <div class="bento-card">
                <div class="section-title">🎯 Ma Trận Chẩn Đoán Năng Lực KS25</div>
                <div class="section-desc" style="margin-bottom:1.25rem;">
                    Click vào thẻ bất kỳ để lọc danh bạ học viên tương ứng:
                </div>

                <div style="display:grid;grid-template-columns:repeat(4, 1fr);gap:1.25rem;">
                    <div class="decision-card" onclick="quickFilterDiag('Nắm vững Lý thuyết')" style="cursor:pointer;border-top:3px solid var(--color-danger);">
                        <div style="display:flex;justify-content:space-between;align-items:center;">
                            <strong style="color:#fb7185;font-size:0.88rem;">🚨 Nắm Lý Thuyết - Hổng Code TH</strong>
                            <span style="font-family:var(--font-heading);font-weight:800;font-size:1.2rem;color:#fff;">{diag_counts_25['rote']} SV</span>
                        </div>
                        <p style="font-size:0.76rem;color:var(--text-muted);margin-top:0.4rem;line-height:1.4;">
                            TN &ge; 65đ, TH &lt; 50đ &rarr; <span style="color:#fecdd3;font-weight:600;">FastAPI Bootcamp 2 tuần</span>
                        </p>
                    </div>

                    <div class="decision-card" onclick="quickFilterDiag('Nắm vững Năng lực Thực hành')" style="cursor:pointer;border-top:3px solid var(--color-success);">
                        <div style="display:flex;justify-content:space-between;align-items:center;">
                            <strong style="color:#34d399;font-size:0.88rem;">💻 Vững Thực Hành Lập Trình</strong>
                            <span style="font-family:var(--font-heading);font-weight:800;font-size:1.2rem;color:#fff;">{diag_counts_25['solid']} SV</span>
                        </div>
                        <p style="font-size:0.76rem;color:var(--text-muted);margin-top:0.4rem;line-height:1.4;">
                            TH &ge; 50đ &rarr; <span style="color:#a7f3d0;font-weight:600;">Lộ trình DSA / AI / RAG Kỳ III</span>
                        </p>
                    </div>

                    <div class="decision-card" onclick="quickFilterDiag('Thế mạnh Giao tiếp')" style="cursor:pointer;border-top:3px solid var(--color-warning);">
                        <div style="display:flex;justify-content:space-between;align-items:center;">
                            <strong style="color:#fbbf24;font-size:0.88rem;">📋 Tiềm Năng BA / QA Sớm</strong>
                            <span style="font-family:var(--font-heading);font-weight:800;font-size:1.2rem;color:#fff;">{diag_counts_25['baqa']} SV</span>
                        </div>
                        <p style="font-size:0.76rem;color:var(--text-muted);margin-top:0.4rem;line-height:1.4;">
                            KNM &ge; 75đ, Code &lt; 50đ &rarr; <span style="color:#fde68a;font-weight:600;">Phân luồng môn BA/QA</span>
                        </p>
                    </div>

                    <div class="decision-card" onclick="quickFilterDiag('Chưa đạt Chuẩn')" style="cursor:pointer;border-top:3px solid var(--border-focus);">
                        <div style="display:flex;justify-content:space-between;align-items:center;">
                            <strong style="color:#e4e4e7;font-size:0.88rem;">⚠️ Cần Phụ Đạo / Trung Gian</strong>
                            <span style="font-family:var(--font-heading);font-weight:800;font-size:1.2rem;color:#fff;">{diag_counts_25['atrisk'] + diag_counts_25['mid']} SV</span>
                        </div>
                        <p style="font-size:0.76rem;color:var(--text-muted);margin-top:0.4rem;line-height:1.4;">
                            Củng cố Python Core &amp; Skeleton Project
                        </p>
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
                    {''.join([f'<option value="{c}">{c}</option>' for c in classes_25])}
                </select>
                <select id="tierFilter" class="filter-select" onchange="applyFilters()">
                    <option value="">-- Mức Độ Năng Lực --</option>
                    <option value="3">Mức 3: Làm Chủ Tốt</option>
                    <option value="2">Mức 2: Đạt Chuẩn Đầu Ra</option>
                    <option value="1">Mức 1: Đạt Cơ Bản / Cần Bổ Trợ</option>
                    <option value="0">Mức 0: Chưa Đạt / Vắng Thi</option>
                </select>
                <select id="personaFilter" class="filter-select" onchange="applyFilters()">
                    <option value="">-- Chẩn Đoán Năng Lực --</option>
                    <option value="Nắm vững Lý thuyết">🚨 Nắm Lý thuyết - Hổng Thực hành ({diag_counts_25['rote']} SV)</option>
                    <option value="Nắm vững Năng lực Thực hành">💻 Vững Thực hành Lập trình ({diag_counts_25['solid']} SV)</option>
                    <option value="Thế mạnh Giao tiếp">📋 Tiềm năng BA/QA ({diag_counts_25['baqa']} SV)</option>
                    <option value="Chưa đạt Chuẩn Kiến thức Cốt lõi">🚨 Cần Phụ đạo Kiến thức ({diag_counts_25['atrisk']} SV)</option>
                    <option value="Đạt Mức Trung bình Cơ bản">🔷 Mức Trung bình Cơ bản ({diag_counts_25['mid']} SV)</option>
                    <option value="Vắng thi">⚪ Vắng thi / Chưa có bài ({diag_counts_25['absent']} SV)</option>
                </select>
            </div>

            <div class="bento-card">
                <div class="section-title">
                    <span>📋 Danh Bạ Khảo Thí &amp; Kế Hoạch Can Thiệp (<span id="recCount">{len(ks25)}</span> SV)</span>
                </div>
                <div class="table-wrapper" style="margin-top:1rem;">
                    <table class="data-table" id="studentTable">
                        <thead>
                            <tr>
                                <th>STT</th>
                                <th>Họ và Tên</th>
                                <th>Lớp</th>
                                <th>Final / 10</th>
                                <th>Thực Hành</th>
                                <th>Trắc Nghiệm</th>
                                <th>KNM</th>
                                <th>Tiếng Anh</th>
                                <th>Mức Độ</th>
                                <th>Chẩn Đoán</th>
                                <th>Kế Hoạch Can Thiệp</th>
                            </tr>
                        </thead>
                        <tbody id="studentTableBody">
                            {tbody_rows_25}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <div class="footer-bar">
            <div>Phòng Chuyên Môn &amp; Khảo Thí Đào Tạo | PTIT Rikkei Education</div>
            <div><a href="Executive_Summary_DGNL_Report.html">📑 Về Báo Cáo Tổng Hợp Ban Giám Đốc</a></div>
        </div>

    </div>

    <script>
    function switchTab(tabId, evt) {{
        document.querySelectorAll('.tab-pane').forEach(el => el.classList.remove('active'));
        document.querySelectorAll('.nav-tab-btn').forEach(el => el.classList.remove('active'));
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

    const ctx1 = document.getElementById('branchChart25').getContext('2d');
    new Chart(ctx1, {{
        type: 'bar',
        data: {{
            labels: ['📍 Cơ sở Hà Nội (HN-KS25)', '📍 Cơ sở TP.HCM (HCM-KS25)'],
            datasets: [{{
                label: 'Điểm TB Final (/10)',
                data: [{round(sum(s['final_10'] for s in ks25 if 'HN' in s['class'] and not s['is_absent'])/len([s for s in ks25 if 'HN' in s['class'] and not s['is_absent']]), 2)},
                       {round(sum(s['final_10'] for s in ks25 if 'HCM' in s['class'] and not s['is_absent'])/len([s for s in ks25 if 'HCM' in s['class'] and not s['is_absent']]), 2)}],
                backgroundColor: ['rgba(59,130,246,0.7)', 'rgba(245,158,11,0.7)'],
                borderColor: ['#3b82f6', '#f59e0b'],
                borderWidth: 1.5, borderRadius: 6
            }}]
        }},
        options: {{
            responsive: true, maintainAspectRatio: false,
            plugins: {{ legend: {{ display: false }} }},
            scales: {{
                y: {{ beginAtZero: true, max: 10, grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ color: '#94a3b8' }} }},
                x: {{ grid: {{ display: false }}, ticks: {{ color: '#94a3b8' }} }}
            }}
        }}
    }});

    const ctx2 = document.getElementById('tierDistChart25').getContext('2d');
    new Chart(ctx2, {{
        type: 'doughnut',
        data: {{
            labels: ['Mức 3 - Làm Chủ Tốt', 'Mức 2 - Đạt Chuẩn Khóa Học', 'Mức 1 - Cơ Bản', 'Mức 0 - Chưa Đạt / Vắng'],
            datasets: [{{
                data: [
                    {len([s for s in ks25 if s['tier']==3])},
                    {len([s for s in ks25 if s['tier']==2])},
                    {len([s for s in ks25 if s['tier']==1])},
                    {len([s for s in ks25 if s['tier']==0])}
                ],
                backgroundColor: ['#10b981', '#3b82f6', '#f59e0b', '#f43f5e'],
                borderWidth: 2, borderColor: '#171820'
            }}]
        }},
        options: {{
            responsive: true, maintainAspectRatio: false,
            cutout: '70%',
            plugins: {{ legend: {{ labels: {{ color: '#94a3b8', font: {{ size: 10 }} }} }} }}
        }}
    }});
    </script>
</body>
</html>
"""
    with open("outputs/KS25_DGNL_Report.html", "w", encoding="utf-8") as f:
        f.write(html_ks25)
    print("Updated outputs/KS25_DGNL_Report.html v7!")


    # ════════════════════════════════════════════════════════════════════════
    # 3. QTKD REPORT
    # ════════════════════════════════════════════════════════════════════════
    qtkd = data["qtkd"]
    total_reg_q = len(qtkd)
    active_q = [s for s in qtkd if not s["is_absent"]]
    took_q = len(active_q)
    ready_q = len([s for s in qtkd if s["tier"] in [2, 3]])
    ready_pct_q = round(ready_q / total_reg_q * 100, 1) if total_reg_q else 0.0
    avg_final_q = round(sum(s["final_10"] for s in active_q) / took_q, 2) if took_q else 0.0
    avg_knm_q = round(sum(s["knm"] for s in active_q if s["knm"] > 0) / len([s for s in active_q if s["knm"] > 0]), 1) if any(s["knm"] > 0 for s in active_q) else 0.0
    avg_ta_q = round(sum(s["ta"] for s in active_q if s["ta"] > 0) / len([s for s in active_q if s["ta"] > 0]), 1) if any(s["ta"] > 0 for s in active_q) else 0.0

    classes_q = sorted(list(set(s["class"] for s in qtkd)))
    class_stats_q = {}
    for c in classes_q:
        c_studs = [s for s in qtkd if s["class"] == c]
        c_act = [s for s in c_studs if not s["is_absent"]]
        c_pass = [s for s in c_studs if s["is_pass"] and not s["is_absent"]]
        c_ready = [s for s in c_studs if s["tier"] in [2, 3]]
        class_stats_q[c] = {
            "total": len(c_studs), "took": len(c_act), "pass": len(c_pass),
            "pass_pct": round(len(c_pass) / len(c_studs) * 100, 1) if c_studs else 0.0,
            "ready": len(c_ready), "ready_pct": round(len(c_ready) / len(c_studs) * 100, 1) if c_studs else 0.0,
            "avg_final": round(sum(s["final_10"] for s in c_act) / len(c_act), 2) if c_act else 0.0,
        }

    groups_q = sorted(list(set(s["nhom"] for s in qtkd if s["nhom"] != "Chưa phân nhóm")))
    group_stats_q = {}
    for g in groups_q:
        g_studs = [s for s in qtkd if s["nhom"] == g]
        g_act = [s for s in g_studs if not s["is_absent"]]
        group_stats_q[g] = {
            "count": len(g_studs),
            "avg_score": round(sum(s["final"] for s in g_act) / len(g_act), 1) if g_act else 0.0,
            "members": [s["name"] for s in g_studs]
        }

    diag_counts_q = {
        "global": len([s for s in qtkd if "Sẵn sàng Doanh nghiệp Quốc tế" in s["persona"]]),
        "lang_gap": len([s for s in qtkd if "Khoảng trống Ngoại ngữ" in s["persona"]]),
        "sales": len([s for s in qtkd if "Thế mạnh Đàm phán" in s["persona"]]),
        "atrisk": len([s for s in qtkd if "Chưa đạt Chuẩn Kiến thức" in s["persona"]]),
        "mid": len([s for s in qtkd if "Đạt Mức Trung bình Cơ bản" in s["persona"]]),
        "absent": len([s for s in qtkd if s["is_absent"]])
    }

    class_rows_q = ""
    for c, st in class_stats_q.items():
        class_rows_q += f"""
        <tr>
            <td style="text-align:left;font-weight:700;color:#fff;">{c}</td>
            <td>{st['total']} SV</td>
            <td>{st['took']} SV</td>
            <td><strong style="color:var(--color-qtkd);font-size:0.95rem;">{st['avg_final']}/10</strong></td>
            <td><span class="badge pass">{st['pass']} SV ({st['pass_pct']}%)</span></td>
            <td><strong style="color:#34d399;">{st['ready']} SV ({st['ready_pct']}%)</strong></td>
        </tr>
        """

    group_cards_q = ""
    for g, gst in group_stats_q.items():
        m_list = ", ".join(gst["members"])
        group_cards_q += f"""
        <div class="decision-card">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.4rem;">
                <span style="font-weight:700;color:#fff;font-size:0.9rem;">📁 {g}</span>
                <span style="font-family:var(--font-heading);font-size:1.25rem;font-weight:800;color:var(--color-qtkd);">{gst['avg_score']}/100</span>
            </div>
            <div style="font-size:0.7rem;color:var(--text-dim);margin-bottom:0.35rem;font-weight:600;text-transform:uppercase;">Thành viên ({gst['count']} SV):</div>
            <div style="font-size:0.78rem;color:var(--text-muted);line-height:1.4;">{m_list}</div>
        </div>
        """

    tbody_rows_q = ""
    for idx, s in enumerate(qtkd):
        p_badge = f'<span class="badge {s["persona_cls"]}">{s["persona"]}</span>'
        tier_badge = f'<span class="badge lvl-{s["tier"]}">{s["tier_label"].split(" (")[0]}</span>'
        sc_color = "#34d399" if s['final_10'] >= 8.0 else ("#60a5fa" if s['final_10'] >= 6.0 else ("#fbbf24" if s['final_10'] >= 4.0 else "#fb7185"))
        tbody_rows_q += f"""
        <tr class="student-row" data-name="{s['name'].lower()}" data-class="{s['class']}" data-tier="{s['tier']}" data-persona="{s['persona']}">
            <td>{idx+1}</td>
            <td style="text-align:left;font-weight:600;color:#fff;">{s['name']}</td>
            <td style="text-align:left;color:var(--text-muted);">{s['class']}</td>
            <td><strong style="color:{sc_color};font-size:1.05rem;">{s['final_10']}</strong></td>
            <td>{s['final']}</td>
            <td>{s['nhom']}</td>
            <td>{s['knm']}</td>
            <td>{f"{s['ta']:.0f}" if s['ta'] > 0 else '<span style="color:var(--text-dim);">-</span>'}</td>
            <td>{tier_badge}</td>
            <td style="text-align:left;">{p_badge}</td>
            <td style="text-align:left;font-size:0.77rem;color:var(--text-muted);max-width:280px;line-height:1.4;">{s['action_plan']}</td>
        </tr>
        """

    html_qtkd = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Báo Cáo ĐGNL Khối K25 QTKD (Quản Trị Kinh Doanh) | Rikkei Education</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        {base_css_q}
        {curric_css}
    </style>
</head>
<body>

    <header class="header">
        <div class="header-inner">
            <div class="logo-wrap">
                <div class="logo-badge" style="background:linear-gradient(135deg, #f59e0b, #d97706);">QTKD</div>
                <div>
                    <div class="logo-title">Báo Cáo ĐGNL Khối K25 – Quản Trị Kinh Doanh</div>
                    <div class="logo-sub">Đánh Giá Nghiệm Thu 11 Nhóm Dự Án Thực Chiến &amp; Bản Lĩnh Thuyết Trình</div>
                </div>
            </div>
            <div class="header-meta">
                Ban Giám Đốc Đào Tạo &amp; Hội Đồng Chuyên Môn<br>
                Cập nhật: 02/09/2026
            </div>
        </div>
    </header>

    <div class="container">

        <!-- NAV TABS -->
        <div class="nav-tabs-wrapper">
            <button class="nav-tab-btn active" onclick="switchTab('tab1', event)">📊 Tổng Quan &amp; Lớp Học</button>
            <button class="nav-tab-btn" onclick="switchTab('tab2', event)">📁 11 Nhóm Dự Án &amp; Điều Chỉnh Chương Trình</button>
            <button class="nav-tab-btn" onclick="switchTab('tab3', event)">🎯 Chẩn Đoán Năng Lực</button>
            <button class="nav-tab-btn" onclick="switchTab('tab4', event)">📋 Danh Bạ Học Viên</button>
        </div>

        <!-- Master KPI Strip -->
        <div class="kpi-grid">
            <div class="kpi-card" style="--kpi-accent: #f59e0b;">
                <div class="kpi-label">Sĩ Số Đăng Ký</div>
                <div class="kpi-value">{total_reg_q}</div>
                <div class="kpi-sub">3 Lớp (HN-K25-QTKD1..3)</div>
            </div>
            <div class="kpi-card" style="--kpi-accent: #fbbf24;">
                <div class="kpi-label">Dự Thi Thực Tế</div>
                <div class="kpi-value">{took_q}</div>
                <div class="kpi-sub">Tỷ lệ: {round(took_q/total_reg_q*100, 1)}%</div>
            </div>
            <div class="kpi-card" style="--kpi-accent: #f59e0b;">
                <div class="kpi-label">Điểm TB Final</div>
                <div class="kpi-value">{avg_final_q}/10</div>
                <div class="kpi-sub">Thang điểm 10 quy đổi</div>
            </div>
            <div class="kpi-card" style="--kpi-accent: #8b5cf6;">
                <div class="kpi-label">Chuẩn Đầu Ra (L2+L3)</div>
                <div class="kpi-value">{ready_q}</div>
                <div class="kpi-sub">Tỷ lệ: {ready_pct_q}%</div>
            </div>
            <div class="kpi-card" style="--kpi-accent: #06b6d4;">
                <div class="kpi-label">Điểm TB Kỹ Năng Mềm</div>
                <div class="kpi-value">{avg_knm_q}</div>
                <div class="kpi-sub">Thang điểm 100</div>
            </div>
            <div class="kpi-card" style="--kpi-accent: #3b82f6;">
                <div class="kpi-label">Điểm TB Tiếng Anh</div>
                <div class="kpi-value">{avg_ta_q:.0f}</div>
                <div class="kpi-sub">Chuẩn TOEIC / 990</div>
            </div>
        </div>

        <!-- TAB 1: TỔNG QUAN -->
        <div id="tab1" class="tab-pane active">
            <div class="bento-card">
                <div class="section-title">🏫 Bảng Thống Kê Theo Lớp Học (K25 QTKD)</div>
                <div class="table-wrapper" style="margin-top:1rem;">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Mã Lớp</th>
                                <th>Sĩ Số</th>
                                <th>Dự Thi</th>
                                <th>Điểm TB Final</th>
                                <th>Tỷ Lệ Đạt</th>
                                <th>Chuẩn Đầu Ra</th>
                            </tr>
                        </thead>
                        <tbody>
                            {class_rows_q}
                        </tbody>
                    </table>
                </div>
            </div>

            <div style="display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;margin-bottom:2rem;">
                <div class="bento-card">
                    <div class="section-title" style="font-size:1rem;margin-bottom:1rem;">📊 Điểm TB Theo Lớp</div>
                    <div style="height:230px;position:relative;">
                        <canvas id="classChartQ"></canvas>
                    </div>
                </div>
                <div class="bento-card">
                    <div class="section-title" style="font-size:1rem;margin-bottom:1rem;">📈 Phân Bố Mức Độ Năng Lực QTKD</div>
                    <div style="height:230px;position:relative;">
                        <canvas id="tierDistChartQ"></canvas>
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 2: 11 NHÓM DỰ ÁN & ĐIỀU CHỈNH CHƯƠNG TRÌNH -->
        <div id="tab2" class="tab-pane">
            <div class="bento-card">
                <div class="section-title">📁 Đánh Giá 11 Nhóm Dự Án Kinh Doanh Thực Chiến</div>
                <div style="display:grid;grid-template-columns:repeat(3, 1fr);gap:1rem;margin-top:1.25rem;">
                    {group_cards_q}
                </div>
            </div>

            <!-- CURRICULUM BENTO GRID QTKD -->
            <div class="bento-card" style="border-top:3px solid var(--color-qtkd);">
                <div class="section-title">🏛️ Chi Tiết Điều Chỉnh Khung Chương Trình Ngoại Ngữ &amp; Đề Án Kỳ III (QTKD)</div>
                <div style="display:grid;grid-template-columns:repeat(3, 1fr);gap:1.25rem;margin-top:1.25rem;">
                    
                    <div class="decision-card">
                        <div class="decision-card-top">
                            <span class="subject-name-tag">Business English Workshop <span class="code-chip">ENG301</span></span>
                            <span class="status-badge upgrade">Bắt Buộc Kỳ III</span>
                        </div>
                        <div class="gap-block">
                            <strong>⚠️ Lỗ hổng ĐGNL:</strong> 40 SV điểm chuyên môn &ge; 70đ nhưng Tiếng Anh &lt; 350đ.
                        </div>
                        <div class="action-block">
                            <ul class="action-list gold">
                                <li><strong>Tiếng Anh Thương Mại:</strong> Đàm phán B2B, viết Email chuyên nghiệp, thuyết trình dự án bằng Tiếng Anh.</li>
                                <li><strong>Rèn luyện phản xạ:</strong> Thực hành giao tiếp theo tình huống doanh nghiệp đa quốc gia.</li>
                            </ul>
                        </div>
                    </div>

                    <div class="decision-card">
                        <div class="decision-card-top">
                            <span class="subject-name-tag">Chuẩn TOEIC &ge; 450+ <span class="code-chip">Tốt Nghiệp</span></span>
                            <span class="status-badge reduce">Điều Kiện Cương Quyết</span>
                        </div>
                        <div class="gap-block">
                            <strong>⚠️ Chuẩn đầu ra:</strong> Doanh nghiệp FDI / MNC yêu cầu bắt buộc giao tiếp cơ bản.
                        </div>
                        <div class="action-block">
                            <ul class="action-list gold">
                                <li><strong>Quy chế tốt nghiệp:</strong> Bắt buộc có chứng chỉ TOEIC &ge; 450+ mới đủ điều kiện bảo vệ khóa luận tốt nghiệp Kỳ IV.</li>
                            </ul>
                        </div>
                    </div>

                    <div class="decision-card">
                        <div class="decision-card-top">
                            <span class="subject-name-tag">Pitching Trước Doanh Nghiệp <span class="code-chip">PRJ404</span></span>
                            <span class="status-badge newmod">Tuyển Dụng Trực Tiếp</span>
                        </div>
                        <div class="gap-block">
                            <strong>⚠️ Cơ hội việc làm:</strong> Kết nối trực tiếp sản phẩm đề án với quỹ đầu tư &amp; doanh nghiệp.
                        </div>
                        <div class="action-block">
                            <ul class="action-list gold">
                                <li><strong>Hội đồng thực tế:</strong> Mời đại diện doanh nghiệp tham gia chấm đề án để tuyển dụng sinh viên trực tiếp tại buổi bảo vệ.</li>
                            </ul>
                        </div>
                    </div>

                </div>
            </div>
        </div>

        <!-- TAB 3: CHẨN ĐOÁN -->
        <div id="tab3" class="tab-pane">
            <div class="bento-card">
                <div class="section-title">🎯 Ma Trận Chẩn Đoán Năng Lực QTKD</div>
                <div class="section-desc" style="margin-bottom:1.25rem;">
                    Click vào thẻ bất kỳ để lọc danh bạ học viên tương ứng:
                </div>

                <div style="display:grid;grid-template-columns:repeat(4, 1fr);gap:1.25rem;">
                    <div class="decision-card" onclick="quickFilterDiag('Khoảng trống Ngoại ngữ')" style="cursor:pointer;border-top:3px solid var(--color-warning);">
                        <div style="display:flex;justify-content:space-between;align-items:center;">
                            <strong style="color:#fbbf24;font-size:0.88rem;">💼 Giỏi QTKD - Yếu Ngoại Ngữ</strong>
                            <span style="font-family:var(--font-heading);font-weight:800;font-size:1.2rem;color:#fff;">{diag_counts_q['lang_gap']} SV</span>
                        </div>
                        <p style="font-size:0.76rem;color:var(--text-muted);margin-top:0.4rem;line-height:1.4;">
                            Điểm QTKD &ge; 70đ, TA &lt; 350đ &rarr; <span style="color:#fde68a;font-weight:600;">Business English Workshop</span>
                        </p>
                    </div>

                    <div class="decision-card" onclick="quickFilterDiag('Sẵn sàng Doanh nghiệp Quốc tế')" style="cursor:pointer;border-top:3px solid var(--color-success);">
                        <div style="display:flex;justify-content:space-between;align-items:center;">
                            <strong style="color:#34d399;font-size:0.88rem;">🌟 Sẵn Sàng Quốc Tế / FDI</strong>
                            <span style="font-family:var(--font-heading);font-weight:800;font-size:1.2rem;color:#fff;">{diag_counts_q['global']} SV</span>
                        </div>
                        <p style="font-size:0.76rem;color:var(--text-muted);margin-top:0.4rem;line-height:1.4;">
                            Vững chuyên môn, TA &ge; 450đ &rarr; <span style="color:#a7f3d0;font-weight:600;">Management Trainee</span>
                        </p>
                    </div>

                    <div class="decision-card" onclick="quickFilterDiag('Thế mạnh Đàm phán')" style="cursor:pointer;border-top:3px solid var(--color-pri);">
                        <div style="display:flex;justify-content:space-between;align-items:center;">
                            <strong style="color:#60a5fa;font-size:0.88rem;">🗣️ Thế Mạnh B2B Sales / Account</strong>
                            <span style="font-family:var(--font-heading);font-weight:800;font-size:1.2rem;color:#fff;">{diag_counts_q['sales']} SV</span>
                        </div>
                        <p style="font-size:0.76rem;color:var(--text-muted);margin-top:0.4rem;line-height:1.4;">
                            KNM &ge; 85đ &rarr; <span style="color:#93c5fd;font-weight:600;">Chuyên viên Phát triển KD</span>
                        </p>
                    </div>

                    <div class="decision-card" onclick="quickFilterDiag('Chưa đạt Chuẩn')" style="cursor:pointer;border-top:3px solid var(--border-focus);">
                        <div style="display:flex;justify-content:space-between;align-items:center;">
                            <strong style="color:#e4e4e7;font-size:0.88rem;">⚠️ Cần Phụ Đạo / Trung Gian</strong>
                            <span style="font-family:var(--font-heading);font-weight:800;font-size:1.2rem;color:#fff;">{diag_counts_q['atrisk'] + diag_counts_q['mid']} SV</span>
                        </div>
                        <p style="font-size:0.76rem;color:var(--text-muted);margin-top:0.4rem;line-height:1.4;">
                            Phụ đạo lập kế hoạch kinh doanh
                        </p>
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
                    {''.join([f'<option value="{c}">{c}</option>' for c in classes_q])}
                </select>
                <select id="tierFilter" class="filter-select" onchange="applyFilters()">
                    <option value="">-- Mức Độ Năng Lực --</option>
                    <option value="3">Mức 3: Làm Chủ Tốt</option>
                    <option value="2">Mức 2: Đạt Chuẩn Đầu Ra</option>
                    <option value="1">Mức 1: Đạt Cơ Bản / Cần Bổ Trợ</option>
                    <option value="0">Mức 0: Chưa Đạt / Vắng Thi</option>
                </select>
                <select id="personaFilter" class="filter-select" onchange="applyFilters()">
                    <option value="">-- Chẩn Đoán Năng Lực --</option>
                    <option value="Khoảng trống Ngoại ngữ">💼 Giỏi QTKD - Yếu Ngoại ngữ ({diag_counts_q['lang_gap']} SV)</option>
                    <option value="Sẵn sàng Doanh nghiệp Quốc tế">🌟 Sẵn sàng Quốc tế ({diag_counts_q['global']} SV)</option>
                    <option value="Thế mạnh Đàm phán">🗣️ Thế mạnh Sales / Account ({diag_counts_q['sales']} SV)</option>
                    <option value="Chưa đạt Chuẩn Kiến thức Cốt lõi">🚨 Cần Phụ đạo Kiến thức ({diag_counts_q['atrisk']} SV)</option>
                    <option value="Đạt Mức Trung bình Cơ bản">🔷 Mức Trung bình Cơ bản ({diag_counts_q['mid']} SV)</option>
                    <option value="Vắng thi">⚪ Vắng thi / Chưa có bài ({diag_counts_q['absent']} SV)</option>
                </select>
            </div>

            <div class="bento-card">
                <div class="section-title">
                    <span>📋 Danh Bạ Khảo Thí &amp; Kế Hoạch Can Thiệp (<span id="recCount">{len(qtkd)}</span> SV)</span>
                </div>
                <div class="table-wrapper" style="margin-top:1rem;">
                    <table class="data-table" id="studentTable">
                        <thead>
                            <tr>
                                <th>STT</th>
                                <th>Họ và Tên</th>
                                <th>Lớp</th>
                                <th>Final / 10</th>
                                <th>Điểm Dự Án</th>
                                <th>Nhóm</th>
                                <th>KNM</th>
                                <th>Tiếng Anh</th>
                                <th>Mức Độ</th>
                                <th>Chẩn Đoán</th>
                                <th>Kế Hoạch Can Thiệp</th>
                            </tr>
                        </thead>
                        <tbody id="studentTableBody">
                            {tbody_rows_q}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <div class="footer-bar">
            <div>Phòng Chuyên Môn &amp; Khảo Thí Đào Tạo | PTIT Rikkei Education</div>
            <div><a href="Executive_Summary_DGNL_Report.html">📑 Về Báo Cáo Tổng Hợp Ban Giám Đốc</a></div>
        </div>

    </div>

    <script>
    function switchTab(tabId, evt) {{
        document.querySelectorAll('.tab-pane').forEach(el => el.classList.remove('active'));
        document.querySelectorAll('.nav-tab-btn').forEach(el => el.classList.remove('active'));
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

    const ctx1 = document.getElementById('classChartQ').getContext('2d');
    new Chart(ctx1, {{
        type: 'bar',
        data: {{
            labels: {json.dumps(classes_q)},
            datasets: [{{
                label: 'Điểm TB Final (/10)',
                data: {[class_stats_q[c]['avg_final'] for c in classes_q]},
                backgroundColor: 'rgba(245,158,11,0.7)',
                borderColor: '#f59e0b',
                borderWidth: 1.5, borderRadius: 6
            }}]
        }},
        options: {{
            responsive: true, maintainAspectRatio: false,
            plugins: {{ legend: {{ display: false }} }},
            scales: {{
                y: {{ beginAtZero: true, max: 10, grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ color: '#94a3b8' }} }},
                x: {{ grid: {{ display: false }}, ticks: {{ color: '#94a3b8' }} }}
            }}
        }}
    }});

    const ctx2 = document.getElementById('tierDistChartQ').getContext('2d');
    new Chart(ctx2, {{
        type: 'doughnut',
        data: {{
            labels: ['Mức 3 - Làm Chủ Tốt', 'Mức 2 - Chuẩn Doanh Nghiệp', 'Mức 1 - Cơ Bản', 'Mức 0 - Chưa Đạt / Vắng'],
            datasets: [{{
                data: [
                    {len([s for s in qtkd if s['tier']==3])},
                    {len([s for s in qtkd if s['tier']==2])},
                    {len([s for s in qtkd if s['tier']==1])},
                    {len([s for s in qtkd if s['tier']==0])}
                ],
                backgroundColor: ['#10b981', '#3b82f6', '#f59e0b', '#f43f5e'],
                borderWidth: 2, borderColor: '#171820'
            }}]
        }},
        options: {{
            responsive: true, maintainAspectRatio: false,
            cutout: '70%',
            plugins: {{ legend: {{ labels: {{ color: '#94a3b8', font: {{ size: 10 }} }} }} }}
        }}
    }});
    </script>
</body>
</html>
"""
    with open("outputs/QTKD_DGNL_Report.html", "w", encoding="utf-8") as f:
        f.write(html_qtkd)
    print("Updated outputs/QTKD_DGNL_Report.html v7!")

if __name__ == "__main__":
    build_cohort_reports_v7()
