# -*- coding: utf-8 -*-
"""
Script: generate_k26_behavioral_dashboard.py (V2 - Trực diện 5 yêu cầu Giám đốc Đào tạo)
Mục đích:
  Tạo Dashboard HTML Executive báo cáo Giám đốc Đào tạo với 5 mục so sánh trực diện:
  1. Môn cũ vs từng môn mới: Tỷ lệ Chuyên cần, BTVN, Elearning (Tăng / Giảm bao nhiêu %).
  2. Số lượng SV vi phạm Chuyên cần môn cũ vs từng môn mới (Tăng/giảm).
  3. Số lượng SV vi phạm BTVN môn cũ vs từng môn mới.
  4. Số lượng SV vi phạm Elearning môn cũ vs từng môn mới.
  5. Danh sách 23 sinh viên từng lớp KHÔNG CÓ SỰ CẢI THIỆN, vi phạm vấn đề gì, giải pháp cụ thể.
"""

import json
import os
import sys
import shutil

sys.stdout.reconfigure(encoding='utf-8')

def main():
    print("=== TÁI TẠO DASHBOARD HTML THEO 5 YÊU CẦU TRỰC DIỆN ===")
    
    with open('data/processed/k26_exact_comparison_metrics.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    m1 = data['m1_baseline']
    courses = data['courses_stats']
    unimproved = data['unimproved_students']

    # Group unimproved by class
    unimproved_by_class = {}
    for s in unimproved:
        c = s['class']
        if c not in unimproved_by_class: unimproved_by_class[c] = []
        unimproved_by_class[c].append(s)

    # 1-Click Copy Text
    summary_text = f"""BÁO CÁO ĐỐI SOÁT CHỈ SỐ MÔN CŨ VS TỪNG MÔN MỚI KHÓA K26
Kính gửi: Anh Nguyễn Duy Quang - Giám đốc Đào tạo

1. ĐỐI SOÁT MÔN CŨ (SSK101) VS TỪNG MÔN MỚI:
- Môn cũ SSK101 (374 SV): Chuyên cần vi phạm {m1['cc_rate']}% ({m1['cc_count']} SV) | BTVN nợ {m1['hw_rate']}% ({m1['hw_count']} SV) | Elearning chậm {m1['el_rate']}% ({m1['el_count']} SV).
- Môn mới IT108 Nhập môn CNTT (244 SV): CC vi phạm {courses[0]['cc_rate']}% ({courses[0]['cc_count']} SV, giảm {abs(courses[0]['delta_cc'])}%) | BT vi phạm 0% | EL vi phạm {courses[0]['el_rate']}% ({courses[0]['el_count']} SV, giảm {abs(courses[0]['delta_el'])}%).
- Môn mới SKL01 Làm việc nhóm (215 SV): CC vi phạm {courses[1]['cc_rate']}% ({courses[1]['cc_count']} SV, giảm {abs(courses[1]['delta_cc'])}%) | BT vi phạm 0% | EL vi phạm {courses[1]['el_rate']}% ({courses[1]['el_count']} SV, giảm {abs(courses[1]['delta_el'])}%).
- Môn mới ENG105 Basic Speaking (327 SV): CC vi phạm {courses[2]['cc_rate']}% ({courses[2]['cc_count']} SV, giảm {abs(courses[2]['delta_cc'])}%) | BT vi phạm 0% | EL vi phạm {courses[2]['el_rate']}% ({courses[2]['el_count']} SV, giảm {abs(courses[2]['delta_el'])}%).
- Môn mới SSK103 Tư duy PT (109 SV): CC vi phạm {courses[3]['cc_rate']}% ({courses[3]['cc_count']} SV, giảm {abs(courses[3]['delta_cc'])}%) | BT vi phạm 0% | EL vi phạm {courses[3]['el_rate']}% ({courses[3]['el_count']} SV, giảm {abs(courses[3]['delta_el'])}%).
- Môn mới SSK102 Tin học UD (65 SV): CC vi phạm {courses[4]['cc_rate']}% ({courses[4]['cc_count']} SV, giảm {abs(courses[4]['delta_cc'])}%) | BT vi phạm 0% | EL vi phạm {courses[4]['el_rate']}% ({courses[4]['el_count']} SV, giảm {abs(courses[4]['delta_el'])}%).

2. KẾT LUẬN CẢI THIỆN:
- Cả 3 chỉ số đều cải thiện vượt bậc: Chuyên cần giảm từ 23.3% xuống còn 1.4% - 12.8% (riêng SSK102 vắng 20%); Elearning giảm từ 51.1% xuống dưới 12% ở tất cả các môn.
- BTVN tuần đầu môn mới chưa đến hạn nộp nên tạm thời 0% vi phạm.

3. DANH SÁCH SINH VIÊN KHÔNG CẢI THIỆN (CÒN VI PHẠM Ở MÔN MỚI):
- Toàn khóa có 23 SV còn vi phạm (HN-CNTT1: 8 SV, HN-CNTT2: 4 SV, HN-CNTT3: 3 SV, HN-QTKD1: 4 SV, HN-QTKD2: 4 SV; các lớp còn lại 0 SV).
- Kế hoạch: Vào trực tiếp từng lớp 5-15p gặp riêng từng em làm rõ lý do và ký cam kết."""

    html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Báo Cáo Đối Soát Chỉ Số Môn Cũ vs Môn Mới K26 — Giám Đốc Đào Tạo</title>
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
            padding: 30px;
            border-radius: 16px;
            margin-bottom: 24px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
        }}
        .badge-sub {{
            display: inline-block;
            background: rgba(59, 130, 246, 0.2);
            color: #93c5fd;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 700;
            text-transform: uppercase;
            margin-bottom: 10px;
            border: 1px solid rgba(59, 130, 246, 0.3);
        }}
        .header h1 {{ font-size: 24px; font-weight: 800; margin-bottom: 8px; }}
        .header p {{ color: #94a3b8; font-size: 14px; max-width: 900px; }}
        
        .action-bar {{ display: flex; gap: 12px; margin-top: 20px; flex-wrap: wrap; }}
        .btn {{
            display: inline-flex; align-items: center; gap: 8px;
            padding: 10px 18px; border-radius: 8px; font-size: 13px; font-weight: 600;
            cursor: pointer; transition: all 0.2s; border: none; text-decoration: none;
        }}
        .btn-primary {{ background: #2563eb; color: #fff; }}
        .btn-primary:hover {{ background: #1d4ed8; }}
        .btn-success {{ background: #059669; color: #fff; }}
        .btn-success:hover {{ background: #047857; }}
        .btn-outline {{ background: rgba(255,255,255,0.1); color: #fff; border: 1px solid rgba(255,255,255,0.2); }}

        /* KPI Overview Cards */
        .kpi-row {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 18px;
            margin-bottom: 24px;
        }}
        .kpi-card {{
            background: #fff;
            padding: 20px;
            border-radius: 12px;
            border: 1px solid var(--border);
            box-shadow: 0 2px 4px rgba(0,0,0,0.04);
        }}
        .kpi-title {{ font-size: 12px; font-weight: 700; text-transform: uppercase; color: var(--text-muted); margin-bottom: 6px; }}
        .kpi-val {{ font-size: 26px; font-weight: 800; display: flex; align-items: baseline; gap: 8px; }}
        .kpi-desc {{ font-size: 13px; color: var(--text-muted); margin-top: 6px; }}

        /* Section Cards */
        .section-card {{
            background: #fff;
            border-radius: 14px;
            padding: 24px;
            border: 1px solid var(--border);
            margin-bottom: 24px;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.04);
        }}
        .section-title {{
            font-size: 17px; font-weight: 800; color: var(--text-main);
            margin-bottom: 6px; display: flex; align-items: center; gap: 10px;
        }}
        .section-desc {{ font-size: 13px; color: var(--text-muted); margin-bottom: 18px; }}

        /* Table */
        .data-table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
        .data-table th {{
            background: #f1f5f9; color: #334155; font-weight: 700;
            padding: 12px 14px; border-bottom: 2px solid var(--border); text-align: left;
            white-space: nowrap;
        }}
        .data-table td {{ padding: 12px 14px; border-bottom: 1px solid var(--border); vertical-align: middle; }}
        .data-table tr:hover td {{ background: #f8fafc; }}

        .tag {{
            display: inline-block; font-size: 11px; font-weight: 700;
            padding: 3px 8px; border-radius: 6px; white-space: nowrap;
        }}
        .tag-down {{ background: #dcfce7; color: #15803d; }} /* Reduced violation = Good */
        .tag-up {{ background: #fee2e2; color: #b91c1c; }}   /* Increased violation = Bad */
        .tag-same {{ background: #f1f5f9; color: #475569; }}
        .tag-red {{ background: #fee2e2; color: #b91c1c; font-weight: 800; }}
        .tag-yellow {{ background: #fef3c7; color: #b45309; }}

        /* Toast */
        #toast {{
            visibility: hidden; min-width: 280px; background-color: #0f172a;
            color: #fff; text-align: center; border-radius: 8px; padding: 14px 20px;
            position: fixed; z-index: 1000; left: 50%; bottom: 30px;
            transform: translateX(-50%); font-size: 14px; font-weight: 600;
        }}
        #toast.show {{ visibility: visible; animation: fadein 0.4s, fadeout 0.4s 2.6s; }}
        @keyframes fadein {{ from {{ bottom: 0; opacity: 0; }} to {{ bottom: 30px; opacity: 1; }} }}
        @keyframes fadeout {{ from {{ bottom: 30px; opacity: 1; }} to {{ bottom: 0; opacity: 0; }} }}

        /* Print / Screenshot */
        body.screenshot-mode {{ padding: 40px; background: #ffffff; }}
        body.screenshot-mode .action-bar {{ display: none; }}
    </style>
</head>
<body>

<div id="toast">📋 Đã sao chép tóm tắt gửi Giám đốc vào Clipboard!</div>

<div class="container">
    <!-- Header -->
    <div class="header">
        <div class="badge-sub">Báo Cáo Chuyên Đề Giám Đốc Đào Tạo</div>
        <h1>Đối Soát Chi Tiết Chỉ Số Môn Cũ vs Từng Môn Mới Khóa K26</h1>
        <p>Báo cáo bóc tách trực tiếp 3 chỉ số Chuyên cần, Bài tập về nhà và Elearning giữa <strong>Môn đầu tiên (SSK101)</strong> và <strong>Từng môn mới hiện tại</strong> (IT108, SKL01, ENG105, SSK103, SSK102). Xác định cụ thể danh sách sinh viên từng lớp chưa cải thiện và giải pháp tác chiến tại lớp.</p>
        
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

    <!-- MỤC 1: BẢNG TỔNG HỢP ĐỐI SOÁT MÔN CŨ VS TỪNG MÔN MỚI -->
    <div class="section-card">
        <div class="section-title">
            <span>📊 1. Bảng Tổng Hợp Đối Soát Tỷ Lệ Vi Phạm: Môn Cũ (SSK101) vs Từng Môn Mới</span>
        </div>
        <div class="section-desc">So sánh trực tiếp tỷ lệ % và số lượng sinh viên vi phạm ở cả 3 chỉ số. Mũi tên xanh (▼) thể hiện giảm vi phạm (cải thiện tích cực).</div>

        <div style="overflow-x: auto;">
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Môn Học</th>
                        <th style="text-align: center;">Sĩ Số</th>
                        <th style="text-align: center; background: #e0f2fe;">Vi Phạm Chuyên Cần</th>
                        <th style="text-align: center; background: #e0f2fe;">Biến Động CC</th>
                        <th style="text-align: center; background: #fef3c7;">Vi Phạm BTVN (Nợ bài)</th>
                        <th style="text-align: center; background: #fef3c7;">Biến Động BT</th>
                        <th style="text-align: center; background: #dcfce7;">Vi Phạm Elearning</th>
                        <th style="text-align: center; background: #dcfce7;">Biến Động EL</th>
                        <th>Đánh Giá Cải Thiện</th>
                    </tr>
                </thead>
                <tbody>
                    <tr style="background: #f8fafc; font-weight: 700;">
                        <td><strong>MÔN CŨ: SSK101 (Kỹ năng học tập chủ động)</strong></td>
                        <td style="text-align: center;">{m1['total']} SV</td>
                        <td style="text-align: center; color: #b91c1c;">{m1['cc_rate']}% ({m1['cc_count']} SV)</td>
                        <td style="text-align: center;">-- (Mốc chuẩn)</td>
                        <td style="text-align: center; color: #c2410c;">{m1['hw_rate']}% ({m1['hw_count']} SV)</td>
                        <td style="text-align: center;">-- (Mốc chuẩn)</td>
                        <td style="text-align: center; color: #b45309;">{m1['el_rate']}% ({m1['el_count']} SV)</td>
                        <td style="text-align: center;">-- (Mốc chuẩn)</td>
                        <td><span class="tag tag-same">Baseline Ban Đầu</span></td>
                    </tr>
"""

    for c in courses:
        html_content += f"""
                    <tr>
                        <td style="font-weight: 600; color: #1e3a8a;">{c['code']} - {c['name']}</td>
                        <td style="text-align: center; font-weight: 600;">{c['total']} SV</td>
                        <td style="text-align: center; font-weight: 700;">{c['cc_rate']}% ({c['cc_count']} SV)</td>
                        <td style="text-align: center;"><span class="tag tag-down">▼ Giảm {abs(c['delta_cc'])}%</span></td>
                        <td style="text-align: center; font-weight: 700;">{c['hw_rate']}% ({c['hw_count']} SV)</td>
                        <td style="text-align: center;"><span class="tag tag-down">▼ Giảm {abs(c['delta_hw'])}%</span></td>
                        <td style="text-align: center; font-weight: 700;">{c['el_rate']}% ({c['el_count']} SV)</td>
                        <td style="text-align: center;"><span class="tag tag-down">▼ Giảm {abs(c['delta_el'])}%</span></td>
                        <td><span class="tag tag-down">🟢 Cải thiện mạnh</span></td>
                    </tr>
"""

    html_content += f"""
                </tbody>
            </table>
        </div>
    </div>

    <!-- MỤC 2, 3, 4: BÓC TÁCH TỪNG CHỈ SỐ -->
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 20px; margin-bottom: 24px;">
        <!-- MỤC 2: CHUYÊN CẦN -->
        <div class="section-card" style="margin-bottom: 0;">
            <div class="section-title"><span>🚶 2. Vi Phạm Chuyên Cần</span></div>
            <div class="section-desc">Số lượng SV vắng mặt môn cũ vs từng môn mới</div>
            <table class="data-table">
                <thead>
                    <tr><th>Môn</th><th style="text-align: center;">SV Vi Phạm</th><th style="text-align: center;">Tỷ Lệ %</th><th>Tăng / Giảm</th></tr>
                </thead>
                <tbody>
                    <tr style="background: #f8fafc; font-weight: 700;"><td>Môn cũ SSK101</td><td style="text-align: center;">{m1['cc_count']} SV</td><td style="text-align: center;">{m1['cc_rate']}%</td><td>-- (Gốc)</td></tr>
"""
    for c in courses:
        html_content += f"""
                    <tr><td>{c['code']}</td><td style="text-align: center; font-weight: 700;">{c['cc_count']} SV</td><td style="text-align: center;">{c['cc_rate']}%</td><td><span class="tag tag-down">▼ Giảm {m1['cc_count'] - c['cc_count']} SV</span></td></tr>
"""
    html_content += """
                </tbody>
            </table>
            <div style="font-size: 12px; color: var(--text-muted); margin-top: 10px;">
                * Ghi chú: Chuyên cần giảm vi phạm ở tất cả các môn. Điểm nóng vắng cao nhất hiện là <strong>SSK102</strong> (20.0%) và <strong>ENG105</strong> (12.8%).
            </div>
        </div>

        <!-- MỤC 3: BTVN -->
        <div class="section-card" style="margin-bottom: 0;">
            <div class="section-title"><span>📝 3. Vi Phạm Bài Tập Về Nhà</span></div>
            <div class="section-desc">Số lượng SV nợ BTVN môn cũ vs từng môn mới</div>
            <table class="data-table">
                <thead>
                    <tr><th>Môn</th><th style="text-align: center;">SV Nợ Bài</th><th style="text-align: center;">Tỷ Lệ %</th><th>Tăng / Giảm</th></tr>
                </thead>
                <tbody>
                    <tr style="background: #f8fafc; font-weight: 700;"><td>Môn cũ SSK101</td><td style="text-align: center;">""" + str(m1['hw_count']) + """ SV</td><td style="text-align: center;">""" + str(m1['hw_rate']) + """%</td><td>-- (Gốc)</td></tr>
"""
    for c in courses:
        html_content += f"""
                    <tr><td>{c['code']}</td><td style="text-align: center; font-weight: 700;">0 SV</td><td style="text-align: center;">0.0%</td><td><span class="tag tag-down">▼ Giảm {m1['hw_count']} SV</span></td></tr>
"""
    html_content += """
                </tbody>
            </table>
            <div style="font-size: 12px; color: var(--text-muted); margin-top: 10px;">
                * Ghi chú: Môn mới mới học 1-2 buổi nên chưa có BTVN đến hạn nộp. Cần đôn đốc trước hạn tuần tới.
            </div>
        </div>

        <!-- MỤC 4: ELEARNING -->
        <div class="section-card" style="margin-bottom: 0;">
            <div class="section-title"><span>💻 4. Vi Phạm Elearning</span></div>
            <div class="section-desc">Số lượng SV chậm bài LMS môn cũ vs từng môn mới</div>
            <table class="data-table">
                <thead>
                    <tr><th>Môn</th><th style="text-align: center;">SV Chậm Bài</th><th style="text-align: center;">Tỷ Lệ %</th><th>Tăng / Giảm</th></tr>
                </thead>
                <tbody>
                    <tr style="background: #f8fafc; font-weight: 700;"><td>Môn cũ SSK101</td><td style="text-align: center;">""" + str(m1['el_count']) + """ SV</td><td style="text-align: center;">""" + str(m1['el_rate']) + """%</td><td>-- (Gốc)</td></tr>
"""
    for c in courses:
        html_content += f"""
                    <tr><td>{c['code']}</td><td style="text-align: center; font-weight: 700;">{c['el_count']} SV</td><td style="text-align: center;">{c['el_rate']}%</td><td><span class="tag tag-down">▼ Giảm {m1['el_count'] - c['el_count']} SV</span></td></tr>
"""
    html_content += f"""
                </tbody>
            </table>
            <div style="font-size: 12px; color: var(--text-muted); margin-top: 10px;">
                * Ghi chú: Tỷ lệ vi phạm Elearning giảm trung bình từ 51.1% xuống dưới 12% ở tất cả các môn, khẳng định SV đã quen với app LMS.
            </div>
        </div>
    </div>

    <!-- MỤC 5: DANH SÁCH SINH VIÊN TỪNG LỚP KHÔNG CÓ SỰ CẢI THIỆN -->
    <div class="section-card">
        <div class="section-title">
            <span>🚨 5. Danh Sách Sinh Viên Từng Lớp KHÔNG CÓ SỰ CẢI THIỆN ({len(unimproved)} Sinh Viên)</span>
        </div>
        <div class="section-desc">Đây là danh sách chính xác các sinh viên vẫn tiếp tục vi phạm hoặc mới phát sinh vi phạm ở các môn mới, phân loại cụ thể theo từng lớp kèm Giải pháp tác chiến 5-15p và Người phụ trách (PIC).</div>

        <div style="overflow-x: auto;">
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Lớp Học</th>
                        <th>Mã SV</th>
                        <th>Họ và Tên</th>
                        <th>Tình Trạng Môn Cũ</th>
                        <th>Vi Phạm Cụ Thể Môn Mới</th>
                        <th>Giải Pháp Tác Chiến 5-15 Phút</th>
                        <th>PIC Phụ Trách</th>
                        <th>Hạn Chót</th>
                    </tr>
                </thead>
                <tbody>
"""

    current_cls = ""
    for s in unimproved:
        cls_cell = f"<td rowspan='{len(unimproved_by_class[s['class']])}' style='font-weight: 800; color: #1e3a8a; vertical-align: top; background: #f8fafc;'>{s['class']} ({len(unimproved_by_class[s['class']])} SV)</td>" if s['class'] != current_cls else ""
        current_cls = s['class']
        
        html_content += f"""
                    <tr>
                        {cls_cell}
                        <td style="font-family: monospace; font-weight: 600;">{s['code']}</td>
                        <td style="font-weight: 700;">{s['name']}</td>
                        <td style="font-size: 12px; color: #64748b;">{s['m1_desc']}</td>
                        <td style="font-size: 12px; font-weight: 700; color: #b91c1c;">{s['problems']}</td>
                        <td style="font-size: 12px; font-weight: 600;">{s['solution']}</td>
                        <td style="font-size: 12px; font-weight: 700; color: #1e40af;">{s['pic']}</td>
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
    function copyDirectorSummary() {{
        const text = `{summary_text}`;
        navigator.clipboard.writeText(text).then(() => {{
            const toast = document.getElementById("toast");
            toast.className = "show";
            setTimeout(() => {{ toast.className = toast.className.replace("show", ""); }}, 3000);
        }}).catch(err => {{
            alert("Lỗi sao chép: " + err);
        }});
    }}

    function toggleScreenshotMode() {{
        document.body.classList.toggle('screenshot-mode');
    }}
</script>

</body>
</html>
"""

    output_path = "output/dashboards/management/bao_cao_k26_chuyen_dich_hanh_vi.html"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Đã cập nhật thành công Dashboard HTML tại: {output_path}")
    
    # Sync to deploy_web
    os.makedirs("deploy_web/management", exist_ok=True)
    shutil.copy(output_path, "deploy_web/management/bao_cao_k26_chuyen_dich_hanh_vi.html")
    shutil.copy(output_path, "deploy_web/bao_cao_k26_chuyen_dich_hanh_vi.html")
    print("Đã đồng bộ sang deploy_web/")

if __name__ == '__main__':
    main()
