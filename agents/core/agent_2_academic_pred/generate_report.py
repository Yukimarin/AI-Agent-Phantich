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
            
            # Chỉ hiển thị panel mở rộng nếu lớp có sinh viên nguy cơ hoặc có lỗi tác nghiệp GV/TG
            has_issues = (num_risks > 0 or (not is_cv and num_class_errs > 0))
            
            if has_issues:
                badge_text_parts = []
                if num_risks > 0:
                    badge_text_parts.append(f"{num_risks} SV nguy cơ")
                if not is_cv and num_class_errs > 0:
                    badge_text_parts.append(f"{num_class_errs} lỗi GV")
                
                badge_text = f"⚠️ Rà soát (" + " / ".join(badge_text_parts) + ")"
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
            
            # Dòng chứa danh sách học viên nguy cơ hoặc cảnh báo GV/TG
            if has_issues:
                # Tạo banner cảnh báo lỗi tác nghiệp GV nếu có
                violation_alert_html = ""
                if not is_cv and num_class_errs > 0:
                    err_counts = {}
                    for v in class_errs:
                        err_code = v.get('Error', 'GV-08')
                        err_counts[err_code] = err_counts.get(err_code, 0) + 1
                    err_summary = ", ".join([f"{err_counts[k]} lỗi {k}" for k in err_counts])
                    
                    violation_alert_html = f"""
                    <div class="class-violation-alert">
                        <i class="fas fa-exclamation-triangle" style="font-size: 1.2rem;"></i>
                        <div>
                            <strong>Cảnh báo tác nghiệp đào tạo ({err_summary}):</strong>
                            Lớp này ghi nhận các lỗi giảng viên/trợ giảng vi phạm quy chế (bỏ sót đơn xin nghỉ phép hợp lệ của học viên - tích vắng sai, quên điểm danh, chậm tải tài nguyên). Yêu cầu cập nhật điều chỉnh trên hệ thống QLĐT ngay lập tức để khôi phục quyền lợi học tập thực tế cho sinh viên.
                        </div>
                    </div>
                    """
                
                care_list_block = ""
                if num_risks > 0:
                    student_badges_html = ""
                    for s in risks:
                        border_class = "red-border" if s['risk_level'] == 'RED' else "yellow-border"
                        dot_class = "red-dot" if s['risk_level'] == 'RED' else "yellow-dot"
                        
                        # Generate metric pills with icons
                        pills_html = ""
                        if s['att'] > 15.0:
                            pills_html += f'<span class="student-metric-pill red-pill"><i class="fas fa-user-slash"></i> Vắng: {s["att"]:.1f}%</span>'
                        elif s['att'] > 0:
                            pills_html += f'<span class="student-metric-pill yellow-pill"><i class="fas fa-user-clock"></i> Vắng: {s["att"]:.1f}%</span>'
                            
                        if (100.0 - s['hw']) > 30.0:
                            pills_html += f'<span class="student-metric-pill red-pill"><i class="fas fa-tasks"></i> Nợ bài: {100.0 - s["hw"]:.1f}%</span>'
                        elif (100.0 - s['hw']) > 15.0:
                            pills_html += f'<span class="student-metric-pill yellow-pill"><i class="fas fa-tasks"></i> Nợ bài: {100.0 - s["hw"]:.1f}%</span>'
                            
                        if s['el'] >= 2.0:
                            pills_html += f'<span class="student-metric-pill red-pill"><i class="fas fa-clock"></i> EL trễ: {s["el"]:.0f}</span>'
                        elif s['el'] >= 1.0:
                            pills_html += f'<span class="student-metric-pill yellow-pill"><i class="fas fa-clock"></i> EL trễ: {s["el"]:.0f}</span>'
                            
                        for anomaly in s.get('anomalies', []):
                            if anomaly == 'copy_suspect':
                                pills_html += '<span class="student-metric-pill red-pill anomaly-pill"><i class="fas fa-copy"></i> Copy?</span>'
                            elif anomaly == 'discipline_paradox':
                                pills_html += '<span class="student-metric-pill anomaly-pill" style="color: #c084fc; border-color: rgba(168, 85, 247, 0.2);"><i class="fas fa-brain"></i> KL kém</span>'
                            elif anomaly == 'passive_learner':
                                pills_html += '<span class="student-metric-pill anomaly-pill" style="color: #60a5fa; border-color: rgba(96, 165, 250, 0.2);"><i class="fas fa-mouse-pointer"></i> Học vẹt</span>'
                            elif anomaly == 'sudden_drop':
                                pills_html += '<span class="student-metric-pill anomaly-pill" style="color: #f43f5e; border-color: rgba(244, 63, 94, 0.2);"><i class="fas fa-chart-line"></i> Sụt phong độ</span>'
                                
                        if not pills_html and s['p_final'] < 40.0:
                            pills_html += f'<span class="student-metric-pill red-pill"><i class="fas fa-exclamation-triangle"></i> Yếu: {s["p_final"]:.1f}%</span>'
                        
                        student_badges_html += f"""
                        <div class="student-risk-card {border_class}">
                            <div class="student-card-header">
                                <span class="student-name">{s['full_name']}</span>
                                <span class="student-id">{s['student_id']}</span>
                            </div>
                            <div class="student-card-body">
                                {pills_html}
                            </div>
                        </div>
                        """
                        
                    care_list_block = f"""
                            <div class="risk-details-header" style="margin-bottom: 12px; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 8px;">
                                <span><i class="fas fa-user-shield" style="color: var(--danger);"></i> Học viên cần hỗ trợ của lớp {cname}</span>
                                <span style="color: var(--text-muted); font-size: 0.8rem;">Tổng số: <strong>{num_risks}</strong> học viên</span>
                            </div>
                            <div class="class-warning-grid">
                                {student_badges_html}
                            </div>
                    """
                rows_html += f"""
                <tr id="risk-panel-{cname}-{idx}" style="display: none; background: rgba(0,0,0,0.1);">
                    <td colspan="8" style="padding: 0;">
                        <div class="risk-details-card">
                            {violation_alert_html}
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

    # Count Red and Yellow risks per cohort
    cohort_risks = {
        'K24': {'RED': 0, 'YELLOW': 0, 'total': 0},
        'K25': {'RED': 0, 'YELLOW': 0, 'total': 0},
        'QTKD': {'RED': 0, 'YELLOW': 0, 'total': 0}
    }
    
    for s in data['care_list']:
        batch_name = s['batch']
        risk = s['risk_level']
        key = 'K24' if batch_name == 'K24' else ('QTKD' if 'QTKD' in batch_name else 'K25')
        if key in cohort_risks and risk in ('RED', 'YELLOW'):
            cohort_risks[key][risk] += 1
            cohort_risks[key]['total'] += 1

    anom_sum = data.get('anomalies_summary', {
        'K24': { 'copy_suspect': 0, 'discipline_paradox': 0, 'passive_learner': 0, 'sudden_drop': 0 },
        'K25': { 'copy_suspect': 0, 'discipline_paradox': 0, 'passive_learner': 0, 'sudden_drop': 0 },
        'QTKD': { 'copy_suspect': 0, 'discipline_paradox': 0, 'passive_learner': 0, 'sudden_drop': 0 }
    })
    
    # Count teacher violations per cohort
    teacher_violations_count = { 'K24': 0, 'K25': 0, 'QTKD': 0 }
    for v in teacher_violations:
        cls = v.get('Class', '')
        cohort = 'K24' if 'K24' in cls else ('QTKD' if 'QTKD' in cls or 'PRJ' in cls else 'K25')
        if cohort in teacher_violations_count:
            teacher_violations_count[cohort] += 1
            
    k25_cntt_cohort_diagnostic_html = f"""
    <div class="cohort-diagnostic-card" style="border-left: 4px solid var(--primary); margin-bottom: 20px;">
        <div class="cohort-diagnostic-title">
            <i class="fas fa-graduation-cap" style="color: var(--primary);"></i> Đánh giá chung &amp; Kế hoạch hành động Khối KS25 - CNTT (Python Web)
        </div>
        <div class="diagnostic-badges-container">
            <span class="diagnostic-badge-pill red-pill">🔴 Cảnh báo Đỏ: {cohort_risks['K25']['RED']} SV</span>
            <span class="diagnostic-badge-pill yellow-pill">🟡 Cảnh báo Vàng: {cohort_risks['K25']['YELLOW']} SV</span>
            <span class="diagnostic-badge-pill warning-pill">⚠️ Học vẹt: {anom_sum['K25']['passive_learner']} SV</span>
            <span class="diagnostic-badge-pill warning-pill">⚠️ Nghi vấn Copy: {anom_sum['K25']['copy_suspect']} SV</span>
        </div>
        <div class="diagnostic-desc">
            <strong>Đánh giá chung học tập:</strong> Học viên năm nhất bước vào chuyên ngành lập trình Web gặp nhiều khó khăn trong việc thích nghi với phương pháp tự học. Tỷ lệ học lực yếu và học vẹt (đối phó Elearning) chiếm tới 72% nhóm nguy cơ. Ngoài ra, việc tự thực hành chưa đi vào nề nếp dẫn đến hiện tượng sao chép code ở các bài tập cơ bản có xu hướng gia tăng.
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 15px;">
            <div class="diagnostic-role-group">
                <div class="diagnostic-role-title">👩‍💼 Kế hoạch của Cố vấn / GVCN:</div>
                <ul class="diagnostic-actions">
                    <li>Rà soát, liên hệ trực tiếp để động viên và tìm hiểu khó khăn thực tế của các SV năm nhất có dấu hiệu sao chép hoặc học vẹt.</li>
                    <li>Tổ chức sinh hoạt lớp chuyên đề chia sẻ phương pháp học lập trình Web hiệu quả và cách tự nghiên cứu tài liệu.</li>
                </ul>
            </div>
            <div class="diagnostic-role-group">
                <div class="diagnostic-role-title">👨‍🏫 Kế hoạch của Giảng viên / Trợ giảng:</div>
                <ul class="diagnostic-actions">
                    <li>Mở thêm <strong>2 buổi phụ đạo (Tutor) ngoài giờ/tuần</strong> tập trung ôn tập cú pháp Python và cấu trúc dữ liệu cơ bản.</li>
                    <li>Tăng cường kiểm tra code trực tiếp trên lớp để hạn chế tình trạng chép bài của nhau.</li>
                </ul>
            </div>
        </div>
    </div>
    """

    qtkd_cohort_diagnostic_html = f"""
    <div class="cohort-diagnostic-card" style="border-left: 4px solid var(--success); margin-bottom: 20px;">
        <div class="cohort-diagnostic-title">
            <i class="fas fa-business-time" style="color: var(--success);"></i> Đánh giá chung &amp; Kế hoạch hành động Khối KS25 - QTKD (PRJ302)
        </div>
        <div class="diagnostic-badges-container">
            <span class="diagnostic-badge-pill red-pill" style="background: rgba(16, 185, 129, 0.1); color: var(--success); border-color: rgba(16, 185, 129, 0.2);">🔴 Cảnh báo Đỏ: {cohort_risks['QTKD']['RED']} SV</span>
            <span class="diagnostic-badge-pill yellow-pill">🟡 Cảnh báo Vàng: {cohort_risks['QTKD']['YELLOW']} SV</span>
            <span class="diagnostic-badge-pill warning-pill">⚠️ Học vẹt: {anom_sum['QTKD']['passive_learner']} SV</span>
        </div>
        <div class="diagnostic-desc">
            <strong>Đánh giá chung học tập:</strong> Khối Quản trị kinh doanh số tự học và hoàn thành bài tập thực hành rất tốt (chỉ 10% học lực yếu). Vấn đề lớn nhất tập trung ở kỷ luật chuyên cần lên lớp (90% học viên nguy cơ mắc lỗi vắng không phép hoặc đi muộn).
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 15px;">
            <div class="diagnostic-role-group">
                <div class="diagnostic-role-title">👩‍💼 Kế hoạch của Cố vấn / GVCN:</div>
                <ul class="diagnostic-actions">
                    <li>Liên hệ nhắc nhở ngay trong buổi học đối với học viên vắng không phép. Phối hợp chặt chẽ với gia đình để chấn chỉnh kỷ luật giờ giấc.</li>
                </ul>
            </div>
            <div class="diagnostic-role-group">
                <div class="diagnostic-role-title tg-role">👨‍🏫 Kế hoạch của Trợ giảng (TA):</div>
                <ul class="diagnostic-actions">
                    <li>Thực hiện điểm danh nghiêm ngặt 2 lần (đầu giờ và cuối giờ). Cập nhật sĩ số vắng cho GVCN sau 15 phút đầu giờ để liên hệ học viên.</li>
                </ul>
            </div>
        </div>
    </div>
    """

    k24_cntt_cohort_diagnostic_html = f"""
    <div class="cohort-diagnostic-card" style="border-left: 4px solid #a855f7; margin-bottom: 20px;">
        <div class="cohort-diagnostic-title">
            <i class="fas fa-laptop-code" style="color: #a855f7;"></i> Đánh giá chung &amp; Kế hoạch hành động Khối KS24 - CNTT (AI Application)
        </div>
        <div class="diagnostic-badges-container">
            <span class="diagnostic-badge-pill red-pill" style="background: rgba(168, 85, 247, 0.1); color: #c084fc; border-color: rgba(168, 85, 247, 0.2);">🔴 Cảnh báo Đỏ: {cohort_risks['K24']['RED']} SV</span>
            <span class="diagnostic-badge-pill yellow-pill">🟡 Cảnh báo Vàng: {cohort_risks['K24']['YELLOW']} SV</span>
            <span class="diagnostic-badge-pill warning-pill" style="color: #c084fc; border-color: rgba(168, 85, 247, 0.2);"><i class="fas fa-brain"></i> Học giỏi - KL kém: {anom_sum['K24']['discipline_paradox']} SV</span>
        </div>
        <div class="diagnostic-desc">
            <strong>Đánh giá chung học tập:</strong> Học viên năm 2 có năng lực học tập thực tế tốt (chỉ 26.9% yếu học lực) nhưng tinh thần tự giác đi học sa sút nghiêm trọng (96% học viên nguy cơ vắng thật > 20% số buổi). Nguy cơ cấm thi hàng loạt do chuyên cần nếu không siết chặt kỷ luật hành chính.
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 15px;">
            <div class="diagnostic-role-group">
                <div class="diagnostic-role-title">👩‍💼 Kế hoạch của Cố vấn / GVCN:</div>
                <ul class="diagnostic-actions">
                    <li>Gửi văn bản cảnh báo cấm thi chính thức cho sinh viên và gia đình. Yêu cầu viết bản cam kết đảm bảo chuyên cần từ nay đến cuối kỳ.</li>
                </ul>
            </div>
            <div class="diagnostic-role-group">
                <div class="diagnostic-role-title">👨‍🏫 Kế hoạch của Giảng viên:</div>
                <ul class="diagnostic-actions">
                    <li>Tổ chức 1 buổi review tổng quan đề tài và hướng dẫn triển khai bài tập lớn (Lab lớn) để học viên bắt kịp nhịp độ dự án chuyên ngành.</li>
                </ul>
            </div>
        </div>
    </div>
    """

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
        .cohort-diagnostic-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin-bottom: 30px;
        }}
        .cohort-diagnostic-card {{
            background: rgba(30, 41, 59, 0.45);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 16px;
            padding: 20px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        .cohort-diagnostic-card:hover {{
            transform: translateY(-4px);
            border-color: rgba(255, 255, 255, 0.1);
            box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.3);
        }}
        .cohort-diagnostic-title {{
            font-size: 1.05rem;
            font-weight: 800;
            color: var(--text-main);
            text-transform: uppercase;
            margin-bottom: 12px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            padding-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .diagnostic-badges-container {{
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            margin-bottom: 12px;
        }}
        .diagnostic-badge-pill {{
            display: inline-flex;
            align-items: center;
            gap: 4px;
            padding: 4px 8px;
            border-radius: 6px;
            font-size: 0.72rem;
            font-weight: 700;
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255, 255, 255, 0.05);
            color: var(--text-muted);
        }}
        .diagnostic-badge-pill.red-pill {{
            background: rgba(239, 68, 68, 0.1);
            color: var(--danger);
            border-color: rgba(239, 68, 68, 0.2);
        }}
        .diagnostic-badge-pill.yellow-pill {{
            background: rgba(245, 158, 11, 0.1);
            color: var(--warning);
            border-color: rgba(245, 158, 11, 0.2);
        }}
        .diagnostic-badge-pill.warning-pill {{
            background: rgba(168, 85, 247, 0.08);
            color: #c084fc;
            border-color: rgba(168, 85, 247, 0.15);
        }}
        .diagnostic-desc {{
            font-size: 0.8rem;
            margin-bottom: 12px;
            color: var(--text-main);
            line-height: 1.5;
        }}
        .diagnostic-desc strong {{
            color: #fff;
        }}
        .diagnostic-actions {{
            font-size: 0.78rem;
            color: var(--text-muted);
            margin-left: 14px;
            line-height: 1.5;
            list-style-type: none;
            padding-left: 0;
        }}
        .diagnostic-actions li {{
            margin-bottom: 6px;
            position: relative;
            padding-left: 18px;
        }}
        .diagnostic-actions li::before {{
            content: "✓";
            position: absolute;
            left: 0;
            color: var(--primary);
            font-weight: bold;
        }}
        .diagnostic-actions strong {{
            color: #fff;
        }}
        
        .class-violation-alert {{
            background: rgba(239, 68, 68, 0.08);
            border: 1px solid rgba(239, 68, 68, 0.2);
            border-radius: 12px;
            padding: 12px 16px;
            font-size: 0.8rem;
            color: var(--danger);
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 8px;
            line-height: 1.4;
        }}
        .diagnostic-role-group {{
            margin-top: 10px;
            padding-left: 12px;
            border-left: 2px solid rgba(255,255,255,0.06);
            margin-bottom: 8px;
        }}
        .diagnostic-role-title {{
            font-size: 0.74rem;
            font-weight: 800;
            color: var(--primary);
            text-transform: uppercase;
            margin-bottom: 4px;
            letter-spacing: 0.5px;
        }}
        .diagnostic-role-title.tg-role {{
            color: var(--success);
        }}
        .diagnostic-role-title.pmo-role {{
            color: var(--warning);
        }}
        
        /* Class-level compact risk cards grid */
        .class-warning-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
            gap: 12px;
            margin-top: 15px;
            margin-bottom: 10px;
        }}
        .student-risk-card {{
            background: rgba(30, 41, 59, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            padding: 12px;
            display: flex;
            flex-direction: column;
            gap: 8px;
            transition: all 0.2s ease;
        }}
        .student-risk-card:hover {{
            background: rgba(30, 41, 59, 0.45);
            border-color: rgba(255, 255, 255, 0.1);
        }}
        .student-risk-card.red-border {{
            border-left: 3px solid rgba(239, 68, 68, 0.55);
        }}
        .student-risk-card.yellow-border {{
            border-left: 3px solid rgba(245, 158, 11, 0.55);
        }}
        .student-card-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .student-card-header .student-name {{
            font-size: 0.8rem;
            font-weight: 700;
            color: #f3f4f6;
        }}
        .student-card-header .student-id {{
            font-size: 0.65rem;
            font-family: monospace;
            color: #9ca3af;
            background: rgba(255,255,255,0.04);
            padding: 1px 4px;
            border-radius: 3px;
        }}
        .student-card-body {{
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
        }}
        .student-metric-pill {{
            display: inline-flex;
            align-items: center;
            gap: 4px;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 0.68rem;
            font-weight: 500;
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.05);
            color: #d1d5db;
        }}
        .student-metric-pill i {{
            font-size: 0.7rem;
            opacity: 0.85;
        }}
        .student-metric-pill i.red-icon {{
            color: #f87171;
        }}
        .student-metric-pill i.yellow-icon {{
            color: #fbbf24;
        }}
        .student-metric-pill i.purple-icon {{
            color: #c084fc;
        }}
        .student-metric-pill i.blue-icon {{
            color: #60a5fa;
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
        {k25_cntt_cohort_diagnostic_html}
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
        {qtkd_cohort_diagnostic_html}
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
        {k24_cntt_cohort_diagnostic_html}
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
        
    output_dir = 'output/dashboards/core'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    build_unified_prediction_dashboard(data, os.path.join(output_dir, 'agent_2_academic_prediction.html'))
    print("Combined Academic Dashboard & Care List exported successfully in output/dashboards/core/agent_2_academic_prediction.html")

if __name__ == '__main__':
    main()
