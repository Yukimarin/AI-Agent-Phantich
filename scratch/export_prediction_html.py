import os
import sys
import re
import requests
import markdown
import json

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

md_path = 'data/three_recent_courses_report.md'
html_dir = 'output'
html_path = os.path.join(html_dir, 'three_recent_courses_report.html')

if not os.path.exists(html_dir):
    os.makedirs(html_dir)

# Doc file markdown
if not os.path.exists(md_path):
    print(f"Error: File {md_path} not found.")
    sys.exit(1)

with open(md_path, 'r', encoding='utf-8') as f:
    md_content = f.read()

# Chuan hoa dong moi
md_content = md_content.replace('\r\n', '\n')

def normalize_class_name(name):
    if not name:
        return ""
    name_str = str(name).strip().upper()
    if '(' in name_str:
        name_str = name_str.split('(')[0].strip()
    name_str = name_str.replace('KS24', 'K24').replace('KS25', 'K25')
    name_str = name_str.lower()
    for word in ['hk2', 'hk1', 'hl', 'cu', 'retake', 'old']:
        name_str = name_str.replace(word, '')
    name_str = re.sub(r'[^a-z0-9]', '', name_str)
    return name_str

# Load student risk data from JSON
risk_data = {}
if os.path.exists('scratch/student_risk_data.json'):
    with open('scratch/student_risk_data.json', 'r', encoding='utf-8') as jf:
        risk_data = json.load(jf)

# -------------------------------------------------------------
# PARSE MARKDOWN TO EXTRACT KPI VALUES & TABLES FOR THE DASHBOARD
# -------------------------------------------------------------

p1_idx = md_content.find("📌 MỤC 1")
if p1_idx == -1: p1_idx = md_content.find("📌 MUC 1")
p2_idx = md_content.find("📌 MỤC 2")
if p2_idx == -1: p2_idx = md_content.find("📌 MUC 2")

if p1_idx != -1 and p2_idx != -1:
    sec_part1 = md_content[p1_idx:p2_idx]
    sec_part2 = md_content[p2_idx:]
else:
    sec_part1 = md_content
    sec_part2 = md_content

# Extract MAE values (Line-specific regex)
mae_values = {}
for key, batch_name in [('KS24', 'KS24-CNTT'), ('KS25', 'KS25-CNTT'), ('KS25_QTKD', 'KS25-QTKD')]:
    pattern = rf'\*\*Đánh giá chung khóa {batch_name} \(Lớp Chính Quy\)\*\*:\s*MAE\s*=\s*\*\*([\d.]+)%\*\*'
    match = re.search(pattern, sec_part1)
    if not match:
        pattern_alt = rf'\*\*Danh gia chung khoa {batch_name} \(Lop Chinh Quy\)\*\*:\s*MAE\s*=\s*\*\*([\d.]+)%\*\*'
        match = re.search(pattern_alt, sec_part1)
    
    if match:
        mae_values[key] = float(match.group(1))
    else:
        mae_values[key] = 0.0

# Parse table Muc 1
def parse_part1_table(section_text, batch_name):
    start_str = f"Khóa {batch_name}"
    if start_str not in section_text:
        start_str = f"Khoa {batch_name}"
    if start_str not in section_text:
        return []
        
    start_idx = section_text.find(start_str)
    end_str = f"Đánh giá chung khóa {batch_name} (Lớp Chính Quy)"
    end_idx = section_text.find(end_str, start_idx)
    if end_idx == -1:
        end_str_alt = f"Danh gia chung khoa {batch_name} (Lop Chinh Quy)"
        end_idx = section_text.find(end_str_alt, start_idx)
    if end_idx == -1:
        end_idx = len(section_text)
        
    sub_text = section_text[start_idx:end_idx]
    
    table_match = re.search(r'(\|.*?\n\|[-:| ]*\|\n(?:\|.*?\n)+)', sub_text)
    if not table_match:
        return []
        
    table_lines = table_match.group(1).strip().split('\n')[2:]
    results = []
    for line in table_lines:
        cells = [c.strip() for c in line.split('|')[1:-1]]
        if len(cells) >= 5:
            try:
                name = cells[0]
                teacher = cells[1]
                pred = float(cells[2].replace('**', '').replace('%', '').strip())
                act = float(cells[3].replace('**', '').replace('%', '').strip())
                err = cells[4]
                results.append({
                    'name': name,
                    'teacher': teacher,
                    'pred': pred,
                    'act': act,
                    'err': err
                })
            except Exception as ex:
                pass
    return results

# Parse table Muc 2
def parse_part2_table(section_text, batch_name):
    start_str = f"Khóa {batch_name}"
    if start_str not in section_text:
        start_str = f"Khoa {batch_name}"
    if start_str not in section_text:
        return []
        
    start_idx = section_text.find(start_str)
    end_str = f"Đánh giá chung khóa {batch_name}"
    end_idx = section_text.find(end_str, start_idx)
    if end_idx == -1:
        end_str_alt = f"Danh gia chung khoa {batch_name}"
        end_idx = section_text.find(end_str_alt, start_idx)
    if end_idx == -1:
        end_idx = len(section_text)
        
    sub_text = section_text[start_idx:end_idx]
    
    table_match = re.search(r'(\|.*?\n\|[-:| ]*\|\n(?:\|.*?\n)+)', sub_text)
    if not table_match:
        return []
        
    table_lines = table_match.group(1).strip().split('\n')[2:]
    results = []
    for line in table_lines:
        cells = [c.strip() for c in line.split('|')[1:-1]]
        if len(cells) >= 9:
            try:
                results.append({
                    'name': cells[0],
                    'teacher': cells[1],
                    'prev_course': cells[2],
                    'prev_act': cells[3],
                    'curr_course': cells[4],
                    'hack': cells[5],
                    'pred': float(cells[6].replace('**', '').replace('%', '').strip()),
                    'act': cells[7],
                    'err': cells[8]
                })
            except Exception as ex:
                pass
    return results

# Lay danh gia chung Muc 2 tu Markdown
def get_part2_evaluation(section_text, batch_name):
    start_str = f"Khóa {batch_name}"
    if start_str not in section_text:
        start_str = f"Khoa {batch_name}"
    if start_str not in section_text:
        return ""
        
    start_idx = section_text.find(start_str)
    
    pattern = rf'(👉 \*\*Đánh giá chung khóa {batch_name}\*\*.*?\n(?:.*?\n)*?)(?=\n###|\n---|\Z)'
    match = re.search(pattern, section_text[start_idx:])
    if not match:
        pattern_alt = rf'(👉 \*\*Danh gia chung khoa {batch_name}\*\*.*?\n(?:.*?\n)*?)(?=\n###|\n---|\Z)'
        match = re.search(pattern_alt, section_text[start_idx:])
        
    if match:
        content = match.group(1).strip()
        content = content.replace("👉", "💡")
        return markdown.markdown(content)
    return ""

# Parse data
data_p1 = {
    'KS24': parse_part1_table(sec_part1, 'KS24-CNTT'),
    'KS25': parse_part1_table(sec_part1, 'KS25-CNTT'),
    'KS25_QTKD': parse_part1_table(sec_part1, 'KS25-QTKD')
}

data_p2 = {
    'KS24': parse_part2_table(sec_part2, 'KS24-CNTT'),
    'KS25': parse_part2_table(sec_part2, 'KS25-CNTT'),
    'KS25_QTKD': parse_part2_table(sec_part2, 'KS25-QTKD')
}

# -------------------------------------------------------------
# BUILD HTML DASHBOARD BODY
# -------------------------------------------------------------

html_content = ""

# 1. Executive KPI Cards
html_content += """
<div class="kpi-grid">
"""

for key, label in [('KS24', 'Kh\u00f3a KS24-CNTT'), ('KS25', 'Kh\u00f3a KS25-CNTT'), ('KS25_QTKD', 'Kh\u00f3a KS25-QTKD')]:
    mae = mae_values.get(key, 0.0)
    badge_class = "badge-green" if mae <= 10.0 else ("badge-yellow" if mae <= 15.0 else "badge-red")
    status_text = "\u0110\u1ea0T M\u1ee4C TI\u00caU" if mae <= 10.0 else ("C\u1ea6N THEO D\u00d5I" if mae <= 15.0 else "V\u01af\u1ee2T NG\u01af\u1ee0NG")
    
    html_content += f"""
    <div class="kpi-card">
        <div class="kpi-title">{label}</div>
        <div class="kpi-value">{mae:.2f}%</div>
        <div class="kpi-footer">
            <span class="badge {badge_class}">{status_text}</span>
            <span class="kpi-desc">Sai s\u1ed1 MAE trung b\u00ecnh</span>
        </div>
    </div>
    """
html_content += "</div>"

# Helper for rendering Progress Bar
def render_progress_bar(pred_val, act_val_str):
    try:
        act_val = float(act_val_str.replace('%', ''))
        has_act = True
    except:
        act_val = 0.0
        has_act = False
        
    act_bar_html = ""
    if has_act:
        act_bar_html = f"""
        <div class="progress-wrapper">
            <div class="progress-label">Th\u1ef1c t\u1ebf: {act_val:.1f}%</div>
            <div class="progress-bg progress-bg-act">
                <div class="progress-fill progress-fill-act" style="width: {act_val}%"></div>
            </div>
        </div>
        """
    else:
        act_bar_html = f"""
        <div class="progress-wrapper">
            <div class="progress-label">Th\u1ef1c t\u1ebf: <span class="text-gray">{act_val_str}</span></div>
            <div class="progress-bg progress-bg-act">
                <div class="progress-fill progress-fill-none" style="width: 0%"></div>
            </div>
        </div>
        """
        
    return f"""
    <div class="bars-container">
        <div class="progress-wrapper">
            <div class="progress-label">D\u1ef1 b\u00e1o: {pred_val:.1f}%</div>
            <div class="progress-bg progress-bg-pred">
                <div class="progress-fill progress-fill-pred" style="width: {pred_val}%"></div>
            </div>
        </div>
        {act_bar_html}
    </div>
    """

# Helper for rendering Error Badge
def render_error_badge(err_str):
    if err_str == "N/A" or not err_str:
        return '<span class="err-badge err-badge-gray">N/A</span>'
    try:
        err_val = float(err_str.replace('+', '').replace('%', '').strip())
        abs_err = abs(err_val)
    except:
        return f'<span class="err-badge err-badge-gray">{err_str}</span>'
        
    badge_class = "err-badge-green" if abs_err <= 10.0 else "err-badge-red"
    return f'<span class="err-badge {badge_class}">{err_str}</span>'

# 2. Section 1 Tables
html_content += """
<div class="section-title">\U0001f4cc M\u1ee4C 1: \u0110O SAI S\u1ed0 D\u1ef0 B\u00c1O TRUNG B\u00ccNH 3 M\u00d4N G\u1ea6N NH\u1ea5T</div>
<p class="section-subtitle">\u0110o l\u01b0\u1eddng \u0111\u1ed9 l\u1ecch trung b\u00ecnh gi\u1eefa t\u1ef7 l\u1ec7 qua m\u00f4n d\u1ef1 b\u00e1o c\u1ee7a m\u00f4 h\u00ecnh v\u00e0 t\u1ef7 l\u1ec7 qua m\u00f4n th\u1ef1c t\u1ebf c\u1ee7a c\u00e1c l\u1edbp h\u1ecdc ch\u00ednh quy.</p>
"""

for key, label in [('KS24', 'Kh\u00f3a KS24-CNTT'), ('KS25', 'Kh\u00f3a KS25-CNTT'), ('KS25_QTKD', 'Kh\u00f3a KS25-QTKD')]:
    rows = data_p1.get(key, [])
    if not rows:
        html_content += f"""
        <div class="table-card">
            <div class="table-card-header">{label}</div>
            <div style="padding: 20px; text-align: center; color: #94a3b8;">Kh\u00f4ng t\u00ecm th\u1ea5y d\u1eef li\u1ec7u cho kh\u00f3a n\u00e0y.</div>
        </div>
        """
        continue
    
    html_content += f"""
    <div class="table-card">
        <div class="table-card-header">{label}</div>
        <div class="table-responsive">
            <table>
                <thead>
                    <tr>
                        <th style="width: 30%">L\u1edbp &amp; Gi\u1ea3ng vi\u00ean</th>
                        <th style="width: 55%">So s\u00e1nh t\u1ef7 l\u1ec7 \u0111\u1ed7 (D\u1ef1 b\u00e1o vs Th\u1ef1c t\u1ebf)</th>
                        <th style="width: 15%; text-align: center">Sai l\u1ecch</th>
                    </tr>
                </thead>
                <tbody>
    """
    for r in rows:
        bars = render_progress_bar(r['pred'], f"{r['act']}%")
        err_badge = render_error_badge(r['err'])
        html_content += f"""
                    <tr>
                        <td>
                            <div class="class-name">{r['name']}</div>
                            <div class="teacher-name">{r['teacher']}</div>
                        </td>
                        <td>{bars}</td>
                        <td style="text-align: center">{err_badge}</td>
                    </tr>
        """
    html_content += """
                </tbody>
            </table>
        </div>
    </div>
    """

# 3. Section 2 Tables
html_content += """
<div class="section-title" style="margin-top: 48px;">\U0001f4cc M\u1ee4C 2: D\u1ef0 B\u00c1O QUA M\u00d4N HI\u1ec6N T\u1ea0I D\u1ef0A TR\u00caN K\u1ebeT QU\u1ea2 M\u00d4N TR\u01af\u1edaC (G\u1ea6N NH\u1ea5T)</div>
<p class="section-subtitle">L\u1ea5y k\u1ebft qu\u1ea3 th\u1ef1c t\u1ebf m\u00f4n tru\u1edbc l\u00e0m \u0111\u1ea7u v\u00e0o \u0111\u1ec3 d\u1ef1 \u0111o\u00e1n t\u1ef7 l\u1ec7 qua m\u00f4n \u1edf m\u00f4n hi\u1ec7n t\u1ea1i. N\u1ebfu m\u00f4n hi\u1ec7n t\u1ea1i ch\u01b0a thi xong, k\u1ebft qu\u1ea3 th\u1ef1c t\u1ebf hi\u1ec3n th\u1ecb tr\u1ea1ng th\u00e1i "Ch\u01b0a k\u1ebft th\u00fac".</p>
"""

for key, label in [('KS24', 'Kh\u00f3a KS24-CNTT'), ('KS25', 'Kh\u00f3a KS25-CNTT'), ('KS25_QTKD', 'Kh\u00f3a KS25-QTKD')]:
    rows = data_p2.get(key, [])
    eval_text = get_part2_evaluation(sec_part2, label.replace('Kh\u00f3a ', ''))
    
    if not rows:
        html_content += f"""
        <div class="table-card">
            <div class="table-card-header">{label}</div>
            <div style="padding: 20px; text-align: center; color: #94a3b8;">Kh\u00f4ng t\u00ecm th\u1ea5y d\u1eef li\u1ec7u d\u1ef1 b\u00e1o m\u00f4n hi\u1ec7n t\u1ea1i.</div>
        </div>
        """
        continue
    
    html_content += f"""
    <div class="table-card">
        <div class="table-card-header">{label}</div>
        <div class="table-responsive">
            <table>
                <thead>
                    <tr>
                        <th style="width: 25%">L\u1edbp &amp; GV Hi\u1ec7n t\u1ea1i</th>
                        <th style="width: 25%">M\u00f4n h\u1ecdc &amp; \u0110i\u1ec3m tr\u01b0\u1edbc</th>
                        <th style="width: 35%">T\u1ef7 l\u1ec7 \u0111\u1ed7 M\u00f4n hi\u1ec7n t\u1ea1i</th>
                        <th style="width: 15%; text-align: center">Sai s\u1ed1</th>
                    </tr>
                </thead>
                <tbody>
    """
    for r in rows:
        bars = render_progress_bar(r['pred'], r['act'])
        err_badge = render_error_badge(r['err'])
        
        # Check matching student risk data
        matched_class_key = None
        r_norm = normalize_class_name(r['name'])
        for k in risk_data.keys():
            if normalize_class_name(k) == r_norm:
                matched_class_key = k
                break
                
        risk_row_html = ""
        if matched_class_key:
            risk_info = risk_data[matched_class_key]
            risk_count = risk_info['risk_count']
            risk_st_list = risk_info['risk_students']
            
            if risk_count > 0:
                rows_st_html = ""
                for s in risk_st_list:
                    att_warning = 'class="risk-val-red"' if s['att'] > 20 else ""
                    hw_warning = 'class="risk-val-red"' if s['hw'] < 80 else ""
                    el_warning = 'class="risk-val-red"' if s['el'] > 3 else ""
                    rp_warning = 'class="risk-val-red"' if s['rp'] < 80 else ""
                    p_warning = 'class="risk-val-red"' if s['p_eligible'] < 50 else ""
                    
                    rows_st_html += f"""
                    <tr>
                        <td style="font-weight: 600; color: var(--text-dark);">{s['code']}</td>
                        <td style="font-weight: 500;">{s['name']}</td>
                        <td style="text-align: center;"><span {att_warning}>{s['att']:.1f}%</span></td>
                        <td style="text-align: center;"><span {hw_warning}>{s['hw']:.1f}%</span></td>
                        <td style="text-align: center;"><span {el_warning}>{s['el']:.0f}</span></td>
                        <td style="text-align: center;"><span {rp_warning}>{s['rp']:.1f}</span></td>
                        <td style="text-align: center;"><span {p_warning}>{s['p_eligible']:.1f}%</span></td>
                        <td class="reason-cell">{s['reasons']}</td>
                    </tr>
                    """
                
                risk_row_html = f"""
                <tr class="risk-details-row">
                    <td colspan="4">
                        <details class="risk-details">
                            <summary class="risk-summary">
                                <span>\u26a0\ufe0f Xem danh s\u00e1ch sinh vi\u00ean c\u00f3 nguy c\u01a1 tr\u01b0\u1ee3t ({risk_count} SV)</span>
                            </summary>
                            <div class="risk-content">
                                <table class="nested-risk-table">
                                    <thead>
                                        <tr>
                                            <th>M\u00e3 SV</th>
                                            <th>H\u1ecd t\u00ean</th>
                                            <th style="text-align: center;">Chuy\u00ean c\u1ea7n (v\u1eafng)</th>
                                            <th style="text-align: center;">B\u00e0i t\u1eadp</th>
                                            <th style="text-align: center;">Elearning (l\u1ed7i)</th>
                                            <th style="text-align: center;">Rpoint</th>
                                            <th style="text-align: center;">\u0110i\u1ec3m d\u1ef1 b\u00e1o</th>
                                            <th>L\u00fd do chi ti\u1ebft</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {rows_st_html}
                                    </tbody>
                                </table>
                            </div>
                        </details>
                    </td>
                </tr>
                """
            else:
                risk_row_html = f"""
                <tr class="risk-details-row">
                    <td colspan="4">
                        <div class="risk-details-empty">
                            <span>\ud83c\udf89 L\u1edbp kh\u00f4ng c\u00f3 sinh vi\u00ean n\u00e0o c\u00f3 nguy c\u01a1 tr\u01b0\u1ee3t m\u00f4n</span>
                        </div>
                    </td>
                </tr>
                """
        
        html_content += f"""
                    <tr>
                        <td>
                            <div class="class-name">{r['name']}</div>
                            <div class="teacher-name">GV: {r['teacher']}</div>
                        </td>
                        <td>
                            <div class="course-badge prev-course-badge">Tr\u01b0\u1edbc: {r['prev_course']}</div>
                            <div class="course-detail">Th\u1ef1c t\u1ebf tr\u01b0\u1edbc: <strong>{r['prev_act']}</strong></div>
                            <div class="course-badge curr-course-badge">Hi\u1ec7n t\u1ea1i: {r['curr_course']}</div>
                            <div class="course-detail">Hackathon: <strong>{r['hack']}</strong></div>
                        </td>
                        <td>{bars}</td>
                        <td style="text-align: center">{err_badge}</td>
                    </tr>
                    {risk_row_html}
        """
    html_content += """
                </tbody>
            </table>
        </div>
    </div>
    """
    
    if eval_text:
        html_content += f"""
        <div class="eval-box">
            {eval_text}
        </div>
        """
        
    html_content += "</div>"

# Add explanations of formulas at the bottom
html_content += """
<div class="formula-card">
    <div class="formula-header">\u03b7 C\u00f4ng th\u1ee9c t\u00ednh ch\u1ec9 s\u1ed1 \u0111o l\u01b0\u1eddng</div>
    <div class="formula-body">
        <p><strong>1. Sai s\u1ed1 tuy\u1ec7t \u0111\u1ed1i trung b\u00ecnh (MAE - Mean Absolute Error):</strong></p>
        <div class="formula-math">MAE = (1/n) * &Sigma; |y_i - y_pred_i|</div>
        <p>Trong \u0111\u00f3: y_i la t\u1ef7 l\u1ec7 qua m\u00f4n th\u1ef1c t\u1ebf c\u1ee7a l\u1edbp, y_pred_i la t\u1ef7 l\u1ec7 qua m\u00f4n d\u1ef1 b\u00e1o c\u1ee7a l\u1edbp. MAE th\u1ec3 hi\u1ec7n m\u1ee9c \u0111\u1ed9 sai l\u1ec7ch trung b\u00ecnh ph\u1ea7n tr\u0103m. Ch\u1ec9 s\u1ed1 d\u01b0\u1edbi 10% th\u1ec3 hi\u1ec7n m\u00f4 h\u00ecnh c\u00f3 \u0111\u1ed9 tin c\u1eady r\u1ea5t cao.</p>
        
        <p style="margin-top: 16px;"><strong>2. Tiêu chí cảnh báo nguy cơ trượt môn cấp độ cá nhân (Mục 2):</strong></p>
        <ul>
            <li><strong>Chuyên cần:</strong> Vắng mặt trên 20% tổng số buổi học.</li>
            <li><strong>Bài tập:</strong> Tỉ lệ hoàn thành bài tập dưới 80% (nợ bài tập trên 20%).</li>
            <li><strong>Elearning:</strong> Số bài nộp muộn/lỗi vượt quá 3 bài.</li>
            <li><strong>Rpoint:</strong> Điểm Rpoint chốt tích lũy cá nhân dưới 80.0 điểm.</li>
            <li><strong>Học lực (Điểm dự báo):</strong> Kết quả GPA môn trước và thi thử Hackathon quy đổi dưới 5.0 (dưới 50%).</li>
            <li><strong>Project:</strong> Đối với các môn có chấm Project, không hoàn thành hoặc chấm dưới 5.0.</li>
        </ul>
    </div>
</div>
"""

# -------------------------------------------------------------
# COMPLETE HTML PAGE TEMPLATE (ELEGANT LINEAR STYLE WITH NESTED RISK TABLES)
# -------------------------------------------------------------

full_html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>B\u00e1o c\u00e1o Th\u1ed1ng k\u00ea &amp; D\u1ef1 b\u00e1o T\u1ef7 l\u1ec7 Qua m\u00f4n 3 M\u00f4n G\u1ea7n Nh\u1ea5t</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --primary: #7c3aed;
            --primary-light: #f5f3ff;
            --secondary: #3b82f6;
            --secondary-light: #eff6ff;
            --success: #10b981;
            --success-light: #d1fae5;
            --danger: #ef4444;
            --danger-light: #fef2f2;
            --text-main: #334155;
            --text-dark: #0f172a;
            --bg-main: #f8fafc;
            --border: #e2e8f0;
        }}
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg-main);
            color: var(--text-main);
            line-height: 1.6;
            padding: 40px 20px;
            max-width: 1200px;
            margin: 0 auto;
        }}
        .card {{
            background: white;
            padding: 40px;
            border-radius: 24px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.02);
            border: 1px solid var(--border);
        }}
        .header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding-bottom: 24px;
            margin-bottom: 32px;
            border-bottom: 1px solid var(--border);
        }}
        .logo-section {{
            display: flex;
            align-items: center;
            gap: 16px;
        }}
        .logo-box {{
            padding: 12px 16px;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            border-radius: 12px;
            color: white;
            font-weight: 800;
            font-size: 1.25rem;
            box-shadow: 0 4px 12px rgba(124, 58, 237, 0.15);
        }}
        .logo-title {{
            font-weight: 800;
            font-size: 1.25rem;
            color: var(--text-dark);
            line-height: 1.2;
        }}
        .logo-subtitle {{
            font-size: 0.7rem;
            color: #94a3b8;
            font-weight: 600;
            letter-spacing: 0.05em;
        }}
        .week-badge {{
            display: inline-block;
            padding: 6px 14px;
            background-color: var(--primary-light);
            color: var(--primary);
            border: 1px solid #ddd6fe;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
        }}
        
        /* KPI Cards Layout */
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        .kpi-card {{
            background: white;
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.01);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}
        .kpi-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.03);
        }}
        .kpi-title {{
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
            color: #64748b;
            letter-spacing: 0.05em;
            margin-bottom: 8px;
        }}
        .kpi-value {{
            font-size: 2.25rem;
            font-weight: 800;
            color: var(--text-dark);
            margin-bottom: 12px;
            background: linear-gradient(135deg, var(--text-dark), var(--primary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .kpi-footer {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-top: 1px solid var(--bg-main);
            padding-top: 12px;
        }}
        .badge {{
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.65rem;
            font-weight: 700;
            text-transform: uppercase;
        }}
        .badge-green {{
            background-color: var(--success-light);
            color: #065f46;
        }}
        .badge-yellow {{
            background-color: #fef3c7;
            color: #92400e;
        }}
        .badge-red {{
            background-color: var(--danger-light);
            color: #991b1b;
        }}
        .kpi-desc {{
            font-size: 0.75rem;
            color: #94a3b8;
        }}
        
        .section-title {{
            font-size: 1.25rem;
            font-weight: 700;
            color: var(--text-dark);
            margin-bottom: 6px;
            display: flex;
            align-items: center;
        }}
        .section-subtitle {{
            font-size: 0.85rem;
            color: #64748b;
            margin-bottom: 20px;
        }}
        
        /* Table Card Layout */
        .table-card {{
            background: white;
            border: 1px solid var(--border);
            border-radius: 16px;
            overflow: hidden;
            margin-bottom: 24px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.01);
        }}
        .table-card-header {{
            background-color: var(--bg-main);
            padding: 16px 20px;
            font-size: 0.9rem;
            font-weight: 700;
            color: var(--text-dark);
            border-bottom: 1px solid var(--border);
        }}
        .table-responsive {{
            overflow-x: auto;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            text-align: left;
        }}
        th {{
            background-color: white;
            color: #64748b;
            font-weight: 600;
            font-size: 0.7rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            padding: 14px 20px;
            border-bottom: 1px solid var(--border);
        }}
        td {{
            padding: 14px 20px;
            font-size: 0.9rem;
            border-bottom: 1px solid var(--border);
            background-color: white;
            vertical-align: middle;
        }}
        tr:hover td {{
            background-color: #fafbfe;
        }}
        
        /* Nested student risk tables inside Accordion details */
        .risk-details-row td {{
            padding: 0 !important;
            border: none !important;
        }}
        .risk-details-row:hover td {{
            background-color: transparent !important;
        }}
        .risk-details {{
            margin: 6px 20px 20px 20px;
            border: 1px dashed var(--border);
            border-radius: 12px;
            background-color: #f8fafc;
            overflow: hidden;
        }}
        .risk-details-empty {{
            margin: 6px 20px 20px 20px;
            border: 1px solid #d1fae5;
            border-radius: 12px;
            background-color: #f0fdf4;
            padding: 12px 20px;
            color: #166534;
            font-size: 0.8rem;
            font-weight: 600;
        }}
        .risk-summary {{
            padding: 12px 20px;
            font-size: 0.8rem;
            font-weight: 700;
            color: var(--primary);
            cursor: pointer;
            user-select: none;
            outline: none;
            background-color: #f3f0ff;
            border-radius: 11px;
            transition: background-color 0.2s ease;
        }}
        .risk-summary:hover {{
            background-color: #eadeff;
        }}
        .risk-content {{
            padding: 16px;
        }}
        .nested-risk-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.75rem;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid var(--border);
        }}
        .nested-risk-table th {{
            padding: 10px 14px;
            background-color: #f1f5f9;
            color: #475569;
            font-weight: 700;
            font-size: 0.75rem;
            border-bottom: 1px solid var(--border);
            text-transform: none;
        }}
        .nested-risk-table td {{
            padding: 10px 14px;
            border-bottom: 1px solid var(--border);
            font-size: 0.75rem;
            background-color: white;
        }}
        .nested-risk-table tr:last-child td {{
            border-bottom: none;
        }}
        .nested-risk-table tr:hover td {{
            background-color: #f8fafc;
        }}
        .risk-val-red {{
            color: var(--danger);
            font-weight: 700;
            background-color: var(--danger-light);
            padding: 2px 6px;
            border-radius: 4px;
        }}
        .reason-cell {{
            color: #e11d48;
            font-weight: 600;
        }}
        
        /* Column Elements */
        .class-name {{
            font-weight: 700;
            color: var(--text-dark);
            font-size: 0.95rem;
        }}
        .teacher-name {{
            font-size: 0.75rem;
            color: #94a3b8;
            margin-top: 2px;
            font-weight: 500;
        }}
        
        /* Progress Bars */
        .bars-container {{
            display: flex;
            flex-direction: column;
            gap: 6px;
        }}
        .progress-wrapper {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        .progress-label {{
            font-size: 0.75rem;
            font-weight: 600;
            color: #475569;
            width: 110px;
        }}
        .progress-bg {{
            flex: 1;
            height: 8px;
            background-color: #e2e8f0;
            border-radius: 4px;
            overflow: hidden;
            position: relative;
        }}
        .progress-bg-pred {{
            background-color: var(--primary-light);
        }}
        .progress-bg-act {{
            background-color: var(--secondary-light);
        }}
        .progress-fill {{
            height: 100%;
            border-radius: 4px;
        }}
        .progress-fill-pred {{
            background: linear-gradient(90deg, var(--primary), #a78bfa);
        }}
        .progress-fill-act {{
            background: linear-gradient(90deg, var(--success), #34d399);
        }}
        .progress-fill-none {{
            background-color: #cbd5e1;
        }}
        
        /* Badges */
        .err-badge {{
            display: inline-block;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 700;
        }}
        .err-badge-green {{
            background-color: var(--success-light);
            color: #065f46;
            border: 1px solid #a7f3d0;
        }}
        .err-badge-red {{
            background-color: var(--danger-light);
            color: #b91c1c;
            border: 1px solid #fecaca;
        }}
        .err-badge-gray {{
            background-color: #f1f5f9;
            color: #64748b;
            border: 1px solid var(--border);
        }}
        
        .course-badge {{
            display: inline-block;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 0.7rem;
            font-weight: 600;
            margin-bottom: 2px;
        }}
        .prev-course-badge {{
            background-color: #f1f5f9;
            color: #475569;
        }}
        .curr-course-badge {{
            background-color: var(--primary-light);
            color: var(--primary);
            margin-top: 4px;
        }}
        .course-detail {{
            font-size: 0.75rem;
            color: #64748b;
            padding-left: 6px;
            margin-bottom: 4px;
        }}
        
        .eval-box {{
            background-color: #f8fafc;
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 20px;
            margin-top: 16px;
            font-size: 0.85rem;
            color: #475569;
        }}
        .eval-box p {{
            margin: 0 0 10px 0;
        }}
        .eval-box p:last-child {{
            margin-bottom: 0;
        }}
        .eval-box ul {{
            margin: 6px 0 0 0;
            padding-left: 20px;
        }}
        .eval-box li {{
            margin-bottom: 6px;
        }}
        .eval-box li:last-child {{
            margin-bottom: 0;
        }}
        
        .formula-card {{
            background-color: white;
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 24px;
            margin-top: 40px;
        }}
        .formula-header {{
            font-size: 1rem;
            font-weight: 700;
            color: var(--text-dark);
            margin-bottom: 12px;
            border-bottom: 1px solid var(--bg-main);
            padding-bottom: 8px;
        }}
        .formula-body {{
            font-size: 0.85rem;
            color: #475569;
        }}
        .formula-math {{
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--text-dark);
            background-color: var(--bg-main);
            padding: 12px;
            border-radius: 8px;
            display: inline-block;
            margin: 10px 0;
            font-family: 'Courier New', Courier, monospace;
        }}
        .formula-body ul {{
            padding-left: 20px;
            margin-top: 8px;
        }}
        .formula-body li {{
            margin-bottom: 6px;
        }}
        .text-gray {{
            color: #94a3b8;
        }}
        
        .footer {{
            margin-top: 48px;
            padding-top: 32px;
            border-top: 1px solid var(--border);
            display: flex;
            align-items: center;
            justify-content: space-between;
            color: #94a3b8;
            font-size: 0.75rem;
            font-weight: 500;
        }}
        .status-badge {{
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        .status-dot {{
            width: 6px;
            height: 6px;
            background-color: #22c55e;
            border-radius: 50%;
        }}
    </style>
</head>
<body>
    <div class="card">
        <div class="header">
            <div class="logo-section">
                <div class="logo-box">DT</div>
                <div>
                    <div class="logo-title">Ph\u00e2n T\u00edch Ch\u1ec9 S\u1ed1 \u0110\u00e0o T\u1ea1o</div>
                    <div class="logo-subtitle">H\u1ec8 TH\u1ed0NG D\u1ef0 B\u00c1O T\u1ef2 L\u1ec6 QUA M\u00d4N &amp; \u0110O SAI S\u1ed0</div>
                </div>
            </div>
            <div>
                <span class="week-badge">Ch\u1ed1t d\u1eef li\u1ec7u: 3 M\u00f4n G\u1ea7n Nh\u1ea5t</span>
            </div>
        </div>
        
        {html_content}
        
        <div class="footer">
            <div>&copy; 2026 PTIT Center. T\u1ea5t c\u1ea3 c\u00e1c quy\u1ec1n \u0111\u01b0\u1ee3c b\u1ea3o l\u01b0u.</div>
            <div class="status-badge">
                <div class="status-dot"></div>
                <span>H\u1ec7 th\u1ed1ng v\u1eadn h\u00e0nh tr\u1ef1c tuy\u1ebfn</span>
            </div>
        </div>
    </div>
</body>
</html>
"""

# Ghi file HTML
with open(html_path, 'w', encoding='utf-8', errors='replace') as f:
    f.write(full_html)

print(f"File HTML da duoc tao thanh cong tai {html_path}")

# Upload lên Catbox
print("Dang tien hanh tai bao cao Du bao qua mon len Catbox.moe...")
try:
    with open(html_path, 'rb') as f:
        data = {'reqtype': 'fileupload'}
        files = {'fileToUpload': f}
        response = requests.post('https://catbox.moe/user/api.php', data=data, files=files)
        
    if response.status_code == 200:
        link = response.text.strip()
        if link.startswith('https://files.catbox.moe/'):
            print("\n==================================================")
            print("🎉 TAI LEN BAO CAO DU BAO PASS THANH CONG!")
            print(f"👉 Duong link xem truc tuyen: {link}")
            print("==================================================\n")
            
            # Cap nhat file shortcut Bao_Cao_2_Du_Bao_Pass.url
            shortcut_path = 'Bao_Cao_2_Du_Bao_Pass.url'
            url_content = f"[InternetShortcut]\nURL={link}\n"
            with open(shortcut_path, 'w', encoding='utf-8') as sf:
                sf.write(url_content)
            print(f"Da cap nhat file shortcut internet tai: {shortcut_path}")
        else:
            print(f"Loi phan hoi tu Catbox: {link}")
    else:
        print(f"Loi ket noi Catbox. Status code: {response.status_code}")
except Exception as e:
    print(f"Loi trong qua trinh upload Catbox: {e}")
