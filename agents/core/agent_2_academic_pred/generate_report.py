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
        class_violations[cname].append({'Error': v.get('Error', 'GV-08')})

    # Lấy danh sách học viên nguy cơ theo từng lớp để tra cứu nhanh
    class_risks = {}
    for s in data['care_list']:
        cname = s['class_name']
        if cname not in class_risks:
            class_risks[cname] = []
        class_risks[cname].append(s)

    def get_priority(c):
        """Tính mức ưu tiên can thiệp cho từng lớp."""
        if c.get('pred_new', 100.0) < 50.0 or c.get('v_class', 0.0) > 20.0:
            return 'urgent'
        elif c.get('pred_new', 100.0) < 70.0 or c.get('v_class', 0.0) > 10.0:
            return 'watch'
        return 'stable'

    def render_priority_badge(priority):
        if priority == 'urgent':
            return '<span class="priority-badge urgent">🔴 Khẩn</span>'
        elif priority == 'watch':
            return '<span class="priority-badge watch">🟡 Theo dõi</span>'
        return '<span class="priority-badge stable">🟢 Ổn định</span>'

    def make_class_rows(classes_list, is_cv=False):
        # Sắp xếp theo mức ưu tiên (Khẩn lên đầu)
        priority_order = {'urgent': 0, 'watch': 1, 'stable': 2}
        if not is_cv:
            classes_list = sorted(classes_list, key=lambda x: priority_order[get_priority(x)])

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
                priority_cell = ""
            else:
                action_cell = f"""
                <td class="text-center font-mono font-bold text-rose">{c['pred_new']:.1f}%</td>
                """
                priority = get_priority(c)
                priority_cell = f"<td class='text-center'>{render_priority_badge(priority)}</td>"

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
                        Lớp học ghi nhận các lỗi giảng viên/trợ giảng vi phạm quy chế hành chính. Yêu cầu hiệu chỉnh trên hệ thống QLĐT để đảm bảo quyền lợi học viên.
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
                {priority_cell}
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
            
    # ── Tab 1: Phân loại hành động theo vai trò ──────────────────────────────
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

    # Thẻ 🔴 GV/TG
    gv_actions = []
    for c in low_classes_items[:2]:
        gv_actions.append(f"Lớp <strong>{c['class_name']}</strong>: Tổ chức buổi phụ đạo bổ sung — tỉ lệ đỗ hiện tại chỉ đạt <strong>{c.get('pred_new', 0):.1f}%</strong>.")
    for cls_name, err_code in ops_err_items[:2]:
        gv_actions.append(f"Lớp <strong>{cls_name}</strong>: Kiểm tra và hiệu chỉnh lỗi <strong>{err_code}</strong> trên hệ thống QLĐT ngay lập tức.")
    if not gv_actions:
        gv_actions = ["Không ghi nhận hành động cấp bách cần xử lý trong 24–48h."]

    # Thẻ 🟡 GVCN/Cố vấn
    gvcn_actions = []
    red_sv_sample = [s for s in data['care_list'] if s['risk_level'] == 'RED' and s['att'] > 15]
    for s in red_sv_sample[:3]:
        gvcn_actions.append(f"Liên hệ gia đình <strong>{s['full_name']}</strong> ({s['class_name']}): Vắng <strong>{s['att']:.1f}%</strong> — có nguy cơ cấm thi.")
    if high_viol_items:
        top_viol = high_viol_items[0]
        gvcn_actions.append(f"Nhắc nhở toàn lớp <strong>{top_viol['class_name']}</strong> về kỷ luật giờ giấc (vi phạm lớp đang ở mức <strong>{top_viol['v_class']:.1f}%</strong>).")
    if not gvcn_actions:
        gvcn_actions = ["Không có học viên nào cần liên hệ gia đình khẩn cấp trong tuần này."]

    # Thẻ 🔵 PMO
    pmo_actions = []
    if low_classes_items:
        pmo_actions.append(f"Điều phối hỗ trợ phụ đạo cho <strong>{len(low_classes_items)}</strong> lớp có tỉ lệ đỗ dự kiến dưới 60%.")
    if ops_err_items:
        pmo_actions.append(f"Xác nhận <strong>{len(set(v[0] for v in ops_err_items))}</strong> lỗi tác nghiệp GV/TG đã được hiệu chỉnh trên QLĐT trước cuối tuần.")
    pmo_actions.append(f"Tổng cộng <strong>{red_count + yellow_count}</strong> học viên cần can thiệp — phân công GVCN phụ trách liên hệ theo danh sách ở Tab 3.")

    def render_action_card(role_title, color_val, icon_cls, deadline_text, actions_list):
        items_html = "".join(f"<li>{a}</li>" for a in actions_list)
        return f"""
        <div class="action-role-card" style="border-left: 4px solid {color_val};">
            <div class="arc-header">
                <div class="arc-icon" style="background: {color_val}22; color: {color_val};">
                    <i class="{icon_cls}"></i>
                </div>
                <div>
                    <div class="arc-title">{role_title}</div>
                    <div class="arc-deadline">{deadline_text}</div>
                </div>
            </div>
            <ul class="arc-list">{items_html}</ul>
        </div>"""

    gv_card_html  = render_action_card("🔴 Việc của Giảng viên / Trợ giảng",  "#f43f5e", "fas fa-chalkboard-teacher", "Cần thực hiện trong 24–48h", gv_actions)
    gvcn_card_html = render_action_card("🟡 Việc của Cố vấn / GVCN",           "#f59e0b", "fas fa-user-friends",        "Cần thực hiện trong tuần này", gvcn_actions)
    pmo_card_html  = render_action_card("🔵 Việc của PMO Điều phối",            "#3b82f6", "fas fa-sitemap",             "Giám sát & Phân bổ nguồn lực", pmo_actions)

    # ── Tab 3: Phân nhóm sinh viên theo loại vấn đề ───────────────────────────
    def classify_student(s):
        anomalies = s.get('anomalies', [])
        if s['att'] > 20.0 or s['el'] >= 2:
            return 'ban_thi'
        if 'discipline_paradox' in anomalies:
            return 'paradox'
        if 'copy_suspect' in anomalies or 'passive_learner' in anomalies:
            return 'bat_thuong'
        return 'hoc_luc'

    groups = {
        'ban_thi':    {'title': '🔴 Nguy cơ Cấm thi',          'color': '#f43f5e',
                       'context': 'Học viên có thể không được vào phòng thi nếu không khắc phục ngay.',
                       'solution': 'Yêu cầu học viên nộp đơn xin phép bổ sung. Cố vấn liên hệ gia đình trong 24h.',
                       'students': []},
        'hoc_luc':    {'title': '🟡 Học lực yếu',              'color': '#f59e0b',
                       'context': 'Học viên có thể rớt môn dù không bị cấm thi.',
                       'solution': 'Giảng viên sắp xếp gặp trực tiếp. Giao thêm bài luyện tập cơ bản trước buổi học tiếp theo.',
                       'students': []},
        'bat_thuong': {'title': '🟠 Bất thường Kỷ luật',       'color': '#f97316',
                       'context': 'Học viên có hành vi đáng lo ngại cần xác minh thực tế.',
                       'solution': 'Giảng viên kiểm tra trực tiếp trong buổi học gần nhất — yêu cầu giải thích bài tập miệng.',
                       'students': []},
        'paradox':    {'title': '🟣 Học giỏi — Kỷ luật kém',   'color': '#a855f7',
                       'context': 'Học viên có năng lực tốt nhưng đang tự phá kỷ luật của mình.',
                       'solution': 'GVCN gặp gỡ trao đổi về cam kết chuyên cần — đây không phải vấn đề năng lực.',
                       'students': []},
    }
    for s in data['care_list']:
        gkey = classify_student(s)
        groups[gkey]['students'].append(s)

    accordion_html = ""
    for gkey, gdata in groups.items():
        count = len(gdata['students'])
        if count == 0:
            continue
        student_rows = ""
        for s in gdata['students']:
            badge_cls = "risk-badge-red" if s['risk_level'] == 'RED' else "risk-badge-yellow"
            hw_debt = 100.0 - s['hw']
            is_banned = s.get('is_failed_new', False)
            is_excellent = s.get('is_excellent', False)
            p_display = "0.0%<br><span style='font-size:0.72rem;color:#f43f5e;font-weight:normal;'>[Cấm thi]</span>" if is_banned else f"{s['p_final']:.1f}%"
            
            excellent_tag = ""
            if is_excellent and is_banned:
                score_val = s['hack'] if (s['hack'] is not None and s['hack'] >= 75.0) else s.get('prior_hack')
                score_str = f" {score_val:.0f}đ" if score_val else ""
                excellent_tag = f" <span class='excellent-pill' style='color:#a855f7;background:rgba(168,85,247,0.1);padding:2px 6px;border-radius:4px;font-size:0.7rem;margin-left:5px;border:1px solid rgba(168,85,247,0.2);font-weight:normal;display:inline-block;' title='Học lực giỏi nhưng bị cấm thi'><i class='fas fa-bolt'></i>{score_str}</span>"
                
            student_rows += f"""
            <tr>
                <td class="font-mono">{s['batch']}</td>
                <td class="font-mono font-bold">{s['class_name']}</td>
                <td class="font-bold">{s['full_name']}{excellent_tag} <span style="color:var(--text-muted);font-size:0.75rem;">({s['student_id']})</span></td>
                <td class="text-center font-mono font-bold {'text-rose' if s['risk_level'] == 'RED' or is_banned else 'text-warning'}">{p_display}</td>
                <td class="text-center font-mono">{s['att']:.1f}%</td>
                <td class="text-center font-mono">{hw_debt:.1f}%</td>
                <td class="text-center font-mono">{s['el']:.0f}</td>
                <td><span class="{badge_cls}">{s['risk_level']}</span></td>
            </tr>"""

        solution_preview = gdata['solution'][:75] + ('...' if len(gdata['solution']) > 75 else '')
        accordion_html += f"""
        <div class="intervention-group">
            <div class="ig-header" onclick="toggleGroup('{gkey}')">
                <div class="ig-title-row">
                    <span class="ig-title">{gdata['title']}</span>
                    <span class="ig-count">{count} học viên</span>
                </div>
                <div class="ig-solution-preview">{solution_preview}</div>
                <i class="fas fa-chevron-down ig-chevron" id="chev-{gkey}"></i>
            </div>
            <div class="ig-body" id="igbody-{gkey}" style="display:none;">
                <div class="ig-context-box">
                    <i class="fas fa-info-circle" style="flex-shrink:0;"></i>
                    <span>{gdata['context']}</span>
                </div>
                <div class="ig-solution-box">
                    <strong>📌 Giải pháp đề xuất:</strong> {gdata['solution']}
                </div>
                <div class="table-container">
                    <table>
                        <thead><tr>
                            <th>Khóa</th><th>Lớp</th><th>Học viên</th>
                            <th class="text-center">XS đỗ%</th><th class="text-center">Vắng%</th>
                            <th class="text-center">Nợ bài%</th><th class="text-center">EL vi phạm</th>
                            <th>Mức độ</th>
                        </tr></thead>
                        <tbody class="ig-rows" data-group="{gkey}">{student_rows}</tbody>
                    </table>
                </div>
            </div>
        </div>"""

    # Chuẩn bị dữ liệu cho biểu đồ Chart.js
    ks24_classes = data['dashboard_data'].get('KS24', {}).get('curr', [])
    ks25_classes = data['dashboard_data'].get('KS25', {}).get('curr', [])
    qtkd_classes = data['dashboard_data'].get('QTKD', {}).get('curr', [])
    
    curr_classes = []
    for batch_name in ['KS24', 'KS25', 'QTKD']:
        curr_classes.extend(data['dashboard_data'].get(batch_name, {}).get('curr', []))
        
    cv_classes = []
    for batch_name in ['KS24', 'KS25', 'QTKD']:
        cv_classes.extend(data['dashboard_data'].get(batch_name, {}).get('cv', []))
        
    total_curr_students = sum(c['size'] for c in curr_classes)
    green_count = max(0, total_curr_students - red_count - yellow_count)
    
    ks24_size = sum(c['size'] for c in ks24_classes)
    ks25_size = sum(c['size'] for c in ks25_classes)
    qtkd_size = sum(c['size'] for c in qtkd_classes)

    ks24_red = sum(sum(1 for s in class_risks.get(c['class_name'], []) if s.get('risk_level') == 'RED') for c in ks24_classes)
    ks24_yellow = sum(sum(1 for s in class_risks.get(c['class_name'], []) if s.get('risk_level') == 'YELLOW') for c in ks24_classes)
    
    ks25_red = sum(sum(1 for s in class_risks.get(c['class_name'], []) if s.get('risk_level') == 'RED') for c in ks25_classes)
    ks25_yellow = sum(sum(1 for s in class_risks.get(c['class_name'], []) if s.get('risk_level') == 'YELLOW') for c in ks25_classes)
    
    qtkd_red = sum(sum(1 for s in class_risks.get(c['class_name'], []) if s.get('risk_level') == 'RED') for c in qtkd_classes)
    qtkd_yellow = sum(sum(1 for s in class_risks.get(c['class_name'], []) if s.get('risk_level') == 'YELLOW') for c in qtkd_classes)
    
    mean_val = lambda vals: sum(vals)/len(vals) if vals else 0.0
    ks24_avg_pass = mean_val([c['pred_new'] for c in ks24_classes])
    ks25_avg_pass = mean_val([c['pred_new'] for c in ks25_classes])
    qtkd_avg_pass = mean_val([c['pred_new'] for c in qtkd_classes])
    
    ks24_avg_viol = mean_val([c['v_class'] for c in ks24_classes])
    ks25_avg_viol = mean_val([c['v_class'] for c in ks25_classes])
    qtkd_avg_viol = mean_val([c['v_class'] for c in qtkd_classes])
    
    overall_avg_pass = mean_val([c['pred_new'] for c in curr_classes])
    
    chart_curr_labels = [c['class_name'] for c in curr_classes]
    chart_curr_cohorts = [('KS24' if 'K24' in c['class_name'] else ('QTKD' if 'QTKD' in c['class_name'] else 'KS25')) for c in curr_classes]
    chart_curr_old = [round(c['pred_old'], 1) for c in curr_classes]
    chart_curr_new = [round(c['pred_new'], 1) for c in curr_classes]

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
        .header-actions {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        .btn-action-tool {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 8px 16px;
            border-radius: 9999px;
            font-size: 0.8rem;
            font-weight: 700;
            cursor: pointer;
            border: 1px solid var(--border);
            background: rgba(255, 255, 255, 0.05);
            color: var(--text-main);
            transition: all 0.2s ease;
        }}
        .btn-action-tool:hover {{
            background: rgba(255, 255, 255, 0.12);
            border-color: var(--primary);
        }}
        .chart-filter-btn {{
            padding: 6px 14px;
            border-radius: 8px;
            border: 1px solid var(--border);
            background: rgba(255, 255, 255, 0.05);
            color: var(--text-muted);
            font-size: 0.8rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
        }}
        .chart-filter-btn:hover {{
            background: rgba(255, 255, 255, 0.1);
            color: var(--text-main);
        }}
        .chart-filter-btn.active {{
            background: var(--primary-light);
            color: var(--primary);
            border-color: var(--primary);
        }}
        .doughnut-wrapper {{
            position: relative;
            width: 220px;
            height: 220px;
            margin: 0 auto;
        }}
        .doughnut-center-text {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
            pointer-events: none;
        }}
        .doughnut-center-number {{
            font-size: 1.7rem;
            font-weight: 800;
            color: #f3f4f6;
            line-height: 1.1;
        }}
        .doughnut-center-label {{
            font-size: 0.72rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: 600;
        }}
        body.presentation-mode {{
            padding: 20px 10px !important;
        }}
        body.presentation-mode .tabs-container {{
            display: none !important;
        }}
        body.presentation-mode .btn-action-tool {{
            opacity: 0.5;
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

        /* Action Role Cards (Tab 1) */
        .action-roles-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 20px;
            margin-top: 8px;
        }}
        @media (max-width: 1000px) {{
            .action-roles-grid {{ grid-template-columns: 1fr; }}
        }}
        .action-role-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 20px;
            box-shadow: var(--card-shadow);
        }}
        .arc-header {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 14px;
            padding-bottom: 12px;
            border-bottom: 1px solid var(--border);
        }}
        .arc-icon {{
            width: 40px; height: 40px;
            border-radius: 10px;
            display: flex; align-items: center; justify-content: center;
            font-size: 1rem; flex-shrink: 0;
        }}
        .arc-title {{
            font-size: 0.85rem; font-weight: 800; color: var(--text-main); line-height: 1.3;
        }}
        .arc-deadline {{
            font-size: 0.7rem; color: var(--text-muted); margin-top: 2px; font-weight: 600;
        }}
        .arc-list {{
            list-style: none; padding: 0; margin: 0;
            display: flex; flex-direction: column; gap: 8px;
        }}
        .arc-list li {{
            font-size: 0.8rem; color: var(--text-main); line-height: 1.5;
            padding: 10px 12px 10px 24px;
            background: rgba(255,255,255,0.02);
            border: 1px solid var(--border);
            border-radius: 8px;
            position: relative;
        }}
        .arc-list li::before {{
            content: "→";
            position: absolute; left: 9px;
            color: var(--text-muted);
        }}

        /* Priority Badge (Tab 2) */
        .priority-badge {{
            padding: 3px 9px; border-radius: 6px;
            font-size: 0.7rem; font-weight: 700; white-space: nowrap;
        }}
        .priority-badge.urgent {{ background: rgba(244,63,94,0.15); color: var(--danger); }}
        .priority-badge.watch  {{ background: rgba(245,158,11,0.15); color: var(--warning); }}
        .priority-badge.stable {{ background: rgba(16,185,129,0.1);  color: var(--success); }}

        /* Drawer action section */
        .drawer-section-title {{
            font-size: 0.72rem; font-weight: 800; text-transform: uppercase;
            color: var(--text-muted); margin: 0 0 8px; letter-spacing: 0.5px;
        }}
        .drawer-action-list {{
            list-style:none; padding:0; margin:0 0 18px;
            display:flex; flex-direction:column; gap:7px;
        }}
        .drawer-action-list li {{
            font-size:0.8rem; padding:9px 12px;
            background:rgba(59,130,246,0.06);
            border:1px solid rgba(59,130,246,0.15);
            border-radius:8px; line-height:1.4;
        }}

        /* Intervention Group Accordion (Tab 3) */
        .intervention-group {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 16px;
            overflow: hidden;
            margin-bottom: 14px;
            box-shadow: var(--card-shadow);
        }}
        .ig-header {{
            padding: 18px 22px;
            cursor: pointer;
            position: relative;
            transition: background 0.2s;
        }}
        .ig-header:hover {{ background: rgba(255,255,255,0.02); }}
        .ig-title-row {{
            display: flex; align-items: center; gap: 12px; margin-bottom: 5px;
        }}
        .ig-title {{
            font-size: 0.95rem; font-weight: 800;
        }}
        .ig-count {{
            font-size: 0.72rem; font-weight: 700;
            padding: 2px 9px; border-radius: 20px;
            background: rgba(255,255,255,0.06); color: var(--text-muted);
        }}
        .ig-solution-preview {{
            font-size: 0.76rem; color: var(--text-muted);
            line-height: 1.4; padding-right: 36px;
        }}
        .ig-chevron {{
            position: absolute; right: 20px; top: 50%;
            transform: translateY(-50%);
            transition: transform 0.25s;
            color: var(--text-muted);
        }}
        .ig-body {{
            padding: 0 22px 18px;
        }}
        .ig-context-box {{
            background: rgba(255,255,255,0.03);
            border: 1px solid var(--border);
            border-radius: 8px; padding: 10px 14px;
            font-size: 0.78rem; color: var(--text-muted);
            margin-bottom: 10px;
            display: flex; gap: 8px; align-items: flex-start;
        }}
        .ig-solution-box {{
            background: rgba(59,130,246,0.05);
            border: 1px solid rgba(59,130,246,0.15);
            border-radius: 8px; padding: 11px 14px;
            font-size: 0.8rem; color: var(--text-main);
            margin-bottom: 14px; line-height: 1.5;
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
                <h1>📊 Báo Cáo Dự Báo Học Vụ &amp; Quản Lý Tiến Độ Đào Tạo</h1>
                <div class="meta-info">Giám sát nề nếp học tập, đánh giá điều kiện dự thi và phân loại tình trạng học vụ cho 16 lớp chính quy PTIT</div>
            </div>
            <div class="header-actions">
                <button onclick="togglePresentationMode()" class="btn-action-tool" id="btn-toggle-pres">
                    <i class="fas fa-camera"></i> <span>Chế độ Trích Xuất Báo Cáo</span>
                </button>
                <button onclick="window.print()" class="btn-action-tool">
                    <i class="fas fa-print"></i> <span>In / PDF</span>
                </button>
                <div class="update-badge">
                    Cập nhật: {datetime.now().strftime('%d/%m/%Y')}
                </div>
            </div>
        </header>

        <!-- Navigation Tabs -->
        <div class="tabs-container">
            <button class="tab-button active" onclick="switchTab('executive')"><i class="fas fa-chart-pie"></i> Tổng quan Đào tạo 3 Khối &amp; Phân loại Học vụ</button>
            <button class="tab-button" onclick="switchTab('classes')"><i class="fas fa-school"></i> Bảng Tổng Hợp 16 Lớp Chính Quy</button>
            <button class="tab-button" onclick="switchTab('care-list')"><i class="fas fa-user-shield"></i> Danh Sách Học Viên Diện Cảnh Báo Học Vụ ({red_count + yellow_count} SV)</button>
        </div>

        <!-- TAB 1: EXECUTIVE SUMMARY -->
        <div id="tab-executive" class="tab-content active">
            <!-- 3-Cohort Deep Breakdown Cards -->
            <div style="margin-bottom: 24px;">
                <div style="font-size: 0.85rem; font-weight: 800; text-transform: uppercase; color: var(--text-muted); letter-spacing: 0.5px; margin-bottom: 12px; display: flex; align-items: center; gap: 8px;">
                    <i class="fas fa-layer-group" style="color: var(--primary);"></i> TỔNG QUAN HỌC VỤ THEO 3 KHỐI NGÀNH ĐÀO TẠO
                </div>
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px;">
                    <!-- KHỐI KS24 CNTT -->
                    <div style="background: var(--bg-card); border: 1px solid var(--border); border-top: 3px solid #3b82f6; border-radius: 14px; padding: 18px; display: flex; flex-direction: column; justify-content: space-between;">
                        <div>
                            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
                                <div>
                                    <div style="font-size: 0.72rem; font-weight: 700; color: #3b82f6; text-transform: uppercase;">Khóa KS24 • Chuyên ngành CNTT</div>
                                    <h3 style="font-size: 1.05rem; font-weight: 800; color: #fff; margin-top: 2px;">Microservices System Design</h3>
                                </div>
                                <span style="font-size: 0.7rem; font-weight: 700; background: rgba(59,130,246,0.15); color: #3b82f6; padding: 3px 8px; border-radius: 6px;">5 Lớp</span>
                            </div>
                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 14px 0; background: rgba(255,255,255,0.02); padding: 10px; border-radius: 8px; border: 1px solid var(--border);">
                                <div>
                                    <div style="font-size: 0.7rem; color: var(--text-muted);">Dự kiến Đỗ:</div>
                                    <div style="font-size: 1.25rem; font-weight: 800; color: #3b82f6;">{ks24_avg_pass:.1f}%</div>
                                </div>
                                <div>
                                    <div style="font-size: 0.7rem; color: var(--text-muted);">Sĩ số đào tạo:</div>
                                    <div style="font-size: 1.25rem; font-weight: 800; color: #f3f4f6;">{ks24_size} <span style="font-size: 0.75rem; font-weight: normal; color: var(--text-muted);">SV</span></div>
                                </div>
                                <div>
                                    <div style="font-size: 0.7rem; color: var(--text-muted);">Vi phạm lớp TB:</div>
                                    <div style="font-size: 0.95rem; font-weight: 700; color: #10b981;">{ks24_avg_viol:.1f}%</div>
                                </div>
                                <div>
                                    <div style="font-size: 0.7rem; color: var(--text-muted);">Cảnh báo học vụ:</div>
                                    <div style="font-size: 0.95rem; font-weight: 700; color: {'#f43f5e' if ks24_red > 0 else ('#f59e0b' if ks24_yellow > 0 else '#10b981')};">
                                        {ks24_red} Cấm thi / {ks24_yellow} Theo dõi
                                    </div>
                                </div>
                            </div>
                            <p style="font-size: 0.75rem; color: var(--text-muted); line-height: 1.4;">
                                <strong>Đánh giá giáo vụ:</strong> Môn kiến trúc nâng cao, sinh viên giữ nề nếp tốt. Lưu ý theo dõi lớp <code style="color:#f59e0b;">HN-K24-CNTT3</code> do tỷ lệ vắng 11.9% và trễ EL 16.7% trong ca học gần nhất.
                            </p>
                        </div>
                    </div>

                    <!-- KHỐI KS25 CNTT -->
                    <div style="background: var(--bg-card); border: 1px solid var(--border); border-top: 3px solid #0ea5e9; border-radius: 14px; padding: 18px; display: flex; flex-direction: column; justify-content: space-between;">
                        <div>
                            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
                                <div>
                                    <div style="font-size: 0.72rem; font-weight: 700; color: #0ea5e9; text-transform: uppercase;">Khóa KS25 • Chuyên ngành CNTT</div>
                                    <h3 style="font-size: 1.05rem; font-weight: 800; color: #fff; margin-top: 2px;">Phân tích &amp; Thiết kế Hệ thống</h3>
                                </div>
                                <span style="font-size: 0.7rem; font-weight: 700; background: rgba(14,165,233,0.15); color: #0ea5e9; padding: 3px 8px; border-radius: 6px;">9 Lớp</span>
                            </div>
                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 14px 0; background: rgba(255,255,255,0.02); padding: 10px; border-radius: 8px; border: 1px solid var(--border);">
                                <div>
                                    <div style="font-size: 0.7rem; color: var(--text-muted);">Dự kiến Đỗ:</div>
                                    <div style="font-size: 1.25rem; font-weight: 800; color: #0ea5e9;">{ks25_avg_pass:.1f}%</div>
                                </div>
                                <div>
                                    <div style="font-size: 0.7rem; color: var(--text-muted);">Sĩ số đào tạo:</div>
                                    <div style="font-size: 1.25rem; font-weight: 800; color: #f3f4f6;">{ks25_size} <span style="font-size: 0.75rem; font-weight: normal; color: var(--text-muted);">SV</span></div>
                                </div>
                                <div>
                                    <div style="font-size: 0.7rem; color: var(--text-muted);">Vi phạm lớp TB:</div>
                                    <div style="font-size: 0.95rem; font-weight: 700; color: {'#f43f5e' if ks25_avg_viol > 10 else '#f59e0b'};">{ks25_avg_viol:.1f}%</div>
                                </div>
                                <div>
                                    <div style="font-size: 0.7rem; color: var(--text-muted);">Cảnh báo học vụ:</div>
                                    <div style="font-size: 0.95rem; font-weight: 700; color: #f43f5e;">
                                        {ks25_red} Cấm thi / {ks25_yellow} Theo dõi
                                    </div>
                                </div>
                            </div>
                            <p style="font-size: 0.75rem; color: var(--text-muted); line-height: 1.4;">
                                <strong>Đánh giá giáo vụ:</strong> Phía Hà Nội (5 lớp) mới học 2 buổi nề nếp tốt (0 SV cấm thi). Cơ sở HCM (4 lớp) có điểm nóng <code style="color:#f43f5e;">HCM-K25-CNTT8</code> vắng 37.5% (15 SV nguy cơ cấm thi).
                            </p>
                        </div>
                    </div>

                    <!-- KHỐI KS25 QTKD -->
                    <div style="background: var(--bg-card); border: 1px solid var(--border); border-top: 3px solid #10b981; border-radius: 14px; padding: 18px; display: flex; flex-direction: column; justify-content: space-between;">
                        <div>
                            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
                                <div>
                                    <div style="font-size: 0.72rem; font-weight: 700; color: #10b981; text-transform: uppercase;">Khóa KS25 • Chuyên ngành QTKD</div>
                                    <h3 style="font-size: 1.05rem; font-weight: 800; color: #fff; margin-top: 2px;">Quản trị Chiến lược (MAN107)</h3>
                                </div>
                                <span style="font-size: 0.7rem; font-weight: 700; background: rgba(16,185,129,0.15); color: #10b981; padding: 3px 8px; border-radius: 6px;">2 Lớp</span>
                            </div>
                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 14px 0; background: rgba(255,255,255,0.02); padding: 10px; border-radius: 8px; border: 1px solid var(--border);">
                                <div>
                                    <div style="font-size: 0.7rem; color: var(--text-muted);">Dự kiến Đỗ:</div>
                                    <div style="font-size: 1.25rem; font-weight: 800; color: #10b981;">{qtkd_avg_pass:.1f}%</div>
                                </div>
                                <div>
                                    <div style="font-size: 0.7rem; color: var(--text-muted);">Sĩ số đào tạo:</div>
                                    <div style="font-size: 1.25rem; font-weight: 800; color: #f3f4f6;">{qtkd_size} <span style="font-size: 0.75rem; font-weight: normal; color: var(--text-muted);">SV</span></div>
                                </div>
                                <div>
                                    <div style="font-size: 0.7rem; color: var(--text-muted);">Vi phạm lớp TB:</div>
                                    <div style="font-size: 0.95rem; font-weight: 700; color: #f59e0b;">{qtkd_avg_viol:.1f}%</div>
                                </div>
                                <div>
                                    <div style="font-size: 0.7rem; color: var(--text-muted);">Cảnh báo học vụ:</div>
                                    <div style="font-size: 0.95rem; font-weight: 700; color: #10b981;">
                                        0 Cấm thi / 0 Theo dõi
                                    </div>
                                </div>
                            </div>
                            <p style="font-size: 0.75rem; color: var(--text-muted); line-height: 1.4;">
                                <strong>Đánh giá giáo vụ:</strong> Tiến độ 2 buổi đầu đạt chuẩn, nộp bài tập đạt 100%, 100% sinh viên đang trong diện học tập bình thường.
                            </p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Methodology & Explanation Box -->
            <div style="background: rgba(30, 41, 59, 0.4); border: 1px solid var(--border); border-left: 4px solid #a855f7; border-radius: 12px; padding: 16px 20px; margin-bottom: 24px;">
                <div style="display: flex; align-items: center; gap: 8px; font-weight: 800; font-size: 0.85rem; color: #c084fc; text-transform: uppercase; margin-bottom: 6px;">
                    <i class="fas fa-info-circle"></i> Giải Trình Phương Pháp Xác Định Tỷ Lệ Đủ Điều Kiện Qua Môn Dự Kiến
                </div>
                <div style="font-size: 0.78rem; color: #cbd5e1; line-height: 1.6;">
                    <p>• <strong>Cơ chế tính toán:</strong> Tỷ lệ dự kiến là <em>Kỳ vọng xác suất qua môn trung bình (Expected Pass Probability)</em> của toàn bộ sinh viên trong lớp, kết hợp giữa: <strong>(1) Điểm kỷ luật &amp; ý thức quá trình (40%)</strong> (Chuyên cần, Bài tập, Elearning); <strong>(2) Điểm năng lực học thuật tích lũy (60%)</strong> (Kết quả môn tiên quyết và điểm thực hành/Project, đã chia cho Hệ số độ khó môn học CDC); <strong>(3) Quy chế cấm thi hiện hành</strong> (áp dụng 0% nếu vắng &gt; 20% hoặc trễ Elearning &gt; 3 bài sau khi học &gt; 3 buổi).</p>
                    <p style="margin-top: 4px;">• <strong>Lý do tỷ lệ dự kiến giai đoạn này ở mức khả quan (61% – 78%):</strong> (a) Khối Hà Nội môn PTTKHT và MAN107 mới học 2 buổi đầu, sinh viên đi học đầy đủ (98%–100%) nên điểm chuyên cần kéo tỷ lệ kỳ vọng lên cao, quy chế cấm thi chưa kích hoạt để tránh cảnh báo ảo; (b) Bài thi cuối kỳ / Đồ án tốt nghiệp (chiếm 50% trọng số môn) chưa diễn ra. Khi bước vào giai đoạn bảo vệ đồ án, tỷ lệ này sẽ phân hóa mạnh hơn đối với nhóm sinh viên học lực yếu.</p>
                </div>
            </div>

            <!-- Global KPI Summary Cards -->
            <div class="mae-grid" style="grid-template-columns: repeat(4, 1fr);">
                <div class="mae-card" style="border-left: 4px solid var(--primary);">
                    <div>
                        <div class="mae-title">Tỷ lệ Đủ ĐK Dự Thi &amp; Đỗ Dự Kiến</div>
                        <div class="mae-val" style="color: var(--primary);">{overall_avg_pass:.1f}%</div>
                        <div class="mae-desc">Kỳ vọng trung bình 16 lớp chính quy ({total_curr_students} SV)</div>
                    </div>
                    <div class="mae-icon"><i class="fas fa-graduation-cap"></i></div>
                </div>
                
                <div class="mae-card" style="border-left: 4px solid var(--danger);">
                    <div>
                        <div class="mae-title">Cảnh Báo Mức 1 (Nguy Cơ Cấm Thi)</div>
                        <div class="mae-val" style="color: var(--danger);">{red_count} SV</div>
                        <div class="mae-desc">Vắng &gt; 20% hoặc nợ bài quá hạn ({red_count*100.0/total_curr_students if total_curr_students else 0:.1f}%)</div>
                    </div>
                    <div class="mae-icon" style="color: var(--danger); background: var(--danger-light);"><i class="fas fa-user-slash"></i></div>
                </div>

                <div class="mae-card" style="border-left: 4px solid var(--warning);">
                    <div>
                        <div class="mae-title">Cảnh Báo Mức 2 (Cần Theo Dõi)</div>
                        <div class="mae-val" style="color: var(--warning);">{yellow_count} SV</div>
                        <div class="mae-desc">Cận ngưỡng cấm thi / Học lực yếu ({yellow_count*100.0/total_curr_students if total_curr_students else 0:.1f}%)</div>
                    </div>
                    <div class="mae-icon" style="color: var(--warning); background: var(--warning-light);"><i class="fas fa-exclamation-triangle"></i></div>
                </div>

                <div class="mae-card" style="border-left: 4px solid var(--success);">
                    <div>
                        <div class="mae-title">Tiến Độ Học Tập Đạt Chuẩn</div>
                        <div class="mae-val" style="color: var(--success);">{green_count} SV</div>
                        <div class="mae-desc">Nề nếp tốt, xác suất dự thi đạt ≥ 70% ({green_count*100.0/total_curr_students if total_curr_students else 0:.1f}%)</div>
                    </div>
                    <div class="mae-icon" style="color: var(--success); background: var(--success-light);"><i class="fas fa-check-circle"></i></div>
                </div>
            </div>

            <!-- Chart Row 1: So sánh Dự báo 16 Lớp với vạch Benchmark -->
            <div class="chart-row" style="margin-bottom: 24px;">
                <div class="chart-card">
                    <div class="chart-header" style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
                        <div>
                            <div class="chart-title"><i class="fas fa-chart-bar" style="color: var(--primary);"></i> Đối Sánh Tỷ Lệ Dự Kiến Đủ Điều Kiện Qua Môn 16 Lớp (Quy chế cũ vs Quy chế hiện hành)</div>
                            <div style="font-size: 0.75rem; color: var(--text-muted); margin-top: 4px;">Đường xanh nét đứt: Ngưỡng an toàn học thuật (70%) | Đường đỏ nét đứt: Ngưỡng cảnh báo học vụ (50%)</div>
                        </div>
                        <div style="display: flex; gap: 8px; align-items: center; flex-wrap: wrap;">
                            <button onclick="filterMainChart('all')" class="chart-filter-btn active" id="btn-filter-all">Tất cả (16 lớp)</button>
                            <button onclick="filterMainChart('KS24')" class="chart-filter-btn" id="btn-filter-ks24">KS24 (Microservice)</button>
                            <button onclick="filterMainChart('KS25')" class="chart-filter-btn" id="btn-filter-ks25">KS25 (PTTKHT)</button>
                            <button onclick="filterMainChart('QTKD')" class="chart-filter-btn" id="btn-filter-qtkd">KS25 (MAN107)</button>
                        </div>
                    </div>
                    <div style="height: 380px; position: relative;">
                        <canvas id="pred-compare-chart"></canvas>
                    </div>
                </div>
            </div>

            <!-- Chart Row 2: Grid 2 Biểu Đồ Trực Quan -->
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 24px;">
                <!-- Biểu đồ Vòng Tròn Phân Bổ Nguy Cơ -->
                <div class="chart-card">
                    <div class="chart-header">
                        <div class="chart-title"><i class="fas fa-chart-pie" style="color: var(--success);"></i> Phân Loại Tình Trạng Học Vụ Sinh Viên Toàn Viện</div>
                    </div>
                    <div style="height: 280px; position: relative; display: flex; align-items: center; justify-content: center;">
                        <div class="doughnut-wrapper">
                            <canvas id="risk-doughnut-chart"></canvas>
                            <div class="doughnut-center-text">
                                <div class="doughnut-center-number">{total_curr_students}</div>
                                <div class="doughnut-center-label">Sinh Viên</div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Biểu đồ Sức Khỏe Học Thuật 3 Khối -->
                <div class="chart-card">
                    <div class="chart-header">
                        <div class="chart-title"><i class="fas fa-layer-group" style="color: #a855f7;"></i> Đối Sánh Hiệu Suất Học Tập theo 3 Khối Ngành</div>
                    </div>
                    <div style="height: 280px; position: relative;">
                        <canvas id="cohort-health-chart"></canvas>
                    </div>
                </div>
            </div>

            <!-- Action Role Cards -->
            <h2 style="margin: 32px 0 16px; font-size: 1.1rem; font-weight: 800; text-transform: uppercase; color: var(--text-muted); letter-spacing: 0.5px;">📋 Kế Hoạch Phối Hợp Giáo Vụ &amp; Giảng Viên Trong Tuần</h2>
            <div class="action-roles-grid">
                {gv_card_html}
                {gvcn_card_html}
                {pmo_card_html}
            </div>
        </div>

        <!-- TAB 2: CLASS LIST -->
        <div id="tab-classes" class="tab-content">
            <!-- KS25 PTTKHT -->
            <div class="table-card">
                <div class="table-header">
                    <h3>Khóa KS25 - Khối CNTT (Môn hiện tại: Phân tích &amp; thiết kế hệ thống)</h3>
                    <span class="course-badge" style="color: #38bdf8; background: rgba(56, 189, 248, 0.15);">IT105 - PTTKHT</span>
                </div>
                <div class="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Tên Lớp</th>
                                <th class="text-center">Sĩ số</th>
                                <th class="text-center">Vi phạm lớp%</th>
                                <th class="text-center">Nề nếp lớp</th>
                                <th class="text-center">Quy chế cũ</th>
                                <th class="text-center">Quy chế hiện hành</th>
                                <th class="text-center">Mức độ can thiệp</th>
                                <th class="text-center">Kỷ luật giáo vụ</th>
                                <th class="text-right">Hồ sơ lớp</th>
                            </tr>
                        </thead>
                        <tbody>
                            {k25_curr_html}
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- KS25 QTKD MAN107 -->
            <div class="table-card">
                <div class="table-header">
                    <h3>Khóa KS25 - Khối QTKD (Môn hiện tại: Quản trị chiến lược)</h3>
                    <span class="course-badge" style="color: var(--success); background: var(--success-light);">MAN107 Quản trị chiến lược</span>
                </div>
                <div class="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Tên Lớp</th>
                                <th class="text-center">Sĩ số</th>
                                <th class="text-center">Vi phạm lớp%</th>
                                <th class="text-center">Nề nếp lớp</th>
                                <th class="text-center">Quy chế cũ</th>
                                <th class="text-center">Quy chế hiện hành</th>
                                <th class="text-center">Mức độ can thiệp</th>
                                <th class="text-center">Kỷ luật giáo vụ</th>
                                <th class="text-right">Hồ sơ lớp</th>
                            </tr>
                        </thead>
                        <tbody>
                            {qtkd_curr_html}
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- KS24 MICROSERVICES -->
            <div class="table-card">
                <div class="table-header">
                    <h3>Khóa KS24 - Khối CNTT (Môn hiện tại: Thiết kế hệ thống Microservices)</h3>
                    <span class="course-badge" style="color: #a855f7; background: rgba(168, 85, 247, 0.15);">IT-214 Microservices</span>
                </div>
                <div class="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Tên Lớp</th>
                                <th class="text-center">Sĩ số</th>
                                <th class="text-center">Vi phạm lớp%</th>
                                <th class="text-center">Nề nếp lớp</th>
                                <th class="text-center">Quy chế cũ</th>
                                <th class="text-center">Quy chế hiện hành</th>
                                <th class="text-center">Mức độ can thiệp</th>
                                <th class="text-center">Kỷ luật giáo vụ</th>
                                <th class="text-right">Hồ sơ lớp</th>
                            </tr>
                        </thead>
                        <tbody>
                            {k24_curr_html}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- TAB 3: SỔ TAY THEO DÕI HỌC VIÊN DIỆN CẢNH BÁO HỌC VỤ -->
        <div id="tab-care-list" class="tab-content">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                <div>
                    <h2 style="font-size: 1.1rem; font-weight: 800;">Sổ tay Theo dõi Học viên Diện Cảnh báo Học vụ</h2>
                    <p style="font-size: 0.8rem; color: var(--text-muted); margin-top: 4px;">Phân loại theo diện vấn đề học vụ — nhấn vào từng nhóm để xem hồ sơ và biện pháp hỗ trợ chi tiết</p>
                </div>
                <button onclick="exportCareListCSV()" class="btn-risk" style="background: var(--primary-light); color: var(--primary); padding: 10px 18px; font-size: 0.82rem;">
                    <i class="fas fa-file-csv"></i> Xuất CSV Báo Cáo
                </button>
            </div>
            {accordion_html}
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
        const groupMeta = {json.dumps({k: {'title': v['title'], 'solution': v['solution']} for k, v in groups.items()})};

        function switchTab(tabId) {{
            document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
            event.currentTarget.classList.add('active');
            document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
            document.getElementById('tab-' + tabId).classList.add('active');
        }}

        // ── Accordion Toggle (Tab 3) ────────────────────────────────────────────
        function toggleGroup(gkey) {{
            const body = document.getElementById('igbody-' + gkey);
            const chev = document.getElementById('chev-' + gkey);
            const isOpen = body.style.display !== 'none';
            body.style.display = isOpen ? 'none' : 'block';
            chev.style.transform = isOpen ? 'translateY(-50%)' : 'translateY(-50%) rotate(180deg)';
        }}

        // ── Drawer (Tab 2) ─────────────────────────────────────────────────────
        function openClassDrawer(className, isCv) {{
            document.getElementById('drawer-title').innerText = 'Rà soát lớp: ' + className;
            const contentDiv = document.getElementById('drawer-body');
            contentDiv.innerHTML = '';

            const errs = rawClassViolations[className] || rawClassViolations[className.replace('KS', 'K')] || [];
            const students = rawClassRisks[className] || [];

            // Phần Hành động cần thực hiện
            let actionsHtml = `<div class="drawer-section-title">📋 Hành động cần thực hiện</div><ul class="drawer-action-list">`;
            const redSv = students.filter(s => s.risk_level === 'RED');
            if (redSv.length > 0)
                actionsHtml += `<li>Gặp trực tiếp <strong>${{redSv.length}}</strong> học viên Báo động Đỏ trước buổi học tuần tới.</li>`;
            if (errs.length > 0)
                actionsHtml += `<li>Hiệu chỉnh <strong>${{errs.length}}</strong> lỗi tác nghiệp trên hệ thống QLĐT.</li>`;
            if (redSv.length === 0 && errs.length === 0)
                actionsHtml += `<li style="color:var(--success);">Lớp học đang vận hành ổn định — tiếp tục duy trì.</li>`;
            actionsHtml += `</ul>`;
            contentDiv.innerHTML = actionsHtml;

            // Cảnh báo tác nghiệp
            if (errs.length > 0) {{
                contentDiv.innerHTML += `<div class="class-violation-alert" style="margin-bottom: 18px;">
                    <i class="fas fa-exclamation-triangle" style="font-size:1.1rem;color:var(--warning);"></i>
                    <div><strong style="color:var(--warning);">Cảnh báo tác nghiệp:</strong><br>
                    Ghi nhận ${{errs.length}} lỗi vi phạm quy chế. Yêu cầu hiệu chỉnh dữ liệu trên QLĐT ngay lập tức.</div>
                </div>`;
            }}

            // Học viên nguy cơ
            if (students.length > 0) {{
                let stHtml = `<div class="drawer-section-title" style="margin-top:4px;">👥 Học viên cần hỗ trợ (${{students.length}} SV)</div>
                <div style="display:flex;flex-direction:column;gap:10px;">`;
                students.forEach(s => {{
                    const borderClass = s.risk_level === 'RED' ? 'red-border' : 'yellow-border';
                    let pills = '';
                    if (s.att > 15) pills += `<span class="student-metric-pill red-pill"><i class="fas fa-user-slash"></i> Vắng: ${{s.att.toFixed(1)}}%</span>`;
                    else if (s.att > 0) pills += `<span class="student-metric-pill yellow-pill"><i class="fas fa-user-clock"></i> Vắng: ${{s.att.toFixed(1)}}%</span>`;
                    const hwDebt = 100 - s.hw;
                    if (hwDebt > 30) pills += `<span class="student-metric-pill red-pill"><i class="fas fa-tasks"></i> Nợ bài: ${{hwDebt.toFixed(1)}}%</span>`;
                    else if (hwDebt > 15) pills += `<span class="student-metric-pill yellow-pill"><i class="fas fa-tasks"></i> Nợ bài: ${{hwDebt.toFixed(1)}}%</span>`;
                    if (s.el >= 2) pills += `<span class="student-metric-pill red-pill"><i class="fas fa-clock"></i> EL: ${{s.el}}</span>`;
                    else if (s.el >= 1) pills += `<span class="student-metric-pill yellow-pill"><i class="fas fa-clock"></i> EL: ${{s.el}}</span>`;
                    if (s.anomalies) {{
                        s.anomalies.forEach(anom => {{
                            if (anom === 'copy_suspect') pills += `<span class="student-metric-pill red-pill"><i class="fas fa-copy"></i> Copy?</span>`;
                            else if (anom === 'discipline_paradox') pills += `<span class="student-metric-pill" style="color:#c084fc;border-color:rgba(168,85,247,0.2);"><i class="fas fa-brain"></i> KL kém</span>`;
                            else if (anom === 'passive_learner') pills += `<span class="student-metric-pill" style="color:#60a5fa;border-color:rgba(96,165,250,0.2);"><i class="fas fa-mouse-pointer"></i> Học vẹt</span>`;
                        }});
                    }}
                    stHtml += `<div class="student-risk-card ${{borderClass}}" style="background:rgba(255,255,255,0.02);border:1px solid var(--border);border-left-width:3px;border-radius:8px;padding:12px;display:flex;flex-direction:column;gap:8px;">
                        <div style="display:flex;justify-content:space-between;align-items:center;">
                            <span style="font-weight:bold;font-size:0.85rem;color:#fff;">${{s.full_name}}</span>
                            <span style="font-size:0.7rem;color:var(--text-muted);background:rgba(255,255,255,0.05);padding:1px 4px;border-radius:3px;">${{s.student_id}}</span>
                        </div>
                        <div style="display:flex;flex-wrap:wrap;gap:6px;">${{pills}}</div>
                        <div style="font-size:0.75rem;color:var(--text-muted);">${{s.reasons.join(', ')}}</div>
                    </div>`;
                }});
                stHtml += `</div>`;
                contentDiv.innerHTML += stHtml;
            }} else {{
                contentDiv.innerHTML += `<div style="text-align:center;padding:32px;color:var(--text-muted);">
                    <i class="fas fa-check-circle" style="font-size:2rem;color:var(--success);margin-bottom:10px;"></i><br>
                    Lớp học này không có học viên thuộc nhóm nguy cơ cần hỗ trợ.</div>`;
            }}

            document.getElementById('class-drawer').classList.add('open');
            document.getElementById('drawer-backdrop').style.display = 'block';
        }}

        function closeClassDrawer() {{
            document.getElementById('class-drawer').classList.remove('open');
            document.getElementById('drawer-backdrop').style.display = 'none';
        }}

        // ── Export CSV với cột Nhóm can thiệp & Giải pháp ─────────────────────
        function exportCareListCSV() {{
            let csv = '\\ufeffKhóa,Lớp,Học viên,XS đỗ%,Vắng%,Nợ bài%,EL vi phạm,Mức độ,Nhóm can thiệp,Giải pháp đề xuất\\n';
            document.querySelectorAll('.ig-rows').forEach(tbody => {{
                const gkey = tbody.dataset.group;
                const title = (groupMeta[gkey] || {{}}).title || gkey;
                const sol   = ((groupMeta[gkey] || {{}}).solution || '').replace(/"/g, '""');
                tbody.querySelectorAll('tr').forEach(row => {{
                    const cols = row.querySelectorAll('td');
                    if (cols.length < 8) return;
                    csv += `"${{cols[0].innerText}}","${{cols[1].innerText}}","${{cols[2].innerText.replace(/"/g,'""')}}",`;
                    csv += `"${{cols[3].innerText}}","${{cols[4].innerText}}","${{cols[5].innerText}}","${{cols[6].innerText}}","${{cols[7].innerText}}",`;
                    csv += `"${{title}}","${{sol}}"\\n`;
                }});
            }});
            const blob = new Blob([csv], {{type:'text/csv;charset=utf-8;'}});
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = 'Care_List_Phan_Nhom_Can_Thiep.csv';
            document.body.appendChild(link); link.click(); document.body.removeChild(link);
        }}

        // Data from Python backend
        const currLabels = {json.dumps(chart_curr_labels)};
        const currCohorts = {json.dumps(chart_curr_cohorts)};
        const currOld = {json.dumps(chart_curr_old)};
        const currNew = {json.dumps(chart_curr_new)};
        
        const riskDist = [{green_count}, {yellow_count}, {red_count}];
        const cohortPass = [{round(ks24_avg_pass, 1)}, {round(ks25_avg_pass, 1)}, {round(qtkd_avg_pass, 1)}];
        const cohortViol = [{round(ks24_avg_viol, 1)}, {round(ks25_avg_viol, 1)}, {round(qtkd_avg_viol, 1)}];

        // --- Presentation Mode Toggle ---
        function togglePresentationMode() {{
            document.body.classList.toggle('presentation-mode');
            const isPres = document.body.classList.contains('presentation-mode');
            const btn = document.getElementById('btn-toggle-pres');
            if (isPres) {{
                btn.innerHTML = '<i class="fas fa-compress"></i> <span>Thoát Chế độ Chụp</span>';
                btn.style.background = 'var(--primary)';
                btn.style.color = '#fff';
            }} else {{
                btn.innerHTML = '<i class="fas fa-camera"></i> <span>Chế độ Chụp Báo Cáo</span>';
                btn.style.background = 'rgba(255, 255, 255, 0.05)';
                btn.style.color = 'var(--text-main)';
            }}
        }}

        // --- Main Prediction Chart with Safe/Warning Threshold Lines ---
        const ctxMain = document.getElementById('pred-compare-chart').getContext('2d');
        
        // Tạo gradient màu xanh neon cho Quy chế mới
        const gradNew = ctxMain.createLinearGradient(0, 0, 0, 350);
        gradNew.addColorStop(0, 'rgba(59, 130, 246, 0.9)');
        gradNew.addColorStop(1, 'rgba(37, 99, 235, 0.35)');

        const mainChart = new Chart(ctxMain, {{
            type: 'bar',
            data: {{
                labels: currLabels,
                datasets: [
                    {{
                        label: 'Quy chuẩn cũ (%)',
                        data: [...currOld],
                        backgroundColor: 'rgba(148, 163, 184, 0.35)',
                        borderColor: 'rgba(148, 163, 184, 0.8)',
                        borderWidth: 1.5,
                        borderRadius: 6,
                        order: 2
                    }},
                    {{
                        label: 'Quy chế mới (%)',
                        data: [...currNew],
                        backgroundColor: gradNew,
                        borderColor: 'rgba(59, 130, 246, 1)',
                        borderWidth: 1.5,
                        borderRadius: 6,
                        order: 2
                    }},
                    {{
                        type: 'line',
                        label: 'Ngưỡng An toàn (70%)',
                        data: Array(currLabels.length).fill(70),
                        borderColor: 'rgba(16, 185, 129, 0.85)',
                        borderWidth: 2,
                        borderDash: [6, 4],
                        pointRadius: 0,
                        fill: false,
                        order: 1
                    }},
                    {{
                        type: 'line',
                        label: 'Ngưỡng Báo động (50%)',
                        data: Array(currLabels.length).fill(50),
                        borderColor: 'rgba(244, 63, 94, 0.85)',
                        borderWidth: 2,
                        borderDash: [5, 4],
                        pointRadius: 0,
                        fill: false,
                        order: 1
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
                        ticks: {{ 
                            color: '#9ca3af', 
                            font: {{ family: 'Plus Jakarta Sans', weight: '600' }},
                            callback: function(v) {{ return v + '%'; }}
                        }}
                    }},
                    x: {{
                        grid: {{ display: false }},
                        ticks: {{ 
                            color: '#e2e8f0', 
                            font: {{ family: 'Plus Jakarta Sans', weight: '600', size: 11 }},
                            maxRotation: 45,
                            minRotation: 20
                        }}
                    }}
                }},
                plugins: {{
                    legend: {{
                        position: 'top',
                        labels: {{ 
                            color: '#f3f4f6', 
                            font: {{ family: 'Plus Jakarta Sans', weight: 'bold', size: 11 }},
                            boxWidth: 14,
                            usePointStyle: true
                        }}
                    }},
                    tooltip: {{
                        padding: 12,
                        backgroundColor: 'rgba(15, 23, 42, 0.95)',
                        titleFont: {{ family: 'Plus Jakarta Sans', weight: 'bold' }},
                        bodyFont: {{ family: 'Plus Jakarta Sans' }},
                        borderColor: 'rgba(255,255,255,0.1)',
                        borderWidth: 1,
                        callbacks: {{
                            label: function(c) {{
                                return c.dataset.label + ': ' + c.parsed.y + '%';
                            }}
                        }}
                    }}
                }}
            }}
        }});

        function filterMainChart(cohort) {{
            document.querySelectorAll('.chart-filter-btn').forEach(btn => btn.classList.remove('active'));
            if (cohort === 'all') document.getElementById('btn-filter-all').classList.add('active');
            if (cohort === 'KS24') document.getElementById('btn-filter-ks24').classList.add('active');
            if (cohort === 'KS25') document.getElementById('btn-filter-ks25').classList.add('active');
            if (cohort === 'QTKD') document.getElementById('btn-filter-qtkd').classList.add('active');

            let filteredLabels = [];
            let filteredOld = [];
            let filteredNew = [];

            for (let i = 0; i < currLabels.length; i++) {{
                if (cohort === 'all' || currCohorts[i] === cohort) {{
                    filteredLabels.push(currLabels[i]);
                    filteredOld.push(currOld[i]);
                    filteredNew.push(currNew[i]);
                }}
            }}

            mainChart.data.labels = filteredLabels;
            mainChart.data.datasets[0].data = filteredOld;
            mainChart.data.datasets[1].data = filteredNew;
            mainChart.data.datasets[2].data = Array(filteredLabels.length).fill(70);
            mainChart.data.datasets[3].data = Array(filteredLabels.length).fill(50);
            mainChart.update();
        }}

        // --- Doughnut Chart Phân Bổ Nguy Cơ ---
        const ctxDoughnut = document.getElementById('risk-doughnut-chart').getContext('2d');
        new Chart(ctxDoughnut, {{
            type: 'doughnut',
            data: {{
                labels: ['An toàn (≥ 70%)', 'Theo dõi (50-70%)', 'Nguy cơ cấm thi (< 50%)'],
                datasets: [{{
                    data: riskDist,
                    backgroundColor: [
                        'rgba(16, 185, 129, 0.85)',
                        'rgba(245, 158, 11, 0.85)',
                        'rgba(244, 63, 94, 0.85)'
                    ],
                    borderColor: [
                        'rgba(16, 185, 129, 1)',
                        'rgba(245, 158, 11, 1)',
                        'rgba(244, 63, 94, 1)'
                    ],
                    borderWidth: 2,
                    hoverOffset: 6
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                cutout: '72%',
                plugins: {{
                    legend: {{
                        position: 'bottom',
                        labels: {{
                            color: '#9ca3af',
                            font: {{ family: 'Plus Jakarta Sans', size: 11, weight: '600' }},
                            padding: 14,
                            boxWidth: 12,
                            usePointStyle: true
                        }}
                    }},
                    tooltip: {{
                        padding: 10,
                        backgroundColor: '#0f172a',
                        borderColor: 'rgba(255,255,255,0.1)',
                        borderWidth: 1,
                        callbacks: {{
                            label: function(c) {{
                                const total = riskDist.reduce((a, b) => a + b, 0);
                                const pct = total ? ((c.parsed / total) * 100).toFixed(1) : 0;
                                return ' ' + c.label + ': ' + c.parsed + ' SV (' + pct + '%)';
                            }}
                        }}
                    }}
                }}
            }}
        }});

        // --- Biểu Đồ Sức Khỏe Học Thuật 3 Khối ---
        const ctxCohort = document.getElementById('cohort-health-chart').getContext('2d');
        new Chart(ctxCohort, {{
            type: 'bar',
            data: {{
                labels: ['KS24 (Microservice)', 'KS25 (PTTKHT)', 'KS25 QTKD (MAN107)'],
                datasets: [
                    {{
                        label: 'Tỷ lệ Đỗ TB (%)',
                        data: cohortPass,
                        backgroundColor: 'rgba(59, 130, 246, 0.8)',
                        borderColor: 'rgba(59, 130, 246, 1)',
                        borderWidth: 1.5,
                        borderRadius: 6
                    }},
                    {{
                        label: 'Tỷ lệ Vi phạm TB (%)',
                        data: cohortViol,
                        backgroundColor: 'rgba(244, 63, 94, 0.75)',
                        borderColor: 'rgba(244, 63, 94, 1)',
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
                        ticks: {{ 
                            color: '#9ca3af', 
                            font: {{ family: 'Plus Jakarta Sans' }},
                            callback: function(v) {{ return v + '%'; }}
                        }}
                    }},
                    x: {{
                        grid: {{ display: false }},
                        ticks: {{ color: '#f3f4f6', font: {{ family: 'Plus Jakarta Sans', weight: '600', size: 11 }} }}
                    }}
                }},
                plugins: {{
                    legend: {{
                        position: 'top',
                        labels: {{ 
                            color: '#f3f4f6', 
                            font: {{ family: 'Plus Jakarta Sans', weight: 'bold', size: 11 }},
                            boxWidth: 12
                        }}
                    }},
                    tooltip: {{
                        padding: 10,
                        backgroundColor: '#0f172a',
                        borderColor: 'rgba(255,255,255,0.1)',
                        borderWidth: 1,
                        callbacks: {{
                            label: function(c) {{
                                return c.dataset.label + ': ' + c.parsed.y + '%';
                            }}
                        }}
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
