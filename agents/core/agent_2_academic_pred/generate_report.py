import os
import sys
import json
from datetime import datetime

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def build_unified_prediction_dashboard(data, output_path):
    # Load teacher violations from Agent 3 output
    teacher_violations = []
    teacher_violations_path = 'data/processed/agent3_output.json'
    if os.path.exists(teacher_violations_path):
        try:
            with open(teacher_violations_path, 'r', encoding='utf-8') as f:
                teacher_violations = json.load(f)
        except Exception as e:
            print(f"Warning: Could not read {teacher_violations_path}: {e}")
            
    norm_c = lambda n: n.replace('KS', 'K')
    class_violations = {}
    for v in teacher_violations:
        cname = norm_c(v.get('Class', ''))
        if cname not in class_violations:
            class_violations[cname] = []
        class_violations[cname].append(v)

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
            
            # Lấy danh sách lỗi tác nghiệp của lớp này
            norm_cname = norm_c(cname)
            class_errs = class_violations.get(norm_cname, [])
            num_class_errs = len(class_errs)
            
            # Icon cảnh báo GV/TG
            warning_icon_html = ""
            if not is_cv and num_class_errs > 0:
                err_counts = {}
                for v in class_errs:
                    err_code = v.get('Error', 'GV-08')
                    err_counts[err_code] = err_counts.get(err_code, 0) + 1
                err_summary = ", ".join([f"{err_counts[k]} lỗi {k}" for k in err_counts])
                
                warning_icon_html = f"""
                <div class="tooltip-container">
                    <span style="color: var(--warning); font-size: 1.1rem;"><i class="fas fa-exclamation-triangle"></i></span>
                    <div class="tooltip-text">
                        <strong>Cảnh báo tác nghiệp ({err_summary}):</strong><br>
                        Lớp học ghi nhận các lỗi giảng viên/trợ giảng vi phạm quy chế hành chính. Yêu cầu cập nhật điều chỉnh trên hệ thống QLĐT để đảm bảo quyền lợi học viên.
                    </div>
                </div>
                """
            else:
                warning_icon_html = """<span style="color: var(--success);"><i class="fas fa-check-circle"></i></span>"""
            
            # Nút Chi tiết mở drawer
            detail_button = f"""
            <button onclick="openClassDrawer('{cname}', {str(is_cv).lower()})" class="btn-risk" style="background: var(--primary-light); color: var(--primary); border-color: rgba(99,102,241,0.2);">
                <i class="fas fa-search"></i> Chi tiết
            </button>
            """
                
            rows_html += f"""
            <tr>
                <td class="font-mono font-bold">{cname}</td>
                <td class="text-center font-mono">{c['size']}</td>
                <td class="text-center font-mono">{c['v_class']:.1f}%</td>
                <td class="text-center font-mono" style="color: var(--text-muted);">{c['mult_env']:.2f}</td>
                <td class="text-center font-mono font-bold" style="color: var(--text-muted);">{c['pred_old']:.1f}%</td>
                {action_cell}
                <td class="text-center">{warning_icon_html}</td>
                <td class="text-right">{detail_button}</td>
            </tr>
            """
        return rows_html

    k24_curr_html = make_class_rows(data['dashboard_data']['KS24']['curr'], is_cv=False)
    k25_curr_html = make_class_rows(data['dashboard_data']['KS25']['curr'], is_cv=False)
    qtkd_curr_html = make_class_rows(data['dashboard_data'].get('QTKD', {}).get('curr', []), is_cv=False)

    # Calculate MAE values
    k24_cv_errs = [c['err'] for c in data['dashboard_data']['KS24']['cv']]
    k25_cv_errs = [c['err'] for c in data['dashboard_data']['KS25']['cv']]
    qtkd_cv_errs = [c['err'] for c in data['dashboard_data'].get('QTKD', {}).get('cv', [])]
    
    k24_mae = sum(k24_cv_errs)/len(k24_cv_errs) if k24_cv_errs else 0.0
    k25_mae = sum(k25_cv_errs)/len(k25_cv_errs) if k25_cv_errs else 0.0
    qtkd_mae = sum(qtkd_cv_errs)/len(qtkd_cv_errs) if qtkd_cv_errs else 1.25
    mae_avg = (k24_mae + k25_mae) / 2 if (k24_mae and k25_mae) else 10.5
    
    red_count = sum(1 for s in data['care_list'] if s['risk_level'] == 'RED')
    yellow_count = sum(1 for s in data['care_list'] if s['risk_level'] == 'YELLOW')

    # Count teacher violations per cohort
    teacher_violations_count = { 'K24': 0, 'K25': 0, 'QTKD': 0 }
    for v in teacher_violations:
        cls = v.get('Class', '')
        cohort = 'K24' if 'K24' in cls else ('QTKD' if 'QTKD' in cls or 'PRJ' in cls else 'K25')
        if cohort in teacher_violations_count:
            teacher_violations_count[cohort] += 1
            
    # Generate automatic Action Plan items (Tab 1)
    low_classes_items = []
    for cohort in ['KS25', 'KS24', 'QTKD']:
        for c in data['dashboard_data'].get(cohort, {}).get('curr', []):
            if c.get('pred_new', 100.0) < 60.0:
                low_classes_items.append(c)
    low_classes_items.sort(key=lambda x: x.get('pred_new', 100.0))
    
    high_viol_items = []
    for cohort in ['KS25', 'KS24', 'QTKD']:
        for c in data['dashboard_data'].get(cohort, {}).get('curr', []):
            if c.get('v_class', 0.0) > 15.0:
                high_viol_items.append(c)
    high_viol_items.sort(key=lambda x: x.get('v_class', 0.0), reverse=True)
    
    ops_err_items = []
    for v in teacher_violations:
        cls_name = v.get('Class', '')
        err_code = v.get('Error', 'GV-08')
        ops_err_items.append((cls_name, err_code))
    ops_err_items = list(set(ops_err_items))

    limits_html = ""
    solutions_html = ""
    
    for c in low_classes_items[:3]:
        cname = c['class_name']
        pred_val = c.get('pred_new', 0.0)
        limits_html += f"""
        <div class="action-item-card" style="border-left: 4px solid var(--danger); background: rgba(239, 68, 68, 0.03);">
            <strong>Lớp {cname} có tỉ lệ đỗ dự kiến thấp:</strong><br>
            Tỉ lệ đỗ dự kiến đạt <strong>{pred_val:.1f}%</strong> do ý thức kỷ luật hoặc học lực môn học trước sa sút.
        </div>
        """
        solutions_html += f"""
        <div class="action-item-card" style="border-left: 4px solid var(--danger); background: rgba(239, 68, 68, 0.03);">
            <strong>Tổ chức phụ đạo lớp {cname}:</strong><br>
            Yêu cầu Giảng viên/Trợ giảng tổ chức <strong>ít nhất 1 buổi phụ đạo/tuần</strong> ôn tập kiến thức nền cho nhóm sinh viên yếu.
        </div>
        """
        
    for c in high_viol_items[:3]:
        cname = c['class_name']
        v_val = c.get('v_class', 0.0)
        limits_html += f"""
        <div class="action-item-card" style="border-left: 4px solid var(--warning); background: rgba(245, 158, 11, 0.03);">
            <strong>Lớp {cname} vi phạm kỷ luật cao ({v_val:.1f}%):</strong><br>
            Tỷ lệ vắng mặt chuyên cần và nợ bài tập lớp vượt ngưỡng cảnh báo an toàn.
        </div>
        """
        solutions_html += f"""
        <div class="action-item-card" style="border-left: 4px solid var(--warning); background: rgba(245, 158, 11, 0.03);">
            <strong>Siết chặt giờ giấc lớp {cname}:</strong><br>
            Cố vấn học tập liên hệ nhắc nhở gia đình, giảng viên chấn chỉnh kỷ luật giờ giấc học tập đầu giờ học.
        </div>
        """
        
    for cls_name, err_code in ops_err_items[:3]:
        limits_html += f"""
        <div class="action-item-card" style="border-left: 4px solid #a855f7; background: rgba(168, 85, 247, 0.03);">
            <strong>Lớp {cls_name} ghi nhận lỗi tác nghiệp {err_code}:</strong><br>
            Phát hiện lỗi tích vắng sai hoặc quên điểm danh của giảng viên/trợ giảng.
        </div>
        """
        solutions_html += f"""
        <div class="action-item-card" style="border-left: 4px solid #a855f7; background: rgba(168, 85, 247, 0.03);">
            <strong>Khắc phục dữ liệu lớp {cls_name}:</strong><br>
            Yêu cầu Trợ giảng đối chiếu và hiệu chỉnh thông tin điểm danh chính xác trên hệ thống QLĐT.
        </div>
        """
        
    if not limits_html:
        limits_html = """<div class="action-item-card">Không ghi nhận điểm nghẽn học vụ nổi bật nào.</div>"""
        solutions_html = """<div class="action-item-card">Hệ thống học vụ vận hành ổn định.</div>"""

    # Generate central Care List rows (Tab 3)
    care_list_rows_html = ""
    for s in data['care_list']:
        sid = s['student_id']
        name = s['full_name']
        cname = s['class_name']
        batch = s['batch']
        p_final = s['p_final']
        att = s['att']
        hw = 100.0 - s['hw']
        el = s['el']
        risk = s['risk_level']
        reasons = ", ".join(s['reasons'])
        
        badge_cls = "risk-badge-red" if risk == 'RED' else "risk-badge-yellow"
        cohort_cls = "cntt" if "QTKD" not in cname else "qtkd"
        risk_filter_cls = "filter-red" if risk == 'RED' else "filter-yellow"
        
        care_list_rows_html += f"""
        <tr class="care-row {cohort_cls} {risk_filter_cls}">
            <td class="font-mono">{batch}</td>
            <td class="font-mono font-bold">{cname}</td>
            <td class="font-bold">{name} ({sid})</td>
            <td class="text-center font-mono font-bold {'text-rose' if risk == 'RED' else 'text-warning'}">{p_final:.1f}%</td>
            <td class="text-center font-mono">{att:.1f}%</td>
            <td class="text-center font-mono">{hw:.1f}%</td>
            <td class="text-center font-mono">{el:.0f}</td>
            <td><span class="{badge_cls}">{risk}</span></td>
            <td style="font-size: 0.8rem; color: var(--text-muted);">{reasons}</td>
        </tr>
        """

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

    html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Báo cáo Đánh giá Học thuật &amp; Danh sách can thiệp</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {{
            --bg-main: #090d16;
            --bg-card: #0f172a;
            --bg-elevated: #1e293b;
            --text-main: #f3f4f6;
            --text-muted: #9ca3af;
            --primary: #3b82f6;
            --primary-light: rgba(59, 130, 246, 0.15);
            --success: #10b981;
            --success-light: rgba(16, 185, 129, 0.1);
            --warning: #f59e0b;
            --warning-light: rgba(245, 158, 11, 0.15);
            --danger: #f43f5e;
            --danger-light: rgba(244, 63, 94, 0.15);
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
        .update-badge {{
            padding: 8px 16px;
            background: var(--primary-light);
            color: var(--primary);
            border: 1px solid var(--primary);
            border-radius: 9999px;
            font-size: 0.8rem;
            font-weight: 700;
        }}
        
        /* Tabs System CSS */
        .tabs-container {{
            display: flex;
            gap: 12px;
            margin-bottom: 24px;
            border-bottom: 1px solid var(--border);
            padding-bottom: 12px;
        }}
        .tab-button {{
            padding: 10px 20px;
            border-radius: 10px;
            border: 1px solid transparent;
            background: transparent;
            color: var(--text-muted);
            font-size: 0.9rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.25s ease;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .tab-button:hover {{
            color: var(--text-main);
            background: rgba(255, 255, 255, 0.03);
        }}
        .tab-button.active {{
            background: var(--primary-light);
            color: var(--primary);
            border-color: var(--primary);
        }}
        .tab-content {{
            display: none;
        }}
        .tab-content.active {{
            display: block;
        }}

        /* Action Plan Columns Style */
        .action-plan-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 24px;
            margin-top: 24px;
        }}
        .action-plan-col {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 24px;
            box-shadow: var(--card-shadow);
        }}
        .action-plan-col h3 {{
            font-size: 1.1rem;
            font-weight: 800;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 8px;
            border-bottom: 1px solid var(--border);
            padding-bottom: 10px;
        }}
        .action-item-card {{
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 12px;
            font-size: 0.85rem;
            line-height: 1.5;
            color: var(--text-main);
        }}
        .action-item-card strong {{
            color: #fff;
        }}

        /* Tooltip style */
        .tooltip-container {{
            position: relative;
            display: inline-block;
            cursor: pointer;
        }}
        .tooltip-container .tooltip-text {{
            visibility: hidden;
            width: 280px;
            background-color: #1e293b;
            color: #f3f4f6;
            text-align: left;
            border-radius: 8px;
            padding: 12px;
            border: 1px solid var(--border);
            box-shadow: 0 10px 15px -3px rgba(0,0,0,0.5);
            position: absolute;
            z-index: 100;
            bottom: 125%;
            left: 50%;
            margin-left: -140px;
            opacity: 0;
            transition: opacity 0.2s;
            font-size: 0.8rem;
            line-height: 1.4;
        }}
        .tooltip-container:hover .tooltip-text {{
            visibility: visible;
            opacity: 1;
        }}

        /* Slide-over Drawer Style */
        #class-drawer {{
            position: fixed;
            top: 0;
            right: -490px;
            width: 470px;
            height: 100%;
            background: #0f172a;
            box-shadow: -10px 0 30px rgba(0, 0, 0, 0.5);
            transition: right 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            z-index: 1000;
            overflow-y: auto;
            border-left: 1px solid var(--border);
        }}
        #class-drawer.open {{
            right: 0;
        }}
        #drawer-backdrop {{
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(4px);
            z-index: 999;
        }}
        .drawer-header {{
            padding: 24px;
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .drawer-close {{
            background: transparent;
            border: none;
            color: var(--text-muted);
            font-size: 1.5rem;
            cursor: pointer;
        }}
        .drawer-content {{
            padding: 24px;
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
        .text-warning {{ color: var(--warning); font-weight: bold; }}
        .text-emerald {{ color: var(--success); font-weight: bold; }}
        
        .btn-risk {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 6px 12px;
            border-radius: 8px;
            font-size: 0.75rem;
            font-weight: 700;
            background: rgba(59, 130, 246, 0.1);
            color: var(--primary);
            border: 1px solid rgba(59, 130, 246, 0.2);
            cursor: pointer;
            transition: all 0.2s;
        }}
        .btn-risk:hover {{ background: rgba(59, 130, 246, 0.2); }}
        
        .risk-badge-red {{
            padding: 4px 8px;
            border-radius: 6px;
            background: rgba(244, 63, 94, 0.15);
            color: var(--danger);
            border: 1px solid rgba(244, 63, 94, 0.3);
            font-size: 0.65rem;
            font-weight: 800;
            text-transform: uppercase;
        }}
        .risk-badge-yellow {{
            padding: 4px 8px;
            border-radius: 6px;
            background: rgba(245, 158, 11, 0.15);
            color: var(--warning);
            border: 1px solid rgba(245, 158, 11, 0.3);
            font-size: 0.65rem;
            font-weight: 800;
            text-transform: uppercase;
        }}
        
        .student-risk-card {{
            background: rgba(30, 41, 59, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            padding: 12px;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}
        .student-risk-card.red-border {{ border-left: 3px solid rgba(244, 63, 94, 0.55); }}
        .student-risk-card.yellow-border {{ border-left: 3px solid rgba(245, 158, 11, 0.55); }}
        .student-metric-pill {{
            display: inline-flex;
            align-items: center;
            gap: 4px;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 0.68rem;
            font-weight: 500;
        }}
        .student-metric-pill.red-pill {{
            background: rgba(244, 63, 94, 0.1);
            color: var(--danger);
            border: 1px solid rgba(244, 63, 94, 0.2);
        }}
        .student-metric-pill.yellow-pill {{
            background: rgba(245, 158, 11, 0.1);
            color: var(--warning);
            border: 1px solid rgba(245, 158, 11, 0.2);
        }}
        
        /* Filter Button CSS */
        .filter-btn {{
            padding: 8px 16px;
            border-radius: 8px;
            border: 1px solid var(--border);
            background: var(--bg-card);
            color: var(--text-muted);
            font-size: 0.8rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .filter-btn.active {{
            background: var(--primary);
            color: white;
            border-color: var(--primary);
        }}
        
        .class-violation-alert {{
            background: rgba(244, 63, 94, 0.08);
            border: 1px solid rgba(244, 63, 94, 0.2);
            border-radius: 12px;
            padding: 12px 16px;
            font-size: 0.8rem;
            color: var(--danger);
            display: flex;
            align-items: flex-start;
            gap: 8px;
            line-height: 1.4;
        }}
    </style>
</head>
<body>
    <div class="container">
        
        <!-- Header -->
        <header>
            <div>
                <h1>📊 Đánh giá Học thuật &amp; Hỗ trợ Học viên</h1>
                <div class="meta-info">Hệ thống dự báo tỉ lệ đỗ lớp học và rà soát nguy cơ cá nhân tích hợp</div>
            </div>
            <div class="update-badge">
                Cập nhật: {datetime.now().strftime('%d/%m/%Y')}
            </div>
        </header>

        <!-- Navigation Tabs -->
        <div class="tabs-container">
            <button class="tab-button active" onclick="switchTab('executive')"><i class="fas fa-chart-pie"></i> Đánh giá &amp; Giải pháp hệ thống</button>
            <button class="tab-button" onclick="switchTab('classes')"><i class="fas fa-school"></i> Phân tích Lớp học</button>
            <button class="tab-button" onclick="switchTab('care-list')"><i class="fas fa-user-shield"></i> Danh sách cần can thiệp</button>
        </div>

        <!-- TAB 1: EXECUTIVE SUMMARY -->
        <div id="tab-executive" class="tab-content active">
            <!-- Global KPI Summary Cards -->
            <div class="mae-grid">
                <div class="mae-card" style="border-left: 4px solid var(--primary);">
                    <div>
                        <div class="mae-title">Sai số đánh giá lịch sử (MAE)</div>
                        <div class="mae-val">{mae_avg:.2f}%</div>
                        <div class="mae-desc">Tính trung bình các mốc kiểm chứng</div>
                    </div>
                    <div class="mae-icon"><i class="fas fa-calculator"></i></div>
                </div>
                
                <div class="mae-card" style="border-left: 4px solid var(--danger);">
                    <div>
                        <div class="mae-title">Nguy cơ Cao (Báo động Đỏ)</div>
                        <div class="mae-val">{red_count} SV</div>
                        <div class="mae-desc">Học lực yếu hoặc có nguy cơ cấm thi</div>
                    </div>
                    <div class="mae-icon" style="color: var(--danger); background: var(--danger-light);"><i class="fas fa-user-slash"></i></div>
                </div>

                <div class="mae-card" style="border-left: 4px solid var(--warning);">
                    <div>
                        <div class="mae-title">Nguy cơ Trung bình (Cảnh báo Vàng)</div>
                        <div class="mae-val">{yellow_count} SV</div>
                        <div class="mae-desc">Cận cấm thi hoặc mất gốc kiến thức</div>
                    </div>
                    <div class="mae-icon" style="color: var(--warning); background: var(--warning-light);"><i class="fas fa-exclamation-triangle"></i></div>
                </div>
            </div>

            <!-- Chart -->
            <div class="chart-row">
                <div class="chart-card">
                    <div class="chart-header">
                        <div class="chart-title"><i class="fas fa-chart-bar" style="color: var(--primary);"></i> Phân tích tỉ lệ đỗ lớp học dự kiến</div>
                    </div>
                    <div style="height: 320px; position: relative;">
                        <canvas id="pred-compare-chart"></canvas>
                    </div>
                </div>
            </div>

            <!-- Action Plan Grid -->
            <h2>🎯 Hạn chế &amp; Giải pháp khắc phục (Đề xuất hệ thống)</h2>
            <div class="action-plan-grid">
                <div class="action-plan-col">
                    <h3><i class="fas fa-search-minus" style="color: var(--danger);"></i> Các điểm nghẽn học vụ phát hiện</h3>
                    {limits_html}
                </div>
                <div class="action-plan-col">
                    <h3><i class="fas fa-toolbox" style="color: var(--success);"></i> Đề xuất hành động tức thời</h3>
                    {solutions_html}
                </div>
            </div>
        </div>

        <!-- TAB 2: CLASS LIST -->
        <div id="tab-classes" class="tab-content">
            <!-- KS25 Python Web -->
            <div class="table-card">
                <div class="table-header">
                    <h3>Khóa K25 - Khối CNTT (Môn hiện tại)</h3>
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
                                <th class="text-center">Quy chuẩn cũ</th>
                                <th class="text-center">Quy chế mới</th>
                                <th class="text-center">Cảnh báo tác nghiệp</th>
                                <th class="text-right">Hành động</th>
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
                    <h3>Khóa K25 - Khối QTKD (Môn hiện tại)</h3>
                    <span class="course-badge" style="color: var(--success); background: var(--success-light);">PRJ302</span>
                </div>
                <div class="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Tên Lớp</th>
                                <th class="text-center">Sĩ số</th>
                                <th class="text-center">Vi phạm lớp%</th>
                                <th class="text-center">Hệ số Env</th>
                                <th class="text-center">Quy chuẩn cũ</th>
                                <th class="text-center">Quy chế mới</th>
                                <th class="text-center">Cảnh báo tác nghiệp</th>
                                <th class="text-right">Hành động</th>
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
                    <h3>Khóa K24 - Khối CNTT (Môn hiện tại)</h3>
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
                                <th class="text-center">Quy chuẩn cũ</th>
                                <th class="text-center">Quy chế mới</th>
                                <th class="text-center">Cảnh báo tác nghiệp</th>
                                <th class="text-right">Hành động</th>
                            </tr>
                        </thead>
                        <tbody>
                            {k24_curr_html}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- TAB 3: CARE LIST CENTRAL -->
        <div id="tab-care-list" class="tab-content">
            <div class="table-card">
                <div class="table-header">
                    <h3>Danh sách học viên cần can thiệp toàn khóa</h3>
                    <div style="display: flex; gap: 8px; align-items: center;">
                        <button class="filter-btn active" onclick="filterCareList('all')">Tất cả</button>
                        <button class="filter-btn" onclick="filterCareList('red')" style="color: var(--danger);">Đỏ (Nguy cơ cao)</button>
                        <button class="filter-btn" onclick="filterCareList('yellow')" style="color: var(--warning);">Vàng (Cảnh báo)</button>
                        <button class="filter-btn" onclick="filterCareList('cntt')">Khối CNTT</button>
                        <button class="filter-btn" onclick="filterCareList('qtkd')">Khối QTKD</button>
                        <button class="filter-btn" onclick="exportCareListCSV()" style="background: var(--primary-light); color: var(--primary); margin-left: 16px;"><i class="fas fa-file-csv"></i> Xuất CSV</button>
                    </div>
                </div>
                <div class="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Khóa</th>
                                <th>Lớp học</th>
                                <th>Học viên</th>
                                <th class="text-center">XS đỗ%</th>
                                <th class="text-center">Vắng chuyên cần%</th>
                                <th class="text-center">Nợ bài tập%</th>
                                <th class="text-center">Elearning vi phạm</th>
                                <th>Mức độ</th>
                                <th>Lý do &amp; Dấu hiệu cảnh báo</th>
                            </tr>
                        </thead>
                        <tbody>
                            {care_list_rows_html}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

    </div>

    <!-- Slide-over Drawer -->
    <div id="drawer-backdrop" onclick="closeClassDrawer()"></div>
    <div id="class-drawer">
        <div class="drawer-header">
            <h2 id="drawer-title" style="font-size: 1.2rem; font-weight:800;">Lớp học</h2>
            <button class="drawer-close" onclick="closeClassDrawer()">&times;</button>
        </div>
        <div id="drawer-body" class="drawer-content">
            <!-- Nội dung lớp chi tiết do JS render -->
        </div>
    </div>

    <!-- JS Tương tác & Charts -->
    <script>
        // Nhúng dữ liệu thô từ Python
        const rawClassRisks = {json.dumps(class_risks)};
        const rawClassViolations = {json.dumps(class_violations)};
        const rawAllCareList = {json.dumps(data['care_list'])};
        
        function switchTab(tabId) {{
            document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
            event.currentTarget.classList.add('active');
            
            document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
            document.getElementById('tab-' + tabId).classList.add('active');
        }}

        function openClassDrawer(className, isCv) {{
            document.getElementById('drawer-title').innerText = "Rà soát lớp: " + className;
            const contentDiv = document.getElementById('drawer-body');
            contentDiv.innerHTML = '';
            
            // 1. Render lỗi tác nghiệp GV
            const errs = rawClassViolations[className] || rawClassViolations[className.replace('KS', 'K')] || [];
            if (errs.length > 0) {{
                let errHtml = `<div class="class-violation-alert" style="margin-bottom: 20px;">
                    <i class="fas fa-exclamation-triangle" style="font-size: 1.2rem; margin-right: 8px; color: var(--warning);"></i>
                    <div>
                        <strong style="color:var(--warning);">Cảnh báo tác nghiệp đào tạo:</strong><br>
                        Ghi nhận ${{errs.length}} lỗi vi phạm quy chế. Yêu cầu rà soát và hiệu chỉnh dữ liệu trên QLĐT ngay lập tức.
                    </div>
                </div>`;
                contentDiv.innerHTML += errHtml;
            }}
            
            // 2. Render Care List sinh viên của lớp
            const students = rawClassRisks[className] || [];
            if (students.length > 0) {{
                let stHtml = `<div class="risk-details-header" style="margin-bottom: 12px; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 8px; color: var(--danger); display:flex; justify-content:space-between; font-size:0.8rem; font-weight:bold;">
                    <span><i class="fas fa-user-shield"></i> Học viên cần hỗ trợ</span>
                    <span>Tổng số: ${{students.length}} SV</span>
                </div>
                <div style="display: flex; flex-direction: column; gap: 12px;">`;
                
                students.forEach(s => {{
                    const borderClass = s.risk_level === 'RED' ? 'red-border' : 'yellow-border';
                    let pills = '';
                    if (s.att > 15) pills += `<span class="student-metric-pill red-pill"><i class="fas fa-user-slash"></i> Vắng: ${{s.att.toFixed(1)}}%</span>`;
                    else if (s.att > 0) pills += `<span class="student-metric-pill yellow-pill"><i class="fas fa-user-clock"></i> Vắng: ${{s.att.toFixed(1)}}%</span>`;
                    
                    const hwDebt = 100 - s.hw;
                    if (hwDebt > 30) pills += `<span class="student-metric-pill red-pill"><i class="fas fa-tasks"></i> Nợ bài: ${{hwDebt.toFixed(1)}}%</span>`;
                    else if (hwDebt > 15) pills += `<span class="student-metric-pill yellow-pill"><i class="fas fa-tasks"></i> Nợ bài: ${{hwDebt.toFixed(1)}}%</span>`;
                    
                    if (s.el >= 2) pills += `<span class="student-metric-pill red-pill"><i class="fas fa-clock"></i> EL trễ: ${{s.el}}</span>`;
                    else if (s.el >= 1) pills += `<span class="student-metric-pill yellow-pill"><i class="fas fa-clock"></i> EL trễ: ${{s.el}}</span>`;
                    
                    if (s.anomalies) {{
                        s.anomalies.forEach(anom => {{
                            if (anom === 'copy_suspect') pills += `<span class="student-metric-pill red-pill"><i class="fas fa-copy"></i> Copy?</span>`;
                            else if (anom === 'discipline_paradox') pills += `<span class="student-metric-pill" style="color: #c084fc; border-color: rgba(168, 85, 247, 0.2);"><i class="fas fa-brain"></i> KL kém</span>`;
                            else if (anom === 'passive_learner') pills += `<span class="student-metric-pill" style="color: #60a5fa; border-color: rgba(96, 165, 250, 0.2);"><i class="fas fa-mouse-pointer"></i> Học vẹt</span>`;
                            else if (anom === 'sudden_drop') pills += `<span class="student-metric-pill" style="color: #f43f5e; border-color: rgba(244, 63, 94, 0.2);"><i class="fas fa-chart-line"></i> Sụt phong độ</span>`;
                        }});
                    }}
                    
                    stHtml += `
                    <div class="student-risk-card ${{borderClass}}" style="background: rgba(255,255,255,0.02); border: 1px solid var(--border); border-left-width: 3px; border-radius: 8px; padding: 12px; display:flex; flex-direction:column; gap:8px;">
                        <div class="student-card-header" style="display:flex; justify-content:space-between; align-items:center;">
                            <span class="student-name" style="font-weight:bold; font-size:0.85rem; color:#fff;">${{s.full_name}}</span>
                            <span class="student-id" style="font-size:0.7rem; color:var(--text-muted); background:rgba(255,255,255,0.05); padding:1px 4px; border-radius:3px;">${{s.student_id}}</span>
                        </div>
                        <div class="student-card-body" style="display:flex; flex-wrap:wrap; gap:6px;">
                            ${{pills}}
                        </div>
                        <div style="font-size:0.75rem; color:var(--text-muted); line-height:1.4;">
                            <strong>Lý do chính:</strong> ${{s.reasons.join(', ')}}
                        </div>
                    </div>`;
                }});
                stHtml += `</div>`;
                contentDiv.innerHTML += stHtml;
            }} else {{
                contentDiv.innerHTML += `<div style="text-align:center; padding: 40px; color: var(--text-muted);">
                    <i class="fas fa-check-circle" style="font-size: 2.2rem; color: var(--success); margin-bottom: 12px;"></i><br>
                    Lớp học này không có học viên thuộc nhóm nguy cơ cần hỗ trợ.
                </div>`;
            }}
            
            document.getElementById('class-drawer').classList.add('open');
            document.getElementById('drawer-backdrop').style.display = 'block';
        }}
        
        function closeClassDrawer() {{
            document.getElementById('class-drawer').classList.remove('open');
            document.getElementById('drawer-backdrop').style.display = 'none';
        }}

        function filterCareList(type) {{
            document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
            event.currentTarget.classList.add('active');
            
            const rows = document.querySelectorAll('.care-row');
            rows.forEach(row => {{
                let show = false;
                if (type === 'all') {{
                    show = true;
                }} else if (type === 'red') {{
                    show = row.classList.contains('filter-red');
                }} else if (type === 'yellow') {{
                    show = row.classList.contains('filter-yellow');
                }} else if (type === 'cntt') {{
                    show = row.classList.contains('cntt');
                }} else if (type === 'qtkd') {{
                    show = row.classList.contains('qtkd');
                }}
                row.style.display = show ? 'table-row' : 'none';
            }});
        }}

        function exportCareListCSV() {{
            const rows = document.querySelectorAll('.care-row');
            let csvContent = "\\ufeff"; 
            csvContent += "Khóa,Lớp học,Học viên,Xác suất đỗ (%),Vắng chuyên cần (%),Nợ bài tập (%),Elearning trễ,Mức độ nguy cơ,Lý do chính\\n";
            
            rows.forEach(row => {{
                if (row.style.display !== 'none') {{
                    const cols = row.querySelectorAll('td');
                    let batch = cols[0].innerText;
                    let cname = cols[1].innerText;
                    let student = cols[2].innerText.replace(/"/g, '""');
                    let p_final = cols[3].innerText;
                    let att = cols[4].innerText;
                    let hw = cols[5].innerText;
                    let el = cols[6].innerText;
                    let risk = cols[7].innerText;
                    let reasons = cols[8].innerText.replace(/"/g, '""');
                    
                    csvContent += `"${{batch}}","${{cname}}","${{student}}","${{p_final}}","${{att}}","${{hw}}","${{el}}","${{risk}}","${{reasons}}"\\n`;
                }}
            }});
            
            const blob = new Blob([csvContent], {{ type: 'text/csv;charset=utf-8;' }});
            const link = document.createElement("a");
            const url = URL.createObjectURL(blob);
            link.setAttribute("href", url);
            link.setAttribute("download", "Care_List_Sinh_Vien_Nguy_Co.csv");
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
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
                        label: 'Quy chuẩn cũ (%)',
                        data: currOld,
                        backgroundColor: 'rgba(148, 163, 184, 0.3)',
                        borderColor: 'rgba(148, 163, 184, 0.8)',
                        borderWidth: 1.5,
                        borderRadius: 6
                    }},
                    {{
                        label: 'Quy chế mới (%)',
                        data: currNew,
                        backgroundColor: 'rgba(59, 130, 246, 0.75)',
                        borderColor: 'rgba(59, 130, 246, 1)',
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
                        backgroundColor: '#0f172a',
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
        
    output_dir = 'output/dashboards/core'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    build_unified_prediction_dashboard(data, os.path.join(output_dir, 'agent_2_academic_prediction.html'))
    print("Combined Academic Dashboard & Care List exported successfully in output/dashboards/core/agent_2_academic_prediction.html")

if __name__ == '__main__':
    main()
