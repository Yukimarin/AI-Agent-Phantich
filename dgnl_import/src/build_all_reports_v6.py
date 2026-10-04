# -*- coding: utf-8 -*-
"""
Executive Summary Generator v6 - Ultra-Modern Bento Grid Architecture
"""
import json
import os
import sys

sys.path.append(os.path.dirname(__file__))
from build_complete_suite import load_data
from modern_theme import get_shared_css

def build_executive_summary_v6():
    data = load_data()
    ks24 = data["ks24"]
    ks25 = data["ks25"]
    qtkd = data["qtkd"]

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

    css = get_shared_css(primary_color="#3b82f6", accent_color="#8b5cf6")

    html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Báo Cáo Tổng Hợp ĐGNL Toàn Hệ Thống | Ban Giám Đốc Đào Tạo</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        {css}
    </style>
</head>
<body>

    <!-- ── HEADER ── -->
    <header class="header">
        <div class="header-inner">
            <div class="logo-wrap">
                <div class="logo-badge">RKE</div>
                <div>
                    <div class="logo-title">Báo Cáo Tổng Hợp Khảo Thí ĐGNL Lần 1</div>
                    <div class="logo-sub">Hệ Thống Đào Tạo PTIT Rikkei Education (Khối KS24, KS25 CNTT &amp; K25 QTKD)</div>
                </div>
            </div>
            <div class="header-meta">
                Ban Giám Đốc Đào Tạo &amp; Hội Đồng Chuyên Môn<br>
                Cập nhật: 02/09/2026
            </div>
        </div>
    </header>

    <div class="container">

        <!-- ── TAB NAVIGATION ── -->
        <div class="nav-tabs-wrapper">
            <button class="nav-tab-btn active" onclick="switchExecTab('tab-dash', event)">📊 Tổng Quan &amp; KPI</button>
            <button class="nav-tab-btn" onclick="switchExecTab('tab-lens', event)">🔬 6 Lăng Kính Khảo Thí</button>
            <button class="nav-tab-btn" onclick="switchExecTab('tab-diag', event)">🎯 Ma Trận Chẩn Đoán</button>
            <button class="nav-tab-btn" onclick="switchExecTab('tab-curric', event)">🏛️ Điều Chỉnh Chương Trình &amp; Môn Mới</button>
            <button class="nav-tab-btn" onclick="switchExecTab('tab-plan', event)">📋 Kế Hoạch Can Thiệp 3 Tầng</button>
        </div>

        <!-- ── KPI BENTO STRIP ── -->
        <div class="kpi-grid">
            <div class="kpi-card" style="--kpi-accent: #3b82f6;">
                <div class="kpi-label">Tổng Sĩ Số Đăng Ký</div>
                <div class="kpi-value">{total_reg}</div>
                <div class="kpi-sub">KS24: {len(ks24)} | KS25: {len(ks25)} | QTKD: {len(qtkd)}</div>
            </div>
            <div class="kpi-card" style="--kpi-accent: #10b981;">
                <div class="kpi-label">Dự Thi Thực Tế</div>
                <div class="kpi-value">{total_took}</div>
                <div class="kpi-sub">Tỷ lệ tham gia: {round(total_took/total_reg*100, 1)}%</div>
            </div>
            <div class="kpi-card" style="--kpi-accent: #f59e0b;">
                <div class="kpi-label">Đạt Chuẩn Chuyên Môn</div>
                <div class="kpi-value">{total_pass}</div>
                <div class="kpi-sub">Tỷ lệ Đạt: {round(total_pass/total_reg*100, 1)}%</div>
            </div>
            <div class="kpi-card" style="--kpi-accent: #8b5cf6;">
                <div class="kpi-label">Chuẩn Đầu Ra (L2+L3)</div>
                <div class="kpi-value">{total_ready}</div>
                <div class="kpi-sub">Tỷ lệ: {round(total_ready/total_reg*100, 1)}%</div>
            </div>
            <div class="kpi-card" style="--kpi-accent: #06b6d4;">
                <div class="kpi-label">Điểm TB Kỹ Năng Mềm</div>
                <div class="kpi-value">{round((avg_knm_ks24*len(ks24) + avg_knm_ks25*len(ks25) + avg_knm_qtkd*len(qtkd))/total_reg, 1)}</div>
                <div class="kpi-sub">Thang điểm 100</div>
            </div>
            <div class="kpi-card" style="--kpi-accent: #3b82f6;">
                <div class="kpi-label">Điểm TB Tiếng Anh</div>
                <div class="kpi-value">{round((avg_ta_ks24*len(ks24) + avg_ta_ks25*len(ks25) + avg_ta_qtkd*len(qtkd))/total_reg, 0):.0f}</div>
                <div class="kpi-sub">Chuẩn TOEIC / 990</div>
            </div>
        </div>

        <!-- ── TAB 1: TỔNG QUAN ────────────────────────────────────────────── -->
        <div id="tab-dash" class="tab-pane active">

            <!-- Executive Bottlenecks Banner -->
            <div class="bottleneck-banner">
                <div class="bottleneck-title">
                    <span>⚠️</span> 4 Điểm Nghẽn Cốt Lõi Cần Ban Giám Đốc Ra Quyết Sách
                </div>
                <div class="bottleneck-grid">
                    <div class="bottleneck-cell">
                        <strong>1. Độ Lệch Giảng Viên (7.7x)</strong>
                        <p>Điểm thực hành giữa các lớp chênh từ 45.8đ xuống 5.9đ &rarr; Cần chuẩn hóa giáo án Live-Coding đồng bộ.</p>
                    </div>
                    <div class="bottleneck-cell">
                        <strong>2. Nghịch Lý Trắc Nghiệm (r = 0.14)</strong>
                        <p>Trắc nghiệm đạt 70-80đ nhưng không code được API &rarr; Giảm 50% trắc nghiệm ở kỳ ĐGNL tới.</p>
                    </div>
                    <div class="bottleneck-cell">
                        <strong>3. Rơi Rụng Phỏng Vấn (53%)</strong>
                        <p>29 SV KS24 giỏi code nhưng liệt vấn đáp &rarr; Bắt buộc tham gia Mock Interview 1-on-1 theo STAR.</p>
                    </div>
                    <div class="bottleneck-cell">
                        <strong>4. Khoảng Trống Tiếng Anh</strong>
                        <p>Điểm TOEIC toàn hệ thống chỉ đạt 260-280đ &rarr; Đưa chuẩn TOEIC 450+ vào điều kiện tốt nghiệp.</p>
                    </div>
                </div>
            </div>

            <div class="section-header">
                <div>
                    <div class="section-title">🏛️ Đối Chiếu 3 Khối Đào Tạo (735 Sinh Viên)</div>
                    <div class="section-desc">Tổng hợp chỉ số phân tầng và chuẩn đầu ra toàn diện theo từng giai đoạn đào tạo</div>
                </div>
            </div>

            <!-- 3 Cohorts Grid -->
            <div style="display:grid;grid-template-columns:repeat(3, 1fr);gap:1.25rem;margin-bottom:2rem;">
                
                <!-- KS24 Card -->
                <div class="bento-card" style="border-top:3px solid var(--color-ks24);display:flex;flex-direction:column;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.75rem;">
                        <span class="cohort-badge-tag ks24">☕ KS24 JAVA / SPRING BOOT</span>
                        <span style="font-size:0.75rem;color:var(--text-muted);font-weight:600;">Cuối Kỳ III</span>
                    </div>
                    <div style="font-size:0.8rem;color:var(--text-muted);line-height:1.45;margin-bottom:1rem;">
                        Nghiệm thu chuẩn bị Đồ án Tốt nghiệp &amp; Tuyển dụng Doanh nghiệp.
                    </div>
                    <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.6rem;margin-bottom:1rem;">
                        <div style="background:rgba(255,255,255,0.02);padding:0.75rem;border-radius:var(--radius-sm);border:1px solid var(--border-subtle);">
                            <div style="font-size:0.68rem;color:var(--text-dim);font-weight:700;text-transform:uppercase;">Dự Thi / Sĩ Số</div>
                            <div style="font-family:var(--font-heading);font-size:1.35rem;font-weight:800;color:var(--color-ks24);margin-top:0.2rem;">{took_ks24} / {len(ks24)}</div>
                        </div>
                        <div style="background:rgba(255,255,255,0.02);padding:0.75rem;border-radius:var(--radius-sm);border:1px solid var(--border-subtle);">
                            <div style="font-size:0.68rem;color:var(--text-dim);font-weight:700;text-transform:uppercase;">Điểm TB Final</div>
                            <div style="font-family:var(--font-heading);font-size:1.35rem;font-weight:800;color:var(--color-ks24);margin-top:0.2rem;">{avg_ks24}/10</div>
                        </div>
                        <div style="background:rgba(255,255,255,0.02);padding:0.75rem;border-radius:var(--radius-sm);border:1px solid var(--border-subtle);">
                            <div style="font-size:0.68rem;color:var(--text-dim);font-weight:700;text-transform:uppercase;">Chuẩn Đầu Ra</div>
                            <div style="font-family:var(--font-heading);font-size:1.15rem;font-weight:800;color:#34d399;margin-top:0.2rem;">{ready_ks24} SV ({round(ready_ks24/len(ks24)*100, 1)}%)</div>
                        </div>
                        <div style="background:rgba(255,255,255,0.02);padding:0.75rem;border-radius:var(--radius-sm);border:1px solid var(--border-subtle);">
                            <div style="font-size:0.68rem;color:var(--text-dim);font-weight:700;text-transform:uppercase;">KNM / Tiếng Anh</div>
                            <div style="font-family:var(--font-heading);font-size:1.05rem;font-weight:800;color:#a7f3d0;margin-top:0.2rem;">{avg_knm_ks24}đ / {avg_ta_ks24:.0f}</div>
                        </div>
                    </div>
                    <div style="margin-top:auto;padding-top:0.75rem;border-top:1px solid var(--border-subtle);">
                        <a href="KS24_DGNL_Report.html" style="display:block;text-align:center;padding:0.5rem;background:rgba(16,185,129,0.12);color:var(--color-ks24);border:1px solid rgba(16,185,129,0.3);border-radius:var(--radius-sm);font-size:0.8rem;font-weight:700;text-decoration:none;">Xem Chi Tiết Khóa KS24 →</a>
                    </div>
                </div>

                <!-- KS25 Card -->
                <div class="bento-card" style="border-top:3px solid var(--color-ks25);display:flex;flex-direction:column;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.75rem;">
                        <span class="cohort-badge-tag ks25">🐍 KS25 FASTAPI / PYTHON</span>
                        <span style="font-size:0.75rem;color:var(--text-muted);font-weight:600;">Giữa Kỳ II</span>
                    </div>
                    <div style="font-size:0.8rem;color:var(--text-muted);line-height:1.45;margin-bottom:1rem;">
                        Khảo sát giữa kỳ phục vụ phân tầng học thuật chuyên sâu Kỳ III.
                    </div>
                    <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.6rem;margin-bottom:1rem;">
                        <div style="background:rgba(255,255,255,0.02);padding:0.75rem;border-radius:var(--radius-sm);border:1px solid var(--border-subtle);">
                            <div style="font-size:0.68rem;color:var(--text-dim);font-weight:700;text-transform:uppercase;">Dự Thi / Sĩ Số</div>
                            <div style="font-family:var(--font-heading);font-size:1.35rem;font-weight:800;color:var(--color-ks25);margin-top:0.2rem;">{took_ks25} / {len(ks25)}</div>
                        </div>
                        <div style="background:rgba(255,255,255,0.02);padding:0.75rem;border-radius:var(--radius-sm);border:1px solid var(--border-subtle);">
                            <div style="font-size:0.68rem;color:var(--text-dim);font-weight:700;text-transform:uppercase;">Điểm TB Final</div>
                            <div style="font-family:var(--font-heading);font-size:1.35rem;font-weight:800;color:var(--color-ks25);margin-top:0.2rem;">{avg_ks25}/10</div>
                        </div>
                        <div style="background:rgba(255,255,255,0.02);padding:0.75rem;border-radius:var(--radius-sm);border:1px solid var(--border-subtle);">
                            <div style="font-size:0.68rem;color:var(--text-dim);font-weight:700;text-transform:uppercase;">Chuẩn Đầu Ra</div>
                            <div style="font-family:var(--font-heading);font-size:1.15rem;font-weight:800;color:#60a5fa;margin-top:0.2rem;">{ready_ks25} SV ({round(ready_ks25/len(ks25)*100, 1)}%)</div>
                        </div>
                        <div style="background:rgba(255,255,255,0.02);padding:0.75rem;border-radius:var(--radius-sm);border:1px solid var(--border-subtle);">
                            <div style="font-size:0.68rem;color:var(--text-dim);font-weight:700;text-transform:uppercase;">KNM / Tiếng Anh</div>
                            <div style="font-family:var(--font-heading);font-size:1.05rem;font-weight:800;color:#93c5fd;margin-top:0.2rem;">{avg_knm_ks25}đ / {avg_ta_ks25:.0f}</div>
                        </div>
                    </div>
                    <div style="margin-top:auto;padding-top:0.75rem;border-top:1px solid var(--border-subtle);">
                        <a href="KS25_DGNL_Report.html" style="display:block;text-align:center;padding:0.5rem;background:rgba(59,130,246,0.12);color:var(--color-ks25);border:1px solid rgba(59,130,246,0.3);border-radius:var(--radius-sm);font-size:0.8rem;font-weight:700;text-decoration:none;">Xem Chi Tiết Khóa KS25 →</a>
                    </div>
                </div>

                <!-- QTKD Card -->
                <div class="bento-card" style="border-top:3px solid var(--color-qtkd);display:flex;flex-direction:column;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.75rem;">
                        <span class="cohort-badge-tag qtkd">💼 K25 QUẢN TRỊ KINH DOANH</span>
                        <span style="font-size:0.75rem;color:var(--text-muted);font-weight:600;">Giữa Kỳ II</span>
                    </div>
                    <div style="font-size:0.8rem;color:var(--text-muted);line-height:1.45;margin-bottom:1rem;">
                        Nghiệm thu 11 nhóm đề án kinh doanh và bảo vệ trước Hội đồng.
                    </div>
                    <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.6rem;margin-bottom:1rem;">
                        <div style="background:rgba(255,255,255,0.02);padding:0.75rem;border-radius:var(--radius-sm);border:1px solid var(--border-subtle);">
                            <div style="font-size:0.68rem;color:var(--text-dim);font-weight:700;text-transform:uppercase;">Dự Thi / Sĩ Số</div>
                            <div style="font-family:var(--font-heading);font-size:1.35rem;font-weight:800;color:var(--color-qtkd);margin-top:0.2rem;">{took_qtkd} / {len(qtkd)}</div>
                        </div>
                        <div style="background:rgba(255,255,255,0.02);padding:0.75rem;border-radius:var(--radius-sm);border:1px solid var(--border-subtle);">
                            <div style="font-size:0.68rem;color:var(--text-dim);font-weight:700;text-transform:uppercase;">Điểm TB Final</div>
                            <div style="font-family:var(--font-heading);font-size:1.35rem;font-weight:800;color:var(--color-qtkd);margin-top:0.2rem;">{avg_qtkd}/10</div>
                        </div>
                        <div style="background:rgba(255,255,255,0.02);padding:0.75rem;border-radius:var(--radius-sm);border:1px solid var(--border-subtle);">
                            <div style="font-size:0.68rem;color:var(--text-dim);font-weight:700;text-transform:uppercase;">Chuẩn Đầu Ra</div>
                            <div style="font-family:var(--font-heading);font-size:1.15rem;font-weight:800;color:#fbbf24;margin-top:0.2rem;">{ready_qtkd} SV ({round(ready_qtkd/len(qtkd)*100, 1)}%)</div>
                        </div>
                        <div style="background:rgba(255,255,255,0.02);padding:0.75rem;border-radius:var(--radius-sm);border:1px solid var(--border-subtle);">
                            <div style="font-size:0.68rem;color:var(--text-dim);font-weight:700;text-transform:uppercase;">KNM / Tiếng Anh</div>
                            <div style="font-family:var(--font-heading);font-size:1.05rem;font-weight:800;color:#fde68a;margin-top:0.2rem;">{avg_knm_qtkd}đ / {avg_ta_qtkd:.0f}</div>
                        </div>
                    </div>
                    <div style="margin-top:auto;padding-top:0.75rem;border-top:1px solid var(--border-subtle);">
                        <a href="QTKD_DGNL_Report.html" style="display:block;text-align:center;padding:0.5rem;background:rgba(245,158,11,0.12);color:var(--color-qtkd);border:1px solid rgba(245,158,11,0.3);border-radius:var(--radius-sm);font-size:0.8rem;font-weight:700;text-decoration:none;">Xem Chi Tiết Khối QTKD →</a>
                    </div>
                </div>

            </div>

            <!-- Charts Row -->
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;margin-bottom:2rem;">
                <div class="bento-card">
                    <div class="section-title" style="font-size:1rem;margin-bottom:1rem;">📈 So Sánh Điểm Chuyên Môn &amp; Kỹ Năng Mềm</div>
                    <div style="height:240px;position:relative;">
                        <canvas id="chartCompDash"></canvas>
                    </div>
                </div>
                <div class="bento-card">
                    <div class="section-title" style="font-size:1rem;margin-bottom:1rem;">🎯 Phân Bố Mức Độ Năng Lực Toàn Hệ Thống</div>
                    <div style="height:240px;position:relative;">
                        <canvas id="chartDoughnutDash"></canvas>
                    </div>
                </div>
            </div>

        </div>

        <!-- ── TAB 2: 6 LĂNG KÍNH KHẢO THÍ ─────────────────────────────────── -->
        <div id="tab-lens" class="tab-pane">
            <div class="section-header">
                <div>
                    <div class="section-title">🔬 6 Lăng Kính Chuyên Sâu Khảo Thí &amp; Quản Trị Đào Tạo</div>
                    <div class="section-desc">Phân tích đa chiều về phương pháp kiểm tra, độ lệch giảng viên và phễu tuyển dụng thực tế</div>
                </div>
            </div>

            <div style="display:grid;grid-template-columns:repeat(2, 1fr);gap:1.25rem;margin-bottom:1.75rem;">
                <div class="bento-card" style="border-left:4px solid var(--color-danger);margin-bottom:0;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.75rem;">
                        <strong style="color:#fff;font-size:0.95rem;">🌐 1. Nghịch Lý Đo Lường: Lý Thuyết vs Live-Coding</strong>
                        <span class="action-tag" style="background:rgba(244,63,94,0.15);color:#fb7185;">r = 0.14</span>
                    </div>
                    <p style="font-size:0.8rem;color:var(--text-muted);line-height:1.5;">
                        Hệ số tương quan r=0.14 cho thấy trắc nghiệm <em>không đo lường được năng lực viết code thực tế</em>. Học viên thuộc định nghĩa lý thuyết nhưng thiếu phản xạ mở IDE tự xây dựng API 4 lớp.
                    </p>
                </div>

                <div class="bento-card" style="border-left:4px solid var(--color-warning);margin-bottom:0;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.75rem;">
                        <strong style="color:#fff;font-size:0.95rem;">👥 2. Hiện Tượng "Ỷ Lại Nhóm" Trong Đồ Án</strong>
                        <span class="action-tag" style="background:rgba(245,158,11,0.15);color:#fbbf24;">r = 0.71 vs 0.17</span>
                    </div>
                    <p style="font-size:0.8rem;color:var(--text-muted);line-height:1.5;">
                        KNM tương quan rất cao với điểm Sản phẩm nhóm (r=0.71) nhưng lại không tương quan với Vấn đáp 1-1 (r=0.17). Cần áp dụng hệ số Git Commit và phỏng vấn độc lập để cá nhân hóa điểm số.
                    </p>
                </div>

                <div class="bento-card" style="border-left:4px solid var(--color-ks25);margin-bottom:0;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.75rem;">
                        <strong style="color:#fff;font-size:0.95rem;">🏫 3. Điểm Nghẽn Chất Lượng Giữa Các Lớp (Giảng Viên)</strong>
                        <span class="action-tag" style="background:rgba(59,130,246,0.15);color:#60a5fa;">Chênh 7.7 Lần</span>
                    </div>
                    <p style="font-size:0.8rem;color:var(--text-muted);line-height:1.5;">
                        Cùng 1 khung chương trình nhưng lớp dạy Hands-on Live Coding có điểm thực hành cao gấp 7.7 lần lớp dạy slide. Cần chuẩn hóa đồng bộ giáo án thực hành giữa tất cả các giảng viên.
                    </p>
                </div>

                <div class="bento-card" style="border-left:4px solid var(--color-ks24);margin-bottom:0;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.75rem;">
                        <strong style="color:#fff;font-size:0.95rem;">💼 4. Mô Phỏng Phễu Tuyển Dụng Doanh Nghiệp</strong>
                        <span class="action-tag" style="background:rgba(16,185,129,0.15);color:#34d399;">Đỗ 47.0%</span>
                    </div>
                    <p style="font-size:0.8rem;color:var(--text-muted);line-height:1.5;">
                        Chỉ <strong>87 / 185 SV (47.0%)</strong> đỗ đồng thời cả 3 vòng nếu phỏng vấn tại doanh nghiệp. 29 SV bị rơi rụng oan ở vòng vấn đáp; 20 SV rơi rụng ở vòng Live-Coding.
                    </p>
                </div>
            </div>

            <!-- Funnel & Class Chart -->
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;margin-bottom:2rem;">
                <div class="bento-card">
                    <div class="section-title" style="font-size:1rem;margin-bottom:1rem;">📉 Mô Phỏng Tỷ Lệ Đỗ Qua 4 Vòng Tuyển Dụng (KS24)</div>
                    <div style="height:220px;position:relative;">
                        <canvas id="chartFunnel"></canvas>
                    </div>
                </div>
                <div class="bento-card">
                    <div class="section-title" style="font-size:1rem;margin-bottom:1rem;">🏫 Độ Phân Hóa Điểm Thực Hành Giữa Các Lớp KS25</div>
                    <div style="height:220px;position:relative;">
                        <canvas id="chartClassDisp"></canvas>
                    </div>
                </div>
            </div>
        </div>

        <!-- ── TAB 3: MA TRẬN CHẨN ĐOÁN ────────────────────────────────────── -->
        <div id="tab-diag" class="tab-pane">
            <div class="section-header">
                <div>
                    <div class="section-title">🎯 Ma Trận Chẩn Đoán Phân Hóa Năng Lực Học Viên</div>
                    <div class="section-desc">Phân loại 4 nhóm học viên đặc thù để áp dụng các giải pháp can thiệp đúng trọng tâm</div>
                </div>
            </div>

            <div style="display:grid;grid-template-columns:repeat(4, 1fr);gap:1.25rem;margin-bottom:2rem;">
                <div class="bento-card" style="border-top:3px solid var(--color-danger);margin-bottom:0;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.75rem;">
                        <strong style="color:#fb7185;font-size:0.88rem;">🔇 Vững Kỹ Thuật - Yếu Vấn Đáp</strong>
                        <span style="font-family:var(--font-heading);font-size:1.25rem;font-weight:800;color:#fff;">29 SV</span>
                    </div>
                    <p style="font-size:0.78rem;color:var(--text-muted);line-height:1.45;margin-bottom:0.85rem;">
                        Code TH &ge; 65đ, Vấn đáp &lt; 50đ. Rào cản tâm lý và thiếu phản xạ trả lời theo mô hình STAR.
                    </p>
                    <div style="background:rgba(244,63,94,0.1);padding:0.5rem 0.75rem;border-radius:var(--radius-sm);font-size:0.75rem;color:#fecdd3;font-weight:600;">
                        👉 Mock Interview 1-on-1 (Không bắt học lại code)
                    </div>
                </div>

                <div class="bento-card" style="border-top:3px solid var(--color-warning);margin-bottom:0;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.75rem;">
                        <strong style="color:#fbbf24;font-size:0.88rem;">🗣️ Thế Mạnh KNM - Yếu Code</strong>
                        <span style="font-family:var(--font-heading);font-size:1.25rem;font-weight:800;color:#fff;">32 SV</span>
                    </div>
                    <p style="font-size:0.78rem;color:var(--text-muted);line-height:1.45;margin-bottom:0.85rem;">
                        KNM &ge; 75đ, Thực hành &lt; 50đ. Dễ đỗ vòng HR nhưng trượt vòng Live-Coding chuyên môn.
                    </p>
                    <div style="background:rgba(245,158,11,0.1);padding:0.5rem 0.75rem;border-radius:var(--radius-sm);font-size:0.75rem;color:#fde68a;font-weight:600;">
                        👉 Tư vấn Chuyển luồng BA / QA / Sales sớm
                    </div>
                </div>

                <div class="bento-card" style="border-top:3px solid var(--color-danger);margin-bottom:0;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.75rem;">
                        <strong style="color:#fb7185;font-size:0.88rem;">🚨 Nắm Lý Thuyết - Hổng Code TH</strong>
                        <span style="font-family:var(--font-heading);font-size:1.25rem;font-weight:800;color:#fff;">151 SV</span>
                    </div>
                    <p style="font-size:0.78rem;color:var(--text-muted);line-height:1.45;margin-bottom:0.85rem;">
                        TN &ge; 65đ, Thực hành &lt; 50đ. Bệnh học vẹt trắc nghiệm, chưa gõ được code API độc lập.
                    </p>
                    <div style="background:rgba(244,63,94,0.1);padding:0.5rem 0.75rem;border-radius:var(--radius-sm);font-size:0.75rem;color:#fecdd3;font-weight:600;">
                        👉 FastAPI Live-Coding Bootcamp 2 tuần
                    </div>
                </div>

                <div class="bento-card" style="border-top:3px solid var(--color-qtkd);margin-bottom:0;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.75rem;">
                        <strong style="color:#fbbf24;font-size:0.88rem;">💼 Giỏi QTKD - Hổng Ngoại Ngữ</strong>
                        <span style="font-family:var(--font-heading);font-size:1.25rem;font-weight:800;color:#fff;">40 SV</span>
                    </div>
                    <p style="font-size:0.78rem;color:var(--text-muted);line-height:1.45;margin-bottom:0.85rem;">
                        Điểm QTKD &ge; 70đ, Tiếng Anh &lt; 350đ. Rào cản khi ứng tuyển doanh nghiệp FDI / MNC.
                    </p>
                    <div style="background:rgba(245,158,11,0.1);padding:0.5rem 0.75rem;border-radius:var(--radius-sm);font-size:0.75rem;color:#fde68a;font-weight:600;">
                        👉 Business English Workshop bắt buộc Kỳ III
                    </div>
                </div>
            </div>
        </div>

        <!-- ── TAB 4: ĐIỀU CHỈNH CHƯƠNG TRÌNH & MÔN MỚI ────────────────────── -->
        <div id="tab-curric" class="tab-pane">
            <div class="section-header">
                <div>
                    <div class="section-title">🏛️ Quyết Sách Điều Chỉnh Từng Môn Học &amp; Khuyến Nghị Môn Mới Tăng Cơ Hội Việc Làm</div>
                    <div class="section-desc">Cải tiến thực chiến từng môn học theo lộ trình CTĐT và bổ sung môn tự chọn mở rộng việc làm</div>
                </div>
            </div>

            <div class="curric-bento-grid">
                
                <!-- KS24 Full Subject Modifications Card -->
                <div class="curric-cohort-card" style="border-top:3px solid var(--color-ks24);">
                    <div class="curric-cohort-header">
                        <div>
                            <span class="cohort-badge-tag ks24">☕ KHÓA KS24 (JAVA / SPRING BOOT)</span>
                            <div style="font-size:0.8rem;color:var(--text-muted);margin-top:0.35rem;">Điều chỉnh học phần Kỳ IV &amp; Đề xuất môn tự chọn Kỳ V</div>
                        </div>
                        <span class="action-tag core">Cuối Kỳ III &rarr; Kỳ IV</span>
                    </div>

                    <!-- Subject 1 -->
                    <div class="subject-item-card">
                        <div class="subject-item-top">
                            <span class="subject-code">1. Microservices System Design <span class="credit-tag">IT214-K24 • 2.5 TC</span></span>
                            <span class="action-tag core">Cải Tiến Lõi</span>
                        </div>
                        <ul class="subject-feature-list">
                            <li><strong>Bridge Module (2 buổi đầu):</strong> Củng cố <code>@Transactional</code> monolithic nâng cao &amp; thực hành <strong>Pessimistic / Optimistic Locking JPA</strong> để chống race condition.</li>
                            <li><strong>OAuth2 Token Propagation:</strong> Cấu hình Feign Client RequestInterceptor truyền JWT qua Gateway để ngăn chặn triệt để lỗi IDOR.</li>
                            <li><strong>Modern Tracing:</strong> Tích hợp <strong>Micrometer + OpenTelemetry + Grafana Tempo</strong> (Spring Boot 3+) thay cho Spring Cloud Sleuth cũ.</li>
                            <li><strong>Tối ưu tránh trùng:</strong> Tái sử dụng Docker Compose từ môn DevOps, không dạy lại từ đầu.</li>
                        </ul>
                    </div>

                    <!-- Subject 2 -->
                    <div class="subject-item-card">
                        <div class="subject-item-top">
                            <span class="subject-code">2. DevOps Fundamentals <span class="credit-tag">IT209-K24 • 1.9 TC</span></span>
                            <span class="action-tag sec">DevSecOps &amp; Infra</span>
                        </div>
                        <ul class="subject-feature-list">
                            <li><strong>Lightweight DevSecOps:</strong> Tích hợp Semgrep / Snyk quét lỗ hổng tĩnh trực tiếp trên GitHub Actions (thay SonarQube cồng kềnh).</li>
                            <li><strong>PLG Observability Stack:</strong> Setup <strong>Prometheus + Loki + Promtail + Grafana</strong> giám sát RAM/CPU VPS (thay thế ELK Stack dễ gây tràn RAM OOM).</li>
                            <li><strong>Database Migration:</strong> Tự động hóa cập nhật schema DB qua Flyway / Liquibase.</li>
                        </ul>
                    </div>

                    <!-- Subject 3 -->
                    <div class="subject-item-card">
                        <div class="subject-item-top">
                            <span class="subject-code">3. AI Integration in Action <span class="credit-tag">IT213-K24 • 1.9 TC</span></span>
                            <span class="action-tag ai">AI &amp; GenAI</span>
                        </div>
                        <ul class="subject-feature-list">
                            <li><strong>Semantic Caching (RedisVL / GPTCache):</strong> Cache câu trả lời LLM tương đồng để tối ưu 80% chi phí API.</li>
                            <li><strong>Advanced AI Agents (LangGraph / CrewAI):</strong> Xây dựng Agent đồ thị đa tác vụ đón đầu xu hướng 2026.</li>
                            <li><strong>SSE Streaming:</strong> Server-Sent Events stream câu trả lời về ReactJS mượt mà, chống nghẽn bộ nhớ.</li>
                        </ul>
                    </div>

                    <!-- Electives VIP Box -->
                    <div class="elective-vip-card">
                        <div class="elective-vip-title">
                            <span>🌟</span> KHUYẾN NGHỊ 2 MÔN HỌC TỰ CHỌN MỚI Ở KỲ V (MỞ RỘNG VIỆC LÀM)
                        </div>
                        <div class="elective-grid">
                            <div class="elective-item">
                                <strong>• Python &amp; Data Analytics Fundamentals</strong>
                                <p>Xử lý dữ liệu với Pandas/SQL + Trực quan hóa Power BI &rarr; Mở rộng việc làm sang <strong>Data Analyst / BI Developer</strong>.</p>
                            </div>
                            <div class="elective-item">
                                <strong>• Cloud Native &amp; Kubernetes Scaling</strong>
                                <p>Thực hành chuyên sâu AWS (EC2/S3/RDS) &amp; K8s &rarr; Đào tạo <strong>Kỹ sư Cloud / DevOps / SRE</strong>.</p>
                            </div>
                        </div>
                    </div>

                </div>

                <!-- KS25 Full Subject Modifications Card -->
                <div class="curric-cohort-card" style="border-top:3px solid var(--color-ks25);">
                    <div class="curric-cohort-header">
                        <div>
                            <span class="cohort-badge-tag ks25">🐍 KHÓA KS25 (FASTAPI / PYTHON)</span>
                            <div style="font-size:0.8rem;color:var(--text-muted);margin-top:0.35rem;">Giảm tải lý thuyết hàn lâm &amp; Bồi dưỡng thực chiến Kỳ III</div>
                        </div>
                        <span class="action-tag sec">Giữa Kỳ II &rarr; Kỳ III</span>
                    </div>

                    <!-- Subject 1 -->
                    <div class="subject-item-card">
                        <div class="subject-item-top">
                            <span class="subject-code">1. Phân Tích Thiết Kế (<code>IT105</code>) &amp; Agile (<code>IT106</code>)</span>
                            <span class="action-tag reduce">Giảm Tải Sơ Đồ</span>
                        </div>
                        <ul class="subject-feature-list blue">
                            <li><strong>Không vẽ diagram trên giấy:</strong> Cắt bỏ các bài tập vẽ sơ đồ lý thuyết suông; chuyển 100% sang mô hình <strong>Design-to-Code</strong>.</li>
                            <li><strong>Thiết kế gắn liền với Code API:</strong> Sinh viên thiết kế ERD Schema &rarr; Chuyển thành Pydantic Schema / SQLAlchemy Models trên FastAPI &rarr; Viết Swagger/OpenAPI Spec.</li>
                            <li><strong>Quản trị Agile Scrum thực chiến:</strong> Chia Sprint trên Jira/Trello và push code trực tiếp lên GitHub Repository.</li>
                        </ul>
                    </div>

                    <!-- Subject 2 -->
                    <div class="subject-item-card">
                        <div class="subject-item-top">
                            <span class="subject-code">2. FastAPI Live-Coding Intensive <span class="credit-tag">2 Tuần Đầu Kỳ III</span></span>
                            <span class="action-tag core">Bồi Dưỡng Cấp Tốc</span>
                        </div>
                        <ul class="subject-feature-list blue">
                            <li><strong>Bồi dưỡng cấp tốc 151 SV hổng code:</strong> Cung cấp sẵn Project Skeleton chuẩn để học viên rèn phản xạ code API độc lập.</li>
                            <li><strong>Tái cấu trúc tỷ trọng kiểm tra:</strong> Tăng bài tập Live-Coding lên 70%, giảm trắc nghiệm xuống 15%, bổ sung 15% vấn đáp tại chỗ.</li>
                        </ul>
                    </div>

                    <!-- Subject 3 -->
                    <div class="subject-item-card" style="border-left:3px solid var(--color-ks25);">
                        <div class="subject-item-top">
                            <span class="subject-code" style="color:#60a5fa;">3. BỔ SUNG CẤP THIẾT: Frontend Framework <span class="credit-tag">ReactJS / NextJS</span></span>
                            <span class="action-tag core">Môn Mới Bắt Buộc</span>
                        </div>
                        <ul class="subject-feature-list blue">
                            <li><strong>Khắc phục khoảng trống lớn nhất của KS25:</strong> Lộ trình KS25 hiện tại thiếu hoàn toàn Frontend nâng cao. Bổ sung ReactJS/NextJS ở Kỳ III để sinh viên đủ năng lực xây dựng ứng dụng <strong>Fullstack Web/AI</strong> hoàn chỉnh.</li>
                        </ul>
                    </div>

                    <!-- Subject 4 -->
                    <div class="subject-item-card">
                        <div class="subject-item-top">
                            <span class="subject-code">4. Applied DSA &amp; Database Optimization <span class="credit-tag">Kỳ III</span></span>
                            <span class="action-tag sec">Nền Tảng AI</span>
                        </div>
                        <ul class="subject-feature-list blue">
                            <li><strong>Nền tảng trước khi học AI:</strong> Củng cố Cấu trúc dữ liệu &amp; Giải thuật ứng dụng cùng kỹ năng tối ưu truy vấn PostgreSQL/SQLAlchemy trước khi bước vào học phần AI/Machine Learning ở Kỳ IV.</li>
                        </ul>
                    </div>

                </div>

            </div>
        </div>

        <!-- ── TAB 5: KẾ HOẠCH CAN THIỆP ───────────────────────────────────── -->
        <div id="tab-plan" class="tab-pane">
            <div class="section-header">
                <div>
                    <div class="section-title">📋 Kế Hoạch Can Thiệp Sư Phạm 3 Tầng Dành Cho Giám Đốc Đào Tạo</div>
                    <div class="section-desc">Lộ trình triển khai đồng bộ từ cấp bách 30 ngày đến tái cấu trúc chuẩn đầu ra dài hạn</div>
                </div>
            </div>

            <div style="display:grid;grid-template-columns:repeat(3, 1fr);gap:1.25rem;margin-bottom:2rem;">
                <div class="bento-card" style="border-top:3px solid var(--color-danger);margin-bottom:0;">
                    <span class="action-tag" style="background:rgba(244,63,94,0.15);color:#fb7185;margin-bottom:1rem;display:inline-block;">⚡ TẦNG 1: CẤP BÁCH (0 – 30 NGÀY)</span>
                    <ul class="subject-feature-list" style="gap:0.75rem;">
                        <li><strong>Mock Interview 1-on-1 (KS24):</strong> Tổ chức 3 buổi phỏng vấn giả định với Tech Lead doanh nghiệp cho 29 SV giỏi code yếu vấn đáp theo phương pháp STAR.</li>
                        <li><strong>FastAPI Live-Coding Bootcamp (KS25):</strong> Khóa bổ trợ 2 tuần cho 151 SV hổng code; cung cấp Project Skeleton sẵn để rèn phản xạ viết API.</li>
                        <li><strong>Hội Thảo Phân Luồng BA / QA Sớm:</strong> Tư vấn chuyển luồng chuyên ngành cho 32 SV có KNM tốt nhưng không có thế mạnh code sâu.</li>
                    </ul>
                </div>

                <div class="bento-card" style="border-top:3px solid var(--color-warning);margin-bottom:0;">
                    <span class="action-tag" style="background:rgba(245,158,11,0.15);color:#fbbf24;margin-bottom:1rem;display:inline-block;">🔄 TẦNG 2: QUY TRÌNH &amp; GIẢNG VIÊN (KỲ III - IV)</span>
                    <ul class="subject-feature-list gold" style="gap:0.75rem;">
                        <li><strong>Quy Định "Live-Code Review 3 Phút":</strong> Bắt buộc dành 30% thời lượng mỗi buổi Lab để sinh viên thuyết trình giải pháp code cá nhân.</li>
                        <li><strong>Chuẩn Hóa Giáo Án Giảng Viên:</strong> Chấn chỉnh phương pháp giảng dạy tại các lớp điểm thực hành dưới 20đ (HCM-CNTT8, HN-CNTT6).</li>
                        <li><strong>Business English Workshop (QTKD):</strong> Triển khai học phần tiếng Anh thương mại bắt buộc từ Kỳ III để nâng chuẩn TOEIC &ge; 450+.</li>
                    </ul>
                </div>

                <div class="bento-card" style="border-top:3px solid var(--color-success);margin-bottom:0;">
                    <span class="action-tag" style="background:rgba(16,185,129,0.15);color:#34d399;margin-bottom:1rem;display:inline-block;">🎯 TẦNG 3: KHẢO THÍ &amp; CHUẨN ĐẦU RA (DÀI HẠN)</span>
                    <ul class="subject-feature-list" style="gap:0.75rem;">
                        <li><strong>Tái Cấu Trúc Đề Thi ĐGNL Lần 2:</strong> Giảm 50% câu hỏi trắc nghiệm lý thuyết, tăng thời lượng bài thi Live-Coding &amp; Vấn đáp thực tế.</li>
                        <li><strong>Áp Dụng Bộ Chỉ Số GEI Tốt Nghiệp:</strong> GEI = Code (40%) + Vấn đáp/KNM (35%) + Ngoại ngữ (25%).</li>
                        <li><strong>Cam Kết Chuẩn Đầu Ra Doanh Nghiệp:</strong> Đảm bảo tỷ lệ sinh viên đỗ phỏng vấn thử việc đúng chuyên ngành đạt &gt; 85% sau tốt nghiệp.</li>
                    </ul>
                </div>
            </div>

            <!-- Fast Navigation Strip -->
            <div style="background:var(--bg-surface);border:1px solid var(--border-subtle);border-radius:var(--radius-lg);padding:1.25rem 1.5rem;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:1rem;">
                <div style="font-size:0.82rem;color:var(--text-muted);">
                    📑 Tra cứu danh bạ chi tiết và kế hoạch can thiệp từng sinh viên:
                </div>
                <div style="display:flex;gap:0.65rem;">
                    <a href="KS24_DGNL_Report.html" style="padding:0.45rem 0.9rem;background:rgba(16,185,129,0.12);color:#34d399;border:1px solid rgba(16,185,129,0.3);border-radius:var(--radius-sm);font-size:0.8rem;font-weight:700;text-decoration:none;">☕ Chi Tiết KS24</a>
                    <a href="KS25_DGNL_Report.html" style="padding:0.45rem 0.9rem;background:rgba(59,130,246,0.12);color:#60a5fa;border:1px solid rgba(59,130,246,0.3);border-radius:var(--radius-sm);font-size:0.8rem;font-weight:700;text-decoration:none;">🐍 Chi Tiết KS25</a>
                    <a href="QTKD_DGNL_Report.html" style="padding:0.45rem 0.9rem;background:rgba(245,158,11,0.12);color:#fbbf24;border:1px solid rgba(245,158,11,0.3);border-radius:var(--radius-sm);font-size:0.8rem;font-weight:700;text-decoration:none;">💼 Chi Tiết QTKD</a>
                </div>
            </div>
        </div>

        <!-- ── FOOTER ── -->
        <div class="footer-bar">
            <div>Phòng Chuyên Môn &amp; Khảo Thí Đào Tạo | PTIT Rikkei Education</div>
            <div>Báo Cáo Tổng Hợp ĐGNL Lần 1 © 2026. Chuẩn Hóa Quản Trị Giáo Dục.</div>
        </div>

    </div>

    <!-- ── CHARTS JS ── -->
    <script>
    function switchExecTab(tabId, evt) {{
        document.querySelectorAll('.tab-pane').forEach(el => el.classList.remove('active'));
        document.querySelectorAll('.nav-tab-btn').forEach(el => el.classList.remove('active'));
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
            plugins: {{ legend: {{ labels: {{ color: '#94a3b8', font: {{ size: 11 }} }} }} }},
            scales: {{
                y: {{ beginAtZero: true, max: 10, grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ color: '#94a3b8' }} }},
                x: {{ grid: {{ display: false }}, ticks: {{ color: '#94a3b8' }} }}
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
                backgroundColor: ['#10b981', '#3b82f6', '#f59e0b', '#f43f5e'],
                borderWidth: 2, borderColor: '#171820'
            }}]
        }},
        options: {{
            responsive: true, maintainAspectRatio: false,
            cutout: '70%',
            plugins: {{ legend: {{ position: 'right', labels: {{ color: '#94a3b8', font: {{ size: 10 }} }} }} }}
        }}
    }});

    const ctx3 = document.getElementById('chartFunnel').getContext('2d');
    new Chart(ctx3, {{
        type: 'bar',
        data: {{
            labels: ['Dự Thi (185 SV)', 'V1: CV/HR (139 SV)', 'V2: Vấn Đáp (128 SV)', 'V3: Live-Code (136 SV)', 'Đỗ Chung Cuộc (87 SV)'],
            datasets: [{{
                data: [100, 75.1, 69.2, 73.5, 47.0],
                backgroundColor: ['#475569', '#3b82f6', '#f59e0b', '#8b5cf6', '#10b981'],
                borderRadius: 6
            }}]
        }},
        options: {{
            indexAxis: 'y', responsive: true, maintainAspectRatio: false,
            plugins: {{ legend: {{ display: false }} }},
            scales: {{
                x: {{ beginAtZero: true, max: 100, grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ callback: v => v + '%', color: '#94a3b8' }} }},
                y: {{ grid: {{ display: false }}, ticks: {{ color: '#94a3b8', font: {{ size: 10 }} }} }}
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
                    '#10b981', '#34d399', '#3b82f6', '#60a5fa', '#f59e0b', '#fbbf24', '#fb7185', '#f43f5e'
                ],
                borderRadius: 6
            }}]
        }},
        options: {{
            responsive: true, maintainAspectRatio: false,
            plugins: {{ legend: {{ display: false }} }},
            scales: {{
                y: {{ beginAtZero: true, max: 50, grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ color: '#94a3b8' }} }},
                x: {{ grid: {{ display: false }}, ticks: {{ color: '#94a3b8', font: {{ size: 9 }} }} }}
            }}
        }}
    }});
    </script>
</body>
</html>
"""
    with open("outputs/Executive_Summary_DGNL_Report.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Compiled outputs/Executive_Summary_DGNL_Report.html v6 successfully!")

if __name__ == "__main__":
    build_executive_summary_v6()
