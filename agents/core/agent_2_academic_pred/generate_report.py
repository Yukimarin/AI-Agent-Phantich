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

            <!-- Action Role Cards -->
            <h2 style="margin: 32px 0 16px; font-size: 1.1rem; font-weight: 800; text-transform: uppercase; color: var(--text-muted); letter-spacing: 0.5px;">🎯 Kế hoạch Can thiệp Tuần này</h2>
            <div class="action-roles-grid">
                {gv_card_html}
                {gvcn_card_html}
                {pmo_card_html}
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
                                <th class="text-center">Ưu tiên</th>
                                <th class="text-center">Tác nghiệp</th>
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
                                <th class="text-center">Ưu tiên</th>
                                <th class="text-center">Tác nghiệp</th>
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
                                <th class="text-center">Ưu tiên</th>
                                <th class="text-center">Tác nghiệp</th>
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

        <!-- TAB 3: CARE LIST — PHÂN NHÓM CAN THIỆP -->
        <div id="tab-care-list" class="tab-content">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                <div>
                    <h2 style="font-size: 1.1rem; font-weight: 800;">Danh sách học viên cần can thiệp toàn khóa</h2>
                    <p style="font-size: 0.8rem; color: var(--text-muted); margin-top: 4px;">Phân loại theo nhóm vấn đề — nhấn vào từng nhóm để xem chi tiết và giải pháp đề xuất</p>
                </div>
                <button onclick="exportCareListCSV()" class="btn-risk" style="background: var(--primary-light); color: var(--primary); padding: 10px 18px; font-size: 0.82rem;">
                    <i class="fas fa-file-csv"></i> Xuất CSV
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
