# Generator for QTKD Dashboard
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

def main():
    json_path = 'scratch/qtkd_data.json'
    if not os.path.exists(json_path):
        print('Error: scratch/qtkd_data.json not found')
        return
        
    with open(json_path, 'r', encoding='utf-8') as f:
        students = json.load(f)
        
    total_reg = len(students)
    active = [s for s in students if not s['is_absent']]
    total_took = len(active)
    total_pass = len([s for s in students if s['is_pass'] and not s['is_absent']])
    pass_pct = round(total_pass / total_reg * 100, 1)
    
    avg_qtkd = round(sum(s['final'] for s in active) / total_took, 1) if total_took else 0
    avg_knm = round(sum(s['knm_score'] for s in active) / total_took, 1) if total_took else 0
    ta_active = [s for s in active if s['ta_score'] > 0]
    avg_ta = round(sum(s['ta_score'] for s in ta_active) / len(ta_active), 1) if ta_active else 0
    
    classes = sorted(list(set(s['class'] for s in students)))
    class_stats = {}
    for c in classes:
        c_studs = [s for s in students if s['class'] == c]
        c_active = [s for s in c_studs if not s['is_absent']]
        c_pass = [s for s in c_studs if s['is_pass'] and not s['is_absent']]
        c_ta = [s for s in c_active if s['ta_score'] > 0]
        class_stats[c] = {
            'total': len(c_studs),
            'took': len(c_active),
            'pass': len(c_pass),
            'pass_pct': round(len(c_pass) / len(c_studs) * 100, 1),
            'avg_qtkd': round(sum(s['final'] for s in c_active) / len(c_active), 1) if c_active else 0,
            'avg_knm': round(sum(s['knm_score'] for s in c_active) / len(c_active), 1) if c_active else 0,
            'avg_ta': round(sum(s['ta_score'] for s in c_ta) / len(c_ta), 1) if c_ta else 0
        }
        
    groups = sorted(list(set(s['nhom'] for s in students if s['nhom'] != 'Chưa phân nhóm')), key=lambda x: int(x.replace('Nhóm ', '')) if 'Nhóm ' in x and x.replace('Nhóm ', '').isdigit() else 99)
    group_stats = {}
    for g in groups:
        g_studs = [s for s in students if s['nhom'] == g]
        g_active = [s for s in g_studs if not s['is_absent']]
        group_stats[g] = {
            'total': len(g_studs),
            'avg_qtkd': round(sum(s['final'] for s in g_active) / len(g_active), 1) if g_active else 0,
            'avg_knm': round(sum(s['knm_score'] for s in g_active) / len(g_active), 1) if g_active else 0,
            'students': [s['name'] for s in g_studs]
        }
        
    tier_counts = {
        'tier_3': len([s for s in students if s['tier'] == 3]),
        'tier_2': len([s for s in students if s['tier'] == 2]),
        'tier_1': len([s for s in students if s['tier'] == 1]),
        'tier_0': len([s for s in students if s['tier'] == 0]),
    }
    
    careers = {}
    for s in students:
        car = s['career']
        careers[car] = careers.get(car, 0) + 1

    students_json = json.dumps(students, ensure_ascii=False)
    
    tbody_rows = ''
    for s in students:
        tier_badge = '<span class="badge tier3">Mức 3</span>' if s['tier'] == 3 else ('<span class="badge tier2">Mức 2</span>' if s['tier'] == 2 else ('<span class="badge tier1">Mức 1</span>' if s['tier'] == 1 else '<span class="badge fail">Mức 0</span>'))
        qtkd_style = 'color:#34d399;font-weight:700;' if s['final'] >= 75 else ('color:#fbbf24;font-weight:700;' if s['final'] >= 60 else 'color:#f87171;font-weight:700;')
        ta_display = f"{s['ta_score']} / 990" if s['ta_score'] > 0 else '<span style="color:var(--text-muted)">Chưa có</span>'
        tbody_rows += f'''
        <tr>
            <td><strong>{s['name']}</strong></td>
            <td>{s['class']}</td>
            <td><span style="color:var(--color-primary);font-weight:600;">{s['nhom']}</span></td>
            <td style="{qtkd_style}">{s['final']}</td>
            <td style="color:#22d3ee;font-weight:600;">{s['knm_score']}</td>
            <td style="color:#60a5fa;font-weight:600;">{ta_display}</td>
            <td>{tier_badge}</td>
            <td><strong style="color:#fff;">{s['career']}</strong></td>
            <td style="font-size:0.78rem;color:var(--text-secondary);max-width:280px;">{s['career_note']}</td>
        </tr>
        '''
        
    class_table_rows = ''
    for c, stats in class_stats.items():
        class_table_rows += f'''
        <tr>
            <td><strong>{c}</strong></td>
            <td>{stats['total']} SV</td>
            <td>{stats['took']} SV</td>
            <td><span class="badge pass">{stats['pass']} SV</span></td>
            <td><strong>{stats['pass_pct']}%</strong></td>
            <td style="color:var(--color-primary);font-weight:700;">{stats['avg_qtkd']}</td>
            <td style="color:#22d3ee;font-weight:700;">{stats['avg_knm']}</td>
            <td style="color:#60a5fa;font-weight:700;">{stats['avg_ta']} / 990</td>
        </tr>
        '''
        
    group_cards_html = ''
    for g, ginfo in group_stats.items():
        score_color = 'var(--color-success)' if ginfo['avg_qtkd'] >= 75 else ('var(--color-primary)' if ginfo['avg_qtkd'] >= 65 else 'var(--color-danger)')
        members_str = ', '.join(ginfo['students'][:6]) + ('...' if len(ginfo['students']) > 6 else '')
        group_cards_html += f'''
        <div class="group-card">
            <div class="group-header">
                <div class="group-title">🎯 {g}</div>
                <div class="group-score" style="color:{score_color}">{ginfo['avg_qtkd']} đ</div>
            </div>
            <div style="font-size:0.75rem;color:var(--text-muted);margin-bottom:0.6rem;">
                Quy mô: <strong>{ginfo['total']} thành viên</strong> • KNM TB: <strong style="color:#22d3ee">{ginfo['avg_knm']}</strong>
            </div>
            <div class="member-list">
                <strong>Thành viên:</strong> {members_str}
            </div>
        </div>
        '''

    group_options = ''.join([f'<option value="{g}">{g}</option>' for g in groups])
    career_options = ''.join([f'<option value="{c}">{c}</option>' for c in sorted(list(careers.keys()))])

    html_out = f'''<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Báo cáo ĐGNL Khóa K25 Quản Trị Kinh Doanh (QTKD) | Rikkei Education</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <style>
        :root {{
            --bg-main:       #09090b;
            --bg-card:       #18181b;
            --bg-card2:      #1c1c1f;
            --border-color:  #27272a;
            --text-primary:  #f4f4f5;
            --text-secondary:#a1a1aa;
            --text-muted:    #71717a;
            --color-primary: #f59e0b;
            --color-accent:  #8b5cf6;
            --color-success: #10b981;
            --color-danger:  #ef4444;
            --color-blue:    #3b82f6;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', sans-serif; }}
        body {{ background: var(--bg-main); color: var(--text-primary); padding-bottom: 80px; }}

        .header {{
            background: rgba(18,18,21,0.85);
            backdrop-filter: blur(14px);
            border-bottom: 1px solid var(--border-color);
            position: sticky; top: 0; z-index: 200;
        }}
        .header-inner {{
            max-width: 1440px; margin: 0 auto;
            padding: 1rem 2rem;
            display: flex; justify-content: space-between; align-items: center;
        }}
        .logo-wrap {{ display: flex; align-items: center; gap: 0.75rem; }}
        .logo-badge {{
            background: linear-gradient(135deg, var(--color-primary), var(--color-accent));
            color: #000; width: 40px; height: 40px; border-radius: 10px;
            display: flex; align-items: center; justify-content: center;
            font-family: 'Outfit', sans-serif; font-weight: 800; font-size: 1.1rem;
            box-shadow: 0 4px 16px rgba(245,158,11,0.3);
        }}
        .logo-text {{ font-family: 'Outfit', sans-serif; font-weight: 700; font-size: 1.05rem; color: #fff; }}
        .header-meta {{ font-size: 0.78rem; color: var(--text-muted); text-align: right; line-height: 1.4; }}

        .container {{ max-width: 1440px; margin: 2rem auto; padding: 0 2rem; }}

        .nav-tabs {{
            display: flex; gap: 0.5rem; border-bottom: 1px solid var(--border-color);
            margin-bottom: 2rem; overflow-x: auto; padding-bottom: 0.2rem;
        }}
        .tab-btn {{
            background: transparent; border: none; color: var(--text-muted);
            font-family: 'Outfit', sans-serif; font-size: 0.95rem; font-weight: 600;
            padding: 0.75rem 1.25rem; border-radius: 8px 8px 0 0; cursor: pointer;
            transition: all 0.2s; border-bottom: 2px solid transparent;
            display: flex; align-items: center; gap: 0.5rem;
        }}
        .tab-btn:hover {{ color: var(--text-primary); background: rgba(255,255,255,0.03); }}
        .tab-btn.active {{
            color: var(--color-primary); border-bottom: 2px solid var(--color-primary);
            background: rgba(245,158,11,0.05);
        }}

        .kpi-grid {{
            display: grid; grid-template-columns: repeat(6, 1fr); gap: 1rem; margin-bottom: 2rem;
        }}
        .kpi-card {{
            background: var(--bg-card); border: 1px solid var(--border-color);
            border-radius: 12px; padding: 1.25rem 1.25rem; position: relative; overflow: hidden;
        }}
        .kpi-card::before {{
            content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
            background: linear-gradient(90deg, var(--accent-l), var(--accent-r));
        }}
        .kpi-card.gold   {{ --accent-l: #f59e0b; --accent-r: #fbbf24; }}
        .kpi-card.green  {{ --accent-l: #10b981; --accent-r: #34d399; }}
        .kpi-card.purple {{ --accent-l: #8b5cf6; --accent-r: #a78bfa; }}
        .kpi-card.blue   {{ --accent-l: #3b82f6; --accent-r: #60a5fa; }}
        .kpi-card.red    {{ --accent-l: #ef4444; --accent-r: #f87171; }}
        .kpi-card.cyan   {{ --accent-l: #06b6d4; --accent-r: #22d3ee; }}

        .kpi-label {{ font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.5px; color: var(--text-muted); margin-bottom: 0.4rem; }}
        .kpi-value {{ font-family: 'Outfit', sans-serif; font-size: 1.8rem; font-weight: 800; color: var(--text-primary); }}
        .kpi-sub   {{ font-size: 0.73rem; color: var(--text-secondary); margin-top: 0.25rem; }}

        .section-title {{
            font-family: 'Outfit', sans-serif; font-size: 1.15rem; font-weight: 700;
            color: #fff; border-left: 4px solid var(--color-primary); padding-left: 0.75rem;
            margin-bottom: 1.25rem; display: flex; justify-content: space-between; align-items: center;
        }}

        .grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-bottom: 2rem; }}
        .grid-3 {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 2rem; }}

        .card {{
            background: var(--bg-card); border: 1px solid var(--border-color);
            border-radius: 12px; padding: 1.5rem;
        }}

        .custom-table {{ width: 100%; border-collapse: collapse; font-size: 0.85rem; }}
        .custom-table th, .custom-table td {{ padding: 0.75rem 1rem; border: 1px solid var(--border-color); text-align: left; }}
        .custom-table th {{ background: rgba(255,255,255,0.03); color: var(--text-secondary); font-weight: 600; font-size: 0.78rem; text-transform: uppercase; }}
        .custom-table tr:hover {{ background: rgba(255,255,255,0.02); }}

        .badge {{
            display: inline-block; padding: 0.2rem 0.6rem; border-radius: 9999px;
            font-size: 0.75rem; font-weight: 700;
        }}
        .badge.pass {{ background: rgba(16,185,129,0.15); color: #34d399; border: 1px solid rgba(16,185,129,0.3); }}
        .badge.fail {{ background: rgba(239,68,68,0.15); color: #f87171; border: 1px solid rgba(239,68,68,0.3); }}
        .badge.tier3 {{ background: rgba(139,92,246,0.15); color: #a78bfa; border: 1px solid rgba(139,92,246,0.3); }}
        .badge.tier2 {{ background: rgba(59,130,246,0.15); color: #60a5fa; border: 1px solid rgba(59,130,246,0.3); }}
        .badge.tier1 {{ background: rgba(245,158,11,0.15); color: #fbbf24; border: 1px solid rgba(245,158,11,0.3); }}

        .filter-bar {{
            display: flex; gap: 1rem; flex-wrap: wrap; margin-bottom: 1.5rem;
            background: var(--bg-card); border: 1px solid var(--border-color);
            padding: 1rem; border-radius: 10px; align-items: center;
        }}
        .filter-input, .filter-select {{
            background: #121214; border: 1px solid var(--border-color);
            color: #fff; padding: 0.55rem 0.85rem; border-radius: 6px; font-size: 0.85rem;
            outline: none;
        }}
        .filter-input:focus, .filter-select:focus {{ border-color: var(--color-primary); }}

        .tab-pane {{ display: none; }}
        .tab-pane.active {{ display: block; animation: fadeIn 0.3s ease; }}
        @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(6px); }} to {{ opacity: 1; transform: translateY(0); }} }}

        .group-card {{
            background: rgba(255,255,255,0.02); border: 1px solid var(--border-color);
            border-radius: 10px; padding: 1.25rem; transition: transform 0.2s, border-color 0.2s;
        }}
        .group-card:hover {{ transform: translateY(-3px); border-color: #52525b; }}
        .group-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem; }}
        .group-title {{ font-family: 'Outfit', sans-serif; font-size: 1.1rem; font-weight: 700; color: #fff; }}
        .group-score {{ font-family: 'Outfit', sans-serif; font-size: 1.3rem; font-weight: 800; color: var(--color-primary); }}
        .member-list {{ font-size: 0.8rem; color: var(--text-secondary); line-height: 1.6; }}

        .callout {{
            background: rgba(245,158,11,0.06); border: 1px solid rgba(245,158,11,0.25);
            border-left: 4px solid var(--color-primary); border-radius: 8px; padding: 1rem 1.25rem;
            margin-bottom: 1.5rem; font-size: 0.85rem; color: var(--text-secondary); line-height: 1.6;
        }}
        .callout strong {{ color: #fbbf24; }}

        .report-footer {{
            margin-top: 3rem; border-top: 1px solid var(--border-color);
            padding-top: 1.5rem; display: flex; justify-content: space-between; align-items: center;
            font-size: 0.78rem; color: var(--text-muted);
        }}
    </style>
</head>
<body>

    <header class="header">
        <div class="header-inner">
            <div class="logo-wrap">
                <div class="logo-badge">QTKD</div>
                <div>
                    <div class="logo-text">Báo Cáo ĐGNL Khóa K25 Quản Trị Kinh Doanh</div>
                    <div style="font-size:0.72rem;color:var(--text-muted);">Hệ Đào tạo PTIT - Rikkei Education | Đợt 1 (Cập nhật sau thi bổ sung)</div>
                </div>
            </div>
            <div class="header-meta">
                Dành cho Ban Giám đốc & Phòng Đào tạo<br>
                Ngày phát hành: 02/09/2026
            </div>
        </div>
    </header>

    <div class="container">

        <div class="nav-tabs">
            <button class="tab-btn active" onclick="switchTab('tab1', event)">📊 Tổng quan Khối QTKD</button>
            <button class="tab-btn" onclick="switchTab('tab2', event)">👥 11 Nhóm Dự Án Kinh Doanh</button>
            <button class="tab-btn" onclick="switchTab('tab3', event)">🎯 Đánh giá Đa chiều 'Kiềng 3 Chân'</button>
            <button class="tab-btn" onclick="switchTab('tab4', event)">📋 Danh bạ Học viên & Hướng nghiệp</button>
        </div>

        <div class="kpi-grid">
            <div class="kpi-card gold">
                <div class="kpi-label">Tổng SV đăng ký</div>
                <div class="kpi-value">{total_reg}</div>
                <div class="kpi-sub">3 lớp: QTKD1, QTKD2, QTKD3</div>
            </div>
            <div class="kpi-card green">
                <div class="kpi-label">Dự thi thực tế</div>
                <div class="kpi-value">{total_took}</div>
                <div class="kpi-sub">Tỷ lệ tham gia: 98.1%</div>
            </div>
            <div class="kpi-card purple">
                <div class="kpi-label">Tỷ lệ Đạt chuẩn</div>
                <div class="kpi-value">{pass_pct}%</div>
                <div class="kpi-sub">{total_pass}/{total_reg} SV Đạt chuyên môn</div>
            </div>
            <div class="kpi-card gold">
                <div class="kpi-label">Điểm TB QTKD</div>
                <div class="kpi-value">{avg_qtkd}/100</div>
                <div class="kpi-sub">Thang điểm chuyên môn 100</div>
            </div>
            <div class="kpi-card cyan">
                <div class="kpi-label">Điểm TB Kỹ năng mềm</div>
                <div class="kpi-value">{avg_knm}/100</div>
                <div class="kpi-sub">Thuyết trình & Làm việc nhóm</div>
            </div>
            <div class="kpi-card blue">
                <div class="kpi-label">Điểm TB Tiếng Anh</div>
                <div class="kpi-value">{avg_ta}/990</div>
                <div class="kpi-sub">Điểm nghẽn cần bổ trợ</div>
            </div>
        </div>

        <!-- TAB 1 -->
        <div id="tab1" class="tab-pane active">
            <div class="callout">
                📌 <strong>Nhận định Tổng quan:</strong> Khối Quản trị Kinh doanh (K25) ghi nhận tỷ lệ tham gia thi rất cao (<strong>98.1%</strong>) và tỷ lệ Đạt chuyên môn ấn tượng (<strong>{pass_pct}%</strong>). Năng lực thuyết trình dự án và làm việc nhóm của sinh viên phát huy xuất sắc (Điểm KNM trung bình đạt <strong>{avg_knm}/100</strong>). Tuy nhiên, <strong>Ngoại ngữ (Tiếng Anh TB {avg_ta}/990)</strong> đang là khoảng trống lớn nhất cản trở cơ hội ứng tuyển vào các tập đoàn đa quốc gia.
            </div>

            <div class="grid-2">
                <div class="card">
                    <div class="section-title">📊 So sánh Kết quả 3 Lớp QTKD</div>
                    <div style="height: 280px; position: relative;">
                        <canvas id="classChart"></canvas>
                    </div>
                </div>

                <div class="card">
                    <div class="section-title">📈 Phân bổ Điểm Chuyên môn QTKD</div>
                    <div style="height: 280px; position: relative;">
                        <canvas id="scoreDistChart"></canvas>
                    </div>
                </div>
            </div>

            <div class="card" style="margin-bottom: 2rem;">
                <div class="section-title">🏫 Bảng Thống kê Chi tiết theo Lớp Học</div>
                <table class="custom-table">
                    <thead>
                        <tr>
                            <th>Mã Lớp</th>
                            <th>Sĩ số</th>
                            <th>Dự thi</th>
                            <th>Đạt chuẩn</th>
                            <th>Tỷ lệ Đạt</th>
                            <th>Điểm TB QTKD</th>
                            <th>Điểm TB Kỹ năng mềm</th>
                            <th>Điểm TB Tiếng Anh</th>
                        </tr>
                    </thead>
                    <tbody>
                        {class_table_rows}
                    </tbody>
                </table>
            </div>
        </div>

        <!-- TAB 2 -->
        <div id="tab2" class="tab-pane">
            <div class="callout">
                🏆 <strong>Hình thức thi ĐGNL QTKD:</strong> Học viên được tổ chức thành <strong>11 Nhóm dự án</strong> để xây dựng kế hoạch kinh doanh thực chiến và bảo vệ trực tiếp trước Hội đồng giám khảo. Điểm số phản ánh sự kết hợp giữa tính khả thi của mô hình kinh doanh và bản lĩnh phản biện của từng thành viên.
            </div>

            <div class="grid-3">
                {group_cards_html}
            </div>
        </div>

        <!-- TAB 3 -->
        <div id="tab3" class="tab-pane">
            <div class="callout">
                ⚖ <strong>Mô hình Đánh giá Kiềng 3 Chân:</strong> Để đảm bảo sinh viên tốt nghiệp có việc làm đúng ngành với mức lương cạnh tranh, năng lực cần đạt chuẩn đồng thời ở 3 trụ cột:
                <strong>1. Kiến thức Chuyên môn QTKD</strong> (Lập kế hoạch, vận hành, phân tích thị trường) 
                • <strong>2. Kỹ năng Mềm & Thuyết trình</strong> (Đàm phán, làm việc nhóm, bảo vệ ý tưởng) 
                • <strong>3. Ngoại ngữ Quốc tế</strong> (Tiếng Anh giao tiếp & thương mại).
            </div>

            <div class="grid-2">
                <div class="card">
                    <div class="section-title">🎯 Phân loại Mức độ Sẵn sàng Nghề nghiệp</div>
                    <div style="display:flex;align-items:center;gap:1.5rem;height:260px;">
                        <div style="width:200px;height:200px;position:relative;flex-shrink:0;">
                            <canvas id="tierChart"></canvas>
                        </div>
                        <div style="display:flex;flex-direction:column;gap:0.6rem;font-size:0.83rem;">
                            <div><span class="badge tier3">Mức 3 - Toàn diện:</span> <strong>{tier_counts['tier_3']} SV</strong> (Sẵn sàng Quốc tế)</div>
                            <div><span class="badge tier2">Mức 2 - Chuẩn Doanh nghiệp:</span> <strong>{tier_counts['tier_2']} SV</strong> (Vững chuyên môn + KNM)</div>
                            <div><span class="badge tier1">Mức 1 - Cơ bản:</span> <strong>{tier_counts['tier_1']} SV</strong> (Cần nâng cao kỹ năng)</div>
                            <div><span class="badge fail">Mức 0 - Chưa đạt:</span> <strong>{tier_counts['tier_0']} SV</strong> (Vắng thi / Cần học lại)</div>
                        </div>
                    </div>
                </div>

                <div class="card">
                    <div class="section-title">🌐 Phân bố Điểm Tiếng Anh Khối QTKD</div>
                    <div style="height:260px;position:relative;">
                        <canvas id="taDistChart"></canvas>
                    </div>
                </div>
            </div>

            <div class="card" style="margin-bottom:2rem;">
                <div class="section-title">💡 Phân tích Chuyên sâu Rủi ro Việc làm & Giải pháp Can thiệp</div>
                <div class="grid-3" style="margin-bottom:0;">
                    <div style="background:rgba(255,255,255,0.02);padding:1rem;border-radius:8px;border:1px solid var(--border-color);">
                        <div style="font-size:1.4rem;margin-bottom:0.4rem;">⚠️</div>
                        <div style="font-weight:700;color:#f87171;font-size:0.9rem;margin-bottom:0.3rem;">Bẫy Ngoại ngữ Sơ cấp</div>
                        <div style="font-size:0.8rem;color:var(--text-secondary);line-height:1.5;">
                            Có tới <strong>40/62 sinh viên</strong> điểm chuyên môn giỏi (>= 70) nhưng Tiếng Anh dưới 350. Khi ra trường, các bạn sẽ bị giới hạn chỉ nộp được vào các doanh nghiệp SME nội địa, bỏ lỡ các vị trí Management Trainee tại MNCs.
                        </div>
                    </div>
                    <div style="background:rgba(255,255,255,0.02);padding:1rem;border-radius:8px;border:1px solid var(--border-color);">
                        <div style="font-size:1.4rem;margin-bottom:0.4rem;">🌟</div>
                        <div style="font-weight:700;color:#34d399;font-size:0.9rem;margin-bottom:0.3rem;">Thế mạnh Giao tiếp & Thuyết trình</div>
                        <div style="font-size:0.8rem;color:var(--text-secondary);line-height:1.5;">
                            Điểm KNM đạt <strong>75.74/100</strong> cho thấy sinh viên QTKD có phong thái tự tin, phản xạ bảo vệ quan điểm tốt. Đây là thế mạnh vượt trội so với sinh viên khối CNTT (vốn hay bị điểm nghẽn vấn đáp).
                        </div>
                    </div>
                    <div style="background:rgba(255,255,255,0.02);padding:1rem;border-radius:8px;border:1px solid var(--border-color);">
                        <div style="font-size:1.4rem;margin-bottom:0.4rem;">🚀</div>
                        <div style="font-weight:700;color:#60a5fa;font-size:0.9rem;margin-bottom:0.3rem;">Khuyến nghị Can thiệp Kỳ Tiếp</div>
                        <div style="font-size:0.8rem;color:var(--text-secondary);line-height:1.5;">
                            Triển khai <strong>Business English Bootcamp</strong> (tiếng Anh thương mại, viết email, thuyết trình dự án bằng tiếng Anh) bắt buộc từ Kỳ 3 để đưa ít nhất 60% học viên cán mốc TOEIC 450+.
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 4 -->
        <div id="tab4" class="tab-pane">
            <div class="filter-bar">
                <input type="text" id="searchInput" class="filter-input" placeholder="🔍 Tìm theo Tên hoặc Email..." style="flex:1;min-width:200px;" oninput="applyFilters()">
                <select id="classFilter" class="filter-select" onchange="applyFilters()">
                    <option value="">-- Tất cả Lớp --</option>
                    <option value="HN-K25-QTKD1">HN-K25-QTKD1</option>
                    <option value="HN-K25-QTKD2">HN-K25-QTKD2</option>
                    <option value="HN-K25-QTKD3">HN-K25-QTKD3</option>
                </select>
                <select id="groupFilter" class="filter-select" onchange="applyFilters()">
                    <option value="">-- Tất cả Nhóm --</option>
                    {group_options}
                </select>
                <select id="tierFilter" class="filter-select" onchange="applyFilters()">
                    <option value="">-- Tất cả Mức Sẵn sàng --</option>
                    <option value="3">Mức 3: Sẵn sàng Quốc tế</option>
                    <option value="2">Mức 2: Chuẩn Doanh nghiệp</option>
                    <option value="1">Mức 1: Cơ bản</option>
                    <option value="0">Mức 0: Chưa đạt / Vắng</option>
                </select>
                <select id="careerFilter" class="filter-select" onchange="applyFilters()">
                    <option value="">-- Định hướng Nghề nghiệp --</option>
                    {career_options}
                </select>
            </div>

            <div class="card">
                <div class="section-title">
                    <span>📋 Danh sách Học viên Khối QTKD (<span id="recordCount">{len(students)}</span> SV)</span>
                </div>
                <div style="overflow-x:auto;">
                    <table class="custom-table" id="studentTable">
                        <thead>
                            <tr>
                                <th>Họ và tên</th>
                                <th>Lớp</th>
                                <th>Nhóm</th>
                                <th>Điểm QTKD</th>
                                <th>Kỹ năng mềm</th>
                                <th>Tiếng Anh</th>
                                <th>Mức Sẵn sàng</th>
                                <th>Định hướng Nghề nghiệp</th>
                                <th>Ghi chú Tư vấn</th>
                            </tr>
                        </thead>
                        <tbody id="tableBody">
                            {tbody_rows}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <div class="report-footer">
            <div>
                <div style="font-weight:600;color:var(--text-secondary);">Báo cáo ĐGNL Khóa K25 Quản Trị Kinh Doanh (QTKD)</div>
                <div>Rikkei Education | Phòng Chuyên môn Đào tạo | Ngày phát hành: 02/09/2026</div>
            </div>
            <div style="text-align:right;">
                <div>Xem thêm báo cáo khác:</div>
                <div><a href="Executive_Summary_DGNL_Report.html" style="color:var(--color-primary)">📑 Executive Summary</a> &nbsp;|&nbsp; <a href="KS24_DGNL_Report.html" style="color:var(--color-success)">☕ Báo cáo KS24</a> &nbsp;|&nbsp; <a href="KS25_DGNL_Report.html" style="color:var(--color-blue)">🐍 Báo cáo KS25</a></div>
            </div>
        </div>

    </div>

    <script>
    const studentsData = {students_json};

    function switchTab(tabId, evt) {{
        document.querySelectorAll('.tab-pane').forEach(el => el.classList.remove('active'));
        document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
        
        document.getElementById(tabId).classList.add('active');
        if (evt && evt.currentTarget) {{
            evt.currentTarget.classList.add('active');
        }}
    }}

    function renderTable(data) {{
        const tbody = document.getElementById('tableBody');
        tbody.innerHTML = '';
        
        data.forEach(s => {{
            const tr = document.createElement('tr');
            
            const tierBadge = s.tier === 3 ? '<span class="badge tier3">Mức 3</span>' :
                             (s.tier === 2 ? '<span class="badge tier2">Mức 2</span>' :
                             (s.tier === 1 ? '<span class="badge tier1">Mức 1</span>' : '<span class="badge fail">Mức 0</span>'));
                             
            const qtkdColor = s.final >= 75 ? 'color:#34d399;font-weight:700;' : (s.final >= 60 ? 'color:#fbbf24;font-weight:700;' : 'color:#f87171;font-weight:700;');
            
            tr.innerHTML = `
                <td><strong>${{s.name}}</strong></td>
                <td>${{s.class}}</td>
                <td><span style="color:var(--color-primary);font-weight:600;">${{s.nhom}}</span></td>
                <td style="${{qtkdColor}}">${{s.final}}</td>
                <td style="color:#22d3ee;font-weight:600;">${{s.knm_score}}</td>
                <td style="color:#60a5fa;font-weight:600;">${{s.ta_score > 0 ? s.ta_score + ' / 990' : '<span style="color:var(--text-muted)">Chưa có</span>'}}</td>
                <td>${{tierBadge}}</td>
                <td><strong style="color:#fff;">${{s.career}}</strong></td>
                <td style="font-size:0.78rem;color:var(--text-secondary);max-width:280px;">${{s.career_note}}</td>
            `;
            tbody.appendChild(tr);
        }});
        
        document.getElementById('recordCount').innerText = data.length;
    }}

    function applyFilters() {{
        const search = document.getElementById('searchInput').value.toLowerCase().trim();
        const cFilter = document.getElementById('classFilter').value;
        const gFilter = document.getElementById('groupFilter').value;
        const tFilter = document.getElementById('tierFilter').value;
        const carFilter = document.getElementById('careerFilter').value;
        
        const filtered = studentsData.filter(s => {{
            const matchSearch = !search || s.name.toLowerCase().includes(search) || (s.email && s.email.toLowerCase().includes(search));
            const matchClass = !cFilter || s.class === cFilter;
            const matchGroup = !gFilter || s.nhom === gFilter;
            const matchTier = tFilter === "" || s.tier.toString() === tFilter;
            const matchCareer = !carFilter || s.career === carFilter;
            return matchSearch && matchClass && matchGroup && matchTier && matchCareer;
        }});
        
        renderTable(filtered);
    }}

    const classCtx = document.getElementById('classChart').getContext('2d');
    new Chart(classCtx, {{
        type: 'bar',
        data: {{
            labels: ['QTKD1', 'QTKD2', 'QTKD3'],
            datasets: [
                {{
                    label: 'Điểm TB QTKD',
                    data: [{class_stats['HN-K25-QTKD1']['avg_qtkd']}, {class_stats['HN-K25-QTKD2']['avg_qtkd']}, {class_stats['HN-K25-QTKD3']['avg_qtkd']}],
                    backgroundColor: 'rgba(245,158,11,0.7)',
                    borderColor: '#f59e0b',
                    borderWidth: 1.5, borderRadius: 6
                }},
                {{
                    label: 'Điểm TB KNM',
                    data: [{class_stats['HN-K25-QTKD1']['avg_knm']}, {class_stats['HN-K25-QTKD2']['avg_knm']}, {class_stats['HN-K25-QTKD3']['avg_knm']}],
                    backgroundColor: 'rgba(34,211,238,0.7)',
                    borderColor: '#22d3ee',
                    borderWidth: 1.5, borderRadius: 6
                }}
            ]
        }},
        options: {{
            responsive: true, maintainAspectRatio: false,
            plugins: {{ legend: {{ labels: {{ color: '#a1a1aa' }} }} }},
            scales: {{
                y: {{ beginAtZero: true, max: 100, grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ color: '#a1a1aa' }} }},
                x: {{ grid: {{ display: false }}, ticks: {{ color: '#a1a1aa' }} }}
            }}
        }}
    }});

    const distCtx = document.getElementById('scoreDistChart').getContext('2d');
    new Chart(distCtx, {{
        type: 'bar',
        data: {{
            labels: ['0-49 (Chưa đạt)', '50-59 (Cơ bản)', '60-69 (Khá)', '70-79 (Giỏi)', '80-100 (Xuất sắc)'],
            datasets: [{{
                label: 'Số lượng sinh viên',
                data: [
                    studentsData.filter(s => s.final < 50).length,
                    studentsData.filter(s => s.final >= 50 && s.final < 60).length,
                    studentsData.filter(s => s.final >= 60 && s.final < 70).length,
                    studentsData.filter(s => s.final >= 70 && s.final < 80).length,
                    studentsData.filter(s => s.final >= 80).length
                ],
                backgroundColor: ['#ef4444', '#f59e0b', '#3b82f6', '#10b981', '#8b5cf6'],
                borderRadius: 6
            }}]
        }},
        options: {{
            responsive: true, maintainAspectRatio: false,
            plugins: {{ legend: {{ display: false }} }},
            scales: {{
                y: {{ beginAtZero: true, grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ color: '#a1a1aa' }} }},
                x: {{ grid: {{ display: false }}, ticks: {{ color: '#a1a1aa', font: {{ size: 10 }} }} }}
            }}
        }}
    }});

    const tierCtx = document.getElementById('tierChart').getContext('2d');
    new Chart(tierCtx, {{
        type: 'doughnut',
        data: {{
            labels: ['Mức 3 - Toàn diện', 'Mức 2 - Chuẩn Doanh nghiệp', 'Mức 1 - Cơ bản', 'Mức 0 - Chưa đạt'],
            datasets: [{{
                data: [{tier_counts['tier_3']}, {tier_counts['tier_2']}, {tier_counts['tier_1']}, {tier_counts['tier_0']}],
                backgroundColor: ['#8b5cf6', '#3b82f6', '#f59e0b', '#ef4444'],
                borderWidth: 2, borderColor: '#18181b'
            }}]
        }},
        options: {{
            responsive: true, maintainAspectRatio: false,
            cutout: '70%',
            plugins: {{ legend: {{ display: false }} }}
        }}
    }});

    const taCtx = document.getElementById('taDistChart').getContext('2d');
    new Chart(taCtx, {{
        type: 'bar',
        data: {{
            labels: ['Chưa có / 0', '< 250 (Sơ cấp A1)', '250 - 350 (A2)', '350 - 500 (B1)', '>= 500 (B2/Quốc tế)'],
            datasets: [{{
                label: 'Số SV',
                data: [
                    studentsData.filter(s => s.ta_score === 0).length,
                    studentsData.filter(s => s.ta_score > 0 && s.ta_score < 250).length,
                    studentsData.filter(s => s.ta_score >= 250 && s.ta_score < 350).length,
                    studentsData.filter(s => s.ta_score >= 350 && s.ta_score < 500).length,
                    studentsData.filter(s => s.ta_score >= 500).length
                ],
                backgroundColor: ['#71717a', '#ef4444', '#f59e0b', '#3b82f6', '#10b981'],
                borderRadius: 6
            }}]
        }},
        options: {{
            responsive: true, maintainAspectRatio: false,
            plugins: {{ legend: {{ display: false }} }},
            scales: {{
                y: {{ beginAtZero: true, grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ color: '#a1a1aa' }} }},
                x: {{ grid: {{ display: false }}, ticks: {{ color: '#a1a1aa', font: {{ size: 10 }} }} }}
            }}
        }}
    }});
    </script>
</body>
</html>
'''

    with open('outputs/QTKD_DGNL_Report.html', 'w', encoding='utf-8') as f:
        f.write(html_out)
        
    print('Generated outputs/QTKD_DGNL_Report.html successfully!')

if __name__ == '__main__':
    main()
