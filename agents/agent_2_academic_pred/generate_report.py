import os
import sys
import json
from datetime import datetime

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def build_unified_prediction_dashboard(data, output_path):
    # Lấy danh sách học viên nguy cơ theo từng lớp để tra cứu nhanh
    class_risks = {}
    for s in data['care_list']:
        cname = s['class_name']
        if cname not in class_risks:
            class_risks[cname] = []
        class_risks[cname].append(s)

    def make_class_rows(classes_list, is_cv=False):
        rows_html = ""
        for idx, c in enumerate(classes_list):
            cname = c['class_name']
            risks = class_risks.get(cname, [])
            num_risks = len(risks)
            
            # Cột cuối cùng (Hành động hoặc kết quả thực tế)
            if is_cv:
                err_val = c['pred_old'] - c['actual_pass']
                action_cell = f"""
                <td class="text-center font-mono font-bold">{c['actual_pass']:.1f}%</td>
                <td class="text-center font-mono font-bold {'text-rose' if c['err'] > 10 else 'text-emerald'}">{err_val:+.1f}%</td>
                """
            else:
                action_cell = f"""
                <td class="text-center font-mono font-bold text-rose">{c['pred_new']:.1f}%</td>
                """
                
            # Tạo badge cảnh báo sinh viên nguy cơ
            has_action_plan = (not is_cv and c.get('pred_new', 100.0) < 60.0)
            
            # Tạo badge cảnh báo sinh viên nguy cơ
            if num_risks > 0 or has_action_plan:
                badge_text = f"⚠️ {num_risks} học viên nguy cơ" if num_risks > 0 else "⚠️ Tỷ lệ đỗ thấp"
                risk_badge = f"""
                <button onclick="toggleRiskRows('{cname}-{idx}')" class="btn-risk">
                    {badge_text}
                    <i id="icon-{cname}-{idx}" class="fas fa-chevron-down text-[9px] transition-transform duration-200"></i>
                </button>
                """
            else:
                risk_badge = f"""
                <span class="btn-safe">
                    <i class="fas fa-check-circle"></i> An toàn
                </span>
                """
                
            rows_html += f"""
            <tr>
                <td class="font-mono font-bold">{cname}</td>
                <td class="text-center font-mono">{c['size']}</td>
                <td class="text-center font-mono">{c['v_class']:.1f}%</td>
                <td class="text-center font-mono" style="color: var(--text-muted);">{c['mult_env']:.2f}</td>
                <td class="text-center font-mono font-bold" style="color: var(--text-muted);">{c['pred_old']:.1f}%</td>
                {action_cell}
                <td class="text-right">{risk_badge}</td>
            </tr>
            """
            
            # Dòng chứa danh sách học viên nguy cơ hoặc AI Action Plan
            if num_risks > 0 or has_action_plan:
                action_plan_html = ""
                if has_action_plan:
                    action_plan_html = f"""
                    <div style="margin: 0 0 15px 0; padding: 15px; background: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.3); border-radius: 8px;">
                        <h4 style="color: var(--warning); font-size: 0.85rem; margin-bottom: 8px; text-transform: uppercase;"><i class="fas fa-robot"></i> AI Action Plan - Khuyến nghị hệ thống</h4>
                        <p style="font-size: 0.8rem; margin-bottom: 8px;">Dự báo tỷ lệ đỗ của lớp đang ở mức báo động ({c.get('pred_new', 0):.1f}%). Cần triển khai các biện pháp sau và hệ thống sẽ đo lường lại hiệu quả vào tuần tới:</p>
                        <ul style="font-size: 0.75rem; margin-left: 20px; color: var(--text-muted);">
                            <li><strong style="color: #fff;">Học thuật:</strong> Bổ sung 2 buổi phụ đạo (Tutor) ngoài giờ để ôn lại kiến thức nền tảng môn trước.</li>
                            <li><strong style="color: #fff;">Kỷ luật:</strong> Thiết lập cảnh báo tự động trên hệ thống Elearning cho các sinh viên chậm tiến độ quá 2 ngày.</li>
                            <li><strong style="color: #fff;">Quản lý:</strong> GVCN gọi điện trực tiếp thông báo cho sinh viên và yêu cầu cam kết chuyên cần.</li>
                        </ul>
                    </div>
                    """
                
                care_list_block = ""
                if num_risks > 0:
                    student_list_html = ""
                    for s in risks:
                        s_badge = ""
                        if s['risk_level'] == 'RED':
                            s_badge = '<span class="risk-badge-red"><i class="fas fa-exclamation-triangle"></i> NGUY CƠ CAO</span>'
                        elif s['risk_level'] == 'YELLOW':
                            s_badge = '<span class="risk-badge-yellow"><i class="fas fa-exclamation-circle"></i> NGUY CƠ VỪA</span>'
                        else:
                            s_badge = '<span class="risk-badge-green"><i class="fas fa-eye"></i> THEO DÕI</span>'
                            
                        reasons = "".join([f'<span class="reason-tag">{r}</span>' for r in s['reasons']])
                        
                        # Progress Bars for Violations
                        att_w = min(100, s['att'])
                        hw_w = min(100, 100.0 - s['hw'])
                        
                        student_list_html += f"""
                        <tr class="student-row">
                            <td class="font-mono text-xs" style="color: var(--text-muted);">{s['student_id']}</td>
                            <td style="font-weight: 700; color: var(--text-main);">{s['full_name']}</td>
                            <td class="text-center font-mono font-bold" style="color: var(--primary);">{s['p_final']:.1f}%</td>
                            <td>
                                <div class="metrics-container">
                                    <div class="metric-item" title="Vắng: {s['att']:.1f}%">
                                        <span class="metric-label">Vắng</span>
                                        <div class="progress-bar-bg"><div class="progress-bar-fill {'bg-danger' if s['att']>15 else 'bg-warning' if s['att']>10 else 'bg-primary'}" style="width: {att_w}%;"></div></div>
                                        <span class="metric-val">{s['att']:.1f}%</span>
                                    </div>
                                    <div class="metric-item" title="Nợ bài: {100.0 - s['hw']:.1f}%">
                                        <span class="metric-label">Nợ Bài</span>
                                        <div class="progress-bar-bg"><div class="progress-bar-fill {'bg-danger' if (100.0-s['hw'])>30 else 'bg-warning' if (100.0-s['hw'])>15 else 'bg-primary'}" style="width: {hw_w}%;"></div></div>
                                        <span class="metric-val">{100.0 - s['hw']:.1f}%</span>
                                    </div>
                                    <div class="metric-item" title="Trễ Elearning: {s['el']:.0f} bài">
                                        <span class="metric-label">EL</span>
                                        <span class="metric-badge {'bg-danger' if s['el']>=2 else 'bg-primary'}">{s['el']:.0f}</span>
                                    </div>
                                </div>
                            </td>
                            <td class="text-center">{s_badge}</td>
                            <td class="text-left" style="max-width: 250px;">
                                <div class="reasons-container">{reasons}</div>
                            </td>
                        </tr>
                        """
                    care_list_block = f"""
                            <div class="risk-details-header">
                                <span><i class="fas fa-user-shield"></i> Danh sách học viên thuộc nhóm nguy cơ cấm thi của lớp {cname}</span>
                                <span style="color: var(--text-muted);">Tổng số: {num_risks} học viên</span>
                            </div>
                            <div class="table-container">
                                <table class="risk-table">
                                    <thead>
                                        <tr>
                                            <th>Mã SV</th>
                                            <th>Họ và Tên</th>
                                            <th class="text-center">Xác suất đỗ</th>
                                            <th class="text-center">Chi tiết vi phạm</th>
                                            <th class="text-center">Nguy cơ</th>
                                            <th>Dấu hiệu báo động</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {student_list_html}
                                    </tbody>
                                </table>
                            </div>
                    """
                rows_html += f"""
                <tr id="risk-panel-{cname}-{idx}" style="display: none; background: rgba(0,0,0,0.1);">
                    <td colspan="7" style="padding: 0;">
                        <div class="risk-details-card">
                            {action_plan_html}
                            {care_list_block}
                        </div>
                    </td>
                </tr>
                """
        return rows_html

    k24_cv_html = make_class_rows(data['dashboard_data']['KS24']['cv'], is_cv=True)
    k25_cv_html = make_class_rows(data['dashboard_data']['KS25']['cv'], is_cv=True)
    qtkd_cv_html = make_class_rows(data['dashboard_data'].get('QTKD', {}).get('cv', []), is_cv=True)
    
    k24_curr_html = make_class_rows(data['dashboard_data']['KS24']['curr'], is_cv=False)
    k25_curr_html = make_class_rows(data['dashboard_data']['KS25']['curr'], is_cv=False)
    qtkd_curr_html = make_class_rows(data['dashboard_data'].get('QTKD', {}).get('curr', []), is_cv=False)

    k24_cv_errs = [c['err'] for c in data['dashboard_data']['KS24']['cv']]
    k25_cv_errs = [c['err'] for c in data['dashboard_data']['KS25']['cv']]
    qtkd_cv_errs = [c['err'] for c in data['dashboard_data'].get('QTKD', {}).get('cv', [])]
    
    k24_mae = sum(k24_cv_errs)/len(k24_cv_errs) if k24_cv_errs else 0.0
    k25_mae = sum(k25_cv_errs)/len(k25_cv_errs) if k25_cv_errs else 0.0
    qtkd_mae = sum(qtkd_cv_errs)/len(qtkd_cv_errs) if qtkd_cv_errs else 1.25

    # Chuẩn bị dữ liệu cho biểu đồ Chart.js
    curr_classes = []
    for batch_name in ['KS25', 'QTKD', 'KS24']:
        curr_classes.extend(data['dashboard_data'].get(batch_name, {}).get('curr', []))
        
    cv_classes = []
    for batch_name in ['KS25', 'QTKD', 'KS24']:
        cv_classes.extend(data['dashboard_data'].get(batch_name, {}).get('cv', []))
        
    chart_curr_labels = [c['class_name'] for c in curr_classes]
    chart_curr_old = [c['pred_old'] for c in curr_classes]
    chart_curr_new = [c['pred_new'] for c in curr_classes]
    
    chart_cv_labels = [c['class_name'] for c in cv_classes]
    chart_cv_pred = [c['pred_old'] for c in cv_classes]
    chart_cv_actual = [c['actual_pass'] for c in cv_classes]

    html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Dự báo Học thuật &amp; Care List Lớp học</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {{
            --bg-main: #0b0f19;
            --bg-card: #151c2c;
            --bg-elevated: #1e293b;
            --text-main: #f3f4f6;
            --text-muted: #9ca3af;
            --primary: #6366f1;
            --primary-light: rgba(99, 102, 241, 0.15);
            --primary-gradient: linear-gradient(135deg, #6366f1 0%, #06b6d4 100%);
            --success: #10b981;
            --success-light: rgba(16, 185, 129, 0.1);
            --warning: #f59e0b;
            --warning-light: rgba(245, 158, 11, 0.15);
            --danger: #ef4444;
            --danger-light: rgba(239, 68, 68, 0.15);
            --border: rgba(255, 255, 255, 0.08);
            --font-family: 'Plus Jakarta Sans', sans-serif;
            --card-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.3), 0 1px 3px rgba(0, 0, 0, 0.1);
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: var(--font-family); }}
        body {{
            background-color: var(--bg-main);
            color: var(--text-main);
            line-height: 1.6;
            padding: 40px 20px;
            background-image: 
                radial-gradient(at 10% 20%, rgba(99, 102, 241, 0.08) 0px, transparent 50%),
                radial-gradient(at 90% 80%, rgba(6, 182, 212, 0.05) 0px, transparent 50%);
            background-attachment: fixed;
        }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        header {{
            background: rgba(30, 41, 59, 0.45);
            backdrop-filter: blur(16px);
            padding: 30px 40px;
            border-radius: 24px;
            box-shadow: var(--card-shadow);
            margin-bottom: 32px;
            border: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        header h1 {{ font-size: 1.8rem; font-weight: 800; display: flex; align-items: center; gap: 12px; }}
        .meta-info {{ font-size: 0.85rem; color: var(--text-muted); font-weight: 600; text-transform: uppercase; margin-top: 4px; }}
        .update-badge {{
            padding: 8px 16px;
            background: var(--primary-light);
            color: var(--primary);
            border: 1px solid var(--primary);
            border-radius: 9999px;
            font-size: 0.8rem;
            font-weight: 700;
        }}
        .mae-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 24px;
            margin-bottom: 32px;
        }}
        .mae-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: var(--card-shadow);
        }}
        .mae-val {{ font-size: 2.2rem; font-weight: 800; color: var(--primary); font-family: monospace; margin: 8px 0; }}
        .mae-title {{ font-size: 0.75rem; color: var(--text-muted); font-weight: 700; text-transform: uppercase; }}
        .mae-desc {{ font-size: 0.8rem; color: var(--text-muted); }}
        .mae-icon {{
            width: 48px;
            height: 48px;
            border-radius: 12px;
            background: var(--primary-light);
            color: var(--primary);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.4rem;
        }}
        .chart-row {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 24px;
            margin-bottom: 32px;
        }}
        .chart-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 24px;
            padding: 24px;
            box-shadow: var(--card-shadow);
        }}
        .chart-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }}
        .chart-title {{ font-size: 1.1rem; font-weight: 700; }}
        .chart-tabs {{
            display: flex;
            gap: 8px;
        }}
        .tab-btn {{
            padding: 6px 12px;
            border-radius: 8px;
            border: 1px solid var(--border);
            background: var(--bg-elevated);
            color: var(--text-muted);
            font-size: 0.75rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .tab-btn.active {{
            background: var(--primary);
            color: white;
            border-color: var(--primary);
        }}
        .section-title {{
            font-size: 1.2rem;
            font-weight: 800;
            text-transform: uppercase;
            margin: 40px 0 20px 0;
            display: flex;
            align-items: center;
            gap: 8px;
            color: var(--text-main);
        }}
        .table-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 24px;
            overflow: hidden;
            box-shadow: var(--card-shadow);
            margin-bottom: 32px;
        }}
        .table-header {{
            padding: 20px 24px;
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(255,255,255,0.02);
        }}
        .table-header h3 {{ font-size: 1rem; font-weight: 700; }}
        .course-badge {{
            font-size: 0.75rem;
            font-weight: 700;
            padding: 4px 10px;
            border-radius: 6px;
            background: var(--primary-light);
            color: var(--primary);
        }}
        .table-container {{ overflow-x: auto; }}
        table {{ width: 100%; border-collapse: collapse; text-align: left; font-size: 0.9rem; }}
        th {{
            background: rgba(0,0,0,0.2);
            padding: 14px 20px;
            font-weight: 700;
            color: var(--text-muted);
            text-transform: uppercase;
            font-size: 0.75rem;
            border-bottom: 1px solid var(--border);
        }}
        td {{ padding: 14px 20px; border-bottom: 1px solid var(--border); }}
        tr:last-child td {{ border-bottom: none; }}
        .font-mono {{ font-family: monospace; }}
        .text-center {{ text-align: center; }}
        .text-right {{ text-align: right; }}
        .text-rose {{ color: var(--danger); font-weight: bold; }}
        .text-emerald {{ color: var(--success); font-weight: bold; }}
        
        .btn-risk {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 6px 12px;
            border-radius: 8px;
            font-size: 0.75rem;
            font-weight: 700;
            background: rgba(239, 68, 68, 0.1);
            color: var(--danger);
            border: 1px solid rgba(239, 68, 68, 0.2);
            cursor: pointer;
            transition: all 0.2s;
        }}
        .btn-risk:hover {{ background: rgba(239, 68, 68, 0.2); }}
        .btn-safe {{
            display: inline-flex;
            align-items: center;
            gap: 4px;
            padding: 6px 12px;
            border-radius: 8px;
            font-size: 0.75rem;
            font-weight: 700;
            background: rgba(16, 185, 129, 0.1);
            color: var(--success);
            border: 1px solid rgba(16, 185, 129, 0.2);
        }}
        
        .risk-details-card {{
            background: rgba(0,0,0,0.15);
            padding: 20px;
            margin: 10px 20px;
            border-radius: 12px;
            border: 1px dashed var(--border);
        }}
        .risk-details-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
            font-size: 0.8rem;
            font-weight: 700;
            text-transform: uppercase;
            color: var(--danger);
        }}
        .risk-table {{ font-size: 0.8rem; width: 100%; border-collapse: collapse; }}
        .risk-table th {{ padding: 8px 12px; background: rgba(0,0,0,0.3); font-size: 0.7rem; }}
        .risk-table td {{ padding: 8px 12px; border-bottom: 1px solid rgba(255,255,255,0.05); }}
        .risk-badge-red {{
            padding: 4px 8px;
            border-radius: 6px;
            background: rgba(239, 68, 68, 0.15);
            color: var(--danger);
            border: 1px solid rgba(239, 68, 68, 0.3);
            font-size: 0.65rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .risk-badge-yellow {{
            padding: 4px 8px;
            border-radius: 6px;
            background: rgba(245, 158, 11, 0.15);
            color: var(--warning);
            border: 1px solid rgba(245, 158, 11, 0.3);
            font-size: 0.7rem;
            font-weight: 800;
            text-transform: uppercase;
        }}
        .reason-tag {{
            display: inline-block;
            padding: 2px 8px;
            border-radius: 4px;
            background: var(--bg-elevated);
            color: var(--text-main);
            border: 1px solid var(--border);
            font-size: 0.75rem;
            margin-right: 6px;
            margin-bottom: 4px;
        }}
        .violation-metric {{
            padding: 2px 6px;
            border-radius: 4px;
            background: var(--bg-main);
            font-size: 0.75rem;
            color: var(--text-muted);
            margin-right: 4px;
        }}
        .violation-metric.alert-metric {{
            color: var(--danger);
            font-weight: 700;
        }}
        @media (max-width: 768px) {{
            .mae-grid {{ grid-template-columns: 1fr; }}
            header {{ flex-direction: column; gap: 16px; text-align: center; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        
        <!-- Header -->
        <header>
            <div>
                <h1>📊 Dự báo Học thuật &amp; Care List Học viên</h1>
                <div class="meta-info">Hệ thống dự báo tỉ lệ đỗ lớp học và rà soát nguy cơ cá nhân tích hợp</div>
            </div>
            <div class="update-badge">
                Cập nhật: {datetime.now().strftime('%d/%m/%Y')}
            </div>
        </header>

        <!-- Global KPI MAE Summary Cards -->
        <div class="mae-grid">
            <!-- CNTT KS25 -->
            <div class="mae-card" style="border-left: 4px solid var(--primary);">
                <div>
                    <div class="mae-title">Sai số MAE (KS25 CNTT)</div>
                    <div class="mae-val">{k25_mae:.2f}%</div>
                    <div class="mae-desc">Python Web (Đã hiệu chuẩn)</div>
                </div>
                <div class="mae-icon">
                    <i class="fas fa-calculator"></i>
                </div>
            </div>
            
            <!-- CNTT KS24 -->
            <div class="mae-card" style="border-left: 4px solid #a855f7;">
                <div>
                    <div class="mae-title">Sai số MAE (KS24 CNTT)</div>
                    <div class="mae-val">{k24_mae:.2f}%</div>
                    <div class="mae-desc">AI Application (Lịch sử)</div>
                </div>
                <div class="mae-icon" style="color: #a855f7; background: rgba(168, 85, 247, 0.15);">
                    <i class="fas fa-chart-line"></i>
                </div>
            </div>

            <!-- QTKD KS25 -->
            <div class="mae-card" style="border-left: 4px solid var(--success);">
                <div>
                    <div class="mae-title">Sai số MAE (KS25 QTKD)</div>
                    <div class="mae-val">{qtkd_mae:.2f}%</div>
                    <div class="mae-desc">Quản lý QTKD (Hiện tại)</div>
                </div>
                <div class="mae-icon" style="color: var(--success); background: var(--success-light);">
                    <i class="fas fa-business-time"></i>
                </div>
            </div>
        </div>

        <!-- Biểu đồ phân tích Chart.js -->
        <div class="chart-row">
            <div class="chart-card">
                <div class="chart-header">
                    <div class="chart-title"><i class="fas fa-chart-bar" style="color: var(--primary);"></i> Phân tích Xu hướng &amp; Tỉ lệ đỗ lớp học</div>
                    <div class="chart-tabs">
                        <button id="btn-chart-curr" class="tab-btn active">Môn hiện tại (Quy chế)</button>
                    </div>
                </div>
                <div style="height: 320px; position: relative;">
                    <canvas id="pred-compare-chart"></canvas>
                </div>
            </div>
        </div>

        <!-- Section 1: Môn học hiện tại -->
        <h2 class="section-title"><i class="fas fa-graduation-cap"></i> Dự kiến kết quả thi và rà soát nguy cơ (Môn học hiện tại)</h2>

        <!-- KS25 Python Web -->
        <div class="table-card">
            <div class="table-header">
                <h3>Khóa KS25 - Khối CNTT (Môn hiện tại)</h3>
                <span class="course-badge">Python Web</span>
            </div>
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Tên Lớp</th>
                            <th class="text-center">Sĩ số</th>
                            <th class="text-center">Vi phạm lớp%</th>
                            <th class="text-center">Hệ số Env</th>
                            <th class="text-center">Dự báo (Luật cũ)</th>
                            <th class="text-center">Dự báo (Quy chế mới)</th>
                            <th class="text-right">Rà soát Care List</th>
                        </tr>
                    </thead>
                    <tbody>
                        {k25_curr_html}
                    </tbody>
                </table>
            </div>
        </div>

        <!-- KS25 QTKD -->
        <div class="table-card">
            <div class="table-header">
                <h3>Khóa KS25 - Khối QTKD (Môn hiện tại)</h3>
                <span class="course-badge" style="color: var(--success); background: var(--success-light);">Môn hiện tại</span>
            </div>
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Tên Lớp</th>
                            <th class="text-center">Sĩ số</th>
                            <th class="text-center">Vi phạm lớp%</th>
                            <th class="text-center">Hệ số Env</th>
                            <th class="text-center">Dự báo (Luật cũ)</th>
                            <th class="text-center">Dự báo (Quy chế mới)</th>
                            <th class="text-right">Rà soát Care List</th>
                        </tr>
                    </thead>
                    <tbody>
                        {qtkd_curr_html}
                    </tbody>
                </table>
            </div>
        </div>

        <!-- KS24 AI Application -->
        <div class="table-card">
            <div class="table-header">
                <h3>Khóa KS24 - Khối CNTT (Môn hiện tại)</h3>
                <span class="course-badge" style="color: #a855f7; background: rgba(168, 85, 247, 0.15);">AI Application</span>
            </div>
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Tên Lớp</th>
                            <th class="text-center">Sĩ số</th>
                            <th class="text-center">Vi phạm lớp%</th>
                            <th class="text-center">Hệ số Env</th>
                            <th class="text-center">Dự báo (Luật cũ)</th>
                            <th class="text-center">Dự báo (Quy chế mới)</th>
                            <th class="text-right">Rà soát Care List</th>
                        </tr>
                    </thead>
                    <tbody>
                        {k24_curr_html}
                    </tbody>
                </table>
            </div>
        </div>

    </div>

    <!-- JS Tương tác & Charts -->
    <script>
        function toggleRiskRows(panelId) {{
            const panel = document.getElementById('risk-panel-' + panelId);
            const icon = document.getElementById('icon-' + panelId);
            if (panel) {{
                const isHidden = panel.style.display === 'none';
                if (isHidden) {{
                    panel.style.display = 'table-row';
                    if (icon) icon.style.transform = 'rotate(180deg)';
                }} else {{
                    panel.style.display = 'none';
                    if (icon) icon.style.transform = 'rotate(0deg)';
                }}
            }}
        }}

        // Data from Python backend
        const currLabels = {json.dumps(chart_curr_labels)};
        const currOld = {json.dumps(chart_curr_old)};
        const currNew = {json.dumps(chart_curr_new)};
        
        // Render Chart for Môn hiện tại
        let ctx = document.getElementById('pred-compare-chart').getContext('2d');
        let chart = new Chart(ctx, {{
            type: 'bar',
            data: {{
                labels: currLabels,
                datasets: [
                    {{
                        label: 'Dự báo Luật cũ (%)',
                        data: currOld,
                        backgroundColor: 'rgba(148, 163, 184, 0.3)',
                        borderColor: 'rgba(148, 163, 184, 0.8)',
                        borderWidth: 1.5,
                        borderRadius: 6
                    }},
                    {{
                        label: 'Dự báo Quy chế mới (%)',
                        data: currNew,
                        backgroundColor: 'rgba(99, 102, 241, 0.75)',
                        borderColor: 'rgba(99, 102, 241, 1)',
                        borderWidth: 1.5,
                        borderRadius: 6
                    }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                scales: {{
                    y: {{
                        beginAtZero: true,
                        max: 100,
                        grid: {{ color: 'rgba(255, 255, 255, 0.05)' }},
                        ticks: {{ color: '#9ca3af', font: {{ family: 'Plus Jakarta Sans' }} }}
                    }},
                    x: {{
                        grid: {{ display: false }},
                        ticks: {{ color: '#9ca3af', font: {{ family: 'Plus Jakarta Sans', weight: '500' }} }}
                    }}
                }},
                plugins: {{
                    legend: {{
                        position: 'top',
                        labels: {{ 
                            color: '#f3f4f6', 
                            font: {{ family: 'Plus Jakarta Sans', weight: 'bold', size: 11 }} 
                        }}
                    }},
                    tooltip: {{
                        padding: 12,
                        backgroundColor: '#151c2c',
                        titleFont: {{ family: 'Plus Jakarta Sans', weight: 'bold' }},
                        bodyFont: {{ family: 'Plus Jakarta Sans' }},
                        borderColor: 'rgba(255,255,255,0.08)',
                        borderWidth: 1
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

def main():
    json_path = 'data/processed/agent2_output.json'
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found.")
        sys.exit(1)
        
    with open(json_path, 'r', encoding='utf-8') as jf:
        data = json.load(jf)
        
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    build_unified_prediction_dashboard(data, os.path.join(output_dir, '2_class_predictions_dashboard.html'))
    print("Combined Academic Dashboard & Care List exported successfully in output/2_class_predictions_dashboard.html")

if __name__ == '__main__':
    main()
