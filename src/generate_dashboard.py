import json
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

def main():
    json_path = "scratch/ks24_stats.json"
    html_output_path = "outputs/KS24_DGNL_Report.html"
    
    if not os.path.exists(json_path):
        print(f"Stats JSON not found: {json_path}")
        return
        
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    summary = data['summary']
    students = data['students']
    
    # Sort students by score descending for default list view
    students_sorted = sorted(students, key=lambda x: x['score'], reverse=True)
    
    # Calculate branch-wise stats for Tab 2 overview
    hn_students = [s for s in students if 'HN' in s['branch']]
    hcm_students = [s for s in students if 'HCM' in s['branch']]
    
    hn_registered = len(hn_students)
    hn_took = len([s for s in hn_students if s['final'] > 0])
    hn_avg = round(sum(s['score'] for s in hn_students if s['final'] > 0) / hn_took, 2) if hn_took else 0.0
    hn_ready = len([s for s in hn_students if s['readiness_level'] in [2, 3]])
    hn_ready_pct = round(hn_ready / hn_registered * 100, 1) if hn_registered else 0.0
    
    hcm_registered = len(hcm_students)
    hcm_took = len([s for s in hcm_students if s['final'] > 0])
    hcm_avg = round(sum(s['score'] for s in hcm_students if s['final'] > 0) / hcm_took, 2) if hcm_took else 0.0
    hcm_ready = len([s for s in hcm_students if s['readiness_level'] in [2, 3]])
    hcm_ready_pct = round(hcm_ready / hcm_registered * 100, 1) if hcm_registered else 0.0
    
    # Prepare data for Chart 1: Score distribution (0 to 10, in steps of 0.5 or 1.0)
    score_bins = {str(i): 0 for i in range(11)}
    # Add floating half scores like 9.5
    score_bins_half = {
        "0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0,
        "9.5": 0, "8.5": 0, "7.5": 0, "6.5": 0, "5.5": 0, "4.5": 0, "3.5": 0, "2.5": 0, "1.5": 0, "0.5": 0
    }
    for s in students:
        sc = s['score']
        # Convert to string to avoid float representation issues
        sc_str = str(sc)
        if sc_str in score_bins_half:
            score_bins_half[sc_str] += 1
        else:
            # fallback to integer rounding
            rounded = str(int(round(sc)))
            if rounded in score_bins_half:
                score_bins_half[rounded] += 1
                
    # Filter active test-takers (final score > 0) for the score distribution chart
    active_students = [s for s in students if s['final'] > 0.0]
    
    # Sort keys for chart
    chart1_labels = ["0-3.5", "4-4.5", "5-5.5", "6-6.5", "7-7.5", "8-8.5", "9-9.5", "10"]
    chart1_data = [0, 0, 0, 0, 0, 0, 0, 0]
    for s in active_students:
        sc = s['score']
        if sc < 4.0: chart1_data[0] += 1
        elif sc < 5.0: chart1_data[1] += 1
        elif sc < 6.0: chart1_data[2] += 1
        elif sc < 7.0: chart1_data[3] += 1
        elif sc < 8.0: chart1_data[4] += 1
        elif sc < 9.0: chart1_data[5] += 1
        elif sc < 10.0: chart1_data[6] += 1
        else: chart1_data[7] += 1
        
    # Prepare sorted job matches for Chart 4
    role_mapping = {
        'backend_dev': 'Lập trình viên Backend Java',
        'frontend_dev': 'Lập trình viên Frontend React',
        'fullstack_dev': 'Lập trình viên Fullstack Java-React',
        'api_qa': 'Kỹ sư kiểm thử API / QA',
        'python_dev': 'Lập trình viên Python (Backend/AI)',
        'devops': 'Kỹ sư DevOps',
        'data_analyst': 'Chuyên viên phân tích dữ liệu',
        'ai_integration': 'Kỹ sư tích hợp AI',
        'business_analyst': 'Chuyên viên phân tích nghiệp vụ (BA)',
        'mobile_dev': 'Lập trình viên di động (Flutter/Android)'
    }
    
    role_sorting = {}
    for r in role_mapping.keys():
        comp = summary['job_compatibility'][r]
        role_sorting[r] = comp['level_3'] + comp['level_2'] + comp['level_1']
        
    sorted_roles = sorted(role_mapping.keys(), key=lambda x: role_sorting[x], reverse=True)
    
    sorted_labels = [role_mapping[r] for r in sorted_roles]
    sorted_l3 = [summary['job_compatibility'][r]['level_3'] for r in sorted_roles]
    sorted_l2 = [summary['job_compatibility'][r]['level_2'] for r in sorted_roles]
    sorted_l1 = [summary['job_compatibility'][r]['level_1'] for r in sorted_roles]
    sorted_l0 = [summary['job_compatibility'][r]['level_0'] for r in sorted_roles]
    
    # Calculate MCQ stats for KS24 cohort based on valid test-takers
    ks24_tn_vals = [s['tn'] for s in students if s.get('tn') is not None]
    mcq_count = len(ks24_tn_vals)
    if mcq_count > 0:
        mcq_avg = sum(ks24_tn_vals) / mcq_count
        variance = sum((x - mcq_avg) ** 2 for x in ks24_tn_vals) / mcq_count
        mcq_std = variance ** 0.5
    else:
        mcq_avg = 0.0
        mcq_std = 0.0
        
    exc_cnt = len([x for x in ks24_tn_vals if x >= 90.0])
    vg_cnt = len([x for x in ks24_tn_vals if 80.0 <= x < 90.0])
    g_cnt = len([x for x in ks24_tn_vals if 70.0 <= x < 80.0])
    avg_cnt = len([x for x in ks24_tn_vals if 50.0 <= x < 70.0])
    fail_cnt = len([x for x in ks24_tn_vals if x < 50.0])
    
    exc_pct = round(exc_cnt / mcq_count * 100, 1) if mcq_count else 0.0
    vg_pct = round(vg_cnt / mcq_count * 100, 1) if mcq_count else 0.0
    g_pct = round(g_cnt / mcq_count * 100, 1) if mcq_count else 0.0
    avg_pct = round(avg_cnt / mcq_count * 100, 1) if mcq_count else 0.0
    fail_pct = round(fail_cnt / mcq_count * 100, 1) if mcq_count else 0.0
        
    html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Báo Cáo ĐGNL Lần 1 - Khóa KS24</title>
    
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    
    <!-- Chart.js CDN -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    
    <style>
        :root {{
            --bg-base: #09090b;
            --bg-card: #18181b;
            --bg-card-hover: #202024;
            --border-color: #27272a;
            --text-primary: #f4f4f5;
            --text-secondary: #a1a1aa;
            --color-primary: #3b82f6; /* Blue */
            --color-primary-rgb: 59, 130, 246;
            --color-success: #10b981; /* Emerald */
            --color-warning: #f59e0b; /* Amber */
            --color-danger: #ef4444; /* Rose */
            --color-purple: #8b5cf6; /* Violet */
        }}
        
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        
        body {{
            background-color: var(--bg-base);
            color: var(--text-primary);
            font-family: 'Inter', sans-serif;
            line-height: 1.6;
            padding-bottom: 60px;
        }}
        
        .header {{
            background: rgba(24, 24, 27, 0.8);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border-color);
            position: sticky;
            top: 0;
            z-index: 100;
        }}
        
        .header-container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 1.25rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .logo-section {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }}
        
        .logo-icon {{
            font-size: 1.5rem;
        }}
        
        .logo-title {{
            font-family: 'Outfit', sans-serif;
            font-weight: 700;
            font-size: 1.1rem;
            color: white;
        }}
        
        .nav-tabs {{
            display: flex;
            gap: 0.5rem;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 2rem auto;
            padding: 0 2rem;
        }}
        
        h1, h2, h3, h4 {{
            font-family: 'Outfit', sans-serif;
            font-weight: 600;
        }}
        
        a {{
            color: var(--color-primary);
            text-decoration: none;
            transition: color 0.2s;
        }}
        
        a:hover {{
            color: #60a5fa;
            text-decoration: underline;
        }}
        

        
        .header-title h1 {{
            font-size: 2.2rem;
            background: linear-gradient(135deg, #fff 30%, var(--color-primary) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }}
        
        .header-title p {{
            color: var(--text-secondary);
            font-size: 1.1rem;
        }}
        
        .badge {{
            background: rgba(var(--color-primary-rgb), 0.1);
            color: var(--color-primary);
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.85rem;
            font-weight: 500;
            border: 1px solid rgba(var(--color-primary-rgb), 0.2);
            display: inline-block;
        }}
        
        /* KPIs */
        .kpi-container {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }}
        
        .kpi-card {{
            background-color: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.5rem;
            display: flex;
            flex-direction: column;
            position: relative;
            overflow: hidden;
            transition: transform 0.2s, border-color 0.2s;
        }}
        
        .kpi-card:hover {{
            transform: translateY(-2px);
            border-color: #3f3f46;
        }}
        
        .kpi-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
        }}
        
        .kpi-card.blue::before {{ background-color: var(--color-primary); }}
        .kpi-card.success::before {{ background-color: var(--color-success); }}
        .kpi-card.warning::before {{ background-color: var(--color-warning); }}
        .kpi-card.danger::before {{ background-color: var(--color-danger); }}
        
        .kpi-title {{
            color: var(--text-secondary);
            font-size: 0.9rem;
            font-weight: 500;
            margin-bottom: 0.5rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        .kpi-value {{
            font-size: 2.2rem;
            font-weight: 700;
            font-family: 'Outfit', sans-serif;
            color: #fff;
            line-height: 1.1;
        }}
        
        .kpi-desc {{
            color: var(--text-secondary);
            font-size: 0.85rem;
            margin-top: 0.5rem;
        }}
        
        /* Tabs */
        .tab-btn {{
            background: rgba(255,255,255,0.03);
            border: 1px solid var(--border-color);
            color: var(--text-secondary);
            padding: 0.5rem 1rem;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.88rem;
            font-weight: 500;
            transition: all 0.2s;
        }}
        
        .tab-btn:hover {{
            background: rgba(255,255,255,0.08);
            color: white;
        }}
        
        .tab-btn.active {{
            background: var(--color-primary);
            color: white;
            border-color: var(--color-primary);
        }}
        
        .tab-content {{
            display: none;
            animation: fadeIn 0.3s ease-in-out;
        }}
        
        .tab-content.active {{
            display: block;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(5px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        /* Grid system for layout */
        .dashboard-grid {{
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 1.5rem;
            margin-bottom: 1.5rem;
        }}
        
        @media (max-width: 1024px) {{
            .dashboard-grid {{
                grid-template-columns: 1fr;
            }}
        }}
        
        .card {{
            background-color: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
        }}
        
        .card-title {{
            font-size: 1.25rem;
            color: #fff;
            margin-bottom: 1.25rem;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 0.75rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        /* Charts styling */
        .charts-row {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
            margin-bottom: 1.5rem;
        }}
        
        .chart-container {{
            position: relative;
            height: 280px;
            width: 100%;
        }}
        
        /* Student Directory interactive view */
        .filter-bar {{
            display: flex;
            gap: 1rem;
            margin-bottom: 1rem;
            flex-wrap: wrap;
        }}
        
        .search-input {{
            background-color: var(--bg-base);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
            border-radius: 8px;
            padding: 0.6rem 1rem;
            font-family: inherit;
            flex-grow: 1;
            outline: none;
            transition: border-color 0.2s;
        }}
        
        .search-input:focus {{
            border-color: var(--color-primary);
        }}
        
        .select-filter {{
            background-color: var(--bg-base);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
            border-radius: 8px;
            padding: 0.6rem 1rem;
            font-family: inherit;
            outline: none;
            cursor: pointer;
        }}
        
        .reset-btn {{
            background-color: #27272a;
            border: 1px solid var(--border-color);
            color: var(--text-primary);
            border-radius: 8px;
            padding: 0.6rem 1rem;
            font-family: inherit;
            cursor: pointer;
            transition: background-color 0.2s, border-color 0.2s;
        }}
        
        .reset-btn:hover {{
            background-color: #3f3f46;
            border-color: #52525b;
        }}
        
        
        .students-table-container {{
            overflow-x: auto;
            border-radius: 8px;
            border: 1px solid var(--border-color);
        }}
        
        .students-table {{
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 0.95rem;
        }}
        
        .students-table th {{
            background-color: #202024;
            color: #fff;
            font-weight: 600;
            padding: 0.75rem 1rem;
            border-bottom: 1px solid var(--border-color);
        }}
        
        .students-table td {{
            padding: 0.75rem 1rem;
            border-bottom: 1px solid var(--border-color);
            color: var(--text-secondary);
        }}
        
        .students-table tr {{
            transition: background-color 0.2s;
        }}
        
        .students-table tr.student-row:hover {{
            background-color: var(--bg-card-hover);
            cursor: pointer;
        }}
        
        .students-table tr.active-row {{
            background-color: #272730;
        }}
        
        .students-table tr.detail-row {{
            display: none;
            background-color: #121214;
        }}
        
        .students-table tr.detail-row.active {{
            display: table-row;
        }}
        
        .student-details-box {{
            padding: 1.5rem;
            border-left: 4px solid var(--color-primary);
        }}
        
        .skills-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 1rem;
            margin-bottom: 1rem;
        }}
        
        .skill-item {{
            background-color: var(--bg-base);
            padding: 0.75rem;
            border-radius: 6px;
            border: 1px solid var(--border-color);
        }}
        
        .skill-item-title {{
            font-size: 0.8rem;
            color: var(--text-secondary);
            margin-bottom: 0.25rem;
        }}
        
        .skill-item-val {{
            font-size: 1.1rem;
            font-weight: 600;
            color: #fff;
            font-family: 'JetBrains Mono', monospace;
        }}
        
        .student-fail-skills {{
            color: var(--color-danger);
            font-size: 0.9rem;
            margin-top: 0.5rem;
        }}
        
        .student-crit-text {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            background-color: var(--bg-base);
            padding: 0.75rem;
            border-radius: 6px;
            border: 1px solid var(--border-color);
            margin-top: 0.5rem;
            white-space: pre-wrap;
            color: var(--text-secondary);
            max-height: 250px;
            overflow-y: auto;
        }}
        
        /* Level and match indicators */
        .lvl-badge {{
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-size: 0.8rem;
            font-weight: 600;
            display: inline-block;
        }}
        .lvl-badge.lvl-3 {{ background-color: rgba(16, 185, 129, 0.15); color: var(--color-success); border: 1px solid rgba(16, 185, 129, 0.3); }}
        .lvl-badge.lvl-2 {{ background-color: rgba(99, 102, 241, 0.15); color: var(--color-purple); border: 1px solid rgba(99, 102, 241, 0.3); }}
        .lvl-badge.lvl-1 {{ background-color: rgba(245, 158, 11, 0.15); color: var(--color-warning); border: 1px solid rgba(245, 158, 11, 0.3); }}
        .lvl-badge.lvl-0 {{ background-color: rgba(239, 68, 68, 0.15); color: var(--color-danger); border: 1px solid rgba(239, 68, 68, 0.3); }}
        
        .match-bar-container {{
            width: 100%;
            background-color: #27272a;
            height: 6px;
            border-radius: 3px;
            margin-top: 4px;
            overflow: hidden;
        }}
        
        .match-bar-fill {{
            height: 100%;
            border-radius: 3px;
        }}
        
        .match-val-text {{
            font-family: 'JetBrains Mono', monospace;
            font-weight: 600;
            color: #fff;
        }}
        
        /* Gaps analysis table */
        .comparison-table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 1.5rem;
            font-size: 0.95rem;
        }}
        
        .comparison-table th, .comparison-table td {{
            padding: 0.85rem 1rem;
            border: 1px solid var(--border-color);
        }}
        
        .comparison-table th {{
            background-color: #202024;
            color: #fff;
            font-weight: 600;
        }}
        
        .comparison-table td {{
            color: var(--text-secondary);
        }}
        
        .gap-highlight {{
            background-color: rgba(239, 68, 68, 0.05);
            color: #fca5a5 !important;
            font-weight: 500;
        }}
        
        /* List element tweaks */
        .proposal-list {{
            list-style-type: none;
        }}
        
        .proposal-list li {{
            margin-bottom: 1.5rem;
            padding-left: 1.5rem;
            position: relative;
        }}
        
        .proposal-list li::before {{
            content: "✦";
            position: absolute;
            left: 0;
            color: var(--color-primary);
        }}
        
        .proposal-list h4 {{
            color: #fff;
            margin-bottom: 0.25rem;
        }}
        
        .proposal-list p {{
            color: var(--text-secondary);
            font-size: 0.95rem;
        }}

        .radar-card-layout {{
            display: grid;
            grid-template-columns: 1.35fr 1.65fr;
            gap: 1.5rem;
            align-items: center;
        }}
        @media (max-width: 768px) {{
            .radar-card-layout {{
                grid-template-columns: 1fr;
            }}
        }}
        
    </style>
</head>
<body>

    <!-- HEADER NAVIGATION -->
    <header class="header">
        <div class="header-container">
            <div class="logo-section">
                <div class="logo-icon">☕</div>
                <div class="logo-title">Báo Cáo ĐGNL Lần 1 - Khóa KS24</div>
            </div>
            <div class="nav-tabs">
                <button class="tab-btn active" onclick="switchTab('tab-overview')">Tổng quan Năng lực</button>
                <button class="tab-btn" onclick="switchTab('tab-directory')">Tra cứu Sinh viên</button>
                <button class="tab-btn" onclick="switchTab('tab-curriculum')">Đối soát & Đề xuất</button>
            </div>
        </div>
    </header>

    <div class="container">

    <!-- KPIs -->
    <div class="kpi-container">
        <div class="kpi-card blue">
            <span class="kpi-title">Tổng số sinh viên đăng ký</span>
            <span class="kpi-value">{summary['total_students']}</span>
            <span class="kpi-desc">Danh sách đăng ký chính thức</span>
        </div>
        <div class="kpi-card blue">
            <span class="kpi-title">Số sinh viên đã dự thi</span>
            <span class="kpi-value">{summary['total_took_exam']}</span>
            <span class="kpi-desc">Có bài làm được ghi nhận</span>
        </div>
        <div class="kpi-card warning">
            <span class="kpi-title">Điểm trung bình ĐGNL</span>
            <span class="kpi-value">{summary['avg_score']} / 10</span>
            <span class="kpi-desc">Trung bình học viên đã thi</span>
        </div>
        <div class="kpi-card success">
            <span class="kpi-title">Tỷ lệ Sẵn sàng</span>
            <span class="kpi-value">{summary['placement_rate']}%</span>
            <span class="kpi-desc">Mức 2 & Mức 3 ({summary['level_counts']['level_2'] + summary['level_counts']['level_3']}/{summary['total_students']} SV)</span>
        </div>
        <div class="kpi-card danger">
            <span class="kpi-title">Tỷ lệ trượt / Chưa sẵn sàng</span>
            <span class="kpi-value">{round(summary['level_counts']['level_0'] / summary['total_students'] * 100, 1)}%</span>
            <span class="kpi-desc">Mức 0 cần đào tạo lại ({summary['level_counts']['level_0']}/{summary['total_students']} SV)</span>
        </div>
    </div>


        
        <!-- TAB 1: OVERVIEW -->
        <div id="tab-overview" class="tab-content active">
            <div class="charts-row">
                <div class="card">
                    <div class="card-title">Phân bố Điểm số ĐGNL</div>
                    <div class="chart-container">
                        <canvas id="scoreDistChart"></canvas>
                    </div>
                </div>
                <div class="card">
                    <div class="card-title">Phân bổ Mức độ Làm chủ Kiến thức</div>
                    <div class="chart-container">
                        <canvas id="readinessChart"></canvas>
                    </div>
                </div>
            </div>
            
            <div class="dashboard-grid">
                <div class="card">
                    <div class="card-title">Bản đồ Năng lực Kỹ năng Trung bình của Sinh viên</div>
                    <div class="radar-card-layout">
                        <div class="chart-container" style="height: 360px;">
                            <canvas id="skillRadarChart"></canvas>
                        </div>
                        <div>
                            <h3 style="color:#fff; margin-bottom: 0.75rem;">Đánh giá của Chuyên gia chất lượng:</h3>
                            <ul class="proposal-list" style="margin: 0; padding: 0;">
                                <li style="margin-bottom: 0.75rem; padding-left: 1.25rem;">
                                    <strong style="color: #fff;">Phân hóa học thuật:</strong> 
                                    <span>Năng lực thực tế của sinh viên KS24 phân hóa sâu sắc. Nhóm sinh viên **Làm chủ Tốt (Mức 3)** chiếm **{summary['level_counts']['level_3'] / summary['total_students'] * 100:.1f}%**, trong khi nhóm cần củng cố hoặc hỗ trợ (Mức 0 & 1) chiếm **{(summary['level_counts']['level_0'] + summary['level_counts']['level_1']) / summary['total_students'] * 100:.1f}%**.</span>
                                </li>
                                <li style="margin-bottom: 0.75rem; padding-left: 1.25rem;">
                                    <strong style="color: #fff;">Điểm nghẽn kỹ năng (Đa luồng):</strong> 
                                    <span>Chỉ số **Xử lý Đa luồng & Giao dịch** có điểm trung bình thấp nhất (**{summary['avg_skills']['concurrency']}%**). Sinh viên hầu hết gặp khó khăn trong việc thiết lập cơ chế khóa (Pessimistic/Optimistic Lock) để chống race condition và cấu hình Transaction hợp lệ.</span>
                                </li>
                                <li style="margin-bottom: 0.75rem; padding-left: 1.25rem;">
                                    <strong style="color: #fff;">Bảo mật ứng dụng:</strong> 
                                    <span>Chỉ số **An toàn & Bảo mật API** đạt trung bình **{summary['avg_skills']['security']}%**. Đa số sinh viên chưa làm chủ các lỗ hổng phân quyền tài nguyên như IDOR và duyệt thư mục trái phép Path Traversal.</span>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
                
                <div class="card">
                    <div class="card-title">Tỷ lệ Đáp ứng Vị trí Tuyển dụng 2026 (Sắp xếp theo độ tương thích)</div>
                    <div class="chart-container" style="height: 480px;">
                        <canvas id="jobMatchesChart"></canvas>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- TAB 2: STUDENT DIRECTORY -->
        <div id="tab-directory" class="tab-content">
            <div class="card">
                <div class="card-title">Danh sách kết quả chi tiết của {summary['total_students']} Sinh viên</div>
                
                <!-- Cohort Overview Cards -->
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1.5rem;">
                    <div style="background-color: #1e1b4b; border: 1px solid #312e81; padding: 1rem; border-radius: 8px;">
                        <h4 style="color: #fff; margin-bottom: 0.5rem; border-bottom: 1px solid #312e81; padding-bottom: 0.25rem;">Cơ sở Hà Nội (HN-KS24)</h4>
                        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.5rem; text-align: center; font-size: 0.85rem;">
                            <div>
                                <div style="color: var(--text-secondary); font-size: 0.8rem;">Sĩ số</div>
                                <strong style="font-size: 1.1rem; color: #fff;">{hn_registered}</strong>
                            </div>
                            <div>
                                <div style="color: var(--text-secondary); font-size: 0.8rem;">Đã thi</div>
                                <strong style="font-size: 1.1rem; color: #fff;">{hn_took}</strong>
                            </div>
                            <div>
                                <div style="color: var(--text-secondary); font-size: 0.8rem;">Điểm TB</div>
                                <strong style="font-size: 1.1rem; color: #f59e0b;">{hn_avg}/10</strong>
                            </div>
                            <div>
                                <div style="color: var(--text-secondary); font-size: 0.8rem;">Đạt chuẩn</div>
                                <strong style="font-size: 1.1rem; color: #10b981;">{hn_ready_pct}%</strong>
                            </div>
                        </div>
                        <div style="font-size: 0.75rem; color: var(--text-secondary); margin-top: 0.5rem; font-style: italic;">
                            (*) Đã tính 30% trọng số sản phẩm thực tế theo công thức chuẩn.
                        </div>
                    </div>
                    
                    <div style="background-color: #1e293b; border: 1px solid #334155; padding: 1rem; border-radius: 8px;">
                        <h4 style="color: #fff; margin-bottom: 0.5rem; border-bottom: 1px solid #334155; padding-bottom: 0.25rem;">Cơ sở TP.HCM (HCM-KS24)</h4>
                        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.5rem; text-align: center; font-size: 0.85rem;">
                            <div>
                                <div style="color: var(--text-secondary); font-size: 0.8rem;">Sĩ số</div>
                                <strong style="font-size: 1.1rem; color: #fff;">{hcm_registered}</strong>
                            </div>
                            <div>
                                <div style="color: var(--text-secondary); font-size: 0.8rem;">Đã thi</div>
                                <strong style="font-size: 1.1rem; color: #fff;">{hcm_took}</strong>
                            </div>
                            <div>
                                <div style="color: var(--text-secondary); font-size: 0.8rem;">Điểm TB</div>
                                <strong style="font-size: 1.1rem; color: #f59e0b;">{hcm_avg}/10</strong>
                            </div>
                            <div>
                                <div style="color: var(--text-secondary); font-size: 0.8rem;">Đạt chuẩn</div>
                                <strong style="font-size: 1.1rem; color: #10b981;">{hcm_ready_pct}%</strong>
                            </div>
                        </div>
                        <div style="font-size: 0.75rem; color: var(--text-secondary); margin-top: 0.5rem; font-style: italic;">
                            (*) Tính theo trọng số Vấn đáp 40% và Thực hành/Trắc nghiệm 60%.
                        </div>
                    </div>
                </div>

                <!-- Criteria Info Box -->
                <details style="background-color: #18181b; border: 1px solid var(--border-color); border-radius: 8px; margin-bottom: 1.5rem; padding: 0.75rem 1rem;">
                    <summary style="cursor: pointer; font-size: 0.95rem; font-weight: 500; color: var(--color-primary); outline: none;">
                        💡 Click để xem tiêu chí Xếp loại Năng lực & Định hướng Vai trò
                    </summary>
                    <div style="margin-top: 0.75rem; border-top: 1px solid var(--border-color); padding-top: 0.75rem; font-size: 0.85rem; line-height: 1.5; color: var(--text-secondary); display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem;">
                        <div>
                            <strong style="color: #fff; display: block; margin-bottom: 0.25rem;">Tiêu chuẩn Làm chủ Kiến thức:</strong>
                            <ul style="padding-left: 1.25rem; margin: 0;">
                                <li><strong>Mức 3 - Làm chủ Tốt:</strong> Final &ge; 8.0/10 VÀ Đa luồng &ge; 75% VÀ Bảo mật &ge; 75% (Tự giải quyết bài toán nâng cao).</li>
                                <li><strong>Mức 2 - Đạt chuẩn Đào tạo:</strong> Final &ge; 6.0/10 VÀ Đa luồng &ge; 50% VÀ Bảo mật &ge; 50%.</li>
                                <li><strong>Mức 1 - Cần bổ trợ:</strong> Final &ge; 4.0/10 VÀ Đa luồng &ge; 40% VÀ Bảo mật &ge; 40% (Cần mentor hỗ trợ).</li>
                                <li><strong>Mức 0 - Chưa đạt chuẩn:</strong> Các trường hợp còn lại hoặc hổng sâu kỹ năng lõi.</li>
                            </ul>
                        </div>
                        <div>
                            <strong style="color: #fff; display: block; margin-bottom: 0.25rem;">Tiêu chí Định hướng Vai trò:</strong>
                            <ul style="padding-left: 1.25rem; margin: 0;">
                                <li><strong>Lập trình Fullstack:</strong> Điểm ĐGNL tốt (&ge; 6.0), có dự án Frontend Git thực tế.</li>
                                <li><strong>Lập trình Backend:</strong> Điểm ĐGNL tốt (&ge; 6.0), không có dự án Frontend Git.</li>
                                <li><strong>Kiểm thử phần mềm (Tester):</strong> Kỹ năng chẩn đoán lỗi tốt (&ge; 55%), lập trình còn hạn chế (&lt; 50%).</li>
                                <li><strong>Bổ trợ nền tảng:</strong> Thuộc nhóm học thuật Mức 0, cần củng cố lập trình cơ bản.</li>
                            </ul>
                        </div>
                    </div>
                </details>
                
                <div class="filter-bar">
                    <input type="text" id="searchInput" class="search-input" placeholder="Tìm kiếm sinh viên theo tên..." onkeyup="filterStudents()">
                    <select id="levelFilter" class="select-filter" onchange="filterStudents()">
                        <option value="">Tất cả mức độ làm chủ</option>
                        <option value="3">Mức 3: Làm chủ Tốt</option>
                        <option value="2">Mức 2: Đạt chuẩn Đào tạo</option>
                        <option value="1">Mức 1: Cần bổ trợ</option>
                        <option value="0">Mức 0: Chưa đạt chuẩn</option>
                    </select>
                    <select id="caFilter" class="select-filter" onchange="filterStudents()">
                        <option value="">Tất cả ca thi</option>
                        <option value="07:00 - 09:00">Ca 07:00 - 09:00</option>
                        <option value="12:10 - 14:10">Ca 12:10 - 14:10</option>
                        <option value="14:20 - 16:20">Ca 14:20 - 16:20</option>
                    </select>
                    <button class="reset-btn" onclick="resetFilters()">Đặt lại bộ lọc</button>
                </div>
                <div id="matchCountText" style="color: var(--text-secondary); font-size: 0.9rem; margin-top: -0.5rem; margin-bottom: 1rem; font-weight: 500;">Tìm thấy {summary['total_students']} / {summary['total_students']} sinh viên</div>
                
                <div class="students-table-container">
                    <table class="students-table" id="studentsTable">
                        <thead>
                            <tr>
                                <th>STT</th>
                                <th>Họ và Tên</th>
                                <th>Điểm số</th>
                                <th>Đề bài thi</th>
                                <th>Mức độ Làm chủ Kiến thức</th>
                                <th>Định hướng Vai trò Phù hợp</th>
                                <th>Ghi chú Năng lực</th>
                            </tr>
                        </thead>
                        <tbody>
                            <!-- Generated Rows -->
    """
    
    for idx, s in enumerate(students_sorted):
        lvl = s['readiness_level']
        lvl_class = f"lvl-{lvl}"
        backend_val = s['job_matches']['backend_dev']
        qa_val = s['job_matches']['api_qa']
        fullstack_val = s['job_matches']['fullstack_dev']
        
        # Color codes for progress bars
        def get_bar_color(val):
            if val >= 80: return "var(--color-success)"
            if val >= 60: return "var(--color-primary)"
            if val >= 40: return "var(--color-warning)"
            return "var(--color-danger)"
            
        backend_color = get_bar_color(backend_val)
        qa_color = get_bar_color(qa_val)
        fullstack_color = get_bar_color(fullstack_val)
        
        failed_skills_str = ", ".join(s['failed_skills']) if s['failed_skills'] else "Không bị phát hiện hổng kỹ năng cốt lõi"
        
        # Safe escape criteria text
        crit_escaped = s.get('criteria_text', '')
        if not crit_escaped:
            crit_escaped = f"Chi tiết kỹ năng:\n- Bug Hunting: {s['bug_hunting']}%\n- Coding & Sửa lỗi: {s['coding']}%\n- Tư duy hệ thống: {s['system_thinking']}%\n- Concurrency/Giao dịch: {s['concurrency']}%\n- Bảo mật API: {s['security']}%"
            
        html_content += f"""
                            <tr class="student-row" onclick="toggleDetails({idx})" data-name="{s['name'].lower()}" data-level="{lvl}" data-ca="{s['ca_thi']}">
                                <td>{idx+1}</td>
                                <td style="font-weight: 500; color: #fff;">{s['name']}</td>
                                <td class="match-val-text">{s['score']}/10</td>
                                <td style="font-size: 0.85rem;">{s['topic']}</td>
                                <td><span class="lvl-badge {lvl_class}">{s['readiness_label'].split(" (")[0]}</span></td>
                                <td style="font-weight: 600; color: #fff; font-size: 0.9rem;">{s['career_orientation']}</td>
                                <td style="font-size: 0.85rem; color: var(--text-secondary);">{s['career_note']}</td>
                            </tr>
                            <tr class="detail-row" id="detail-{idx}">
                                <td colspan="7">
                                    <div class="student-details-box">
                                        <h4 style="margin-bottom: 0.5rem;">Chi tiết năng lực của {s['name']}</h4>
                                        <div class="skills-grid">
                                            <div class="skill-item">
                                                <div class="skill-item-title">Chẩn đoán & Phát hiện lỗi</div>
                                                <div class="skill-item-val">{s['bug_hunting']}%</div>
                                            </div>
                                            <div class="skill-item">
                                                <div class="skill-item-val-desc" style="display:none"></div>
                                                <div class="skill-item-title">Lập trình & Tối ưu code</div>
                                                <div class="skill-item-val">{s['coding']}%</div>
                                            </div>
                                            <div class="skill-item">
                                                <div class="skill-item-title">Xử lý Đa luồng & Giao dịch</div>
                                                <div class="skill-item-val">{s['concurrency']}%</div>
                                            </div>
                                            <div class="skill-item">
                                                <div class="skill-item-title">An toàn & Bảo mật API</div>
                                                <div class="skill-item-val">{s['security']}%</div>
                                            </div>
                                            <div class="skill-item">
                                                <div class="skill-item-title">Kiến trúc & Phân tích hệ thống</div>
                                                <div class="skill-item-val">{s['sys_think']}%</div>
                                            </div>
                                        </div>
                                        <p class="student-fail-skills"><strong>Kỹ năng bị hổng/yếu cần bổ trợ:</strong> {failed_skills_str}</p>
                                        <div class="student-crit-text"><strong>Chi tiết kết quả đánh giá chi tiết:</strong><br>{crit_escaped}</div>
                                        
                                        <div class="job-compatibility-details" style="margin-top: 1rem; border-top: 1px solid #27272a; padding-top: 0.75rem; margin-bottom: 0.75rem;">
                                            <h5 style="margin-bottom: 0.5rem; color: #fff; font-size: 0.9rem;">Độ tương thích & Khả năng đảm nhận Vị trí Tuyển dụng:</h5>
                                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; font-size: 0.82rem; color: var(--text-secondary);">
                                                <div>Java Backend: <strong style="color:#fff;">{s['job_matches']['backend_dev']}%</strong> ({s['job_tiers']['backend_dev'].replace('level_3', 'Phù hợp cao').replace('level_2', 'Khá phù hợp').replace('level_1', 'Tiềm năng').replace('level_0', 'Chưa phù hợp')})</div>
                                                <div>React Frontend: <strong style="color:#fff;">{s['job_matches']['frontend_dev']}%</strong> ({s['job_tiers']['frontend_dev'].replace('level_3', 'Phù hợp cao').replace('level_2', 'Khá phù hợp').replace('level_1', 'Tiềm năng').replace('level_0', 'Chưa phù hợp')})</div>
                                                <div>Fullstack Java-React: <strong style="color:#fff;">{s['job_matches']['fullstack_dev']}%</strong> ({s['job_tiers']['fullstack_dev'].replace('level_3', 'Phù hợp cao').replace('level_2', 'Khá phù hợp').replace('level_1', 'Tiềm năng').replace('level_0', 'Chưa phù hợp')})</div>
                                                <div>Python (Backend/AI): <strong style="color:#fff;">{s['job_matches']['python_dev']}%</strong> ({s['job_tiers']['python_dev'].replace('level_3', 'Phù hợp cao').replace('level_2', 'Khá phù hợp').replace('level_1', 'Tiềm năng').replace('level_0', 'Chưa phù hợp')})</div>
                                                <div>API Tester / QA: <strong style="color:#fff;">{s['job_matches']['api_qa']}%</strong> ({s['job_tiers']['api_qa'].replace('level_3', 'Phù hợp cao').replace('level_2', 'Khá phù hợp').replace('level_1', 'Tiềm năng').replace('level_0', 'Chưa phù hợp')})</div>
                                                <div>DevOps: <strong style="color:#fff;">{s['job_matches']['devops']}%</strong> ({s['job_tiers']['devops'].replace('level_3', 'Phù hợp cao').replace('level_2', 'Khá phù hợp').replace('level_1', 'Tiềm năng').replace('level_0', 'Chưa phù hợp')})</div>
                                                <div>Data Analyst: <strong style="color:#fff;">{s['job_matches']['data_analyst']}%</strong> ({s['job_tiers']['data_analyst'].replace('level_3', 'Phù hợp cao').replace('level_2', 'Khá phù hợp').replace('level_1', 'Tiềm năng').replace('level_0', 'Chưa phù hợp')})</div>
                                                <div>Tích hợp AI: <strong style="color:#fff;">{s['job_matches']['ai_integration']}%</strong> ({s['job_tiers']['ai_integration'].replace('level_3', 'Phù hợp cao').replace('level_2', 'Khá phù hợp').replace('level_1', 'Tiềm năng').replace('level_0', 'Chưa phù hợp')})</div>
                                                <div>Business Analyst (BA): <strong style="color:#fff;">{s['job_matches']['business_analyst']}%</strong> ({s['job_tiers']['business_analyst'].replace('level_3', 'Phù hợp cao').replace('level_2', 'Khá phù hợp').replace('level_1', 'Tiềm năng').replace('level_0', 'Chưa phù hợp')})</div>
                                                <div>Mobile (Flutter/Android): <strong style="color:#fff;">{s['job_matches']['mobile_dev']}%</strong> ({s['job_tiers']['mobile_dev'].replace('level_3', 'Phù hợp cao').replace('level_2', 'Khá phù hợp').replace('level_1', 'Tiềm năng').replace('level_0', 'Chưa phù hợp')})</div>
                                            </div>
                                        </div>
                                        
                                        <div style="margin-top: 0.75rem; font-size: 0.85rem;">
                                            <strong>Dự án Git cá nhân:</strong> <a href="{s['git_link']}" target="_blank">{s['git_link']}</a>
                                        </div>
                                    </div>
                                </td>
                            </tr>
        """
        
    html_content += f"""
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        
        <!-- TAB 3: CURRICULUM GAP & PROPOSALS -->\n                <div id="tab-curriculum" class="tab-content">\n                    <!-- Unified Quality Evaluation Card (KS24) -->\n                    <div class="card" style="margin-bottom: 2rem;">\n                        <div class="card-title">Phân tích & Đánh giá chất lượng đề thi ĐGNL (KS24)</div>\n                        <div style="color: var(--text-secondary); font-size: 0.9rem; margin-bottom: 1rem; line-height: 1.5;">\n                            📊 Báo cáo đánh giá chất lượng đề thi ĐGNL Lần 1 (bao gồm Trắc nghiệm & Tự luận/Thực hành) dựa trên đối chiếu học thuật trực tiếp với nội dung chương trình ôn tập hè của học viên khóa KS24.\n                        </div>\n\n                        <!-- Overall Suitability Progress Bar -->\n                        <div style="margin-top: 1.25rem; margin-bottom: 2rem; display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; background: rgba(255,255,255,0.01); padding: 1.25rem 1.5rem; border-radius: 6px; border: 1px solid var(--border-color);">\n                            <!-- Indicator 1 -->\n                            <div>\n                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">\n                                    <strong style="color: #fff; font-size: 0.9rem;">1. Độ phù hợp giữa Đề thi & Nội dung ôn tập:</strong>\n                                    <span style="font-size: 1.15rem; font-weight: 700; color: var(--color-success);">90% (Rất cao - Chuẩn học thuật)</span>\n                                </div>\n                                <div style="background: rgba(255,255,255,0.1); height: 8px; border-radius: 4px; overflow: hidden;">\n                                    <div style="background: var(--color-success); width: 90%; height: 100%; border-radius: 4px;"></div>\n                                </div>\n                                <div style="font-size: 0.78rem; color: var(--text-secondary); margin-top: 0.5rem; line-height: 1.4;">\n                                    ✔️ Đề thi bám sát 90% nội dung ôn tập lý thuyết & logic thực hành về Spring Boot và ReactJS. Các lỗi nghiệp vụ là điển hình trong phát triển thực tế.\n                                </div>\n                            </div>\n                            <!-- Indicator 2 -->\n                            <div>\n                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">\n                                    <strong style="color: #fff; font-size: 0.9rem;">2. Độ phù hợp giữa Đề thi & Năng lực thực tế SV:</strong>\n                                    <span style="font-size: 1.15rem; font-weight: 700; color: var(--color-warning);">70% (Trung bình - Khá)</span>\n                                </div>\n                                <div style="background: rgba(255,255,255,0.1); height: 8px; border-radius: 4px; overflow: hidden;">\n                                    <div style="background: var(--color-warning); width: 70%; height: 100%; border-radius: 4px;"></div>\n                                </div>\n                                <div style="font-size: 0.78rem; color: var(--text-secondary); margin-top: 0.5rem; line-height: 1.4;">\n                                    ⚠️ Học viên KS24 có phản xạ code tốt hơn KS25 (đã qua Kỳ III). Tuy nhiên, tỷ lệ yếu ở Đa luồng (53.8%) và Bảo mật (54%) phản ánh khả năng tự rà soát lỗi logic code vẫn cần củng cố.\n                                </div>\n                            </div>\n                        </div>\n\n                        <div class="metrics-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1.5rem; margin-bottom: 2rem;">\n                            <div class="metric-card" style="background: rgba(255,255,255,0.02); border: 1px solid var(--border-color); padding: 1rem 1.25rem; border-radius: 6px;">\n                                <div class="metric-label" style="color: var(--text-secondary); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.25rem;">Học viên dự thi</div>\n                                <div class="metric-value" style="font-size: 1.8rem; font-weight: 700; font-family: 'Outfit', sans-serif;">{mcq_count}</div>\n                                <div class="metric-trend" style="color: var(--text-secondary); font-size: 0.75rem; margin-top: 0.25rem;">Hệ CNTT Khóa KS24</div>\n                            </div>\n                            <div class="metric-card" style="background: rgba(255,255,255,0.02); border: 1px solid var(--border-color); padding: 1rem 1.25rem; border-radius: 6px;">\n                                <div class="metric-label" style="color: var(--text-secondary); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.25rem;">Điểm trung bình trắc nghiệm</div>\n                                <div class="metric-value" style="font-size: 1.8rem; font-weight: 700; font-family: 'Outfit', sans-serif; color: var(--color-primary);">{mcq_avg:.2f} <span style="font-size: 1.1rem; font-weight: normal; color: var(--text-secondary);">/ 100</span></div>\n                                <div class="metric-trend" style="color: var(--color-success); font-size: 0.75rem; margin-top: 0.25rem;">➔ Mức Khá - Giỏi</div>\n                            </div>\n                            <div class="metric-card" style="background: rgba(255,255,255,0.02); border: 1px solid var(--border-color); padding: 1rem 1.25rem; border-radius: 6px;">\n                                <div class="metric-label" style="color: var(--text-secondary); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.25rem;">Độ lệch chuẩn (Std Dev)</div>\n                                <div class="metric-value" style="font-size: 1.8rem; font-weight: 700; font-family: 'Outfit', sans-serif; color: var(--color-purple);">{mcq_std:.2f}</div>\n                                <div class="metric-trend" style="color: var(--color-success); font-size: 0.75rem; margin-top: 0.25rem;">➔ Độ phân hóa Cao (Tốt)</div>\n                            </div>\n                        </div>\n\n                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2.5rem; align-items: start; margin-bottom: 1.5rem;">\n                            <div>\n                                <h4 style="color: #fff; font-size: 0.95rem; margin-bottom: 1rem; border-left: 3px solid var(--color-purple); padding-left: 0.5rem;">1. Thống kê & Nhận xét Đề Trắc nghiệm (MCQ) - Phù hợp 90%</h4>\n                                <table class="comparison-table" style="font-size: 0.88rem; width: 100%; margin-bottom: 1.25rem;">\n                                    <thead>\n                                        <tr>\n                                            <th>Dải điểm (Thang 100)</th>\n                                            <th>Số lượng SV</th>\n                                            <th>Tỷ lệ (%)</th>\n                                        </tr>\n                                    </thead>\n                                    <tbody>\n                                        <tr>\n                                            <td><strong>90 - 100 (Xuất sắc)</strong></td>\n                                            <td>{exc_cnt}</td>\n                                            <td><span class="badge" style="background-color: rgba(16, 185, 129, 0.1); color: var(--color-success); padding: 2px 6px; border-radius: 4px;">{exc_pct}%</span></td>\n                                        </tr>\n                                        <tr>\n                                            <td><strong>80 - 89 (Giỏi)</strong></td>\n                                            <td>{vg_cnt}</td>\n                                            <td><span class="badge" style="background-color: rgba(59, 130, 246, 0.1); color: var(--color-primary); padding: 2px 6px; border-radius: 4px;">{vg_pct}%</span></td>\n                                        </tr>\n                                        <tr>\n                                            <td><strong>70 - 79 (Khá)</strong></td>\n                                            <td>{g_cnt}</td>\n                                            <td><span class="badge" style="background-color: rgba(139, 92, 246, 0.1); color: var(--color-purple); padding: 2px 6px; border-radius: 4px;">{g_pct}%</span></td>\n                                        </tr>\n                                        <tr>\n                                            <td><strong>50 - 69 (Trung bình)</strong></td>\n                                            <td>{avg_cnt}</td>\n                                            <td><span class="badge" style="background-color: rgba(245, 158, 11, 0.1); color: var(--color-warning); padding: 2px 6px; border-radius: 4px;">{avg_pct}%</span></td>\n                                        </tr>\n                                        <tr>\n                                            <td><strong>&lt; 50 (Yếu kém)</strong></td>\n                                            <td>{fail_cnt}</td>\n                                            <td><span class="badge" style="background-color: rgba(239, 68, 68, 0.1); color: var(--color-danger); padding: 2px 6px; border-radius: 4px;">{fail_pct}%</span></td>\n                                        </tr>\n                                    </tbody>\n                                </table>\n                                <div style="background-color: rgba(139, 92, 246, 0.03); border: 1px solid rgba(139, 92, 246, 0.08); padding: 1rem; border-radius: 6px; font-size: 0.85rem; color: var(--text-secondary); line-height: 1.5;">\n                                    <strong>Nhận xét chất lượng:</strong> Độ lệch chuẩn lý thuyết của học viên đạt {mcq_std:.2f} phản ánh độ phân hóa điểm số tự nhiên và rất tốt. Học viên KS24 đạt điểm trung bình trắc nghiệm khá tốt (72.57) và tỷ lệ yếu kém rất thấp (chỉ 4.3%), chứng tỏ nội dung thi trắc nghiệm bao phủ và bám sát chính xác các lý thuyết cơ bản đã được ôn tập hè (Spring annotations, React Hooks, Scrum).\n                                </div>\n                            </div>\n                            <div>\n                                <h4 style="color: #fff; font-size: 0.95rem; margin-bottom: 1rem; border-left: 3px solid var(--color-primary); padding-left: 0.5rem;">2. Đối soát & Nhận định Đề Tự luận (Thực hành) - Phù hợp 90%</h4>\n                                <div style="background-color: rgba(59, 130, 246, 0.03); border: 1px solid rgba(59, 130, 246, 0.08); padding: 1rem; border-radius: 6px; font-size: 0.85rem; color: var(--text-secondary); line-height: 1.55;">\n                                    <ul style="padding-left: 1.2rem; margin: 0; list-style-type: disc;">\n                                        <li style="margin-bottom: 0.75rem;">\n                                            <strong style="color: #fff;">Giao dịch & Đồng thời (Phù hợp 90%):</strong> Đề thi thực tế chỉ yêu cầu học viên rà soát lỗi thiếu annotation <code>@Transactional</code> và race condition cơ bản khi trừ kho hoặc đặt ghế, đề xuất giải pháp synchronized hoặc lock. Đây hoàn toàn là lý thuyết transaction cơ bản đã học trong ôn tập hè (ACID, propagation, isolation). Đề thi không đòi hỏi sinh viên code các kỹ năng phức tạp ngoài phạm vi.\n                                        </li>\n                                        <li style="margin-bottom: 0.75rem;">\n                                            <strong style="color: #fff;">Bảo mật API & Validations (Phù hợp 90%):</strong> Đề thi kiểm tra các lỗi logic web cơ bản: (1) tin tưởng tham số giá tiền do client truyền lên mà không truy vấn DB để kiểm tra, (2) thiếu kiểm tra quyền sở hữu bản ghi (patientId không khớp prescriptionId). Đây là các lỗ hổng phân quyền/validation căn bản của Spring Boot đã được dạy, đề thi không đòi hỏi cấu hình Security ngoài chương trình.\n                                        </li>\n                                        <li>\n                                            <strong style="color: #fff;">Tư duy Thiết kế Hệ thống (Phù hợp 90%):</strong> Đề thi tự luận câu 3 hỏi về giải pháp tối ưu hệ thống dưới tải lớn (suất chiếu phim hot / chuyển tiền trùng). Học viên chỉ cần vận dụng các lý thuyết scalability đã học trong ôn tập hè (như Caching và DB Indexing) để trả lời.\n                                        </li>\n                                    </ul>\n                                </div>\n                            </div>\n                        </div>\n\n                        <div style="margin-top: 1.5rem; background-color: rgba(16, 185, 129, 0.03); border: 1px solid rgba(16, 185, 129, 0.08); padding: 1.25rem; border-radius: 6px; font-size: 0.88rem; line-height: 1.6; color: var(--text-secondary);">\n                            💡 <strong style="color: #fff;">Kết luận chất lượng đề thi từ Ban chuyên môn:</strong> Đề thi ĐGNL Lần 1 hoàn toàn đảm bảo chất lượng, bám sát và có độ phù hợp rất cao (90%) với nội dung đào tạo của Rikkei Education. Các bài toán đưa ra trong đề thi là những lỗi logic nghiệp vụ Spring Boot điển hình mà một lập trình viên bắt buộc phải nắm được. Việc sinh viên trượt nhiều ở phần thực hành bộc lộ điểm yếu trong khả năng tự rà soát lỗi (code auditing) và chuyển dịch lý thuyết thành code thực tế của sinh viên, chứ không phải do đề thi vượt quá phạm vi ôn tập.\n                        </div>\n                    </div>\n                </div> <!-- Close tab-curriculum -->\n            </div> <!-- Close container -->\n            <div class="card" style="margin-bottom: 2rem;">
                <div class="card-title">Đề xuất cải tiến Chương trình Đào tạo cho Kỳ IV & Kỳ V</div>
                
                <!-- Section 1: Nhận xét về chương trình học KS24 -->
                <div style="margin-bottom: 2rem;">
                    <h3 style="color: #fff; border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem; margin-bottom: 0.75rem; font-size: 1.05rem; display: flex; align-items: center; gap: 0.5rem;">
                        <span style="color: var(--color-primary);">1.</span> Nhận xét chương trình học KS24 (Qua số liệu trượt môn Kỳ III)
                    </h3>
                    <p style="color: var(--text-secondary); line-height: 1.6; font-size: 0.9rem; margin-bottom: 0.75rem;">
                        Học kỳ III ghi nhận tỷ lệ trượt môn cao đột biến, tạo thành nút cổ chai nhận thức lớn: 
                        <strong>70 SV trượt Java Advanced</strong>, 
                        <strong>46 SV trượt Java Web App</strong>, và 
                        <strong>42 SV trượt Java Web Service</strong>.
                    </p>
                    <div style="background-color: rgba(239, 68, 68, 0.06); border-left: 4px solid var(--color-danger); padding: 0.75rem 1rem; border-radius: 4px; font-size: 0.85rem; color: #f87171; line-height: 1.5;">
                        <strong>Cảnh báo sư phạm:</strong> Mặc dù chương trình đào tạo chính thức (PM) thiết kế rất bài bản các công nghệ phân tán (Saga, Kafka, API Gateway...) ở Kỳ IV, việc gần 40% sinh viên bị hổng nền tảng Java Web ở Kỳ III sẽ làm họ gặp cực kỳ nhiều khó khăn khi bắt tay vào cấu hình các hệ thống phức tạp này. Cần có giải pháp củng cố gấp ở đầu kỳ IV.
                    </div>
                </div>

                <!-- Section 2: Đánh giá về năng lực chung sinh viên sau đợt ĐGNL -->
                <div style="margin-bottom: 2rem;">
                    <h3 style="color: #fff; border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem; margin-bottom: 0.75rem; font-size: 1.05rem; display: flex; align-items: center; gap: 0.5rem;">
                        <span style="color: var(--color-primary);">2.</span> Đánh giá Năng lực Sinh viên sau ĐGNL & Khả năng Đảm nhận Công việc
                    </h3>
                    <p style="color: var(--text-secondary); line-height: 1.6; font-size: 0.9rem; margin-bottom: 0.75rem;">
                        Kết quả kỳ thi ĐGNL Lần 1 ({hn_took + hcm_took} SV dự thi) phản ánh rõ rệt khoảng trống kỹ năng này:
                    </p>
                    <ul class="proposal-list" style="padding-left: 1.25rem; font-size: 0.88rem; line-height: 1.6; color: var(--text-secondary); margin: 0;">
                        <li style="margin-bottom: 0.5rem;">
                            <strong style="color:#fff;">Phân bổ năng lực:</strong> Chỉ <strong>{summary['level_counts']['level_3'] / summary['total_students'] * 100:.1f}%</strong> đạt Mức 3 (Làm chủ tốt), trong khi <strong>{(summary['level_counts']['level_0'] + summary['level_counts']['level_1']) / summary['total_students'] * 100:.1f}%</strong> ở Mức 0 & 1 (cần hỗ trợ/đào tạo lại).
                        </li>
                        <li style="margin-bottom: 0.5rem;">
                            <strong style="color:#fff;">Lỗ hổng cốt lõi:</strong> Hổng sâu ở <strong>Xử lý Đa luồng & Giao dịch</strong> (53.8% trượt tiêu chí) và <strong>An toàn & Bảo mật API</strong> (54.0% trượt tiêu chí - đặc biệt là lỗi IDOR và tin tưởng tham số từ Client).
                        </li>
                        <li style="margin-bottom: 0.5rem;">
                            <strong style="color:#fff;">Khả năng đáp ứng vai trò công việc:</strong>
                            <ul style="padding-left: 1.25rem; margin-top: 0.25rem; list-style-type: circle;">
                                <li><strong>Lập trình Fullstack (React + Spring Boot):</strong> Chỉ khoảng <strong>25%</strong> sinh viên đáp ứng (đòi hỏi có sản phẩm Git/React Frontend và điểm tốt).</li>
                                <li><strong>Lập trình Backend:</strong> Khoảng <strong>45%</strong> sinh viên (gồm cả nhóm đạt chuẩn và nhóm cần kèm cặp thêm do yếu đa luồng/bảo mật).</li>
                                <li><strong>Kiểm thử phần mềm (QA/Tester):</strong> Khoảng <strong>20%</strong> sinh viên (thế mạnh chẩn đoán lỗi nhưng viết code mới yếu).</li>
                                <li><strong>Bổ trợ nền tảng (Mức 0):</strong> Khoảng <strong>10%</strong> sinh viên mất gốc hoàn toàn, chưa thể giao việc.</li>
                            </ul>
                        </li>
                    </ul>
                </div>

                <!-- Section 3: Đề xuất chi tiết về phần Chương trình đào tạo Kỳ IV & Kỳ V -->
                <div>
                    <h3 style="color: #fff; border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem; margin-bottom: 0.75rem; font-size: 1.05rem; display: flex; align-items: center; gap: 0.5rem;">
                        <span style="color: var(--color-primary);">3.</span> Đề xuất Điều chỉnh Chương trình Đào tạo tiếp theo (Kỳ IV & Kỳ V)
                    </h3>
                    
                    <!-- Bullet points nhận xét PM ngắn gọn -->
                    <div style="margin-bottom: 1.5rem;">
                        <strong style="color: #fff; font-size: 0.92rem;">Ghi nhận về khung PM hiện tại (Thiết kế bài bản của Ban Đào tạo):</strong>
                        <ul style="padding-left: 1.25rem; font-size: 0.88rem; color: var(--text-secondary); line-height: 1.6; margin-top: 0.4rem; margin-bottom: 0;">
                            <li><strong>Microservices (IT214):</strong> Đầy đủ công nghệ phân tán hiện đại (Saga, Kafka, API Gateway, Eureka, Resilience4j, Spring Cache/Redis).</li>
                            <li><strong>DevOps (IT209):</strong> Lộ trình bài bản từ VPS hosting, Nginx, Linux CLI, Docker/Docker Compose đến GitHub Actions CI/CD.</li>
                            <li><strong>AI Integration (IT213):</strong> Rất đón đầu xu hướng với Spring AI, pgvector RAG, Function Calling, AI Agent, Langfuse, và MCP.</li>
                        </ul>
                    </div>

                    <div style="background-color: rgba(59, 130, 246, 0.05); border: 1px solid rgba(59, 130, 246, 0.15); padding: 0.75rem 1rem; border-radius: 6px; font-size: 0.85rem; color: #93c5fd; line-height: 1.5; margin-bottom: 1.5rem;">
                        💡 <strong>Nguyên tắc đề xuất:</strong> Các phần bổ sung dưới đây được thiết kế <strong>trực tiếp dựa trên các thiếu sót cốt lõi của sinh viên trong đợt ĐGNL Lần 1</strong> (như việc thiếu kỹ năng khóa concurrency, hổng bảo mật IDOR/Input validation, và lỗi nghẽn RAM/bộ nhớ). Đồng thời, đề xuất sử dụng <strong>các công nghệ mới nhất đón đầu xu hướng hiện nay</strong> thay vì các công nghệ cũ.
                    </div>

                    <div style="margin-bottom: 1.5rem;">
                        <h4 style="color: var(--color-primary); font-size: 0.95rem; margin-bottom: 0.5rem;">A. Nội dung đề xuất bổ sung vào các môn học hiện hành (Chưa có trong PM):</h4>
                        <ul class="proposal-list" style="padding-left: 1.25rem; font-size: 0.88rem; line-height: 1.6; color: var(--text-secondary); margin: 0;">
                            <li style="margin-bottom: 0.75rem;">
                                <strong style="color:#fff;">Môn Thiết kế Hệ thống Microservices (IT214-K24):</strong><br>
                                - <strong>[BỔ SUNG] Bridge Module (Cầu nối - 2 buổi đầu):</strong> Dạy phụ đạo củng cố giao dịch <code>@Transactional</code> monolithic và cơ chế khóa đồng thời (<strong>Pessimistic/Optimistic Lock</strong>) trong JPA để chống race condition.<br>
                                - <strong>[BỔ SUNG] OAuth2 Token Propagation:</strong> Cấu hình Feign Client RequestInterceptor truyền JWT token qua API Gateway xuống các downstream service nhằm ngăn chặn lỗ hổng IDOR.<br>
                                - <strong>[BỔ SUNG] Modern Distributed Tracing:</strong> Tích hợp <strong>Micrometer Tracing + OpenTelemetry (OTel) + Grafana Tempo / Jaeger</strong> (chuẩn hiện đại nhất cho Spring Boot 3+) để thay thế cho Spring Cloud Sleuth đã lỗi thời.<br>
                                - <em>Lưu ý về Docker:</em> Không dạy lại Docker Compose trong môn này vì PM DevOps Session 9 đã thiết kế bài bản, giảng viên chỉ hướng dẫn học sinh tái sử dụng.
                            </li>
                            <li style="margin-bottom: 0.75rem;">
                                <strong style="color:#fff;">Môn DevOps Fundamentals (IT209-K24):</strong><br>
                                - <strong>[BỔ SUNG] Lightweight DevSecOps Pipeline:</strong> Tích hợp các tool quét lỗ hổng bảo mật tĩnh hiện đại, nhanh gọn như <strong>Semgrep hoặc Snyk</strong> (chạy trực tiếp trong GitHub Actions) thay vì setup SonarQube server cồng kềnh cho các dự án vừa/nhỏ.<br>
                                - <strong>[BỔ SUNG] Lightweight Observability Stack (PLG Stack):</strong> Setup <strong>Prometheus + Loki + Promtail + Grafana</strong> để theo dõi tài nguyên RAM/CPU và log của VPS. Đây là xu hướng hiện đại thay thế cho ELK Stack rất nặng, dễ gây lỗi Out of Memory (OOM) trên VPS cấu hình thấp.<br>
                                - <strong>[BỔ SUNG] Database Migration:</strong> Sử dụng Flyway hoặc Liquibase tích hợp trong pipeline để tự động hóa cập nhật schema DB.
                            </li>
                            <li style="margin-bottom: 0.5rem;">
                                <strong style="color:#fff;">Môn AI Integration in Action (IT213-K24):</strong><br>
                                - <strong>[BỔ SUNG] Semantic Caching with Redis VL:</strong> Sử dụng thư viện vector chuyên dụng của Redis (RedisVL) hoặc GPTCache để cache các câu trả lời LLM tương đồng nhằm tối ưu chi phí API LLM và tăng tốc phản hồi.<br>
                                - <strong>[BỔ SUNG] Advanced AI Agents:</strong> Xây dựng các AI Agent dạng đồ thị đa tác vụ sử dụng <strong>LangGraph / CrewAI</strong> (xu hướng mới thay thế cho LangChain Chain tuần tự cũ).<br>
                                - <strong>[BỔ SUNG] Server-Sent Events (SSE) / Streaming:</strong> Cấu hình endpoint trả kết quả AI dạng stream về ReactJS để tránh nghẽn RAM khi tạo câu trả lời dài và nâng cao trải nghiệm UI.
                            </li>
                        </ul>
                    </div>

                    <div>
                        <h4 style="color: var(--color-primary); font-size: 0.95rem; margin-bottom: 0.5rem;">B. Bổ sung các môn học tự chọn mới để mở rộng vị trí việc làm (Kỳ V):</h4>
                        <ul class="proposal-list" style="padding-left: 1.25rem; font-size: 0.88rem; line-height: 1.6; color: var(--text-secondary); margin: 0;">
                            <li style="margin-bottom: 0.75rem;">
                                <strong style="color:#fff;">Python & Data Engineering / Analytics Fundamentals (Môn tự chọn mới):</strong><br>
                                Cung cấp nền tảng xử lý dữ liệu bằng Python (Pandas/SQL) kết hợp trực quan hóa bằng PowerBI.<br>
                                <span style="color: var(--color-success); font-weight: 500;">➔ Mục tiêu: Mở rộng cơ hội việc làm sang hướng Data Analyst, BI Developer cho học viên không chuyên sâu backend.</span>
                            </li>
                            <li style="margin-bottom: 0.5rem;">
                                <strong style="color:#fff;">Cloud Native & Kubernetes Scaling (Môn tự chọn mới):</strong><br>
                                Dành cho nhóm khá/giỏi học sâu về hạ tầng Cloud (AWS EC2, S3, RDS, IAM) và điều phối Kubernetes (K8s).<br>
                                <span style="color: var(--color-success); font-weight: 500;">➔ Mục tiêu: Đào tạo hướng Kỹ sư Cloud (Cloud Engineer), DevOps/SRE chuyên nghiệp.</span>
                            </li>
                        </ul>
                    </div>
                </div>
        </div>
        
    </div>

    <!-- Charts Initialization Script -->
    <script>
        // Tab switching logic
        function switchTab(tabId) {{
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
            
            document.getElementById(tabId).classList.add('active');
            
            const btnIdx = tabId === 'tab-overview' ? 0 : (tabId === 'tab-directory' ? 1 : 2);
            document.querySelectorAll('.tab-btn')[btnIdx].classList.add('active');
        }}

        // Expand details table row
        function toggleDetails(index) {{
            var row = document.getElementById("detail-" + index);
            var parent = row.previousElementSibling;
            if (row.classList.contains("active")) {{
                row.classList.remove("active");
                parent.classList.remove("active-row");
            }} else {{
                // Close other details rows first
                var activeRows = document.getElementsByClassName("detail-row");
                for (var i = 0; i < activeRows.length; i++) {{
                    activeRows[i].classList.remove("active");
                    activeRows[i].previousElementSibling.classList.remove("active-row");
                }}
                row.classList.add("active");
                parent.classList.add("active-row");
            }}
        }}

        // Filter students directory search table
        function filterStudents() {{
            var input, filterName, selectLevel, selectCa, table, tr, tdName, tdLvl, tdCa, i, txtValue;
            input = document.getElementById("searchInput");
            filterName = input.value.toLowerCase();
            selectLevel = document.getElementById("levelFilter").value;
            selectCa = document.getElementById("caFilter").value;
            
            table = document.getElementById("studentsTable");
            tr = table.getElementsByClassName("student-row");
            
            var matchCount = 0;
            for (i = 0; i < tr.length; i++) {{
                var row = tr[i];
                var nameAttr = row.getAttribute("data-name");
                var lvlAttr = row.getAttribute("data-level");
                var caAttr = row.getAttribute("data-ca");
                
                var show = true;
                
                if (filterName && nameAttr.indexOf(filterName) === -1) {{
                    show = false;
                }}
                if (selectLevel !== "" && lvlAttr !== selectLevel) {{
                    show = false;
                }}
                if (selectCa !== "" && caAttr !== selectCa) {{
                    show = false;
                }}
                
                if (show) {{
                    row.style.display = "";
                    matchCount++;
                }} else {{
                    row.style.display = "none";
                    // Close expanded details row if parent is hidden
                    var detailRow = document.getElementById("detail-" + i);
                    detailRow.classList.remove("active");
                    row.classList.remove("active-row");
                }}
            }}
            document.getElementById("matchCountText").innerText = "Tìm thấy " + matchCount + " / " + tr.length + " sinh viên";
        }}

        // Reset all filters
        function resetFilters() {{
            document.getElementById("searchInput").value = "";
            document.getElementById("levelFilter").value = "";
            document.getElementById("caFilter").value = "";
            filterStudents();
        }}

        // Load Chart.js Visualizations
        window.onload = function() {{
            
            // Chart 1: Score Distribution (Bimodal)
            var ctx1 = document.getElementById('scoreDistChart').getContext('2d');
            new Chart(ctx1, {{
                type: 'bar',
                data: {{
                    labels: {json.dumps(chart1_labels)},
                    datasets: [{{
                        label: 'Số lượng sinh viên',
                        data: {chart1_data},
                        backgroundColor: function(context) {{
                            var index = context.dataIndex;
                            if (index <= 1) return 'rgba(239, 68, 68, 0.7)'; // Red for fails
                            if (index <= 3) return 'rgba(245, 158, 11, 0.7)'; // Amber for borderline
                            if (index <= 5) return 'rgba(59, 130, 246, 0.7)'; // Blue for good
                            return 'rgba(16, 185, 129, 0.7)'; // Emerald for excellent
                        }},
                        borderColor: '#27272a',
                        borderWidth: 1,
                        borderRadius: 6
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{ display: false }}
                    }},
                    scales: {{
                        y: {{
                            grid: {{ color: '#27272a' }},
                            ticks: {{ color: '#a1a1aa' }}
                        }},
                        x: {{
                            ticks: {{ color: '#a1a1aa' }}
                        }}
                    }}
                }}
            }});

            // Chart 2: Readiness Levels (Doughnut)
            var ctx2 = document.getElementById('readinessChart').getContext('2d');
            new Chart(ctx2, {{
                type: 'doughnut',
                data: {{
                    labels: ['Mức 0: Chưa đạt chuẩn', 'Mức 1: Cần bổ trợ', 'Mức 2: Đạt chuẩn Đào tạo', 'Mức 3: Làm chủ Tốt'],
                    datasets: [{{
                        data: [
                            {summary['level_counts']['level_0']},
                            {summary['level_counts']['level_1']},
                            {summary['level_counts']['level_2']},
                            {summary['level_counts']['level_3']}
                        ],
                        backgroundColor: [
                            'rgba(239, 68, 68, 0.75)',
                            'rgba(245, 158, 11, 0.75)',
                            'rgba(99, 102, 241, 0.75)',
                            'rgba(16, 185, 129, 0.75)'
                        ],
                        borderColor: '#18181b',
                        borderWidth: 2
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{
                            position: 'right',
                            labels: {{ color: '#a1a1aa', boxWidth: 15 }}
                        }}
                    }}
                }}
            }});

            // Chart 3: Skill Radar Map
            var ctx3 = document.getElementById('skillRadarChart').getContext('2d');
            new Chart(ctx3, {{
                type: 'radar',
                data: {{
                    labels: ['Chẩn đoán lỗi', 'Tối ưu code', 'Kiến trúc hệ thống', 'Đa luồng & Giao dịch', 'Bảo mật API'],
                    datasets: [{{
                        label: 'Chỉ số trung bình (%)',
                        data: [
                            {summary['avg_skills']['bug_hunting']},
                            {summary['avg_skills']['coding']},
                            {summary['avg_skills']['system_thinking']},
                            {summary['avg_skills']['concurrency']},
                            {summary['avg_skills']['security']}
                        ],
                        backgroundColor: 'rgba(59, 130, 246, 0.15)',
                        borderColor: 'rgba(59, 130, 246, 0.8)',
                        pointBackgroundColor: 'rgba(59, 130, 246, 1)',
                        pointBorderColor: '#fff',
                        borderWidth: 2
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{ display: false }}
                    }},
                    scales: {{
                        r: {{
                            angleLines: {{ color: '#27272a' }},
                            grid: {{ color: '#27272a' }},
                            pointLabels: {{ color: '#a1a1aa', font: {{ size: 10 }} }},
                            ticks: {{
                                backdropColor: 'transparent',
                                color: '#71717a',
                                stepSize: 20
                            }},
                            min: 0,
                            max: 100
                        }}
                    }}
                }}
            }});

            // Chart 4: Stacked Job Compatibility Rates
            var ctx4 = document.getElementById('jobMatchesChart').getContext('2d');
            new Chart(ctx4, {{
                type: 'bar',
                data: {{
                    labels: {sorted_labels},
                    datasets: [
                        {{
                            label: 'Junior (Sẵn sàng)',
                            data: {sorted_l3},
                            backgroundColor: 'rgba(16, 185, 129, 0.75)',
                            borderColor: '#18181b',
                            borderWidth: 1
                        }},
                        {{
                            label: 'Fresher',
                            data: {sorted_l2},
                            backgroundColor: 'rgba(99, 102, 241, 0.75)',
                            borderColor: '#18181b',
                            borderWidth: 1
                        }},
                        {{
                            label: 'Intern',
                            data: {sorted_l1},
                            backgroundColor: 'rgba(245, 158, 11, 0.75)',
                            borderColor: '#18181b',
                            borderWidth: 1
                        }},
                        {{
                            label: 'Chưa đạt',
                            data: {sorted_l0},
                            backgroundColor: 'rgba(239, 68, 68, 0.75)',
                            borderColor: '#18181b',
                            borderWidth: 1
                        }}
                    ]
                }},
                options: {{
                    indexAxis: 'y',
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{
                            position: 'bottom',
                            labels: {{ color: '#a1a1aa', boxWidth: 12, font: {{ size: 10 }} }}
                        }},
                        tooltip: {{
                            callbacks: {{
                                label: function(context) {{
                                    return context.dataset.label + ': ' + context.raw + '%';
                                }}
                            }}
                        }}
                    }},
                    scales: {{
                        x: {{
                            stacked: true,
                            grid: {{ color: '#27272a' }},
                            ticks: {{ color: '#a1a1aa' }},
                            min: 0,
                            max: 100
                        }},
                        y: {{
                            stacked: true,
                            grid: {{ display: false }},
                            ticks: {{ color: '#a1a1aa', font: {{ size: 10 }} }}
                        }}
                    }}
                }}
            }});
        }}
    </script>
</body>
</html>
"""
    
    with open(html_output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    print(f"Generated stunning HTML dashboard at: {html_output_path}")

if __name__ == "__main__":
    main()
