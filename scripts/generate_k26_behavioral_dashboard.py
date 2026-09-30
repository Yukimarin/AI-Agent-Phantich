# -*- coding: utf-8 -*-
"""
Script: generate_k26_behavioral_dashboard.py
Mục đích:
  1. Đọc kết quả phân tích từ data/processed/k26_behavioral_analysis.json.
  2. Tạo Dashboard HTML Executive cao cấp báo cáo Giám đốc Đào tạo.
  3. Tích hợp Chart.js, các thẻ KPI, bảng tiến độ 9 lớp, kế hoạch tác chiến PIC/Deadline.
  4. Xuất file ra output/dashboards/management/bao_cao_k26_chuyen_dich_hanh_vi.html
     và đồng bộ sang deploy_web/.
"""

import json
import os
import sys
import shutil

sys.stdout.reconfigure(encoding='utf-8')

def main():
    print("=== BẮT ĐẦU TẠO DASHBOARD HTML EXECUTIVE BÁO CÁO GIÁM ĐỐC ===")
    
    with open('data/processed/k26_behavioral_analysis.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    overall = data['overall']
    classes = data['classes']
    students = data['all_students']
    
    th1_students = [s for s in students if s['group'] == 'TH1_PERSISTENT_RISK']
    th4_students = [s for s in students if s['group'] == 'TH4_NEW_EMERGENT_RISK']
    th2_students = [s for s in students if s['group'] == 'TH2_IMPROVING']
    th3_students = [s for s in students if s['group'] == 'TH3_RESOLVED']

    # Text summary for 1-Click Copy
    summary_text = f"""BÁO CÁO CHUYÊN ĐỀ TÂN SINH VIÊN K26 — CHUYỂN DỊCH HÀNH VI & KẾ HOẠCH TÁC CHIẾN TẠI LỚP
Kính gửi: Anh Nguyễn Duy Quang - Giám đốc Đào tạo

1. TỔNG QUAN TỶ LỆ CẢI THIỆN:
- Quy mô: {overall['total_students']} sinh viên / 9 lớp K26 đang học.
- Tỷ lệ Cải thiện chung toàn khóa: {overall['overall_improvement_rate']}% (356/374 SV).
  * TH3 (Đã sạch lỗi / Thích nghi tốt): {overall['th3_count']} SV ({overall['th3_pct']}%) -> Tuần 1 lỗi LMS, sang môn mới đã vào guồng chuẩn 100%.
  * TH2 (Đang tiến bộ rõ rệt): {overall['th2_count']} SV ({overall['th2_pct']}%) -> Vi phạm giảm mạnh so với môn đầu.
  * TH1 (Nguy cơ bỏ học / Báo động Đỏ): {overall['th1_count']} SV ({overall['th1_pct']}%) -> Vắng dai dẳng từ môn 1 sang môn mới.
  * TH4 (Sốc môn mới chuyên ngành): {overall['th4_count']} SV ({overall['th4_pct']}%) -> Môn 1 tốt nhưng môn mới (IT108/ENG105) nợ bài/vắng.

2. XẾP HẠNG TỶ LỆ CẢI THIỆN 9 LỚP:
- Nhóm Xuất Sắc (100% Cải thiện): HCM-CNTT1, HCM-CNTT2, HCM-QTKD1, HN-QTKD3.
- Nhóm Khá Tốt (90% - 97.6%): HN-CNTT3 (97.6%), HN-QTKD2 (95.5%), HN-QTKD1 (90.9%), HN-CNTT2 (90.7%).
- Điểm Nóng Cần Tập Trung: HN-KS26-CNTT1 (83.7% cải thiện, có 3 SV TH1 và 4 SV TH4).

3. KẾ HOẠCH HÀNH ĐỘNG TÁC CHIẾN (VÀO TRỰC TIẾP LỚP 5-15 PHÚT):
- Nhóm TH1 (5 SV): Gặp riêng 5p cuối giờ tại lớp, lập biên bản cam kết, gọi phụ huynh. PIC: Quản lý ĐT + CVHT. Deadline: 48h.
- Nhóm TH4 (13 SV): Gặp 5p giữa giờ, tháo gỡ bài tập khó môn IT108/ENG105, bàn giao Trợ giảng kèm cặp. PIC: GV bộ môn + Trợ giảng. Deadline: Trước buổi học tới.
- Nhóm TH2 (5 SV): Gặp 3p đầu giờ, biểu dương tiến bộ, nhắc nộp bài đúng hạn. PIC: CVHT. Deadline: Hết tuần.
- Nhóm TH3 (351 SV): Miễn can thiệp kỷ luật, tuyên dương qua nhóm Zalo lớp.

(Đã xuất bản File Excel tác chiến 14 Sheet tại output/dashboards/management/K26_Theo_Doi_Chuyen_Dich_Hanh_Vi_Va_Giai_Phap.xlsx)"""

    # Generate Chart Data
    class_labels = [c['class'] for c in reversed(classes)]
    class_rates = [c['improvement_rate'] for c in reversed(classes)]
    
    html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Báo Cáo Chẩn Đoán Chuyển Dịch Hành Vi K26 — Giám Đốc Đào Tạo</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --primary: #1e3a8a;
            --primary-light: #3b82f6;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
            --orange: #f97316;
            --bg-main: #f8fafc;
            --card-bg: #ffffff;
            --text-main: #0f172a;
            --text-muted: #64748b;
            --border: #e2e8f0;
        }}
        
        * {{ margin: 0; padding: 0; box-sizing: border-box; font-family: 'Inter', -apple-system, sans-serif; }}
        body {{ background-color: var(--bg-main); color: var(--text-main); padding: 24px; line-height: 1.5; }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        
        /* Header */
        .header {{
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            color: #ffffff;
            padding: 32px;
            border-radius: 16px;
            margin-bottom: 24px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
            position: relative;
            overflow: hidden;
        }}
        .header::after {{
            content: '';
            position: absolute;
            top: -50%;
            right: -10%;
            width: 400px;
            height: 400px;
            background: radial-gradient(circle, rgba(59,130,246,0.15) 0%, transparent 70%);
            border-radius: 50%;
        }}
        .badge-sub {{
            display: inline-block;
            background: rgba(59, 130, 246, 0.2);
            color: #93c5fd;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            margin-bottom: 12px;
            border: 1px solid rgba(59, 130, 246, 0.3);
        }}
        .header h1 {{ font-size: 26px; font-weight: 800; margin-bottom: 8px; letter-spacing: -0.5px; }}
        .header p {{ color: #94a3b8; font-size: 14px; max-width: 850px; }}
        
        /* Action Bar */
        .action-bar {{
            display: flex;
            gap: 12px;
            margin-top: 20px;
            flex-wrap: wrap;
        }}
        .btn {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 10px 18px;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            border: none;
            text-decoration: none;
        }}
        .btn-primary {{ background: #2563eb; color: #fff; }}
        .btn-primary:hover {{ background: #1d4ed8; }}
        .btn-success {{ background: #059669; color: #fff; }}
        .btn-success:hover {{ background: #047857; }}
        .btn-outline {{ background: rgba(255,255,255,0.1); color: #fff; border: 1px solid rgba(255,255,255,0.2); }}
        .btn-outline:hover {{ background: rgba(255,255,255,0.2); }}
        
        /* KPI Cards Grid */
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-bottom: 24px;
        }}
        .kpi-card {{
            background: var(--card-bg);
            border-radius: 14px;
            padding: 24px;
            border: 1px solid var(--border);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            position: relative;
            overflow: hidden;
        }}
        .kpi-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 6px;
            height: 100%;
        }}
        .kpi-card.green::before {{ background: var(--success); }}
        .kpi-card.red::before {{ background: var(--danger); }}
        .kpi-card.orange::before {{ background: var(--orange); }}
        .kpi-card.blue::before {{ background: var(--primary-light); }}
        
        .kpi-title {{ font-size: 13px; font-weight: 600; color: var(--text-muted); text-transform: uppercase; margin-bottom: 8px; }}
        .kpi-val {{ font-size: 32px; font-weight: 800; color: var(--text-main); margin-bottom: 6px; display: flex; align-items: baseline; gap: 8px; }}
        .kpi-sub {{ font-size: 13px; color: var(--text-muted); }}
        .kpi-badge {{
            display: inline-block;
            font-size: 11px;
            font-weight: 700;
            padding: 3px 8px;
            border-radius: 6px;
            margin-top: 10px;
        }}
        .kpi-badge.green {{ background: #dcfce7; color: #15803d; }}
        .kpi-badge.red {{ background: #fee2e2; color: #b91c1c; }}
        .kpi-badge.orange {{ background: #ffedd5; color: #c2410c; }}
        .kpi-badge.blue {{ background: #dbeafe; color: #1d4ed8; }}

        /* Charts Row */
        .charts-row {{
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 20px;
            margin-bottom: 24px;
        }}
        @media (max-width: 1024px) {{ .charts-row {{ grid-template-columns: 1fr; }} }}
        
        .chart-box {{
            background: var(--card-bg);
            border-radius: 14px;
            padding: 24px;
            border: 1px solid var(--border);
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
        }}
        .chart-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }}
        .chart-title {{ font-size: 16px; font-weight: 700; color: var(--text-main); }}
        .chart-sub {{ font-size: 13px; color: var(--text-muted); }}

        /* Table Card */
        .section-card {{
            background: var(--card-bg);
            border-radius: 14px;
            padding: 24px;
            border: 1px solid var(--border);
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
            margin-bottom: 24px;
        }}
        .section-header {{
            margin-bottom: 18px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 12px;
        }}
        .section-title {{ font-size: 18px; font-weight: 800; color: var(--text-main); display: flex; align-items: center; gap: 10px; }}
        
        /* Table Styles */
        .data-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }}
        .data-table th {{
            background: #f1f5f9;
            color: #475569;
            font-weight: 700;
            text-align: left;
            padding: 12px 14px;
            border-bottom: 2px solid var(--border);
            white-space: nowrap;
        }}
        .data-table td {{
            padding: 14px;
            border-bottom: 1px solid var(--border);
            vertical-align: middle;
        }}
        .data-table tr:hover td {{ background: #f8fafc; }}
        
        .progress-bar-bg {{
            background: #e2e8f0;
            border-radius: 8px;
            height: 8px;
            width: 100%;
            overflow: hidden;
            margin-top: 4px;
        }}
        .progress-bar-fill {{
            height: 100%;
            border-radius: 8px;
        }}
        
        /* Action Matrix Cards */
        .action-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(310px, 1fr));
            gap: 18px;
            margin-bottom: 24px;
        }}
        .action-card {{
            border-radius: 12px;
            padding: 20px;
            border: 1px solid var(--border);
            background: #ffffff;
        }}
        .action-card.red {{ border-top: 4px solid var(--danger); background: #fffafb; }}
        .action-card.orange {{ border-top: 4px solid var(--orange); background: #fffcf8; }}
        .action-card.blue {{ border-top: 4px solid var(--primary-light); background: #fbfdff; }}
        .action-card.green {{ border-top: 4px solid var(--success); background: #f9fdfa; }}
        
        .action-title {{ font-size: 15px; font-weight: 700; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; }}
        .action-body {{ font-size: 13px; color: #334155; margin-bottom: 14px; }}
        .action-meta {{
            border-top: 1px dashed var(--border);
            padding-top: 12px;
            font-size: 12px;
            display: flex;
            flex-direction: column;
            gap: 6px;
        }}
        .meta-row {{ display: flex; justify-content: space-between; }}
        .meta-label {{ color: var(--text-muted); font-weight: 600; }}
        .meta-value {{ font-weight: 700; }}

        /* Tag Badges */
        .tag {{
            display: inline-block;
            font-size: 11px;
            font-weight: 700;
            padding: 3px 8px;
            border-radius: 6px;
            white-space: nowrap;
        }}
        .tag-red {{ background: #fee2e2; color: #b91c1c; }}
        .tag-orange {{ background: #ffedd5; color: #c2410c; }}
        .tag-yellow {{ background: #fef3c7; color: #b45309; }}
        .tag-green {{ background: #dcfce7; color: #15803d; }}
        .tag-blue {{ background: #dbeafe; color: #1e40af; }}

        /* Toast notification */
        #toast {{
            visibility: hidden;
            min-width: 280px;
            background-color: #0f172a;
            color: #fff;
            text-align: center;
            border-radius: 8px;
            padding: 14px 20px;
            position: fixed;
            z-index: 1000;
            left: 50%;
            bottom: 30px;
            transform: translateX(-50%);
            font-size: 14px;
            font-weight: 600;
            box-shadow: 0 10px 15px -3px rgba(0,0,0,0.3);
        }}
        #toast.show {{
            visibility: visible;
            animation: fadein 0.4s, fadeout 0.4s 2.6s;
        }}
        @keyframes fadein {{ from {{ bottom: 0; opacity: 0; }} to {{ bottom: 30px; opacity: 1; }} }}
        @keyframes fadeout {{ from {{ bottom: 30px; opacity: 1; }} to {{ bottom: 0; opacity: 0; }} }}

        /* Screenshot Mode */
        body.screenshot-mode {{ padding: 40px; background: #ffffff; }}
        body.screenshot-mode .action-bar {{ display: none; }}
        body.screenshot-mode .container {{ max-width: 1600px; }}
        body.screenshot-mode .kpi-val {{ font-size: 40px; }}
        body.screenshot-mode .data-table {{ font-size: 15px; }}
    </style>
</head>
<body>

<div id="toast">📋 Đã sao chép tóm tắt gửi Giám đốc vào Clipboard!</div>

<div class="container">
    <!-- Header -->
    <div class="header">
        <div class="badge-sub">Báo Cáo Chuyên Đề Giám Đốc Đào Tạo</div>
        <h1>Chẩn Đoán Chuyển Dịch Hành Vi Tân Sinh Viên K26 & Kế Hoạch Tác Chiến 5-15 Phút</h1>
        <p>Báo cáo đối soát 2 chiều giữa Môn đầu tiên (SSK101 - Kỹ năng Học tập chủ động) và Các môn mới đang học (IT108, SKL01, ENG105, SSK102, SSK103). Phân rã tỷ lệ cải thiện 9 lớp và phân luồng giải pháp trực tiếp tại lớp.</p>
        
        <div class="action-bar">
            <button class="btn btn-primary" onclick="copyDirectorSummary()">
                <span>📋</span> Sao chép Tóm tắt gửi Giám đốc (Zalo/Slack)
            </button>
            <a href="K26_Theo_Doi_Chuyen_Dich_Hanh_Vi_Va_Giai_Phap.xlsx" download class="btn btn-success">
                <span>📥</span> Tải File Excel Tác Chiến 14 Sheet (.xlsx)
            </a>
            <button class="btn btn-outline" onclick="toggleScreenshotMode()">
                <span>📸</span> Chế độ Chụp Ảnh Màn Hình
            </button>
        </div>
    </div>

    <!-- 4 KPI Cards -->
    <div class="kpi-grid">
        <div class="kpi-card green">
            <div class="kpi-title">Tỷ Lệ Cải Thiện Toàn Khóa</div>
            <div class="kpi-val">{overall['overall_improvement_rate']}% <span style="font-size: 18px; color: var(--success);">▲ Xuất sắc</span></div>
            <div class="kpi-sub"><strong>{overall['th3_count'] + overall['th2_count']}</strong> / {overall['total_students']} sinh viên đã thích nghi tốt hoặc giảm vi phạm</div>
            <div class="kpi-badge green">Vượt qua bỡ ngỡ kỹ thuật LMS tuần đầu</div>
        </div>

        <div class="kpi-card blue">
            <div class="kpi-title">TH3: Sạch 100% Vi Phạm Môn Mới</div>
            <div class="kpi-val">{overall['th3_count']} <span style="font-size: 16px; color: var(--text-muted);">SV ({overall['th3_pct']}%)</span></div>
            <div class="kpi-sub">Tuần 1 vi phạm do chưa quen LMS, nay đạt chuẩn nề nếp</div>
            <div class="kpi-badge blue">Miễn can thiệp kỷ luật — Tuyên dương</div>
        </div>

        <div class="kpi-card red">
            <div class="kpi-title">TH1: Nguy Cơ Bỏ Học (Báo Động Đỏ)</div>
            <div class="kpi-val">{overall['th1_count']} <span style="font-size: 16px; color: var(--danger);">SV ({overall['th1_pct']}%)</span></div>
            <div class="kpi-sub">Vắng dai dẳng từ môn 1 sang môn mới (gồm 4 SV 0 buổi CC)</div>
            <div class="kpi-badge red">Gặp riêng 5p cuối giờ + Gọi Phụ huynh</div>
        </div>

        <div class="kpi-card orange">
            <div class="kpi-title">TH4: Sốc Môn Mới Chuyên Ngành</div>
            <div class="kpi-val">{overall['th4_count']} <span style="font-size: 16px; color: var(--orange);">SV ({overall['th4_pct']}%)</span></div>
            <div class="kpi-sub">Môn 1 tốt nhưng môn mới (IT108/ENG105) nợ bài/vắng</div>
            <div class="kpi-badge orange">GV bộ môn + Trợ giảng phụ đạo học thuật</div>
        </div>
    </div>

    <!-- Charts Row -->
    <div class="charts-row">
        <div class="chart-box">
            <div class="chart-header">
                <div>
                    <div class="chart-title">Bảng Xếp Hạng Tỷ Lệ Cải Thiện 9 Lớp K26 (%)</div>
                    <div class="chart-sub">Đo lường tỷ lệ sinh viên sạch lỗi (TH3) và đang tiến bộ (TH2) ở các môn học mới</div>
                </div>
            </div>
            <div style="height: 320px;">
                <canvas id="barChart"></canvas>
            </div>
        </div>

        <div class="chart-box">
            <div class="chart-header">
                <div>
                    <div class="chart-title">Cơ Cấu 4 Nhóm Hành Vi K26</div>
                    <div class="chart-sub">Tổng số 374 sinh viên trên 9 lớp</div>
                </div>
            </div>
            <div style="height: 320px; position: relative;">
                <canvas id="doughnutChart"></canvas>
            </div>
        </div>
    </div>

    <!-- Class Leaderboard Table -->
    <div class="section-card">
        <div class="section-header">
            <div>
                <div class="section-title">📊 Bảng Chỉ Số Cải Thiện & Điểm Nghẽn Môn Học Từng Lớp</div>
                <div style="color: var(--text-muted); font-size: 13px;">Dữ liệu đối chuẩn giữa Môn đầu tiên (SSK101) và Các môn mới đang học (IT108, SKL01, ENG105, SSK102, SSK103)</div>
            </div>
        </div>

        <div style="overflow-x: auto;">
            <table class="data-table">
                <thead>
                    <tr>
                        <th style="width: 50px;">Hạng</th>
                        <th>Lớp Học</th>
                        <th>Giảng Viên / CVHT</th>
                        <th style="text-align: center;">Sĩ Số</th>
                        <th style="width: 220px;">Tỷ Lệ Cải Thiện</th>
                        <th style="text-align: center;">TH3 (Sạch lỗi)</th>
                        <th style="text-align: center;">TH2 (Tiến bộ)</th>
                        <th style="text-align: center;">TH1 (Nguy cơ)</th>
                        <th style="text-align: center;">TH4 (Sốc môn)</th>
                        <th>Môn Gây Nghẽn</th>
                        <th>Ưu Tiên Tác Chiến 5-15p</th>
                    </tr>
                </thead>
                <tbody>
"""

    for idx, c in enumerate(classes, 1):
        color_fill = "#10b981" if c['improvement_rate'] >= 95 else ("#f59e0b" if c['improvement_rate'] >= 90 else "#ef4444")
        html_content += f"""
                    <tr>
                        <td style="font-weight: 700; text-align: center;">#{idx}</td>
                        <td style="font-weight: 700; color: #1e3a8a;">{c['class']}</td>
                        <td>{c['teacher']}</td>
                        <td style="text-align: center; font-weight: 600;">{c['total']}</td>
                        <td>
                            <div style="display: flex; justify-content: space-between; font-weight: 700; font-size: 12px; margin-bottom: 2px;">
                                <span>{c['improvement_rate']}%</span>
                                <span style="color: var(--text-muted); font-weight: 500;">{c['improvement_count']}/{c['total']} SV</span>
                            </div>
                            <div class="progress-bar-bg">
                                <div class="progress-bar-fill" style="width: {c['improvement_rate']}%; background: {color_fill};"></div>
                            </div>
                        </td>
                        <td style="text-align: center;"><span class="tag tag-green">{c['th3_count']} ({c['th3_pct']}%)</span></td>
                        <td style="text-align: center;"><span class="tag tag-blue">{c['th2_count']} ({c['th2_pct']}%)</span></td>
                        <td style="text-align: center;"><span class="tag tag-red">{c['th1_count']} ({c['th1_pct']}%)</span></td>
                        <td style="text-align: center;"><span class="tag tag-orange">{c['th4_count']} ({c['th4_pct']}%)</span></td>
                        <td style="font-size: 12px; font-weight: 600; color: #475569;">{c['bottleneck_course']}</td>
                        <td><span class="tag {'tag-red' if '🚨' in c['priority'] else ('tag-yellow' if '🟡' in c['priority'] else 'tag-green')}">{c['priority']}</span></td>
                    </tr>
"""

    html_content += f"""
                    <tr style="background: #f1f5f9; font-weight: 800;">
                        <td style="text-align: center;">--</td>
                        <td>TOÀN KHÓA K26</td>
                        <td>Tất cả Giảng viên</td>
                        <td style="text-align: center;">{overall['total_students']}</td>
                        <td>
                            <div style="display: flex; justify-content: space-between; font-size: 13px;">
                                <span>{overall['overall_improvement_rate']}%</span>
                                <span>{overall['th3_count'] + overall['th2_count']}/{overall['total_students']} SV</span>
                            </div>
                            <div class="progress-bar-bg">
                                <div class="progress-bar-fill" style="width: {overall['overall_improvement_rate']}%; background: #10b981;"></div>
                            </div>
                        </td>
                        <td style="text-align: center;"><span class="tag tag-green">{overall['th3_count']} ({overall['th3_pct']}%)</span></td>
                        <td style="text-align: center;"><span class="tag tag-blue">{overall['th2_count']} ({overall['th2_pct']}%)</span></td>
                        <td style="text-align: center;"><span class="tag tag-red">{overall['th1_count']} ({overall['th1_pct']}%)</span></td>
                        <td style="text-align: center;"><span class="tag tag-orange">{overall['th4_count']} ({overall['th4_pct']}%)</span></td>
                        <td style="font-size: 12px;">IT108 / ENG105</td>
                        <td><span class="tag tag-blue">Vào trực tiếp 9 lớp 5-15p</span></td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>

    <!-- Action Matrix Cards (4 Streams) -->
    <div class="section-card">
        <div class="section-header">
            <div>
                <div class="section-title">🎯 Kế Hoạch Tác Chiến 5-15 Phút Trực Tiếp Tại Lớp (Phân Luồng PIC & Deadline)</div>
                <div style="color: var(--text-muted); font-size: 13px;">Giải pháp cụ thể cho từng nhóm, giải quyết triệt để tình trạng trốn họp online và lãng phí nguồn lực</div>
            </div>
        </div>

        <div class="action-grid">
            <div class="action-card red">
                <div class="action-title" style="color: var(--danger);">
                    <span>🔴 STREAM 1: BÁO ĐỘNG ĐỎ</span>
                    <span class="tag tag-red">{len(th1_students)} SV</span>
                </div>
                <div class="action-body">
                    <strong>Bản chất:</strong> Nguy cơ bỏ học, mất động lực, vắng mặt kéo dài từ môn 1 sang môn 2.<br><br>
                    <strong>Giải pháp 5p tại lớp:</strong> Gặp riêng 5 phút cuối giờ, yêu cầu ký cam kết nề nếp. Nếu không chuyển biến &rarr; Gọi điện thoại 1-1 cho Phụ huynh.
                </div>
                <div class="action-meta">
                    <div class="meta-row"><span class="meta-label">Người phụ trách (PIC):</span><span class="meta-value" style="color: #b91c1c;">Quản lý Đào tạo + CVHT</span></div>
                    <div class="meta-row"><span class="meta-label">Hạn chót giải quyết:</span><span class="meta-value">Trong 48 giờ tới</span></div>
                    <div class="meta-row"><span class="meta-label">Hình thức:</span><span class="meta-value">Trực tiếp cuối giờ + Gọi PH</span></div>
                </div>
            </div>

            <div class="action-card orange">
                <div class="action-title" style="color: var(--orange);">
                    <span>🟠 STREAM 2: HỖ TRỢ HỌC THUẬT</span>
                    <span class="tag tag-orange">{len(th4_students)} SV</span>
                </div>
                <div class="action-body">
                    <strong>Bản chất:</strong> Môn 1 học tốt nhưng môn mới (IT108 Nhập môn CNTT, ENG105) nợ bài tập/vắng do sốc độ khó.<br><br>
                    <strong>Giải pháp 5p tại lớp:</strong> Gặp 5 phút giữa giờ, làm rõ nội dung lý thuyết/bài tập chưa hiểu, bàn giao cho Trợ giảng kèm cặp (Peer Tutoring).
                </div>
                <div class="action-meta">
                    <div class="meta-row"><span class="meta-label">Người phụ trách (PIC):</span><span class="meta-value" style="color: #c2410c;">GV Bộ Môn + Trợ giảng</span></div>
                    <div class="meta-row"><span class="meta-label">Hạn chót giải quyết:</span><span class="meta-value">Trước buổi học kế tiếp</span></div>
                    <div class="meta-row"><span class="meta-label">Hình thức:</span><span class="meta-value">Trực tiếp giữa giờ + Kèm cặp</span></div>
                </div>
            </div>

            <div class="action-card blue">
                <div class="action-title" style="color: var(--primary-light);">
                    <span>🟡 STREAM 3: ĐÔN ĐỐC NỀ NẾP</span>
                    <span class="tag tag-blue">{len(th2_students)} SV</span>
                </div>
                <div class="action-body">
                    <strong>Bản chất:</strong> Đã có ý thức nỗ lực và giảm vi phạm rõ rệt so với môn đầu, chỉ còn sót nhẹ Elearning.<br><br>
                    <strong>Giải pháp 3p tại lớp:</strong> Gặp nhanh 3 phút đầu giờ: Biểu dương sự tiến bộ trước lớp, nhắc nhở nộp bài đúng hạn để giữ vững nề nếp.
                </div>
                <div class="action-meta">
                    <div class="meta-row"><span class="meta-label">Người phụ trách (PIC):</span><span class="meta-value" style="color: #1e40af;">CVHT lớp</span></div>
                    <div class="meta-row"><span class="meta-label">Hạn chót giải quyết:</span><span class="meta-value">Hết tuần này</span></div>
                    <div class="meta-row"><span class="meta-label">Hình thức:</span><span class="meta-value">Trực tiếp đầu giờ</span></div>
                </div>
            </div>

            <div class="action-card green">
                <div class="action-title" style="color: var(--success);">
                    <span>🟢 STREAM 4: BIỂU DƯƠNG</span>
                    <span class="tag tag-green">{len(th3_students)} SV</span>
                </div>
                <div class="action-body">
                    <strong>Bản chất:</strong> Lỗi tuần 1 thuần túy do bỡ ngỡ kỹ thuật LMS, sang môn mới đã đạt chuẩn 100% nề nếp.<br><br>
                    <strong>Hành động:</strong> Miễn can thiệp kỷ luật. Gửi thông báo chúc mừng và ghi nhận sự thích nghi xuất sắc qua nhóm Zalo lớp.
                </div>
                <div class="action-meta">
                    <div class="meta-row"><span class="meta-label">Người phụ trách (PIC):</span><span class="meta-value" style="color: #15803d;">CVHT lớp</span></div>
                    <div class="meta-row"><span class="meta-label">Hạn chót giải quyết:</span><span class="meta-value">Hoàn thành ngay</span></div>
                    <div class="meta-row"><span class="meta-label">Hình thức:</span><span class="meta-value">Nhắn tin Zalo lớp</span></div>
                </div>
            </div>
        </div>
    </div>

    <!-- Focus Student List (5 TH1 + 13 TH4) -->
    <div class="section-card">
        <div class="section-header">
            <div>
                <div class="section-title">🚨 Danh Sách 18 Sinh Viên Trọng Tâm Cần Can Thiệp Tại Lớp (5 SV TH1 & 13 SV TH4)</div>
                <div style="color: var(--text-muted); font-size: 13px;">Danh sách ưu tiên cao nhất để Quản lý Đào tạo và Giảng viên xử lý dứt điểm trong tuần</div>
            </div>
        </div>

        <div style="overflow-x: auto;">
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Nhóm</th>
                        <th>Mã SV</th>
                        <th>Họ và Tên</th>
                        <th>Lớp</th>
                        <th>Vi Phạm Môn 1</th>
                        <th>Vi Phạm Môn Mới</th>
                        <th>Vấn Đề Gặp Phải</th>
                        <th>Kế Hoạch Tác Chiến 5-15p</th>
                        <th>PIC</th>
                        <th>Hạn Chót</th>
                    </tr>
                </thead>
                <tbody>
"""

    urgent_students = th1_students + th4_students
    for s in urgent_students:
        is_th1 = s['group'] == 'TH1_PERSISTENT_RISK'
        tag_cls = 'tag-red' if is_th1 else 'tag-orange'
        group_badge = 'TH1: Báo Động Đỏ' if is_th1 else 'TH4: Sốc Môn Mới'
        m1_str = f"CC {s['m1_att_violate']}% | BT {s['m1_hw_violate']}% | EL {s['m1_el_violate']}%"
        m2_str = f"CC {s['new_att_violate']}% | BT {s['new_hw_violate']}% | EL {s['new_el_violate']}%"
        
        html_content += f"""
                    <tr>
                        <td><span class="tag {tag_cls}">{group_badge}</span></td>
                        <td style="font-weight: 600; font-family: monospace;">{s['code']}</td>
                        <td style="font-weight: 700;">{s['name']}</td>
                        <td style="font-weight: 600; color: #1e3a8a;">{s['class']}</td>
                        <td style="font-size: 12px; color: #64748b;">{m1_str}</td>
                        <td style="font-size: 12px; font-weight: 700; color: {'#b91c1c' if is_th1 else '#c2410c'};">{m2_str}</td>
                        <td style="font-size: 12px;">{s['problem']}</td>
                        <td style="font-size: 12px; font-weight: 600;">{s['solution']}</td>
                        <td style="font-size: 12px; font-weight: 700;">{s['pic']}</td>
                        <td style="font-size: 12px; font-weight: 600; color: #dc2626;">{s['deadline']}</td>
                    </tr>
"""

    html_content += f"""
                </tbody>
            </table>
        </div>
    </div>
</div>

<script>
    // 1-Click Copy
    function copyDirectorSummary() {{
        const text = `{summary_text}`;
        navigator.clipboard.writeText(text).then(() => {{
            const toast = document.getElementById("toast");
            toast.className = "show";
            setTimeout(() => {{ toast.className = toast.className.replace("show", ""); }}, 3000);
        }}).catch(err => {{
            alert("Lỗi khi sao chép: " + err);
        }});
    }}

    // Toggle Screenshot Mode
    function toggleScreenshotMode() {{
        document.body.classList.toggle('screenshot-mode');
    }}

    // Horizontal Bar Chart
    const ctxBar = document.getElementById('barChart').getContext('2d');
    new Chart(ctxBar, {{
        type: 'bar',
        data: {{
            labels: {json.dumps(class_labels, ensure_ascii=False)},
            datasets: [{{
                label: 'Tỷ lệ Cải thiện (%)',
                data: {json.dumps(class_rates)},
                backgroundColor: {json.dumps([
                    '#10b981' if r >= 95 else ('#f59e0b' if r >= 90 else '#ef4444')
                    for r in class_rates
                ])},
                borderRadius: 6
            }}]
        }},
        options: {{
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {{
                legend: {{ display: false }},
                tooltip: {{
                    callbacks: {{
                        label: function(context) {{
                            return 'Tỷ lệ Cải thiện: ' + context.raw + '%';
                        }}
                    }}
                }}
            }},
            scales: {{
                x: {{
                    min: 60,
                    max: 100,
                    ticks: {{ callback: value => value + '%' }},
                    grid: {{ color: '#f1f5f9' }}
                }},
                y: {{
                    grid: {{ display: false }}
                }}
            }}
        }}
    }});

    // Doughnut Chart
    const ctxDoughnut = document.getElementById('doughnutChart').getContext('2d');
    new Chart(ctxDoughnut, {{
        type: 'doughnut',
        data: {{
            labels: [
                'TH3: Sạch vi phạm môn mới ({overall['th3_pct']}%)',
                'TH2: Đang tiến bộ ({overall['th2_pct']}%)',
                'TH4: Sốc môn mới ({overall['th4_pct']}%)',
                'TH1: Nguy cơ bỏ học ({overall['th1_pct']}%)'
            ],
            datasets: [{{
                data: [{overall['th3_count']}, {overall['th2_count']}, {overall['th4_count']}, {overall['th1_count']}],
                backgroundColor: ['#10b981', '#3b82f6', '#f97316', '#ef4444'],
                borderWidth: 2,
                borderColor: '#ffffff'
            }}]
        }},
        options: {{
            responsive: true,
            maintainAspectRatio: false,
            plugins: {{
                legend: {{
                    position: 'bottom',
                    labels: {{ boxWidth: 12, font: {{ size: 11 }} }}
                }}
            }},
            cutout: '65%'
        }}
    }});
</script>

</body>
</html>
"""

    output_path = "output/dashboards/management/bao_cao_k26_chuyen_dich_hanh_vi.html"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Đã tạo thành công Dashboard HTML tại: {output_path}")
    
    # Deploy to deploy_web/
    os.makedirs("deploy_web/management", exist_ok=True)
    shutil.copy(output_path, "deploy_web/management/bao_cao_k26_chuyen_dich_hanh_vi.html")
    shutil.copy(output_path, "deploy_web/bao_cao_k26_chuyen_dich_hanh_vi.html")
    print("Đã đồng bộ sang deploy_web/ và deploy_web/management/")

if __name__ == '__main__':
    main()
